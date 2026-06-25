# Test quality — good vs. brittle, and minimal mocking

Reference for `test-driven-development`. The SKILL.md gives the loop; this file is the deeper guidance on *what a good test looks like* and *how little to mock*.

---

## The one question that sorts good from bad

> **If I rewrote the internals without changing what the code does, would this test still pass?**

- **Yes** → the test is anchored to behavior. Keep it.
- **No** → the test is coupled to implementation. It will break on refactors that change nothing a caller cares about, which trains everyone to avoid cleanup. Rewrite it against the public interface, or delete it.

A good test reads like a **specification**: a stranger could learn what the unit is supposed to do from the test names and assertions alone, without opening the implementation.

---

## Good test

- **Arranges** a realistic input, **acts** through the public entry point, **asserts** on the observable result or effect.
- Names state the behavior: `returns_zero_for_empty_cart`, `rejects_expired_token` — readable as a spec line.
- One behavior per test. When it fails, the name already tells you what broke.
- Independent and order-free: no shared mutable state, no "test B only passes if test A ran first."
- Deterministic: time, randomness, ordering, and network are pinned, so it fails (or passes) the same way every run.
- Asserts on **outcomes** — the returned value, the persisted record, the emitted event — not on *how* the outcome was produced.

## Brittle test (anti-patterns to avoid)

- **Tests a private method directly.** Private means "free to change." If it needs testing, exercise it through the public path that uses it.
- **Asserts on internal state** — a private field, an internal cache, a specific data shape that isn't part of the contract.
- **Asserts call order or call counts** on internal collaborators ("then it calls `validate` then `save`"). That pins the implementation, not the behavior.
- **Mirrors the implementation** — the test re-computes the expected value with the same algorithm the code uses, so a shared bug passes both. Hard-code expected values or derive them independently.
- **Over-mocks** until the test only proves "the code calls the mocks I told it to call" — a tautology that survives no real change. (See below.)
- **Snapshot-everything** with no thought — large auto-snapshots break on every cosmetic change and nobody reads the diff, so they get blindly re-blessed.

---

## Minimal mocking

Mocks are a cost, not a default. Every mock is a place where the test's idea of a collaborator can drift from the real thing, so the bar is **mock as little as possible**.

**Mock only at true boundaries you don't own or can't run fast/deterministically:**

- Network / third-party APIs.
- Clock, randomness, UUID generation (or inject them so you can pass a fixed value — often cleaner than a mock).
- The filesystem or a real database **when** it would make the test slow or flaky. Prefer a real in-memory or temp instance when it's fast and faithful.
- Anything with side effects you must not trigger in a test (sending email, charging a card).

**Do NOT mock:**

- The unit under test, or its own internal helpers — mocking what you're testing tests nothing.
- Plain value objects, pure functions, simple data structures — just use the real thing.
- Collaborators that are fast, deterministic, and side-effect-free — real is more honest than a stub.

**Prefer, in order:** the real object → a lightweight fake (a small working stand-in, e.g. an in-memory repository) → a stub that returns canned data → a mock that asserts interactions. Reach down the list only when the one above is genuinely impractical. Interaction-asserting mocks ("was this called with X") are the last resort because they couple the test to *how* the code works, which is exactly what we're trying to avoid.

**Heuristic:** if a test needs a tall stack of mocks to stand up, that's usually a design signal — the unit is reaching across too many boundaries. Consider whether the seam should move, rather than piling on more mocks.

---

## Quick checklist

- [ ] Would survive an internal refactor (the sorting question above).
- [ ] Asserts on observable outcomes via the public interface.
- [ ] Reads like a spec — name says the behavior.
- [ ] Independent, order-free, deterministic.
- [ ] Mocks only true external/non-deterministic boundaries; real objects everywhere else.
- [ ] Expected values aren't computed by the same logic under test.
