# Phase 2 — Non-protocol file merge

For each file in the "other" bucket from Phase 1, decide what happens to it.

## Per-file question

Use `AskUserQuestion` for each non-protocol file (batch when sensible).

Options:
- **Brain docs** — move into `brain/docs/<filename>` (or `brain/docs/detail/<filename>` for deep dives on one specific feature/flow) because the file is project documentation that all agents should be able to read (feature notes, integration docs, architecture supplements, domain reference, how-we-work notes). The file is also registered in `brain/docs/INDEX.md` Key Files and root `CLAUDE.md` `## Extended Context` — same rules the `add-context` skill uses (see below).
- **Merge** — extract content into a protocol file (mapping table below).
- **Reference** — add a one-line pointer in root CLAUDE.md; leave file untouched.
- **Leave** — no changes, no reference.
- **Skip** — stale or generated; ignore entirely.

Rule of thumb when the user is unsure:
- If the file talks about *how* the work gets done OR *what* gets built / *how it works* → Brain docs.
- If the file talks about a single small fact that belongs in a protocol file → Merge.
- If the file is too long to merge cleanly but useful to point at → Reference.

## Merge destination mapping

| Source file pattern | Merge destination |
|---|---|
| README.md (project overview) | "What this is" section of root CLAUDE.md |
| README.md (setup / install) | `brain/BRIEF.md` tech stack section |
| CONTRIBUTING.md (coding rules) | `brain/BRIEF.md` (note as a locked coding-standard decision) |
| ARCHITECTURE.md (legacy) | Reference in root CLAUDE.md |
| DESIGN.md (legacy, not in brain/) | Reference, then Phase 4 handles `brain/DESIGN.md` |
| CHANGELOG.md (legacy at root) | Extract recent decisions → new version block in `brain/BRIEF.md` |
| HISTORY.md | Same as CHANGELOG.md |
| TODO.md, TASKS.md | Extract open items → `brain/STATUS.md` Next Actions |
| docs/*.md API/reference | Reference in `brain/docs/INDEX.md` Key Files |
| Any file > 100 lines | Reference, don't merge |

**Rule:** When in doubt, prefer **Brain docs** (or Reference) rather than Merge — never silently drop content into a protocol file you can't trace later.

## What "Brain docs" means

Move the file into `brain/docs/<filename>` (or `brain/docs/detail/<filename>` if it's a deep dive on one specific feature or flow). Then immediately cross-reference:

- **`brain/docs/INDEX.md`** — find the Key Files section/table and add:
  ```
  | brain/docs/<filename> | <one-line: what this file contains — read before <trigger condition> |
  ```
  If `brain/docs/INDEX.md` doesn't exist yet (will be created in Phase 5), buffer the entry and write it during Phase 5.
- **Root `CLAUDE.md`** — find or create `## Extended Context` section and append:
  ```
  - `brain/docs/<filename>` — <one-line description>. Read before <trigger condition>.
  ```

This matches the `add-context` skill's cross-referencing pattern so every brain-docs file is discoverable.

Use this for: feature notes, integration docs, architecture supplements, domain reference, API references, how-we-work notes, anything that explains *what is being built*, *how something works*, or *how the work gets done*.

## What "Reference" means

Add a one-line pointer in root CLAUDE.md under a `## Reference files` section. The actual file is left alone — neither moved nor edited.

```markdown
## Reference files
- `LEGACY-ARCHITECTURE.md` — old system design diagram; read when investigating pre-rewrite behavior
- `docs/API.md` — REST endpoint reference (15 endpoints)
```

Use this when the file is too long to merge cleanly, or the user wants it to stay in its current location.

## What "Merge" means

Extract content into the target protocol file. Cite the source inline:

```markdown
## What this is
[content merged from former README.md project overview]
```

After merge, the source file can be deleted OR kept as `LEGACY-<name>.md` per user choice.

## Output of Phase 2

A decision table mapping every non-protocol file → action (brain-docs / merge / reference / leave / skip) + destination. Pass to Phase 3 for execution. Any brain-docs cross-references not yet written (because `brain/docs/INDEX.md` doesn't exist) are buffered for Phase 5 to apply.
