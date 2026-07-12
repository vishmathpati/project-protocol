# Phase 3 — Create the brain/ structure

Create the root files + the single `brain/` folder + protocol files. Apply Phase 2 merge decisions during template population.

## 3a. Create folders and the plugin-version marker

```bash
mkdir -p brain/docs/detail brain/preview brain/chapters
```

### Write `brain/chapters/README.md`

```markdown
# brain/chapters/ — Delegated-Work Units

One file per chapter, named `NN-name.md` (e.g. `01-auth.md`).

## Lifecycle

1. **CEO** opens a new file, fills in `## Goal` and `## Plan`, then hands it off.  
   (Use the `ceo` skill — it scaffolds the file and delegates to a worktree.)
2. **Worker** executes the work on a branch, then appends `## Completion Report`.  
   (Use the `worker` skill — it defines the exact report format.)
3. **CEO** reads the report and fills in `## CEO Verdict` (approved → merge, or returned → reason).

## Template

Copy `_TEMPLATE.md` when creating a new chapter.
```

### Write `brain/chapters/_TEMPLATE.md`

```markdown
# Chapter NN — <name>

## Goal
<CEO: what this chapter delivers>

**Method:** solo | CEO+worker | CEO+specialists

## Plan
<CEO: approach; how it splits across workers if multi-specialist>

---
<!-- Completion Reports append below — one per worker pass (e.g. backend, then UI, then wire-up). Never overwrite a prior report. -->

<!-- CEO Verdicts append below, one per report verified. -->
```

The canonical **Completion Report** format (workers append one per pass):

```markdown
## Completion Report — YYYY-MM-DD · <author stamp>
**Goal:** … / **Status:** done|partial|blocked / **Changed:** … / **Verified:** … / **Flags:** … / **Commit:** branch · hash
```

The canonical **Verdict** format (CEO appends one per report verified):

```markdown
## Verdict — YYYY-MM-DD · CEO (<author stamp>)
**Decision:** approved | changes requested / **Notes:** …
```

### Write `brain/.plugin-version` marker

Write the current plugin version (read from the plugin manifest) to this one-line file. The `SessionStart` drift-detector hook compares it against the installed plugin version to detect drift.

```bash
# Resolve plugin version from the manifest, then stamp it.
echo "<current-plugin-version>" > brain/.plugin-version
```

On re-init / audit: overwrite with the current version after standards are re-applied.

> There is no `.session-type` marker. The old three-folder layout used it to pick a WORKLOG path. With a single `brain/` folder there is only one WORKLOG (`brain/WORKLOG.md`). Authorship is captured by the **author-stamp** on each entry, not by a marker file.

### Author-stamp at write time

When writing any WORKLOG / BRIEF / CHANGELOG entry, stamp it with the current author detected from the runtime:

- `· Codex` when `CODEX_PLUGIN_ROOT` is set.
- `· Claude Code` when running as Claude Code.
- `· Agent` when the host can't be determined.

A reasonable detection (used only to choose the stamp string — nothing is persisted):

```bash
if [ -n "${CODEX_PLUGIN_ROOT:-}" ]; then
  AUTHOR="Codex"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTHOR="Claude Code"
else
  AUTHOR="Agent"
fi
```

## 3b. Root files

### Root `CLAUDE.md` template

```markdown
# CLAUDE.md — [Project Name]

> Always loaded by every agent. This is the front page / rules index — NOT the brain. The brain is the `brain/` folder; this file points into it. Read top to bottom every session.

## Coding Standards

**1. Think Before Coding** — State assumptions. Surface tradeoffs. Ask when unclear.
**2. Simplicity First** — Minimum code. No speculative features. No unnecessary abstractions.
**3. Surgical Changes** — Touch only what you must. Match existing style.
**4. Verify Before Closing** — Define done before touching code. Screenshot UI changes. Reproduce bugs before fixing.

## Non-negotiable rules

