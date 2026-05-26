---
name: init-project
description: Initialize or audit a project with the three-folder protocol (cowork/agents/human + root CLAUDE.md/README.md). Triggers — "init project", "bootstrap project", or when a project has no root CLAUDE.md.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*,ls:*,find:*,cat:*,cp:*), AskUserQuestion, Task
---

# Init Project

Initialize or audit the current project with the **three-folder layout**. Goal: ONE unified system where every file has a clear audience.

---

## Output layout (what gets created)

```
project-root/
├── CLAUDE.md              ← rules + folder map (always loaded)
├── README.md              ← file-and-dependency map (open before any edit)
├── cowork/                ← orchestration tier (Cowork's discipline files)
│   ├── CLAUDE.md
│   ├── STATUS.md
│   ├── BRIEF.md
│   ├── WORKLOG.md
│   └── CHANGELOG.md
├── agents/                ← project canon tier (Codex / Claude Code read here)
│   ├── .session-type      ← written at Phase 3a; one of: cowork, claude-code, codex
│   ├── STATUS.md
│   ├── BRIEF.md
│   ├── ROADMAP.md
│   ├── BRAND.md
│   ├── FUNDAMENTALS.md
│   ├── TOOLING.md         ← Node projects only; package manager rendered at Phase 4a
│   ├── DESIGN.md
│   ├── SITUATIONS.md      ← situation router; written at Phase 3b
│   ├── STRUCTURE.md       ← created on first build-component run, or during Phase 0c modernize
│   ├── DISCOVERIES.md
│   ├── WORKLOG.md
│   ├── CHANGELOG.md
│   └── docs/
│       ├── INDEX.md
│       └── detail/
└── human/                 ← human-facing tier
    └── agenda.md          ← daily steering file
```

---

## The phases

0.  **Mode detection** — decide which init mode applies (audit / migration / empty / fresh).
    → See `references/phase-0-mode-detection.md`. **Always runs first.**

0a. **Empty bootstrap** — only when mode = empty. Ask the user a short set of questions about the project so templates get real content instead of placeholders.
    → See `references/phase-0a-empty-bootstrap.md`. After this, jump to Phase 3.

0b. **Old-version migration** — only when mode = migration. Move every old-layout file into the three-folder layout, split root `CLAUDE.md`, preserve all user content, layer in new-version files where missing.
    → See `references/phase-0b-migration.md`. After this, continue to Phase 1 with `migration_complete = true`.

0c. **Modernize existing project** — only when mode = modernize. Re-confirm canon with user, sweep for drift, archive waste.
    → See `references/phase-0c-modernize.md`.

1.  **Discovery** — find every `.md` file, bucket into protocol / design / other.
    → See `references/phase-1-discovery.md`. Skipped if mode = empty.

2.  **Non-protocol merge** — ask the user what to do with each non-protocol file (cowork / agent-docs / merge / reference / leave / skip).
    → See `references/phase-2-non-protocol-merge.md`. Skipped if mode = empty.

3.  **Three-folder structure** — create root + subfolders + protocol files. Bootstrap answers (if any) populate templates; migrated files are never overwritten.
    → See `references/phase-3-three-folder-create.md`.

4.  **Design system** — create BRAND, BRIEF, FUNDAMENTALS, DESIGN, DISCOVERIES in `agents/`.
    → See `references/phase-4-design-system.md`.

5.  **docs/INDEX.md** — generate by analyzing codebase via sub-agents. Empty-mode writes a minimal stub. Apply any agent-docs cross-references buffered from Phase 2.
    → See `references/phase-5-docs-index.md`.

6.  **Extended context** — optional loop for adding deep-reference files.
    → See `references/phase-6-extended-context.md`.

7.  **Final summary** — surface anything that needs user attention. Output varies by mode.
    → See `references/phase-7-summary.md`.

Open each reference only when entering that phase. Progressive disclosure keeps your context lean.

---

## Sub-agent model routing

Delegate file analysis via the Task tool — do NOT do heavy reads inline (fills your context).

| Task | Tier | Why |
|------|------|-----|
| Scanning route/page files, extracting names | fast | Pure extraction |
| Scanning `.env.example` for service keys | fast | Pattern matching |
| Scanning `package.json` for stack | fast | Structured read |
| Finding shared functions across files | reasoning | Import graph analysis |
| Identifying features and their dependencies | reasoning | Reasoning about relationships |
| Writing INDEX.md sections | reasoning | Judgment about what matters |
| Writing CLAUDE.md from merged content | reasoning | Synthesis |
| Categorizing WORKLOG entries for CHANGELOG | fast | Simple classification |
| Generating DESIGN.md from BRAND + stack | reasoning | Judgment about design tokens |

Rule: fast/cheap model for extraction, reasoning model for judgment. Never the most expensive model for any init-project task.

---

## Hard rules

- Never silently overwrite an existing file. Read first, ask before replacing.
- `agents/FUNDAMENTALS.md` is one exception — global standard, always copied from plugin template `templates/FUNDAMENTALS.md`.
- `agents/TOOLING.md` — generated for Node projects only (detected via `package.json` at project root). On first init, rendered from `templates/TOOLING.md` with the package manager the user chooses (or confirms from detected lockfile) during Phase 4a. On re-init, re-generated with confirmed manager. Skipped silently for Swift / Python / non-Node projects.
- `agents/CHANGELOG.md` and `cowork/CHANGELOG.md` are never overwritten. Append-only.
- All decisions made during init that warrant locking go into `cowork/BRIEF.md` (orchestration) or `agents/BRIEF.md` (product).
- The three folders are non-negotiable — every file belongs to exactly one tier.
- Root `CLAUDE.md` has a **300-line ceiling**. If it would exceed that, extract detail into a support file under `agents/docs/` and leave a one-line pointer in `CLAUDE.md`. Keep the always-loaded file lean.

---

## Mode detection (Phase 0)

Phase 0 runs before anything else and produces one of five modes:

- **`modernize`** — three-folder layout already in place AND canon files are populated AND the user invoked an upgrade pass (or opted in from audit). Phase 0c re-confirms each populated canon file with the user, sweeps the codebase for design-system drift, archives waste, reconciles STRUCTURE.md, and silently re-applies global standards.
- **`audit`** — three-folder layout already in place. Read existing files; do not overwrite populated content. Fill missing files only. Report mismatches at Phase 7. Apply the `audit` skill at the end to surface canon inconsistencies.
- **`migration`** — older flat-root layout detected. Phase 0b migrates everything into the three-folder layout (preserving all user content) before the standard phases run.
- **`empty`** — no markdown anywhere. Phase 0a collects basic project info from the user so templates can be populated with real content.
- **`fresh`** — existing codebase with no protocol files. Standard Phase 1 → 7 flow.

Sub-detail lives in `references/phase-0-mode-detection.md`.

---

## When init-project finishes

You should have:
- Root `CLAUDE.md` and `README.md` populated with project-specific content.
- `cowork/` populated with orchestration-tier stubs.
- `agents/` populated with full agent canon — STATUS, BRIEF stub, ROADMAP, BRAND/FUNDAMENTALS/DESIGN, DISCOVERIES stub, WORKLOG empty, CHANGELOG header, docs/INDEX.md generated. For Node projects: `TOOLING.md` also copied from plugin template.
- `human/agenda.md` empty stub for the user to fill via the first real session.

End with the Phase 7 summary outputting any [VERIFY] items that need user confirmation.
