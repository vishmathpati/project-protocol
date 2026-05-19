---
name: audit
description: Periodic consistency check across canon files (CLAUDE.md, STATUS.md, BRIEF.md, ROADMAP.md, etc.). Reports drift by severity. Does not auto-fix. Run when drift is suspected.
allowed-tools: Read, Glob, Grep
---

# Audit

Cross-file consistency check. Surfaces drift, does not fix.

---

## When this fires

- User explicitly invokes `/audit`.
- User asks "are the files consistent?", "is anything stale?", "check for drift".
- After multiple sessions of work on canon files without a sweep.
- Before any major release or chapter close that spans multiple files.

---

## The protocol

**1. Read the canon files.**
- `CLAUDE.md` (rules, agent split)
- `STATUS.md` (current state, next actions)
- `BRIEF.md` (decisions, all version blocks)
- `ROADMAP.md` (direction, phases, slots)
- `DESIGN.md` (brand tokens)
- `FUNDAMENTALS.md` (universal craft rules + pre-ship checklist)
- `docs/INDEX.md` (file dependency map)
- Any project-specific canon files referenced from `CLAUDE.md`.

**2. Cross-check.** For each pair of canon files, look for contradictions:
- Does `STATUS.md`'s "Next Actions" reference anything `ROADMAP.md` doesn't acknowledge?
- Does any `BRIEF.md` decision contradict the latest `STATUS.md` state?
- Does `CLAUDE.md` describe rules that the actual project structure violates?
- Does `docs/INDEX.md` list features that no longer exist? Miss features that do?

**3. Design-system scan** (UI projects only — skip if no `components/` or equivalent).

Run the pre-ship checklist from `FUNDAMENTALS.md` against the current codebase:

- **Raw values:** grep component files for hex literals (`#[0-9a-fA-F]{3,8}`), raw px outside utility classes, raw `font-family` strings. Any hit = token rule violation.
- **Cardinal sins:** grep for any indigo / violet Tailwind hex from FUNDAMENTALS.md's list. Grep for emoji characters inside `<button>`, `<h*>`, `<li>`. Grep for two-stop gradients on hero elements.
- **Accessibility floor:** grep for `outline: none` without `:focus-visible` nearby. Grep for `<img>` without `alt` or `width`/`height`. Grep for `<div onClick>`.
- **Banned words:** grep shipped copy (page files, marketing components) for the banned-words list from FUNDAMENTALS.md.

Findings here are category (A) — real violations.

**4. Categorize findings:**
- **(A) Real contradiction / violation** — two files state mutually exclusive facts, OR a design-system rule is broken in code. Must fix.
- **(B) Stale wording** — wording that's no longer accurate but not strictly conflicting. Should fix.
- **(C) Intentional difference** — files differ on purpose (e.g., human-facing vs. agent-facing wording). No fix needed.

**5. Report.** Output each finding with category and source files. Example:

```
[A] STATUS.md Next Action #3 references "ChannelTypes audit" but ROADMAP §7 slot 5 is named "Channel Types CRUD". Names disagree.
[A] src/components/Pricing.tsx:42 uses raw hex #1a1a1a — token rule violation. Should be var(--surface).
[A] src/components/Hero.tsx:28 has emoji 🚀 inside <button> — cardinal sin #3.
[B] CLAUDE.md "Tech stack" still says "Next.js" but BRIEF v1.4 locked "React + Vite". Wording is stale.
[C] human/agenda.md uses "you" wording; agents/STATUS.md uses neutral wording. Two-audience rule — no fix.
```

**6. Do not auto-fix.** Show findings. Let the user decide which to fix and in what order. The fix typically requires the `discipline` skill for canon edits or the `design-check` skill for UI fixes.

---

## Why it exists

Drift compounds silently. By the time the agent acts on a contradictory canon, the wrong decision is already cemented. Periodic auditing makes drift visible while it's still cheap to fix.