1. Decide before you act. Write it down before you decide.
2. When you change one file, list every other file that becomes stale (see `README.md` cascade rules).
3. Lock-before-cascade: changes hit `brain/BRIEF.md` first, then propagate. Rejected options go in `brain/WONT-DO.md`.
4. Audit before close: independent verification before any chapter is marked done.
5. Commit + push before leaving any chat. Pull main before starting one.
6. One tool active at a time.
7. **If Node project:** read `brain/TOOLING.md` before any package, install, or dev-server work. Never run the wrong package manager — check TOOLING.md for this project's choice.
8. **UI work uses the design system. No hardcoded values, ever.** Before editing any `.tsx` / `.jsx` / `.vue` / `.svelte` / `.swift` / styles file: read `brain/DESIGN.md` for tokens and `brain/FUNDAMENTALS.md` for the Token Rule. Run the `design-check` skill before writing and again after. Raw hex, raw px, raw `font-family` strings, emoji-as-icon, and other cardinal sins from `FUNDAMENTALS.md` in component files are violations — not preferences. If a needed token doesn't exist in `DESIGN.md`: stop and propose adding it. Do not improvise.
9. **UI components — archetype-scoped (see `brain/DESIGN.md` `archetype:`).** For **`dashboard` / `app`** archetypes: shadcn-first when shadcn is in `package.json` — always use the shadcn primitive (`<Button>`, `<Input>`, `<Select>`, `<Dialog>`, `<Popover>`, `<Tooltip>`, `<Sheet>`, `<Drawer>`, `<Tabs>`, `<Accordion>`, `<DropdownMenu>`, `<Command>`, `<Toast>`, `<Alert>`, `<Checkbox>`, `<Radio>`, `<Switch>`, `<Slider>`, `<Textarea>`); never silently fall back to the native element because it's faster to type. For **`marketing` / `content`** archetypes: the *expressive* components (heroes, editorial bands, galleries, scroll sequences) are built **bespoke to the brand** — shadcn and community libraries (Aceternity, Magic UI) are craft *references*, never installed aesthetics; use shadcn only for genuine primitives (form controls, dialogs, menus). Either way — allowed native elements: `<a href>` for navigation, `<button type="submit">` inside a `<form>` when no styled `<Button>` is needed, `<input type="hidden">`. If a needed primitive doesn't exist in shadcn (e.g. date-range picker), stop and ask: build one in `components/ui/` following shadcn conventions, install a community block, or use another library.
10. Use the skill index below. Don't improvise a workflow when a skill exists for it.
11. **Won't-do:** when any idea or option is rejected, append one author-stamped line to `brain/WONT-DO.md` (format: `YYYY-MM-DD · [stamp] — what — why`). Read `brain/WONT-DO.md` before proposing new ideas so nothing is re-litigated.
12. **Change-tracking:** note every change as it happens — one author-stamped WORKLOG line or Completion Report entry per action. No version numbers. Never reconstruct the log at the end of a session.
13. **Research, don't reflect.** When the user asks for an opinion, a recommendation, or expert input, you must (a) research current facts first — search, don't answer from memory — and (b) give an independent, reasoned view with trade-offs and at least one risk they didn't raise. Never end by simply restating the user's own input as the answer. For non-trivial decisions, invoke the `advisor` skill. Present findings in whatever form helps most — table, diagram, chart, HTML, form, artifact — using any available tool.

## Git rules

**Commit format:** `type(scope): summary [ch-NN] · Agent` — Agent is `· Claude Code` or `· Codex` (unknown host → `· Agent`).

**Branches:** CEO works on `main` / the canon branch. Worker branches are named `ch-NN-name` (e.g. `ch-03-auth`).

**Worktree sync is local:** to bring canon into a worktree, run `git merge main` inside the worktree — never push-then-pull through GitHub. GitHub is a backup, not the sync mechanism.

**Push policy:** push at session close (end of chat) or as a manual backup anytime. The CEO↔worker loop does not require a push.

**Write boundary:** workers edit code files and their own chapter file only. The CEO owns the shared canon: `brain/STATUS.md`, `brain/BRIEF.md`, `brain/ROADMAP.md`, `brain/WONT-DO.md`.

Full per-tool procedures: see the `git` skill.

## Skill index — what's available and when to use it

