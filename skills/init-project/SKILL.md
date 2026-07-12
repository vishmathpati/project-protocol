---
name: init-project
description: "Create or repair the Universal Foundation for a project: inspect the repository, establish the single brain canon, capture universal project truth once, and route to the appropriate next skill without running brand, marketing, design, research, or implementation."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*,ls:*,find:*,cat:*,git:*)
---

# Init Project — Universal Foundation

Establish the universal project contract once. Specialized groups consume it instead of asking the same project questions again.

## Modes

- `new-empty` — empty or near-empty repository.
- `new-existing` — code exists but Project Protocol does not.
- `initialized` — current `brain/` foundation exists; audit missing pieces only.
- `legacy` — old flat or three-folder protocol; route to migration.

Foundation is not a modernization mega-mode. Version drift belongs to migration; inconsistency to Project Audit; design drift to Design Check.

## 1. Inspect first

Read repository structure, manifests, lockfiles, configs, existing documentation, Git branch/worktree, and existing canon. Never ask for a fact already present.

## 2. Ask only universal gaps

Capture project identity and stage; users and problem; relevant business context; logical project parts and kinds; current scope and out-of-scope; locked project decisions; first priority; and necessary technical facts inspection cannot establish.

Do not ask brand positioning, marketing strategy, visual taste, colors, fonts, research depth, page composition, chapter plans, or implementation questions.

## 3. Create universal canon

Always ensure these exist, preserving customized content:

- root `CLAUDE.md`
- `brain/.plugin-version`
- `brain/BRIEF.md`
- `brain/STATUS.md`
- `brain/STRUCTURE.md`
- `brain/WORKLOG.md`
- `brain/CHANGELOG.md`
- `brain/agenda.md`
- `brain/WONT-DO.md`
- `brain/chapters/README.md`
- `brain/chapters/TEMPLATE.md`

Conditional owners create ROADMAP, TOOLING, docs/INDEX, BRAND, DESIGN, FUNDAMENTALS, TASTE, DISCOVERIES, marketing, research, moodboard, and dashboard artifacts. Foundation may create a conditional file only when applicability is established and real information is available.

Never create a real chapter, fake roadmap, fake history, invented brand/design direction, or research artifact.

## 4. File ownership

- BRIEF: current universal project contract and durable decisions.
- STATUS: current state, active chapters, blockers, pending human decisions, last saved session.
- STRUCTURE: logical-part-to-physical-path and stack map.
- WORKLOG: temporary meaningful recovery notes.
- CHANGELOG: accepted or shipped outcomes.
- agenda: next human checkout, role, chapter, or decision.
- WONT-DO: material active/reopened refusals.
- CLAUDE: concise constitution, skill router, and source index.

## 5. Finish and route

Validate cross-references, then recommend exactly one next doorway based on the first priority: `/ceo`, `/solo`, `/brand-foundation`, or continuation of active work. Do not auto-invoke it.

## Rules

- One source of truth per concern.
- Existing project configuration wins.
- Never overwrite customized files silently.
- Never modify root README merely to advertise protocol files.
- Never create `SITUATIONS.md`.
- Root CLAUDE is a concise index, not a procedure manual.
- Foundation is universal; specialized groups own their questions and outputs.
