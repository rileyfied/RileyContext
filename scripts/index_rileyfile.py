#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import traceback
from pathlib import Path

from context_hub_common import (
    compute_fingerprint,
    file_type_for,
    infer_tags,
    list_files_for_index,
    now_local,
    open_db,
    parse_meta,
    rel_to_root,
    resolve_paths,
    sha256_file,
)

HASH_EXTENSIONS = {".md", ".txt", ".json", ".html", ".htm", ".pdf", ".url", ".webloc"}
HASH_PREFIXES = ("CONTEXT_HUB/", "RileyShare/captures/")


def sidecar_for(path: Path) -> Path:
    return path.with_name(path.name + ".meta.json")


def should_hash(rel_path: str, ext: str) -> bool:
    if ext in HASH_EXTENSIONS:
        return True
    return any(rel_path.startswith(prefix) for prefix in HASH_PREFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description="Index RileyFile tree into sqlite")
    parser.add_argument("--rileyfile-root", default=None, help="Override RileyFile root path")
    parser.add_argument("--runtime-root", default=None, help="Override local runtime root path")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=int(os.environ.get("INDEX_PROGRESS_EVERY", "250")),
        help="Print progress every N files",
    )
    args = parser.parse_args()

    try:
        paths = resolve_paths(
            require_existing_root=True,
            riley_root=args.rileyfile_root,
            runtime_root=args.runtime_root,
        )
        conn = open_db(paths.index_sqlite)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=5000;")

        existing_rows = {
            row[0]: {
                "sha": row[1],
                "fingerprint": row[2],
                "size": row[3],
                "mtime": row[4],
                "first_seen": row[5],
                "extracted_text_path": row[6],
            }
            for row in conn.execute(
                "SELECT path, sha, fingerprint, size, mtime, first_seen, extracted_text_path FROM files"
            )
        }

        files = list_files_for_index(paths.riley_root)
        total = len(files)

        indexed = 0
        hashed = 0
        fingerprint_only = 0
        reused = 0
        now_iso = now_local().isoformat()

        for i, abs_path in enumerate(files, start=1):
            rel_path = rel_to_root(abs_path, paths.riley_root)
            if rel_path.startswith("CONTEXT_HUB/captures/_text/"):
                continue

            st = abs_path.stat()
            size = st.st_size
            mtime = st.st_mtime
            fingerprint = compute_fingerprint(size=size, mtime=mtime)
            meta = parse_meta(sidecar_for(abs_path))
            existing = existing_rows.get(rel_path)

            unchanged = bool(existing and existing.get("fingerprint") == fingerprint)
            ext = abs_path.suffix.lower()
            do_hash = should_hash(rel_path, ext)

            if unchanged:
                sha = existing.get("sha")
                reused += 1
            else:
                if do_hash:
                    sha = sha256_file(abs_path)
                    hashed += 1
                else:
                    sha = None
                    fingerprint_only += 1

            filename = abs_path.name
            tags = infer_tags(
                path_rel=rel_path,
                filename=filename,
                text=(meta.get("note") or ""),
                meta_tags=meta.get("tags") if isinstance(meta.get("tags"), list) else None,
            )

            first_seen = existing.get("first_seen") if existing else now_iso
            extracted_text_path = existing.get("extracted_text_path") if existing else None

            conn.execute(
                """
                INSERT INTO files(
                    path, sha, fingerprint, size, mtime, type, first_seen, last_seen,
                    extracted_text_path, tags_json, note, source_app, captured_at, extraction_error
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    sha=excluded.sha,
                    fingerprint=excluded.fingerprint,
                    size=excluded.size,
                    mtime=excluded.mtime,
                    type=excluded.type,
                    last_seen=excluded.last_seen,
                    tags_json=excluded.tags_json,
                    note=COALESCE(excluded.note, files.note),
                    source_app=COALESCE(excluded.source_app, files.source_app),
                    captured_at=COALESCE(excluded.captured_at, files.captured_at),
                    extracted_text_path=COALESCE(files.extracted_text_path, excluded.extracted_text_path),
                    extraction_error=COALESCE(files.extraction_error, excluded.extraction_error)
                """,
                (
                    rel_path,
                    sha,
                    fingerprint,
                    size,
                    mtime,
                    file_type_for(abs_path),
                    first_seen,
                    now_iso,
                    extracted_text_path,
                    json.dumps(tags, ensure_ascii=False),
                    meta.get("note") if isinstance(meta.get("note"), str) else None,
                    meta.get("source_app") if isinstance(meta.get("source_app"), str) else None,
                    meta.get("captured_at") if isinstance(meta.get("captured_at"), str) else None,
                    None,
                ),
            )
            indexed += 1

            if args.progress_every > 0 and i % args.progress_every == 0:
                print(f"progress={i}/{total} current={rel_path}")

        conn.commit()
        conn.close()

        print(f"scan_roots={paths.riley_root}")
        print(f"indexed_files={indexed}")
        print(f"hashed_files={hashed}")
        print(f"fingerprint_only_files={fingerprint_only}")
        print(f"reused_entries={reused}")
        print(f"index_path={paths.index_sqlite}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
