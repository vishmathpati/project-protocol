# Phase 2 — Non-protocol file merge

For each file in the "other" bucket from Phase 1, decide what happens to it.

## Per-file question

Use `AskUserQuestion` for each non-protocol file (batch when sensible).

Options:
- **Merge** — extract content into a protocol file
- **Reference** — add a one-line pointer in root CLAUDE.md; leave file untouched
- **Leave** — no changes, no reference
- **Skip** — stale or generated; ignore entirely

## Merge destination mapping

| Source file pattern | Merge destination |
|---|---|
| README.md (project overview) | "What this is" section of root CLAUDE.md |
| README.md (setup / install) | agents/CLAUDE.md tech stack section |
| CONTRIBUTING.md (coding rules) | agents/CLAUDE.md coding standards |
| ARCHITECTURE.md (legacy) | Reference in root CLAUDE.md |
| DESIGN.md (legacy, not in agents/) | Reference, then Phase 4 handles agents/DESIGN.md |
| CHANGELOG.md (legacy at root) | Extract recent decisions → new version block in agents/BRIEF.md |
| HISTORY.md | Same as CHANGELOG.md |
| TODO.md, TASKS.md | Extract open items → agents/STATUS.md Next Actions |
| docs/*.md API/reference | Reference in agents/docs/INDEX.md Key Files |
| Any file > 100 lines | Reference, don't merge |

**Rule:** When in doubt, reference rather than merge.

## What "Reference" means

Add a one-line pointer in root CLAUDE.md under a `## Reference files` section:

```markdown
## Reference files
- `LEGACY-ARCHITECTURE.md` — old system design diagram; read when investigating pre-rewrite behavior
- `docs/API.md` — REST endpoint reference (15 endpoints)
```

The actual file is left alone — neither moved nor edited.

## What "Merge" means

Extract content into the target protocol file. Cite the source inline:

```markdown
## What this is
[content merged from former README.md project overview]
```

After merge, the source file can be deleted OR kept as `LEGACY-<name>.md` per user choice.

## Output of Phase 2

A decision table mapping every non-protocol file → action (merge/reference/leave/skip) + destination. Pass to Phase 3 for execution.
