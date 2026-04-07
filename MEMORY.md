# MEMORY.md — Long-Term Context
Last updated: 2026-03-23

## About Riley

Entrepreneur, content creator, Chick-fil-A restaurant manager (Merritt Island, FL). Building AI tools and content while working full-time. Married. "Multi-channel dumper" — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time.

- Email: rileygcolley@icloud.com
- Timezone: America/New_York
- Pronouns: he/him

### Core Traits
- Working Style: Rapid iteration, minimal friction, direct communication
- Design Eye: Clean, minimal, non-generic. Gets distracted by formatting options.
- Decision-Making: Context over structure. Speed over perfection. Minimal over feature-rich.
- Communication: Direct and efficient. No fluff. No emojis unless asked.
- Faith: Christ follower. Heart for service, hospitality, servant leadership.
- Music: Writes songs (Suno for demos), learning piano (chord inversions, 2-5-1 progressions, solfege). Knows music theory and guitar.

## System & Workflow

### Canonical Root
Local: `~/dev/RileyContext/` (this IS the git repo)
- Claude Code works directly in this folder
- Claude.ai reads via GitHub raw URL or Desktop Commander
- GPT/Gemini/Codex/Sider fetch from GitHub: https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md
- Pipeline commits and pushes directly from this folder

### Devices
- MacBook (rileycolleyFW) — laptop, PRIMARY machine. Riley refers to this as "laptop," "desktop," "computer," or "home computer." Default assumption unless iMac is explicitly named.
- iMac Pro (rileycashpro) — desktop, 64GB RAM, 8-core Xeon. Secondary Claude Code machine.
- iPhone — captures, Claude.ai iOS, ChatGPT, Gemini
- Deep Apple ecosystem user. Comfortable with Terminal despite identifying as non-coder.

### Capture Methods
- iOS Share Sheet shortcut (one-tap save to CONTEXT_HUB/captures/inbox/)
- Voice capture via home screen icon
- Back Tap (double-tap phone back = clipboard saved)
- Manual typing in any AI chat, then /capture command
- All captures route to local inbox (or iCloud _move-to-dev drop folder from iOS)

### Pipeline
- sync_context.sh runs twice daily (8am, 10pm) via launchd
- Indexes files, ingests captures, builds digests, promotes to RILEY_CONTEXT.md
- Runtime state (sqlite, locks) stays local at ~/.rileyfile/runtime/
- After pipeline: git commits and pushes RILEY_CONTEXT.md directly from ~/dev/RileyContext/

## Active Projects (March 2026)

1. **YouTube Channel** — First video "You're Using AI Wrong" scripted and ready. Target: non-technical frontline managers. Style: Nate B. Jones, Fireship, Igor Pogany.
2. **7shifts Scheduling** — Automating CFA schedule creation. Brain dumps captured about rotating minors, catering team scheduling, Claude-powered schedule generation.
3. **Armor App** — Scripture memorization with gamified 5-mechanic ladder. Blueprint done. Fighter Verses data sets A-E ready.
4. **Car Spotter Training Arcade** — Multi-game car logo quiz for CFA drive-thru team. Design phase.
5. **Daily AI Audio Brief** — 15-20 min solo-narration AI news. Sources: The Rundown AI, Ben's Bites, Nate B. Jones, The Algorithm, TechCrunch AI, VentureBeat, Axios AI+, arXiv, X/Reddit. Spotlight triggers: major AI figures, viral posts (>15K likes or >100K views). Ongoing production.
6. **Piano / HarmonyHelper** — Learning piano. App queued. Extensive resources in RileyProjects/Piano.
7. **AI Operations Monitor (Conductor)** — Watches AI processes, reports costs, flags waste. Spec complete.
8. **Dashboard (RileyHQ)** — Command center for all projects. Design discovery.
9. **Virtual Restaurant Manager** — CFA knowledge base agent. Long-term concept.

## AI Team

- **Claude Code** — Lead Engineer. Builds, file ops, pipeline, architecture.
- **Claude.ai** — Lead Strategist. Planning, design, long-form thinking.
- **ChatGPT** — Ideation Partner. Brainstorming, content drafts, AI briefs.
- **Gemini** — Google Integration. YouTube, Search, research, AI Studio.
- **Sider** — Multi-Model Hub. Browser queries, web research, PDF analysis.

## Positioning & Revenue
- Unique niche: "AI for non-tech frontline managers" — underserved market
- YouTube channel is clearest near-term revenue path (ads, sponsorships, courses)
- Daily AI Brief could become a podcast/newsletter with monetization
- Armor App has niche market potential (Christian scripture memorization)
- CFA operational leadership is current income; side projects are the growth play
- Mantra: "I help non-tech people go from AI chat threads to actual systems and automation"

## Key Interests
- Psychology of AI, human-AI interaction
- Mission: Democratize AI for non-technical audiences
- Architecture & strategy, early adoption signals
- Building tools for frontline workers, not enterprise

## Important Preferences
- NotebookLM audio overviews → readable transcripts
- Copy/paste-friendly outputs
- Specific over vague
- No excessive bullets/hierarchy
- Standalone HTML apps for team tools (run in iPhone Shortcuts, no server)
- No AI-generic design — every tool should feel crafted

## Lessons Learned
- OpenClaw consumed tokens overnight with no monitoring. Local agents need spending limits and monitoring before deployment.
- API keys should never be hardcoded in shell configs.
- Cloud sync (iCloud AND Google Drive) causes file locking conflicts with programmatic writes. Local-first eliminates this.
- Build the monitor BEFORE deploying more agents.
- Always read files before moving/archiving them. Verify they're current.
- Local dev folder is the hub. Cloud sync is only for iOS capture bridge, never for canonical storage.
- "Text > Brain" — if you want to remember something, write it to a file. Mental notes don't survive sessions.
- Don't move files without reading them first. Verify they're current and relevant before taking action.
