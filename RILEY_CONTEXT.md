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
## Last Updated: 2026-04-17

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

### 2026-04-07
- **Context pipeline sync**: Pulled RILEY_CONTEXT.md v4. Diagnosed context pipeline crash on laptop (Errno 11 file locking, missing state.json). Architecture decision pending: Option A = local canonical + GitHub distribution. #context #pipeline
- **7shifts scheduling work**: Analyzed 132-employee availability PDF. Wednesday worst-staffed. 14 likely minors. 8 fully flexible. Built 4-tier CFA schedule AI training plan with 52-question questionnaire. #cfa #schedule #7shifts
- **activity-tracker skill built and installed**: Auto-logs dispatches to ACTIVITY_LOG.md, recalls on demand, syncs to GitHub. Includes RileyNotes drop folder ingestion. #productivity #context
- **RileyNotes ingested**: (1) Block "From Hierarchy to Intelligence" — AI replacing middle management, maps to YouTube thesis. (2) LLM Knowledge Base workflow — wiki-style knowledge compilation blueprint. Both processed to CONTEXT_HUB/captures/inbox/. #context #ingest
- **Block article captured**: URL: https://block.xyz/inside/from-hierarchy-to-intelligence #youtube #context
- **CFA training PDFs moved**: Cleaning Cards and Food Safety resources moved from iCloud drop folder to `RileyProjects/CFA/Training/`. #cfa
- **knowledge-base-compiler skill scoped**: Obsidian-style .md wiki compiled and maintained by LLM. The knowledge layer the pipeline feeds into. #productivity #context #buildit
- **auto-context-on-session-start added to CLAUDE.md**: New sessions now auto-read ACTIVITY_LOG.md and scan RileyNotes drop folder before starting work. #productivity #context
- **Creative Media Studio app captured**: New project. App that interrogates user's creative vision (taste, style, references) then uses all available AI tools (Adobe, Seedance, HeyGen, ElevenLabs, Descript, etc.) to produce final creative media. Examples: faceless YouTube videos, t-shirt designs, TikTok videos, birthday cards, avatar scenes. #buildit #app #creative
- **Stale naming purged**: All references to old repo/pipeline naming removed from ACTIVITY_LOG.md and MEMORY.md. MacBook correctly documented as primary machine. #context

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

## PROJECT CONTEXT PROMOTIONS

### #7shifts — `CONTEXT_HUB/captures/_processed/#7shifts #schedule #Departments.txt`
- Captured at: 2026-03-24T15:54:39.249029-04:00
- Tags: #7shifts #departments #schedule
- Content: 7shifts calls front of house (FOH) the “service” department and back of house (BOH) the “kitchen” department. I will be using all of these terms interchangeably.

I will list the employee and whether they belong in the service or kitchen department. Memorize these so you can group them and work on the schedule later

A-K FIRST NAME:
Aaron Hubbard kitchen
Abdiel Estrada kitchen
Adam kitchen
Addi service
Aiden Novak kitchen
Alanah service
Alex Paulo service
Alexis service
Allison service
Amelia se…
[context_ingest_sha=3cad90cb06a2e2ff2e798231e5d3f8362f07448f0d55d1072c507b6c18875174]

### #armor — `CONTEXT_HUB/captures/_processed/rsvp_verse_app_idea.txt`
- Captured at: 2026-03-24T22:00:06.832081-04:00
- Tags: #armor #bible #scripture #video #youtube
- Content: RSVP speed reading verse app idea — words revealed one at a time, accelerating pace, anchor/current word highlighted in red (like viral speed reading videos). Designed for scripture memorization. Also want a YouTube channel where every Bible verse gets its own video in this format — user clicks verse, it plays with sound. Armor App adjacent but could be standalone. Strong YouTube channel concept. #armor #scripture #youtube #video
[context_ingest_sha=877b0735bc2051573fcc9f58e16419c1d7fdfbefdb2ceb2839217757dcfb95e6]

