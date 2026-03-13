#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import traceback
from pathlib import Path
from typing import Any

from context_hub_common import (
    canonicalize_url,
    compute_fingerprint,
    db_set_state,
    file_type_for,
    infer_tags,
    now_local,
    open_db,
    parse_meta,
    path_in_root,
    rel_to_root,
    resolve_paths,
    sha256_bytes,
    sha256_file,
)

URL_LINE_RE = re.compile(r"^https?://\S+$", re.IGNORECASE)


def normalize_explicit_tags(raw: Any) -> list[str]:
    out: list[str] = []
    if isinstance(raw, str):
        raw = raw.split()
    if not isinstance(raw, list):
        return out
    for item in raw:
        if not isinstance(item, str):
            continue
        tag = item.strip()
        if not tag:
            continue
        if not tag.startswith("#"):
            tag = f"#{tag}"
        out.append(tag.lower())
    deduped: list[str] = []
    seen = set()
    for tag in out:
        if tag in seen:
            continue
        seen.add(tag)
        deduped.append(tag)
    return deduped


def strip_html(raw: str) -> str:
    no_script = re.sub(r"<script[\\s\\S]*?</script>", " ", raw, flags=re.IGNORECASE)
    no_style = re.sub(r"<style[\\s\\S]*?</style>", " ", no_script, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", no_style)
    return re.sub(r"\\s+", " ", text).strip()


def parse_url_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".url":
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.lower().startswith("url="):
                return line.split("=", 1)[1].strip()
        return ""
    if ext == ".webloc":
        data = plistlib.loads(path.read_bytes())
        val = data.get("URL")
        return val if isinstance(val, str) else ""
    return ""


def maybe_extract_single_url_from_text(path: Path) -> str:
    if path.suffix.lower() != ".txt":
        return ""
    if path.stat().st_size > 8192:
        return ""
    body = path.read_text(encoding="utf-8", errors="ignore")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if len(lines) != 1:
        return ""
    if URL_LINE_RE.match(lines[0]):
        return lines[0]
    return ""


def extract_text(path: Path, file_type: str, out_txt: Path) -> tuple[str | None, str | None, str | None]:
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    try:
        if file_type == "text":
            raw = path.read_text(encoding="utf-8", errors="ignore")
            if path.suffix.lower() in {".html", ".htm"}:
                extracted_content = f"[RAW_HTML]\\n{raw}\\n\\n[STRIPPED_TEXT]\\n{strip_html(raw)}\\n"
            else:
                extracted_content = raw
            out_txt.write_text(extracted_content, encoding="utf-8")
            return str(out_txt), extracted_content, None

        if file_type == "url":
            url = parse_url_file(path)
            out_txt.write_text(url, encoding="utf-8")
            return str(out_txt), url, None

        if file_type == "pdf":
            tmp = out_txt.with_suffix(".tmp.txt")
            cmd = ["pdftotext", "-layout", str(path), str(tmp)]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            extracted_content = tmp.read_text(encoding="utf-8", errors="ignore")
            tmp.unlink(missing_ok=True)
            out_txt.write_text(extracted_content, encoding="utf-8")
            return str(out_txt), extracted_content, None

        return None, None, None

    except Exception as exc:
        return None, None, str(exc)


def choose_processed_destination(processed_dir: Path, original_name: str, sha: str) -> Path:
    base = processed_dir / original_name
    if not base.exists():
        return base
    stem = base.stem
    suffix = base.suffix
    candidate = processed_dir / f"{stem}__{sha[:10]}{suffix}"
    i = 1
    while candidate.exists():
        candidate = processed_dir / f"{stem}__{sha[:10]}_{i}{suffix}"
        i += 1
    return candidate


def collect_artifacts(source_root: Path) -> list[Path]:
    out: list[Path] = []
    skip_dir_names = {"_processed", "_text", ".lock"}
    for dirpath, dirnames, filenames in os.walk(source_root):
        current = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in skip_dir_names]
        for name in filenames:
            p = current / name
            if p.name.lower().endswith(".meta.json"):
                continue
            if p.name.startswith("."):
                continue
            out.append(p)
    out.sort(key=lambda p: p.as_posix())
    return out


