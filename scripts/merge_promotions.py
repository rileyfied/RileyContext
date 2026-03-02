#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import traceback
from datetime import datetime

from context_hub_common import resolve_paths

SECTION_HEADER = "## PROJECT CONTEXT PROMOTIONS"


def parse_promotion_blocks(text: str) -> list[tuple[str, str, str]]:
    lines = text.splitlines()
    blocks: list[tuple[str, str, str]] = []
    current_tag = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current_tag, buf
        if not current_tag or not buf:
            current_tag = None
            buf = []
            return
        block_text = "\n".join(buf).strip() + "\n"
        m = re.search(r"\[context_ingest_sha=([a-f0-9]{64})\]", block_text)
        if m:
            blocks.append((current_tag, m.group(1), block_text))
        current_tag = None
        buf = []

    for line in lines:
        if line.startswith("### "):
            flush()
            current_tag = line[4:].strip()
            buf = [line]
        elif current_tag:
            buf.append(line)

    flush()
    return blocks


def merge_into_context(context_text: str, blocks: list[tuple[str, str, str]]) -> tuple[str, int]:
    if not blocks:
        return context_text, 0

    deduped: list[str] = []
    for _, sha, block in blocks:
        if f"[context_ingest_sha={sha}]" in context_text:
            continue
        deduped.append(block.strip())

    if not deduped:
        return context_text, 0

    insert_blob = "\n\n".join(deduped).rstrip() + "\n"

    if SECTION_HEADER not in context_text:
        marker = "\n## DAILY LOG"
        if marker in context_text:
            idx = context_text.index(marker)
            prefix = context_text[:idx].rstrip()
            suffix = context_text[idx:]
            merged = f"{prefix}\n\n{SECTION_HEADER}\n\n{insert_blob}\n{suffix.lstrip()}"
        else:
            merged = context_text.rstrip() + f"\n\n{SECTION_HEADER}\n\n{insert_blob}\n"
        return merged, len(deduped)

    start = context_text.index(SECTION_HEADER)
    next_section_idx = context_text.find("\n## ", start + len(SECTION_HEADER))
    if next_section_idx == -1:
        section = context_text[start:].rstrip()
        merged_section = section + "\n\n" + insert_blob
        merged = context_text[:start] + merged_section + "\n"
    else:
        section = context_text[start:next_section_idx].rstrip()
        merged_section = section + "\n\n" + insert_blob + "\n"
        merged = context_text[:start] + merged_section + context_text[next_section_idx:]

    return merged, len(deduped)


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge promotion blocks into RILEY_CONTEXT.md")
    parser.add_argument("--rileyfile-root", default=None, help="Override RileyFile root path")
    parser.add_argument("--runtime-root", default=None, help="Override local runtime root path")
    args = parser.parse_args()

    try:
        paths = resolve_paths(
            require_existing_root=True,
            riley_root=args.rileyfile_root,
            runtime_root=args.runtime_root,
        )

        promo_text = paths.promotions_md.read_text(encoding="utf-8", errors="ignore") if paths.promotions_md.exists() else ""
        blocks = parse_promotion_blocks(promo_text)

        context_text = paths.riley_context.read_text(encoding="utf-8")
        merged_text, merged_count = merge_into_context(context_text, blocks)

        if merged_count > 0:
            paths.riley_context.write_text(merged_text, encoding="utf-8")
            stamp = datetime.now().strftime("%Y%m%d_%H%M")
            archive_path = paths.archive_dir / f"promotions_{stamp}.md"
            archive_path.write_text(promo_text.rstrip() + "\n", encoding="utf-8")

        paths.promotions_md.write_text("# Context Promotions\n\n- No pending promotions.\n", encoding="utf-8")

        print(f"merged_blocks={merged_count}")
        print(f"context_path={paths.riley_context}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
