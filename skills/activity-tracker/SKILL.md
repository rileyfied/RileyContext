---
name: activity-tracker
description: "Tracks Riley's high-level action items, tasks, and ideas across ALL sessions and agents. Auto-triggers on ANY of these: 'what were we doing', 'where were we', 'catch me up', 'what's my status', 'what did we do today', 'last thing we worked on', 'recap', 'what's open', 'what have I been working on'. Also triggers at the END of every significant interaction to log what was accomplished. If Riley asks about recent work, progress, or wants to pick up where he left off — use this skill. Even if he just says 'hey' after being away for a while, check the activity log and offer a recap."
---

# Activity Tracker

Persistent activity log that tracks high-level action items across all of Riley's sessions — Cowork, Dispatch, Claude Code (desktop & phone), Claude Chat (web & phone), remote control sessions, and cross-agent work with ChatGPT/Gemini/Codex/Sider.

## How This Relates to Other Skills

- **what-am-i-doing**: Reads pipeline state (digests, promotions, inbox). Use for "what's happening in my projects."
- **activity-tracker** (this skill): Reads the ACTION LOG — what Riley and his agents actually DID. Use for "what did we work on" / "where did we leave off."
- **context-sync**: Runs the pipeline. Use for "sync my context" / "push my context."
- **cowork-context**: Loads RileyContext for task awareness. Use at session start.

These are complementary. Activity-tracker is the ONLY one that maintains a timestamped log of completed work.
## Core Concept

Riley works across many surfaces and agents throughout the day. When he comes back to Claude (any surface), he needs to instantly know what's been happening and what's next. This skill maintains a running log of major action items and ensures they persist to memory and sync to GitHub.

## What Gets Logged

Log items that represent **distinct units of work or thought** — not sub-steps within a task:

- Project work sessions (e.g., "Analyzed 7shifts employee availability for CFA schedule project")
- New project ideas or brainstorms (e.g., "New idea: Bible trivia arcade game for CFA training")
- Decisions made (e.g., "Decided to move RileyContext canonical source from Google Drive to local")
- Reminders Riley asked for (e.g., "Reminder: Fill out 7shifts planning questionnaire when home")
- Deliverables created (e.g., "Created schedule analysis doc with 9 template recommendations")
- Research completed (e.g., "Researched RileyContext pipeline — found deadlock error in ingest step")
- Action items assigned (e.g., "Need to feed Claude 2-3 more completed CFA schedules")
- Cross-agent handoffs (e.g., "Updated RileyContext for GPT/Gemini sync")

Do NOT log:
- Individual tool calls or sub-steps
- Greetings or small talk
- Repeat entries for the same ongoing task (update the existing entry instead)
## Activity Log Location

The activity log lives at TWO locations — keep both in sync:
1. **Local repo**: `~/dev/RileyContext/ACTIVITY_LOG.md` (canonical — syncs to GitHub for cross-agent access)
2. **Cowork auto-memory**: The auto-memory activity_log.md file (for Cowork/Dispatch recall when filesystem unavailable)

If you have filesystem access (Claude Code, Cowork with Desktop Commander), always write to the local repo first, then sync to auto-memory. If no filesystem access, write to auto-memory only.

## Entry Format

```markdown
## [DATE — DAY OF WEEK]

- **[TIME] [SOURCE]** — [One-line summary]
  - Context: [What happened, what's next]
  - Status: [active | completed | waiting | reminder]
  - Tags: [#project-hashtags]
```

SOURCE values: DISPATCH, COWORK, CODE, CHAT, WEB, REMOTE, PHONE
- Use DISPATCH for task sessions spawned from Dispatch or remote phone Dispatch sessions
- Use CODE for Claude Code terminal sessions
- Use COWORK for direct Cowork desktop sessions
- Use CHAT for Claude.ai web/app chat
- Default to best guess based on available tools
## Behavior 1: Auto-Log (end of significant interactions)

After completing any significant task or conversation thread:

1. Determine if the interaction produced a loggable action item (see "What Gets Logged")
2. If yes, construct the entry with timestamp, source, summary, context, status, tags
3. Read the current activity log
4. Append under today's date header (create header if first entry today)
5. Keep only the last 14 days of entries
6. Write to local repo and auto-memory
7. If Desktop Commander available, commit and push:
   ```bash
   cd ~/dev/RileyContext && git add ACTIVITY_LOG.md && git commit -m "activity: update log" && git push
   ```

## Behavior 2: Recall (when Riley asks what's happening)

Triggers: "what were we doing", "where were we", "catch me up", "recap", "what's open", etc.

1. Read the activity log (local repo first, auto-memory fallback)
2. Present the last ~10 major items, grouped by day
3. For each: one-line summary + context
4. Highlight anything with status "waiting" or "reminder" — these need attention
5. Flag stale items (marked active but older than 3 days)
## Behavior 3: Sync (push to persistent storage)

After logging new activity:

1. **Local repo** (always when filesystem available): Write to `~/dev/RileyContext/ACTIVITY_LOG.md`, git commit + push
2. **Auto-memory** (always): Update the activity_log.md memory file
3. **RILEY_CONTEXT.md** (when significant): If major project progress, update the activity log section of RILEY_CONTEXT.md too — this is what ChatGPT/Gemini/Sider read

## Hashtag Recognition

Match content to Riley's known project hashtags:
- #youtube #video — YouTube Channel
- #aibrief #audio #news — Daily AI Audio Brief
- #armor #scripture #bible #fighterverses — Armor App
- #harmony #piano #music — HarmonyHelper
- #conductor #monitor #agents — AI Operations Monitor
- #dashboard #productivity — RileyHQ Dashboard
- #virtualmanager #visor #cfa — Virtual Restaurant Manager
- #cfa #schedule #7shifts — CFA Scheduling
- #context #pipeline — RileyContext Infrastructure

New hashtags: add to the entry and flag "New tag: #newtag — not yet mapped to a project."

## Behavior 4: Ingest RileyNotes Captures

Riley captures notes from his iPhone via the RileyNotes app. These land in:
`~/Library/Mobile Documents/com~apple~CloudDocs/_move-to-dev_icloud/`

When running Behavior 2 (Recall), also scan this folder for new files:

1. List all files in the drop folder
2. Read any .txt files, especially those with hashtags in the filename
3. Priority tags: #Claude #Prompt #BuildIt #Ingest — these are direct requests for Claude to act on
4. Include relevant captures in the recall output, grouped under a "Pending Captures" section
5. For files tagged #Claude or #BuildIt: flag as actionable — Riley wants Claude to do something with these
6. For files tagged #Ingest or #Context: flag as context to absorb — add to memory or project files
7. For non-text files (PDFs, images, videos): note their existence and filename but dont try to read them unless asked
8. After processing, suggest whether captures should be moved to the RileyContext inbox (`~/dev/RileyContext/CONTEXT_HUB/captures/inbox/`)

The filenames ARE the hashtags. A file named `#claude #article #ingest #context.txt` has tags: #claude, #article, #ingest, #context.

## Principles

1. **Be proactive, not prompted.** Log activity automatically after significant work. Don't wait to be asked.
2. **High-level only.** "Analyzed employee availability" — not "Read PDF, ran search, parsed results, created CSV."
3. **Context is king.** The summary orients Riley. The context line tells him what's next.
4. **Cross-session continuity.** When Riley returns after being away, offer a recap without being asked.
5. **Don't duplicate.** If an action item exists for the same work, update it — don't create a new entry.