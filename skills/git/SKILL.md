---
name: git
description: Git operations under the Project Protocol — committing, branching, creating or syncing a worktree, merging canon locally, pushing, the CEO verify-by-reading loop, and one-time git setup in Cowork. Use whenever you commit, branch, create or sync a worktree, push, read a worker's branch, or touch git in any tool. The /ceo, /worker, and /solo roles call this. Triggers — "commit this", "make a branch", "create a worktree", "sync the canon", "merge main", "push", "set up git in Cowork", "git.lock", "git is stuck".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*, rm:*)
---

# Git — Project Protocol

Everything git in this protocol, in one place. The role skills (`/ceo`, `/worker`, `/solo`) and the agent both reach for this whenever git is touched.

Two facts drive every rule below:

1. **The canon is one folder — `brain/`.** Chapters live in `brain/chapters/NN-name.md`. The CEO owns the shared canon; workers own only their own chapter file + code.
2. **Worktrees of a repo share ONE local `.git`.** A commit on any worktree's branch is instantly visible to every other worktree with **no push**. GitHub is a **BACKUP**, not the sync path. Moving work between worktrees is a *local* `git merge`, offline and instant.

And one hard constraint:

- **Cowork can read git and commit LOCALLY but CANNOT push** — it has no credentials in its sandbox. Host tools (Claude Code / Codex) push. In Cowork you commit, then emit the exact `git push` command for the user to run.

---

## Step 0 — Detect context

Two things to detect: which **tool** is running, and whether you're in a **worktree**.

**Tool** (this is the author stamp, and decides whether you can push):

- `CLAUDE_PLUGIN_ROOT` set → **Claude Code** · stamp `· Claude Code` · can push
- `CODEX_PLUGIN_ROOT` set → **Codex** · stamp `· Codex` · can push
- neither set → **Cowork** · stamp `· Cowork` · **cannot push** (commit locally, emit the push command)

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
- **Not a worktree** — you're in the main checkout, on `main` (the canon branch).

The CEO works on the **main / canon branch**. Workers work on a **worktree branch**. If a worker finds itself on `main`, STOP and say so — a worker works on a branch, not the canon.

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
- **Agent** — the author stamp from Step 0: `· Cowork`, `· Codex`, or `· Claude Code`.

Examples:

```
feat(auth): add password reset flow [ch-03] · Codex
fix(dashboard): correct totals rollup [ch-07] · Claude Code
chore(session): save session 2026-06-24 · Cowork
```

**When to commit:**

- Commit at **meaningful checkpoints** — a working slice, a passing test, a completed sub-task — not one giant end-of-day dump, and not after every line.
- **Always a final commit** that carries the **Completion Report** (the report lives in `brain/chapters/NN-name.md`; commit code + report together). That commit is the contract the CEO reads.

---

## Step 2 — Branch naming

- The **CEO works on the main / canon branch** (`main`). Never branch the CEO.
- **Worker branches are named `ch-NN-name`** — matching the chapter (`brain/chapters/NN-name.md`). One chapter → one branch → one worktree.

```
ch-03-auth-reset
ch-07-dashboard-rollup
```

This keeps the branch, the worktree, the chapter file, and the `[ch-NN]` commit tag all in lock-step.

---

## Step 3 — Local sync rule (the important one)

**To pull the latest canon into a worktree, merge LOCALLY — never push-then-pull through GitHub.**

Inside the worktree branch:

```bash
git merge main          # or: git rebase main
```

Because all worktrees share one object store, this is **instant and offline** — `main` is already present locally; there is nothing to fetch from GitHub. The old habit of "push from the canon, then pull in the worktree" is wrong here and is the root cause of "I had to push first."

If the merge conflicts, **STOP and report it** (a worker records it under Flags) — do not guess through a canon conflict.

---

## Step 4 — Per-tool worktree setup

The goal in every tool: **new worktrees branch from your LOCAL HEAD of the canon branch, not from the remote.** Branching from `origin/HEAD` is exactly what forces a "push first" — avoid it.

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

Because each chapter is exactly one file owned by one worker, two workers in two worktrees never touch the same canon file — so their branches merge into `main` without conflicts. If a worker thinks the canon must change, that's a **Flag** to the CEO, not an edit.

---

