# Activity Log

## 2026-04-07 -- Monday

- **1:00pm DISPATCH** -- Loaded and synced RileyContext context from GitHub
  - Context: Pulled RILEY_CONTEXT.md (v4, dated 2026-03-25). Built 5 auto-memory files for Cowork persistence.
  - Status: completed
  - Tags: #context

- **1:15pm DISPATCH** -- Investigated context pipeline on iMac
  - Context: Found canonical at ~/dev/RileyContext/ (Google Drive). Pipeline crashed with Errno 11 file locking. State.json missing.
  - Status: completed
  - Tags: #context #pipeline

- **1:30pm DISPATCH** -- Architecture review for context pipeline fix
  - Context: Recommended Option A: local canonical + GitHub distribution. Eliminates cloud sync locking. Riley reviewing.
  - Status: waiting
  - Tags: #context #pipeline

- **2:00pm DISPATCH** -- Analyzed 7shifts employee availability PDF
  - Context: 132 employees mapped. Wednesday worst-staffed. 14 likely minors. 8 fully flexible. Need CFA ops knowledge training.
  - Status: completed
  - Tags: #cfa #schedule #7shifts

- **2:30pm DISPATCH** -- Created CFA schedule AI training plan
  - Context: 4-tier plan. Tier 1: CFA ops rules, minor labor laws, role mapping, locked assignments. 52-question questionnaire opened on iMac for Riley to fill out.
  - Status: active
  - Tags: #cfa #schedule #7shifts

- **3:00pm DISPATCH** -- Built and installed activity-tracker skill
  - Context: Skill installed on iMac at ~/.claude/skills/activity-tracker/. Auto-logs actions, recalls on demand, syncs to GitHub. Includes RileyNotes capture ingestion (Behavior 4). Seeded and pushed.
  - Status: completed
  - Tags: #productivity #context

- **3:30pm DISPATCH** -- Ingested 2 RileyNotes captures from iCloud drop folder
  - Context: (1) Block From Hierarchy to Intelligence article -- AI replacing middle management, maps to YouTube thesis. (2) LLM Knowledge Base workflow -- blueprint for wiki-style knowledge compilation. Both moved to CONTEXT_HUB/captures/inbox/.
  - Status: completed
  - Tags: #context #ingest

- **3:45pm DISPATCH** -- Moved CFA training PDFs and updated RILEY_CONTEXT.md
  - Context: Cleaning Cards and Food Safety PDFs moved to CFA/Training/. Block article referenced in context with #youtube #context tags. Committed and pushed.
  - Status: completed
  - Tags: #cfa #context

- **4:00pm DISPATCH** -- Scoping knowledge-base-compiler skill
  - Context: Riley wants searchable data warehouse built from all files. Not parallel to pipeline -- its the knowledge layer the pipeline feeds into. Obsidian-style .md wiki compiled and maintained by LLM.
  - Status: active
  - Tags: #productivity #context #buildit

- **4:15pm DISPATCH** -- Added auto-context-on-session-start to CLAUDE.md
  - Context: New sessions now auto-read ACTIVITY_LOG.md and scan RileyNotes drop folder before doing anything. Ensures continuity across all Claude surfaces.
  - Status: completed
  - Tags: #productivity #context

- **4:30pm DISPATCH** -- New RileyNotes capture: Creative Media Studio app concept
  - Context: Major new project idea. App that interrogates user to understand their creative vision (taste, style, references), then uses all available AI tools (Adobe, Seedance, HeyGen, ElevenLabs, Descript, etc) to produce the final creative media. Examples: faceless YouTube videos, t-shirt designs, TikTok videos, birthday cards, avatar scenes. Tagged #Claude #Prompt #Ingest #Context #BuildIt #App.
  - Status: active
  - Tags: #buildit #app #creative #new-project


## 2026-04-08 — 7shifts Knowledge Base Build (Cowork session)
#cfa #7shifts #context #schedule