### #cfa — `CONTEXT_HUB/captures/_processed/cfa_training_arcade_concept.txt`
- Captured at: 2026-03-24T22:00:06.831189-04:00
- Tags: #arcade #carspotter #cfa #training
- Content: CFA Merritt Island Training Arcade App — standalone HTML app, arcade/quiz game collection for the CFA team. All games in one place. Inspired by every popular beautiful quiz/game app that has existed.

Game ideas so far:
- Priority Tap: tap tasks in correct priority order (e.g. clean in place, greet guest, stock, change paper towels, wash hands)
- Core Values Order: put the 7 CFA core values in correct order
- Lemonade Recipe: how do you make lemonade step by step
- Ring It In: how do you ring in…
[context_ingest_sha=898d5d3f6ac73c82b9a28807f3d721e8f1dd0756c6ac057cdbb8e59cb58d8d21]

### #armor — `CONTEXT_HUB/captures/_processed/BibleGameNight.html`
- Captured at: 2026-03-25T15:10:59.314317-04:00
- Tags: #060a20 #0a0e27 #0d1333 #0f1445 #1a1f4e #2ecc71 #7a7568 #8a6d2b #armor #bible #d4a853 #e74c3c #e8e0d0 #f0c75e #f0eadc #menu
- Content: <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Bible Game Night</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
--navy:#0a0e27;--deep:#0d1333;--indigo:#1a1f4e;--gold:#d4a853;--gold-bright:#f0c75e;
--gold-dim:#8a6d2b;--correct:#2ecc71;--wrong:#e74c3c;--white:#f0eadc;--glass:rgba(255,255,255,0.06);
--glass2:rg…
[context_ingest_sha=f604a3d659cbedf00a4577f7cb1759c2340706b6b1e365f35f3c1d5044130880]

### #armor — `CONTEXT_HUB/captures/_processed/cfa_arcade_app_plan.txt`
- Captured at: 2026-03-25T15:10:59.314869-04:00
- Tags: #armor #bible #scripture
- Content: CFA Merritt Island Arcade App — Project Kickoff Capture
Date: 2026-03-24

### #claude — `CONTEXT_HUB/captures/_processed/#Claude #Prompt #Ingest #Context #BuildIt #App.txt`
- Captured at: 2026-04-07T21:04:12.055146-04:00
- Tags: #app #buildit #claude #context #ingest #prompt #youtube
- Content: I want an app that makes any creative media or creative design project that i can describe or think of. This app will ask the User questions to narrow down exactly what the final creative design project or media or product should look like, sound like, act like, PRODUCE, cause, make, create, or any other action or purpose it should invoke. It should help the User create any kind of creative media including video, graphic design, vector design, printed design, color, social media post, filtered p…
[context_ingest_sha=172e2718a298e8b031c9329b6a539e5c69ae716633d9300ec84a9acb9cf062e0]

### #claude — `CONTEXT_HUB/captures/_processed/#claude #article #ingest #context.txt`
- Captured at: 2026-04-07T21:04:12.057790-04:00
- Tags: #article #claude #context #ingest
- Content: At Sequoia, we see that speed is the best predictor of start-up success. Most companies are focused on AI as a productivity enhancer. Few are focused on the potential of AI to change how we work together. Block is showing what it looks like to fundamentally rethink organization design, ultimately harnessing AI to increase speed as a compounding competitive advantage.
Two thousand years before the first corporate org chart, the Roman Army solved a problem that every large organization still faces…
[context_ingest_sha=df4056ccdf761b9ecf2a8217d737672bb243bc6d52e382752ad4e5d67bb0b062]

### #ingest — `CONTEXT_HUB/captures/_processed/#ingest #claude #skill.txt`
- Captured at: 2026-04-07T21:04:12.058803-04:00
- Tags: #aibrief #claude #ingest #skill
- Content: Claude: read and analyze this then create skills for it and tell me what you created  and how to use it

LLM Knowledge Bases

Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge (stored as markdown and images). The latest LLMs are quite good at it. So:

Data ingest:
I index source docum…
[context_ingest_sha=b04da490f8368cf29ddda24f2350a9bb449e8c6094ec1f404f06f39f339ad1c8]