## Step 6 — Push policy

**Push to GitHub is a BACKUP, not a sync requirement.** Local merges (Step 3) already move work between worktrees. So:

- **Default: push at close.** End of session / chapter close, via `save-session`. That's the normal push point.
- **A worker MAY push its branch manually** as a backup on a long or risky chapter — optional, never required for the handoff.
- **The CEO↔worker verify loop never needs a push** — it's all local (Step 8).
- **Whoever can push, pushes.** A host tool (Claude Code / Codex) runs `git push`. In **Cowork**, commit locally and **emit the exact `git push` command** for the user — never claim to have pushed.

Cowork push snippet (emit verbatim, filling in the real branch):

````
✅ Committed locally. Cowork can't push — run this in your terminal to sync:

```bash
git push origin <branch>
```
````

---

## Step 7 — Cowork git setup (run on first git use in a Cowork session)

The first time you touch git in a Cowork session, do this once so git behaves:

1. **Recommend "Act without asking" mode.** Tell the user that switching Cowork to *Act without asking* lets git run its sequence of commands without a prompt on each one.
2. **Ensure delete permission for the project folder.** Cowork blocks file deletes until the user grants delete permission for the folder — and that block **also stops git from managing its lock files**. Ask the user to grant delete permission for the project folder.
3. **Auto-clear any stale lock.** If a previous run left a lock behind, clear it (safe when no git process is running):

   ```bash
   rm -f .git/index.lock
   ```

After these, **git works normally in Cowork** — commit / branch / merge all run locally. The only thing it still cannot do is **push**; commit locally and emit the push command (Step 6).

---

## Step 8 — CEO verify-by-reading

The CEO verifies a worker's finished chapter **locally, with no GitHub** — the worktrees share `.git`, so the worker's branch is already readable:

```bash
git show <branch>:brain/chapters/NN-name.md     # read the Completion Report (the contract)
git diff main..<branch>                          # read the actual code change
```

Read the **report** first (Goal / Status / Changed / Verified / Flags), then the **diff** to confirm it matches. No checkout, no fetch, no push. Find `<branch>` from `git worktree list --porcelain` or ask the user.

After accepting, the CEO merges and (optionally) removes the worktree:

```bash
git merge --no-ff <branch> -m "merge: chapter NN <name> · <stamp>"
git worktree remove <worktree-path>     # add --force only after confirming nothing unmerged
```

---

## Step 9 — Lockfile / dependency rule

**Don't change lockfiles or dependencies in two worktrees at once** — they conflict at merge (lockfiles regenerate divergently and don't auto-merge).

- Do dependency changes (add/remove/upgrade packages, regenerate the lockfile) **on the canon branch**.
- Workers that need a new dependency **Flag it** to the CEO rather than installing it in their worktree.

---

## Quick reference

| Situation | Command / action |
|---|---|
| Which tool / can I push? | env vars (Step 0). Cowork = no push. |
| Pull latest canon into a worktree | `git merge main` — local, offline (Step 3) |
| Name a worker branch | `ch-NN-name` (Step 2) |
| Commit message | `type(scope): summary [ch-NN] · Agent` (Step 1) |
| New worktree, Claude Code | `worktree.baseRef: "head"` + `claude --worktree <name>` (Step 4) |
| New worktree, Codex | "Worktree" thread, select canon branch as base (Step 4) |
| CEO reads a worker's branch | `git show <branch>:…` + `git diff main..<branch>` (Step 8) |
| Cowork git stuck on lock | `rm -f .git/index.lock` + grant delete perm (Step 7) |
| Push | at close (default); Cowork emits the command (Step 6) |

---

## Rules

- The canon is one folder, `brain/`. Workers write code + their own chapter file only; the CEO owns the shared canon.
- Worktrees share one local `.git` — sync between them with a **local merge**, never push-then-pull. GitHub is a backup.
- Cowork commits locally and **never claims to have pushed** — it emits the `git push` command for the user.
- New worktrees must branch from **local HEAD** of the canon branch (`baseRef: head` in Claude Code; select the canon branch in Codex), or you reintroduce "push first."
- Don't touch lockfiles/dependencies in two worktrees at once — do them on the canon branch.
- Every commit carries the author stamp; the final commit carries the Completion Report.
