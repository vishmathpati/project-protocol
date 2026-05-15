# Phase 0b — Old-version migration

Runs only when Phase 0 classifies the project as **migration mode** (Mode B) — the project is on the older flat-root layout of project-protocol. The goal is to move every existing protocol file into the three-folder layout while preserving all user content, then let the remaining phases layer in any new files this plugin version adds.

---

## Non-negotiable principles

1. **Preserve user content.** Nothing the user wrote is deleted or overwritten. Old content gets repositioned, not replaced.
2. **Mechanical first, ask only when ambiguous.** Files with a single clear destination move automatically. Files that could go to more than one tier surface a question.
3. **Layer, don't replace.** New files this plugin version introduces (e.g., `agents/docs/INDEX.md`, `cowork/CHANGELOG.md` if missing) are added on top of the migrated content, not in place of it.
4. **Confirm before destructive moves.** Show the full migration plan before any file moves, and ask for go-ahead.
5. **No file is silently dropped.** Every markdown file at root and in `docs/` is accounted for in the plan — either moved, classified, referenced in place, or explicitly skipped.

---

## 0b.1 — Build the migration plan

### Clean-match table (no question needed)

| Source (old layout) | Destination (new layout) | Notes |
|---|---|---|
| `ROADMAP.md` | `agents/ROADMAP.md` | Direct move. Project canon. |
| `BRAND.md` | `agents/BRAND.md` | Direct move. |
| `DESIGN.md` | `agents/DESIGN.md` | Direct move. Phase 4 may add the YAML frontmatter if missing. |
| `DISCOVERIES.md` | `agents/DISCOVERIES.md` | Direct move. Append-only — no edits. |
| `FUNDAMENTALS.md` | `agents/FUNDAMENTALS.md` | Plugin standard — silently replaced with the current template (see Phase 4). |
| `agenda.md` | `human/agenda.md` | Direct move. |
| `README.md` at root | Stays at root | Phase 3 may extend it with the file-dependency map if missing. |

### Ambiguous files (classify with a sub-agent)

`STATUS.md`, `BRIEF.md`, `WORKLOG.md`, `CHANGELOG.md` could be orchestration-tier or project-canon-tier — in the old single-tier layout there was no distinction. Run a Haiku classifier on each:

```
Task(
  prompt="Read this file. Classify its content as ORCHESTRATION (how the user and agents work together, session discipline, cross-tool coordination, decisions about process) or PROJECT-CANON (what's being built, product decisions, sprint state, technical worklog, feature notes). If a single file mixes both, identify the split as roughly N% orchestration / N% canon and quote two short examples of each. Output: classification + brief reasoning + (if mixed) the split.",
  subagent_type="general-purpose",
  model="haiku"
)
```

Map results:
- **Pure ORCHESTRATION** → `cowork/<filename>` (single move, no question).
- **Pure PROJECT-CANON** → `agents/<filename>` (single move, no question).
- **Mixed** → surface the file to the user with the sub-agent's split estimate:

```
<filename> looks like roughly N% orchestration content and M% project canon.

How would you like to handle it?

A — Move the whole file to cowork/<filename>
B — Move the whole file to agents/<filename>
C — Split it: orchestration parts to cowork/<filename>, canon parts to agents/<filename> (I'll show the proposed split before writing)

Or describe what you want.
```

If C: a second sub-agent (Sonnet — judgment) does the actual split, returning two file contents. Show the preview side-by-side before writing.

### Root `CLAUDE.md` split

The old single root `CLAUDE.md` typically mixes three things:
1. Global rules + folder map that every agent must follow.
2. Cowork-specific orchestration discipline (when to discuss vs. act, lock-before-cascade, read-back rules, tier loading, sub-agent rules).
3. Project canon notes for Claude Code / Codex (tech stack, project-specific coding standards, feature flow guidance, vault locations, gotchas).

Run a Haiku sub-agent to segment:

```
Task(
  prompt="Read root CLAUDE.md. Identify three categories of content and quote the exact text under each: (1) global rules every agent must follow + the folder/file map; (2) Cowork-specific orchestration discipline (discussion mode, lock-before-cascade, read-back, tier loading, sub-agent routing); (3) project-canon notes belonging to Claude Code / Codex (tech stack, project coding standards, feature flow guidance, locations, gotchas). Some sections may belong nowhere — flag those separately as 'unclassified'. Output: four labeled sections with the exact source text under each.",
  subagent_type="general-purpose",
  model="haiku"
)
```

Map results:
- Category 1 → stays at root `CLAUDE.md` (the existing root template).
- Category 2 → appended into `cowork/CLAUDE.md` under the template's existing sections.
- Category 3 → routed conservatively into `agents/BRIEF.md` Notes section (or split across `agents/STATUS.md` / `agents/docs/INDEX.md` if the user prefers). When in doubt, route everything in Category 3 to `agents/BRIEF.md` so nothing is lost.
- Unclassified → presented to the user verbatim with three options: (A) keep at root, (B) move to a specific destination they pick, (C) drop.

