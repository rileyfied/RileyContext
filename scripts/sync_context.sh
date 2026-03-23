#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Missing dependency: python3"
  echo "Install suggestion: brew install python"
  exit 1
fi

if ! python3 - <<'PY' >/dev/null 2>&1
import sqlite3
PY
then
  echo "Missing dependency: sqlite (python sqlite3 module)"
  echo "Install suggestion: brew install sqlite"
  exit 1
fi

if ! command -v pdftotext >/dev/null 2>&1; then
  echo "Missing dependency: pdftotext"
  echo "Install suggestion: brew install poppler"
  exit 1
fi

RESOLVE_ARGS=()
if [[ -n "${RILEYFILE_ROOT:-}" ]]; then
  RESOLVE_ARGS+=(--rileyfile-root "$RILEYFILE_ROOT")
fi
if [[ -n "${RILEYFILE_RUNTIME_ROOT:-}" ]]; then
  RESOLVE_ARGS+=(--runtime-root "$RILEYFILE_RUNTIME_ROOT")
fi

if (( ${#RESOLVE_ARGS[@]} > 0 )); then
  PATH_JSON="$(python3 "$SCRIPT_DIR/resolve_paths.py" --json "${RESOLVE_ARGS[@]}")"
else
  PATH_JSON="$(python3 "$SCRIPT_DIR/resolve_paths.py" --json)"
fi
RILEY_ROOT="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["riley_root"])')"
RUNTIME_ROOT="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["runtime_root"])')"
LOCK_DIR="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["lock_dir"])')"
STATE_JSON="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["state_json"])')"
CAPTURE_ROOTS_CSV="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(",".join(d.get("capture_roots", [])))')"
INBOX_ROOTS_CSV="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(",".join(d.get("inbox_roots", [])))')"

# --- single-instance lock (prevents concurrent sqlite writes) ---
LOCK_TTL_SECONDS="${LOCK_TTL_SECONDS:-3600}"

acquire_lock() {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    date +%s > "$LOCK_DIR/started_epoch"
    echo "$$" > "$LOCK_DIR/pid"
    return 0
  fi

  if [[ -f "$LOCK_DIR/started_epoch" ]]; then
    local started now age
    started="$(cat "$LOCK_DIR/started_epoch" 2>/dev/null || echo 0)"
    now="$(date +%s)"
    age=$(( now - started ))
    if (( age > LOCK_TTL_SECONDS )); then
      echo "Stale lock detected (age=${age}s). Removing and retrying..."
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR" 2>/dev/null || { echo "Lock busy; exiting."; exit 3; }
      date +%s > "$LOCK_DIR/started_epoch"
      echo "$$" > "$LOCK_DIR/pid"
      return 0
    fi
  fi

  echo "Another sync_context run is in progress. Exiting."
  exit 3
}

release_lock() {
  rm -rf "$LOCK_DIR" 2>/dev/null || true
}

acquire_lock
trap release_lock EXIT INT TERM
# --- end lock ---

FULL_INGEST_COMPLETED="$(python3 - <<PY
import json, pathlib
p = pathlib.Path(r'''$STATE_JSON''')
if not p.exists():
    print('0')
else:
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        print('1' if data.get('full_ingest_completed') is True else '0')
    except Exception:
        print('0')
PY
)"

write_state() {
  python3 - <<PY
import json, pathlib, datetime
p = pathlib.Path(r'''$STATE_JSON''')
p.parent.mkdir(parents=True, exist_ok=True)
data = {
  "full_ingest_completed": True,
  "completed_at": datetime.datetime.now().astimezone().isoformat(),
  "index_version": 3,
}
p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
}

COMMON_ARGS=(--rileyfile-root "$RILEY_ROOT" --runtime-root "$RUNTIME_ROOT")
echo "runtime_root=$RUNTIME_ROOT"

# --- pull files from iCloud drop folder into local inbox ---
LOCAL_INBOX="$RILEY_ROOT/CONTEXT_HUB/captures/inbox"

# Pull from iCloud drop folder
ICLOUD_DROP="$HOME/Library/Mobile Documents/com~apple~CloudDocs/_move-to-dev_icloud"
if [[ -d "$ICLOUD_DROP" ]]; then
  find "$ICLOUD_DROP" -maxdepth 1 -type f ! -name '.DS_Store' ! -name '.*' 2>/dev/null | while read -r f; do
    fname="$(basename "$f")"
    mv "$f" "$LOCAL_INBOX/$fname" 2>/dev/null && echo "icloud_pull: $fname"
  done
  echo "icloud_drop=scanned"
else
  echo "icloud_drop=not_found"
fi

# Pull from Google Drive drop folder
GDRIVE_DROP="$HOME/Library/CloudStorage/GoogleDrive-grahamedelweiss@gmail.com/My Drive/move-to-dev_google-drive"
if [[ -d "$GDRIVE_DROP" ]]; then
  find "$GDRIVE_DROP" -maxdepth 1 -type f ! -name '.DS_Store' ! -name '.*' ! -name '*.gdoc' ! -name '*.gsheet' ! -name '*.gslides' 2>/dev/null | while read -r f; do
    fname="$(basename "$f")"
    mv "$f" "$LOCAL_INBOX/$fname" 2>/dev/null && echo "gdrive_pull: $fname"
  done
  echo "gdrive_drop=scanned"
else
  echo "gdrive_drop=not_found"
fi

if [[ "$FULL_INGEST_COMPLETED" != "1" ]]; then
  echo "run_mode=full_baseline"
  echo "scan_roots=$CAPTURE_ROOTS_CSV"

  python3 "$SCRIPT_DIR/index_rileyfile.py" "${COMMON_ARGS[@]}"
  python3 "$SCRIPT_DIR/ingest_captures.py" "${COMMON_ARGS[@]}" --mode all
  python3 "$SCRIPT_DIR/build_digest.py" "${COMMON_ARGS[@]}"
  python3 "$SCRIPT_DIR/build_promotions.py" "${COMMON_ARGS[@]}"
  python3 "$SCRIPT_DIR/merge_promotions.py" "${COMMON_ARGS[@]}"
  write_state
else
  if [[ "${SYNC_CONTEXT_FAST:-0}" == "1" ]]; then
    echo "run_mode=fast_inbox"
    echo "scan_roots=$INBOX_ROOTS_CSV"

    python3 "$SCRIPT_DIR/ingest_captures.py" "${COMMON_ARGS[@]}" --mode inbox
    python3 "$SCRIPT_DIR/build_digest.py" "${COMMON_ARGS[@]}"
    python3 "$SCRIPT_DIR/build_promotions.py" "${COMMON_ARGS[@]}"
    python3 "$SCRIPT_DIR/merge_promotions.py" "${COMMON_ARGS[@]}"
  else
    echo "run_mode=incremental"
    echo "scan_roots=$INBOX_ROOTS_CSV"

    python3 "$SCRIPT_DIR/index_rileyfile.py" "${COMMON_ARGS[@]}"
    python3 "$SCRIPT_DIR/ingest_captures.py" "${COMMON_ARGS[@]}" --mode inbox
    python3 "$SCRIPT_DIR/build_digest.py" "${COMMON_ARGS[@]}"
    python3 "$SCRIPT_DIR/build_promotions.py" "${COMMON_ARGS[@]}"
    python3 "$SCRIPT_DIR/merge_promotions.py" "${COMMON_ARGS[@]}"
  fi
fi

# --- commit & push RILEY_CONTEXT.md to GitHub ---
if [[ "${SYNC_CONTEXT_SKIP_GIT:-0}" == "1" ]]; then
  echo "Skipping git commit/push (SYNC_CONTEXT_SKIP_GIT=1)"
  exit 0
fi

if [[ ! -d "$RILEY_ROOT/.git" ]]; then
  echo "No git repo at $RILEY_ROOT, skipping commit/push"
  exit 0
fi

cd "$RILEY_ROOT"

git add RILEY_CONTEXT.md
if git diff --cached --quiet -- RILEY_CONTEXT.md; then
  echo "No git changes to commit"
  exit 0
fi

git commit -m "chore: sync context hub $(date '+%Y-%m-%d %H:%M')"
git push
