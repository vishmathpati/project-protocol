# Phase 3 — Create three-folder structure

Create the root files + cowork/, agents/, human/ subfolders + protocol files. Apply Phase 2 merge decisions during template population.

## 3a. Create folders

```bash
mkdir -p cowork agents human agents/docs/detail
```

## 3b. Root files

### Root `CLAUDE.md` template

```markdown
# CLAUDE.md — [Project Name]

> Always loaded by every agent. Rules + folder map.

## Coding Standards

**1. Think Before Coding** — State assumptions. Surface tradeoffs. Ask when unclear.
**2. Simplicity First** — Minimum code. No speculative features. No unnecessary abstractions.
**3. Surgical Changes** — Touch only what you must. Match existing style.
**4. Verify Before Closing** — Define done before touching code. Screenshot UI changes. Reproduce bugs before fixing.

## Who reads what

- **Human** reads `human/agenda.md` to know what to do next.
- **Cowork** reads `cowork/CLAUDE.md` for orchestration discipline, plus the rest of `cowork/` and `agents/` as needed.
- **Codex / Claude Code** read `agents/CLAUDE.md` (if present) and the agent canon files in `agents/`.

## Non-negotiable rules

1. Decide before you act. Write it down before you decide.
2. When you change one file, list every other file that becomes stale (see `README.md` cascade rules).
3. Lock-before-cascade: changes hit `BRIEF.md` first, then propagate.
4. Audit before close: independent verification before any chapter is marked done.
5. Commit + push before leaving any chat. Pull main before starting one.
6. One tool active at a time.

## Folder map

- `cowork/` — orchestration tier. Cowork edits here. Agents do not read it.
- `agents/` — project canon. All agents read here.
- `human/` — your tier. Cowork derives this from `agents/`.

## Pre-task classification (mandatory before any code change)

1. NEW standalone feature
2. ADDITION to existing feature
3. UI CHANGE
4. BUG FIX

Check `agents/docs/INDEX.md` dependency entries before classifying.
```

### Root `README.md` template

```markdown
# README.md — File Map & Dependencies

> Open this whenever you're about to change a non-trivial file. Find that file below. Its "When this changes" line tells you which other files need updating.

## File catalog

### Root
- **CLAUDE.md** — rules + folder map. Always loaded by every agent.
- **README.md** — this file. Open before any non-trivial edit.

### `cowork/`
- **CLAUDE.md** — Cowork-specific rules and discipline.
- **STATUS.md** — current orchestration state. No cascade.
- **BRIEF.md** — orchestration decisions (HOW we work). When this changes: `cowork/CLAUDE.md` may need updating.
- **WORKLOG.md** — real-time. Cleared by save-session.
- **CHANGELOG.md** — orchestration history. Never cleared.

### `agents/`
- **STATUS.md** — project state. No cascade.
- **BRIEF.md** — project decisions (WHAT we build). When this changes: `agents/ROADMAP.md` may need updating, `agents/STATUS.md` Next Actions may need updating, `human/agenda.md` may need re-derivation.
- **ROADMAP.md** — phases and ordering. When this changes: `agents/STATUS.md` Next Actions update, `human/agenda.md` re-derive.
- **BRAND.md** — product identity. When this changes: `agents/DESIGN.md` may need updating.
- **FUNDAMENTALS.md** — global design framework. Never edited per project.
- **DESIGN.md** — project tokens. When this changes: pending UI work pauses until tokens validate.
- **DISCOVERIES.md** — append-only UI patterns. No cascade.
- **WORKLOG.md** / **CHANGELOG.md** — same role as cowork's but for project work.
- **docs/INDEX.md** — feature dependency map. Source for cross-feature lookups.
- **docs/detail/** — deep reference. When changed: relevant feature contracts may need re-reading.

### `human/`
- **agenda.md** — daily steering file. When `agents/ROADMAP.md` or `agents/BRIEF.md` change: re-derive.

## Cascade summary (rule of thumb)

```
agents/BRIEF.md → agents/ROADMAP.md → agents/STATUS.md → human/agenda.md
```

If you change anything upstream, check everything downstream.
```

## 3c. cowork/ files

### `cowork/CLAUDE.md`