def choose_processed_root(src: Path, roots: list[tuple[Path, Path]], default_root: Path) -> Path:
    for capture_root, processed_root in roots:
        if path_in_root(src, capture_root):
            return processed_root
    return default_root


def canonical_sha_for(src: Path, file_type: str) -> tuple[str, str | None]:
    if file_type == "url":
        raw = parse_url_file(src)
        canon = canonicalize_url(raw)
        if canon:
            return sha256_bytes(canon.encode("utf-8")), canon

    if file_type == "text":
        possible = maybe_extract_single_url_from_text(src)
        canon = canonicalize_url(possible)
        if canon:
            return sha256_bytes(canon.encode("utf-8")), canon

    return sha256_file(src), None


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest capture artifacts")
    parser.add_argument("--rileyfile-root", default=None, help="Override RileyFile root path")
    parser.add_argument("--runtime-root", default=None, help="Override local runtime root path")
    parser.add_argument("--mode", choices=["inbox", "all"], default="inbox", help="Ingest scope")
    parser.add_argument("--first-run", action="store_true", help="Alias for --mode all")
    args = parser.parse_args()

    mode = "all" if args.first_run else args.mode

    try:
        paths = resolve_paths(
            require_existing_root=True,
            riley_root=args.rileyfile_root,
            runtime_root=args.runtime_root,
        )
        conn = open_db(paths.index_sqlite)

        existing_shas = {
            row[0]
            for row in conn.execute("SELECT sha FROM files WHERE sha IS NOT NULL")
            if row and isinstance(row[0], str) and row[0]
        }

        scan_roots = paths.capture_roots if mode == "all" else paths.inbox_roots
        processed_map: list[tuple[Path, Path]] = list(zip(paths.capture_roots, paths.processed_roots))

        artifacts: list[Path] = []
        for root in scan_roots:
            if root.exists():
                artifacts.extend(collect_artifacts(root))
        artifacts.sort(key=lambda p: p.as_posix())

        run_id = now_local().strftime("%Y%m%d_%H%M%S")
        seen_this_run: set[str] = set()

        ingested = 0
        moved_duplicates = 0
        skipped_missing = 0

        for src in artifacts:
            if not src.exists() or not src.is_file():
                skipped_missing += 1
                continue

            rel_src = rel_to_root(src, paths.riley_root)
            ftype = file_type_for(src)
            dedupe_sha, canonical_url = canonical_sha_for(src, ftype)

            target_processed_root = choose_processed_root(src, processed_map, paths.captures_processed)
            target_processed_root.mkdir(parents=True, exist_ok=True)

            meta_path = src.with_name(src.name + ".meta.json")
            meta = parse_meta(meta_path)
            source_meta_rel = rel_to_root(meta_path, paths.riley_root) if meta_path.exists() else None

            if dedupe_sha in existing_shas or dedupe_sha in seen_this_run:
                # move duplicate out of inbox, but do not log/ingest again
                dup_dest = choose_processed_destination(target_processed_root, src.name, dedupe_sha)
                shutil.move(str(src), str(dup_dest))
                if meta_path.exists():
                    meta_dest = dup_dest.with_name(dup_dest.name + ".meta.json")
                    shutil.move(str(meta_path), str(meta_dest))
                moved_duplicates += 1
                continue

            explicit_tags = normalize_explicit_tags(meta.get("tags"))
            text_out = paths.captures_text / f"{dedupe_sha}.txt"

            extracted_rel = None
            extracted_for_tags = ""
            extraction_error = None

            extracted_out, extracted_body, maybe_error = extract_text(src, ftype, text_out)
            if ftype in {"text", "url", "pdf"}:
                if extracted_out:
                    extracted_rel = rel_to_root(Path(extracted_out), paths.riley_root)
                elif maybe_error:
                    extraction_error = maybe_error

            if extracted_body:
                extracted_for_tags = extracted_body[:4000]

            # If no explicit tags from meta, check if first line is hashtag-only
            # (RileyNotes convention: "#tag1 #tag2" on line 1, content below)
            if not explicit_tags and ftype == "text" and extracted_body:
                first_line = extracted_body.split("\n")[0].strip()
                tokens = first_line.split()
                if tokens and all(tok.startswith("#") for tok in tokens):
                    explicit_tags = [tok.lower() for tok in tokens]

            tags = infer_tags(
                path_rel=rel_src,
                filename=src.name,
                text=f"{meta.get('note', '')} {extracted_for_tags}",
                meta_tags=explicit_tags,
                url=canonical_url,
            )

            dest = choose_processed_destination(target_processed_root, src.name, dedupe_sha)
            shutil.move(str(src), str(dest))

            moved_meta_rel = None
            if meta_path.exists():
                meta_dest = dest.with_name(dest.name + ".meta.json")
                shutil.move(str(meta_path), str(meta_dest))
                moved_meta_rel = rel_to_root(meta_dest, paths.riley_root)

            rel_dest = rel_to_root(dest, paths.riley_root)
            now_iso = now_local().isoformat()
            st = dest.stat()

            conn.execute(
                """
                INSERT INTO files(
                    path, sha, fingerprint, size, mtime, type, first_seen, last_seen,
                    extracted_text_path, tags_json, note, source_app, captured_at, extraction_error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    sha=excluded.sha,
                    fingerprint=excluded.fingerprint,
                    size=excluded.size,
                    mtime=excluded.mtime,
                    type=excluded.type,
                    last_seen=excluded.last_seen,
                    extracted_text_path=COALESCE(excluded.extracted_text_path, files.extracted_text_path),
                    tags_json=excluded.tags_json,
                    note=COALESCE(excluded.note, files.note),
                    source_app=COALESCE(excluded.source_app, files.source_app),
                    captured_at=COALESCE(excluded.captured_at, files.captured_at),
                    extraction_error=COALESCE(excluded.extraction_error, files.extraction_error)
                """,
                (
                    rel_dest,
                    dedupe_sha,
                    compute_fingerprint(size=st.st_size, mtime=st.st_mtime),
                    st.st_size,
                    st.st_mtime,
                    ftype,
                    now_iso,
                    now_iso,
                    extracted_rel,
                    json.dumps(tags, ensure_ascii=False),
                    meta.get("note") if isinstance(meta.get("note"), str) else None,
                    meta.get("source_app") if isinstance(meta.get("source_app"), str) else None,
                    meta.get("captured_at") if isinstance(meta.get("captured_at"), str) else None,
                    extraction_error,
                ),
            )

            log_payload: dict[str, Any] = {
                "run_id": run_id,
                "processed_at": now_iso,
                "source_path": rel_src,
                "processed_path": rel_dest,
                "source_meta_path": source_meta_rel,
                "processed_meta_path": moved_meta_rel,
                "sha": dedupe_sha,
                "type": ftype,
                "tags": tags,
                "explicit_tags": explicit_tags,
                "note": meta.get("note") if isinstance(meta.get("note"), str) else "",
                "source_app": meta.get("source_app") if isinstance(meta.get("source_app"), str) else "",
                "captured_at": meta.get("captured_at") if isinstance(meta.get("captured_at"), str) else "",
                "extracted_text_path": extracted_rel,
                "extraction_error": extraction_error,
                "canonical_url": canonical_url,
            }
            with paths.ingest_log.open("a", encoding="utf-8") as logf:
                logf.write(json.dumps(log_payload, ensure_ascii=False) + "\n")

            ingested += 1
            seen_this_run.add(dedupe_sha)
            existing_shas.add(dedupe_sha)

        conn.commit()
        if mode == "all":
            db_set_state(conn, "captures_first_run_complete", "1")
            conn.commit()
        conn.close()

        print(f"scan_roots={','.join(str(p) for p in scan_roots)}")
        print(f"ingested={ingested}")
        print(f"moved_duplicates={moved_duplicates}")
        print(f"skipped_missing={skipped_missing}")
        print(f"ingest_log={paths.ingest_log}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
