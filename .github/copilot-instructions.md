# Copilot Instructions — RileyContext

## System Overview

**RileyContext** is Riley's canonical knowledge base system. It's a multi-agent context pipeline that ingests captures from iOS and local sources, processes them through a tagging/promotion workflow, and surfaces priority content to `RILEY_CONTEXT.md` — the single source of truth read by all AI agents.

**Canonical Root**: `~/dev/RileyContext/` (local, NOT cloud-synced)
- This folder IS the git repo (github.com/rileyfied/RileyContext)
- Claude Code works directly in this folder
- All agents read from it or its GitHub raw URL
- Runtime state lives at `~/.rileyfile/runtime/` (sqlite, state json, locks)
- iOS captures land in iCloud `_move-to-dev` folder, pipeline ingests them locally

## Architecture & Data Flow

### Three-Layer Model
1. **Ingestion** — Captures land in `CONTEXT_HUB/captures/inbox/` (iOS shortcuts, phone voice memos, manual dumps, iCloud drop folder)
2. **Processing** — `sync_context.sh` pipeline: index > ingest > digest > promotions > merge > git push
3. **Consumption** — Agents read `RILEY_CONTEXT.md` or `RILEY_INDEX.sqlite` for project/context lookups

### Pipeline Scripts (see `scripts/`)
- `sync_context.sh` — Main orchestrator, runs via launchd twice daily (8am, 10pm)
- `index_rileyfile.py` — Scans all files, builds sqlite baseline
- `ingest_captures.py` — Tags captures using domain rules + keyword rules, deduplicates via fingerprinting
- `build_digest.py` — Identifies trending captures (last 24h), flags signals
- `build_promotions.py` — Selects top digests to promote to RILEY_CONTEXT.md
- `merge_promotions.py` — Merges promotions into RILEY_CONTEXT.md under `## DAILY LOG`

### Critical Concepts
- **Metadata Sidecars**: `.meta.json` files alongside captures enable tagging without modifying originals
- **Fingerprinting**: SHA256 hashes prevent duplicate captures
- **Tag Propagation**: Captures with tags matching known projects become promotion candidates
- **Lock Mechanism**: Shell-based mutex at `~/.rileyfile/runtime/.lock/` prevents concurrent sqlite writes

## Key Workflows

### Run Full Pipeline
```bash
cd ~/dev/RileyContext/scripts
./sync_context.sh
```

### Run Digest Only (FAST Mode)
```bash
SYNC_CONTEXT_SKIP_GIT=1 SYNC_CONTEXT_FAST=1 ./sync_context.sh
```

### Path Resolution
Use environment variables:
- `RILEYFILE_ROOT` — Override root (default: ~/dev/RileyContext)
- `RILEYFILE_RUNTIME_ROOT` — Override runtime (default: ~/.rileyfile/runtime)

Scripts auto-detect or resolve via `scripts/resolve_paths.py`.

## Files to Know

| File | Purpose |
|------|---------|
| RILEY_CONTEXT.md | Canonical context, daily log. All agents read this. |
| scripts/config.json | Project definitions, paths, known hashtags, AI team. |
| scripts/sync_context.sh | Pipeline orchestrator. |
| scripts/context_hub_common.py | Shared Python utilities (path resolution, tagging, hashing). |
| MEMORY.md | Long-term context about Riley. |

## When Working Here

- **Before editing pipeline files**: Understand the full flow (ingest > digest > promote > merge).
- **Adding features**: Keep in mind double-agent runs (Claude Code + launchd). Use locks.
- **Modifying captures**: Never delete processed captures. Archive instead.
- **Adding projects**: Update `scripts/config.json` with hashtags + metadata.
- **Testing changes**: Use SYNC_CONTEXT_FAST=1 to skip expensive index step.
