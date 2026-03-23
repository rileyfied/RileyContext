---

## SYNC PROTOCOL v4 (ACTIVE)

Canonical Source of Truth:
- Local: `~/dev/RileyContext/` (this IS the git repo)
- NOT cloud-synced. No iCloud, no Google Drive for canonical storage.
- GitHub: `rileyfied/RileyContext` — auto-pushed by pipeline for remote agent access.
- Raw URL: https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md

Who Can Write:
- Claude Code (laptop or desktop) runs the pipeline and writes RILEY_CONTEXT.md.
- Phone captures drop into iCloud `_move-to-dev_icloud` folder, pipeline pulls them to local inbox.

Runtime State (local-only, not synced):
- `~/.rileyfile/runtime/` — sqlite index, state json, lock files.

Deprecated Systems:
- iCloud as canonical root (caused deadlocks)
- Google Drive as canonical root (caused file locking OSError 11)
- `~/dev/rileyfile/` as separate git mirror (merged into RileyContext)
- GitHub repo name `rileyfied/rileyfile` (renamed to `rileyfied/RileyContext`)

---

# RILEY_CONTEXT.md
## Last Updated: 2026-03-23

> **Purpose**: Context reference for Riley's projects, preferences, and active work. Read by all AI agents.
> **Canonical**: `~/dev/RileyContext/RILEY_CONTEXT.md` (local)
> **Remote**: https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md (GPT, Gemini, Codex, Sider)

---

## CONTEXT HUB STATUS (2026-03-23)

- Context Hub v4 — local-first architecture. Canonical root at `~/dev/RileyContext/`.
- Runtime/content split is live:
  - Runtime state uses local path (`~/.rileyfile/runtime`).
  - All content lives locally in `~/dev/RileyContext/`. GitHub is the distribution mirror.
- Launchd scheduling is active:
  - `com.rileyfile.sync_context` runs twice daily (8am and 10pm) and executes: pull drop folders > index > ingest > digest > promotions > merge > commit > push.
- iOS captures: land in iCloud `_move-to-dev_icloud`, pipeline pulls to local inbox each run.
- Google Drive captures: land in `move-to-dev_google-drive`, pipeline pulls to local inbox each run.

---

## WHO IS RILEY

Entrepreneur, content creator, restaurant operations leader (Chick-fil-A). Building in the AI space while working full-time. "Multi-channel dumper" — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time.

**Communication**: Direct, efficient. No excessive formatting. Hashtags over folders. Context over structure. Show don't tell.

**Design eye**: Clean, minimal, non-generic. Gets distracted by formatting options — keep UI stripped down.

---

## ACTIVE PROJECTS (Priority Order)

**1. YouTube Channel** — #youtube #video #ai #tutorial
AI tools for non-technical audiences. First video: "You're Using AI Wrong." Target: frontline operational managers, not enterprise knowledge workers. Style refs: Nate B. Jones, Fireship, Igor Pogany.
Resources: `RileyProjects/YOUTUBE CHANNEL`

**2. 7shifts Scheduling** — #7shifts #schedule #cfa
Automating CFA schedule creation. Brain dumps captured about rotating minors, catering team scheduling, Claude-powered schedule generation.
Resources: `RileyProjects/CFA/Schedule`

**3. Daily AI Audio Brief** — #aibrief #audio #news
15-20 min solo-narration briefings on breaking AI news. Sources: The Rundown AI, Ben's Bites, TechCrunch AI, arXiv, X/Reddit. NotebookLM format with copy/paste-ready blocks.

**4. Armor App** — #armor #scripture #bible #fighterverses
Scripture memorization with gamified 5-mechanic ladder (Word Bank > Word Scramble > Type 1st Letter > Type Full Word > Recite). Fighter Verses data sets A-E ready. Full blueprint exists at `RileyProjects/ARMOR APP/`.
Resources: `RileyProjects/ARMOR APP`

**5. Car Spotter Training Arcade** — #carspotter #cfa #training
Multi-game car logo quiz for CFA drive-thru team. Design phase.
Resources: `RileyProjects/CFA/Training`

**6. HarmonyHelper** — #harmony #piano #music #chords
Piano practice app. Python backend, web frontend.
Resources: `RileyProjects/Piano`

**7. AI Operations Monitor** — #conductor #monitor #agents
Local agent that watches AI processes on machine, reports costs, flags waste, eventually orchestrates which AI does what. Vision: non-technical conductor for AI workflows. PWA prototype first.

**8. Dashboard App (RileyHQ)** — #dashboard #productivity
Command center for all projects. Zero manual maintenance. Design discovery phase.

