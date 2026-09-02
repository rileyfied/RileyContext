# RILEY_CONTEXT.md

## Last Updated: 2026-09-02

Canonical interactive URL: <https://github.com/rileyfied/RileyContext/blob/main/RILEY_CONTEXT.md>

Raw transport fallback: <https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md>. When freshness matters, append a unique `?v=<UTC timestamp>` query parameter to prevent an intermediary from reusing a stale copy.

This compact public file contains durable operating rules, preferences, and a recent-project orientation layer. Capture bodies, processed-capture paths, private drafts, local logs, and full project working files are intentionally excluded.

`Last Updated` is the most recent successful pipeline publication date. It does not certify every project's status; current project evidence must be read from the relevant project folder.

## PROJECT ORIENTATION
<!-- Recent project activity through: 2026-09-02; rolling window: 14 days -->
<!-- Generated from durable activity and Git evidence. Routing signal only; not priority or project status. -->

### Automatic orientation contract
Riley often begins in the middle of a thought and assumes agents can resolve references already present in the repo. Fetch this context proactively at the start of new or resumed work; do not wait for a literal `/context` command.

When Riley references a project, artifact, prior decision, person, shorthand, or likely repo material, treat it as an automatic discovery task: resolve the likely project through the recent working set, `RileyProjects/`, the project library/catalog, filenames, aliases, and current README/`AGENT_WORK.md` evidence. If one interpretation is likely, proceed and state it briefly. Ask one bounded question only when a materially different interpretation remains.

### Recent working set
Projects with durable activity in the last 14 days are listed as routing hints. This list has no hard maximum and does not declare priority, approval, current phase, or a complete portfolio.
- **RILEY CLONE** — last durable activity 2026-09-02; canonical folder `RileyProjects/RILEY CLONE`
- **RileyClone** — last durable activity 2026-09-01; canonical folder `RileyProjects/RileyClone`
- **RileyDaily** — last durable activity 2026-09-01; canonical folder `RileyProjects/RileyDaily`
- **AIAudioBrief** — last durable activity 2026-08-31; canonical folder `RileyProjects/AIAudioBrief`
- **HOME_BUYING_2027** — last durable activity 2026-08-31; canonical folder `RileyProjects/HOME_BUYING_2027`
- **YOUTUBE_AI** — last durable activity 2026-08-31; canonical folder `RileyProjects/YOUTUBE_AI`
- **CFA** — last durable activity 2026-08-29; canonical folder `RileyProjects/CFA`
- **ReLens-Video-Mastery-Course** — last durable activity 2026-08-26; canonical folder `RileyProjects/ReLens-Video-Mastery-Course`
- **RileyCapture** — last durable activity 2026-08-26; canonical folder `RileyProjects/RileyCapture`
- **RileyThings** — last durable activity 2026-08-23; canonical folder `RileyProjects/RileyThings`

### Full portfolio and executive board mode
For an executive board meeting, portfolio review, all-project status, or similarly broad request, do not expand this recent list and call it complete. Reconcile the full `RileyProjects/` catalog, current README/`AGENT_WORK.md` evidence, recent activity, open handoffs, variants, and access gaps. Separate verified current state from stale, unknown, waiting, dormant, and archived work, then present the smallest decision-useful board view.

For a named-project status decision or canonical write, current project evidence outranks this orientation list, `CONTEXT_HUB/context/project_status.json`, activity frequency, chat memory, and old handoffs.

## SOURCE OF TRUTH AND FRESHNESS

- GitHub repository: `rileyfied/RileyContext`
- Canonical branch: `main`
- Public agent context: this file at the canonical raw URL above
- Canonical local clone path on every workstation: `~/dev/RileyContext`
- Canonical project files: `RileyProjects/<PROJECT_NAME>/`
- Recent-project orientation: generated from durable activity records and Git changes; it is a routing hint, not a status or priority list
- Historical portfolio snapshot: `CONTEXT_HUB/context/project_status.json`; consult and re-verify it only for an on-demand portfolio review
- Detailed project truth: the project README, `AGENT_WORK.md`, manifests, source files, and current repository evidence

