---
name: git
description: Git operations under the Project Protocol — committing, branching, creating or syncing a worktree, merging canon locally, pushing, and the CEO verify-by-reading loop. Use whenever you commit, branch, create or sync a worktree, push, read a worker's branch, or touch git in any tool. The /ceo, /worker, and /solo roles call this. Triggers — "commit this", "make a branch", "create a worktree", "sync the canon", "merge main", "push", "git.lock", "git is stuck".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*, rm:*)
---

# Git — Project Protocol

Everything git in this protocol, in one place. The role skills (`/ceo`, `/worker`, `/solo`) and the agent both reach for this whenever git is touched.

Two facts drive every rule below:

1. **The canon is one folder — `brain/`.** Worker authority is chapter-scoped inside an isolated worktree. The CEO owns approval, reconciliation, and the integration branch.
2. **Worktrees of a repo share ONE local `.git`.** A commit on any worktree's branch is instantly visible to every other worktree with **no push**. GitHub is a **BACKUP**, not the sync path. Moving work between worktrees is a *local* `git merge`, offline and instant.

---

## Step 0 — Detect context

Detect the **tool**, checkout topology, current branch/commit, and declared integration branch. The application chooses Local vs Worktree before `/ceo`, `/worker`, or `/solo` is invoked; checkout topology never selects the role.

**Tool** (this is the author stamp, and decides whether you can push):

- `CLAUDE_PLUGIN_ROOT` set → **Claude Code** · stamp `· Claude Code` · can push
- `CODEX_PLUGIN_ROOT` set → **Codex** · stamp `· Codex` · can push
- neither set → stamp `· Agent` · treat as a full-capability host · can push

**Worktree?** Run:

```bash
git rev-parse --abbrev-ref HEAD     # branch name (or "HEAD" if detached)
git rev-parse --show-toplevel       # this worktree's root path
git worktree list --porcelain       # all worktrees + which holds main
```

Recognize the worktree flavor:

- **Codex worktree** — lives under `~/.codex/worktrees`, usually in **detached HEAD** (branch shows `HEAD`).
- **Claude Code worktree** — lives under `.claude/worktrees/`, branch named `worktree-*`.
- **Manual worktree** — created by a plain `git worktree add`, any path/branch.
- **Not a worktree** — usually the integration checkout. Confirm its actual branch; do not assume it is named `main`.

If already in a worktree, use it regardless of role. If in the local checkout, show this notice once before the first edit:

> This session is using the shared local checkout. A worktree is recommended for isolation, parallel work, and easier review. Continue locally only if that was intentional.

Honor the user's choice. CEO and solo may continue locally. A local worker must use a clean dedicated chapter branch and must never edit on the integration branch.

If an app-created worktree starts at detached HEAD, create a named branch before the first commit: `ch-NN-name` for a worker, and a clear task branch for CEO or solo. The detached checkpoint remains recoverable, but unnamed commits are a poor continuation contract.

---

## Step 1 — Commit conventions

**Message format:**

```
type(scope): summary [ch-NN] · Agent
```