### #claude — `CONTEXT_HUB/captures/_processed/#Claude #Prompt #Ingest #Context #BuildIt #App__32b0560e75.txt`
- Captured at: 2026-04-07T22:00:06.012565-04:00
- Tags: #app #buildit #claude #context #ingest #prompt #youtube
- Content: I want an app that makes any creative media or creative design project that i can describe or think of. This app will ask the User questions to narrow down exactly what the final creative design project or media or product should look like, sound like, act like, PRODUCE, cause, make, create, or any other action or purpose it should invoke. It should help the User create any kind of creative media including video, graphic design, vector design, printed design, color, social media post, filtered p…
[context_ingest_sha=32b0560e7580474593cc8b5ca2214751ca080016478277601f42ce3bdea68b1f]

### #cfa — `CONTEXT_HUB/captures/_processed/Leader Quiz 2.pdf`
- Captured at: 2026-04-09T08:00:02.864418-04:00
- Tags: #1 #2 #4 #cfa #virtualmanager
- Content: %PDF-1.7
%
1 0 obj
<</Type/Catalog/Pages 2 0 R/Lang(en) /StructTreeRoot 19 0 R/MarkInfo<</Marked true>>/Metadata 156 0 R/ViewerPreferences 157 0 R>>
endobj
2 0 obj
<</Type/Pages/Count 2/Kids[ 3 0 R 16 0 R] >>
endobj
3 0 obj
<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 5 0 R/F2 9 0 R/F3 11 0 R>>/ExtGState<</GS7 7 0 R/GS8 8 0 R>>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI] >>/MediaBox[ 0 0 612 792] /Contents 4 0 R/Group<</Type/Group/S/Transparency/CS/DeviceRGB>>/Tabs/S/StructParents 0>>
endobj
4 0…
[context_ingest_sha=efd5afc17af00e1c315af3df0a7ec688567c516a8cbb836f15d9b0b804cc8d41]

### #producerai — `CONTEXT_HUB/captures/_processed/#ProducerAI #Suno #ArmorApp #ArmorSongs #Scripture #Bible.txt`
- Captured at: 2026-04-09T08:00:02.081407-04:00
- Tags: #armor #armorapp #armorsongs #bible #producerai #scripture #suno
- Content: Producer.ai “flow” instructions for Armor project:
________________

/suno

Generate a short Lyric-driven memorization song.

NOTES ON LYRICS:
-Sing only the provided lyrics in the exact format I give it to you.
-Do not add any extra words, ad libs, commentary, or paraphrasing.
-if you get pushback from the generation model on the specific lyrics I give you, change a small thing in style settings and try again.
-if you get recurring pushback, try singing the first Line as “la la la…” or “da da d…
[context_ingest_sha=6b9048d28da0c25bca7d18ce069858e24e96a9170ebed70c7e654dce40bf45d9]

### #claude — `CONTEXT_HUB/captures/_processed/#Claude #Inbox.txt`
- Captured at: 2026-04-09T22:12:44.129284-04:00
- Tags: #claude #inbox
- Content: Remind me to build a tool tomorrow that will scan paper photos for me and attach a name on the front of the picture for my dad so he can more easily remember who the person is in the picture. I want to upload it to his digital frame and I don’t have a lot of time. He has boxes and boxes of photos create this task build the skill find the photos and make me an app where it is easy for me to give you these photos with just a snap of my phone and you will take care of the rest
[context_ingest_sha=ab88fe8b0f3ec959edbe897f1fe19e8b2e744b6ad335d2c56e2213f7a2dcd629]

### #claude — `CONTEXT_HUB/captures/_processed/#claude #ingest #append.txt`
- Captured at: 2026-04-09T22:12:44.129939-04:00
- Tags: #append #claude #ingest
- Content: Append this text to the most recent drop .txt file:

