---
name: project-audit
description: Read-only consistency audit across project canon, chapters, declared structure, and actual repository state. Use for periodic drift checks, stale references, contradictions, and protocol health.
allowed-tools: Read, Glob, Grep
---

# Project Audit

Cross-file consistency check. Surfaces drift, does not fix.

---

## When this fires

- User explicitly invokes `/project-audit`.
- User asks "are the files consistent?", "is anything stale?", "check for drift".
- After multiple sessions of work on canon files without a sweep.
- Before any major release or chapter close that spans multiple files.

---

## The protocol

**1. Read the canon files.**
- `CLAUDE.md` (rules, agent split)
- `brain/STATUS.md` (current state, next actions)
- `brain/BRIEF.md` (decisions, all version blocks)
- `brain/ROADMAP.md` (direction, phases, slots)
- `brain/DESIGN.md` (brand tokens)
- `brain/FUNDAMENTALS.md` (universal craft rules + pre-ship checklist)
- `brain/WONT-DO.md` (deferred / declined items with reasons)
- `brain/agenda.md` (active chapter agenda / open questions)
- `brain/chapters/*` (all chapter files — read each one)
- `docs/INDEX.md` (file dependency map)
- Any project-specific canon files referenced from `CLAUDE.md`.

**2. Cross-check.** For each pair of canon files, look for contradictions:
- Does `brain/STATUS.md`'s "Next Actions" reference anything `brain/ROADMAP.md` doesn't acknowledge?
- Does `brain/STATUS.md` point at a chapter (by name or slug) that actually exists in `brain/chapters/`? A pointer to a missing chapter is a category (A) violation.
- Does any `brain/BRIEF.md` decision contradict the latest `brain/STATUS.md` state?
- Does `CLAUDE.md` describe rules that the actual project structure violates?
- Does `docs/INDEX.md` list features that no longer exist? Miss features that do?
- Do chapter files in `brain/chapters/` reference canon concepts (stack, surfaces, brand tokens) that contradict `brain/BRIEF.md` or `brain/STRUCTURE.md`? Any mismatch is a category (A) violation.
- Does `brain/WONT-DO.md` contain entries that lack a stated reason? Missing reasons are category (B) — should fix.
- Does `brain/STRUCTURE.md`'s declared surfaces match the actual codebase? (Marketing surface declared but no `(marketing)` route group on disk → drift. New `(dashboard)` folder added but STRUCTURE.md doesn't mention it → drift.) Surfaces with file-system mismatch are category (A) violations.

**3. Design-system scan** (UI projects only — skip if no `components/` or equivalent).

First, determine where to scan:

1. Read `brain/STRUCTURE.md`. Extract every path from the `## Component locations` table (Generic, Marketing, App, Desktop tier paths).
2. If `brain/STRUCTURE.md` has `**Monorepo:** true` in `## Project layout`, also read `**App paths:**` and include each app's component paths.
3. If `brain/STRUCTURE.md` is missing, fall back to scanning from the project root.
4. Always exclude from all grep commands: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.turbo/`, `coverage/`. Pass these as exclusions to grep: `--exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist --exclude-dir=build --exclude-dir=.next --exclude-dir=.turbo --exclude-dir=coverage`.
5. For monorepos, scan each app's component paths separately and label findings with the app path (e.g. `apps/web/src/components/ui/button.tsx`).

Run the pre-ship checklist from `brain/FUNDAMENTALS.md` against the scoped paths:

- **Raw values:** grep component files for hex literals (`#[0-9a-fA-F]{3,8}`), raw px outside utility classes, raw `font-family` strings. Any hit = token rule violation.
- **Cardinal sins:** grep for any indigo / violet Tailwind hex from FUNDAMENTALS.md's list. Grep for emoji characters inside `<button>`, `<h*>`, `<li>`. Grep for two-stop gradients on hero elements.
- **Accessibility floor:** grep for `outline: none` without `:focus-visible` nearby. Grep for `<img>` without `alt` or `width`/`height`. Grep for `<div onClick>`.
- **Banned words:** grep shipped copy (page files, marketing components) for the banned-words list from `brain/FUNDAMENTALS.md`.

Findings here are category (A) — real violations.

**4. Garbage-collect `brain/preview/`.**

Style Lock may write versioned HTML previews to `brain/preview/<direction-slug>-<date>.html`. Treat them as generated artifacts; report stale previews but do not delete without confirmation.

1. List all files in `brain/preview/` (if the folder exists).
2. Group by direction-slug (the filename prefix before the date).
3. For each slug, keep the 2 most recent files (by filename date or mtime). Mark older ones for deletion.
4. If there are files to delete, surface them to the user before acting:
   ```
   brain/preview/ — found N preview files, M can be cleaned:
   Would delete:
     brain/preview/brand-forest-2026-03-12.html
     brain/preview/brand-forest-2026-02-28.html
   Would keep (2 most recent per slug):
     brain/preview/brand-forest-2026-05-01.html
     brain/preview/brand-forest-2026-04-15.html
   
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
[A] brain/STATUS.md Next Action #3 references "ChannelTypes audit" but brain/ROADMAP.md §7 slot 5 is named "Channel Types CRUD". Names disagree.
[A] src/components/Pricing.tsx:42 uses raw hex #1a1a1a — token rule violation. Should be var(--surface).
[A] src/components/Hero.tsx:28 has emoji 🚀 inside <button> — cardinal sin #3.
[A] brain/STRUCTURE.md declares Marketing surface at app/(marketing)/ but that route group does not exist on disk. Either drop the surface row or create the folder.
[A] brain/STATUS.md points at chapter "onboarding-v2" but brain/chapters/onboarding-v2.md does not exist.
[A] brain/chapters/billing.md references stack "Next.js + Prisma" but brain/BRIEF.md v1.4 locked "React + Vite + Supabase". Stack mismatch.
[B] brain/WONT-DO.md entry "Dark mode" has no reason stated.
[B] CLAUDE.md "Tech stack" still says "Next.js" but brain/BRIEF.md v1.4 locked "React + Vite". Wording is stale.
[C] brain/agenda.md uses "you" wording; brain/STATUS.md uses neutral wording. Two-audience rule — no fix.
```

**7. Do not auto-fix.** Show findings. Let the owning role decide which to fix. Consequential canon repairs may require `change-check`; UI repairs may require `design-check`.

---

## Why it exists

Drift compounds silently. By the time the agent acts on a contradictory canon, the wrong decision is already cemented. Periodic auditing makes drift visible while it's still cheap to fix.
