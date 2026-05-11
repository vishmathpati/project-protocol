# Phase 7 — Final summary

Surface everything that needs user attention after init-project completes.

## Output

```
✅ Init complete — three-folder layout created.

Created:
  Root: CLAUDE.md, README.md
  cowork/: CLAUDE, STATUS, BRIEF (stub), WORKLOG, CHANGELOG
  agents/: STATUS, BRIEF (stub), ROADMAP, BRAND ([VERIFY]), FUNDAMENTALS (global standard), DESIGN ([VERIFY]), DISCOVERIES, WORKLOG, CHANGELOG, docs/INDEX, docs/detail/README
  human/: agenda.md (stub)

Phase 2 decisions applied:
  [list each merge/reference action taken]

Extended context added:
  [list any agents/docs/ files created in Phase 6, or "none"]

Sub-agent runs used:
  [list which Haiku/Sonnet sub-agents fired, for transparency]
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
