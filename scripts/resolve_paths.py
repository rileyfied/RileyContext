#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import traceback

from context_hub_common import resolve_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve and verify Context Hub paths")
    parser.add_argument("--json", action="store_true", help="Print resolved paths as JSON")
    parser.add_argument("--rileyfile-root", default=None, help="Override RileyFile root path")
    parser.add_argument("--runtime-root", default=None, help="Override local runtime root path")
    args = parser.parse_args()

    try:
        resolved = resolve_paths(
            require_existing_root=True,
            riley_root=args.rileyfile_root,
            runtime_root=args.runtime_root,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1

    payload = resolved.as_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for k, v in payload.items():
            print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
