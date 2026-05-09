# Status — project-protocol plugin
> Last updated: 2026-05-09 · Cowork

## Current Sprint

v3.3.1 shipped. Hardening session: agent-agnostic fixes + canonical project folder + GitHub setup.

## Health

- ✅ Working: all 5 skills functional in Claude Code and Codex
- ✅ Working: plugin validates and installs correctly in Cowork
- ✅ Fixed: session-recap now detects both Codex and Claude Code worktrees
- ✅ Fixed: init-project no longer references Claude-specific model names
- ✅ Fixed: FUNDAMENTALS.md embedded inline (no ${CLAUDE_PLUGIN_ROOT} dependency)
- ✅ Fixed: SessionStart hook has graceful fallback if ${CLAUDE_PLUGIN_ROOT} unset
- 🔒 Blocked: (none)

## Needs CEO Input

(none)

## Recent Sessions (rolling — keep last 5)

- 2026-05-08 · Cowork: debug plugin validation failure → root cause plugin.json description length → shipped v3.2.1
- 2026-05-08 · Cowork: session-recap worktree detection → added git+pwd to allowed-tools → shipped v3.3.0
- 2026-05-08 · Cowork: extend worktree detection to Claude Code (.claude/worktrees/) → shipped v3.3.1
- 2026-05-09 · Cowork: agent-agnostic fixes + canonical project folder + GitHub setup

## Next Actions

1. Push to GitHub (commands provided at end of session)
2. Clean up old .plugin files from ~/Arel OS/ root
3. Verify plugin installs correctly from new build
