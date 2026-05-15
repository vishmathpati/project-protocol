# Phase 1 — Discovery

Find every `.md` file in the project and bucket it by audience.

> **Note:** Phase 0 (mode detection) runs upstream of this phase and sets the mode. Phase 1 only runs for `mode = fresh` or `mode = audit`. For `mode = empty`, Phase 1 is skipped — the bootstrap answer object from Phase 0a is passed straight to Phase 3. For `mode = migration`, Phase 0b runs first and Phase 1 only buckets the non-standard markdown files Phase 0b passed forward.

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

## 1d. (Moved upstream)

Layout detection used to live here but now runs in Phase 0 (mode detection). By the time Phase 1 runs, the mode and audit flag are already known. If `audit_flag = true`, Phase 1 still buckets every markdown file but Phases 3–6 only fill missing files and never overwrite populated content.

## Output of Phase 1

Three bucket lists (protocol files, design system files, other) + the "other" summary table. Pass to Phase 2. Audit flag and mode are carried forward from Phase 0.
