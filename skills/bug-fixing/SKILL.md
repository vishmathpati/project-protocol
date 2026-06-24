---
name: bug-fixing
description: Repro-first bug discipline — build a reliable red/green reproduction BEFORE theorizing, list 3–5 ranked falsifiable hypotheses, test one variable at a time against the signal, fix, keep the repro as a regression test, clean up debug instrumentation, and record a one-line lesson in the chapter's Completion Report. The /worker and /solo roles call this on bug chapters. Triggers — "fix this bug", "it's broken", "this throws", "stack trace", "intermittent failure", "flaky test", "regression", "this used to work", "why is this happening", "reproduce the bug", "debug this".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*)
---

# Bug-fixing — Project Protocol

Practical repro-first discipline for fixing a bug. The one rule that matters most: **build the reproduction before you theorize.** A bug you can reliably trigger is a bug you can fix; a bug you're guessing at is a bug you'll "fix" three times. Used by `/worker` or `/solo` when a chapter is a bug.

There is ONE canon: `brain/`. The fix and the one-line lesson go into the chapter's Completion Report (`/worker` / `/solo` write that).

---

## Step 1 — Build a reliable reproduction FIRST

Before any theory, get the bug to happen **on demand**: one command, or a tiny throwaway test, that goes **RED on this exact bug** and will go **GREEN once it's fixed**. Spend disproportionate effort here — this is the heart of the job, not the warm-up. Do not theorize about causes before the repro exists.

Then **tighten** it: make it fast and deterministic. Strip it down to the smallest input that still triggers the bug; pin anything non-deterministic (time, ordering, randomness, network) so it fails the same way every run. A flaky repro is barely better than none.

---

## Step 2 — 3–5 ranked, falsifiable hypotheses

Before testing anything, write **3 to 5 hypotheses**, ranked most-to-least likely. Each must be **falsifiable** — it states a concrete prediction you could prove wrong (e.g. "if it's the cache, clearing it before the repro makes it pass"). "Something's off in the data layer" is not a hypothesis; "the rollup double-counts when the list is empty, so an empty input reproduces it" is.

**Show the list to the user.** They often know the codebase's ghosts and can re-rank instantly — a five-second re-rank can save an hour of testing the wrong thing first.

---

## Step 3 — Test one at a time, one variable at a time

Work down the ranked list, testing **one hypothesis at a time** against the red/green signal from Step 1. **Change one variable at a time** — if you alter two things and the signal flips, you've learned nothing. Tag any debug logging you add with a **unique prefix** (e.g. `DBG_ch07_`) so every line is trivially greppable for cleanup later.

A hypothesis that predicted X and produced not-X is **eliminated** — move on, don't rationalize it back to life.

---

## Step 4 — Fix, and keep the repro as a regression test

Once a hypothesis is confirmed, make the fix and watch the Step 1 signal go **GREEN**. Then **promote the reproduction into a permanent regression test** — wire it into the test suite so this exact bug can never silently return. The repro you invested in becomes the asset that guards the fix.

---

## Step 5 — Clean up debug instrumentation

Remove every piece of temporary debugging you added — the prefixed logs, scratch print statements, throwaway scripts. Grep your unique prefix from Step 3 to find them all. The only thing that survives is the fix and the regression test; the diff should contain nothing you'd be embarrassed to merge.

---

## Step 6 — One-line lesson

Record, as a single line in the chapter's **Completion Report**, what actually caused the bug + what would have prevented it (e.g. "caused by empty-list rollup double-count; prevented by an empty-input test — added"). This is the cheap insurance that keeps the same class of bug from recurring.

If the lesson is a **broadly reusable gotcha** — something a future session on a different part of the project would also trip over — **offer to add it to `brain/DISCOVERIES.md`** (offer; the role that owns canon decides). Project-specific one-offs stay in the report; reusable traps graduate to DISCOVERIES.

---

## Rules

- Reproduction before theory, always. No hypothesis-testing until a red/green signal exists.
- Tighten the repro: fast and deterministic, smallest triggering input.
- 3–5 ranked falsifiable hypotheses, shown to the user, before testing any.
- One hypothesis and one variable at a time; eliminated means eliminated.
- The repro becomes a regression test; debug instrumentation gets cleaned up (grep your prefix).
- One-line lesson in the Completion Report; reusable gotchas offered to DISCOVERIES.md.
