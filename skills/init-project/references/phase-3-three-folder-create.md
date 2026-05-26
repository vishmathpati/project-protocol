# Phase 3 — Create three-folder structure

Create the root files + cowork/, agents/, human/ subfolders + protocol files. Apply Phase 2 merge decisions during template population.

## 3a. Create folders and session-type marker

```bash
mkdir -p cowork agents human agents/docs/detail
```

### Write `agents/.session-type` marker

Detect the current session type and write it as a one-line file:

```bash
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -z "${CODEX_PLUGIN_ROOT:-}" ]; then
  echo "claude-code" > agents/.session-type
elif [ -n "${CODEX_PLUGIN_ROOT:-}" ]; then
  echo "codex" > agents/.session-type
else
  echo "cowork" > agents/.session-type
fi
```

This file is read by all hooks to determine the correct WORKLOG path (`agents/WORKLOG.md` for claude-code/codex, `cowork/WORKLOG.md` for cowork). On re-init: overwrite — the session type is always the current runtime, not a persisted choice.

## 3b. Root files

### Root `CLAUDE.md` template

```markdown
# CLAUDE.md — [Project Name]

> Always loaded by every agent. The brain. Read top to bottom every session.

## Coding Standards

**1. Think Before Coding** — State assumptions. Surface tradeoffs. Ask when unclear.
**2. Simplicity First** — Minimum code. No speculative features. No unnecessary abstractions.
**3. Surgical Changes** — Touch only what you must. Match existing style.
**4. Verify Before Closing** — Define done before touching code. Screenshot UI changes. Reproduce bugs before fixing.

## Non-negotiable rules

1. Decide before you act. Write it down before you decide.
2. When you change one file, list every other file that becomes stale (see `README.md` cascade rules).
3. Lock-before-cascade: changes hit `BRIEF.md` first, then propagate.
4. Audit before close: independent verification before any chapter is marked done.
5. Commit + push before leaving any chat. Pull main before starting one.
6. One tool active at a time.
7. **If Node project:** read `agents/TOOLING.md` before any package, install, or dev-server work. Never run the wrong package manager — check TOOLING.md for this project's choice.
8. **UI work uses the design system. No hardcoded values, ever.** Before editing any `.tsx` / `.jsx` / `.vue` / `.svelte` / `.swift` / styles file: read `agents/DESIGN.md` for tokens and `agents/FUNDAMENTALS.md` for the Token Rule. Run the `design-check` skill before writing and again after. Raw hex, raw px, raw `font-family` strings, emoji-as-icon, and other cardinal sins from `FUNDAMENTALS.md` in component files are violations — not preferences. If a needed token doesn't exist in `DESIGN.md`: stop and propose adding it. Do not improvise.
9. **UI components — shadcn first when shadcn is in `package.json`.** Default: always use the shadcn primitive (`<Button>`, `<Input>`, `<Select>`, `<Dialog>`, `<Popover>`, `<Tooltip>`, `<Sheet>`, `<Drawer>`, `<Tabs>`, `<Accordion>`, `<DropdownMenu>`, `<Command>`, `<Toast>`, `<Alert>`, `<Checkbox>`, `<Radio>`, `<Switch>`, `<Slider>`, `<Textarea>`). Never silently fall back to the native element because it's faster to type. Allowed native elements: `<a href>` for navigation, `<button type="submit">` inside a `<form>` when no styled `<Button>` is needed, `<input type="hidden">`. If a needed primitive doesn't exist in shadcn (e.g. date-range picker), stop and ask: build one in `components/ui/` following shadcn conventions, install a community block, or use another library.
10. Use the skill index below. Don't improvise a workflow when a skill exists for it.

## Skill index — what's available and when to use it

| Skill | When to use it | How to invoke |
|---|---|---|
| `add-context` | Adding a deep-reference doc (integration, API, design notes) to the project. | `/add-context` · "add context", "add context file" |
| `audit` | Periodic consistency check across all canon files to surface drift. | `/audit` · "run audit", "check canon consistency" |
| `audit-before-close` | Verification gate before marking any chapter, task, or feature complete. | `/audit-before-close` · "audit before close", before any chapter close |
| `build-component` | Building a new UI component or adopting an external one into the design system. | `/build-component` · "build component", "new component", "create component" |
| `build-page` | Composing a whole page (marketing or dashboard) through an iterative conversation. | `/build-page` · "build the homepage", "build the X page", "compose page X" |
| `design-check` | Pre- and post-write gate for any UI file edit — checks tokens, reuse, and cardinal sins. | `/design-check` · "edit UI", "change styles", "add page", any visual change |
| `design-direction` | Deep brand diagnostic: extracts taste axes, proposes 3 named directions + moodboard. | `/design-direction` · "design direction", "set up the design system", "re-anchor brand" |
| `discipline` | Pre-action gate before any non-trivial change — forces pause, declares cascades, verifies canon. | `/discipline` · "before I do this", "I'm about to edit Y" |
| `discussion-mode` | No-edit conversation mode — prevents file edits during thinking or planning. | `/discussion-mode` · "discuss", "let's talk", "brainstorm", "explore" |
| `edit-plugin` | Mandatory gate when editing this plugin's own source files. | `/edit-plugin` · "edit the plugin", "update the X skill" |
| `init-project` | Initialize or re-initialize a project with the three-folder protocol. | `/init-project` · "init project", "bootstrap project" |
| `marketing-brief` | Deep marketing-site brief that writes canonical `agents/marketing/` files consumed by build-page. | `/marketing-brief` · "marketing brief", "write marketing site", "build marketing copy" |
| `migrate-project` | Apply version-by-version plugin deltas to bring a project up to the current plugin version. (Added in v2.5.0 — see Phase D.) | `/migrate-project` · "migrate project", "update plugin files" |
| `save-session` | Save and close a project session — updates WORKLOG → CHANGELOG, STATUS, BRIEF. | `/save-session` · "save", "save session", "close session", "done for today" |
| `session-recap` | Mid-session snapshot — reads WORKLOG + STATUS and reports current state. | `/session-recap` · "recap", "where are we", "what have we done", "catch me up" |
| `verify-by-reading` | Read-before-answer enforcement — opens actual files before answering questions about content. | `/verify-by-reading` · "what does X say", "is Y implemented", before answering any file-content question |

## Hooks index — what runs automatically

| Hook event | What it does | What to do when it warns |
|---|---|---|
| `SessionStart` | Injects orient reminder: read CLAUDE.md + STATUS.md before touching code, run save-session before closing. | Follow it. Read CLAUDE.md and STATUS.md now if you haven't. |
| `UserPromptSubmit` | Reminds to classify the task (NEW / ADDITION / UI CHANGE / BUG FIX) and append to WORKLOG after each action. | Classify before acting. Append WORKLOG entry after each change. |
| `PreToolUse Edit\|Write` | Checks if WORKLOG is in cleared state; warns if so (means no entry logged yet this session). | Append a WORKLOG entry for the change you're about to make. |
| `PreCompact` | Backs up WORKLOG before compaction so content survives context trim. | No action needed — informational. Content is preserved in backup. |
| `PostCompact` | Re-injects orient reminder after compaction. | Re-read CLAUDE.md and STATUS.md to re-orient before continuing. |
| `SubagentStart` | Appends a `subagent_start` timestamp to WORKLOG. | No action needed — automatic bookkeeping. |
| `SubagentStop` | Appends a `subagent_stop` timestamp to WORKLOG. | No action needed — automatic bookkeeping. |
| `Stop` | Checks WORKLOG for unsaved work; warns with line count if save-session hasn't run. | Run `/save-session` before closing the chat. |
| `PostToolUse Edit\|Write` (design-scan) | After any UI file write, greps content for raw hex, raw px, raw font-family, native elements when shadcn exists, banned patterns. | Fix each flagged violation before continuing. Violations are not preferences. |
| `PostToolUse Edit\|Write` (design-check dispatcher) | After writing to a component-tier path, instructs agent to run `/design-check` on the file. | Run `/design-check` on the written file immediately. |
| `SessionStart` (drift-detector) | Detects plugin-version drift by comparing `agents/.plugin-version` to current plugin version. (Added in v2.5.0 Phase D — stub.) | Run `/migrate-project` when prompted to apply pending deltas. |

## Situation router — common requests → which skill

See `agents/SITUATIONS.md` for the full routing table.

## Folder map

- `cowork/` — orchestration tier. Cowork edits here. Agents do not read it.
- `agents/` — project canon. All agents read here.
- `human/` — your tier. Cowork derives this from `agents/`.

## Pre-task classification (mandatory before any code change)

1. NEW standalone feature
2. ADDITION to existing feature
3. UI CHANGE
4. BUG FIX

Check `agents/docs/INDEX.md` dependency entries before classifying.

## Extended Context

<!-- add-context appends here -->
```