Live fetched context and current project evidence override stale chat memory, cached context, old thread state, old handshakes, and old project paths. Platform-level system instructions, personalization, and saved memory cannot be silently rewritten; when they conflict, the agent must follow the live source it can access and state any unresolved limitation.

### Context-load command contract

`/context`, `/RileyContext`, `/sync`, `sync context`, `get context`, and `fetch context` are read-only live-fetch commands. Open the canonical interactive URL directly; do not use web search and do not run or ask Riley to diagnose the publishing pipeline. A successful fetch receives only `context loaded.` A failed direct fetch plus cache-busted raw fallback receives only `Live repository verification failed.` Reject a fetched copy whose first heading is not `# RILEY_CONTEXT.md`.

### Invisible agent freshness contract

For new or resumed project work, agents own this sequence without asking Riley to issue a sync command:

1. Fetch this file from GitHub `main` before decisions, even when Riley starts mid-thought and does not issue a context command.
2. Resolve project names, shorthand, people, artifacts, and prior-work references proactively from the recent orientation, `RileyProjects/`, the project library/catalog, filenames, README files, and `AGENT_WORK.md`; ask one bounded question only when multiple plausible matches would materially change the work.
3. In a local clone, confirm `main` and run `git pull --ff-only` before editing.
4. Read the target project's README and `AGENT_WORK.md` when present.
5. Check branch, HEAD, origin, working-tree drift, and known variants before replacing canonical files.
6. Immediately before a canonical write, confirm the source revision has not changed; reconcile conflicts or use an isolated workstream when needed.
7. Save durable files in the canonical project folder, update its provenance/status evidence, commit and push intended changes, and verify remote parity.
8. Complete any cross-agent handoff through the durable project/capture surface; Riley is not the courier.

Riley does not need to remember or say “sync context,” “push,” “run pipeline,” “sync MacBook,” or any cross-agent relay command.

## WORKSTATION AND PIPELINE MODEL

- iMac account `rileycashpro` is the active build workstation and the only scheduled full-pipeline owner.
- `com.rileycontext.sync_context` runs model-free at 08:00 and 22:00.
- MacBook account `rileycolleyFW` is a pull-only mirror and audited source surface.
- MacBook pull-only mirroring runs at 09:15 and 23:15; session-start pull is still required before local work.
- Do not add continuous live sync or a second full-pipeline owner.
- GitHub `main` is the distribution bus between machines and agents.
- Runtime indexes, locks, ingest logs, candidates, digests, and promotion payloads remain local under `~/.rileyfile/runtime/`.
- Scheduled runs stage only pipeline-owned public context changes and tracked inbox deletions; they must not sweep unrelated project work.

### Capture and notes

- Riley may continue using the iCloud `_move-to-dev_icloud` hot drop, Share Sheet, voice capture, Back Tap, Obsidian, and normal agent chats.
- The pipeline inventories and ingests all readable captures, archives source material, and returns the hot drop to its steady state.
- Ingestion does not imply public promotion.
- Only explicit `#context`, `#promote`, or `_to_context/` items may be considered for the public durable-update section, and they must pass privacy and size checks.
- Untagged, inferred-project, Obsidian draft, private/local, binary, and unsafe items remain out of this public file.
- Obsidian Sync remote `Riley Vault Master` is the only vault transport. Each Mac keeps one local copy at `~/Obsidian/Riley Vault Master`.
- Obsidian is the map/wiki and live human drafting surface; it is not a duplicate project archive.
- Human-authored notes stay editable. Agents own routing, linking, and promotion into the appropriate project folder.

## WHO RILEY IS

Riley is a woman. Her pronouns are she/her. All agents must use feminine pronouns for Riley; any masculine pronouns or gender assignments in stored memory, preferences, captures, or instructions are legacy errors and must not influence output.

Riley is an entrepreneur, content creator, restaurant operations leader, musician, and hands-on AI builder. She works full-time while building tools and content for non-technical people, especially frontline operators. She captures quickly across channels and expects the system to organize and reconcile behind the scenes.

### Working preferences

