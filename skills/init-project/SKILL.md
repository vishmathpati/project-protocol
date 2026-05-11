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
│   ├── STATUS.md
│   ├── BRIEF.md
│   ├── ROADMAP.md
│   ├── BRAND.md
│   ├── FUNDAMENTALS.md
│   ├── DESIGN.md
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

## The 7 phases

1. **Discovery** — find every `.md` file, bucket into protocol / design / other.
   → See `references/phase-1-discovery.md`.
2. **Non-protocol merge** — ask the user what to do with each non-protocol file.
   → See `references/phase-2-non-protocol-merge.md`.
3. **Three-folder structure** — create root + subfolders + protocol files.
   → See `references/phase-3-three-folder-create.md`.
4. **Design system** — create BRAND, BRIEF, FUNDAMENTALS, DESIGN, DISCOVERIES in `agents/`.
   → See `references/phase-4-design-system.md`.
5. **docs/INDEX.md** — generate by analyzing codebase via sub-agents.
   → See `references/phase-5-docs-index.md`.
6. **Extended context** — optional loop for adding deep-reference files.
   → See `references/phase-6-extended-context.md`.
7. **Final summary** — surface anything that needs user attention.
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
- `agents/FUNDAMENTALS.md` is the one exception — global standard, always copied from plugin template `templates/FUNDAMENTALS.md`.
- `agents/CHANGELOG.md` and `cowork/CHANGELOG.md` are never overwritten. Append-only.
- All decisions made during init that warrant locking go into `cowork/BRIEF.md` (orchestration) or `agents/BRIEF.md` (product).
- The three folders are non-negotiable — every file belongs to exactly one tier.

---

## Audit-mode detection

If the project already has root `CLAUDE.md` + the three subfolders (`cowork/`, `agents/`, `human/`), this is an **audit run** rather than fresh init. Behavior changes:

- Read existing files; do not overwrite populated content.
- Fill missing files only.
- Report mismatches between expected layout and actual.
- Apply the `audit` skill at the end to surface canon inconsistencies.

---

## When init-project finishes

You should have:
- Root `CLAUDE.md` and `README.md` populated with project-specific content.
- `cowork/` populated with orchestration-tier stubs.
- `agents/` populated with full agent canon — STATUS, BRIEF stub, ROADMAP, BRAND/FUNDAMENTALS/DESIGN, DISCOVERIES stub, WORKLOG empty, CHANGELOG header, docs/INDEX.md generated.
- `human/agenda.md` empty stub for the user to fill via the first real session.

End with the Phase 7 summary outputting any [VERIFY] items that need user confirmation.
