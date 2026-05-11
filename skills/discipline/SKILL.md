---
name: discipline
description: Pre-action gate before any non-trivial change — editing files, locking decisions, structural changes. Forces pause, declare what's changing, list cascades, verify canon, confirm before acting.
allowed-tools: Read, Glob, Grep
---

# Discipline

A 7-step gate before any non-trivial action. The skill itself does not edit anything — it forces a pause and declaration before whoever invoked it proceeds.

---

## When this fires

- About to edit a file in the project.
- About to lock a decision into BRIEF.md.
- About to commit to a recommendation that affects multiple files.
- About to agree to a structural change.
- Slash command: `/discipline`

---

## The 7 steps

**1. Stop.** Do not proceed with the action.

**2. State the action** in plain language. One sentence: "I'm about to do X."

**3. List the files** this action will modify directly.

**4. Cascade.** List every file that may become stale as a downstream effect.
- Check `README.md` cascade rules if the project has them.
- Check `docs/INDEX.md` dependency entries for the touched files.

**5. Canon check.** State whether the canon files (`CLAUDE.md`, `BRIEF.md`, `STATUS.md`, `ROADMAP.md`) currently support this action.
- If yes: name the supporting decision/section.
- If no: name the gap. The gap must be closed before the action proceeds — typically by locking a new `BRIEF.md` version block first.

**6. Read back.** Restate to the user what you understand the task to be. Wait for explicit confirmation ("go", "do it", "confirmed", "yes").

**7. Act.** Only after confirmation. Immediately after, append a `WORKLOG.md` entry for the change.

---

## Skip conditions

The user can override the gate with explicit phrases like "skip discipline, just do it" or "no gate, proceed". The skill respects this. Default behavior is the full 7 steps.

---

## Why it exists

AI agents drift when they act before verifying. This skill makes the verification mechanical and visible. The user can see exactly what the agent is about to do and stop it cheaply before bad work hits the filesystem.

---

## Difference from `audit-before-close`

`discipline` is the gate BEFORE acting. `audit-before-close` is the gate AT THE END of work. Different moments. Both apply to non-trivial work.
