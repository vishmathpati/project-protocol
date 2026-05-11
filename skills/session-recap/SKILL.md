---
name: session-recap
description: >
  Mid-session snapshot for any project following the standard project protocol.
  Use when someone says "recap", "where are we", "what have we done", "catch me up",
  or when context feels lost after a long session. Reads WORKLOG.md and STATUS.md
  to give a crisp snapshot of what happened this session and what is still open.
  Does not save the session — use save-session for that.
allowed-tools: Read, Glob, Bash(ls:*,date:*,git:*,pwd:*)
---

# Session Recap

A mid-session orientation check. Not a save — just a clear view of where things
stand right now so work can continue without losing the thread.

---

## Step 1 — Read context

Read in order:

1. Run `pwd` and `git status --short --branch` if this is a git repository.
   - If the branch is detached, say so clearly.
   - If the cwd contains `.codex/worktrees/`, warn: this is a **Codex worktree** — local uncommitted changes from the main checkout are not present here.
   - If the cwd contains `.claude/worktrees/`, warn: this is a **Claude Code worktree** — local uncommitted changes from the main checkout are not present here.
   - In either worktree case, state the main checkout path (strip the worktree suffix) so the user knows where the real files live.
   - If there are uncommitted changes, summarize them briefly.
2. `WORKLOG.md` — real-time log of this session's events.
3. `STATUS.md` — the project's health at session start.
4. `BRIEF.md` — latest locked decisions, especially the newest version block.
5. Most recent file in `sessions/` if the directory exists.
   - If `sessions/` is missing, do not treat that as a problem unless this project explicitly requires session files.

---

## Step 2 — Output the snapshot

```
📋 SESSION RECAP — YYYY-MM-DD
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
- If WORKLOG.md is empty, say so — session may have just started.
- Surface any STATUS.md blockers even if not discussed this session.
- Never report "no commit", "no branch", "no file changes", or similar git state unless verified with `git status --short --branch` in the current cwd.
- If STATUS.md and git state disagree, trust live git state and mention the mismatch.
- Worktree check is mandatory — both `.codex/worktrees/` and `.claude/worktrees/` patterns must be detected and surfaced before reading any project files.
- Do not trigger save-session automatically. If the user wants to save, they'll say so.
- End with: "Want to continue, or save and close?"
