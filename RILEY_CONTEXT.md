---

## SYNC PROTOCOL v2 (ACTIVE)

Canonical Source of Truth:
- GitHub repository (rileyfied/rileyfile)

Single Writer:
- Codex (local) is the only agent allowed to modify RILEY_CONTEXT.md.

Agent Roles:
- ChatGPT, Claude, Gemini generate summaries only.
- They do NOT modify context files directly.
- They do NOT run compile systems.
- They do NOT merge or push changes.

Update Mechanism:
- Codex-controlled write paths only:
  - `./scripts/eod_append.sh <file> <SOURCE>` for manual daily log appends.
  - `./scripts/sync_context.sh` for ingest/promotions merge runs.
- Automated scheduling is active via launchd:
  - `com.rileyfile.sync_context` runs hourly (`StartInterval=3600`) and pushes updates.
- Runtime state is local-only (`~/.rileyfile/runtime` by default):
  - `RILEY_INDEX.sqlite`, `.state.json`, `.promotions_state.json`, and lock artifacts.
- Canonical context content remains in the GitHub repo root and `CONTEXT_HUB/context/`.

Deprecated Systems:
- Inbox folder workflows
- Compile scripts
- CoWork merge systems
- iCloud as canonical bus
- Any automated context regeneration outside Codex

All prior sync logic is permanently deprecated.

---

# RILEY_CONTEXT.md
## Last Updated: 2026-03-14

> **Purpose**: Context reference for Riley's projects, preferences, and active work. Read by all AI agents. Hosted at: https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md

---

## CONTEXT HUB STATUS (2026-03-02)

- Context Hub v3 hardening is complete and active.
- Runtime/content split is live:
  - Runtime state uses local path (`~/.rileyfile/runtime` default, overridable by `RILEYFILE_RUNTIME_ROOT`).
  - Canonical outputs remain in repo/iCloud (`RILEY_CONTEXT.md`, ingest logs, digests, candidates, promotions).
- Launchd scheduling is active:
  - `com.rileyfile.sync_context` runs hourly and executes index -> ingest -> digest -> promotions -> merge -> commit -> push.
- Break-glass and rollback runbooks exist in:
  - `CONTEXT_HUB/context/README_ingest.md`.
- Known edge risks resolved:
  - iCloud sqlite corruption risk.
  - iCloud state/lock drift risk.
  - lock artifact cloud conflicts.
  - missing recovery path documentation.

---

## WHO IS RILEY

Entrepreneur, content creator, restaurant operations leader (Chick-fil-A). Building in the AI space while working full-time. "Multi-channel dumper" — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time.

**Communication**: Direct, efficient. No excessive formatting. Hashtags over folders. Context over structure. Show don't tell.

**Design eye**: Clean, minimal, non-generic. Gets distracted by formatting options — keep UI stripped down.

---

## ACTIVE PROJECTS (Priority Order)

**1. YouTube Channel** — #youtube #video #ai #tutorial
AI tools for non-technical audiences. First video: "You're Using AI Wrong." Target: frontline operational managers, not enterprise knowledge workers. Style refs: Nate B. Jones, Fireship, Igor Pogany.
Resources: `RileyFile/RileyProjects/YOUTUBE CHANNEL`

**2. Daily AI Audio Brief** — #aibrief #audio #news
15-20 min solo-narration briefings on breaking AI news. Sources: The Rundown AI, Ben's Bites, TechCrunch AI, arXiv, X/Reddit. NotebookLM format with copy/paste-ready blocks.

**3. Armor App** — #armor #scripture #bible #fighterverses
Scripture memorization with gamified 5-mechanic ladder (Word Bank → Word Scramble → Type 1st Letter → Type Full Word → Recite). Fighter Verses data sets A-E ready. Full blueprint exists at `RileyProjects/ARMOR APP/Armour_GPT_InfoArchBlueprint_v1.rtf`.
Resources: `RileyFile/RileyProjects/ARMOR APP`