| Skill | When to use it | How to invoke |
|---|---|---|
| `ceo` | Orchestrate a chapter: define goal/plan, delegate to a worktree, verify the worker's report, merge on approval. | `/ceo` · "start a chapter", "define chapter", "delegate work" |
| `worker` | Execute one chapter in a worktree, write the Completion Report, commit on its branch. | `/worker` · "work on chapter", "execute chapter" |
| `solo` | Plan and do small self-contained work in a single session, skipping the CEO/worker handoff. | `/solo` · "solo session", "quick task", "do it myself" |
| `add-context` | Adding a deep-reference doc (integration, API, design notes) to the project. | `/add-context` · "add context", "add context file" |
| `audit` | Periodic consistency check across all canon files to surface drift. | `/audit` · "run audit", "check canon consistency" |
| `audit-before-close` | Verification gate before marking any chapter, task, or feature complete. | `/audit-before-close` · "audit before close", before any chapter close |
| `build-component` | Building a new UI component or adopting an external one into the design system. | `/build-component` · "build component", "new component", "create component" |
| `build-page` | Composing a whole page (marketing or dashboard) through an iterative conversation. | `/build-page` · "build the homepage", "build the X page", "compose page X" |
| `design-check` | Pre- and post-write gate for any UI file edit — checks tokens, reuse, and cardinal sins. | `/design-check` · "edit UI", "change styles", "add page", any visual change |
| `design-direction` | Deep brand diagnostic: extracts taste axes, proposes 3 named directions + moodboard. | `/design-direction` · "design direction", "set up the design system", "re-anchor brand" |
| `calibrate` | Capture an annotated moodboard + follow/deviate/refuse conventions audit — the bridge inside design-direction, before the three directions. | `/calibrate` · "build the moodboard", "annotate references", "conventions audit" |
| `discipline` | Pre-action gate before any non-trivial change — forces pause, declares cascades, verifies canon. | `/discipline` · "before I do this", "I'm about to edit Y" |
| `discussion-mode` | No-edit conversation mode — prevents file edits during thinking or planning. | `/discussion-mode` · "discuss", "let's talk", "brainstorm", "explore" |
| `git` | Commit/branch conventions, local worktree sync, push policy. | model-invoked |
| `grill` | Relentless interview to sharpen a chapter's goal or feature intent before building. | model-invoked |
| `bug-fixing` | Repro-first bug discipline: reliable red/green reproduction, ranked hypotheses, fix, regression test. | model-invoked |
| `handoff` | Write a Carry-over note into the active chapter when a session fills up, so the next session continues cleanly. | model-invoked |
| `init-project` | Initialize or re-initialize a project with the brain/ protocol. | `/init-project` · "init project", "bootstrap project" |
| `marketing-brief` | Deep marketing-site brief that writes canonical `brain/marketing/` files consumed by build-page. | `/marketing-brief` · "marketing brief", "write marketing site", "build marketing copy" |
| `migrate-to-brain` | Convert an OLD three-folder or flat-root project to the single `brain/` layout. | `/migrate-to-brain` · "migrate to brain", "consolidate folders" |
| `migrate-project` | Apply version-by-version plugin deltas to bring a project up to the current plugin version. | `/migrate-project` · "migrate project", "update plugin files" |
| `save-session` | Save and close a project session — updates WORKLOG → CHANGELOG, STATUS, BRIEF. | `/save-session` · "save", "save session", "close session", "done for today" |
| `session-recap` | Mid-session snapshot — reads WORKLOG + STATUS and reports current state. | `/session-recap` · "recap", "where are we", "what have we done", "catch me up" |
| `advisor` | Expert research + recommendation — researches before opining, forms an independent view, never just reflects. | model-invoked |
| `verify-by-reading` | Read-before-answer enforcement — opens actual files before answering questions about content. | `/verify-by-reading` · "what does X say", "is Y implemented", before answering any file-content question |
| `test-driven-development` | Implementing a feature or bugfix test-first — RED-GREEN-REFACTOR cycle. | model-invoked |

## Hooks index — what runs automatically

