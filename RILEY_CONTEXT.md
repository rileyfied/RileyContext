---

## SYNC PROTOCOL v3 (ACTIVE)

Canonical Source of Truth:
- Google Drive: `My Drive/RileyContext/`
- This file, all captures, context hub, and pipeline scripts live here.
- Claude.ai reads directly via Google Drive connector. No fetch commands needed.
- GitHub mirror (rileyfied/rileyfile) is updated automatically for GPT/Gemini URL access.

Who Can Write:
- Claude Code (laptop or desktop) runs the pipeline and writes RILEY_CONTEXT.md.
- Phone captures drop into `RileyContext/CONTEXT_HUB/captures/inbox/` via Shortcuts.

Runtime State (local-only, not synced):
- `~/.rileyfile/runtime/` — sqlite index, state json, lock files.

Deprecated Systems:
- iCloud as canonical bus
- Local ~/dev/rileyfile as primary (now GitHub mirror only)
- iCloud as pipeline root (caused deadlocks; local repo is canonical)
- Codex as single writer (Claude Code is now the engineer)

---

# RILEY_CONTEXT.md
## Last Updated: 2026-03-22

> **Purpose**: Context reference for Riley's projects, preferences, and active work. Read by all AI agents.
> **Primary**: Google Drive `My Drive/RileyContext/RILEY_CONTEXT.md` (Claude.ai, Gemini)
> **Mirror**: https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md (GPT, other agents)

---

## CONTEXT HUB STATUS (2026-03-15)

- Context Hub v3 migrated to Google Drive as canonical root.
- Runtime/content split is live:
  - Runtime state uses local path (`~/.rileyfile/runtime`).
  - All content lives in Google Drive (`RILEY_CONTEXT.md`, captures, digests, promotions).
- Launchd scheduling is active:
  - `com.rileyfile.sync_context` runs twice daily (8am and 10pm) and executes index -> ingest -> digest -> promotions -> merge -> commit -> push.
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

### 2026-03-16
- **Google Drive migration complete**: Canonical root moved from iCloud to Google Drive `My Drive/RileyContext/`. Pipeline, captures, scripts all migrated.
- **Context pipeline v3**: Claude Code is now the lead engineer. Codex deprecated as single writer.
- **GitHub mirror**: `rileyfied/rileyfile` auto-pushes RILEY_CONTEXT.md for agent access via raw URL.
- **Agent configs updated**: CHATGPT.md, GEMINI.md, SIDER.md rewritten for v3 architecture.
- **File cleanup**: Merged CFA folders, cleaned Downloads, archived old iCloud/OpenClaw files.

### 2026-02-23
- Agent handshake files pushed to GitHub. Git auth resolved.

### 2026-02-15
- Boil Out: Nuked OpenClaw. Cleaned exposed API keys. AI Operations Monitor spec complete.

### Previous
- YouTube Video #1 script and production plan complete
- Armor App blueprint and data sets ready
- iOS capture shortcut live

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

### #capture — `CONTEXT_HUB/captures/_processed/#capture #schedule #context #BrainDump #brainstorm #7shifts #capture-2.txt`
- Captured at: 2026-03-15T05:05:37.626852-04:00
- Tags: #7shifts #braindump #brainstorm #capture #capture-2 #context #schedule
- Content: /capture

Figure out how we are going to schedule catering team members or just schedule team members to be the catering point person each day. This will involve Myles and Seth and Michelle and will require their feedback and ideas as we try it out. The goal:
-increase catering fan base & sales!
-sustainable excellence
-best place on the island to order catered food
-best place on the island to prepare/serve catered food
-allow catering to be our pleasure rather than a pain in the bleeping bleep…
[context_ingest_sha=16df052f1b77d6e57a43badd530d77b70cd150aae3b6857fbb1eac3217f1fad7]

### #capture — `CONTEXT_HUB/captures/_processed/#capture #schedule #context #BrainDump #brainstorm #7shifts #capture.txt`
- Captured at: 2026-03-15T05:05:37.627983-04:00
- Tags: #7shifts #braindump #brainstorm #capture #context #schedule
- Content: /capture

REMEMBER AND EXPLORE THIS IDEA IMMEDIATELY!!!!!
come up with an idea where we don’t have to send brakes in the middle of the shift… Like minors work a few hours in hospitality and then switch with another minor who worked the morning in service. The service team member takes a break and then works hospitality for the remainder of the shift. The team member who worked hospitality in the morning switches to service when the other team member comes off of service. This helps reduce the mo…
[context_ingest_sha=db036f2a6dd7e95d2a24575ed766f7b7a8a347e8849f1121083f09111a5322cb]