**4. HarmonyHelper** — #harmony #piano #music #chords
Piano practice app. Python backend, web frontend.
Resources: `/Desktop/HarmonyApp/`

**5. AI Operations Monitor** — #conductor #monitor #agents
Local agent that watches AI processes on machine, reports costs, flags waste, eventually orchestrates which AI does what. Vision: non-technical conductor for AI workflows. PWA prototype first.

**6. Dashboard App (RileyHQ)** — #dashboard #productivity
Command center for all projects. Zero manual maintenance. Design discovery phase.

**7. Virtual Restaurant Manager** — #virtualmanager #visor #cfa
Knowledge base agent for restaurant operations. All roles in one place — owner, managers, vendors, HR, etc. Multi-year vision. Concept documented.

---

## RILEYDOMAIN STRUCTURE

```
RileyFile/
├── RILEY_CONTEXT.md        ← Canonical context file
├── README.md               ← Minimal workflow docs
├── scripts/
│   └── eod_append.sh       ← Canonical append + commit + push workflow
└── _deprecated/            ← Quarantined legacy workflows and files
```

---

## AI TEAM

**Claude** (Lead Architect) — Claude.ai + Cowork
Planning, architecture, and summaries. Session start: reads this file.

**Codex** — Terminal / local agentic tasks
Runs automations, file operations, local scripts. Session start: reads `~/.codex/AGENTS.md` which points to this GitHub URL. `/context` or `/rf` = fetch and confirm "Context loaded ✓".

**Sider** (Multi-Model Hub) — Browser extension (Plus)
Quick queries, web research, deep research, model comparison, PDF analysis. Wisebase "Riley Context Hub" loaded with RILEY_CONTEXT + ARMOR_APP_SPEC notes. Session start: reads Wisebase.

**ChatGPT** — Ideation, long-form content, AI briefs
Brainstorming, daily AI briefs, scripts. 80+ saved memories. `/context` = fetches GitHub URL. Session start: loads context from GitHub.

**Gemini** — Google ecosystem
Search, research, Google integration. `/context` = fetches GitHub URL. Session start: loads context from GitHub.

---

## CAPTURE METHODS

- RileyNotes app (manual typing)
- iOS Share Sheet shortcut (one-tap save)
- Back Tap (double-tap phone back = clipboard saved)
- Voice capture via home screen icon
- macOS automation (Codex-based capture — tested and working 2026-02-19)
- All captures land in `RileyShare/captures/` and get organized by Claude

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

### 2026-02-23
- **Agent handshake files pushed to GitHub**: CHATGPT.md, GEMINI.md, SIDER.md, CONTEXT_SYNC_SETUP.md, INDEX.md, MEMORY.md, RILEY_CONTEXT_SYNC.md all committed and live on repo.
- **Codex AGENTS.md created**: Written to `~/.codex/AGENTS.md` and `~/AGENTS.md`. Contains /context protocol, workflow rules, file routing, capture methods.
- **Git auth resolved**: repository authentication and email privacy settings finalized; unrelated-history merge conflict resolved.

### 2026-02-15
- **Boil Out**: Nuked OpenClaw (config, binary, credentials, completions). Removed Codex (old version). Stripped agent personality files from RileyFile. Cleaned exposed API keys from .zshrc.
- **AI Operations Monitor spec complete**: Tracks spend on Claude.ai, Sider, ChatGPT, Gemini. iPhone widget + Mac app. Phased: Monitor → Flag → Execute.
- **Cross-platform browser automation**: Claude Chrome extension configured with approved domains.

### 2026-02-14
- YouTube content planning, desktop capture setup, RileyFile organization

### Previous
- YouTube Video #1 script and production plan complete
- Armor App blueprint and data sets ready
- 13,890 Safari bookmarks imported
- iOS capture shortcut live
- Sider onboarded with Riley Context Hub Wisebase

---

*Maintained in git.*

