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
- Does `agents/STRUCTURE.md`'s declared surfaces match the actual codebase? (Marketing surface declared but no `(marketing)` route group on disk → drift. New `(dashboard)` folder added but STRUCTURE.md doesn't mention it → drift.) Surfaces with file-system mismatch are category (A) violations.

**3. Design-system scan** (UI projects only — skip if no `components/` or equivalent).

First, determine where to scan:

1. Read `agents/STRUCTURE.md`. Extract every path from the `## Component locations` table (Generic, Marketing, App, Desktop tier paths).
2. If `agents/STRUCTURE.md` has `**Monorepo:** true` in `## Project layout`, also read `**App paths:**` and include each app's component paths.
3. If `agents/STRUCTURE.md` is missing, fall back to scanning from the project root.
4. Always exclude from all grep commands: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.turbo/`, `coverage/`. Pass these as exclusions to grep: `--exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist --exclude-dir=build --exclude-dir=.next --exclude-dir=.turbo --exclude-dir=coverage`.
5. For monorepos, scan each app's component paths separately and label findings with the app path (e.g. `apps/web/src/components/ui/button.tsx`).

Run the pre-ship checklist from `FUNDAMENTALS.md` against the scoped paths:

- **Raw values:** grep component files for hex literals (`#[0-9a-fA-F]{3,8}`), raw px outside utility classes, raw `font-family` strings. Any hit = token rule violation.
- **Cardinal sins:** grep for any indigo / violet Tailwind hex from FUNDAMENTALS.md's list. Grep for emoji characters inside `<button>`, `<h*>`, `<li>`. Grep for two-stop gradients on hero elements.
- **Accessibility floor:** grep for `outline: none` without `:focus-visible` nearby. Grep for `<img>` without `alt` or `width`/`height`. Grep for `<div onClick>`.
- **Banned words:** grep shipped copy (page files, marketing components) for the banned-words list from FUNDAMENTALS.md.

Findings here are category (A) — real violations.

**4. Garbage-collect `agents/preview/`.**

`design-direction` writes versioned HTML preview files to `agents/preview/<direction-slug>-<date>.html`. These accumulate over multiple runs and are never automatically cleaned.

1. List all files in `agents/preview/` (if the folder exists).
2. Group by direction-slug (the filename prefix before the date).
3. For each slug, keep the 2 most recent files (by filename date or mtime). Mark older ones for deletion.
4. If there are files to delete, surface them to the user before acting:
   ```
   agents/preview/ — found N preview files, M can be cleaned:
   Would delete:
     agents/preview/brand-forest-2026-03-12.html
     agents/preview/brand-forest-2026-02-28.html
   Would keep (2 most recent per slug):
     agents/preview/brand-forest-2026-05-01.html
     agents/preview/brand-forest-2026-04-15.html
   
   Delete the older files? [yes / no / show them first]
   ```
5. Only delete after explicit user confirmation. Do not auto-delete.

Findings here are category (B) — stale files. No fix required if the user chooses to keep them.

**5. Categorize findings:**
- **(A) Real contradiction / violation** — two files state mutually exclusive facts, OR a design-system rule is broken in code. Must fix.
- **(B) Stale wording** — wording that's no longer accurate but not strictly conflicting. Should fix.
- **(C) Intentional difference** — files differ on purpose (e.g., human-facing vs. agent-facing wording). No fix needed.

**6. Report.** Output each finding with category and source files. Example:

```
[A] STATUS.md Next Action #3 references "ChannelTypes audit" but ROADMAP §7 slot 5 is named "Channel Types CRUD". Names disagree.
[A] src/components/Pricing.tsx:42 uses raw hex #1a1a1a — token rule violation. Should be var(--surface).
[A] src/components/Hero.tsx:28 has emoji 🚀 inside <button> — cardinal sin #3.
[A] STRUCTURE.md declares Marketing surface at app/(marketing)/ but that route group does not exist on disk. Either drop the surface row or create the folder.
[B] CLAUDE.md "Tech stack" still says "Next.js" but BRIEF v1.4 locked "React + Vite". Wording is stale.
[C] human/agenda.md uses "you" wording; agents/STATUS.md uses neutral wording. Two-audience rule — no fix.
```

**7. Do not auto-fix.** Show findings. Let the user decide which to fix and in what order. The fix typically requires the `discipline` skill for canon edits or the `design-check` skill for UI fixes.

---

## Why it exists

Drift compounds silently. By the time the agent acts on a contradictory canon, the wrong decision is already cemented. Periodic auditing makes drift visible while it's still cheap to fix.
