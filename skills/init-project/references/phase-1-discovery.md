# Phase 1 — Discovery

Find every `.md` file in the project and bucket it by audience.

## 1a. Glob for markdown

Use Glob to find every `.md` file. Exclude `node_modules/`, `.git/`, `vendor/`, `dist/`, `build/`.

For large projects (>200 markdown files), spawn a fast-tier sub-agent:

```
Task(
  prompt="Glob '**/*.md' under project root, exclude node_modules, .git, vendor, dist, build. List every path one per line, sorted.",
  subagent_type="general-purpose",
  model="haiku"
)
```

## 1b. Bucket the files

Separate every file into three buckets:

**Protocol files** (Phase 3 handles):
- Root `CLAUDE.md`, root `README.md`
- `STATUS.md`, `BRIEF.md`, `WORKLOG.md`, `CHANGELOG.md` (any location)
- `ROADMAP.md`

**Design system files** (Phase 4 handles):
- `BRAND.md`, `FUNDAMENTALS.md`, `DESIGN.md`, `DISCOVERIES.md`

**Other** (Phase 2 handles):
- README.md if not at root, CONTRIBUTING.md, ARCHITECTURE.md, NOTES.md, legacy docs/ files outside `agents/docs/`, etc.

## 1c. Summarize "other" files

For every non-protocol file, read and produce a one-line summary.

For 5+ "other" files, spawn a Haiku sub-agent:

```
Task(
  prompt="Read each file below and produce one-line summary per file. Format: 'path — summary'. [list of paths]",
  subagent_type="general-purpose",
  model="haiku"
)
```

Example output:
```
README.md         — project overview, setup, feature list
ARCHITECTURE.md   — system design, component diagram
NOTES.md          — scratch notes, mostly outdated
docs/API.md       — REST endpoint reference, 15 endpoints
```

## 1d. Detect existing layout

Check whether the project already has the three-folder layout:

```bash
[ -f CLAUDE.md ] && [ -f README.md ] && [ -d cowork ] && [ -d agents ] && [ -d human ]
```

If yes — this is an **audit run**, not fresh init. Set the audit flag and:
- Read existing files; do not overwrite populated content
- Only fill missing files
- Report layout mismatches at Phase 7

If no — proceed with fresh init.

## Output of Phase 1

Three bucket lists + the "other" summary table + audit-flag boolean. Pass these to Phase 2.