## PROJECT CONTEXT PROMOTIONS

### #idea — `CONTEXT_HUB/captures/_processed/#idea #fun #claude #skills #howto #prompt #rileyfied.txt`
- Captured at: 2026-03-14T19:34:12.534184-04:00
- Tags: #aibrief #claude #fun #howto #idea #prompt #rileyfied #skills
- Content: This is a transcript from a YouTube video.

Idea: create a skill like this for teenagers who want to convince their parents of something. Like go on a spring break trip or push curfew back by 1 hour or even stay over a friend’s house again for just one more night!

Let's get into the good
stuff. Here's the prompt I'm giving it.
Check my calendar for meetings and help
me prepare. In each meeting, I will have
notes of the documents I need you to
create and anything else that needs to
happen. Read…
[context_ingest_sha=f0d147f1a35ea4db85ac5de7c0c79ee9976623e0638373a4345806a5a6f286cb]

### #projects — `CONTEXT_HUB/captures/_processed/#projects #youtube #gemini #gems #prompt.txt`
- Captured at: 2026-03-14T19:34:12.535883-04:00
- Tags: #gemini #gems #projects #prompt #youtube
- Content: Idea for a Gemini Gem: YouTube growth engine.

Prompt:

Create an Al mini app called "YouTube Growth Engine". Build this app
as a multi-step workflow with separate nodes for each stage. Do NOT
combine steps into one generation node. Required workflow structure
Node 1: Topic Input
- Accept a YouTube niche or topic.
Node 2: Subtopic Decomposition
- Break the niche into 5-10 high-potential subtopics.
Node 3: Audience & Demand Analysis
- Identify audience intent and content demand signals.
From Node…
[context_ingest_sha=fc5201dcb3d36e260793b5fca92e5ce255309a2793e22bf0541357b62e6303e1]

### #promote — `CONTEXT_HUB/captures/_processed/#promote #context #inbox #Claude #Prompt #skill #7shifts #Schedule #Automation.txt`
- Captured at: 2026-03-14T19:34:12.536949-04:00
- Tags: #7shifts #automation #claude #context #inbox #promote #prompt #schedule #skill
- Content: This is a brain dump for Claude code context to read an analyze and understand so it can find patterns and identify things in the schedule that are making it difficult to automate and repeat from week two week.

There are Marriott parameters around the schedule each week, including but not limited to staff availability, staff performance, legal child labor law parameters, projected sales, shift template and layout, time off requests, new employee training, spring break sales increase, day of the…
[context_ingest_sha=74f46ddcfd66d68641fc7a67ede9ac48f439a997a4234f94ff232006a04fd433]

### #skills — `CONTEXT_HUB/captures/_processed/#skills #claude #howto #fun #idea #rileyfied.txt`
- Captured at: 2026-03-14T19:34:12.537649-04:00
- Tags: #claude #fun #howto #idea #rileyfied #skills #youtube
- Content: YouTube video transcript explaining “Claude Skills 2.0”

I want to learn how to leverage Claude Code and CoWork skills creatively to make things and build Rileyfied workflows and other fun things!

Chapter 1: Intro: What is Claude Skills 2.0?
0:00Claude Skills 2.0 is insane. Claude just dropped Skills 2.0 and it is a big deal.
0:066 secondsWe are talking about AI that can now test itself, fix itself, and stack on top of itself. Build once, run forever.
0:1313 secondsNo babysitting. I am going to…
[context_ingest_sha=1660452f04ec0dfb164ea184a3b70d9566648d9a13ee187ad8ba64b2bec0ea83]

### #productivity — `CONTEXT_HUB/captures/_processed/capture_20260314_194023.md`
- Captured at: 2026-03-14T19:48:25.793677-04:00
- Tags: #productivity
- Content: timestamp: 2026-03-14T19:40:23
source: claude-direct
tags: pipeline, rileyfile, infrastructure, capture-skill
---
Session summary: Pipeline consolidation & capture skill fixes (2026-03-14)