### Root `README.md` template

```markdown
# README.md — File Map & Dependencies

> Open this whenever you're about to change a non-trivial file. Find that file below. Its "When this changes" line tells you which other files need updating.

## File catalog

### Root
- **CLAUDE.md** — rules + folder map. Always loaded by every agent.
- **README.md** — this file. Open before any non-trivial edit.

### `cowork/`
- **CLAUDE.md** — Cowork-specific rules and discipline.
- **STATUS.md** — current orchestration state. No cascade.
- **BRIEF.md** — orchestration decisions (HOW we work). When this changes: `cowork/CLAUDE.md` may need updating.
- **WORKLOG.md** — real-time. Cleared by save-session.
- **CHANGELOG.md** — orchestration history. Never cleared.

### `agents/`
- **STATUS.md** — project state. No cascade.
- **BRIEF.md** — project decisions (WHAT we build). When this changes: `agents/ROADMAP.md` may need updating, `agents/STATUS.md` Next Actions may need updating, `human/agenda.md` may need re-derivation.
- **ROADMAP.md** — phases and ordering. When this changes: `agents/STATUS.md` Next Actions update, `human/agenda.md` re-derive.
- **BRAND.md** — product identity. When this changes: `agents/DESIGN.md` may need updating.
- **FUNDAMENTALS.md** — global design framework. Never edited per project.
- **TOOLING.md** — Node tooling convention for this project (package manager, lockfile, Node version). When this changes: refreshed from plugin template with chosen package manager, not by hand.
- **DESIGN.md** — project tokens. When this changes: pending UI work pauses until tokens validate.
- **DISCOVERIES.md** — append-only UI patterns. No cascade.
- **WORKLOG.md** / **CHANGELOG.md** — same role as cowork's but for project work.
- **docs/INDEX.md** — feature dependency map. Source for cross-feature lookups.
- **docs/detail/** — deep reference. When changed: relevant feature contracts may need re-reading.
- **preview/** — design-direction preview HTML files. Gitignored. Garbage-collected by `audit` (keeps most recent 2 per direction-slug).

### `human/`
- **agenda.md** — daily steering file. When `agents/ROADMAP.md` or `agents/BRIEF.md` change: re-derive.

## Cascade summary (rule of thumb)

```
agents/BRIEF.md → agents/ROADMAP.md → agents/STATUS.md → human/agenda.md
```

If you change anything upstream, check everything downstream.
```

