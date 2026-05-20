---
name: edit-plugin
description: Mandatory discipline gate when editing this plugin's own source (skills, hooks, commands, manifest, templates, README, build scripts). Forces edit → commit → push → verify on every change. Triggers — "edit the plugin", "update the X skill", "change the X hook", "modify the protocol", "fix the plugin", "edit save-session", or any change to files under skills/, hooks/, commands/, templates/, .claude-plugin/, .codex-plugin/.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*,ls:*,cat:*,date:*,wc:*)
---

# Edit Plugin — Self-Discipline for project-protocol

This skill fires whenever an agent (Cowork, Claude Code, Codex) edits the **project-protocol plugin's own source code** — skills, hooks, commands, manifests, templates, build scripts, README, CHANGELOG.

The problem it solves: an agent edits a skill, the user thanks them, the session moves on — but the change was never committed or pushed. The next time the user pulls from GitHub or reinstalls the plugin, the change is gone. This skill makes that impossible by chaining commit + push to every edit.

---

## When this fires

- User asks to edit, update, fix, or change anything in this plugin: a skill, hook, command, template, manifest, README, build script, CHANGELOG.
- About to call `Edit` or `Write` on any file under:
  - `skills/<name>/SKILL.md` or `skills/<name>/agents/openai.yaml` or `skills/<name>/references/`
  - `hooks/hooks.json` or any `hooks/*.md`
  - `commands/*` (if/when added)
  - `templates/*.md`
  - `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`
  - `README.md`, `CHANGELOG.md`, `build.sh`, `install.sh`
- Slash command: `/edit-plugin`

**Does NOT fire for:** edits to *projects that use this plugin* (their `cowork/`, `agents/`, `human/` files). That work uses `save-session` for its git hygiene. This skill is only for changes to the plugin source itself.

---

## The 7 steps

### 1. Confirm location

Verify the file you're about to touch lives in the plugin source repo, not in a dist copy or installed copy.

```bash
git -C "<file's parent dir>" rev-parse --show-toplevel
```

The output must be the project-protocol repo root. If the path contains `dist/` or `/rpm/plugin_` or any other installed-copy location: **STOP**. Tell the user — "That's a build artifact / installed copy. The source is at `<source path>`. Edit there instead."

### 2. Read before edit

Always `Read` the current file before changing it. No edits from memory. If touching `SKILL.md`, also read the sibling `agents/openai.yaml` (Codex sidecar) — many changes need to be mirrored there.

### 3. Make the edit

Use `Edit` (preferred) or `Write` (for new files). Match the conventions of the surrounding files:

- SKILL.md frontmatter: `name`, `description`, `allowed-tools` (comma-separated, Bash with explicit subcommand allowlist)
- Codex sidecar at `skills/<name>/agents/openai.yaml` if the skill is meant to work in Codex too
- New skill ⇒ create both `SKILL.md` and `agents/openai.yaml`
- README's skill count and skill list must be kept in sync if you add/remove a skill

### 4. Check `git status` and stage

```bash
cd <repo-root>
git status --porcelain
```

Stage every file you actually changed. Do not bulk-add. Do not stage unrelated dirty files left over from prior work — show them to the user and ask first.

```bash
git add <each file you edited>
```

### 5. Commit with a structured message

```bash
git commit -m "plugin(<area>): <short summary>

<optional body explaining why or what cascades>"
```

`<area>` is one of:
- `skill:<skill-name>` — e.g. `skill:save-session`
- `hook` — for `hooks/`
- `template:<name>` — e.g. `template:DESIGN`
- `manifest` — for plugin.json edits
- `build` — for build.sh / install.sh
- `docs` — for README / CHANGELOG

If the edit changes user-facing behavior of an installed skill, also bump the version in **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` and add a `### Changed` / `### Added` / `### Fixed` line to `CHANGELOG.md` under `## [Unreleased]`. The plugin version + changelog edits go into the **same commit** as the source change.

### 6. Push to GitHub

```bash
git push origin <current-branch>
```

If the current branch is not `main` (you're on a worktree branch): push the branch, then follow `save-session` Step 10d to fast-forward / merge into `main`. The plugin's source-of-truth is `origin/main` on GitHub.

If push fails (auth, non-fast-forward, network): **STOP** and report the exact error. Do not leave the user thinking the change shipped when it didn't.

### 7. Report + activation instructions

Confirm to the user with this template:

```
✅ Edited: <file(s)>
✅ Committed: <SHA> — <commit subject>
✅ Pushed: origin/<branch> (and merged to main if applicable)
✅ GitHub now has the change.

To activate locally:
  • Hot-copy (no version bump): copy <file> to the installed plugin path
    ~/Library/Application Support/Claude/.../rpm/plugin_<id>/skills/<name>/
    and restart the session.
  • Clean install (with version bump): run ./build.sh, then reinstall the new .zip
    from dist/ via Cowork or `claude plugin install`.
```

If the change was a version bump → recommend the clean install path.
If it was a fix or tweak between releases → hot-copy is fine.

---

## Strict rules

- **Never edit `dist/` directly.** It's generated. Edit source, then run `./build.sh` if you want a packaged build.
- **Never edit the installed copy** at `~/Library/Application Support/Claude/.../rpm/plugin_*`. That's the runtime copy; it gets clobbered on reinstall.
- **One logical change = one commit.** Don't bundle a save-session fix + a new skill + a README rewrite into one commit. Multiple commits, each pushed, each verifiable.
- **No silent skips.** If you decided not to commit (because the edit was reverted, or it's only a scratch), say so explicitly: "Not committing — this was an exploratory edit and I'm reverting it."
- **Codex parity.** If you add or rename a skill, you must create/rename the matching `agents/openai.yaml` sidecar in the same commit, or the plugin breaks for Codex users.
- **README skill count stays in sync** with the actual number of skill directories. If you add a skill, update the count in README.md (and in `.claude-plugin/plugin.json` description if it mentions a count).

---

## Why this exists

When an agent edits the plugin and forgets to commit, the work *looks done* on the user's screen (the file changed locally) but it doesn't propagate to GitHub. Future installs, future worktrees, and any teammate pulling the repo see the *old* version. The bug is invisible until something breaks downstream.

The plugin is the discipline mechanism for every other project. The plugin itself needs the same discipline applied to it.

---

## Difference from `save-session`

`save-session` syncs **a project that uses this plugin** — its `cowork/agents/human` markdown files. `edit-plugin` syncs **changes to this plugin itself**. The user's local folder for project-protocol is the plugin source repo, and it must always match `origin/main` on GitHub.
