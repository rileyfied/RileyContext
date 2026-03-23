# RileyContext Index
Last updated: 2026-03-16

## Root Files
| File | Purpose |
|------|---------|
| RILEY_CONTEXT.md | Canonical context — projects, preferences, activity log. Read by all agents. |
| README.md | Quick-start overview |
| INDEX.md | This file — folder map |
| MEMORY.md | Long-term context about Riley |

## Folder Structure

### AgentConfigs/
Per-agent handshake files. Each agent reads its file at session start.
- CHATGPT.md, GEMINI.md, SIDER.md

### AI BRIEFS/
Daily AI audio brief production files — scripts, audio, PDFs, NotebookLM outputs.
- DESCRIPT/ — audio editing exports
- NOTEBOOKLM/ — generated audio overviews
- SRIPTS & NOTES/ — brief scripts and research

### CONTEXT_HUB/
Pipeline-managed content. Do not manually edit pipeline-generated files.
- captures/inbox/ — new captures land here (phone, shortcuts, manual)
- captures/_processed/ — captures after pipeline processes them
- captures/_text/ — extracted text from captures
- context/ — pipeline outputs (digests, promotions, candidates, logs)
- index/ — sqlite index of all files
- scripts/ — pipeline helper scripts

### RileyAgents/
AI memory archives — exported memories from each platform.
- CLAUDE MEMORY ARCHIVE/
- ChatGPT MEMORY ARCHIVE/
- BROWSER BOOKMARKS/

### RileyProjects/
All active and queued projects.
- ARMOR APP/ — Scripture memorization app (blueprint + data sets)
- CFA/ — Chick-fil-A ops (Training, Schedule, Office, Branding)
- GoogleAIStudio/ — AI Studio experiments and app prototypes
- NoLimitLeaderboard/ — Leaderboard project
- Opal/ — Opal app experiments
- Piano/ — Sheet music, practice resources, NotebookLM
- RILEY API/ — Personal API concept
- RileyClone/ — AI clone/persona project
- YOUTUBE CHANNEL/ — Video production, scripts, plans
- _misc/ — Standalone docs (Faceless Bible Videos, Second Brain, TikTok proposals, etc.)

### scripts/
Pipeline scripts and configuration.
- sync_context.sh — main pipeline runner
- config.json — project definitions, paths, AI team, sync settings
- CONTEXT_SYNC_SETUP.md — how /context works across all AI tools
- Python scripts for ingest, indexing, digests, promotions

## Active Hashtags
#youtube #video #ai #7shifts #schedule #armor #scripture #fighterverses #cfa #training #carspotter #aibrief #piano #harmony #conductor #dashboard #virtualmanager #rileyfied

## Current Priorities (March 2026)
1. YouTube Channel — Video #1 ready to film
2. 7shifts Scheduling — automation in progress
3. Armor App — blueprint + data ready
4. Car Spotter Training Arcade — design phase
5. Daily AI Brief — ongoing
6. Piano — learning + app queued
