---
name: context-sync
description: Force a full RileyContext pipeline run and report what was promoted and merged. Use when Riley says "sync my context", "run the pipeline", "push my context", "update context", "ingest captures", or after any significant work session. ALWAYS includes: drop folder ingest, captures ingest, RILEY_CONTEXT.md update, git push, and live URL verification.
---

# Force Context Sync

Full pipeline run — covers drop folder, captures, context update, push, and live verification.

## Step 1 — Check if we're on the laptop

If running remotely (iPhone app, remote session), SSH first:
```bash
ssh rileycolleyFW@192.168.1.50
```

## Step 2 — Ingest drop folder captures

Pull any new files from both drop folders into the local inbox:
```bash
ICLOUD_DROP="$HOME/Library/Mobile Documents/com~apple~CloudDocs/_move-to-dev_icloud"
GDRIVE_DROP="$HOME/Library/CloudStorage/GoogleDrive-rileygcolley@gmail.com/My Drive/move-to-dev_google-drive"
INBOX="$HOME/dev/RileyContext/CONTEXT_HUB/captures/inbox"

# List new files before moving
ls "$ICLOUD_DROP" 2>/dev/null
ls "$GDRIVE_DROP" 2>/dev/null

# Move to inbox
[ -d "$ICLOUD_DROP" ] && mv "$ICLOUD_DROP"/* "$INBOX"/ 2>/dev/null
[ -d "$GDRIVE_DROP" ] && mv "$GDRIVE_DROP"/* "$INBOX"/ 2>/dev/null
```

Read and summarize any new .txt captures. Flag files tagged #Claude, #BuildIt, #Ingest, or #Context as actionable.

## Step 3 — Read CONTEXT_HUB/captures inbox

```bash
ls "$HOME/dev/RileyContext/CONTEXT_HUB/captures/inbox/"
ls "$HOME/dev/RileyContext/CONTEXT_HUB/captures/_processed/"
```

Read any unprocessed captures. Add relevant content to RILEY_CONTEXT.md activity log and/or project context sections.

## Step 4 — Run the full pipeline

```bash
cd "$HOME/dev/RileyContext" && bash "$HOME/dev/RileyContext/scripts/sync_context.sh" 2>&1 | tee /tmp/sync_output.txt
```

Wait for it to complete. If pipeline errors or is unavailable, manually update RILEY_CONTEXT.md:
- Bump "Last Updated" date to today
- Add today's activity log entries (sync from ACTIVITY_LOG.md)
- Update any active project statuses that changed this session

## Step 5 — Commit and push

```bash
cd "$HOME/dev/RileyContext" && git add -A && git commit -m "context: sync [DATE] session" && git push
```

If git push fails, diagnose and retry. Do not mark sync complete until push succeeds.

## Step 6 — Verify live URL

Fetch the raw GitHub URL and confirm the content is fresh:
```
https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md
```

Check that "Last Updated" matches today's date. If still stale (CDN cache), note the delay and tell Riley what other agents will see until cache clears (typically 2-5 min).

## Step 7 — Report

```
SYNC COMPLETE — [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Drop folder captures:  [N new files / filenames]
Inbox captures:        [N processed]
Context updated:       [yes/no]
Git push:              [success / failed — commit hash]
Live URL verified:     [yes — Last Updated: DATE / no — CDN stale, clears ~Xmin]
Errors:                [none / list]
```

If errors found, suggest running `/rileyfile-debug`.
If git push failed, show the error and offer to retry.
If CDN is stale, advise Riley what other agents are currently seeing.