Show the user the proposed split before writing. The user can accept as-is, hand-edit boundaries, or override per category.

### Non-standard markdown files

Any markdown file at root or in `docs/` that does NOT match a standard protocol filename is non-standard. Phase 0b records these for Phase 2 to handle — Phase 2 has been extended to offer cowork / agents/docs / merge / reference / leave / skip options (see `phase-2-non-protocol-merge.md`).

Phase 0b does not ask about these files itself — it just collects the list and passes it forward.

---

## 0b.2 — Show the migration plan

Output a table to the user before any file is moved. Example:

```
Migration plan

  Clean moves (no question):
    ROADMAP.md         →  agents/ROADMAP.md
    BRAND.md           →  agents/BRAND.md
    DESIGN.md          →  agents/DESIGN.md
    DISCOVERIES.md     →  agents/DISCOVERIES.md
    agenda.md          →  human/agenda.md
    FUNDAMENTALS.md    →  agents/FUNDAMENTALS.md (replaced with current plugin standard)

  Classified by sub-agent:
    STATUS.md          →  agents/STATUS.md   (project-canon — confidence high)
    BRIEF.md           →  agents/BRIEF.md    (project-canon — confidence high)
    WORKLOG.md         →  cowork/WORKLOG.md  (orchestration — confidence high)
    CHANGELOG.md       →  Split — ~60% to cowork/CHANGELOG.md, ~40% to agents/CHANGELOG.md
                          [I'll show you the proposed split before writing]

  Root CLAUDE.md split (3 categories detected):
    Global rules + folder map  →  stays at root CLAUDE.md
    Cowork discipline section  →  appended to cowork/CLAUDE.md
    Project canon notes        →  appended to agents/BRIEF.md Notes section
                                  [I'll show you the proposed split before writing]

  Non-standard markdown (Phase 2 will ask per file):
    ARCHITECTURE.md
    NOTES.md
    docs/API.md
    docs/team-conventions.md

  New files this version adds (created only if missing):
    Root: README.md (file-dependency map)
    cowork/: CLAUDE.md, STATUS.md, BRIEF.md, CHANGELOG.md
    agents/: WORKLOG.md, CHANGELOG.md
    agents/docs/: INDEX.md, detail/README.md

Proceed?
  A — Yes, run the plan as shown
  B — Yes, but I want to adjust some destinations first
  C — Cancel
```

If B: walk every "Classified by sub-agent" entry and the root `CLAUDE.md` split via `AskUserQuestion` and apply user overrides.

If C: stop the skill cleanly — no files have been moved at this point.

---

## 0b.3 — Execute the plan

In this order — each step must complete before the next begins:

1. **Create the three folders:**
   ```bash
   mkdir -p cowork agents human agents/docs/detail
   ```
2. **Apply clean moves.** For each entry in the clean-match table, read the source content, write it to the destination, then delete the source. Never use shell `mv` blindly — always read-then-write so the content is in your context if anything fails.
3. **Apply classified moves.** For pure-classified files, same read-then-write pattern. For mixed/split files, write both target files from the sub-agent's split output.
4. **Apply the root `CLAUDE.md` split.** Write the segmented content into root, `cowork/CLAUDE.md`, and `agents/BRIEF.md` (or wherever Category 3 was routed by the user).
5. **Create any missing new-version files** from Phase 3 templates — but only files that don't exist yet after steps 2–4. Never overwrite a migrated file.

For step 5, set a flag on every migrated file: `migrated = true`. Phases 3–6 must check this flag and skip overwrite even if the file appears in a template.

---

## 0b.4 — Verify

```bash
ls -la
ls cowork/ agents/ human/ agents/docs/
```

Confirm:
- The three folders exist.
- Every file in the clean-match table has moved to its destination and is no longer at root.
- Every classified file is in its destination.
- The new-version files exist where they should.
- No migrated file is missing.

If anything is missing: stop, surface the issue to the user, and do NOT continue.

---

## 0b.5 — Hand off

Continue to Phase 1 (Discovery) with `migration_complete = true` and the list of non-standard markdown files collected in 0b.1. Phase 1 records the audit-flag situation; Phase 2 picks up the non-standard list and asks per-file. Phases 3–6 run normally but skip writes for any file flagged `migrated = true`.

---

## End of Phase 0b

Output a one-line summary for Phase 7 to include in the final report:

```
Migrated from flat layout: <N> clean moves, <M> sub-agent classifications applied, root CLAUDE.md split into <X> destinations, <K> non-standard files passed to Phase 2.
```
