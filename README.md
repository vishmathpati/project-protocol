# project-protocol

A plugin for Claude Code and Codex (and any tool that supports the [agentskills.io](https://agentskills.io) standard) that gives every project a consistent session discipline — so your AI agent always knows where things stand, logs its work in real time, audits before closing, and hands off cleanly when a session ends.

Install once. Every project gets a shared system that works the same way no matter which agent you're using.

---

## Install

### One command (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/vishmathpati/project-protocol/main/install.sh | bash
```

Downloads the latest release and installs it directly into Claude Code.

### Homebrew

```bash
brew install --cask vishmathpati/project-protocol/project-protocol
```

### Manual

Download the latest `.zip` file from [Releases](https://github.com/vishmathpati/project-protocol/releases), then:

```bash
# Claude Code
claude plugin install ~/Downloads/project-protocol-vX.Y.Z.zip

# Cowork (Claude desktop)
# Drag the .zip file into the Cowork chat window
```

---

## What you get

12 skills + 8 hooks that turn every AI coding session into a disciplined operation.

### Session lifecycle (the core 5)

- **`init-project`** — Bootstrap or audit a project. Creates the standard three-folder layout (`cowork/`, `agents/`, `human/`).
- **`save-session`** — Close cleanly: WORKLOG → CHANGELOG, update STATUS, clear WORKLOG. Tier-aware.
- **`session-recap`** — Mid-session snapshot: what's been done, what's still open.
- **`add-context`** — Add extended context files (data contracts, domain reference, integrations).
- **`project-protocol`** — Reference document defining the file set + session discipline.

### Discipline skills

Auto-fire on description match, also invokable via slash command.

- **`discipline`** — Pre-action gate: pause, declare files-to-change, cascade-effects, verify canon, confirm, then act.
- **`verify-by-reading`** — Open the file before answering questions about it. Catches memory drift.
- **`audit-before-close`** — Spec-vs-implementation check before any chapter or task is marked done.
- **`discussion-mode`** — Read-only mode when the user signals thinking ("discuss", "let's talk", "what do you think").
- **`audit`** — Cross-file consistency check across canon. Reports drift, does not auto-fix. v1.3 adds a design-system raw-value / cardinal-sin scan.
- **`design-check`** *(new in v1.3)* — UI-work gate. Reads `DESIGN.md` + `FUNDAMENTALS.md`, searches `components/` for reuse, halts on missing tokens, scans the diff for raw hex / px / font values. Fires on any visual change.
- **`edit-plugin`** *(new in v1.4)* — Self-discipline gate for changes to this plugin's own source (skills, hooks, manifests, README). Chains commit + push to every edit so changes always reach `origin/main` on GitHub.

### Hooks (8 total)

| Hook | What it does |
|---|---|
| `SessionStart` | Inject required reading context |
| `UserPromptSubmit` | Pre-task classification reminder |
| `PreToolUse` (Edit\|Write) | Warn if WORKLOG is in cleared state |
| `PreCompact` | Back up WORKLOG before context compaction |
| `PostCompact` | Re-orient context after compaction |
| `SubagentStart` / `SubagentStop` | Log sub-agent invocations to WORKLOG |
| `Stop` | Warn if WORKLOG has unsaved lines |

---

## Project layout

When `init-project` runs, it creates this structure in your project:

```
project-root/
├── CLAUDE.md              ← rules + folder map (always loaded)
├── README.md              ← file-and-dependency map
├── cowork/                ← orchestration tier
│   └── CLAUDE.md, STATUS.md, BRIEF.md, WORKLOG.md, CHANGELOG.md
├── agents/                ← project canon tier (Codex / Claude Code read here)
│   ├── STATUS.md, BRIEF.md, ROADMAP.md, BRAND.md, FUNDAMENTALS.md,
│   │   TOOLING.md (Node only), DESIGN.md, DISCOVERIES.md, WORKLOG.md, CHANGELOG.md
│   └── docs/
│       ├── INDEX.md
│       └── detail/
└── human/
    └── agenda.md          ← daily steering file
```

Each tier serves one audience. The root `CLAUDE.md` is the brain — non-negotiable rules + a map of where everything lives. The root `README.md` is the file-and-dependency map you consult before any non-trivial edit.

---

## Why it works

AI agents forget everything between sessions. This plugin fixes that by keeping all context in plain markdown files the agent reads at session start.

`WORKLOG.md` is the discipline engine: every response that changes something appends one line. By session end, you have a full real-time audit trail. `save-session` distills it into `CHANGELOG.md` and `STATUS.md` so the next session starts from solid ground.

The **discipline skills** add a second layer: gates that fire automatically when their description matches the conversation. They force the agent to verify before acting, read before answering, and audit before closing — the patterns that fail in untrained agent sessions.

---

## Compatibility

Works with Claude Code, Codex CLI, and any tool that supports the [agentskills.io](https://agentskills.io) skill standard.

- No hardcoded model names.
- Every skill ships with both a Claude Code `SKILL.md` and a Codex `agents/openai.yaml` sidecar.
- Dual manifest: `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json`.
- Worktree detection in `session-recap` for both Codex (`.codex/worktrees/`) and Claude Code (`.claude/worktrees/`).
- SessionStart hook degrades gracefully if the host doesn't expose `${CLAUDE_PLUGIN_ROOT}` or `${CODEX_PLUGIN_ROOT}`.

**Codex one-time setup:** add this to `~/.codex/config.toml` so Codex reads `CLAUDE.md` automatically:

```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

---

## Build from source

```bash
git clone https://github.com/vishmathpati/project-protocol
cd project-protocol
./build.sh
```

Outputs `project-protocol-vX.Y.Z.zip` in the `dist/` folder.

To release: bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, then run `./build.sh`.

---

## License

MIT

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
