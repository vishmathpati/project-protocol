---
name: init-project
description: Initialize or audit a project with the single-folder brain protocol (one `brain/` folder + root CLAUDE.md/README.md). Triggers — "init project", "bootstrap project", or when a project has no root CLAUDE.md.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*,ls:*,find:*,cat:*,cp:*), AskUserQuestion, Task
---

# Init Project

Initialize or audit the current project with the **single-folder `brain/` layout**. Goal: ONE unified system where every canon file lives once, in one place, with no folder duplication.

---

## Output layout (what gets created)

```
project-root/
├── CLAUDE.md              ← always-loaded front page / rules index (NOT the brain)
├── README.md              ← file-and-dependency map (open before any edit)
└── brain/                 ← the single canon folder. Every agent reads here.
    ├── .plugin-version    ← plugin-version marker (read by the drift-detector hook)
    ├── STATUS.md          ← current project state
    ├── BRIEF.md           ← project decisions (WHAT we build), author-stamped per entry
    ├── WONT-DO.md         ← running list of rejected decisions, each with a one-line reason
    ├── ROADMAP.md         ← phases and ordering
    ├── WORKLOG.md         ← real-time log, author-stamped per entry; cleared by save-session
    ├── CHANGELOG.md       ← project history, author-stamped; never cleared
    ├── agenda.md          ← daily steering file
    ├── BRAND.md           ← product identity
    ├── FUNDAMENTALS.md     ← global design framework (copied from plugin template)
    ├── TOOLING.md         ← Node projects only; package manager rendered at Phase 4a
    ├── DESIGN.md          ← project design tokens
    ├── STRUCTURE.md       ← codebase surface map; created on first build-component run, OR during Phase 0c modernize, OR during Phase 4 of fresh init if user opts in
    ├── DISCOVERIES.md      ← append-only UI patterns
    ├── SITUATIONS.md       ← situation router; written at Phase 3b
    ├── preview/           ← design-direction preview HTML lives here; gitignored; cleaned by audit
    ├── marketing/         ← marketing-brief output (CONTENT registry, sitemap, per-page briefs/copy); created by marketing-brief
    └── docs/
        ├── INDEX.md
        └── detail/
```

Every canon file stays SEPARATE by purpose. STATUS, BRIEF, WORKLOG, CHANGELOG are distinct files — they are not merged. We removed folder duplication (`cowork/` + `agents/` + `human/` → one `brain/`), not the distinction between files.

---

## Author-stamp convention (replaces the old tier concept)

There is no longer a "tier" or a `.session-type` marker. Instead, every **WORKLOG**, **BRIEF**, and **CHANGELOG** entry is stamped with who wrote it:

- `· Codex` — written during a Codex session.
- `· Claude Code` — written during a Claude Code session.
- `· Agent` — written by a host that can't be determined.

The stamp goes on the `> Last updated:` line and on each version/entry header. This makes authorship visible without splitting the project across three folders. Detect the current author at write time from the runtime (Codex / Claude Code / Agent) — do not persist it to a marker file.

---

## The phases

0.  **Mode detection** — decide which init mode applies (audit / modernize / hand-off / empty / fresh).
    → See `references/phase-0-mode-detection.md`. **Always runs first.**

0a. **Empty bootstrap** — only when mode = empty. Ask the user a short set of questions about the project so templates get real content instead of placeholders.
    → See `references/phase-0a-empty-bootstrap.md`. After this, jump to Phase 3.

0c. **Modernize existing project** — only when mode = modernize (already on the `brain/` layout, user wants an upgrade pass). Re-confirm canon with user, sweep for drift, archive waste.
    → See `references/phase-0c-modernize.md`.

(There is no inline migration phase. Old three-folder or flat-root projects are handed off to the `migrate-to-brain` skill — see Phase 0 mode detection.)

1.  **Discovery** — find every `.md` file, bucket into protocol / design / other.
    → See `references/phase-1-discovery.md`. Skipped if mode = empty.

2.  **Non-protocol merge** — ask the user what to do with each non-protocol file (brain-docs / merge / reference / leave / skip).
    → See `references/phase-2-non-protocol-merge.md`. Skipped if mode = empty.

3.  **Brain structure** — create root files + `brain/` + protocol files. Bootstrap answers (if any) populate templates.
    → See `references/phase-3-brain-create.md`.

4.  **Design system** — create BRAND, BRIEF, FUNDAMENTALS, DESIGN, DISCOVERIES in `brain/`.
    → See `references/phase-4-design-system.md`.

5.  **docs/INDEX.md** — generate by analyzing codebase via sub-agents. Empty-mode writes a minimal stub. Apply any brain-docs cross-references buffered from Phase 2.
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
- `brain/FUNDAMENTALS.md` is one exception — global standard, always copied from plugin template `templates/FUNDAMENTALS.md`.
- `brain/TOOLING.md` — generated for Node projects only (detected via `package.json` at project root). On first init, rendered from `templates/TOOLING.md` with the package manager the user chooses (or confirms from detected lockfile) during Phase 4a. On re-init, re-generated with confirmed manager. Skipped silently for Swift / Python / non-Node projects.
- `brain/CHANGELOG.md` is never overwritten. Append-only.
- All decisions made during init that warrant locking go into `brain/BRIEF.md` (author-stamped).
- Rejected decisions go into `brain/WONT-DO.md` — a running list, each with a one-line reason.
- One folder, one home. Every canon file lives once inside `brain/`. No duplication across folders.
- Root `CLAUDE.md` has a **300-line ceiling**. If it would exceed that, extract detail into a support file under `brain/docs/` and leave a one-line pointer in `CLAUDE.md`. Keep the always-loaded file lean.

---

## Mode detection (Phase 0)

Phase 0 runs before anything else and produces one of four modes:

- **`modernize`** — `brain/` layout already in place AND canon files are populated AND the user invoked an upgrade pass (or opted in from audit). Phase 0c re-confirms each populated canon file with the user, sweeps the codebase for design-system drift, archives waste, reconciles STRUCTURE.md, and silently re-applies global standards.
- **`audit`** — `brain/` layout already in place. Read existing files; do not overwrite populated content. Fill missing files only. Report mismatches at Phase 7. Apply the `audit` skill at the end to surface canon inconsistencies.
- **`empty`** — no markdown anywhere. Phase 0a collects basic project info from the user so templates can be populated with real content.
- **`fresh`** — existing codebase with no protocol files. Standard Phase 1 → 7 flow.

There is a fifth case that is NOT an init mode: a project on the **OLD three-folder layout (`cowork/` + `agents/` + `human/`)** or an **old flat-root legacy layout**. init-project does NOT migrate these inline. Phase 0 detects them and tells the user to run the `migrate-to-brain` skill instead.

Sub-detail lives in `references/phase-0-mode-detection.md`.

---

## When init-project finishes

You should have:
- Root `CLAUDE.md` and `README.md` populated with project-specific content.
- `brain/` populated with full canon — STATUS, BRIEF stub, WONT-DO stub, ROADMAP, BRAND/FUNDAMENTALS/DESIGN, DISCOVERIES stub, SITUATIONS router, WORKLOG empty, CHANGELOG header, agenda stub, docs/INDEX.md generated, `.plugin-version` marker. For Node projects: `TOOLING.md` also copied from plugin template.

End with the Phase 7 summary outputting any [VERIFY] items that need user confirmation.