```Put these instructions in front of every image prompt you write, before you write anything else: "Magnum opus, best quality, highly professional, unwavering depth in alignment, lighting that adds allure, sharp/crisp and deep focus digital colored line drawing:" Create a !!!2D!!! illustration in a (Thematically original portmanteau art optimization style name): (Improvised description of the art optimization style). Key functions include des…
[context_ingest_sha=ff1a3ba7ccda7c75282a0f4d1c9f1ca61f8f5bd9848e532d872666c2285eb785]

### #idea — `CONTEXT_HUB/captures/_processed/#idea #skill #claude #ingest #context #buildit.txt`
- Captured at: 2026-04-09T22:12:44.130420-04:00
- Tags: #buildit #claude #context #idea #ingest #skill
- Content: I found this text file on my phone. It sounds like a great prompt/skill. I think the goal is for the agent to analyze a given source image or video or design element or artwork etc? Maybe even music, and then create a prompt for another AI that explains what the user wants to generate? Not sure. Read this text file and add it to the BuildIt list and activity log for pending builds and projects.
[context_ingest_sha=3c7d0a98f3fe661fc308232576a21bc4ea37a43b87f293f5c1d6ea3179d2f52f]

### #claude — `CONTEXT_HUB/captures/_processed/#claude #ingest #buildit #idea.txt`
- Captured at: 2026-04-10T04:06:55.135842-04:00
- Tags: #buildit #claude #idea #ingest #video #youtube
- Content: https://youtu.be/VRub1w-APTc?si=hw0EeSA1IQBLURX7

Another video about building the ultimate wiki-style personal knowledge base
[context_ingest_sha=a38846f0aade32d59a297c217ea3e0c193a15c76b79400882643fc20a18dbdcd]

### #ingest — `CONTEXT_HUB/captures/_processed/#ingest #claude #buildit #context.txt`
- Captured at: 2026-04-10T04:06:55.136836-04:00
- Tags: #buildit #claude #context #ingest #video #youtube
- Content: https://youtu.be/sboNwYmH3AY?si=Ng37Kk5uBw_ysFZU

Already talked about this the other day but let’s add this to your task list
[context_ingest_sha=065b4d4645d3aa0ce88aac2477cc46964185632408b31033bed3dcc97e43b14c]

### #buildit — `CONTEXT_HUB/captures/_processed/#BuildIt #Project #recall #FireCrawl #Scrape #Bible.txt`
- Captured at: 2026-04-10T05:44:52.502635-04:00
- Tags: #armor #bible #buildit #firecrawl #project #recall #recalled #scrape
- Content: I just remembered when we created the fire crawl Skills because I wanted to create a full Bible knowledge database and found a website that had hundreds of links and information that I wanted to use as the knowledge base. Where were we on that? Remind me the next time I ask you for a list of recalled projects.

NEW RULE FOR YOU:
Treat any file that includes the tag #recall this way—
-read the dropped text or file & ingest to context (usual pipeline)
-deep dive your chats, memory, projects, conte…
[context_ingest_sha=8a4ab79e1a5848d979d37f66f87dda66ac9d147107246c124fa20a6ba331ff67]

### #youtube — `CONTEXT_HUB/captures/_processed/#youtube #ai #quote.txt`
- Captured at: 2026-04-11T08:00:01.364921-04:00
- Tags: #ai #quote #youtube
- Content: Having the right format doesn’t necessarily give you the best results. You can have the best church, the best books, you can homeschool your kids, teach them scripture, set boundaries, use discipline.

But God is the one. Without God it’s system failure.

The stack was secure, the foundation is strong.

But God is the only failsafe. The first and the last command.

(Whatever that’s called in programming speak)

Basically you can build a great system all day, but good systems don’t always bear go…
[context_ingest_sha=c75d481e40cbf8adc1089d111e424ffde1771b76f5f87b160979bac9b4cc82cd]

### #youtube — `CONTEXT_HUB/captures/_processed/GEMOJI_training.txt`
- Captured at: 2026-04-11T08:00:01.369972-04:00
- Tags: #youtube
- Content: Gemini

Conversation with Gemini:



You said

