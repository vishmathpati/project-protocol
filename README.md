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

16 skills + 9 hook events that turn every AI coding session into a disciplined operation. As of v2.5.0, the plugin is built on a three-layer architecture: **Rules** (root `CLAUDE.md` is the always-loaded brain — skill index, hooks index, situation router, non-negotiable rules), **Enforcement** (hooks fire deterministically on tool events), **Workflow** (skills are invokable, with explicit `Skill()` calls between them — no more description-match guessing).

### Session lifecycle (the core 4)

- **`init-project`** — Bootstrap or audit a project. Creates the standard three-folder layout (`cowork/`, `agents/`, `human/`).
- **`save-session`** — Close cleanly: WORKLOG → CHANGELOG, update STATUS, clear WORKLOG. Tier-aware.
- **`session-recap`** — Mid-session snapshot: what's been done, what's still open.
- **`add-context`** — Add extended context files (data contracts, domain reference, integrations).

### Discipline skills

Auto-fire on description match, also invokable via slash command.

- **`discipline`** — Pre-action gate: pause, declare files-to-change, cascade-effects, verify canon, confirm, then act.
- **`verify-by-reading`** — Open the file before answering questions about it. Catches memory drift.
- **`audit-before-close`** — Spec-vs-implementation check before any chapter or task is marked done.
- **`discussion-mode`** — Read-only mode when the user signals thinking ("discuss", "let's talk", "what do you think").
- **`audit`** — Cross-file consistency check across canon. Reports drift, does not auto-fix. v1.3 adds a design-system raw-value / cardinal-sin scan.
- **`design-check`** *(new in v1.3)* — UI-work gate. Reads `DESIGN.md` + `FUNDAMENTALS.md`, searches `components/` for reuse, halts on missing tokens, scans the diff for raw hex / px / font values. Fires on any visual change. *v2.0 adds Step 8: auto-fix for mechanical violations (raw hex matching tokens, missing dimensions, ellipsis, nbsp, etc.) with user confirmation. Human-judgment violations (indigo accent, banned words, invented metrics) are still surfaced for user input only.*
- **`edit-plugin`** *(new in v1.4; v2.5.0 adds Step 5 manifest discipline — version bumps must ship with a `migrations/vX.Y.Z.md` file)* — Self-discipline gate for changes to this plugin's own source (skills, hooks, manifests, README). Chains commit + push to every edit so changes always reach `origin/main` on GitHub.
- **`migrate-project`** *(new in v2.5.0)* — Apply version-by-version plugin migration deltas to bring an existing project up to the current plugin version. Driven by per-release manifests under `migrations/`. Refuses to run in Cowork (Cowork can't `git push`); user runs it from Claude Code or terminal. Triggered automatically by the SessionStart drift-detector hook when project's recorded plugin version is behind the installed plugin.
- **`design-direction`** *(new in v1.5)* — Deep brand-direction diagnostic. Takes a raw brand dump, silently extracts 9 taste axes (trust, frequency, density, culture, archetype, tribe, surface, tempo, refusals), proposes 3 named directions with a moodboard, and writes a rich `BRAND.md` + `DESIGN.md` Overview + brand-specific refusal list. Sits one layer upstream of `init-project` Phase 4 — or runs standalone on already-initiated projects to re-anchor brand.
- **`build-component`** *(new in v2.0)* — Per-component build skill. Reads `agents/STRUCTURE.md` and the relevant canon, scans for reusable existing components, proposes a strategy (compose existing primitives, extend, or build new primitive), generates the component, then fires `design-check`. Tier-aware (Generic / Marketing / App), surface-aware (hides Marketing tier on dashboard-only projects), supports adopt-external and recreate-from-inspiration sub-modes.
- **`marketing-brief`** *(new in v2.0)* — One-time deep marketing-site brief. Reads existing canon, builds an `agents/marketing/CONTENT.md` content registry (FEATURES, AUDIENCES, COMPARISONS, TESTIMONIALS, FAQS, LEGAL_PAGES), proposes a sitemap, writes per-page briefs, copy, media manifest, and layout sketches. Auto-skips on dashboard-only / internal-tool projects.
- **`build-page`** *(new in v2.2, redesigned in v2.3)* — Compositional sibling to `build-component`. For whole pages (marketing or dashboard), not atomic components. Long iterative conversation: asks which page, reads the brief and canon, surfaces an analysis, proposes a starting plan, then iterates with the user — section by section — accepting external references (Stripe / Aceternity / shadcn URLs, pasted code, screenshots) and cross-checking them against `DESIGN.md` + `BRAND.md` before adoption. Calls `build-component` inline as a subroutine for every net-new primitive, so each component gets its own focused conversation instead of one 400-line page-wide code drop. Writes the actual page file directly when the conversation gets there. Copy is inlined verbatim from `agents/marketing/copy/<slug>.md` — no intermediate `marketing-content.ts` or runtime mirror file ever created. Marketing pages enforce RSC + `generateMetadata` for SEO. Follows the same protocols as every other skill (WORKLOG entries on decisions, BRIEF appends on locks, INDEX update on new routes); no state files, no scratch folders, no special mode machinery.

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
│   │   TOOLING.md (Node only), DESIGN.md, STRUCTURE.md, DISCOVERIES.md,
│   │   WORKLOG.md, CHANGELOG.md
│   ├── marketing/         ← CONTENT.md, SITEMAP.md, briefs/, copy/, MEDIA.md, layouts/
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

**Handoff between agents.** Cowork seeds the project with the always-loaded files (`CLAUDE.md`, `BRAND.md`, the first `BRIEF.md` version block signed `· Cowork`). Claude Code / Codex bootstrap the rest of the canon (`STATUS.md`, `ROADMAP.md`, `FUNDAMENTALS.md`, `DESIGN.md`, `DISCOVERIES.md`, `docs/INDEX.md`, worklogs, changelogs) via `init-project` on the first coding session. When the project returns to Cowork mid-flight, Cowork re-reads the canon, then appends a new `BRIEF.md` version block signed `· Cowork` before handing back. **One agent at a time** — either Claude Code or Codex is active on a project, never both simultaneously. Every significant write to BRIEF / STATUS / DISCOVERIES / CHANGELOG carries an agent label (`· Cowork` / `· Claude Code` / `· Codex`) so the next agent can see who decided what.

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
