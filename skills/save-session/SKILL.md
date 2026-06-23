---
name: save-session
description: Save and close a project session. Updates brain/WORKLOG → CHANGELOG, STATUS, BRIEF. Triggers — "save", "save session", "close session", "end session", "done for today".
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*,date:*,wc:*,git:*)
---

# Save Session — Project Protocol

Closes the current session cleanly. Works for any project that follows the protocol layout — a single canon in `brain/`.

There is ONE canon. Every step operates on `brain/WORKLOG.md`, `brain/STATUS.md`, `brain/BRIEF.md`, `brain/CHANGELOG.md`, `brain/DISCOVERIES.md`, and `brain/agenda.md`.

---

## Step 0 — Determine the author stamp

We detect which tool is running ONLY to label entries — never to pick a folder. Detect via environment variables:

- `CLAUDE_PLUGIN_ROOT` set → stamp `· Claude Code`
- `CODEX_PLUGIN_ROOT` set → stamp `· Codex`
- neither set → stamp `· Cowork`

Call this value the **author stamp**. Apply it to the CHANGELOG dated section and the BRIEF version block below.

---

## Step 1 — Read WORKLOG

Read `brain/WORKLOG.md`. This is your real-time log of what happened.

If WORKLOG is empty or in cleared state (`# Worklog — cleared after each session.`), reconstruct from session memory.

---

## Step 2 — Update `brain/CHANGELOG.md`

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
## [YYYY-MM-DD] [author stamp]

### Added
- [new feature or capability shipped]

### Changed
- [modification to existing feature]

### Fixed
- [bug resolved]

### Removed
- [anything deliberately deleted]
```

The author stamp is one of `· Cowork`, `· Claude Code`, `· Codex` (from Step 0).

If nothing shipped: `- No changes shipped this session.`

CHANGELOG header (created once, never overwritten):

```markdown
# Changelog

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]
```

**CHANGELOG.md is never cleared.**

---

## Step 3 — Check `brain/docs/INDEX.md` was updated

If any feature was added, page changed, or shared function modified this session:
- Verify `brain/docs/INDEX.md` was updated inline during the session.
- If not, add a reminder to `brain/STATUS.md` Next Actions: `[ ] Update brain/docs/INDEX.md — [what changed]`.

Do not update INDEX.md yourself during save-session — that should have happened inline.

---

## Step 4 — Update `brain/STATUS.md`

Read `brain/STATUS.md`. Apply:
1. Update "Last updated" line: `> Last updated: YYYY-MM-DD [author stamp]`.
2. Add this session's one-line summary to Recent Sessions (rolling — keep last 5, drop oldest).
3. Update Health: add new bugs as 🔴, remove resolved ones.
4. Update "Pending human input" / "Needs CEO input": add open decisions, clear resolved ones.
5. Update "Next actions" to reflect what's actually next.

STATUS.md must never exceed 60 lines.

---

## Step 5 — Sign `brain/BRIEF.md` if decisions were made

If any architecture, tech stack, or significant scope decisions were made this session:

Append a new version block to `brain/BRIEF.md`:

```markdown
---

## v1.X — YYYY-MM-DD HH:MM [author stamp]

