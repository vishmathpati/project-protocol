# Phase 7 — Final summary

Surface everything that needs user attention after init-project completes. The summary varies slightly by mode (from Phase 0):

- `audit` — report what was filled in vs. what was already populated.
- `migration` — include the migration summary line from Phase 0b plus the layered-in new files.
- `empty` — include the bootstrap answer object and every `[VERIFY]` item produced because of "skip"/"undecided" answers.
- `fresh` — standard output (below).

## Output (fresh)

```
✅ Init complete — three-folder layout created.

Created:
  Root: CLAUDE.md, README.md
  cowork/: CLAUDE, STATUS, BRIEF (stub), WORKLOG, CHANGELOG
  agents/: STATUS, BRIEF (stub), ROADMAP, BRAND ([VERIFY]), FUNDAMENTALS (global standard), DESIGN ([VERIFY]), DISCOVERIES, WORKLOG, CHANGELOG, docs/INDEX, docs/detail/README
  human/: agenda.md (stub)

Phase 2 decisions applied:
  [list each cowork / agent-docs / merge / reference / leave / skip action taken]

Extended context added:
  [list any agents/docs/ files created in Phase 6, or "none"]

Sub-agent runs used:
  [list which Haiku/Sonnet sub-agents fired, for transparency]
```

## Output (empty bootstrap)

```
✅ Init complete — three-folder layout created from bootstrap answers.

Bootstrap captured:
  Project: <name>
  One sentence: <sentence>
  Target user: <user>
  Stack: <stack> [VERIFY if "undecided"]
  Stage: <stage>
  Locked decisions: <count>
  First direction: <direction>

Created:
  [same file list as fresh mode]

Populated from your answers (not placeholders):
  Root CLAUDE.md "What this is", README.md opening, cowork/STATUS.md current focus,
  agents/BRIEF.md v1.0 (What we're building / Tech stack / Architecture decisions),
  agents/ROADMAP.md Direction, agents/STATUS.md sprint line.

Still placeholder ([VERIFY] markers):
  [list each]
```

## Output (migration)

```
✅ Migration complete — three-folder layout in place. All your old content preserved.

From Phase 0b:
  <N> clean moves applied (mechanical, no questions asked)
  <M> sub-agent classifications applied
  Root CLAUDE.md split into <X> destinations
  <K> non-standard files passed to Phase 2

Phase 2 decisions applied:
  [cowork / agent-docs / merge / reference / leave / skip per non-standard file]

New files this version added (only where missing):
  [list each — these are the v1.0+ additions that didn't exist in your old layout]

Skipped (already present from migration, never overwritten):
  [list each migrated file]
```

## Output (audit)

```
✅ Audit complete — three-folder layout already present.

Filled missing files:
  [list each]

Populated files left untouched:
  [list each]

Drift / mismatch reports:
  [run the audit skill output here, by category A/B/C]
```

## Items the user needs to confirm

After the summary, list any `[VERIFY]` items and stubs that need filling:

```
👁  Needs your attention:

1. agents/BRAND.md fields marked [VERIFY] — confirm or correct.
2. agents/DESIGN.md fields marked [VERIFY] — confirm or correct color tokens.
3. agents/docs/INDEX.md items marked [VERIFY] — confirm or correct.
4. agents/BRIEF.md v1.0 block — fill in tech stack, architecture decisions, scope, open questions.
5. cowork/BRIEF.md v1.0 block — fill in orchestration decisions worth locking.
6. human/agenda.md — empty. Will be populated as you and Cowork plan your first chapters.

📋 Reminder for BRIEF.md:
  Stubs were created for both BRIEF files. Drop key decisions in them when you have a moment.
  Don't ask Cowork to populate BRIEF.md unsupervised — these are human-curated.
```

## Codex setup reminder (one-time)

```
🔧 If you're using Codex on this project, add one line to ~/.codex/config.toml:

  project_doc_fallback_filenames = ["CLAUDE.md"]

This makes Codex read CLAUDE.md automatically — same as Claude Code.
One-time setup, applies to all projects.
```

## Final reminders

1. **agents/FUNDAMENTALS.md is a global standard** — never edit it. It updates with the plugin.
2. **Lock-before-act discipline:** for any decision in this project going forward, write it in `agents/BRIEF.md` (project) or `cowork/BRIEF.md` (orchestration) BEFORE acting on it.
3. **Cascade-before-derive:** when you change `agents/BRIEF.md` or `agents/ROADMAP.md`, the changes need to flow through to `agents/STATUS.md` and `human/agenda.md`.
4. **Audit before close:** every chapter / task / work unit gets an independent re-read of the spec before being marked done.
5. **Three folders, one job each.** Don't blur the boundaries.

## When this skill ends

Hand back control to the user. They take it from here — typically:
- Open the relevant tool (Cowork chat for first orchestration session).
- Tell Cowork: "Start by locking decisions in `agents/BRIEF.md` v1.0."
- Then proceed via the `discipline` skill for any further edits.