Key changes made this session:

1. PERMISSIONS STREAMLINED — Added broad allow rules for pipeline commands (ls, wc, cat, tail, head, grep, git, python3, bash) so skills don't stall on approval pop-ups. Critical for phone/remote sessions where pop-ups aren't visible.

2. TWO-REPO SPLIT FIXED — Discovered ~/dev…
[context_ingest_sha=1ae8507b91eb099a70f450a929f40add5e53eed2716ae482fe94f52de3b3e61a]


## DAILY LOG

### 2026-02-23 02:29:01
- No new inbox files processed.

### 2026-02-23 03:28:06
- No new inbox files processed.

### 2026-02-23 05:32:44
- `inbox/codex/2026-02-23_041536_launchd_test.md`

### 2026-02-23 05:36:30
- `inbox/codex/2026-02-23_053526_launchd_test.md`
- `inbox/codex/2026-02-23_053629_launchd_test.md`

### 2026-02-23 05:53:07
- `inbox/codex/2026-02-23_055306_setforget_test.md`

### 2026-02-23 05:58:29
- `inbox/claude/2026-02-23_055811_workspace_sync.md`
- `inbox/codex/2026-02-23_055811_workspace_sync.md`
- `inbox/codex/2026-02-23_055829_workspace_sync.md`

### 2026-02-23 06:06:29
- `inbox/codex/2026-02-23_060623_workspace_sync.md`

### 2026-02-23 06:06:34
- `inbox/codex/2026-02-23_060634_workspace_sync.md`

### 2026-02-23 06:06:46
- `inbox/codex/2026-02-23_060646_workspace_sync.md`

### 2026-02-23 06:07:07
- `inbox/codex/2026-02-23_060706_workspace_sync.md`

### 2026-02-23 06:07:17
- `inbox/codex/2026-02-23_060717_workspace_sync.md`

### 2026-02-23 06:07:28
- `inbox/codex/2026-02-23_060728_workspace_sync.md`

### 2026-02-23 06:09:01
- `inbox/codex/2026-02-23_060842_workspace_sync.md`

### 2026-02-23 11:00:56
- `inbox/codex/2026-02-23_110056_workspace_sync.md`

### 2026-02-23 11:01:08
- `inbox/codex/2026-02-23_110108_workspace_sync.md`

### 2026-02-23 18:42:44
- `inbox/codex/2026-02-23_184244_workspace_sync.md`

### 2026-02-23 18:52:47
- `inbox/codex/2026-02-23_185247_workspace_sync.md`

### 2026-02-23 18:57:50
- `inbox/codex/2026-02-23_185750_workspace_sync.md`

### 2026-02-23 19:02:52
- `inbox/codex/2026-02-23_190252_workspace_sync.md`

### 2026-02-23 19:07:55
- `inbox/codex/2026-02-23_190755_workspace_sync.md`

### 2026-02-23 19:12:57
- `inbox/codex/2026-02-23_191257_workspace_sync.md`

### 2026-02-23 19:18:00
- `inbox/codex/2026-02-23_191800_workspace_sync.md`

### 2026-02-23 19:20:33
- `inbox/codex/2026-02-23_192033_workspace_sync.md`

### 2026-02-23 19:21:14
- `inbox/codex/2026-02-23_192114_workspace_sync.md`

### 2026-02-23 19:26:35
- `inbox/codex/2026-02-23_192635_workspace_sync.md`

### 2026-02-23 19:31:38
- `inbox/codex/2026-02-23_193138_workspace_sync.md`

### 2026-02-23 19:36:40
- `inbox/codex/2026-02-23_193640_workspace_sync.md`

### 2026-02-23 19:41:43
- `inbox/codex/2026-02-23_194142_workspace_sync.md`

### 2026-02-23 19:46:45
- `inbox/codex/2026-02-23_194645_workspace_sync.md`

