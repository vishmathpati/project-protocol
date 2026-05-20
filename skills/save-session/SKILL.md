---
name: save-session
description: Save and close a project session. Updates the active tier's WORKLOG → CHANGELOG, STATUS, BRIEF. Triggers — "save", "save session", "close session", "end session", "done for today".
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*,date:*,wc:*,git:*)
---

# Save Session — Project Protocol

Closes the current session cleanly. Works for any project that follows the three-folder protocol layout (`cowork/`, `agents/`, `human/`).

---

## Step 1 — Detect tier

Identify which tier the current session belongs to:

- **Cowork session** — agent is Cowork; touches `cowork/` files primarily. Operates on `cowork/WORKLOG.md`, `cowork/STATUS.md`, `cowork/BRIEF.md`, `cowork/CHANGELOG.md`.
- **Agent session** — agent is Claude Code or Codex; touches `agents/` files primarily. Operates on `agents/WORKLOG.md`, `agents/STATUS.md`, `agents/BRIEF.md`, `agents/CHANGELOG.md`.

Determine tier from:
1. Which agent is running (Cowork vs. Claude Code/Codex — check available context).
2. If ambiguous, ask: "Which tier is this session — cowork/ or agents/?"

All steps below operate on the tier's matching files.

---

## Step 2 — Read WORKLOG

Read `<tier>/WORKLOG.md` (where `<tier>` is `cowork` or `agents`). This is your real-time log of what happened.

If WORKLOG is empty or in cleared state (`# Worklog — cleared after each session.`), reconstruct from session memory.

---

## Step 3 — Update `<tier>/CHANGELOG.md`

Read WORKLOG entries, categorize into Keep a Changelog format. If CHANGELOG doesn't exist, create with header first.

**Mapping WORKLOG → CHANGELOG categories:**
- `fixed:` entries → `### Fixed`
- `decided:` entries about new capabilities → `### Added`
- `decided:` entries about changes to existing features → `### Changed`
- `tried_failed:` entries → **excluded** (internal working notes)
- `found_bug:` entries → **excluded** unless fixed this session

**Only include things that actually shipped.**

Append a new dated section at the top (below header):

```markdown
## [YYYY-MM-DD] · [agent label]

### Added
- [new feature or capability shipped]

### Changed
- [modification to existing feature]

### Fixed
- [bug resolved]

### Removed
- [anything deliberately deleted]
```

Agent labels: `· Cowork`, `· Claude Code`, `· Codex`.

If nothing shipped: `- No changes shipped this session.`

CHANGELOG header (created once, never overwritten):

```markdown
# Changelog — [tier]

All notable changes to this tier are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]
```

**CHANGELOG.md is never cleared.**

---

## Step 4 — Check `agents/docs/INDEX.md` was updated

If any feature was added, page changed, or shared function modified this session:
- Verify `agents/docs/INDEX.md` was updated inline during the session.
- If not, add a reminder to `agents/STATUS.md` Next Actions: `[ ] Update agents/docs/INDEX.md — [what changed]`.

Do not update INDEX.md yourself during save-session — that should have happened inline.

(Only applies to agent-tier sessions. Cowork sessions skip this step.)

---

## Step 5 — Update `<tier>/STATUS.md`

Read `<tier>/STATUS.md`. Apply:
1. Update "Last updated" line: `> Last updated: YYYY-MM-DD · [agent label]`.
2. Add this session's one-line summary to Recent Sessions (rolling — keep last 5, drop oldest).
3. Update Health: add new bugs as 🔴, remove resolved ones.
4. Update "Pending human input" / "Needs CEO input": add open decisions, clear resolved ones.
5. Update "Next actions" to reflect what's actually next.

STATUS.md must never exceed 60 lines.

---

## Step 6 — Sign `<tier>/BRIEF.md` if decisions were made

If any architecture, tech stack, or significant scope decisions were made this session:

Append a new version block to `<tier>/BRIEF.md`:

```markdown
---

## v1.X — YYYY-MM-DD HH:MM · [agent label]

[describe only the delta — what changed or was decided this session]
[rejected options if any]
```

Rules:
- Increment version from last block.
- Include exact time (`date +%Y-%m-%d\ %H:%M`).
- Append only; never edit existing blocks.
- If no significant decisions: skip this step.
- **500-line limit:** if BRIEF.md approaches 500 lines, create `BRIEF-2.md` in the same tier, add pointer `> Continued in BRIEF-2.md` at the top of BRIEF.md, append the new block to BRIEF-2.md instead.

---

## Step 7 — Update `agents/DISCOVERIES.md` if needed

(Only applies to agent-tier sessions.)

If any UI patterns, component integrations, or design decisions proved out this session, append:

