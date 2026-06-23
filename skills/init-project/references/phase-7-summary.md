# Phase 7 — Final summary

Surface everything that needs user attention after init-project completes. The summary varies slightly by mode (from Phase 0):

- `audit` — report what was filled in vs. what was already populated.
- `empty` — include the bootstrap answer object and every `[VERIFY]` item produced because of "skip"/"undecided" answers.
- `fresh` — standard output (below).

(Old three-folder / flat-root projects never reach Phase 7 — Phase 0 hands them off to `migrate-to-brain`.)

## Output (fresh)

```
✅ Init complete — brain/ layout created.

Created:
  Root: CLAUDE.md, README.md
  brain/: .plugin-version, STATUS, BRIEF (stub), WONT-DO (stub), ROADMAP, BRAND ([VERIFY]),
          FUNDAMENTALS (global standard), DESIGN ([VERIFY]), DISCOVERIES, SITUATIONS,
          WORKLOG, CHANGELOG, agenda (stub), docs/INDEX, docs/detail/README

Phase 2 decisions applied:
  [list each brain-docs / merge / reference / leave / skip action taken]

Extended context added:
  [list any brain/docs/ files created in Phase 6, or "none"]

Sub-agent runs used:
  [list which Haiku/Sonnet sub-agents fired, for transparency]
```

## Output (empty bootstrap)

```
✅ Init complete — brain/ layout created from bootstrap answers.

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
  Root CLAUDE.md "What this is", README.md opening, brain/STATUS.md current sprint,
  brain/BRIEF.md v1.0 (What we're building / Tech stack / Architecture decisions),
  brain/ROADMAP.md Direction.

Still placeholder ([VERIFY] markers):
  [list each]
```

## Output (audit)

```
✅ Audit complete — brain/ layout already present.

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

1. brain/BRAND.md fields marked [VERIFY] — confirm or correct.
2. brain/DESIGN.md fields marked [VERIFY] — confirm or correct color tokens.
3. brain/docs/INDEX.md items marked [VERIFY] — confirm or correct.
4. brain/BRIEF.md v1.0 block — fill in tech stack, architecture decisions, scope, open questions.
5. brain/WONT-DO.md — empty. Add a line each time you reject an option, with a one-line reason.
6. brain/agenda.md — empty. Will be populated as you plan your first chapters.

📋 Reminder for BRIEF.md:
  A stub was created for brain/BRIEF.md. Drop key decisions in it when you have a moment.
  Don't ask an agent to populate BRIEF.md unsupervised — it's human-curated.
```

## Author-stamp reminder

```
✍  Authorship convention:
  Every WORKLOG, BRIEF, and CHANGELOG entry is stamped with who wrote it —
  · Cowork, · Codex, or · Claude Code. There is no tier folder; the stamp is how
  authorship stays visible inside the single brain/ folder.
```

## Codex setup reminder (one-time)

```
🔧 If you're using Codex on this project, add one line to ~/.codex/config.toml:

  project_doc_fallback_filenames = ["CLAUDE.md"]

This makes Codex read CLAUDE.md automatically — same as Claude Code.
One-time setup, applies to all projects.
```

## Final reminders

1. **brain/FUNDAMENTALS.md is a global standard** — never edit it. It updates with the plugin.
2. **Lock-before-act discipline:** for any decision in this project going forward, write it in `brain/BRIEF.md` BEFORE acting on it. Rejected options go in `brain/WONT-DO.md`.
3. **Cascade-before-derive:** when you change `brain/BRIEF.md` or `brain/ROADMAP.md`, the changes need to flow through to `brain/STATUS.md` and `brain/agenda.md`.
4. **Audit before close:** every chapter / task / work unit gets an independent re-read of the spec before being marked done.
5. **One folder, one home.** Every canon file lives once inside `brain/`. Don't recreate the old folder split.

## When this skill ends

Hand back control to the user. They take it from here — typically:
- Open the relevant tool (Cowork chat for first orchestration session).
- Tell Cowork: "Start by locking decisions in `brain/BRIEF.md` v1.0."
- Then proceed via the `discipline` skill for any further edits.