### 2026-02-23 19:51:53
- `inbox/codex/2026-02-23_195153_workspace_sync.md`

### 2026-02-23 19:56:56
- `inbox/codex/2026-02-23_195656_workspace_sync.md`

### 2026-02-23 20:01:58
- `inbox/codex/2026-02-23_200158_workspace_sync.md`

### 2026-02-23 20:03:13
- `inbox/codex/2026-02-23_200313_workspace_sync.md`

### 2026-02-23 20:09:17
- `inbox/codex/2026-02-23_200917_workspace_sync.md`

### 2026-02-23 20:14:19
- `inbox/codex/2026-02-23_201419_workspace_sync.md`

### 2026-02-23 20:19:22
- `inbox/codex/2026-02-23_201922_workspace_sync.md`

### 2026-02-23 20:24:24
- `inbox/codex/2026-02-23_202424_workspace_sync.md`

### 2026-02-23 20:29:26
- `inbox/codex/2026-02-23_202926_workspace_sync.md`

### 2026-02-23 20:34:29
- `inbox/codex/2026-02-23_203429_workspace_sync.md`

### 2026-02-23 20:39:31
- `inbox/codex/2026-02-23_203931_workspace_sync.md`

### 2026-02-23 20:44:34
- `inbox/codex/2026-02-23_204434_workspace_sync.md`

### 2026-02-23 20:46:36
- `inbox/codex/2026-02-23_204636_workspace_sync.md`

### 2026-02-23 20:51:38
- `inbox/codex/2026-02-23_205138_workspace_sync.md`

### 2026-02-23 20:56:41
- `inbox/codex/2026-02-23_205641_workspace_sync.md`

### 2026-02-23 21:01:43
- `inbox/codex/2026-02-23_210143_workspace_sync.md`

### 2026-02-23 21:06:46
- `inbox/codex/2026-02-23_210645_workspace_sync.md`

### 2026-02-23 21:11:48
- `inbox/codex/2026-02-23_211148_workspace_sync.md`

### 2026-02-23 21:16:50
- `inbox/codex/2026-02-23_211650_workspace_sync.md`

### 2026-02-23 21:21:53
- `inbox/codex/2026-02-23_212153_workspace_sync.md`

### 2026-02-23 21:28:07
- `inbox/codex/2026-02-23_212807_workspace_sync.md`

### 2026-02-23 21:33:10
- `inbox/codex/2026-02-23_213310_workspace_sync.md`

### 2026-02-23 21:38:12
- `inbox/codex/2026-02-23_213812_workspace_sync.md`

### 2026-02-23 21:43:15
- `inbox/codex/2026-02-23_214315_workspace_sync.md`

### 2026-02-23 21:48:18
- `inbox/codex/2026-02-23_214818_workspace_sync.md`

### 2026-02-23 21:53:20
- `inbox/codex/2026-02-23_215320_workspace_sync.md`

### 2026-02-23 21:58:23
- `inbox/codex/2026-02-23_215823_workspace_sync.md`

### 2026-02-23 22:03:26
- `inbox/codex/2026-02-23_220325_workspace_sync.md`

### 2026-02-23 22:08:28
- `inbox/codex/2026-02-23_220828_workspace_sync.md`

### 2026-02-23 22:13:31
- `inbox/codex/2026-02-23_221331_workspace_sync.md`

### 2026-02-23 22:18:33
- `inbox/codex/2026-02-23_221833_workspace_sync.md`

### 2026-02-23 22:23:36
- `inbox/codex/2026-02-23_222336_workspace_sync.md`

### 2026-02-23 22:28:38
- `inbox/codex/2026-02-23_222838_workspace_sync.md`

### 2026-02-23 22:33:41
- `inbox/codex/2026-02-23_223341_workspace_sync.md`

### 2026-02-23 22:37:05
- `inbox/codex/2026-02-23_223705_workspace_sync.md`

### 2026-02-23 22:39:37
- `inbox/codex/2026-02-23_223937_workspace_sync.md`