| Hook event | What it does | What to do when it warns |
|---|---|---|
| `SessionStart` | Injects orient reminder: read CLAUDE.md + brain/STATUS.md before touching code, run save-session before closing. | Follow it. Read CLAUDE.md and brain/STATUS.md now if you haven't. |
| `UserPromptSubmit` | Reminds to classify the task (NEW / ADDITION / UI CHANGE / BUG FIX) and append to brain/WORKLOG.md after each action. | Classify before acting. Append a WORKLOG entry (author-stamped) after each change. |
| `PreToolUse Edit\|Write` | Checks if brain/WORKLOG.md is in cleared state; warns if so (means no entry logged yet this session). | Append a WORKLOG entry for the change you're about to make. |
| `PreCompact` | Backs up brain/WORKLOG.md before compaction so content survives context trim. | No action needed — informational. Content is preserved in backup. |
| `PostCompact` | Re-injects orient reminder after compaction. | Re-read CLAUDE.md and brain/STATUS.md to re-orient before continuing. |
| `SubagentStart` | Appends a `subagent_start` timestamp to brain/WORKLOG.md. | No action needed — automatic bookkeeping. |
| `SubagentStop` | Appends a `subagent_stop` timestamp to brain/WORKLOG.md. | No action needed — automatic bookkeeping. |
| `Stop` | Checks brain/WORKLOG.md for unsaved work; warns with line count if save-session hasn't run. | Run `/save-session` before closing the chat. |
| `PostToolUse Edit\|Write` (design-scan) | After any UI file write, greps content for raw hex, raw px, raw font-family, native elements when shadcn exists, banned patterns. | Fix each flagged violation before continuing. Violations are not preferences. |
| `PostToolUse Edit\|Write` (design-check dispatcher) | After writing to a component-tier path, instructs agent to run `/design-check` on the file. | Run `/design-check` on the written file immediately. |
| `SessionStart` (drift-detector) | Detects plugin-version drift by comparing `brain/.plugin-version` to current plugin version. | Run `/migrate-project` when prompted to apply pending deltas. |

## Situation router — common requests → which skill

See `brain/SITUATIONS.md` for the full routing table.

## Folder map

- `brain/` — the single canon folder. Every agent reads here. Every protocol file (STATUS, BRIEF, ROADMAP, WORKLOG, CHANGELOG, agenda, design system, docs) lives here, once.
- `brain/chapters/` — one file per unit of delegated work (CEO goal + worker report + verdict).

## Pre-task classification (mandatory before any code change)

1. NEW standalone feature
2. ADDITION to existing feature
3. UI CHANGE
4. BUG FIX

Check `brain/docs/INDEX.md` dependency entries before classifying.

## Extended Context

<!-- add-context appends here -->
```

### Root `README.md` template

```markdown
# README.md — File Map & Dependencies

> Open this whenever you're about to change a non-trivial file. Find that file below. Its "When this changes" line tells you which other files need updating.

## File catalog

### Root
- **CLAUDE.md** — always-loaded front page / rules index. Points into `brain/`.
- **README.md** — this file. Open before any non-trivial edit.

