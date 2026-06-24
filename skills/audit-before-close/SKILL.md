---
name: audit-before-close
description: End-of-work verification gate. Before marking any chapter, task, or feature complete, re-read the contract, compare against implementation, and surface drift or scope creep.
allowed-tools: Read, Glob, Grep
---

# Audit Before Close

The last gate. Before marking work done, verify it actually matches the spec.

---

## When this fires

- About to mark a chapter or task complete.
- About to update `brain/STATUS.md` to remove an item from "in progress".
- About to write a `CHANGELOG.md` entry that says something shipped.
- About to tell the user "this is done".
- Slash command: `/audit-close`

---

## The protocol

**1. Open the original contract/spec.** The `brain/BRIEF.md` version block for this chapter, the Goal/contract section at the top of the active chapter file in `brain/chapters/`, a PRD the user names, or whatever defined "done" for this work. If none of those exist, ask the user: "What was the contract for this work?"

**2. List the requirements.** Extract each requirement from the spec as a one-line item.

**3. Open the implementation files.** The actual files that were changed.

**4. Match line by line.** For each requirement: does the implementation satisfy it? State yes/no for each.

**5. Surface drift.** Any of:
- Missing items (spec said do X, code doesn't do X).
- Scope creep (code does Y, spec didn't ask for Y).
- Hidden assumptions (code assumes Z, spec didn't lock Z).

State each clearly. Do not gloss.

**6. User confirmation.** Show the audit findings. Wait for explicit "satisfied, close it" before updating `brain/STATUS.md` / `CHANGELOG.md` / closing the chapter.

**7. If not satisfied:** capture the gap as a new `brain/BRIEF.md` version block and return the chapter to active status. Do not silently close incomplete work.

---

## Why it exists

Sloppy closures compound. Once "done" is wrong, the next chapter builds on a faulty foundation. This skill makes the closure gate mechanical so drift surfaces before it sets.

---

## Difference from `discipline`

`discipline` is the gate BEFORE acting. `audit-before-close` is the gate AT THE END of work. Different moments. Both apply to non-trivial work.
