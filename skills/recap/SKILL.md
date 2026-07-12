---
name: recap
description: Role-aware orientation at the start of a CEO, worker, or solo session, after compaction, on returning later, or whenever the user asks where things stand. Reads live Git and canon; never saves or chooses authority.
allowed-tools: Read, Glob, Bash(ls:*, pwd:*, date:*, git status:*, git worktree:*, git log:*)
---

# Recap

Read-only orientation from live Git and canon. It does not save, select a role,
or close work.

---

## Step 1 — Verify role and checkout

Use the role the human invoked; never infer authority from the branch alone. Run
`pwd`, `git status --short --branch`, and `git worktree list --porcelain` first.

## Step 2 — Read context

> Single canon: all project state lives in `brain/`. Recap always reads `brain/STATUS.md` and `brain/WORKLOG.md` regardless of which tool (Claude Code or Codex) saved last — this is what prevents empty recaps.

Read in order:

1. Run `pwd` and `git status --short --branch` if this is a git repository.
   - If the branch is detached, say so clearly and record the checkpoint commit.
   - If the cwd contains `.codex/worktrees/`, state: this is a **Codex worktree** — an isolated real checkout; uncommitted changes in other worktrees are not present here.
   - If the cwd contains `.claude/worktrees/`, state: this is a **Claude Code worktree** — an isolated real checkout; uncommitted changes in other worktrees are not present here.
   - For any worktree, identify the repository's other checkout paths from `git worktree list`; never call one checkout the location of the "real files."
   - If this is not a worktree, give the one-time notice: "This session is using the shared local checkout. A worktree is recommended for isolation and easier review. Continue locally only if that was intentional." Do not repeat it later in the same session.
   - If there are uncommitted changes, summarize them briefly.
2. Root `CLAUDE.md` — overall project orientation: active skills, rules.
3. `brain/STATUS.md` — project health, blockers, last-known state.
4. Tail of `brain/WORKLOG.md` — meaningful recovery notes for unfinished work. Read only the useful tail.

---

## Step 3 — Output the snapshot

```
📋 RECAP — YYYY-MM-DD · <role>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Done this session:
  ✓ [specific thing completed]
  ✓ [specific thing completed]

Decisions locked:
  • [decision and short reason]

Still open:
  ○ [unfinished item from this session]

Carried from last session (not touched yet):
  ○ [item from STATUS.md or last session file]

Where we are:
  [1–2 sentences — what's working, what's blocked, what's next.]
```

---

## Rules

- Keep it short. Purpose is orientation, not documentation.
- If `brain/WORKLOG.md` is empty, say so — session may have just started.
- Surface any `brain/STATUS.md` blockers even if not discussed this session.
- Never report "no commit", "no branch", "no file changes", or similar git state unless verified with `git status --short --branch` in the current cwd.
- If STATUS.md and git state disagree, trust live git state and mention the mismatch.
- Worktree check is mandatory — both `.codex/worktrees/` and `.claude/worktrees/` patterns must be detected and surfaced before reading any project files.
- Do not trigger save-session automatically. If the user wants to save, they'll say so.
- End with the role's immediate next action. Do not ask a generic question when canon already answers it.
