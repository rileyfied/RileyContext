#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import traceback
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from context_hub_common import last_24h_cutoff, now_local, open_db, resolve_paths


def read_ingest_lines(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def top_folder(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else path


def build_signals(capture_rows: list[dict], changed_rows: list[tuple]) -> list[tuple[str, int, str]]:
    keyword_buckets = {
        "keyboard shortcuts": ["keyboard", "shortcut", "hotkey"],
        "substack links": ["substack", "nate b", "nate b. jones"],
        "video avatar clone": ["avatar", "clone", "voice clone"],
    }

    corpus = []
    for row in capture_rows:
        corpus.append(
            " ".join(
                [
                    row.get("processed_path", ""),
                    row.get("note", ""),
                    " ".join(row.get("tags", []) if isinstance(row.get("tags"), list) else []),
                    row.get("canonical_url", "") or "",
                ]
            ).lower()
        )

    for path, tags_json, *_ in changed_rows:
        txt = (path or "").lower()
        if tags_json:
            txt += " " + str(tags_json).lower()
        corpus.append(txt)

    results: list[tuple[str, int, str]] = []
    for label, words in keyword_buckets.items():
        count = sum(1 for line in corpus if any(w in line for w in words))
        if count:
            interpretation = f"You had {count} item(s) related to {label} in the last 24h."
            results.append((label, count, interpretation))

    if not results:
        tag_counter: Counter[str] = Counter()
        for row in capture_rows:
            for t in row.get("tags", []) if isinstance(row.get("tags"), list) else []:
                tag_counter[t] += 1
        for tag, count in tag_counter.most_common(3):
            results.append((tag, count, f"{count} capture(s) clustered under {tag}."))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build daily digest")
    parser.add_argument("--rileyfile-root", default=None, help="Override RileyFile root path")
    parser.add_argument("--runtime-root", default=None, help="Override local runtime root path")
    args = parser.parse_args()

    try:
        paths = resolve_paths(
            require_existing_root=True,
            riley_root=args.rileyfile_root,
            runtime_root=args.runtime_root,
        )
        conn = open_db(paths.index_sqlite)
        ingest_rows = read_ingest_lines(paths.ingest_log)

        now = now_local()
        cutoff = last_24h_cutoff()
        today = now.date()

        new_captures: list[dict] = []
        for row in ingest_rows:
            dt = parse_dt(row.get("captured_at")) or parse_dt(row.get("processed_at"))
            if dt and dt.astimezone().date() == today:
                new_captures.append(row)

        changed_rows = conn.execute(
            """
            SELECT path, tags_json, note, source_app, captured_at
            FROM files
            WHERE datetime(mtime, 'unixepoch') >= datetime(?)
              AND path NOT LIKE 'CONTEXT_HUB/captures/%'
              AND path NOT LIKE 'RileyShare/captures/%'
              AND path NOT LIKE 'CONTEXT_HUB/context/_daily_digest/%'
            ORDER BY mtime DESC
            """,
            (cutoff.astimezone().strftime("%Y-%m-%d %H:%M:%S"),),
        ).fetchall()

        by_folder: dict[str, list[str]] = defaultdict(list)
        for path, *_ in changed_rows:
            by_folder[top_folder(path)].append(path)

        signals = build_signals(new_captures, changed_rows)

        lines: list[str] = []
        lines.append(f"# Riley Daily Digest — {today.isoformat()}")
        lines.append("")

        lines.append("## New Captures")
        if new_captures:
            for row in new_captures:
                tags = " ".join(row.get("tags", [])[:6]) if isinstance(row.get("tags"), list) else ""
                note = row.get("note", "")
                line = f"- `{row.get('processed_path', '')}`"
                if tags:
                    line += f" {tags}"
                if note:
                    line += f" — {note}"
                lines.append(line)
        else:
            lines.append("- No new captures today.")
        lines.append("")

        lines.append("## Changed Files Elsewhere in RileyFile")
        if by_folder:
            for folder in sorted(by_folder.keys()):
                lines.append(f"### {folder}")
                for p in by_folder[folder][:10]:
                    lines.append(f"- `{p}`")
        else:
            lines.append("- No non-capture file changes detected in the last 24h.")
        lines.append("")

        lines.append("## Signals")
        if signals:
            for label, count, text in signals:
                lines.append(f"- {label}: {count}")
                lines.append(f"  - {text}")
        else:
            lines.append("- No strong clusters detected today.")
        lines.append("")

        lines.append("## Suggested Next Actions")
        prompts: list[str] = []
        for label, _, _ in signals[:3]:
            prompts.append(f"- Should we promote today's {label} captures into project context?")
        if not prompts:
            prompts = [
                "- Do you want to tag today’s untagged captures for project routing?",
                "- Should we promote any _to_context items now?",
            ]
        lines.extend(prompts[:5])
        lines.append("")

        out_path = paths.digest_dir / f"{today.isoformat()}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

        print(f"digest_path={out_path}")
        print(f"new_captures={len(new_captures)}")
        print(f"changed_elsewhere={len(changed_rows)}")
        conn.close()
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