- **type** ∈ `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
- **scope** — the area touched (a module, page, or `session`), optional but preferred.
- **summary** — imperative, one line.
- **`[ch-NN]`** — the chapter this work belongs to. **Omit it for non-chapter work** (e.g. session saves, plugin chores).
- **Agent** — the author stamp from Step 0: `· Claude Code`, `· Codex`, or `· Agent` (unknown-host fallback).

Examples:

```
feat(auth): add password reset flow [ch-03] · Codex
fix(dashboard): correct totals rollup [ch-07] · Claude Code
chore(session): save session 2026-06-24 · Claude Code
```

**When to commit:**

- Commit at **meaningful checkpoints** — a working slice, a passing test, a completed sub-task — not one giant end-of-day dump, and not after every line.
- **Always a final commit** that carries the **Completion Report** (the report lives in `brain/chapters/NN-name.md`; commit code + report together). That commit is the contract the CEO reads.

---

## Step 2 — Branch naming

- The **declared integration branch** is where accepted canon lands; do not hardcode `main`. A CEO session may itself run in a worktree proposal branch and reconcile through the checkout that holds the integration branch.
- **Worker branches are named `ch-NN-name`** — matching the chapter (`brain/chapters/NN-name.md`). One chapter → one branch → normally one worktree; deliberate local mode uses the same branch contract without a linked worktree.

```
ch-03-auth-reset
ch-07-dashboard-rollup
```

This keeps the branch, the worktree, the chapter file, and the `[ch-NN]` commit tag all in lock-step.

---

## Step 3 — Local sync rule (the important one)

**To bring the latest integration state into a worktree, merge or rebase LOCALLY. Never manually copy canon between chats or worktrees.**

Inside the worktree branch:

```bash
git merge <integration-branch>          # or: git rebase <integration-branch>
```

Because all worktrees share one object store, the integration branch is already present locally; there is nothing to fetch merely to see local commits.

If the merge conflicts, **STOP and report it** (a worker records it under Flags) — do not guess through a canon conflict.

---

## Step 4 — Per-tool worktree setup

When the user selects Worktree, **new worktrees branch from the intended LOCAL base branch/checkpoint, not an accidentally stale remote.** When the user selects Local, do not create a worktree behind their back; apply the one-time recommendation and continue under the role's local-checkout rules.

### Claude Code

1. **Verify `worktree.baseRef` BEFORE creating any worktree.** Read the active Claude Code settings (`.claude/settings.json` in the project root, or `~/.claude/settings.json` if no project-level file exists) and check the value of `worktree.baseRef`.

   ```bash
   # Check project-level settings first, fall back to user-level:
   cat .claude/settings.json 2>/dev/null || cat ~/.claude/settings.json 2>/dev/null
   ```

   - If `worktree.baseRef` is `"head"` → proceed to step 2.
   - If it is **missing, `null`, or `"origin/HEAD"`** (the default) → **STOP and warn the user:**

   > ⚠️ **`worktree.baseRef` is not set to `"head"`.**
   > With the current setting, new worktrees will branch from the **stale remote** (`origin/HEAD`), which forces a push before work can begin. Add this to your Claude Code settings (`.claude/settings.json` or `~/.claude/settings.json`):
   >
   > ```json
   > { "worktree": { "baseRef": "head" } }
   > ```
   >
   > Confirm once you've saved the change, then we'll proceed.

   Do not create the worktree until the user confirms the setting is in place.

2. **Set the base ref to local HEAD** (if not already set — do this once per project or globally):

   ```json
   { "worktree": { "baseRef": "head" } }
   ```

   The default is `origin/HEAD` (= the remote) — that default is the cause of "I had to push first." Setting `head` makes new worktrees branch from local HEAD.

3. **Create the worktree:**

   ```bash
   claude --worktree <name>
   ```

   …or use the desktop **auto-worktree** (it creates one per session under `.claude/worktrees/`, branch `worktree-*`).

4. **Bring gitignored files across.** A new worktree is a clean checkout — `.env` and other gitignored files don't come with it. Add a **`.worktreeinclude`** file listing them (e.g. `.env`, `.env.local`) so Claude Code copies them into each new worktree.

### Codex

1. Start a **"Worktree" thread** and **select the canon branch as the base**. Codex branches from the **local HEAD of the selected branch** — so selecting the canon branch is the whole trick (no push needed).
2. The worktree lives under `~/.codex/worktrees` in **detached HEAD**.
3. **Bring env files across** with a **Codex local-environment setup script** (runs on worktree creation) that copies `.env` etc. into the worktree.
4. Thread controls:
   - **"Create branch here"** — names the current (detached) worktree's branch (use `ch-NN-name`).
   - **"Handoff"** — moves a thread between **Local** and **Worktree**.

---

## Step 5 — Canon write-boundary

This is what keeps parallel-worktree merges conflict-free:

- **Workers** edit **code + their own chapter file** (`brain/chapters/NN-name.md`) only.
- **The CEO** owns the **shared canon** — `brain/STATUS.md`, `brain/BRIEF.md`, `brain/ROADMAP.md`, `brain/WONT-DO.md` (and `brain/CHANGELOG.md`, `brain/agenda.md`).

Workers may touch overlapping files when their chapter contracts require it, so conflicts are possible and must be reconciled by the CEO. Worktree isolation prevents uncontrolled shared working-copy edits; it does not eliminate Git conflicts.

---

## Step 6 — Push policy

**Push to GitHub is a BACKUP, not a sync requirement.** Local merges (Step 3) already move work between worktrees. So:

- **Default: push at close.** End of session / chapter close, via `save-session`. That's the normal push point.
- **A worker MAY push its branch manually** as a backup on a long or risky chapter — optional, never required for the handoff.
- **The CEO↔worker verify loop never needs a push** — it's all local (Step 8).
- **Whoever runs the session pushes at close.** The host tool (Claude Code / Codex / unknown-host `· Agent`) runs `git push`.

---

## Step 7 — CEO verify-by-reading

The CEO verifies a worker's finished chapter **locally, with no GitHub** — the worktrees share `.git`, so the worker's branch is already readable:

```bash
git show <branch>:brain/chapters/NN-name.md     # read the Completion Report (the contract)
git diff <integration-branch>..<branch>          # read the actual code change
```

Read the **report** first (Goal / Status / Changed / Verified / Flags), then the **diff** to confirm it matches. No checkout, no fetch, no push. Find `<branch>` from `git worktree list --porcelain` or ask the user.

After accepting, the CEO merges and (optionally) removes the worktree:

```bash
git merge --no-ff <branch> -m "merge: chapter NN <name> · <stamp>"
git worktree remove <worktree-path>     # add --force only after confirming nothing unmerged
```

---

## Step 8 — Lockfile / dependency rule

**Don't change lockfiles or dependencies in two worktrees at once** — they conflict at merge (lockfiles regenerate divergently and don't auto-merge).

- Do dependency changes (add/remove/upgrade packages, regenerate the lockfile) **on the canon branch**.
- Workers that need a new dependency **Flag it** to the CEO rather than installing it in their worktree.

---

## Quick reference

| Situation | Command / action |
|---|---|
| Which tool / can I push? | env vars (Step 0). All hosts can push. |
| Pull latest canon into a worktree | `git merge <integration-branch>` — local (Step 3) |
| Name a worker branch | `ch-NN-name` (Step 2) |
| Commit message | `type(scope): summary [ch-NN] · Agent` (Step 1) |
| New worktree, Claude Code | `worktree.baseRef: "head"` + `claude --worktree <name>` (Step 4) |
| New worktree, Codex | "Worktree" thread, select canon branch as base (Step 4) |
| CEO reads a worker's branch | `git show <branch>:…` + `git diff <integration-branch>..<branch>` (Step 7) |
| Push | at close (default) (Step 6) |

---

## Rules

- The canon is one folder, `brain/`. Workers may propose any chapter-required code or canon change in their isolated branch; the CEO owns approval, merge, and shared-state reconciliation.
- Local vs Worktree is a user/application checkout choice; CEO/worker/solo is an independent authority choice. Every role supports an existing worktree, and local mode remains supported with a one-time isolation notice.
- Worktrees share one local `.git` — sync between them with a **local merge**, never push-then-pull. GitHub is a backup.
- New worktrees must branch from **local HEAD** of the canon branch (`baseRef: head` in Claude Code; select the canon branch in Codex), or you reintroduce "push first."
- Don't touch lockfiles/dependencies in two worktrees at once — do them on the canon branch.
- Every commit carries the author stamp; the final commit carries the Completion Report.
