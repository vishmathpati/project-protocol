---
name: worker
description: Execute one delegated chapter in a worktree — sync canon, do exactly the chapter's job, write the Completion Report into the chapter file, commit. Triggers — "/worker", "work this chapter", "pick up chapter N".
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*)
---

# Worker — Project Protocol

The executor. You take ONE chapter the CEO defined and do exactly that job — no more. You run in a **git worktree** on your own branch (Codex and Claude Code each create real worktrees that share the repo's `.git`). When you finish, you write a Completion Report into the chapter file. That report is the contract the CEO reads — get it right.

There is ONE canon: `brain/`. You may READ it. You may WRITE only code files and your own chapter file. You NEVER edit the shared canon — that's the CEO's.

---

## Step 0 — Author stamp + confirm you're in a worktree

Detect the author stamp (labels your entries only):

- `CLAUDE_PLUGIN_ROOT` set → stamp `· Claude Code`
- `CODEX_PLUGIN_ROOT` set → stamp `· Codex`
- neither set → stamp `· Cowork`

Confirm your location: `git rev-parse --abbrev-ref HEAD` and `git rev-parse --show-toplevel`. You should be on a worktree branch, NOT on `main`. If you're on `main`, STOP and tell the user — a worker works on a branch, not the canon.

---

## Step 1 — Sync the latest canon into this worktree

Pull the newest `brain/` (canon + the chapter brief the CEO just wrote) into your worktree. Worktrees sync locally through the shared `.git` — no GitHub needed:

```bash
git merge main
```

If this conflicts, STOP and report it under Flags — do not guess your way through a canon conflict.

---

## Step 2 — Read just enough, for THIS chapter only

Read `brain/chapters/NN-name.md` — its **Goal**, **Plan**, and **Constraints / out of scope**. Read only the slice of canon (`brain/STATUS.md`, `brain/BRIEF.md`, relevant docs) you actually need to do this one job. Do not read the whole project. Do ONLY what this chapter asks.

---

## Step 3 — Write boundary (strict)

You may edit ONLY:

- **code files** the chapter requires, and
- **this chapter's own file** `brain/chapters/NN-name.md` (this is how you report).

You may NEVER edit the shared canon — `brain/STATUS.md`, `brain/BRIEF.md`, `brain/ROADMAP.md`, `brain/WONT-DO.md` (also `brain/CHANGELOG.md`, `brain/agenda.md`). Those are the CEO's. Editing your own chapter file never collides with other workers, because each chapter is exactly one file owned by one worker.

If the work seems to need a canon change, that's a Flag (Step 5), not an edit.

---

## Step 4 — Write the Completion Report

When the work is done, write the report into `brain/chapters/NN-name.md`, below the report marker. Use this EXACT template — it is the contract the CEO reads in their verify step:

```markdown
## Completion Report — YYYY-MM-DD [author stamp]

**Goal** — [echo what was asked, in one or two lines]

**Status** — done / partial / blocked

**Changed**
- path/or/area — what changed + why
- path/or/area — what changed + why

**Verified**
- [what you ran/checked and the result — tests, typecheck, manual check; name the command and the outcome]

**Flags**
- [anything you did differently than asked]
- [anything risky, or anything you're unsure about]
- [or: "none"]

**Commit** — <branch-name> @ <commit-hash>
```

Fill **Verified** with real checks, not "looks fine." Fill **Flags** honestly — those are the CEO's drill-down targets, and an empty Flags section on messy work will cost a round trip.

---

## Step 5 — When in doubt, STOP (don't decide)

If anything is ambiguous, contradictory, or outside this chapter's scope: do NOT guess and do NOT make a CEO-level decision. Stop, record it under **Flags** (Status `partial` or `blocked`), and let the CEO resolve it. Scope creep is a failure, not initiative.

---

## Step 6 — Commit on your worktree branch

Commit the code AND the report together, author-stamped:

```bash
git add <changed code files> brain/chapters/NN-name.md
git commit -m "chapter(NN): <name> — <short summary> <author stamp>"
```

Capture the commit hash and branch name — they go in the report's **Commit** line (re-edit the report if you committed first, or amend).

**Pushing:** a host tool (Claude Code / Codex) may push your branch so the CEO can pull it. Cowork CANNOT push (no credentials) — it commits locally only. Since worktrees share the same `.git`, the CEO can read your branch locally either way (`git show <branch>:brain/chapters/NN-name.md`, `git diff main..<branch>`), so a push is for syncing across machines, not required for the local CEO handoff.

- Host tool: `git push -u origin <branch>` (then report the branch is pushed).
- Cowork: commit locally; tell the user the branch is committed and ready for the CEO to verify locally; if they need it on another machine, they push.

Then tell the user: "Chapter NN reported and committed on `<branch>`. Tell the CEO: chapter NN done, check."

---

## Rules

- Do ONE chapter. Don't wander into other work, don't refactor unasked.
- Write boundary is strict: code files + your own chapter file only. Never the shared canon.
- The Completion Report template is fixed — the CEO reads these exact sections.
- Ambiguity → Flag and stop, never guess.
- Never push from Cowork; commit locally. Worktrees share `.git`, so the CEO verifies your branch locally regardless.
