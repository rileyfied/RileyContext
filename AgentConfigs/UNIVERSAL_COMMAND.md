# /RileyContext — Universal Sync Command

## What it does
When Riley types `/RileyContext`, fetch and load his canonical context file. This keeps all AI agents in sync with his current projects, preferences, and system.

## Context URL
```
https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md
```

## Instructions for each model

### ChatGPT / Gemini / Codex / any URL-capable model
When Riley types `/RileyContext`:
1. Fetch: `https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md`
2. Load as session background context
3. Respond: `Context loaded — [today's date]`
4. State which project you're working on (if one is specified)

### Sider (no URL fetch)
When Riley types `/RileyContext`:
1. Confirm "Riley Context Hub" Wisebase is your active chat source
2. Respond: `Context loaded from Wisebase — [today's date]`
3. If Wisebase feels stale, say: "Context may be stale — please refresh Wisebase"

### Claude Code (this session)
`/RileyContext` runs the `cowork-context` skill — reads local `~/dev/RileyContext/` files directly.

---

## Paste into model custom instructions / system prompts

> **For ChatGPT "Custom Instructions" or "About Riley" section:**
>
> My context system is called RileyContext. When I type `/RileyContext`, fetch this URL and load it as background context, then confirm "Context loaded — [date]":
> `https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md`
> Also respond to `/context` the same way.

> **For Gemini Gems / system instructions:**
>
> Riley uses a context system called RileyContext. When he types `/RileyContext` or `/context`, fetch and load:
> `https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md`
> Confirm with: "Context loaded — [date]"

> **For Codex / any OpenAI model:**
>
> When the user types `/RileyContext`, fetch `https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md` and treat it as session context. Confirm: "Context loaded — [date]"

---

## Note on old customization rules in web models

If a web model (ChatGPT, Gemini, etc.) has old pipeline instructions referencing:
- `~/dev/rileyfile/` — outdated path, now `~/dev/RileyContext/`
- `rileyfied/rileyfile` GitHub repo — outdated, now `rileyfied/RileyContext`
- Google Drive or iCloud as canonical storage — outdated, now local-first

**Delete those old instructions and replace with the paste blocks above.** Agents cannot auto-update their own system prompts — you must update them manually in each model's settings.