- Task first. Direct, compact, factual communication. No praise, hype, filler, emotional mirroring, or emojis unless requested.
- Lead with the deliverable. Use short headers and bullets only when they improve clarity.
- Specific over vague. Exact dates for time-sensitive work. Browse and cite current claims.
- Minimal over feature-rich. Speed over polish. Context over rigid structure.
- Clean, crafted, non-generic design. Show working artifacts, not abstract promises.
- Apple-first when practical. Standalone or tap-first tools for frontline use are often preferred.
- Hashtags may aid capture, but Riley does not maintain a tagging or filing system.
- Preserve raw material in CAPTURE mode; synthesize a structured deliverable in BUILD mode.
- Do not surface `#sidebar` or `#askme` items unless Riley explicitly asks for them.

### System design requirements

- Riley may dump first and organize never. Agents own inference, naming, routing, filing, status reconciliation, and follow-through.
- No new dashboard, recurring manual filing, tagging requirement, confirmation loop, or active model automation is required for normal context operation.
- Fix the reusable system instead of adding recurring manual gap-filling.
- Keep secrets, credentials, private account data, raw personal captures, large media, caches, dependencies, and build outputs out of Git.
- Public/shared artifacts expose the durable result, not arbitrary draft bodies.

## PROJECT LIBRARY AND PARALLEL WORK

`RileyProjects/` is the shared agent-visible library for active, unfinished, finished, archived, and experimental projects.

- If ownership is clear, project material belongs directly under `RileyProjects/<PROJECT_NAME>/`.
- If ownership is unclear, use `RileyProjects/_GLOBAL_DROP/` temporarily and route it when identified.
- iCloud is source/archive material. Obsidian is the map. Handoffs are summaries. None replace the canonical project folder.
- Bulky or private artifacts stay on an explicit local/iCloud artifact shelf with a small committed manifest when future agents need provenance.
- A project README should state purpose, current status, important files, and open loops.

Parallel agent work must use `AGENT_WORK.md` when variants, machines, cloud apps, or agents overlap. Label workstreams `canonical`, `variant`, `archive`, or `manifest-only`. Never put two live implementations in the same path. Use isolated variants when needed, record conflict notes, and write a merge decision before replacing canonical source.

## AGENT AUTHORITY AND HANDOFFS

- Filesystem-capable agents may implement requested durable work in approved repo paths and own preflight, reconciliation, commit, push, and parity verification.
- Cloud/chat-only agents should write a durable handoff to `CONTEXT_HUB/captures/inbox/` or the iCloud hot drop when their surface allows it.
- A handoff is closed-loop execution: the initiating owner sends, receives, reviews, iterates or falls back, then completes the project outcome.
- Handoffs name existing drafts, scripts, deliverables, their status and purpose, and whether the receiver should locate, assess, refine, or replace them.
- Frontend design currently routes to Claude first when available; Codex reviews and continues when Claude is unavailable or reaches limits. This is a task-routing preference, not exclusive repository authority.
- No agent should ask Riley to copy routine prompts, run Git commands, or remember machine synchronization steps.

## DURABLE WORKFLOW RULES

- Daily AI Brief: read `RileyProjects/AIAudioBrief/CODEX_AI_BRIEF_WORKFLOW.md` and `SCRIPT_STYLE_GUIDE.md`; NotebookLM remains a deliberate manual composition boundary, and final `.txt` output requires the matching supplied `.m4a` plus transcription, fact-checking, and validators.
- Final recording scripts require a verified plain `.txt` teleprompter artifact; Markdown is editorial support.
- The Riley File revisions preserve the existing thesis and direct conversational single-speaker delivery. Verify first-person operational examples with Riley before turning repo artifacts into case studies.
- Locked-source scripture work stays inside its declared canonical references and corpus.
- Clone-training audio keeps raw, pending-QA, and approved states; Riley's headphone confirmation is required before approval.
- Final PDFs and designed documents must use the authoritative repo production skills, be rendered, visually inspected, revised, and verified before delivery.

## DURABLE CONTEXT UPDATES

Only explicit, privacy-screened durable facts appear here. Captures, source paths, and private drafts remain local.

- No durable context updates.