### ## — `CONTEXT_HUB/captures/_processed/10-12. PHILIPPIANS 25–11.md`
- Captured at: 2026-03-16T06:00:23.298663-04:00
- Tags: ##
- Content: ## 10-12. PHILIPPIANS 2:5–11

### #capture — `CONTEXT_HUB/captures/_processed/test_capture_20260316_173117.txt`
- Captured at: 2026-03-16T17:31:21.663284-04:00
- Tags: #capture #test
- Content: Pipeline test capture from Claude Code. Testing that captures land in Google Drive inbox and get processed correctly.
[context_ingest_sha=4bd7806e14bc35fa2766c499601de4e5d8d8a81de9e94316e7e02fab75ee4282]

### #aibrief — `CONTEXT_HUB/captures/_processed/capture-2026-03-17-063033.txt`
- Captured at: 2026-03-17T08:00:04.017119-04:00
- Tags: #7shifts #aibrief #cfa #prompt #schedule
- Content: ---
captured: 2026-03-17 06:31:51
source: CaptureApp
---

#cfa #schedule #7shifts #Prompt



PROMPT FOR CLAUDE.ai or CLAUDE COWORK or CODEX or GEMINI CODE:

https://login.7shifts.com/oauth2/authorize?client_id=36ebe0e2-ffd0-4fa2-84ff-937870aef5db&response_type=code&redirect_uri=https%3A%2F%2Fapp.7shifts.com%2Foauth2%2Fcallback&tenant_id=88d83f1a-7084-dc05-b977-57e205198ff6&code_challenge=iCjM5ay2I3VZEHbMmOOM7r8CDDaKOfDY1M6gst_yvn8&state=tbRMeAT6gN6B5uKRN4kfd2VThC-WSubL-mDmssFP5ec



This is a lo…
[context_ingest_sha=740d45b42ba9e3d56f6716611451e0071bf0406bcc017514bf07b019c2397f3c]

### #armor — `CONTEXT_HUB/captures/_processed/Faceless%20Bible%20Videos.pdf.pdf`
- Captured at: 2026-03-22T08:00:02.016541-04:00
- Tags: #aitools #armor #audio #bible #scripture #youtube
- Content: %PDF-1.4
%
1 0 obj
<</Title (Faceless Bible Videos)
/Producer (Skia/PDF m148 Google Docs Renderer)>>
endobj
3 0 obj
<</ca 1
/BM /Normal>>
endobj
7 0 obj
<</Filter /FlateDecode
/Length 12325>> stream
x}$9r~0G+
ya-	0-ˀ߈"dޞmIj2H'^~
/;H翼_3
__ۻz!ߟWq^~?~_^?WyAh^~wuE^~q@Jo8)?(m?|m )xV!
 1F̀R: n?0F?
