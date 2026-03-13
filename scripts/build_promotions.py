#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import traceback
from collections import defaultdict
from pathlib import Path

from context_hub_common import KNOWN_PROJECT_HASHTAGS, resolve_paths


def read_log(path: Path) -> list[dict]:
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


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"offset": 0}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"offset": 0}


def save_state(path: Path, offset: int) -> None:
    path.write_text(json.dumps({"offset": offset}, indent=2) + "\n", encoding="utf-8")


def first_project_tag(tags: list[str]) -> str | None:
    for t in tags:
        if t.lower() in KNOWN_PROJECT_HASHTAGS:
            return t.lower()
    return None


def is_forced_context(entry: dict) -> bool:
    src = str(entry.get("source_path", "")).lower()
    dst = str(entry.get("processed_path", "")).lower()
    return "_to_context/" in src or "_to_context/" in dst


def to_candidates_markdown(entries: list[dict]) -> str:
    lines = ["# Context Candidates", ""]
    if not entries:
        lines.append("- No new ingest entries.")
        return "\n".join(lines).rstrip() + "\n"

    for entry in entries:
        tags = entry.get("tags", []) if isinstance(entry.get("tags"), list) else []
        lines.append(f"## `{entry.get('processed_path', '')}`")
        lines.append(f"- sha: `{entry.get('sha', '')}`")
        lines.append(f"- tags: {' '.join(tags) if tags else '(none)'}")
        lines.append(f"- note: {entry.get('note', '') or '(none)'}")
        lines.append(f"- source_app: {entry.get('source_app', '') or '(unknown)'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def promotion_block(entry: dict, tag: str) -> str:
    path = entry.get("processed_path", "")
    tags = entry.get("tags", []) if isinstance(entry.get("tags"), list) else []
    note = entry.get("note", "") or "No note provided."
    source_app = entry.get("source_app", "") or "Unknown"
    captured_at = entry.get("captured_at", "") or entry.get("processed_at", "") or "Unknown"
    sha = entry.get("sha", "")

    bullets = [
        f"- Capture path: `{path}`",
        f"- Captured at: {captured_at}",
        f"- Source app: {source_app}",
        f"- Note: {note}",
        f"- Inferred tags: {' '.join(tags) if tags else '(none)'}",
    ]

    lines = [f"### {tag}", *bullets, f"[context_ingest_sha={sha}]", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build candidates and promotions")
    parser.add_argument("--rileyfile-root", default=None, help="Override RileyFile root path")
    parser.add_argument("--runtime-root", default=None, help="Override local runtime root path")
    args = parser.parse_args()

    try:
        paths = resolve_paths(
            require_existing_root=True,
            riley_root=args.rileyfile_root,
            runtime_root=args.runtime_root,
        )

        entries = read_log(paths.ingest_log)
        state = load_state(paths.promotions_state)
        offset = int(state.get("offset", 0))
        offset = max(0, min(offset, len(entries)))
        new_entries = entries[offset:]

        paths.candidates_md.write_text(to_candidates_markdown(new_entries), encoding="utf-8")

        grouped: dict[str, list[dict]] = defaultdict(list)
        for entry in new_entries:
            explicit_tags = [
                str(t).lower()
                for t in (entry.get("explicit_tags", []) if isinstance(entry.get("explicit_tags"), list) else [])
            ]
            tag = explicit_tags[0] if explicit_tags else first_project_tag(
                [str(t).lower() for t in (entry.get("tags", []) if isinstance(entry.get("tags"), list) else [])]
            )
            in_to_context = is_forced_context(entry)
            if tag or in_to_context:
                grouped[tag or "#general"].append(entry)

        promotion_lines = ["# Context Promotions", ""]
        if grouped:
            for tag in sorted(grouped.keys()):
                for entry in grouped[tag]:
                    promotion_lines.append(promotion_block(entry, tag))
        else:
            promotion_lines.append("- No promotion-eligible entries this run.")
        paths.promotions_md.write_text("\n".join(promotion_lines).rstrip() + "\n", encoding="utf-8")

        save_state(paths.promotions_state, len(entries))

        print(f"candidates_written={paths.candidates_md}")
        print(f"promotions_written={paths.promotions_md}")
        print(f"new_entries={len(new_entries)}")
        print(f"promotion_entries={sum(len(v) for v in grouped.values())}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