Built comprehensive 7shifts knowledge base for CFA account via Chrome MCP + direct API calls to `/api/v2/*` endpoints. Logged into `app.7shifts.com` (Riley logged in manually, then handed off).

**Data captured:**
- Account: Chick-fil-A, Works Plan, location 57515 (Merritt Island, FL), company_id 46891
- Riley's user_id: 9237492, permission_template 27109, user_type 2 (Manager/employer), primary role Director
- 2 departments: Service (77195), Kitchen (77196). 9 Service roles including Director, TL, TM-Day/Flex/Night, Hospitality, Marketing, Training, Meeting
- 139 total active employees, 95 with Service Dept roles
- All 95 Service employees' availability fetched (93 have availability set; Riley + Sara Peterson do not)
- Service Mar '26 template (id 681115): 205 shifts, 1,179.8 hrs/week, 200 open / 5 pre-assigned (Michelle Sears Mon–Fri 06:00–13:00 TM-Day)
- Daily distribution: Mon/Thu 34 shifts, Tue/Wed 33, Fri 37 (heaviest), Sat 34 (later close 23:00)
- Role weekly totals: TMN 74, TMD 71, TL 24, TMF 18, H 13, Director 5
- No Sunday shifts (CFA closed)
- Template has zero projected sales and zero labor targets populated
- Director shifts are single 13:00–20:00 Mon–Fri only — no Sat director, no morning/evening overlap
- 43 shifts flagged `close: true`, zero flagged `open: true`

**Deliverable:**
`/Users/rileycolleyFW/Library/Application Support/Claude/local-agent-mode-sessions/6794d830-9211-4824-8c66-7a930aac96dd/0fcb78dc-7f43-4f3b-ab49-18ced6c2f56d/local_b2cf9e41-a70a-41b1-aba8-b5f7a82388f3/outputs/7shifts_knowledge_base.md` — full markdown knowledge base covering account identity, permissions, nav map, org structure, 95-person roster with availability tables by role, priority personnel lists (openers, closers, full-flex), complete Mar '26 template analysis with daily breakdowns, sample Monday build, improvement notes, raw endpoints for future sessions, and quick reference card.

**Observations for Riley's review:**
- Only Michelle Sears is pre-locked in the template. Every other week requires full drag-assign.
- Labor targets are blank — template carries no guard rails for OT/labor cost.
- 10 Service employees have no primary role marked — cleanup opportunity in Employees area.
- Director coverage may have a Sat gap worth questioning.
- Hospitality is lightly staffed (13/week) — expansion point if needed.

**Also today:**
- Delivered cleaned-up user preferences rewrite → `/Users/rileycolleyFW/Library/Application Support/Claude/local-agent-mode-sessions/6794d830-9211-4824-8c66-7a930aac96dd/0fcb78dc-7f43-4f3b-ab49-18ced6c2f56d/local_b2cf9e41-a70a-41b1-aba8-b5f7a82388f3/outputs/riley_user_preferences.md`. Killed all stale "RileyFile" aliases, added session-start auto-context instruction (iCloud + Google Drive drop folder scan), MacBook-primary device rule, context transparency clause, auto-log directive, operating principle, Google Drive scan.


## 2026-04-10 — Context sync (Cowork session)
#context #ingest

- **4:05am COWORK** -- /context-sync run. Ingested 2 new iCloud captures (both YouTube links re: personal knowledge base / wiki-style LLM workflow). Ran ingest_captures → build_digest → build_promotions → merge_promotions. 2 new entries promoted into RILEY_CONTEXT.md.
  - Captures: #claude #ingest #buildit #idea (VRub1w-APTc, wiki-style KB video), #ingest #claude #buildit #context (sboNwYmH3AY, follow-up to prior discussion — add to task list)
  - Status: completed
  - Tags: #context #ingest #buildit