### `brain/`
- **.plugin-version** — plugin-version marker. Read by the drift-detector hook; bumped by migrate-project / modernize.
- **STATUS.md** — current project state. No cascade.
- **BRIEF.md** — project decisions (WHAT we build). Author-stamped per version block. When this changes: `brain/ROADMAP.md` may need updating, `brain/STATUS.md` Next Actions may need updating, `brain/agenda.md` may need re-derivation.
- **WONT-DO.md** — running list of rejected decisions, each with a one-line reason. No cascade.
- **ROADMAP.md** — phases and ordering. When this changes: `brain/STATUS.md` Next Actions update, `brain/agenda.md` re-derive.
- **WORKLOG.md** — real-time, author-stamped per entry. Cleared by save-session.
- **CHANGELOG.md** — project history, author-stamped. Never cleared.
- **agenda.md** — daily steering file. When `brain/ROADMAP.md` or `brain/BRIEF.md` change: re-derive.
- **BRAND.md** — product identity. When this changes: `brain/DESIGN.md` may need updating.
- **FUNDAMENTALS.md** — global design framework. Never edited per project.
- **TOOLING.md** — Node tooling convention for this project (package manager, lockfile, Node version). When this changes: refreshed from plugin template with chosen package manager, not by hand.
- **DESIGN.md** — project tokens (+ `archetype:`, `motion:`, `icon:`). When this changes: pending UI work pauses until tokens validate.
- **TASTE.md** — learned-preferences ledger (confidence-scored). Fed by `save-session`; read by `build-page` / `design-check` so high-confidence preferences apply before the user re-asks. No cascade.
- **STRUCTURE.md** — codebase surface map. When this changes: build-component / design-check read the new surfaces.
- **DISCOVERIES.md** — append-only UI patterns. No cascade.
- **SITUATIONS.md** — situation router (linked from root CLAUDE.md).
- **docs/INDEX.md** — feature dependency map. Source for cross-feature lookups.
- **docs/detail/** — deep reference. When changed: relevant feature contracts may need re-reading.
- **preview/** — design-direction preview HTML files. Gitignored. Garbage-collected by `audit` (keeps most recent 2 per direction-slug).
- **marketing/** — marketing-brief output (CONTENT registry, sitemap, per-page briefs/copy, media manifest). Consumed by build-page.
- **chapters/** — one file per unit of delegated work (CEO goal + worker report + verdict).

## Cascade summary (rule of thumb)

```
brain/BRIEF.md → brain/ROADMAP.md → brain/STATUS.md → brain/agenda.md
```

If you change anything upstream, check everything downstream.
```

### `brain/SITUATIONS.md` template

```markdown
# brain/SITUATIONS.md — Situation Router

> When the user says or you're about to do X, use skill Y and read Z first.
> This is the full routing table; root CLAUDE.md points here.

| If the user says or you're about to do X | Use skill | Read first |
|---|---|---|
| Starting a new unit of work — need to define goal, plan, and delegate to a worktree | `ceo` | `brain/ROADMAP.md`, `brain/BRIEF.md` |
| Picked up a chapter to execute in a worktree — need to do the work and write a report | `worker` | the chapter file in `brain/chapters/` |
| Quick self-contained task — no delegation needed, doing it all in one session | `solo` | `brain/BRIEF.md`, `brain/STATUS.md` |
| Any UI work — editing a component, page, or styles file | `design-check` | `brain/DESIGN.md`, `brain/FUNDAMENTALS.md` |
| Design feels wrong / palette off / looks too generic | `design-direction` | `brain/BRAND.md` |
| Raw hex / px / font-family values found in a component | `design-check` | `brain/FUNDAMENTALS.md` (Token Rule section) |
| Want to commit, update WORKLOG, and close the session | `save-session` | `brain/STATUS.md` |
| Committing, branching, syncing a worktree, or pushing — need git conventions | `git` | `brain/STATUS.md` (for branch context) |
| Setting up a brand new project or re-initializing | `init-project` | nothing (this is the entry point) |
| Converting an old three-folder / flat-root project to the brain layout | `migrate-to-brain` | nothing (the migration entry point) |
| Migrating an existing project to the current plugin version | `migrate-project` | `brain/.plugin-version` |
| About to edit something non-trivial — risky or cascading | `discipline` | `README.md` (cascade rules) |
| Want a recap of where the project stands right now | `session-recap` | nothing (reads WORKLOG + STATUS itself) |
| Writing a feature spec or locking a product decision | `discipline` then `brain/BRIEF.md` append | `brain/BRIEF.md`, `brain/ROADMAP.md` |
| Rejecting an option / killing an idea | append to `brain/WONT-DO.md` | `brain/BRIEF.md` |
| A chapter's goal feels fuzzy or the scope is unclear before work starts | `grill` | the chapter file in `brain/chapters/` |
| Investigating or fixing a bug | `bug-fixing` | `brain/STATUS.md` (for known bugs) |
| Implementing a feature or bugfix test-first (TDD / red-green-refactor) | `test-driven-development` | the chapter file or task description |
| Session is filling up and work isn't done — need to preserve state for the next session | `handoff` | the active chapter file in `brain/chapters/` |
| Running a full marketing site build | `marketing-brief` then `build-page` | `brain/BRIEF.md`, `brain/BRAND.md` |
| Writing or composing a full page (marketing or dashboard) | `build-page` | `brain/marketing/briefs/<slug>.md`, `brain/DESIGN.md` |
| Building a UI component or adopting one from an external source | `build-component` | `brain/STRUCTURE.md`, `brain/DESIGN.md` |
| Adding a long reference doc (API spec, integration notes) | `add-context` | `brain/docs/INDEX.md` |
| About to mark a feature, chapter, or task as done | `audit-before-close` | the relevant spec or contract file |
| Need to verify what a file actually says (not memory) | `verify-by-reading` | the file in question |
| User asks for an opinion, recommendation, or expert input on a non-trivial decision | `advisor` | nothing (advisor researches first) |
```

## 3c. brain/ protocol files

### `brain/STATUS.md` (60-line max, fixed schema)

```markdown
# brain/STATUS.md
> Last updated: YYYY-MM-DD · [Claude Code | Codex | Agent]

## Current sprint
[One-paragraph context]

## Health
- ✅ Working: [confirmed working features]
- 🔴 Broken: [known bugs P1/P2/P3]
- 🔒 Blocked: [items waiting on something external]

## Needs human input
- [questions or decisions that require a human session]

## Recent sessions (rolling 5)
- YYYY-MM-DD · [Claude Code | Codex | Agent]: [one-line summary]

## Next actions
1. [specific next step]
```

### `brain/BRIEF.md` (500-line max)

```markdown
# brain/BRIEF.md — Project Decisions
> What we're building and why. Append-only. New version block per change.
> Every version block is stamped with its author: · Claude Code, · Codex, or · Agent.

---

## v1.0 — YYYY-MM-DD · [Claude Code | Codex | Agent]

### What we're building
[One paragraph]

### Tech stack — chosen
| Technology | Why |
|------------|-----|

### Architecture decisions
1. [Decision]

### Scope — in / out
**In:** ...
**Out:** ...

### Open questions
1. [Question]
```

> Rejected technologies and killed options no longer live in BRIEF.md. Put them in `brain/WONT-DO.md` with a one-line reason, so BRIEF.md stays a record of what we ARE doing.

### `brain/WONT-DO.md`

```markdown
# brain/WONT-DO.md — Rejected Decisions
> A running list of things we deliberately decided NOT to do, each with a one-line reason.
> Append-only. When you reject an option during any session, add it here instead of burying it in chat.
> Format: YYYY-MM-DD · [Claude Code | Codex | Agent] — what we rejected — one-line reason.

## Log
(none yet — add a line each time an option is killed)
```

### `brain/ROADMAP.md`

```markdown
# brain/ROADMAP.md — Direction & Phases
> Owner: the human + the CEO session (joint). Workers execute against this; do not edit unless authorized.

## Direction
[One paragraph — what we're going toward]

## Out of scope
[Explicit refusals — mirror to brain/WONT-DO.md when a refusal is a decision]

## Phases / Acts
### Act 1 — [Name]
[Goal · output · done criteria · status]
```

### `brain/WORKLOG.md`

```markdown
# brain/WORKLOG.md — Real-time work log
> Real-time log. Cleared by save-session. Every entry is author-stamped.
> Format per entry: YYYY-MM-DD HH:MM · [Claude Code | Codex | Agent] — what was done.

> WORKLOG cleared — last session closed cleanly.
```

### `brain/CHANGELOG.md`

```markdown
# brain/CHANGELOG.md — Project history
> Project history. Never cleared. Keep a Changelog format. Every entry is author-stamped.
> Each dated block notes who wrote it: · Claude Code, · Codex, or · Agent.

## [Unreleased]
```

### `brain/agenda.md`

```markdown
# Agenda

> Open this. Find the next un-ticked chapter. Open the tool. Do the work. Tick. Move on.

## How to use
(empty — populated as the project unfolds)

## ✓ Done
(none yet)
```

## 3d. Design-system & docs files

- `brain/BRAND.md`, `brain/FUNDAMENTALS.md`, `brain/DESIGN.md`, `brain/DISCOVERIES.md` — created in Phase 4 (see `phase-4-design-system.md`).
- `brain/STRUCTURE.md` — created on first `build-component` run, OR during Phase 0c modernize, OR during Phase 4 if the user opts in.
- `brain/TOOLING.md` — Node projects only; rendered in Phase 4a.
- `brain/docs/INDEX.md` and `brain/docs/detail/README.md` — created in Phase 5.

## 3e. Apply Phase 2 merge decisions

For every file in the Phase 2 decision table:
- **Merge** → write the extracted content into the destination protocol file
- **Brain docs** → move into `brain/docs/` and buffer the cross-references for Phase 5
- **Reference** → add one line to root CLAUDE.md `## Reference files`
- **Leave** / **Skip** → no action

## 3f. Verify

```bash
ls -la
ls brain/
ls brain/docs/
```

Confirm the single `brain/` folder exists with expected files. Specifically check:
- `CLAUDE.md` — root (always-loaded front page / rules index)
- `README.md` — root (file catalog + cascade rules)
- `brain/.plugin-version` — version marker present
- `brain/SITUATIONS.md` — situation router (linked from root CLAUDE.md)
- `brain/WONT-DO.md` — rejected-decisions log present
- `brain/TOOLING.md` — if Node project (package manager filled in from Phase 4a ask-at-init)
