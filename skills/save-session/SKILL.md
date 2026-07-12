---
name: save-session
description: Save and close a project session by persisting the active role's meaningful work into the correct canon, committing only owned changes, and reporting branch and push state. Use when the user says save, save session, close, or finish for today.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*)
---

# Save Session

Persistence dispatcher for CEO, worker, and solo sessions. Saving is not completion, approval, or merge.

## 1. Verify identity

Determine the human-invoked role. Run `git status --short --branch`, `git rev-parse --show-toplevel`, and `git worktree list --porcelain`. Record repository, worktree, branch, and active chapter. Never infer the role from Git alone.

## 2. Read recovery state

Read `brain/WORKLOG.md`, `brain/STATUS.md`, the active chapter, and changed-file status. WORKLOG is a temporary recovery buffer, not a complete transcript. If useful context exists only in the conversation, capture it before clearing.

## 3. Fold durable information into its owner

- Current state, active chapters, blockers, pending human decisions, and one Last saved session → `STATUS.md`.
- Changed durable project contract or locked project decision → update the relevant section of `BRIEF.md`.
- Accepted or shipped outcome → `CHANGELOG.md`.
- Proven reusable implementation lesson → `DISCOVERIES.md`.
- Evidence-backed preference signal → `TASTE.md`.
- Immediate human checkout, role, chapter, or decision → `agenda.md`.
- Unfinished chapter recovery → append Carry-over or run `handoff`.

Do not write empty history, discussion summaries, rejected variants, routine edits, or worker work awaiting CEO approval into CHANGELOG.

## 4. Apply the role contract

### CEO

Reconcile only approved work into shared canon. Update agenda from live chapter and Git state. In the local integration checkout, commit explicit owned files there. In a CEO worktree, commit the CEO proposal branch and use the CEO/Git reconciliation path before reporting anything as shared canon; unfinished CEO work may remain on the proposal branch. Saving does not approve an unverified worker branch.

### Worker

Do not merge. If unfinished, write Carry-over or Handoff. If finished, append the Completion Report with verification, diff, canon-change, untouched-region, flag, branch, and commit evidence. Commit explicit chapter-owned files and push the worker branch. Report that it is ready for CEO review.

### Solo

Persist the small result and its evidence in the current local checkout or worktree. Run `completion-check` before calling substantial work done. Update shared canon only where the completed result requires it. Commit explicit files and push the current named branch.

## 5. Clear only folded recovery entries

Remove WORKLOG entries whose durable content has been folded or is no longer needed. Preserve unresolved entries. An empty WORKLOG is valid; no cleared-state marker is required.

## 6. Git safely

- Never use `git add -A` or stage a whole directory blindly.
- Stage explicit files owned by this session.
- Preserve unrelated dirty or untracked files.
- Do not switch branches, merge, or delete a worktree unless the role contract explicitly requires and authorizes it.
- Push the current owned branch and report any failure exactly.

## 7. Report

Return: role, saved state, canon files changed, carry-over/report path, commit hash, branch, push result, remaining dirty files, and the exact next human action.

## Distinctions

- WORKLOG remembers unfinished session detail.
- Handoff transfers unfinished work to another session/tool.
- Completion Check proves a finished result against its contract.
- Project Audit checks system-wide drift.
- Save Session persists role-owned state; it does none of the above implicitly.