**9. Virtual Restaurant Manager** — #virtualmanager #visor #cfa
Knowledge base agent for restaurant operations. All roles in one place — owner, managers, vendors, HR, etc. Multi-year vision. Concept documented.

---

## RILEYDOMAIN STRUCTURE

```
~/dev/RileyContext/
├── RILEY_CONTEXT.md        <- Canonical context file (read by all agents)
├── MEMORY.md               <- Long-term context about Riley
├── INDEX.md                <- Folder map and priorities
├── README.md               <- Quick-start overview
├── AgentConfigs/           <- Per-agent handshake files (CHATGPT.md, GEMINI.md, SIDER.md)
├── CONTEXT_HUB/            <- Pipeline-managed content (captures, digests, promotions)
├── RileyProjects/          <- All active and queued projects
├── RileyAgents/            <- AI memory archives
├── scripts/                <- Pipeline scripts and config
└── .github/                <- Copilot instructions
```

---

## AI TEAM

**Claude Code** (Lead Engineer) — Terminal / local
Builds, file ops, pipeline, architecture. Works directly in `~/dev/RileyContext/`. Session start: reads CLAUDE.md + MEMORY.md locally.

**Claude.ai** (Lead Strategist) — Web + iOS (Dispatch/Cowork)
Planning, architecture, long-form thinking. Session start: reads RILEY_CONTEXT.md via GitHub raw URL or Desktop Commander.

**ChatGPT** (Ideation Partner) — Web/app
Brainstorming, daily AI briefs, scripts. 80+ saved memories. `/context` = fetches GitHub URL. Session start: loads context from GitHub.

**Gemini** (Google Integration) — Web/app, AI Studio, Gems
Search, research, YouTube analytics. `/context` = fetches GitHub URL. Session start: loads context from GitHub.

**Sider** (Multi-Model Hub) — Browser extension (Plus)
Quick queries, web research, PDF analysis, model comparison. Wisebase "Riley Context Hub" loaded with RILEY_CONTEXT + ARMOR_APP_SPEC notes. Session start: reads Wisebase.

---

## CAPTURE METHODS

- iOS Share Sheet shortcut (one-tap save to iCloud `_move-to-dev_icloud` drop folder)
- Voice capture via home screen icon
- Back Tap (double-tap phone back = clipboard saved)
- Manual typing in any AI chat, then /capture command
- macOS CaptureApp.applescript (direct to local inbox)
- All captures route to `CONTEXT_HUB/captures/inbox/` (directly or via drop folder pull)

---

## DESIGN THINKING (Apply to Every Build)

1. **Empathize**: Fast/messy capture is intentional. Organization should be invisible.
2. **Define**: What friction is this solving? Ask before building.
3. **Ideate**: Present options, not just solutions. Match minimal aesthetic.
4. **Prototype**: Functional first. Artifacts over documentation.
5. **Test**: Watch for "close but..." feedback. Adjust fast, don't defend.

## DECISION PRINCIPLES

Minimal > Feature-rich. Speed > Perfection. Context > Structure. Cross-platform required. Auto-organize, don't ask the user. Build for others to use — tools should be shareable and non-technical-friendly.

---

## ACTIVITY LOG

### 2026-03-23
- **Local-first migration complete**: Canonical root moved from Google Drive to `~/dev/RileyContext/` (local, not cloud-synced). Eliminates file locking errors from cloud sync daemons.
- **Repo merged**: `~/dev/rileyfile/` git mirror merged into `~/dev/RileyContext/` as single repo.
- **GitHub repo renamed**: `rileyfied/rileyfile` -> `rileyfied/RileyContext`.
- **Drop folder capture**: iCloud `_move-to-dev_icloud` and Google Drive `move-to-dev_google-drive` wired as pipeline capture inboxes. Pipeline pulls files to local inbox each run.
- **All references updated**: CLAUDE.md, AGENTS.md, agent configs, skills, memory files, scripts, copilot instructions — all pointing to `~/dev/RileyContext/`.
- **Pipeline v4**: sync_context.sh now pulls drop folders, runs pipeline, commits and pushes directly from canonical root.

### 2026-03-16
- Google Drive migration (now superseded by local-first v4).
- Context pipeline v3: Claude Code became lead engineer.
- Agent configs rewritten for v3 architecture.

### 2026-02-23
- Agent handshake files pushed to GitHub. Git auth resolved.

### 2026-02-15
- Boil Out: Nuked OpenClaw. Cleaned exposed API keys. AI Operations Monitor spec complete.

### Previous
- YouTube Video #1 script and production plan complete
- Armor App blueprint and data sets ready
- iOS capture shortcut live
