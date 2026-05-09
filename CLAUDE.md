# CLAUDE.md — project-protocol plugin

## Coding Standards

**1. Think Before Coding** — Don't assume. Don't hide confusion. Surface tradeoffs.
**2. Simplicity First** — Minimum code that solves the problem. Nothing speculative.
**3. Surgical Changes** — Touch only what you must. Match existing style.
**4. Verify Before Closing** — Define what "done" looks like before touching code.

---

## What this is

A plugin for Claude Code and Codex that enforces a standard project protocol. Five skills: `project-protocol` (session discipline), `init-project` (bootstrap), `save-session` (close), `session-recap` (mid-session orientation), `add-context` (extended docs). One hooks file: `hooks.json` (SessionStart, PreCompact, Stop).

## Stack

No code. Pure markdown skill files + JSON hooks. Packaged as a `.plugin` zip.

## Plugin structure

```
.claude-plugin/plugin.json   ← manifest (name, version, description, keywords)
skills/<name>/SKILL.md       ← one file per skill (YAML frontmatter + markdown instructions)
hooks/hooks.json             ← SessionStart, PreCompact, Stop hooks
hooks/session-start-context.md ← content injected by SessionStart hook
templates/FUNDAMENTALS.md    ← design principles (copied to projects by init-project)
```

## What NOT to do

- Never add agent-specific model names (no `claude-haiku-*`, `claude-sonnet-*`, `codex-*` etc.)
- Never use `${CLAUDE_PLUGIN_ROOT}` paths as the only access method — always provide inline fallback
- Never make skills Claude-only — they must work in Codex too
- plugin.json description must stay under 250 chars

## Build

```bash
./build.sh
```

Outputs `~/Arel OS/project-protocol-vX.Y.Z.plugin`. Drag into Cowork or run `claude plugin install` in any project.

## Session rules

- Read STATUS.md before doing anything.
- After every response with a change: append one line to WORKLOG.md.
- Run save-session before closing.
