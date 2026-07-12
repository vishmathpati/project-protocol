---
name: solo
description: Wear both CEO and worker hats for small work done in one pass, in either an app-created worktree or the local checkout. Reach for quick changes that do not warrant the delegation loop. Triggers — "/solo", "small fix", "just do this", "quick change".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, mkdir:*, git:*)
---

# Solo — Project Protocol

Both hats, small work. For jobs too small to be worth the `/ceo` + `/worker` ceremony — a quick fix, a tiny addition, a one-file change. You plan lightly, do the work yourself, write a short report, and commit. The app may have placed this session in a worktree or the local checkout; either is valid. Checkout topology does not select the role.

There is ONE canon: `brain/`.

---

## Step 0 — Author stamp + checkout

- `CLAUDE_PLUGIN_ROOT` set → stamp `· Claude Code`
- `CODEX_PLUGIN_ROOT` set → stamp `· Codex`
- neither set → stamp `· Agent` (treat as a full-capability host)

Run `recap` before sizing the work so the session starts from live Git, canon, and any active chapter.

Use the checkout the user selected when creating the session. If it is a worktree, stay in it and identify its branch/base commit; if HEAD is detached, create a named solo branch before editing. If it is the local checkout, show the protocol's one-time worktree recommendation before the first edit and honor the user's choice to continue locally. Never reject solo mode merely because the app created a worktree.

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

For UI work, run Design Check preflight and use the established component system. Brand-facing substantial pages use Build Page. Conventional dashboard/product UI may proceed directly with existing patterns and shadcn. Build Component is for a genuine gap; UI Research and Inspect Component are explicit optional tools.

---

## Step 4 — Write a short Completion Report

Pick the lighter of two homes by size:

**Trivial work** (typo, one-liner, cosmetic) → one author-stamped line in `brain/WORKLOG.md`:

```
[YYYY-MM-DD] [author stamp] · fixed: <what> — <where>
```

**Small-but-real work** → use an existing chapter when one governs the work. Create a chapter only when a durable reviewable contract is useful; do not manufacture one for ceremony. Append the same Completion Report used by `/worker`.

```
## Completion Report — YYYY-MM-DD · <author stamp>
**Goal:** <echo what was asked>
**Status:** done | partial | blocked
**Changed:** <one line per file/area>
**Verified:** <what ran + result>
**Diff:** <git diff --stat against the starting point>
**Flags:** <deviations / risks / unsure — these are the CEO's drill-down targets>
**Commit:** <branch · hash>
```

Run `completion-check` before claiming substantial work done. Solo may close genuinely small work after the check passes.

---

## Step 5 — Commit

Commit code + the report together, author-stamped, on the current branch:

```bash
git add <changed files> brain/chapters/NN-name.md   # or brain/WORKLOG.md for trivial work
git commit -m "<type>: <short summary> <author stamp>"
```

**Pushing:** push your branch — `git push origin <branch>`.

Then capture the hash into the report's **Commit** line if you committed first.

---

## Rules

- Solo is for small work only. The moment it grows — multiple parts, decisions to lock, or a sensitive area (auth, money, deletion, security) — escalate to `/ceo` + `/worker`.
- Report shape matches `/worker`'s Completion Report, so records stay consistent across all three skills.
- Trivial work goes to WORKLOG; small-but-real work goes to a chapter file — **append** a new dated report if the chapter already exists, never overwrite a prior one.
