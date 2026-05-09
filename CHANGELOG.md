# Changelog — project-protocol

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [3.3.2] — 2026-05-09

### Fixed
- Add `.codex-plugin/plugin.json` to plugin archive (Codex was missing metadata, requiring manual post-install patching)
- hooks.json SessionStart: try `CODEX_PLUGIN_ROOT` before `CLAUDE_PLUGIN_ROOT` so Codex gets full `session-start-context.md` instead of fallback mini-message
- build.sh: now includes `.codex-plugin/` in staged zip

## [3.3.1] — 2026-05-09

### Fixed
- session-recap: extend worktree detection to Claude Code (`.claude/worktrees/`) in addition to Codex (`.codex/worktrees/`)
- session-recap: add state path printed for both worktree types so user knows where real files live

## [3.3.0] — 2026-05-08

### Added
- session-recap: pwd + git status checks BEFORE reading WORKLOG/STATUS (mandatory orientation)
- session-recap: Codex worktree detection — warns when running inside a detached worktree
- session-recap: BRIEF.md and docs/AGENT-WORKFLOW.md added to read list

### Fixed
- session-recap: allowed-tools now includes `git:*` and `pwd:*` (required for worktree detection)

## [3.2.1] — 2026-05-08

### Fixed
- plugin.json: description trimmed from 581 → 198 chars (Cowork validation limit ~250 chars)
- plugin.json: reduced keyword count from 10 → 6

## [3.2.0] — 2026-05-08

### Added
- add-context skill: extended context file loop for already-initialized projects
- init-project: Phase 6 extended context file loop
- DESIGN.md: adopted google/design.md spec (YAML frontmatter + 9-section markdown body)
- DESIGN.md: legacy upgrade path included
- DESIGN.md: npx @google/design.md lint step after generation

## [3.1.0] — 2026-04-29

### Added
- docs/INDEX.md generation in init-project (Phases 4a–4f)
- DISCOVERIES.md stub creation
- Pre-task classification (NEW / ADDITION / UI CHANGE / BUG FIX)
- Sub-agent model routing table in init-project

## [3.0.0] — 2026-04-29

### Added
- CHANGELOG.md (Keep a Changelog format)
- docs/INDEX.md (human map + agent dependency index)
- PreCompact hook: echoes WORKLOG.md into compaction context
- Sub-agent routing: Haiku for extraction, Sonnet for judgment

## [2.0.0] — 2026-04-28

### Added
- BRIEF.md (versioned decision log)
- BRAND.md (product identity)
- FUNDAMENTALS.md (global design principles)
- DESIGN.md (project-specific design system)

## [1.0.0] — 2026-04-20

### Added
- Initial plugin: project-protocol, init-project, save-session, session-recap skills
- SessionStart, PreCompact, Stop hooks
- CLAUDE.md, STATUS.md, ROADMAP.md, WORKLOG.md templates
