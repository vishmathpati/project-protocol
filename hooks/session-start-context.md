# Project Protocol — Session Start

You are starting a coding session. This project follows the standard project protocol.

## Required reading before touching any code

1. **CLAUDE.md** — what this project is, tech stack, guardrails, coding rules
2. **STATUS.md** — current state, known bugs, next actions
3. **STRUCTURE.md** — structural map of the project: surfaces present, component locations per tier, conventions (if present — created by `build-component` on first invocation)
4. **BRAND.md** — product identity and what NOT to build (if it exists)
5. **BRIEF.md** — every major decision made in Cowork and why, including rejected options (if it exists)
6. **docs/INDEX.md** — project map + agent dependency index (if it exists)

Before any UI work: also read **FUNDAMENTALS.md** + **DESIGN.md** if they exist.

Do NOT ask the user what the current state is if STATUS.md exists. Read it.

## Pre-task classification (mandatory — do this before every change)

Before writing a single line of code, classify the work:

1. **NEW standalone feature** — completely new capability, no existing code touches it
   → Add to docs/INDEX.md Features section + create dependency map entry before session ends

2. **ADDITION to existing feature** — extending or modifying something that already exists
   → Read its dependency map entry in docs/INDEX.md first
   → Check every item listed under `shared with:` — those will be affected

3. **UI CHANGE** — modifying how something looks or behaves visually
   → Check docs/INDEX.md Critical Functions/Components for shared UI elements
   → A component used in 3 places breaks in 3 places

4. **BUG FIX** — correcting broken behaviour
   → Identify which feature owns the broken code
   → Read that feature's dependency map entry before touching anything

Do not skip this classification. It takes 30 seconds and prevents breaking things you didn't know were connected.

## WORKLOG.md discipline

After EVERY response where you changed a file, found a bug, made a decision, or tried
something that didn't work — append one line to WORKLOG.md immediately:

```
[HH:MM] fixed: what was fixed and where
[HH:MM] found_bug: description — file/location — P1/P2/P3
[HH:MM] decided: what was decided and why
[HH:MM] tried_failed: what was attempted and why it didn't work
```

Do not wait until session end. The worklog is your real-time memory.

## Session end

Run the `save-session` skill before closing. It updates CHANGELOG.md, STATUS.md,
signs BRIEF.md if decisions were made, and clears WORKLOG.md.
A session that ends without this is incomplete.

## Coding rules

1. **Think Before Coding** — State assumptions. Surface tradeoffs. Ask when unclear.
2. **Simplicity First** — Minimum code. No speculative features. No unnecessary abstractions.
3. **Surgical Changes** — Touch only what you must. Match existing style. Every line traces to the request.
4. **Verify Before Closing** — Define done before touching code. Screenshot UI changes. Reproduce bugs before fixing.