```
[YYYY-MM-DD] · [agent label] · [component/pattern] — what worked and why
```

Belongs here: shadcn component that integrated cleanly, layout pattern that solved a specific spacing problem, animation timing that felt right, CSS variable combination producing a specific effect.

Does NOT belong here: bug fixes (go to CHANGELOG), architecture decisions (go to BRIEF), session events (were in WORKLOG before clearing).

Never clear or reorganize. Append only.

---

## Step 8 — Update `human/agenda.md` if relevant

(Only applies when the session shipped a chapter or changed roadmap order.)

If a chapter completed: move it to ✓ Done in `human/agenda.md`, promote next chapter to Up Next.

If `agents/ROADMAP.md` or `agents/BRIEF.md` shape changed: re-derive `human/agenda.md` from current canon.

Otherwise: skip.

---

## Step 9 — Clear `<tier>/WORKLOG.md`

Replace contents with:

```
# Worklog — [tier]
> Cleared after each session.
```

---

## Step 10 — Git sync (commit, push, auto-merge into `main`)

Without this step the canon updates from steps 3–9 stay stranded on the session's worktree branch. The user's local folder is on `main` and will not see them. Run this every save.

### 10a — Capture git state

From the active worktree directory, run:

```bash
git rev-parse --show-toplevel       # current worktree path
git rev-parse --abbrev-ref HEAD     # current branch
git status --porcelain              # uncommitted changes
git worktree list --porcelain       # all worktrees + which holds main
git remote -v                       # confirm a remote exists
```

If `HEAD` is detached (not on a branch): **STOP** and report — "Not on a branch — cannot auto-merge. Checkout a branch first, then re-run save."

If the repo has no remote: skip the push in 10c and the push in 10d; still do the local merge into `main`.

### 10b — Stage and commit session updates

If `git status --porcelain` is clean: skip to 10c.

Otherwise, separate the changed files into two groups:

- **Protocol .md files** under `cowork/`, `agents/`, or `human/` → expected output of steps 3–9. Stage automatically.
- **Anything else** (code files, configs, untracked files outside the protocol folders) → list them to the user and ASK before staging. Never sweep arbitrary changes into a `save-session` commit.

Stage protocol files only:

```bash
git add cowork/ agents/ human/
git commit -m "chore(session): save session YYYY-MM-DD · <agent label>"
```

### 10c — Push the worktree branch to GitHub

If current branch is already `main`: skip to 10d.

```bash
git push -u origin <current-branch>
```

If push fails (auth, non-fast-forward, network): **STOP** and report the exact error. Do not attempt the merge — leave the user in a clean recoverable state.

### 10d — Auto-merge into `main`

From `git worktree list --porcelain`, find the worktree on `main` (the user's local folder in Finder). Call its absolute path `<MAIN_PATH>`.

If current branch IS `main`: just run `git -C "<MAIN_PATH>" push origin main` and skip the merge.

Otherwise:

```bash
git -C "<MAIN_PATH>" fetch origin
git -C "<MAIN_PATH>" merge --no-ff <current-branch> -m "merge: session YYYY-MM-DD · <agent label>"
git -C "<MAIN_PATH>" push origin main
```

If merge fails (conflicts): **STOP** and report — list the conflicted files and tell the user: "Resolve conflicts in `<MAIN_PATH>`, then run `git merge --continue && git push origin main`."

### 10e — Report git outcome (feeds into Step 11)

Capture for the final confirmation:
- Files committed (count + tier)
- Branch pushed to origin
- Merge commit SHA on main (or "fast-forward")
- Main pushed to origin
- Anything skipped or that requires user follow-up

---

## Step 11 — Confirm

```
✅ <tier>/CHANGELOG.md updated — [N Added, N Changed, N Fixed]
✅ <tier>/STATUS.md updated · [agent label]
✅ <tier>/BRIEF.md signed (v1.X) — [Y/N, or "no decisions this session"]
✅ <tier>/WORKLOG.md cleared
✅ agents/DISCOVERIES.md appended — [Y/N]
✅ human/agenda.md updated — [Y/N]
✅ Git: committed N file(s) · pushed <branch> → GitHub · merged into main · main pushed
   Your local folder is now up to date.

Session closed.
```

If git sync was skipped or halted partway, replace the last `✅ Git:` line with:

```
⚠️ Git: <what happened> — <exact command the user needs to run>
```

---

## Rules

- Never make up content that wasn't in the session. Only log what actually happened.
- If nothing changed this session, still run through the steps — update STATUS.md at minimum.
- CHANGELOG.md, DISCOVERIES.md, BRIEF.md are never overwritten — only appended to.
- Goal: a new session reading `<tier>/STATUS.md` + `<tier>/BRIEF.md` has 100% context to continue without asking the user anything.