[describe only the delta — what changed or was decided this session]
[rejected options if any]
```

Rules:
- Increment version from last block.
- Include exact time (`date +%Y-%m-%d\ %H:%M`).
- The author stamp is one of `· Cowork`, `· Claude Code`, `· Codex` (from Step 0).
- Append only; never edit existing blocks.
- If no significant decisions: skip this step.
- **500-line limit:** if BRIEF.md approaches 500 lines, create `brain/BRIEF-2.md`, add pointer `> Continued in BRIEF-2.md` at the top of BRIEF.md, append the new block to BRIEF-2.md instead.

---

## Step 6 — Update `brain/DISCOVERIES.md` if needed

If any UI patterns, component integrations, or design decisions proved out this session, append:

```
[YYYY-MM-DD] [author stamp] · [component/pattern] — what worked and why
```

Belongs here: shadcn component that integrated cleanly, layout pattern that solved a specific spacing problem, animation timing that felt right, CSS variable combination producing a specific effect.

Does NOT belong here: bug fixes (go to CHANGELOG), architecture decisions (go to BRIEF), session events (were in WORKLOG before clearing).

Never clear or reorganize. Append only.

---

## Step 7 — Update `brain/agenda.md` if relevant

If a chapter completed: move it to ✓ Done in `brain/agenda.md`, promote next chapter to Up Next.

If `brain/ROADMAP.md` or `brain/BRIEF.md` shape changed: re-derive `brain/agenda.md` from current canon.

Otherwise: skip.

---

## Step 8 — Clear `brain/WORKLOG.md`

Replace contents with:

```
# Worklog
> Cleared after each session.
```

---

## Step 9 — Invoke `audit-before-close`

Before committing, run the close-gate audit:

```
Skill("audit-before-close")
```

This is unconditional. `audit-before-close` is idempotent — if it was already invoked earlier in this session, the double-call is accepted (locked Risk 7). Surface any findings to the user before proceeding to Step 10.

---

## Step 10 — Git sync — environment-aware

There are two real cases now, keyed on whether the runtime can push:

- **Host tool (Claude Code or Codex)** — `CLAUDE_PLUGIN_ROOT` or `CODEX_PLUGIN_ROOT` is set. The runtime CAN commit and push. See branch (a) / (b).
- **Cowork** — neither env var is set. Cowork CAN commit locally but CANNOT push (no credentials in its sandbox). See branch (c).

**Staging — same rule in every branch:**
- Stage `brain/` (plus root `CLAUDE.md` / `README.md` if changed).
- **Protocol .md files** under `brain/`, plus changed root `CLAUDE.md` / `README.md` → stage automatically.
- **Anything else** → list to the user and ASK before staging. Never sweep code files into a save-session commit.

Determine the environment from the env vars above (this is the same detection used for the author stamp in Step 0).

---

### Branch (a) — host tool, working directly on `main`

Detected when: `CLAUDE_PLUGIN_ROOT` or `CODEX_PLUGIN_ROOT` is set, AND `git rev-parse --abbrev-ref HEAD` returns `main`.

Simple add → commit → push:

```bash
git add brain/ CLAUDE.md README.md
git commit -m "chore(session): save session YYYY-MM-DD <author stamp>"
git push origin main
```

(Only add `CLAUDE.md` / `README.md` to the stage command if they changed.)

If `git status --porcelain` is clean: skip the commit; still run `git push origin main` to ensure main is up to date.

If push fails (auth, non-fast-forward, network): **STOP** and report the exact error.

---

### Branch (b) — host tool, on a worktree branch

Detected when: `CLAUDE_PLUGIN_ROOT` or `CODEX_PLUGIN_ROOT` is set, AND current branch is NOT `main`.

This is the existing merge-to-main flow:

**10b-1 — Capture git state**

```bash
git rev-parse --show-toplevel       # current worktree path
git rev-parse --abbrev-ref HEAD     # current branch
git status --porcelain              # uncommitted changes
git worktree list --porcelain       # all worktrees + which holds main
git remote -v                       # confirm a remote exists
```

If `HEAD` is detached: **STOP** — "Not on a branch — cannot auto-merge. Checkout a branch first."

If no remote: skip pushes; still do the local merge.

**10b-2 — Stage and commit**

Separate files (same staging rule above). Stage protocol files only:

```bash
git add brain/ CLAUDE.md README.md
git commit -m "chore(session): save session YYYY-MM-DD <author stamp>"
```

**10b-3 — Push worktree branch**

```bash
git push -u origin <current-branch>
```

If push fails: **STOP** and report. Do not attempt merge.

**10b-4 — Merge into main**

From `git worktree list --porcelain`, find `<MAIN_PATH>` (worktree on `main`):

```bash
git -C "<MAIN_PATH>" fetch origin
git -C "<MAIN_PATH>" merge --no-ff <current-branch> -m "merge: session YYYY-MM-DD <author stamp>"
git -C "<MAIN_PATH>" push origin main
```

If merge fails (conflicts): **STOP** — list conflicted files and tell the user: "Resolve conflicts in `<MAIN_PATH>`, then run `git merge --continue && git push origin main`."

---

### Branch (c) — Cowork (can commit, cannot push)

Detected when: neither `CLAUDE_PLUGIN_ROOT` nor `CODEX_PLUGIN_ROOT` is set.

Cowork CAN commit locally but CANNOT push (no credentials in its sandbox). So:

1. Stage and commit locally (same staging rule above):

```bash
git add brain/ CLAUDE.md README.md
git commit -m "chore(session): save session YYYY-MM-DD <author stamp>"
```

2. Then output the exact `git push` command as a copy-paste snippet for the user to run themselves:

````
✅ Committed locally. Cowork can't push — run this in your terminal to sync:

```bash
git push origin main
```
````

Replace `YYYY-MM-DD` and `<author stamp>` with the actual values. Do NOT claim to have pushed. Note this in Step 11 with a ⚠️ line on the push status.

---

### 10-final — Report git outcome (feeds into Step 11)

Capture for the final confirmation:
- Which branch was taken (a / b / c)
- Files staged (count)
- Branch pushed to origin (or "committed locally; push snippet provided" for Cowork)
- Merge commit SHA on main (or "fast-forward" or "N/A — working on main")
- Anything skipped or requiring user follow-up

---

## Step 11 — Confirm

```
✅ brain/CHANGELOG.md updated — [N Added, N Changed, N Fixed]
✅ brain/STATUS.md updated [author stamp]
✅ brain/BRIEF.md signed (v1.X) — [Y/N, or "no decisions this session"]
✅ brain/WORKLOG.md cleared
✅ audit-before-close: ran (Step 9) — [findings or "clean"]
✅ brain/DISCOVERIES.md appended — [Y/N]
✅ brain/agenda.md updated — [Y/N]
✅ Git: committed N file(s) · pushed <branch> → GitHub · merged into main · main pushed
   Your local folder is now up to date.

Session closed.
```

If git sync was skipped or halted partway, replace the `✅ Git:` line with:

```
⚠️ Git: <what happened> — <exact command the user needs to run>
```

For Cowork sessions (branch c), replace the `✅ Git:` line with:

```
⚠️ Git: committed locally — Cowork can't push. Run the snippet above (`git push origin main`) in your terminal to sync.
```

---

## Rules

- Never make up content that wasn't in the session. Only log what actually happened.
- If nothing changed this session, still run through the steps — update STATUS.md at minimum.
- CHANGELOG.md, DISCOVERIES.md, BRIEF.md are never overwritten — only appended to.
- Goal: a new session reading `brain/STATUS.md` + `brain/BRIEF.md` has 100% context to continue without asking the user anything.