NN8F^\ 
%oU循
Rap@bT*FP1hkU-(?xﵧɕ %KJt\
Q!hLZ#6b"9s,d7
=C|)E)nQH#?Hrx1
1Hˌ![{gSBP<Cxrqrg

/>:@_3O%ʡȲ˂RV*xvuͽ p(6# O>}}!|{R4Wx8b<}7
~q t>~t
~tA;Εm:_E0…
[context_ingest_sha=6b6fc672f0eb7913c0be8f2acd3ea476bce500788f92c2f1c5777119f8f66ac4]

### #knowthis — `CONTEXT_HUB/captures/_processed/#knowthis #cfa #training #app #idea.txt`
- Captured at: 2026-03-22T08:00:01.826111-04:00
- Tags: #app #cfa #idea #knowthis #training
- Content: A quick app idea that we can eventually add to the KnowThis app:

Quick simple slide deck style info cards that we can blast a few times during the week. These will have special
[context_ingest_sha=92edc7d31be351ee88676e8518e14eed42b7d4e6120f82fb74d92fd91249ebba]


##   
## Philippians 2:5–11  
## Tone: Reverent, steady, rising declaration. Not slow.
Style: Modern hymn with clear dynamic lift.  
##   
  
## STYLE PROMPT (Style Field Only)  
  
## Piano with light strings and subtle percussion. Warm male vocal. Moderate steady tempo. Clear, reverent tone. Gradual dynamic build beginning at “Therefore God has highly exalted him.” Strong melodic emphasis on “every knee” and “every tongue confess.” No long intro. No instrumental…
[context_ingest_sha=61ee411693790faed6c2ebda7fa7a322cc3ad6492dbfe72638810d32595e4261]

### #aibrief — `CONTEXT_HUB/captures/_processed/AI Brief uploaded to Descript. NEXT: practice reading transcript, have chatGPT:openclaw edit it down.txt`
- Captured at: 2026-03-16T06:00:23.317999-04:00
- Tags: #aibrief
- Content: AI Brief uploaded to Descript. NEXT: practice reading transcript, have chatGPT/openclaw edit it down & polish for viral status.
[context_ingest_sha=a1de56db6256f60720470f7cf961cec387ccaded68afe2077c6a36d2310750da]

### #armor — `CONTEXT_HUB/captures/_processed/#armor #prompt #suno #versesongs.txt`
- Captured at: 2026-03-16T06:00:23.087633-04:00
- Tags: #armor #bible #prompt #scripture #suno #versesongs
- Content: GLOBAL SUNO INSTRUCTION BLOCK (Use for all 5)

Paste this at top of every prompt:

Lyric-driven Scripture song.
Sing only the provided Bible reference and exact ESV verse text.
Do not add any extra words, ad libs, commentary, or paraphrasing.
Reference sung clearly at beginning and repeated clearly at end.
Clear diction. Words must be intelligible.
Simple memorable melody.
Light instrumentation.
Minimal instrumental intro or outro.
No long instrumental breaks.
Moderate tempo unless otherwise spe…
[context_ingest_sha=29567e1016442e3cfaa123e58aab447a5167af64b4d57f033ef5ce8f4bd1e01d]

### #armor — `CONTEXT_HUB/captures/_processed/#armor #todo.txt`
- Captured at: 2026-03-16T06:00:23.088195-04:00
- Tags: #armor #todo
- Content: Export Armor to GPT for coding
[context_ingest_sha=4e4c2e8415e418598113d8b8b6f5e5e9a85f3ea125db25e738d2b50b06c7dd76]

### #armor — `CONTEXT_HUB/captures/_processed/#armor #versesongs #suno #prompt #chatgpt Write me simple melodic songs to memorize these verses. Ea.txt`
- Captured at: 2026-03-16T06:00:23.089316-04:00
- Tags: #armor #chatgpt #prompt #scripture #suno #versesongs
- Content: #armor #versesongs #suno #prompt #chatgpt Write me simple melodic songs to memorize these verses. Each verse will have a simple song that goes with it. Easy to listen to, not annoying. Can be all different genres but lyrics should be front and center. Minimal oohs and ahhs, minimal repetition (except repeating a whole verse or part of a verse for memorization). Songs will be 1-2 mins, give or take. Short verses repeat. Long verses may repeat but do not extend song past 2:30. We will make a song…
[context_ingest_sha=0b0dbb3ead1b7344b2d6c75e7baa6255665051c188c94f884c16d50bcc854b95]

### #armor — `CONTEXT_HUB/captures/_processed/#article #idea #youtube context is everything: comparing people who don’t read the Bible to an AI ag.txt`
- Captured at: 2026-03-16T06:00:23.090097-04:00
- Tags: #armor #article #bible #idea #youtube
- Content: #article #idea #youtube context is everything: comparing people who don’t read the Bible to an AI agent who suddenly joins the convo & doesn’t know what you’re talking ab but has an opinion anyway
[context_ingest_sha=8e4b0905736a7d65bf5e06733dacc430c3e056bd62085061af1ed525a39f17d6]

### #armor — `CONTEXT_HUB/captures/_processed/2. Deuteronomy 1012–13.md`
- Captured at: 2026-03-16T06:00:23.301824-04:00
- Tags: #armor #bible #scripture
- Content: **2. Deuteronomy 10:12–13**  
  
Tone: Instructional, steady, forward-moving.  
Style: Light folk-pop. Acoustic-driven. Not slow. Clear pulse.  
  
⸻  
  
**SUNO STYLE PROMPT**  
  
Acoustic guitar with light percussion. Warm female lead vocal. Light folk-pop style with clear rhythmic phrasing. Moderate tempo. Words front and center. Simple harmony on final line only. No long instrumental intro. No instrumental breaks. Lyric clarity is priority.  
  
⸻  
  
**GLOBAL INSTRUCTION BLOCK (Paste abov…
[context_ingest_sha=debd73a9b4bfa562df2c2db15c5231c4fa953f99e74bc34a73baf140a4be57f4]

### #armor — `CONTEXT_HUB/captures/_processed/20. Ephesians 426.md`
- Captured at: 2026-03-16T06:00:23.302638-04:00
- Tags: #armor #scripture
- Content: **20. Ephesians 4:26**  
**Tone**  
Direct instruction. Firm. Not aggressive.  
**Style**  
Simple acoustic rhythmic chant-pop.  
  
Acoustic guitar with light percussion. Female vocal. Moderate tempo. Clear instructional tone. No instrumental breaks. Repeat full verse twice for memorization. Clear diction. No added words.  
  
**LYRICS**  
Ephesians 4:26  
Be angry and do not sin;
do not let the sun go down on your anger,  
Be angry and do not sin;
do not let the sun go down on your anger,  
Ep…
[context_ingest_sha=e450dd395bc77f7ce0a69b82146a80882c97677091d7cee765195c13b1c308e1]

### #armor — `CONTEXT_HUB/captures/_processed/3. John 112–13.md`
- Captured at: 2026-03-16T06:00:23.311200-04:00
- Tags: #armor #bible #scripture
- Content: **3. John 1:12–13**  
  
Tone: Confident, hopeful, identity-centered.  
Style: Gentle cinematic pop. Steady tempo. Not slow.  
  
⸻  
  
**SUNO STYLE PROMPT**  
  
Light piano and subtle strings. Male lead vocal. Gentle cinematic pop style. Steady moderate tempo. Clear, confident delivery. Minimal instrumental intro. No instrumental breaks. Words must remain fully intelligible. Simple harmony only on final repetition.  
  
⸻  
  
**GLOBAL INSTRUCTION BLOCK (paste above lyrics)**  
  
Lyric-drive…
[context_ingest_sha=c0549f984a7bbdc35cd6786e0e10f79aa32e425c4e12e8538514d5a3983f8fe8]

### #armor — `CONTEXT_HUB/captures/_processed/4. Romans 1133–36.md`
- Captured at: 2026-03-16T06:00:23.312418-04:00
- Tags: #armor #bible #scripture
- Content: **4. Romans 11:33–36**  
  
Lyric-driven Scripture song.  
Sing only the provided Bible reference and exact ESV verse text.  
Do not add any extra words, ad libs, commentary, or paraphrasing.  
Reference sung clearly at beginning and repeated clearly at end.  
Clear diction. Words must be intelligible.  
Simple memorable melody.  
Light instrumentation.  
Minimal instrumental intro or outro.  
No long instrumental breaks.  
Moderate tempo.  
Simple harmony allowed but must never obscure lyrics.…
[context_ingest_sha=f497968357112729e25bb350512bc3816aa276f2dc2fc7bf8576ecf65cbe0f89]

### #armor — `CONTEXT_HUB/captures/_processed/5. Romans 121–2.md`
- Captured at: 2026-03-16T06:00:23.313157-04:00
- Tags: #armor #bible #scripture
- Content: **5. Romans 12:1–2**  
  
Tone: Resolute, instructional, practical.  
Style: Simple piano-driven melodic pop (Randy Newman–inspired feel). Clear rhythm. Not slow.  
  
⸻  
  
**SUNO STYLE PROMPT**  
  
Piano-driven arrangement with light bass and subtle percussion. Warm male vocal. Simple melodic pop style with clear rhythmic phrasing. Moderate tempo. Slight lift in chorus-like sections but no instrumental breaks. Words must remain fully intelligible. Harmony only on final repetition if needed.…
[context_ingest_sha=b89dbdfdb8f433ed2238c41b9900c3c63336bcc43548180f6be2099ea03f6654]

### #armor — `CONTEXT_HUB/captures/_processed/GLOBAL SUNO INSTRUCTION BLOCK (Use for all 5).md`
- Captured at: 2026-03-16T06:00:23.323189-04:00
- Tags: #armor #bible #scripture #seta #suno
- Content: **GLOBAL SUNO INSTRUCTION BLOCK (Use for all 5)**  
  
Paste this at top of every prompt:  
  
Lyric-driven Scripture song.  
Sing only the provided Bible reference and exact ESV verse text.  
Do not add any extra words, ad libs, commentary, or paraphrasing.  
Reference sung clearly at beginning and repeated clearly at end.  
Clear diction. Words must be intelligible.  
Simple memorable melody.  
Light instrumentation.  
Minimal instrumental intro or outro.  
No long instrumental breaks.  
Moder…
[context_ingest_sha=1abcbcaf55bdd8d437a3fe2b513cb78ca32de28eebe57df808123d92846b15fb]

### #armor — `CONTEXT_HUB/captures/_processed/Male or female or mixed.txt`
- Captured at: 2026-03-16T06:00:23.479735-04:00
- Tags: #armor #gpt #prompt #scripture #versesongs
- Content: Male or female or mixed
Adults and teens ok
Rotate by genre
Harmony is ok but simple harmony that doesn’t muddy the lyrics, no heavy BGVs
Reference at beginning and end
Yes long verses can split into verses if it makes sense.
Yes, singing full verse/full song through twice is preferable unless it’s a longer verse. Can repeat first line or a key phrase if it makes sense.
Randomize tempo is ok, but think about the verse and context before you write prompt. Mismatched vibe could be weird. **Don’t b…
[context_ingest_sha=72368668eee9ee6b698a261da003563ca9fa1b4fb6070079e3b65f0d7d5fba55]

### #armor — `CONTEXT_HUB/captures/_processed/and they say I'm coming in and set up my tables and exchange when you say you're not welcome like th.txt`
- Captured at: 2026-03-16T06:00:23.490996-04:00
- Tags: #armor #bible
- Content: and they say I'm coming in and set up my tables and exchange when you say you're not welcome like that processing crap for the next even even realize I'm doing it and then then you feel like why do I feel like I'm so far from God why am I going to church in eight months or three months and why haven't I ever been studying in the Bible watching sermons because you've got a filthy temple and God's grieved in spirit not not on you pulling you in and you're not close to God because you devised yours…
[context_ingest_sha=50e1fdf89fcd9f53b0f83bfc47805293d1ecd35ebb97b725d21c1b0335f4cf83]

### #build — `CONTEXT_HUB/captures/_processed/#build #tool #agent #LocalAgent #PersonalAgent #OpenClaw #idea #Cowork.txt`
- Captured at: 2026-03-16T06:00:23.091091-04:00
- Tags: #agent #build #cowork #idea #localagent #openclaw #personalagent #tool
- Content: Create tool that pops up on my iPhone screen when I am  driving and using any app or using any tool on my phone that requires interaction or contains txt I have to read.

Clicking this tool will immediately trigger an agent to initiate an interactive conversation in voice mode by acknowledging that it’s gonna read the rest of the text on the page or ask me how I want to proceed with my current task and then I will just talk to it like a conversation and it will ask clarifying questions if needed…
[context_ingest_sha=ca7630e611b7cf736fab70b1903b9a01011475bd1d6cf623c7821fbe0dfe8dfc]

### #cfa — `CONTEXT_HUB/captures/_processed/Virtual Restaurant Manager.rtf`
- Captured at: 2026-03-16T06:00:23.488619-04:00
- Tags: #ai #cfa #context #idea #makeit #productivity #rileyfile #virtualman #virtualmanager #visor
- Content: {\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red61\green61\blue61;\red0\green0\blue0;\red61\green61\blue61;
}
{\*\expandedcolortbl;;\cssrgb\c30741\c30741\c30741;\cssrgb\c0\c0\c0;\cssrgb\c30741\c30741\c30741;
}
\margl1440\margr1440\vieww14500\viewh14440\viewkind0
\deftab720
\pard\pardeftab720\sa240\partightenfactor0

\f0\fs48 \cf2 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec3 #makei…
[context_ingest_sha=b2ab4ffc38387e8d3d6d12cc3ef03bc0d5fcb05e6deedc97038d679f47da6076]

### #cfaschedule — `CONTEXT_HUB/captures/_processed/#cfaschedule #todo.txt`
- Captured at: 2026-03-16T06:00:23.092287-04:00
- Tags: #cfaschedule #todo
- Content: Do a test run with Claude making the Chick-fil-A schedule
[context_ingest_sha=9171a73117a48755a2792c08f66aa2caeefc7922cf326c54a0f5feec1403293c]

### #context — `CONTEXT_HUB/captures/_processed/#context #memory #agentrules #claude.txt`
- Captured at: 2026-03-16T06:00:23.093168-04:00
- Tags: #agentrules #claude #context #memory
- Content: Claude needs to work this way. More bottlenecks tonight. 

how to fix bad onboarding:

• remove 30% of steps
• show the result before the form
• delay account creation

let users experience value before you ask for commitment
[context_ingest_sha=ae707c4f64925c40d136f492ce5498bfa9876dcec3a24a5a315202a9aa8fc133]

### #context — `CONTEXT_HUB/captures/_processed/#context #sync.txt`
- Captured at: 2026-03-16T06:00:23.094026-04:00
- Tags: #context #sync
- Content: Sider is my Custom Travel Agent
[context_ingest_sha=e96980fe3ed1ccdc6eba62a96ceeb192a040787ed547454e6452f0a15f3617de]

### #dashboard — `CONTEXT_HUB/captures/_processed/Thoughts brewing #projects #buildit #dashboard #artifacts #workflow #tools #apps #RileyFile #streaml.txt`
- Captured at: 2026-03-16T06:00:23.488000-04:00
- Tags: #apps #artifacts #buildit #context #dashboard #idea #madeit #makeit #productivity #projects #rileyfile #scripts #shipit #streaml #streamline #terminal #tools #widgets #workflow #youtube
- Content: Thoughts brewing #projects #buildit #dashboard #artifacts #workflow #tools #apps #RileyFile #streamline #widgets #scripts #terminal #shipit #youtube #idea #madeit #makeit #context

CLAUDE (& all agents) SHOULD REMEMBER: Things I am building should be for me, yes, but the ultimate goal is to share them with other people so they can use them too. The tools should be easy and workflows simple and very user friendly and very non-tech friendly. They should be tools that can be useful for anyone to ju…
[context_ingest_sha=a8fb1597440a436c22e1bbafbf2f00ff8d2bce233564f29fe30663d0a7199d4d]

### #gpt — `CONTEXT_HUB/captures/_processed/#gpt #prompt #agentsync #sync #instructions #memory #rules.txt`
- Captured at: 2026-03-16T06:00:23.096146-04:00
- Tags: #agentsync #gpt #instructions #memory #prompt #rules #sync
- Content: These are the details in my chatGPT iOS App personalization settings.

I can’t save the About Me section bc it is too long.

Read your current rules and research all your system memories, projects, and chats about my context and rules and preferences and past memory commands, etc.

Using what you researched, rewrite the current settings above for the “Custom Instructions” and “About Me” sections for the GPT iOS app so they best align with my context and what you know. Be sure to stay within the…
[context_ingest_sha=426d883aff138535ca9ee39f60c9898290abe028093bef3179b668dbfe226cfc]

### #idea — `CONTEXT_HUB/captures/_processed/#idea #cfami2026 #KnowThis #interface #design #inspiro.txt`
- Captured at: 2026-03-16T06:00:23.097001-04:00
- Tags: #cfami2026 #design #idea #inspiro #interface #knowthis
- Content: Look at WordBoard app design, interface & form filling examples. Use UX for example of multiple choice quizz templates
[context_ingest_sha=eaaa2aadba910123301738c24cf0f4bea83d313583efcba034325be3f50c6f55]

### #inspiro — `CONTEXT_HUB/captures/_processed/#inspiro #design #2026 #ai #KnowThis.txt`
- Captured at: 2026-03-16T06:00:23.098022-04:00
- Tags: #2026 #ai #design #inspiro #knowthis
- Content: https://www.bytesizeapps.net/

Workbook app
[context_ingest_sha=7f6828556fe92ecbfc6db4100c74f448448e22268965ae85b843013641835738]

### #productivity — `CONTEXT_HUB/captures/_processed/MacMostKeyboardShortcutsTahoe.pdf`
- Captured at: 2026-03-16T06:00:23.478780-04:00
- Tags: #productivity
- Content: %PDF-1.3
%
3 0 obj
<< /Filter /FlateDecode /Length 14691 >>
stream
x}r$uz%٘!9ɁZ @C@w?/>)ۏ}bw2d<YUh/W
U].uy)^ޖgUyPV%>A6u|S~V_/^<	+vVjU|Lfꪚˮպm
m'E˛YWռ/u[\oo)?zy&YVmK*zQ.fꢷ?55l^9=
ʺnf\V
,/o
0?os7?'/?Ϫūg/狟?ɧ,Ϟa"#/<++
ggeʓg'><_^/oʏϋ^7rm떶)hټ0W$!+A>l߸+h

