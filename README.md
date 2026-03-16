# RileyFile

GitHub mirror for Riley's canonical context system.

## Architecture

- **Canonical root**: Google Drive `My Drive/RileyContext/`
- **This repo**: Git mirror serving `RILEY_CONTEXT.md` via raw URL for agents without Google Drive access (ChatGPT, Gemini)
- **Pipeline scripts**: `scripts/` — git-tracked, executed by launchd
- **Runtime state**: `~/.rileyfile/runtime/` (sqlite, locks — local only)

## How it works

1. `sync_context.sh` runs the pipeline (index, ingest, digest, promotions, merge)
2. Pipeline reads/writes to Google Drive `RileyContext/`
3. Updated `RILEY_CONTEXT.md` is copied here and pushed to GitHub
4. Agents fetch: `https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md`