### 2026-02-23 22:43:28
- `inbox/codex/2026-02-23_224328_workspace_sync.md`

### 2026-02-23 22:44:17
- `inbox/codex/2026-02-23_224417_workspace_sync.md`

### 2026-02-23 22:45:53
- `inbox/codex/2026-02-23_224553_workspace_sync.md`

### 2026-02-23 22:47:35
- `inbox/codex/2026-02-23_224735_workspace_sync.md`

### 2026-02-23 22:50:11
- `inbox/codex/2026-02-23_225011_workspace_sync.md`

### 2026-02-23 22:51:35
- `inbox/codex/2026-02-23_225135_workspace_sync.md`

### 2026-02-23 22:53:46
- `inbox/codex/2026-02-23_225346_workspace_sync.md`

### 2026-02-23 22:58:48
- `inbox/codex/2026-02-23_225848_workspace_sync.md`

### 2026-02-23 23:00:59
- `inbox/codex/2026-02-23_230059_workspace_sync.md`

### 2026-02-23 23:06:01
- `inbox/codex/2026-02-23_230601_workspace_sync.md`

### 2026-02-23 23:08:56
- `inbox/codex/2026-02-23_230856_workspace_sync.md`

### 2026-02-23 23:12:53
- `inbox/codex/2026-02-23_231253_workspace_sync.md`

### 2026-02-23 23:13:44
- `inbox/codex/2026-02-23_231344_workspace_sync.md`

### 2026-02-23 23:15:35
- `inbox/codex/2026-02-23_231535_workspace_sync.md`

### 2026-02-23 23:17:45
- `inbox/codex/2026-02-23_231745_workspace_sync.md`

### 2026-02-23 23:24:04
- `inbox/codex/2026-02-23_232404_workspace_sync.md`

### 2026-02-23 23:29:06
- `inbox/codex/2026-02-23_232906_workspace_sync.md`

### 2026-02-23 23:30:03
- `inbox/codex/2026-02-23_233002_workspace_sync.md`

### 2026-02-23 23:35:05
- `inbox/codex/2026-02-23_233505_workspace_sync.md`

### 2026-02-23 23:40:08
- `inbox/codex/2026-02-23_234008_workspace_sync.md`

### 2026-02-23 23:45:10
- `inbox/codex/2026-02-23_234510_workspace_sync.md`

### 2026-02-23 23:50:13
- `inbox/codex/2026-02-23_235013_workspace_sync.md`

### 2026-02-23 23:55:15
- `inbox/codex/2026-02-23_235515_workspace_sync.md`

### 2026-02-24 00:00:18
- `inbox/codex/2026-02-24_000018_workspace_sync.md`

### 2026-02-24 00:05:21
- `inbox/codex/2026-02-24_000521_workspace_sync.md`

### 2026-02-24 00:10:24
- `inbox/codex/2026-02-24_001024_workspace_sync.md`

### 2026-02-24 00:15 [GPT]

---

# EOD TEST DROP

- Completed workflow hardening test.
- Verifying append/commit/push pipeline.

## DEPRECATED SYNC LOGIC

- Legacy inbox folder workflows and compile pipelines are deprecated.
- CoWork-based merge flows are deprecated.
- iCloud-as-canonical sync bus is deprecated.
- Any non-Codex automated context regeneration is deprecated.
- Manual Claude `/sync` trigger workflows are deprecated.
- Multi-agent context merge/update flows are deprecated.

### 2026-02-24 01:00 [GPT]

---

---
CHATGPT_EOD_SUMMARY | 2026-02-24

SESSIONS TODAY:
- Test entry | Mode: Capture | Outcome: Verify append script

DECISIONS MADE:
- Use SYNC PROTOCOL v2

OPEN LOOPS:
- None

PROJECT SIGNALS:
- None

CONTENT CAPTURES:
- None

HANDOFF TO CLAUDE:
- None
---

