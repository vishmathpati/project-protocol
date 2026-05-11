# Changelog

All notable changes to project-protocol are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]

## [1.0.0] — 2026-05-11

Initial public release. Clean v1.0.0 baseline.

### Skills (10)

**Session lifecycle:**
- `init-project` — bootstrap or audit a project with the standard three-folder layout.
- `save-session` — close a session: WORKLOG → CHANGELOG, update STATUS, clear WORKLOG (tier-aware).
- `session-recap` — mid-session snapshot of what's been done and what's still open.
- `add-context` — add extended context files (data contracts, domain reference, integrations).
- `project-protocol` — reference document defining the file set + session discipline.

**Discipline (new):**
- `discipline` — pre-action gate: pause, declare, cascade, verify, confirm.
- `verify-by-reading` — read-before-answer enforcement.
- `audit-before-close` — spec-vs-implementation check before marking work done.
- `discussion-mode` — read-only conversation mode when user signals thinking.
- `audit` — cross-file consistency check across canon.

### Hooks (8)

- `SessionStart` — inject required reading.
- `UserPromptSubmit` — pre-task classification reminder.
- `PreToolUse` (Edit|Write filter) — WORKLOG-cleared warning.
- `PreCompact` — back up WORKLOG before context compaction.
- `PostCompact` — re-orient context after compaction.
- `SubagentStart` / `SubagentStop` — log sub-agent invocations to WORKLOG.
- `Stop` — warn if WORKLOG has unsaved lines.

### Project layout

`init-project` creates a three-folder structure in target projects:

- Root `CLAUDE.md` (rules + folder map) + root `README.md` (file-and-dependency map).
- `cowork/` — orchestration tier (Cowork's files).
- `agents/` — project canon tier (Codex / Claude Code read here).
- `human/` — human-facing tier (daily steering file at `agenda.md`).

### Compatibility

- Skills follow [agentskills.io](https://agentskills.io) core spec — portable across Claude Code, Codex, Gemini CLI, Cursor, and other tools that adopt the standard.
- Every skill ships with a Codex `agents/openai.yaml` sidecar for polished Codex UX.
- Dual manifest: `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json`.
- Worktree detection in `session-recap` covers both Codex and Claude Code worktree paths.