```markdown
# cowork/CLAUDE.md — Cowork Discipline

> Loaded when Cowork is working inside `cowork/` or orchestrating cross-tool.

## Cowork's role

- Orchestrator. Plans, locks, cascades, derives, delegates, audits.
- Never executes specialist work directly (UI goes to Claude Code, backend to Codex).
- Holds context across sessions via persistent memory.

## Rules

1. **Discussion-default.** When user says "discuss" / "let's talk," do not edit (`discussion-mode` skill applies).
2. **Lock-before-act.** Conversational decisions captured in `cowork/BRIEF.md` (orchestration) or `agents/BRIEF.md` (project) before acting (`discipline` skill applies).
3. **Cascade declaration.** Before any edit, list which other files become stale.
4. **Read-back rule.** Before recording a decision, read it back to the user in chat.
5. **Sub-agent for deep reads.** Tier-3 files get read by a sub-agent, synthesis returned (`verify-by-reading` skill applies).

## Tier loading

- **Tier 1 (always):** root CLAUDE.md, root README.md, this file, cowork/STATUS.md.
- **Tier 2 (on demand):** cowork/BRIEF.md, agents/STATUS.md, agents/BRIEF.md, agents/ROADMAP.md.
- **Tier 3 (sub-agent):** agents/docs/detail/, individual memory files.
```

### `cowork/STATUS.md` (60-line max)

```markdown
# cowork/STATUS.md
> Last updated: YYYY-MM-DD · Cowork

## Current focus
[One-line: what we're orchestrating right now]

## Health
- ✅ Working: [solid items]
- 🔴 Broken: [nothing or what's broken]
- 🔒 Blocked: [nothing or what's blocked]

## Pending human input
- [Items needing decision]

## Pending Cowork drafting
- [Things I owe]

## Recent sessions (rolling 5)
- YYYY-MM-DD · [one-line summary]

## Next actions
1. [Concrete next move]
```

### `cowork/BRIEF.md`

```markdown
# cowork/BRIEF.md — Orchestration Decisions
> How the user and Cowork work together. Append-only. 500-line limit; overflow to BRIEF-2.md.

---

## v1.0 — YYYY-MM-DD · Cowork

### What this is
[One-paragraph context]

### Locked decisions
1. [Decision]

### Rejected this session
- [Option rejected and why]
```

### `cowork/WORKLOG.md`

```markdown
# Worklog — Cowork orchestration
> Real-time log. Cleared by save-session.

(empty — last session closed cleanly)
```

### `cowork/CHANGELOG.md`

```markdown
# Changelog — Cowork
> Orchestration history. Never cleared. Keep a Changelog format.

## [Unreleased]
```

## 3d. agents/ files

### `agents/STATUS.md` (60-line max, fixed schema)

```markdown
# agents/STATUS.md
> Last updated: YYYY-MM-DD · [agent label]

## Current sprint
[One-paragraph context]

## Health
- ✅ Working: [confirmed working features]
- 🔴 Broken: [known bugs P1/P2/P3]
- 🔒 Blocked: [items waiting on something external]

## Needs CEO input
- [questions or decisions that require a Cowork session]

## Recent sessions (rolling 5)
- YYYY-MM-DD · [agent label]: [one-line summary]

## Next actions
1. [specific next step]
```

### `agents/BRIEF.md` (500-line max)

```markdown
# agents/BRIEF.md — Project Decisions
> What we're building and why. Append-only. New version block per change.

---

## v1.0 — YYYY-MM-DD · Cowork

### What we're building
[One paragraph]

### Tech stack — chosen
| Technology | Why |
|------------|-----|

### Tech stack — rejected
| Technology | Why rejected |
|------------|--------------|

### Architecture decisions
1. [Decision]

### Scope — in / out
**In:** ...
**Out:** ...

### Open questions
1. [Question]
```

### `agents/ROADMAP.md`

```markdown
# agents/ROADMAP.md — Direction & Phases
> Owner: Vish + Cowork (joint). Agents execute against this; do not edit unless authorized.

## Direction
[One paragraph — what we're going toward]

## Out of scope
[Explicit refusals]

## Phases / Acts
### Act 1 — [Name]
[Goal · output · done criteria · status]
```

### `agents/WORKLOG.md`, `agents/CHANGELOG.md`

Same as cowork's templates but with "project" framing.

### `agents/BRAND.md`, `agents/FUNDAMENTALS.md`, `agents/DESIGN.md`, `agents/DISCOVERIES.md`

See `phase-4-design-system.md` — created in Phase 4.

## 3e. human/ files

### `human/agenda.md`

```markdown
# Agenda

> Open this. Find the next un-ticked chapter. Open the tool. Do the work. Tick. Move on.

## How to use
(empty — populated as the project unfolds)

## ✓ Done
(none yet)
```

## 3f. Apply Phase 2 merge decisions

For every file in the Phase 2 decision table:
- **Merge** → write the extracted content into the destination protocol file
- **Reference** → add one line to root CLAUDE.md `## Reference files`
- **Leave** / **Skip** → no action

## 3g. Verify

```bash
ls -la
ls cowork/
ls agents/
ls human/
```

Confirm all four tiers exist with expected files.