Please read the following thread in its entirety. I heard grok was very good at image generation, so I asked it to recreate (essentially "clone" my original 2D Bitmoji. I have about 300 downloaded images of the Bitmoji. Grok made it sound like it would be easy. But it did not produce images, it just produced links to the x.ai website and called the links "png's" ...not sure what that's all about. But this has to be possible somewhere. So can u do th…
[context_ingest_sha=29216cbf6d0c6fd5fa51ad57784dc324fe3581801618f7225b64d62f7fad9a28]

### #suno — `CONTEXT_HUB/captures/_processed/#Suno #ArmorSongs #ArmorApp #Prompt #YouTube.txt`
- Captured at: 2026-04-12T08:00:06.254655-04:00
- Tags: #armorapp #armorsongs #prompt #suno #youtube
- Content: This prompt made a really fun song! Deuteronomy 7:9 

Simple Up Front Melody, Clear Diction And Lyrics. Piano And Male Vocal. Simple Vibe, Minimal Production. Mid-To-Upbeat, Play Along/Sing Along Style, Lyric-Driven
[context_ingest_sha=da19fecc18eb71ea817434acd7b26749ebe24a768d8b5eefcec4b85b006306b6]

### #aibrief — `CONTEXT_HUB/captures/_processed/AI_filmmaking_project_handoff.md`
- Captured at: 2026-04-17T08:00:04.618868-04:00
- Tags: #aibrief
- Content: # AI Filmmaking Language Book / Phrasebook — Project Handoff

## Project Goal
Build a high-value reference for AI filmmaking and AI video production that helps a serious user:
- know what they want visually
- know how to describe it to AI tools
- save time during prompting and iteration
- understand cinematic language, shot language, editing language, lighting, composition, staging, and style
- translate abstract ideas into concrete AI prompt language
- work across storyboard images, text-to-vid…
[context_ingest_sha=22346c40dade884dd6fcbcf34fa3591b0a110f4c7d0f84b927e6796d042c3f0e]


## Concept
Collection of arcade-style training games and pop-up quizzes for CFA Merritt Island team.
Standalone HTML app. Timer countdowns, arcade vibes, beautiful UI.

## Game Ideas (from Riley)
1. Tap-in-Order — prioritize tasks in correct order (clean in place fans, greet guest, stock, change paper towels, wash hands, etc.)
2. Core Values Order — put 7 core values in correct sequence
3. How Do You Make It — lemonade rec…
[context_ingest_sha=10536611c3b99b6a6f3929ccffa5419a805bd7701958b8eb7992eaf44ca63a74]

### #cfa — `CONTEXT_HUB/captures/_processed/cfa_folder_discovery.txt`
- Captured at: 2026-03-25T15:10:59.315375-04:00
- Tags: #cfa #virtualmanager
- Content: CFA iCloud Folder Discovery — Full Audit
Date: 2026-03-24

## Summary
1,837 files in ~/Library/Mobile Documents/com~apple~CloudDocs/CFA/
Full discovery pass completed. Categorized as Merritt Island-specific vs. corporate/templates/external.

## Merritt Island-Specific Files
- FOH EMPLOYEE ROSTER_06.14.2025.csv (77 FOH staff)
- CFAMI_EmployeeList__06-14-25.csv (full employee list)
- Employee POS codes_numbers.csv (129 employees)
- CFAMI_Sidework_AM_PM_Simple.pdf (opening/closing by position)
- CF…
[context_ingest_sha=e4c958e692544acca205f6ee64e493113011e7228f41dd6435922e98f208e8fa]

### #schedule — `CONTEXT_HUB/captures/_processed/#Schedule #BrainDump.txt`
- Captured at: 2026-03-25T15:10:59.311932-04:00
- Tags: #braindump #schedule
- Content: The template is very fluid because my boss has been using it forever and he’s the one who wrote it so he basically just knows what to do and it’s easy for him for example the template comes in and then if any shifts look funny like maybe 7shifts auto schedules a minor for nine hours or something he knows just to split the shift we’re adding our here takeoff an hour there stay within the parameters and know exactly who he’s gonna give it to and where they are in the list and this is making me cra…
[context_ingest_sha=500f3cddf7441d22867b91e8140e584965b5765d328fc4ab3cc7a5f55386bc8b]

