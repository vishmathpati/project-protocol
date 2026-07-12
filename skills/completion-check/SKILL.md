---
name: completion-check
description: End-of-work contract verification before a chapter, task, or feature is called complete. Compare the implemented result and evidence with the original chapter, brief, and execution decisions.
allowed-tools: Read, Glob, Grep
---

# Completion Check

The last gate. Before marking work done, verify it actually matches the spec.

---

## When this fires

- About to mark a chapter or task complete.
- About to update `brain/STATUS.md` to remove an item from "in progress".
- About to write a `CHANGELOG.md` entry that says something shipped.
- About to tell the user "this is done".
- Slash command: `/completion-check`

---

## The protocol

**1. Open the original contract.** Prefer the chapter Goal, Done When, Constraints, and Page Execution Decisions, plus relevant BRIEF or named specifications. If no durable contract exists, report that completion cannot yet be proven.

**2. List the requirements.** Extract each requirement from the spec as a one-line item.

**3. Read the evidence.** Read the Completion Report, verification results, diff summary, and only the changed hunks needed to answer the contract questions.

**4. Match line by line.** For each requirement: does the implementation satisfy it? State yes/no for each.

**5. Surface drift.** Any of:
- Missing items (spec said do X, code doesn't do X).
- Scope creep (code does Y, spec didn't ask for Y).
- Hidden assumptions (code assumes Z, spec didn't lock Z).

State each clearly. Do not gloss.

**6. Return a verdict.** `pass`, `pass with follow-up`, or `fail`. This check does not approve a worker branch; the CEO owns approval.

**7. If not satisfied:** return specific gaps to the executing role. Do not rewrite BRIEF, STATUS, CHANGELOG, or a chapter verdict.

---

## Why it exists

Sloppy closures compound. Once "done" is wrong, the next chapter builds on a faulty foundation. This skill makes the closure gate mechanical so drift surfaces before it sets.

---

## Difference from `change-check`

`change-check` protects scope before consequential work. `completion-check` proves finished work against its contract. Save Session persists state; Project Audit checks system drift.
