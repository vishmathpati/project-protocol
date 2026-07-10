# project-protocol

A plugin for Claude Code and Codex (and any tool that supports the [agentskills.io](https://agentskills.io) standard) that gives every project a consistent session discipline — so your AI agent always knows where things stand, logs its work in real time, audits before closing, and hands off cleanly when a session ends.

Install once. Every project gets a shared system that works the same way no matter which agent you're using.

---

## Install & updates

The repo ships its own plugin marketplace (`.claude-plugin/marketplace.json`), so the marketplace is the primary install path on every tool. The built `.zip` in `dist/` is the manual fallback.

### Claude Code (recommended)

Add this repo as a marketplace, then install the plugin from it:

```bash
/plugin marketplace add vishmathpati/project-protocol
/plugin install project-protocol@project-protocol
```

The first command registers the catalog (the `owner/repo` shorthand clones the repo over git, which is what makes the same-repo relative `source` resolve). The second installs the plugin; the name is `project-protocol@project-protocol` (plugin name `@` marketplace name).

**Updates.** Claude Code refreshes marketplaces and bumps installed plugins at startup when auto-update is on for the marketplace — enable it under `/plugin` → **Marketplaces** → select `project-protocol` → **Enable auto-update**. After an update you'll be prompted to run `/reload-plugins`. To pull a refresh by hand: `/plugin marketplace update project-protocol`.

How a new version is detected: Claude Code resolves the plugin version from `version` in `plugin.json` first, then the marketplace entry, then the git commit SHA. This plugin sets `version` in `.claude-plugin/plugin.json`, so existing installs see a new version when that field is bumped on a release. (If the `version` field were omitted, every new commit on the default branch would count as a new version instead.)

### Cowork (Claude desktop)

**Team / Enterprise org.** Connect this repo as a GitHub-synced org marketplace in admin settings and turn on "sync automatically." Members then receive updates on their next session after a PR merges to the default branch. Org sync requires the repo to be **private** and the marketplace plugin `source` entries to be **relative paths within the repo** — this plugin's entry uses `"source": "./"`, which satisfies that.

**Personal (no org features).** Either add the marketplace from the repository (same flow as Claude Code), or drag the built zip `dist/project-protocol-vX.Y.Z.zip` into the Cowork chat window. The zip is the manual fallback — re-drag the newer zip to update.

### Codex

Install via the co-located Codex manifest at `.codex-plugin/plugin.json`. Codex updates are manual — restart or re-sync after pulling a newer version. See [Compatibility](#compatibility) for the one-time `~/.codex/config.toml` setup that lets Codex read `CLAUDE.md` automatically.

### Manual zip fallback (any tool)

Download the latest `.zip` from [Releases](https://github.com/vishmathpati/project-protocol/releases), or build it yourself (see [Build from source](#build-from-source)), then:

```bash
# Claude Code
claude plugin install ~/Downloads/project-protocol-vX.Y.Z.zip

# Cowork (Claude desktop) — drag the .zip into the chat window
```

---

## What you get

27 skills + hook events that turn every AI coding session into a disciplined operation. As of v3.0.0, all project context lives in a single `brain/` folder. The root `CLAUDE.md` is the always-loaded brain — skill index, hooks index, situation router, non-negotiable rules. Hooks fire deterministically on tool events. Skills are invokable via explicit `Skill()` calls — no description-match guessing.

### Role model (new in v3.0.0)

Work is organized around three roles:

- **CEO** — plans the work, breaks it into chapters, reviews and merges completed work.
- **Worker** — picks up one chapter, executes it in a git worktree, writes a Completion Report, then calls `handoff`.
- **Solo** — single-agent mode for smaller tasks that don't need the CEO/worker split.

Invoke a role with `/ceo`, `/worker`, or `/solo` at the start of a session. The CEO defines chapters in `brain/chapters/`. Each chapter is a scoped unit of work executed by a worker in an isolated git worktree; the CEO verifies the Completion Report and merges. The `handoff` skill (model-invoked) signals the end of a worker session and packages the report for CEO review.

### Session lifecycle (the core 4)

- **`init-project`** — Bootstrap or audit a project. Creates the `brain/` layout and root `CLAUDE.md`.
- **`save-session`** — Close cleanly: WORKLOG → CHANGELOG, update STATUS, clear WORKLOG.
- **`session-recap`** — Mid-session snapshot: what's been done, what's still open.
- **`add-context`** — Add extended context files (data contracts, domain reference, integrations).

### Role skills (new in v3.0.0)

- **`ceo`** — CEO mode: plan chapters, review Completion Reports, merge worker branches.
- **`worker`** — Worker mode: claim a chapter, execute in a git worktree, write a Completion Report.
- **`solo`** — Solo mode: single-agent execution without the CEO/worker split.
- **`handoff`** *(model-invoked)* — Worker session teardown: write Completion Report, clean worktree state, signal to CEO.
- **`git`** — Git operations gate. Validates branch state, enforces commit message discipline, guards against unintended force-pushes.
- **`grill`** — Adversarial review: stress-tests a plan, implementation, or decision before it ships.
- **`bug-fixing`** — Structured bug investigation: reproduce → isolate → fix → verify, with WORKLOG entries at each step.
- **`migrate-to-brain`** *(temporary)* — One-time structural migration from the old three-folder layout (`cowork/`, `agents/`, `human/`) to `brain/`. Merges duplicates, confirms before writing, removes `agents/.session-type`.

### Discipline skills

Auto-fire on description match, also invokable via slash command.

- **`discipline`** — Pre-action gate: pause, declare files-to-change, cascade-effects, verify canon, confirm, then act.
- **`verify-by-reading`** — Open the file before answering questions about it. Catches memory drift.
- **`audit-before-close`** — Spec-vs-implementation check before any chapter or task is marked done.
- **`discussion-mode`** — Read-only mode when the user signals thinking ("discuss", "let's talk", "what do you think").
- **`audit`** — Cross-file consistency check across canon. Reports drift, does not auto-fix.
- **`design-check`** — UI-work gate. Reads `DESIGN.md` + `FUNDAMENTALS.md`, searches `components/` for reuse, halts on missing tokens, scans the diff for raw hex / px / font values. Step 8 auto-fixes mechanical violations (raw hex matching tokens, missing dimensions, ellipsis, nbsp, etc.) with user confirmation. Human-judgment violations are surfaced for user input only.
- **`edit-plugin`** — Self-discipline gate for changes to this plugin's own source (skills, hooks, manifests, README). Chains commit + push to every edit. Version bumps must ship with a `migrations/vX.Y.Z.md` file (Step 5 manifest discipline).
- **`migrate-project`** — Apply version-by-version plugin migration deltas to bring an existing project up to the current plugin version. Driven by per-release manifests under `migrations/`. Refuses to run in Cowork. Triggered automatically by the SessionStart drift-detector hook when project's recorded plugin version is behind the installed plugin.

### Build skills

- **`build-component`** — Per-component build skill. Reads `brain/STRUCTURE.md` and relevant canon, scans for reusable existing components, proposes a strategy, generates the component, then fires `design-check`.
- **`build-page`** — Compositional sibling to `build-component`. For whole pages (marketing or dashboard). Long iterative conversation: asks which page, reads the brief and canon, proposes a plan section by section, accepts external references. Calls `build-component` inline for net-new primitives.
- **`design-direction`** — Deep brand-direction diagnostic. Extracts 9 taste axes, proposes 3 named directions with a moodboard, and writes `BRAND.md` + `DESIGN.md` Overview.
- **`calibrate`** — Calibration bridge inside `design-direction` (Phase 4→5). Builds a mission file from brand + register + archetype, walks a tiered inspiration source map, captures an annotated moodboard via the Aside browser, and writes a FOLLOW / DEVIATE / REFUSE conventions audit to `DESIGN.md`. Hands back via an explicit `Skill()` call.
- **`marketing-brief`** — One-time deep marketing-site brief. Builds a content registry, proposes a sitemap, writes per-page briefs, copy, media manifest, and layout sketches. Auto-skips on dashboard-only / internal-tool projects.

---

## Project layout

When `init-project` runs on v3.0.0, it creates this structure in your project:

```
project-root/
├── CLAUDE.md              ← rules + skill index + hooks index (always loaded)
├── README.md              ← file-and-dependency map
└── brain/                 ← single canon folder (all tiers merged here)
    ├── STATUS.md
    ├── BRIEF.md
    ├── WONT-DO.md
    ├── ROADMAP.md
    ├── WORKLOG.md
    ├── CHANGELOG.md
    ├── agenda.md          ← daily steering file
    ├── BRAND.md
    ├── FUNDAMENTALS.md
    ├── TOOLING.md         ← (Node projects only)
    ├── DESIGN.md
    ├── STRUCTURE.md
    ├── DISCOVERIES.md
    ├── docs/
    │   ├── INDEX.md
    │   └── detail/
    └── chapters/          ← one .md per chapter (CEO defines, worker executes)
```

The root `CLAUDE.md` is the brain — non-negotiable rules, skill index, hooks index, and a map of where everything lives. Every significant write to `BRIEF.md`, `STATUS.md`, `DISCOVERIES.md`, or `CHANGELOG.md` carries an author stamp (`· Cowork` / `· Claude Code` / `· Codex`) so the next agent can see who decided what. The old `.session-type` file is gone; author stamps carry that signal instead.

---

## Why it works

AI agents forget everything between sessions. This plugin fixes that by keeping all context in plain markdown files the agent reads at session start.

`brain/WORKLOG.md` is the discipline engine: every response that changes something appends one line. By session end, you have a full real-time audit trail. `save-session` distills it into `brain/CHANGELOG.md` and `brain/STATUS.md` so the next session starts from solid ground.

The **discipline skills** add a second layer: gates that fire automatically when their description matches the conversation. They force the agent to verify before acting, read before answering, and audit before closing — the patterns that fail in untrained agent sessions.

**CEO/worker/solo model.** For non-trivial work the CEO breaks the project into chapters, each chapter is a scoped unit a worker picks up in an isolated git worktree. The worker executes, writes a Completion Report, and calls `handoff`. The CEO reviews and merges. This keeps individual sessions small and the audit trail clean. Solo mode collapses the model to a single agent for simpler work.

**One agent at a time.** Either Claude Code or Codex is active on a project, never both simultaneously. Author stamps on every significant write record which agent made each decision.

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

Outputs `project-protocol-vX.Y.Z.zip` in the `dist/` folder. This zip is the manual fallback documented under [Install & updates](#install--updates); the repo marketplace is the primary install path.

To release: bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, then run `./build.sh`. Bumping `version` in `plugin.json` is also what signals a new version to marketplace installs.

---

## License

MIT

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
