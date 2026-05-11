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
- `docs/INDEX.md` (file dependency map)
- Any project-specific canon files referenced from `CLAUDE.md`.

**2. Cross-check.** For each pair of canon files, look for contradictions:
- Does `STATUS.md`'s "Next Actions" reference anything `ROADMAP.md` doesn't acknowledge?
- Does any `BRIEF.md` decision contradict the latest `STATUS.md` state?
- Does `CLAUDE.md` describe rules that the actual project structure violates?
- Does `docs/INDEX.md` list features that no longer exist? Miss features that do?

**3. Categorize findings:**
- **(A) Real contradiction** — two files state mutually exclusive facts. Must fix.
- **(B) Stale wording** — wording that's no longer accurate but not strictly conflicting. Should fix.
- **(C) Intentional difference** — files differ on purpose (e.g., human-facing vs. agent-facing wording). No fix needed.

**4. Report.** Output each finding with category and source files. Example:

```
[A] STATUS.md Next Action #3 references "ChannelTypes audit" but ROADMAP §7 slot 5 is named "Channel Types CRUD". Names disagree.
[B] CLAUDE.md "Tech stack" still says "Next.js" but BRIEF v1.4 locked "React + Vite". Wording is stale.
[C] human/agenda.md uses "you" wording; agents/STATUS.md uses neutral wording. Two-audience rule — no fix.
```

**5. Do not auto-fix.** Show findings. Let the user decide which to fix and in what order. The fix typically requires the `discipline` skill for the actual edits.

---

## Why it exists

Drift compounds silently. By the time the agent acts on a contradictory canon, the wrong decision is already cemented. Periodic auditing makes drift visible while it's still cheap to fix.