### `agents/SITUATIONS.md` template

```markdown
# agents/SITUATIONS.md — Situation Router

> When the user says or you're about to do X, use skill Y and read Z first.
> This is the full routing table; root CLAUDE.md points here.

| If the user says or you're about to do X | Use skill | Read first |
|---|---|---|
| Any UI work — editing a component, page, or styles file | `design-check` | `agents/DESIGN.md`, `agents/FUNDAMENTALS.md` |
| Design feels wrong / palette off / looks too generic | `design-direction` | `agents/BRAND.md` |
| Raw hex / px / font-family values found in a component | `design-check` | `agents/FUNDAMENTALS.md` (Token Rule section) |
| Want to commit, update WORKLOG, and close the session | `save-session` | `agents/STATUS.md` |
| Setting up a brand new project or re-initializing | `init-project` | nothing (this is the entry point) |
| Migrating an existing project to the current plugin version | `migrate-project` | `agents/.plugin-version` |
| About to edit something non-trivial — risky or cascading | `discipline` | `README.md` (cascade rules) |
| Want a recap of where the project stands right now | `session-recap` | nothing (reads WORKLOG + STATUS itself) |
| Writing a feature spec or locking a product decision | `discipline` then `agents/BRIEF.md` append | `agents/BRIEF.md`, `agents/ROADMAP.md` |
| Running a full marketing site build | `marketing-brief` then `build-page` | `agents/BRIEF.md`, `agents/BRAND.md` |
| Writing or composing a full page (marketing or dashboard) | `build-page` | `agents/marketing/briefs/<slug>.md`, `agents/DESIGN.md` |
| Building a UI component or adopting one from an external source | `build-component` | `agents/STRUCTURE.md`, `agents/DESIGN.md` |
| Editing this plugin's own skills, hooks, or templates | `edit-plugin` | plugin `SKILL.md` for the skill being changed |
| Adding a long reference doc (API spec, integration notes) | `add-context` | `agents/docs/INDEX.md` |
| About to mark a feature, chapter, or task as done | `audit-before-close` | the relevant spec or contract file |
| Need to verify what a file actually says (not memory) | `verify-by-reading` | the file in question |
```

## 3c. cowork/ files

### `cowork/CLAUDE.md`

```markdown
# cowork/CLAUDE.md — Cowork Discipline

> Loaded when Cowork is working inside `cowork/` or orchestrating cross-tool.

## Cowork's role

- Orchestrator. Plans, locks, cascades, derives, delegates, audits.
- Never executes specialist work directly (UI goes to Claude Code, backend to Codex).
- Holds context across sessions via persistent memory.

## Rules

1. **Discussion-default.** When user says "discuss" / "let's talk," do not edit (`discussion-mode` skill applies).
2. **Lock-before-act.** Conversational decisions captured in `cowork/BRIEF.md` (orchestration) or `agents/BRIEF.md` (project) before acting (`discipline` skill applies).
3. **Cascade declaration.** Before any edit, list which other files become stale.
4. **Read-back rule.** Before recording a decision, read it back to the user in chat.
5. **Sub-agent for deep reads.** Tier-3 files get read by a sub-agent, synthesis returned (`verify-by-reading` skill applies).

## Tier loading

- **Tier 1 (always):** root CLAUDE.md, root README.md, this file, cowork/STATUS.md.
- **Tier 2 (on demand):** cowork/BRIEF.md, agents/STATUS.md, agents/BRIEF.md, agents/ROADMAP.md.
- **Tier 3 (sub-agent):** agents/docs/detail/, individual memory files.
```

