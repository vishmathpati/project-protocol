---
name: solo
description: Wear both CEO and worker hats for small work done in one pass, with no worktree and no handoff. Reach for it on quick changes that don't warrant the full delegation loop. Triggers — "/solo", "small fix", "just do this", "quick change".
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, mkdir:*, git:*)
---

# Solo — Project Protocol

Both hats, small work. For jobs too small to be worth the `/ceo` + `/worker` ceremony — a quick fix, a tiny addition, a one-file change. You plan lightly, do the work yourself, write a short report, and commit. No worktree, no branch handoff, no delegation. Work directly on the current branch.

There is ONE canon: `brain/`.

---

## Step 0 — Author stamp

- `CLAUDE_PLUGIN_ROOT` set → stamp `· Claude Code`
- `CODEX_PLUGIN_ROOT` set → stamp `· Codex`
- neither set → stamp `· Cowork`

---

## Step 1 — Size the job first

Before doing anything, sanity-check that this is actually solo-sized. Solo is for work that:

- touches one or a few files,
- has no real ambiguity about what "done" means,
- doesn't need a second pair of eyes (no auth, money/payments, data deletion, or security surface — those deserve a real chapter and a CEO check).

If the job is bigger than that — multiple moving parts, decisions to lock, or it'll outlive one sitting — **STOP and say so**: "This is big enough to be a real chapter. Run `/ceo` to define it and `/worker` to execute it." Then let the user choose. Don't quietly grind a large job through solo mode.

---

## Step 2 — Plan lightly

A few lines is enough — what you're going to change and how. No formal Plan document. Just enough that you don't wander.

---

## Step 3 — Do the work

Make the change directly. Read the slice of canon you need; edit the code files. You wear both hats here, so you MAY touch the shared canon if the small job legitimately calls for it (e.g. a STATUS line) — but keep it minimal and stay honest about it in the report.

When building a feature or fixing a bug, invoke `test-driven-development` for the implementation (RED-GREEN-REFACTOR); for a bug, `bug-fixing` provides the structured repro that becomes the RED test.

When the work creates or modifies any page or UI component — files under a `components/`, `app/`, `pages/`, or `marketing/` path, or the job is visual — do NOT hand-roll the UI. Route it explicitly: call `Skill("build-page")` for a whole page and/or `Skill("build-component")` for a component. The `design-check` gate fires per the existing PostToolUse hook. UI touched by hand, bypassing the design skills, is out of bounds even in solo mode.

---

## Step 4 — Write a short Completion Report

Pick the lighter of two homes by size:

**Trivial work** (typo, one-liner, cosmetic) → one author-stamped line in `brain/WORKLOG.md`:

```
[YYYY-MM-DD] [author stamp] · fixed: <what> — <where>
```

**Small-but-real work** → a chapter file `brain/chapters/NN-name.md`. If the chapter doesn't exist yet, start it with the title + a `> Solo:` stamp; if it already exists (a chapter may already hold earlier reports and Verdicts), **append** your report as a new dated section at the bottom — never overwrite an existing one. Use this EXACT Completion Report template (same as `/worker`, so the record speaks the CEO's language):

```
## Completion Report — YYYY-MM-DD · <author stamp>
**Goal:** <echo what was asked>
**Status:** done | partial | blocked
**Changed:** <one line per file/area>
**Verified:** <what ran + result>
**Flags:** <deviations / risks / unsure — these are the CEO's drill-down targets>
**Commit:** <branch · hash>
```

Same sections as the `/worker` Completion Report — so if a solo job later grows into a delegated one, the record already speaks the CEO's language.

---

## Step 5 — Commit

Commit code + the report together, author-stamped, on the current branch:

```bash
git add <changed files> brain/chapters/NN-name.md   # or brain/WORKLOG.md for trivial work
git commit -m "<type>: <short summary> <author stamp>"
```

**Pushing:** host tools (Claude Code / Codex) can push — `git push origin <branch>`. Cowork CANNOT push (no credentials); commit locally and emit the command for the user:

````
✅ Done + committed locally. Cowork can't push — run this to sync:

```bash
git push origin <branch>
```
````

Then capture the hash into the report's **Commit** line if you committed first.

---

## Rules

- Solo is for small work only. The moment it grows — multiple parts, decisions to lock, or a sensitive area (auth, money, deletion, security) — escalate to `/ceo` + `/worker`.
- Report shape matches `/worker`'s Completion Report, so records stay consistent across all three skills.
- Trivial work goes to WORKLOG; small-but-real work goes to a chapter file — **append** a new dated report if the chapter already exists, never overwrite a prior one.
- Never push from Cowork; commit locally and emit the push command.
