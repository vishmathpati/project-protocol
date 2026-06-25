---
name: test-driven-development
description: Use when implementing a feature or fixing a bug, before writing implementation code — and when the user mentions test-first, TDD, red-green-refactor, or "write the test first." The /worker and /solo roles call this on implementation chapters. Triggers — "TDD", "test-driven", "test first", "red green refactor", "write a failing test", "add a test for this feature", "build this test-first".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*)
---

# Test-driven development — Project Protocol

RED-GREEN-REFACTOR discipline for building *new feature* work test-first. Used by `/worker` or `/solo` on an implementation chapter. The whole point is a tight loop: one test, one slice of code, repeat — each cycle informed by what the last one taught you.

There is ONE canon: `brain/`. The work and any one-line lesson go into the chapter's Completion Report (`/worker` / `/solo` write that).

---

## Philosophy — test behavior, not implementation

A test exists to verify **behavior through the public interface** — what a caller can observe, not how the code does it internally. Good tests read like a spec: someone could understand what the unit is supposed to *do* from the tests alone, without reading the implementation. And because they only touch the public surface, they **survive refactors** — you can rip out and rewrite the internals and the tests still pass, because behavior didn't change.

Tests coupled to internals — private methods, internal data shapes, call ordering, mock-everything assertions — are the anti-pattern. They break the moment you refactor even when behavior is identical, so they punish exactly the cleanup you want to encourage. If a test would fail after a pure internal refactor, it's testing the wrong thing.

---

## The loop — one test at a time

Run this cycle for **one behavior at a time**. Do not batch.

1. **RED** — write **ONE** failing test that describes the next slice of behavior. Run it. Watch it **fail for the right reason** (the behavior is missing — not a typo, import error, or wrong test). A test that fails for the wrong reason has told you nothing.
2. **GREEN** — write the **minimal** code to make that one test pass. Not the elegant version, not the general version — the smallest thing that goes green. Run it. Watch it **pass**.
3. **REFACTOR** — now clean up: dedupe, rename, extract — while staying green. Re-run after each change. **Never refactor while red.** Refactoring is changing structure without changing behavior, which is only provable when the bar is green.

Then **commit that slice** — author-stamped, **one commit per green slice** (this matches the change-tracking habit in `git`: commit at meaningful checkpoints, a passing test being exactly that). Then back to RED for the next behavior.

---

## Anti-pattern — horizontal slicing

Do **NOT** write all the tests first and then all the code. Writing every test up front means writing tests for **imagined** behavior — you're guessing at interfaces and edge cases before a single line has taught you anything, and you'll discover halfway through that the shape was wrong, leaving a pile of tests to rewrite.

Work in **vertical slices (tracer bullets)** instead: one test → one implementation → repeat. Each full cycle is informed by the last — the code you just wrote reveals the next test worth writing, the next edge case, the next interface tweak. The loop is a feedback loop; horizontal slicing throws the feedback away.

---

## Per-cycle checklist

Before you move to the next slice, the test you just wrote should pass all of these:

- [ ] Describes a **behavior**, not an implementation detail.
- [ ] Uses the **public interface only** — no private methods, internal state, or call-order assertions.
- [ ] Would **survive an internal refactor** — if you rewrote the internals without changing behavior, it stays green.
- [ ] The code you wrote is **minimal** for this test — nothing added "while you're in there."
- [ ] **No speculative / un-needed features** — you built exactly what this test demanded, no more.

---

## You can't test everything

You will not test every line, and you shouldn't try — exhaustive coverage of trivial code is wasted effort. **Concentrate where mistakes are expensive:** critical paths, complex branching logic, the rules that actually carry the feature's value. Trivial getters and glue need little.

Before starting the loop, **confirm with the user which behaviors matter most** — which paths are critical, which logic is genuinely tricky. That conversation directs your test effort where it pays off and is the cheapest way to avoid both over- and under-testing.

---

## Respect the project's tooling

Read **`brain/TOOLING.md`** (if present) for the project's test command and runner conventions — don't assume `npm test` or guess the framework. During the loop, run the **single test file** you're working on so the cycle stays fast and the signal is focused. Run the **full suite once at the end** to confirm the new slices didn't break anything elsewhere.

---

## Relationship to bug-fixing

`test-driven-development` is for **new feature** work. For a **bug** chapter, do not duplicate it: the **failing reproduction** built by the `bug-fixing` skill **IS the RED test** — its repro-first step produces the red/green signal, and the fix turns it green, then it's promoted to a regression test. So:

- **Feature chapter** → this skill drives the build (RED-GREEN-REFACTOR, one slice at a time).
- **Bug chapter** → hand off to `bug-fixing`; its reproduction is the RED, its fix is the GREEN, no separate TDD pass needed.

They don't overlap — pick by chapter type.

---

## Rules

- Test **behavior through the public interface**, never implementation details — good tests survive refactors.
- One test at a time: RED (fail for the right reason) → GREEN (minimal code) → REFACTOR (stay green) → commit the slice.
- **Never refactor while red.** Cleanup only happens on a green bar.
- **Vertical slices, not horizontal** — never all-tests-then-all-code; each cycle informs the next.
- Code is **minimal** for the current test; no speculative features.
- You can't test everything — confirm critical paths with the user; focus effort there.
- Read `brain/TOOLING.md` for the test command; single file during the loop, full suite at the end.
- Bug chapters belong to `bug-fixing` (its repro is the RED test); this skill is for new features.

See `references/test-quality.md` for what separates a good test from a brittle one, and for minimal-mocking guidance.
