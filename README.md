# project-protocol

A project operating system for Claude Code and Codex: durable canon, role-aware sessions, isolated worktrees, disciplined engineering, optional brand/frontend expertise, and one generated human dashboard.

Install once. Every project gets a shared system that works the same way no matter which agent you're using.

---

## Install & updates

The repo ships its own plugin marketplace (`.claude-plugin/marketplace.json`) — the marketplace is the install path on every tool.

### Claude Code (recommended)

Add this repo as a marketplace, then install the plugin from it:

```bash
/plugin marketplace add vishmathpati/project-protocol
/plugin install project-protocol@project-protocol
```

The first command registers the catalog (the `owner/repo` shorthand clones the repo over git, which is what makes the same-repo relative `source` resolve). The second installs the plugin; the name is `project-protocol@project-protocol` (plugin name `@` marketplace name).

**Updates.** Claude Code refreshes marketplaces and bumps installed plugins at startup when auto-update is on for the marketplace — enable it under `/plugin` → **Marketplaces** → select `project-protocol` → **Enable auto-update**. After an update you'll be prompted to run `/reload-plugins`. To pull a refresh by hand: `/plugin marketplace update project-protocol`.

How a new version is detected: Claude Code resolves the plugin version from `version` in `plugin.json` first, then the marketplace entry, then the git commit SHA. This plugin sets `version` in `.claude-plugin/plugin.json`, so existing installs see a new version when that field is bumped on a release. (If the `version` field were omitted, every new commit on the default branch would count as a new version instead.)

### Codex

