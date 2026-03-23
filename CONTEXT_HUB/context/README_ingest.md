# Context Hub Ingest Guide

## Runtime vs Canonical Storage

Canonical content remains at `RILEYFILE_ROOT` (defaults to `~/dev/RileyContext/`):
- `RILEY_CONTEXT.md`
- `CONTEXT_HUB/context/_ingest_log.ndjson`
- `CONTEXT_HUB/context/_daily_digest/YYYY-MM-DD.md`
- `CONTEXT_HUB/context/_candidates.md`
- `CONTEXT_HUB/context/_promotions.md`
- `CONTEXT_HUB/context/_archive/`

Local runtime state lives outside the repo:
- `RILEY_INDEX.sqlite`
- `.state.json`
- `.promotions_state.json`
- sync lock directory

Runtime root resolution order:
1. `--runtime-root <PATH>`
2. `RILEYFILE_RUNTIME_ROOT`
3. `$XDG_DATA_HOME/rileyfile/runtime`
4. `~/.rileyfile/runtime`

## Watched capture inboxes
Every pipeline run watches:
- `RileyContext/CONTEXT_HUB/captures/inbox/`
- `RileyContext/RileyShare/captures/inbox/` (if this folder exists)

Before inbox scan, the pipeline also pulls files from:
- iCloud `_move-to-dev_icloud` folder (iOS captures)
- Google Drive `move-to-dev_google-drive` folder

## First full ingest behavior
On first full ingest (`.state.json` missing or `full_ingest_completed=false`), the runner does:
1. Full RileyContext index baseline.
2. Full ingest from both capture roots:
- `RileyContext/CONTEXT_HUB/captures/`
- `RileyContext/RileyShare/captures/` (if exists)
3. Digest + candidates + promotions + merge.
4. Writes runtime state:

```json
{
  "full_ingest_completed": true,
  "completed_at": "...",
  "index_version": 3
}
```

## FAST mode
FAST mode skips indexing and only ingests inboxes + digest/promotions/merge.

```bash
SYNC_CONTEXT_SKIP_GIT=1 \
SYNC_CONTEXT_FAST=1 \
./scripts/sync_context.sh
```

## Runtime paths
With defaults, runtime files are in:
- `~/.rileyfile/runtime/index/RILEY_INDEX.sqlite`
- `~/.rileyfile/runtime/context/.state.json`
- `~/.rileyfile/runtime/context/.promotions_state.json`
- `~/.rileyfile/runtime/.lock/`

## Metadata sidecar
For any file `example.ext`, optional sidecar:
`example.ext.meta.json`

```json
{
  "tags": ["#youtube", "#aibrief"],
  "note": "why I saved this",
  "source_app": "Chrome iOS",
  "captured_at": "2026-02-27T10:15:00-05:00"
}
```

Promotion eligibility:
- Explicit known project hashtag in `tags`, or
- File originated from any `_to_context/` path.

## Direct script usage
```bash
python3 scripts/resolve_paths.py --rileyfile-root ~/dev/RileyContext --runtime-root ~/.rileyfile/runtime
python3 scripts/ingest_captures.py --rileyfile-root ~/dev/RileyContext --runtime-root ~/.rileyfile/runtime --mode inbox
python3 scripts/ingest_captures.py --rileyfile-root ~/dev/RileyContext --runtime-root ~/.rileyfile/runtime --mode all
python3 scripts/build_digest.py --rileyfile-root ~/dev/RileyContext --runtime-root ~/.rileyfile/runtime
python3 scripts/build_promotions.py --rileyfile-root ~/dev/RileyContext --runtime-root ~/.rileyfile/runtime
python3 scripts/merge_promotions.py --rileyfile-root ~/dev/RileyContext --runtime-root ~/.rileyfile/runtime
```

## Break-Glass Writer Path (Claude unavailable)
Use this only when Claude is unavailable and keep append-only semantics.

1. Create a timestamped markdown drop file with source label (`GPT`, `CLAUDE`, or `GEM`).
2. Append it under `## DAILY LOG` in `RILEY_CONTEXT.md` with a clear timestamp header.
3. Do not rewrite or reorder prior log entries.
4. Commit only the intended context changes with a clear message (`chore: append daily log ...`).
5. Push to `main` and record the commit hash in team handoff notes.

## Rollback Runbook
If bad context lands in `main`:

1. Identify bad commit:
```bash
git log --oneline -- RILEY_CONTEXT.md CONTEXT_HUB/context
```
2. Revert commit (non-destructive history):
```bash
git revert <bad_commit_hash>
```
3. Push revert:
```bash
git push
```
4. Rebuild runtime index/state from current repo content:
```bash
rm -f "$HOME/.rileyfile/runtime/index/RILEY_INDEX.sqlite"
rm -f "$HOME/.rileyfile/runtime/context/.state.json"
rm -f "$HOME/.rileyfile/runtime/context/.promotions_state.json"
SYNC_CONTEXT_SKIP_GIT=1 ./scripts/sync_context.sh
```

If shell safety policy blocks `rm -f` in your environment, delete the same runtime files using the platform-approved file edit/delete path, then run the sync command above.