- **5:44am CLAUDE CODE** -- /context-sync run. Ingested 1 new iCloud capture (#BuildIt #Project #recall #FireCrawl #Scrape #Bible). Pipeline failed twice on too-long filename in `_processed/` and `_archive_google-drive_2026-03-22/.../inbox/` (the rambling "lets work on my schedule project..." capture); renamed both to `lets_work_on_my_schedule_project_7shifts_template.txt` and re-ran. Pipeline succeeded: 4619 indexed, 1 ingested, 1 promoted. Commit `7d5b2c2` pushed; live URL verified fresh.
  - **NEW RULE absorbed:** any capture tagged `#recall` triggers a deep dive across chats/memory/projects/files, activity log update, and a #recall section the next time Riley asks "what were we working on." After update, the project is reclassified from #recalled to current.
  - Status: completed
  - Tags: #context #ingest #recall #pipeline-fix

### #recall — Bible Knowledge Database (Firecrawl origin project)
- **Why Firecrawl skills exist:** Riley built the firecrawl-* skill suite specifically to scrape Christianity.com and assemble a full Bible knowledge database.
- **Status:** Scrape phase complete; game/integration phase paused.
- **Crawled data (Mar 24, 2026)** at `~/.firecrawl/christianity/`:
  - `trivia.json` — 52 entries / 357KB (Jeopardy, fill-in-the-blank, quotes, timeline, geography)
  - `wiki.json` — 100 entries / 1.3MB (encyclopedic Bible content, theology, people, places)
  - `christianity_urls.json` — 573KB (5,000+ mapped URLs)
  - `christianity_homepage.md`
- **Game scaffold:** `~/dev/RileyContext/CONTEXT_HUB/captures/_processed/BibleGameNight.html` (1,288 lines, working game UI). Modes drafted: Jeopardy, Millionaire, Bible Blitz, Sword Drill, True/False, Fill-in-the-Verse, Head-to-Head Trivia.
- **Related tool:** `~/dev/RileyContext/RileyProjects/bible-lookup.html` — standalone ESV scripture search.
- **Last touched:** 2026-03-25.
- **Next step to revive:** parse trivia.json + wiki.json into structured question bank → wire into BibleGameNight.html → ship game-mode selector + multi-player setup.
- **Reclassified:** now an active current project (no longer #recalled).


## 2026-04-13 — Higgsfield pricing analysis + Cowork fix (Claude Code session)
#video #youtube #tools #cowork #fix

- **CLAUDE CODE** -- Analyzed Higgsfield AI pricing structure for Riley's AI video production goals. Scraped full pricing page via Playwright. Evaluated Starter/Plus/Ultra/Business tiers against 3 active video projects: RileyAI (personal AI clone), Behold (faceless Gospel YouTube channel), Armor App song videos.
  - Recommended: Plus monthly at $34 first month / $49 renewal. Unlimited Kling 3.0 on annual only — monthly Plus is nerfed (Seedance 2.0 access only, no unlimited burst). Still best value for testing the workflow.
  - Compared vs CapCut, OpenArt (Riley tried, bad), direct Seedance access on fal/Replicate, rolling own in Premiere.
  - Supplemental tools recommended: ElevenLabs for voice cloning ($22/mo), HeyGen only if Kling lipsync insufficient.
  - Status: completed
  - Tags: #video #youtube #tools #behold #rileyai

- **CLAUDE CODE** -- Fixed Cowork RPC mount error. Root cause: `.claude/skills` was a symlink → `~/dev/RileyContext/skills`. Cowork's sandboxed VM (virtiofs) can't follow symlinks to host paths outside its mount. Replaced symlink with real directory copy at both `.claude/skills` and the session-level skills path. Cowork sessions now boot cleanly.
  - Tradeoff: skills in `.claude/skills/` and `~/dev/RileyContext/skills/` are now two separate copies — edits in one don't auto-propagate. Sync hook deferred.
  - Status: completed
  - Tags: #cowork #fix #skills

- **3 empty iCloud captures found** (RileyLink 2026-04-12 16:54, 16:55, 16:55-2). All 0 bytes. Skipped — nothing to ingest.
  - Tags: #context #ingest