Install via the co-located Codex manifest at `.codex-plugin/plugin.json`. Codex updates are manual — restart or re-sync after pulling a newer version. See [Compatibility](#compatibility) for the one-time `~/.codex/config.toml` setup that lets Codex read `CLAUDE.md` automatically.

---

## What you get

Skills and mechanical hooks turn AI coding sessions into a disciplined operation. Project context lives in a single `brain/` folder. Root `CLAUDE.md` is the concise always-loaded constitution, skill router, and source index.

### Role model (new in v3.0.0)

Work is organized around three roles:

- **CEO** — plans the work, breaks it into chapters, reviews and merges completed work.
- **Worker** — executes one chapter in an isolated worktree and writes an evidence-rich Completion Report.
- **Solo** — single-agent mode for smaller tasks that don't need the CEO/worker split.

Invoke `/ceo`, `/worker`, or `/solo` deliberately at session start; the role runs Recap from live Git and canon. Workers report finished work through Completion Reports. Handoff is reserved for unfinished cross-session or cross-tool continuity.

### Session lifecycle (the core 4)

- **`init-project`** — Establish the Universal Foundation without running specialist workflows.
- **`save-session`** — Persist role-owned state safely; saving is not completion, approval, or merge.
- **`recap`** — Role-aware orientation at session start, after compaction, or on return.
- **`add-context`** — Add extended context files (data contracts, domain reference, integrations).

### Role skills (new in v3.0.0)

- **`ceo`** — CEO mode: plan chapters, review Completion Reports, merge worker branches.
- **`worker`** — Worker mode: claim a chapter, execute in a git worktree, write a Completion Report.
- **`solo`** — Solo mode: single-agent execution without the CEO/worker split.
- **`handoff`** — Durable carry-over plus a paste-ready packet for continuing unfinished work from the same branch/checkpoint, including in a fresh app-created worktree.
- **`git`** — Git operations gate. Validates branch state, enforces commit message discipline, guards against unintended force-pushes.
- **`grill`** — Adversarial review: stress-tests a plan, implementation, or decision before it ships.
- **`bug-fixing`** — Structured bug investigation: reproduce → isolate → fix → verify, recording only meaningful recovery evidence.
- **`migrate-to-brain`** — Legacy compatibility migration from old flat/three-folder layouts to `brain/`. It inventories first, preserves README and customized canon, reconciles duplicates, and hands back without stamping success early.

### Discipline skills

Invoked explicitly — via `Skill()` calls from other skills, slash commands, or the hooks that dispatch them.

- **`change-check`** — Pre-action gate: pause, declare files-to-change, cascade-effects, verify canon, confirm, then act.
- **`verify-by-reading`** — Open the file before answering questions about it. Catches memory drift.
- **`completion-check`** — Spec-vs-implementation check before any chapter or task is marked done.
- **`discuss`** — Read-only mode when the user signals thinking ("discuss", "let's talk", "what do you think").
- **`project-audit`** — Cross-file consistency check across canon and repository truth. Reports drift, does not auto-fix.
- **`design-check`** — UI-work gate. Reads `DESIGN.md` + `FUNDAMENTALS.md`, searches `components/` for reuse, halts on missing tokens, scans the diff for raw hex / px / font values. Step 8 auto-fixes mechanical violations (raw hex matching tokens, missing dimensions, ellipsis, nbsp, etc.) with user confirmation. Human-judgment violations are surfaced for user input only.
- **`migrate-project`** — Build one consolidated migration plan, apply deterministic deltas, review semantic diffs, validate the target, and stamp the installed version only after every mandatory change succeeds.
- **`advisor`** — Research-first expert mode: searches before opining, gives an independent view with trade-offs; model-invoked on "what do you think / recommend" questions.
- **`test-driven-development`** — RED-GREEN-REFACTOR discipline for features and bugfixes; worker/solo route implementation chapters through it.

### Build skills

- **`build-component`** — Per-component build skill. Reads `brain/STRUCTURE.md` and relevant canon, scans for reusable existing components, proposes a strategy, generates the component, then fires `design-check`.
- **`build-page`** — Iterative composition and implementation for substantial brand-facing pages. Research-led marketing builds require one approved site-wide direction before page-by-page execution; conventional dashboard/product pages may use established project and shadcn patterns directly.
- **`brand-foundation`** — Establishes differentiation, emotional transformation, voice, cultural context, trust, archetype, distinctive assets, and refusals without repeating Universal Foundation questions.
- **`marketing-brief`** — Resumable Stage A/B workflow for conversion goals, offers, audiences, proof, sitemap, page intent, copy, and media requirements. It never owns page layout.
- **`ui-research`** — Optional Aside workflow that turns sitemap families, content goals, available media, and evidence into page-aware recommendations. Focused follow-up and exact component inspection remain separate lanes.
- **`inspect-component`** — Investigates one exact external UI region when its implementation mechanics are unclear.
- **`style-lock`** — Converts brand, content, research, existing tokens, and surface needs into an approved visual system through a real-content preview.
- **`project-dashboard`** — Deterministically renders bounded Project, Brand, Design, Research/Moodboard, and Build Progress views. Its loopback server persists only an explicitly submitted/updated provisional decision draft; `--check` detects staleness.

The Aside package ships standalone `ui-research` and `inspect-component` skills under `aside-skill/`. Upload them into Aside; Project Protocol supplies each project mission and ingests the evidence.

---

## Project layout

Universal Foundation creates the core files; specialist groups add their optional canon when used:

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
    ├── moodboard/         ← local screenshots + manifest.md from UI Research
    ├── research/          ← evidence plus derived page recommendations and provisional decision draft
    ├── project-dashboard.html  ← concise visual review/decision aid; never source of truth
    ├── docs/
    │   ├── INDEX.md
    │   └── detail/
    └── chapters/          ← one .md per chapter (CEO defines, worker executes)
```

Root `CLAUDE.md` is the concise constitution, skill router, and source index. Detailed truth stays in its owning canon file. The generated dashboard summarizes those sources and presents research one concept/site/recommendation at a time. Candidate choices remain browser-local until universal Submit/Update writes one provisional JSON draft; Claude or Codex validates the complete combination, and only explicit human approval produces the exact Markdown site-direction lock.

---

## Why it works

AI agents forget everything between sessions. This plugin fixes that by keeping all context in plain markdown files the agent reads at session start.

`brain/WORKLOG.md` is a temporary recovery buffer for meaningful progress, decisions, blockers, failed attempts, and next actions. Save Session folds durable information into its proper owner and removes only recovery entries that were safely folded.

Mechanical hooks provide reminders and deterministic findings; skills own judgment. Hooks never choose roles, approve work, save, research, merge, or regenerate the dashboard.

**CEO/worker/solo model.** Role controls authority; Local vs Worktree controls checkout topology. All roles accept an app-created worktree. Local mode remains supported with a one-time isolation recommendation; workers use a dedicated branch. The CEO defines and verifies durable chapters, workers report evidence, and solo collapses the model for genuinely small work.

### Mechanical hooks

- Session Start: role/Recap reminder plus version-drift detection.
- PreCompact/PostCompact: branch/worktree recovery context and same-role Recap routing; no backup-file accumulation.
- Stop: warning only when Git or WORKLOG suggests unpersisted state.
- Post-write: deterministic UI findings, Design Check routing, and Style Lock synchronization reminder after DESIGN changes.

**Multiple tools, isolated work.** Claude Code and Codex may work on separate chapter worktrees. Git branches and chapter contracts establish ownership; author stamps record provenance.

---

## Compatibility

Works with Claude Code, Codex CLI, and any tool that supports the [agentskills.io](https://agentskills.io) skill standard.

- No hardcoded model names.
- Every skill ships with both a Claude Code `SKILL.md` and a Codex `agents/openai.yaml` sidecar.
- Dual manifest: `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json`.
- Worktree detection in `recap` for both Codex (`.codex/worktrees/`) and Claude Code (`.claude/worktrees/`).
- SessionStart hook degrades gracefully if the host doesn't expose `${CLAUDE_PLUGIN_ROOT}` or `${CODEX_PLUGIN_ROOT}`.

**Codex one-time setup:** add this to `~/.codex/config.toml` so Codex reads `CLAUDE.md` automatically:

```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

---

## Developing this plugin

Contributor-specific instructions, private project canon, and personal workshop skills intentionally live outside this public repository. This repository contains only distributable plugin source, tests, migrations, and public documentation. Contributors should use their own private project-management layer and must never commit private canon or installed/cache artifacts here.

Only a human-approved release chapter may release. At that point run `scripts/bump-version.sh <new-version>` (syncs both plugin.json files + marketplace.json), add `migrations/vX.Y.Z.md` and a CHANGELOG entry, then run `scripts/bump-version.sh --audit`. The audit structurally validates manifests, skills, sidecars, hooks, migration presence, and package cleanliness before integration.

---

## License

MIT

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
