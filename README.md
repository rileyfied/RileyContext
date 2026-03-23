# RileyFile

Canonical knowledge base for all agents.

## Canonical file

- `RILEY_CONTEXT.md` is the only source of truth.
- All agents read from that file.
- Only Codex appends/merges daily updates and pushes.

## Daily update command

```bash
./scripts/eod_append.sh path/to/drop.md [SOURCE]
```

`SOURCE` defaults to `UNKNOWN`.

## Notes

- Daily entries append under `## DAILY LOG` in `RILEY_CONTEXT.md`.
- Legacy/duplicate workflows are quarantined in `/_deprecated/`.