ZhȪ[-e;[؎]VMWOB9sp^;	8aR8:d]vxn	%m"-
Wn|᤺:zXV4ucF!-Zz%Uh]ֳźm1(4^
/4d8#?)<:
Ϝ
Ǩ*Hk۲YX	_@2ˢx-_H
;=xVĶmWfvq
\̺y0l|"ǵϰ
cf2gϥ̒pĞ&v;QƩU5p
ټUug&0g'q27pbLCNUt4Ɖ̉2yyO
fĭA'ZUEf
o	ɿ-3%Xߢ…
[context_ingest_sha=74831608b11f8effcf5d0335616ca34c4bd5f92ad0f650ec75251075e5592619]

### #productivity — `CONTEXT_HUB/captures/_processed/See new posts.txt`
- Captured at: 2026-03-16T06:00:23.483353-04:00
- Tags: #productivity
- Content: See new posts
Conversation

jordy

@jordymaui
Image
I wasted 80 hours and $800 setting up OpenClaw - so you don't have to.
I tried everything. AWS servers, remote setups, wrong API keys, wrong models. I burned through about $800 on Anthropic API tokens alone. Tried Kimi. Tried Opus. Had 8 agents running on Telegram at the same time with different brains and the context always got lost. Every single one forgot what the other was doing. I made every mistake in the book.
This is now the best, most…
[context_ingest_sha=770af2af24d88d45aac2686a83a9f6c7f866842e302ffe42d593e942f4843db4]

### #prompt — `CONTEXT_HUB/captures/_processed/#prompt #eod #sync #RileyAgents #ChatGPT #eod:gpt.txt`
- Captured at: 2026-03-16T06:00:23.099675-04:00
- Tags: #aibrief #cfa #chatgpt #eod #eod/gpt #eod:gpt #prompt #rileyagents #sync #virtualmanager
- Content: When I type /eod/gpt, generate a structured end-of-day summary for Riley's Lead AI Architect (Claude). This will be pasted directly into Claude to update its context memory.

Review our conversation history from today and output the following structure exactly:

---
CHATGPT_EOD_SUMMARY | [DATE]

SESSIONS TODAY:
- [Topic] | Mode: [Ideation/Build/Research/Capture] | Outcome: [1 sentence]

DECISIONS MADE:
- [Decision + rationale in 1 line]

OPEN LOOPS:
- [Unfinished threads, pending ideas, or follo…
[context_ingest_sha=0a67265463cb6673f749484befa1e5079d3e6cf799d4afbb9c189b2b147de85a]

### #rileywrite — `CONTEXT_HUB/captures/_processed/#RileyWrite.txt`
- Captured at: 2026-03-16T06:00:23.086898-04:00
- Tags: #rileywrite
- Content: My attempts to fit in were like a single grain of sand trying to join a granite mountain.
[context_ingest_sha=02f33b84e6d7014d2e2e4a817e49c5511637506922bcc960c61182ddcc1ad109]

### #skill — `CONTEXT_HUB/captures/_processed/#skill #context #claude.txt`
- Captured at: 2026-03-16T06:00:23.100757-04:00
- Tags: #claude #context #skill
- Content: Create a new skill called
/next where you will choose the very next task we need to tackle. This should be specific and actionable. It can be a solo task or it can be part of a larger project or projects. It can be a brainstorm idea that you are suggesting for the first time, or maybe it is an idea that was buried in my context files from months ago, or even an idea from my Apple notes file or Bear notes file or old Google documents. This can be the beginning of a project, a project within a lar…
[context_ingest_sha=f8a6ab098511bc6697ff3e0fbbecd9818db9ecd3f3083c3f4223834cb81c8cf3]

### #task — `CONTEXT_HUB/captures/_processed/#task #DoNext #reminder #Claude #skill.txt`
- Captured at: 2026-03-16T06:00:23.101720-04:00
- Tags: #claude #donext #reminder #skill #task
- Content: Create a skill called
 /what-am-i-doing

This skill will run any time I say what was I doing or pick up where we left off or what’s the last thing we did or anything similar in context.

You will read the context from my most recent session and tell me:
-the one specific project we were most recently working on
-the goal of the project
-the most recent task you completed
-the status of the project
-next steps or if it’s ready to test.

Then look through my context files and tell me if you are aw…
[context_ingest_sha=689100dcda29cb24872430c15426a7ba1b0ba7ebc9bf597e0994f7d675107333]

### #test — `CONTEXT_HUB/captures/_processed/#test #context #claudecode #shortcut #rileyfile.txt`
- Captured at: 2026-03-16T06:00:23.102683-04:00
- Tags: #claudecode #context #productivity #rileyfile #shortcut #test
- Content: this is a note I am sharing for context.
[context_ingest_sha=2125f81ea25d9d9bf347de24ce0287d39c2200bdf3f409db2f6c29ad0b3803e6]

### #test — `CONTEXT_HUB/captures/_processed/#test #shortcut #rileyfile #context.txt`
- Captured at: 2026-03-16T06:00:23.104219-04:00
- Tags: #context #productivity #rileyfile #shortcut #test
- Content: This is a test note for Claude Code
[context_ingest_sha=551c5db2dc085ea6f9006889cf2c4fbefa2f40719028ccff1312ece4e25a6099]

### #textfx — `CONTEXT_HUB/captures/_processed/#textfx #ai #xpost #tweet #rileyfied #idea #article #blog.txt`
- Captured at: 2026-03-16T06:00:23.105142-04:00
- Tags: #ai #article #blog #idea #rileyfied #textfx #tweet #xpost
- Content: This impossible assimilation left me feeling like a patchwork quilt with seams that refused to lie flat.
[context_ingest_sha=700efee91a18747c89fdcb3ff3a521b12ba69cd1c061098c06860826f1b74624]

### #todo — `CONTEXT_HUB/captures/_processed/#todo.txt`
- Captured at: 2026-03-16T06:00:23.107138-04:00
- Tags: #todo
- Content: Armor app - 20 songs
Claude - scheduling skill
[context_ingest_sha=903837145d94fb9c9f455df930d8267988da68c320846831691a63b178fa93d1]

### #twitter — `CONTEXT_HUB/captures/_processed/#twitter #post-2.txt`
- Captured at: 2026-03-16T06:00:23.108043-04:00
- Tags: #post #post-2 #twitter
- Content: Splish splash what the hell is a bash
[context_ingest_sha=29ebd8fbc100461891aa63cb4a661ab14d3a0b8dc5a0d904e9c81e61a1acacaa]

### #twitter — `CONTEXT_HUB/captures/_processed/#twitter #post-3.txt`
- Captured at: 2026-03-16T06:00:23.108997-04:00
- Tags: #post #post-3 #twitter
- Content: Splish splash do u wanna play MASH
[context_ingest_sha=75d9e99ffae1ba806a7409e97cf22b73dc2767af9a50f6b6070583c0312cfff4]

### #twitter — `CONTEXT_HUB/captures/_processed/#twitter #post-4.txt`
- Captured at: 2026-03-16T06:00:23.109653-04:00
- Tags: #post #post-4 #twitter
- Content: Claude just told me what time it is and asked if I want to call it a night. Rude…5 points from Hufflepuff.
[context_ingest_sha=edb1bc1a507319c4c86977574145663fc21b0b57b8fe7546a04dd35407c04839]

### #twitter — `CONTEXT_HUB/captures/_processed/#twitter #post.txt`
- Captured at: 2026-03-16T06:00:23.110511-04:00
- Tags: #post #twitter
- Content: Splish splash your opinion is trash

Splish splash iteration is trash
[context_ingest_sha=38de14dead15f4821620aaefe8080bafa9894f2ac57b623e6b892f0270515d15]

### #youtube — `CONTEXT_HUB/captures/_processed/#youtube #bible #behold #idea.txt`
- Captured at: 2026-03-16T06:00:23.111202-04:00
- Tags: #armor #behold #bible #idea #youtube
- Content: God has the scroll ready, Jesus says “wait not yet, just one more…let me save one more…”
[context_ingest_sha=ee83c8853a7b5cb17cb469643bcf5e145076093bad492f016350a248b82443a4]

### #youtube — `CONTEXT_HUB/captures/_processed/#youtube #videoidea #rileyfile #AI #strategy #article #idea-2.txt`
- Captured at: 2026-03-16T06:00:23.111807-04:00
- Tags: #ai #article #idea #idea-2 #productivity #rileyfile #strategy #videoidea #youtube
- Content: Article beginning idea: 
“I’ve spent 3 months hiring “ai consultants” “support staff” “administrative assistants” “design architects” “developer” and every type of middle manager to put together the business of Riley. I have trained and studied and guided and trained some more. I’ve built this team like I build my staff.

It’s like all 15 years of “real work” (as opposed to knowledge work) experience in low-middle-upper-under-over-upside down people management came barreling out of the tunnel on…
[context_ingest_sha=c5d7af623f3b4cdc0f87dc2987457fbd5f9ee625ca16b88ea57d8d2d19a9826a]

### #youtube — `CONTEXT_HUB/captures/_processed/My Goal: to make something and help you make something too..txt`
- Captured at: 2026-03-16T06:00:23.480372-04:00
- Tags: #idea #rileybrand #rileychannel #rileyfile #tagline #youtube
- Content: My Goal: to make something and help you make something too.

Riley brand quote/tag line idea: “When you make something, you’ve made it.” Or something similar #rileyfile #youtube #rileychannel #rileybrand #tagline #idea
[context_ingest_sha=05beb546a76df3fa1f0d51ef40435c67f4186b11aabd0249906be06941765c1d]

### #youtube — `CONTEXT_HUB/captures/_processed/Soft skills for AI #softskills #ai #youtube #aistrategy.txt`
- Captured at: 2026-03-16T06:00:23.484770-04:00
- Tags: #ai #aistrategy #softskills #youtube
- Content: Soft skills for AI #softskills #ai #youtube #aistrategy

Knowing “quality” looks like (discernment in excellence)
[context_ingest_sha=c1b1baca8836631ce671b38f348b9b543146fc1f5fcea030e0737476a0688c09]


## DAILY LOG

(Legacy daily log entries from February 2026 have been archived. Current activity is tracked via the pipeline's daily digest in CONTEXT_HUB/context/_daily_digest/.)