### `cowork/STATUS.md` (60-line max)

```markdown
# cowork/STATUS.md
> Last updated: YYYY-MM-DD · Cowork

## Current focus
[One-line: what we're orchestrating right now]

## Health
- ✅ Working: [solid items]
- 🔴 Broken: [nothing or what's broken]
- 🔒 Blocked: [nothing or what's blocked]

## Pending human input
- [Items needing decision]

## Pending Cowork drafting
- [Things I owe]

## Recent sessions (rolling 5)
- YYYY-MM-DD · [one-line summary]

## Next actions
1. [Concrete next move]
```

### `cowork/BRIEF.md`

```markdown
# cowork/BRIEF.md — Orchestration Decisions
> How the user and Cowork work together. Append-only. 500-line limit; overflow to BRIEF-2.md.

---

## v1.0 — YYYY-MM-DD · Cowork

### What this is
[One-paragraph context]

### Locked decisions
1. [Decision]

### Rejected this session
- [Option rejected and why]
```

### `cowork/WORKLOG.md`

```markdown
# Worklog — Cowork orchestration
> Real-time log. Cleared by save-session.

(empty — last session closed cleanly)
```

### `cowork/CHANGELOG.md`

```markdown
# Changelog — Cowork
> Orchestration history. Never cleared. Keep a Changelog format.

## [Unreleased]
```

## 3d. agents/ files

### `agents/STATUS.md` (60-line max, fixed schema)

```markdown
# agents/STATUS.md
> Last updated: YYYY-MM-DD · [agent label]

## Current sprint
[One-paragraph context]

## Health
- ✅ Working: [confirmed working features]
- 🔴 Broken: [known bugs P1/P2/P3]
- 🔒 Blocked: [items waiting on something external]

## Needs CEO input
- [questions or decisions that require a Cowork session]

## Recent sessions (rolling 5)
- YYYY-MM-DD · [agent label]: [one-line summary]

## Next actions
1. [specific next step]
```

### `agents/BRIEF.md` (500-line max)

```markdown
# agents/BRIEF.md — Project Decisions
> What we're building and why. Append-only. New version block per change.

---

## v1.0 — YYYY-MM-DD · Cowork

### What we're building
[One paragraph]

### Tech stack — chosen
| Technology | Why |
|------------|-----|

### Tech stack — rejected
| Technology | Why rejected |
|------------|--------------|

### Architecture decisions
1. [Decision]

### Scope — in / out
**In:** ...
**Out:** ...

### Open questions
1. [Question]
```

### `agents/ROADMAP.md`

```markdown
# agents/ROADMAP.md — Direction & Phases
> Owner: Vish + Cowork (joint). Agents execute against this; do not edit unless authorized.

## Direction
[One paragraph — what we're going toward]

## Out of scope
[Explicit refusals]

## Phases / Acts
### Act 1 — [Name]
[Goal · output · done criteria · status]
```

### `agents/WORKLOG.md`, `agents/CHANGELOG.md`

Same as cowork's templates but with "project" framing.

### `agents/BRAND.md`, `agents/FUNDAMENTALS.md`, `agents/DESIGN.md`, `agents/DISCOVERIES.md`

See `phase-4-design-system.md` — created in Phase 4.

## 3e. human/ files

### `human/agenda.md`

```markdown
# Agenda

> Open this. Find the next un-ticked chapter. Open the tool. Do the work. Tick. Move on.

## How to use
(empty — populated as the project unfolds)

## ✓ Done
(none yet)
```

## 3f. Apply Phase 2 merge decisions

For every file in the Phase 2 decision table:
- **Merge** → write the extracted content into the destination protocol file
- **Reference** → add one line to root CLAUDE.md `## Reference files`
- **Leave** / **Skip** → no action

## 3g. Verify

```bash
ls -la
ls cowork/
ls agents/
ls human/
```

Confirm all four tiers exist with expected files. Specifically check:
- `CLAUDE.md` — root (always-loaded brain)
- `README.md` — root (file catalog + cascade rules)
- `agents/SITUATIONS.md` — situation router (linked from root CLAUDE.md)
- `agents/TOOLING.md` — if Node project (package manager filled in from Phase 4a ask-at-init)
