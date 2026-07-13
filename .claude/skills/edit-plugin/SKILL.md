---
name: edit-plugin
description: Mandatory workshop overlay for changing Project Protocol source. Uses the active role and chapter, keeps private development canon outside the public repository, verifies source changes, and separates implementation from release.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*,python3:*,ls:*,cat:*,date:*,wc:*)
---

# Edit Plugin — Project Protocol Dogfooding Gate

Use Project Protocol to build Project Protocol. This workshop-only skill adds
source-repository safety; it does not replace CEO, worker, solo, chapters,
Recap, Save Session, Completion Check, or the Git skill.

## Governing model

There are two independent stores:

1. **Public source repository** — shipped skills, hooks, templates, migrations,
   tests, manifests, README, and public CHANGELOG.
2. **Private development canon** — CLAUDE, brain, agenda, chapters, WORKLOG,
   internal decisions, reports, and dashboard. It lives in a separate local Git
   repository and is attached through the private-canon resolver.

Never stage private canon in the public source repository. Never treat the
public CHANGELOG as the private project's session history.

## When this fires

Invoke for any change to the Project Protocol source repository, including:

- `skills/`, `hooks/`, `templates/`, `migrations/`, `tests/`, `scripts/`
- `.claude-plugin/`, `.codex-plugin/`, `.claude/skills/edit-plugin/`
- public `README.md` or `CHANGELOG.md`

It does not fire for a consumer project such as Singh Empire.

## 1. Confirm both locations

Before editing, verify:

```bash
git rev-parse --show-toplevel
git status --short --branch
git worktree list --porcelain
python3 hooks/scripts/private_canon.py status --repo "$PWD"
```

The source root must be the Project Protocol source repository. Never edit a
marketplace cache, installed plugin copy, or generated package.

Private canon must resolve outside the source root. If it is absent, stop and
register the private canon before continuing. If `brain` or `CLAUDE.md` is a
conflicting real path, do not overwrite it.

## 2. Enter through the normal session model

The human invokes CEO, worker, or solo. Run Recap and read:

- private `CLAUDE.md`
- private `brain/STATUS.md` and useful WORKLOG tail
- the active private chapter
- only the additional canon relevant to the chapter

Do not create an uncontracted feature because the source request sounds small.
Truly trivial maintenance may use the solo trivial-work rule.

## 3. Respect authority

- **CEO** owns planning, approval, source integration, and shared private canon.
- **Worker** changes chapter-required source in an isolated source worktree and
  appends evidence to the assigned private chapter. Worker output remains a
  proposal until CEO approval.
- **Solo** may plan and implement in one session, while still recording the
  contract and evidence for non-trivial work.

Private canon is shared operational state for this public repository. Workers
may read it but must not rewrite shared BRIEF, STATUS, agenda, or WONT-DO;
proposed durable changes belong in the chapter report for CEO reconciliation.

## 4. Read source before editing

Read every source file being changed. For a shipped skill, also read its
`agents/openai.yaml`. Follow references only when needed to understand the
contract. Check current tests and validation scripts before inventing a new
verification method.

## 5. Make one chapter-scoped change

- Preserve unrelated dirty files.
- Keep Claude Code and Codex behavior aligned.
- New or renamed shipped skills require matching `agents/openai.yaml` metadata.
- Update README only when public behavior or contributor instructions changed.
- Update public CHANGELOG under Unreleased for user-visible behavior.
- Do not edit installed copies to test a source fix.

## 6. Verify proportionally

Run the narrow tests for the changed contract, then the structural audit. For a
release candidate, run the full release verification bundle from the active
chapter. Record commands and exact results in the private chapter report.

Minimum structural check:

```bash
python3 scripts/validate_plugin.py
```

## 7. Keep implementation separate from release

A source edit does **not** automatically authorize a version bump, marketplace
release, merge to main, or push of main.

Only an explicit, human-approved release chapter may change versions. When it
does, the same release series must include:

- aligned `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and
  `.claude-plugin/marketplace.json`
- `migrations/vX.Y.Z.md`, including a no-project-deltas declaration when true
- public CHANGELOG entry
- release audit evidence

Use `scripts/bump-version.sh` for an approved release. Never bump merely because
user-facing behavior changed during development.

## 8. Commit the two stores independently

### Public source repository

Stage explicit source files only. Commit with a structured message:

```text
plugin(<area>): <short summary>
```

Push the feature branch when Save Session or the human requests a durable
remote checkpoint. CEO approval controls integration into main.

### Private development canon repository

Commit chapter reports, STATUS, agenda, WORKLOG folding, and durable decisions
in the private canon repository. Do not add a public remote unless the human
explicitly chooses a private backup destination. A local private commit is a
valid persistence checkpoint; it is not a public release.

Never run `git add brain` or `git add CLAUDE.md` in the public source repo.

## 9. Close through Project Protocol

Run Completion Check against the chapter. Then Save Session folds recovery
state, commits the correct owner files in the correct repository, and reports:

- public source branch, commit, push, and integration state
- private canon commit state, without exposing private contents
- tests and validation evidence
- release state separately from implementation state

## Strict rules

- Source repo and private canon repo are never staged together.
- No automatic version bump.
- No automatic merge or release.
- No editing installed copies.
- No claim that GitHub contains private canon.
- No claim that implementation is released merely because a branch was pushed.
- No source edit without live Git, current source, active role, and chapter
  context.
