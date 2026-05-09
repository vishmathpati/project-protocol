# project-protocol

A plugin for Claude Code and Codex that gives every project a consistent session discipline — so your AI agent always knows where things stand, logs its work in real time, and hands off cleanly when a session ends.

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
brew tap vishmathpati/project-protocol
brew install project-protocol
```

### Manual

Download the latest `.plugin` file from [Releases](https://github.com/vishmathpati/project-protocol/releases), then:

```bash
# Claude Code
claude plugin install ~/Downloads/project-protocol-vX.Y.Z.plugin

# Cowork (Claude desktop)
# Drag the .plugin file into the Cowork chat window
```

---

## What it does

Once installed, every coding session on any project gets three things automatically:

1. **Session start** — the agent is reminded to read `CLAUDE.md` and `STATUS.md` before touching any code
2. **Live work log** — every change, decision, and failed attempt gets appended to `WORKLOG.md` in real time
3. **Clean session close** — `save-session` writes the handoff: updates `STATUS.md`, appends to `CHANGELOG.md`, clears the worklog

The agent never loses context between sessions. You never have to re-explain what's happening.

---

## Skills

### `init-project`
Bootstrap any project — new or existing. Scans all markdown files, asks what to do with each, and creates a unified set of protocol files. Also generates `docs/INDEX.md` from live codebase analysis.

**Say:** *"init project"* or *"set up protocol files"*

Creates these files in your project:

```
your-project/
├── CLAUDE.md          ← project identity, stack, guardrails, coding rules
├── STATUS.md          ← current health, blockers, next actions
├── ROADMAP.md         ← direction and phases
├── WORKLOG.md         ← real-time session log (cleared by save-session)
├── CHANGELOG.md       ← version history (Keep a Changelog format)
├── BRIEF.md           ← versioned decision log from planning sessions
├── BRAND.md           ← product identity (auto-detected from codebase)
├── FUNDAMENTALS.md    ← design principles reference
├── DESIGN.md          ← project design system (google/design.md spec)
└── docs/
    ├── INDEX.md       ← human map + agent dependency index
    └── detail/        ← deep-dive docs for complex features
```

### `save-session`
Close a session properly. Reads the worklog, appends to `CHANGELOG.md`, updates `STATUS.md`, signs `BRIEF.md` if decisions were made, and clears the worklog.

**Say:** *"save session"*, *"close session"*, *"done for today"*

### `session-recap`
Mid-session orientation. Checks your current directory and git state (including worktree detection), reads `WORKLOG.md` and `STATUS.md`, and prints a crisp snapshot of what's been done and what's still open.

**Say:** *"recap"*, *"where are we"*, *"catch me up"*

### `add-context`
Add a deep-reference document to an already-initialized project — data contracts, domain knowledge, architecture docs, integration specs. Auto cross-references in `CLAUDE.md` and `docs/INDEX.md`.

**Say:** *"add context"*, *"add a data contracts file"*, *"add domain reference"*

---

## Why it works

Most AI agent sessions start cold — the agent has no memory of what was decided, what broke, or what was tried last time. This plugin solves that by keeping the context in plain markdown files the agent reads at the start of every session.

`WORKLOG.md` is the key: every response that changes something appends one line. By the time a session ends, there's a full real-time audit trail. `save-session` distills that into `CHANGELOG.md` and `STATUS.md` for the next session to start from.

---

## Compatibility

Works with Claude Code and Codex. Designed to be agent-agnostic:

- No hardcoded model names
- `FUNDAMENTALS.md` content is embedded inline — no plugin path dependencies
- SessionStart hook degrades gracefully if the host agent doesn't support `${CLAUDE_PLUGIN_ROOT}`
- `session-recap` detects both Codex worktrees (`.codex/worktrees/`) and Claude Code worktrees (`.claude/worktrees/`) and warns when running in a detached context

**Codex one-time setup:** Add this to `~/.codex/config.toml` to make Codex read `CLAUDE.md` automatically:
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

Outputs `project-protocol-vX.Y.Z.plugin` in the `dist/` folder.

To release a new version: bump `version` in `.claude-plugin/plugin.json`, then run `./build.sh`.

---

## License

MIT

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
