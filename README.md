# RileyContext

Canonical knowledge base for all agents.

## Canonical file

- `RILEY_CONTEXT.md` is the only source of truth.
- All agents read from that file.
- Pipeline appends/merges daily updates and pushes to GitHub.

## Repo

- GitHub: `rileyfied/RileyContext`
- Raw URL: `https://raw.githubusercontent.com/rileyfied/RileyContext/main/RILEY_CONTEXT.md`
- Local: `~/dev/RileyContext/`

## Daily update command

```bash
./scripts/sync_context.sh
```

Pipeline runs automatically at 8am and 10pm via launchd.

## Notes

- Daily entries append under `## DAILY LOG` in `RILEY_CONTEXT.md`.
- iOS captures drop into iCloud `_move-to-dev_icloud` folder, pipeline pulls them into local inbox.
