---
name: change-check
description: Pre-action scope and cascade check for structural, cross-cutting, destructive, or otherwise high-risk changes. Use before a change that may invalidate canon, affect several systems, or be difficult to reverse.
allowed-tools: Read, Glob, Grep
---

# Change Check

A lightweight gate for consequential changes. Routine bounded implementation does not need it.

---

## When this fires

- About to restructure files, ownership, or architecture.
- About to lock a decision into BRIEF.md.
- About to commit to a recommendation that affects multiple files.
- About to agree to a structural change.
- Slash command: `/change-check`

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

**6. Authority.** Confirm the requested action is authorized. Ask only when it expands scope or needs a material user choice.

**7. Act.** Proceed within the confirmed boundary. Log only meaningful decisions, blockers, failures, or recovery state.

---

## Skip conditions

Skip for routine, reversible, chapter-scoped edits whose dependencies and authority are already clear.

---

## Why it exists

AI agents drift when they act before verifying. This skill makes the verification mechanical and visible. The user can see exactly what the agent is about to do and stop it cheaply before bad work hits the filesystem.

---

## Difference from `completion-check`

`change-check` protects scope before consequential work. `completion-check` verifies the finished contract.
