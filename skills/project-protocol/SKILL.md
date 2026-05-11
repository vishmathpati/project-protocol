---
name: project-protocol
description: Standard project protocol — file set, session discipline, worklog rules, agent signatures. Read at session start. Triggers — "project start", "init project", "session start", "read protocol".
allowed-tools: Read, Glob, Grep
---

# Project Protocol

Every coding project that uses this plugin follows this protocol. No exceptions.

---

## The File Set

Every project root contains these files:

### `CLAUDE.md` — Agent operating manual (max 300 lines)

**Coding Standards must appear at the top** — they get the most attention in long files.

```markdown
# CLAUDE.md — [Project Name]

## Coding Standards

**1. Think Before Coding** — Don't assume. Don't hide confusion. Surface tradeoffs.
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**2. Simplicity First** — Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked. No abstractions for single-use code.
- No "flexibility" that wasn't requested. No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

**3. Surgical Changes** — Touch only what you must. Clean up only your own mess.
- Don't improve adjacent code, comments, or formatting.
- Match existing style. If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused.
- Every changed line should trace directly to the request.

**4. Verify Before Closing** — Define what "done" looks like before touching code.
- Visual change → screenshot the affected UI and confirm it looks right.
- Bug fix → reproduce it first, then confirm it's gone.
- Feature → state how you'll confirm it works (test, manual check, or screenshot).
- No blanket test requirement — use the right verification method for the task.

---

## What this is
[2–3 sentences]

## Tech stack
[locked choices only]

## What NOT to do
[guardrails]

## Context files
- Read BRAND.md before any work — product identity and what NOT to build.
- Read BRIEF.md at session start — every major decision made in Cowork and why, including rejected options.
- Before any UI work: read FUNDAMENTALS.md + DESIGN.md first.
- No hardcoded visual values. All colors, radii, shadows must use CSS variables from DESIGN.md.
- Show plan before building any new UI component. No code before confirmation.
- **Tailwind v4 projects:** `globals.css` must use `@theme inline { }` — never bare `@theme { }` (dark mode and opacity modifiers silently break without `inline`). Opacity modifiers (`/N`) work only on colors registered in `@theme inline` as `--color-*`. Semantic tokens like `--success` / `--warning` / `--error` use direct arbitrary syntax (`text-[--success]`); pre-compute opacity tints in `:root` using `color-mix(in oklch, var(--success) 15%, transparent)` — never `bg-[--success]/15`.

## Design System Enforcement (mandatory when project has DESIGN.md)

**1. Values from tokens — never hardcoded.**
- Colors → `bg-card` / `text-foreground` / `text-[--success]` — never `bg-zinc-900` or any raw hex/color class
- Radius → `rounded-[--radius-card]` — never `rounded-md` / `rounded-none` by assumption; only if a token is defined that way
- Custom spacing → use named token if defined in DESIGN.md; Tailwind's built-in scale (`p-4`, `gap-6`) is acceptable when no custom token exists
- Fonts, shadows, borders → same rule
- If a token doesn't exist for the value you need: **add it to globals.css first**, then use it. Never hardcode to unblock yourself.

**2. Structure from project primitives.**
If the project has a component library (check CLAUDE.md tech stack — e.g. shadcn/ui):
- Use its primitives — `<Card>`, `<Button>`, `<Badge>` etc. — never replicate their shapes inline with raw div + className
- `<div className="rounded-... border ... bg-card ...">` in a page component = wrong. Use `<Card>`.
- Need a new variant? Add it inside the primitive file, not at the call site.
- Need a new shape that doesn't exist yet? Create a primitive in `components/ui/` first, confirm with user, then use it.

**3. Exceptions require inline documentation.**
Permitted literals: third-party brand colors, external system requirements, canvas/SVG drawing, Next.js metadata.
Every exception must have an inline comment — no silent hardcoding:
`backgroundColor: "#25D366" // WhatsApp brand color — no token replacement possible`

**4. Verify compliance before closing.**
Before claiming any UI change is design-system compliant, grep for the forbidden patterns listed in DESIGN.md §7 (Do's and Don'ts).
Agent summary does not count as verification — only grep output counts.
If non-zero results: fix first, close after.

## Session rules
- Follow the project-protocol plugin skill.
- Read STATUS.md before doing anything each session.
- Read docs/INDEX.md for the feature map and dependency index.
- Run save-session skill before closing every session.
- After every response with a change, bug, or decision — append one line to WORKLOG.md immediately.
```

**Limit:** 300 lines. If CLAUDE.md exceeds this, extract detail into a support file and add a one-line pointer.

---

### `BRAND.md` — Product identity (short, always loaded)

```markdown
# BRAND.md — [Project Name]
> What every agent must know before touching this project.

## Product
- Name:
- Domain:
- One sentence: [what it does]

## User
- Who it's for:
- Problem it solves:
- What it is NOT:

## Personality
- Tone: [e.g. fast and opinionated / calm and professional]
- Values: [e.g. simplicity, speed, privacy]
```

**Rule:** Short — one page max. Updated only on major pivots.

---

### `BRIEF.md` — Distilled decisions (versioned, signed)

The single handoff channel between Cowork, Claude Code, and Codex. Every agent reads it at session start. Every agent that makes a significant decision appends a version block with their signature.

```markdown
# BRIEF.md — [Project Name]
> Distilled from Cowork sessions. The why behind every decision.

---

## v1.0 — YYYY-MM-DD HH:MM · Cowork

### What we're building
[paragraph]

### Tech stack — chosen
| Technology | Why |
|------------|-----|

### Tech stack — rejected
| Technology | Why rejected |
|------------|-------------|

### Architecture decisions
[decisions with reasons]

### Scope — in / out
[explicit scope boundaries]

### Open questions
[unresolved items]

---

## v1.1 — YYYY-MM-DD HH:MM · Claude Code

[only the delta — what changed or was decided this session]
```

**Rules:**
- When decisions change, append a new version block — never overwrite history.
- **500-line limit.** When BRIEF.md reaches 500 lines, create `BRIEF-2.md` and add a pointer at the top of BRIEF.md: `> Continued in BRIEF-2.md`. New version blocks go into BRIEF-2.md from that point.
- Every version block header must include: version number, date+time, and agent label (`· Cowork`, `· Claude Code`, or `· Codex`).

---

### `FUNDAMENTALS.md` — Design principles (same on every project)

The 6-level design framework: Space → Hierarchy → Color Foundation → Typography → Depth → Decoration. Ratio rule. Motion principles. Token rule. Quality questions. Copied from plugin template at init — never modified per project.

**Rule:** Read before any UI work. Do not modify — it is a global standard.

---

### `DESIGN.md` — Project-specific design system (9 sections)

```
1. Visual Theme & Atmosphere
2. Color Palette & Roles (CSS variables)
3. Typography Rules
4. Component Stylings
5. Layout Principles
6. Depth & Elevation
7. Do's and Don'ts
8. Responsive Behavior
9. Agent Prompt Guide (one-paragraph summary for agents — written last)
```

**Rule:** All values as CSS variables — no hardcoded values anywhere in the codebase. When a new token is needed, add it here first, then use it.

**Tailwind v4 projects — add §10 to DESIGN.md and enforce these rules codebase-wide:**

§10. Tailwind v4 Color Integration

These rules are non-negotiable. Violations cause silent dark-mode failures and broken opacity modifiers — the kind that look fine in light mode and completely break in dark.

1. **`@theme inline { }` is required.** Never write bare `@theme { }`. Without `inline`, Tailwind emits vars on `:root` — outside `.dark` scope — so dark mode silently gets light-mode colors. Opacity modifiers (`/80`) also break because `color-mix()` receives an unresolvable var chain. If colors look wrong or everything is monochrome in dark mode: check that globals.css starts with `@theme inline {`, not `@theme {`.

2. **Only `@theme`-registered colors get Tailwind utilities and working opacity modifiers.** Register all shadcn contract colors in `@theme inline` as `--color-*`:
   ```css
   @theme inline {
     --color-background: var(--background);
     --color-foreground: var(--foreground);
     --color-card: var(--card);
     --color-border: var(--border);
     --color-primary: var(--primary);
     --color-muted-foreground: var(--muted-foreground);
     /* etc. */
   }
   ```
   These generate `bg-background`, `text-foreground`, `bg-card`, `border-border` etc. with working `/N` opacity modifiers.

3. **Semantic tokens not in `@theme` (e.g. `--success`, `--warning`, `--error`) must use direct arbitrary syntax.** Use `text-[--success]`, not `text-success`. **Never add `/N` opacity modifiers to these** — `bg-[--success]/15` silently produces nothing in Tailwind v4.

4. **Pre-compute all opacity tints as named CSS vars** (in both `:root` and `.dark`) using `color-mix()`:
   ```css
   --success-bg:     color-mix(in oklch, var(--success) 10%, transparent);
   --success-subtle: color-mix(in oklch, var(--success) 15%, transparent);
   --success-border: color-mix(in oklch, var(--success) 30%, transparent);
   ```
   Then use `bg-[--success-bg]` in components. This replaces `bg-[--success]/10`.

5. **The enforced color chain — no shortcuts:**
   ```
   DESIGN.md spec → globals.css CSS vars → @theme inline → Tailwind class → component
   ```
   Never define a token inside a component file. Never hardcode a hex in a component.

---

### `DISCOVERIES.md` — What actually worked (per project)

```markdown
# DISCOVERIES.md — [Project Name]
> What worked. Updated per session, not per feature.
> Format: [date] · [agent] · [component/pattern] — what worked and why

## Log
(empty — add entries as you build)
```

**Rule:** Append-only. Every entry includes date, agent label, and what worked.

---

### `STATUS.md` — Live pulse (fixed schema, max 60 lines)

```markdown
# Status — [Project Name]
> Last updated: YYYY-MM-DD · Claude Code

## Current Sprint
[3–5 lines — what we're working on right now]

## Health
- ✅ Working: [list confirmed working features]
- 🔴 Broken: [known bugs with severity P1/P2/P3]
- 🔒 Blocked: [items waiting on something external]

## Needs CEO Input
- [questions or decisions that require a Cowork session — leave blank if none]

## Recent Sessions (rolling — keep last 5, drop oldest)
- YYYY-MM-DD · Claude Code: [one-line summary]

## Next Actions
1. [specific next step]
2. [specific next step]
3. [specific next step]
```

**Rule:** Never exceed 60 lines. The "Needs CEO Input" section is how Claude Code escalates back to Cowork.

---

### `ROADMAP.md` — Feature phases and direction

High-level phases. Updated by Cowork when direction changes, by Claude Code when phases complete.

---

### `WORKLOG.md` — Real-time session log (cleared after each session)

Append one line after every response where you changed something, found a bug, made a decision, or tried something that didn't work. Four entry types:

```
[HH:MM] fixed: what was fixed and where
[HH:MM] found_bug: description — file/location — P1/P2/P3
[HH:MM] decided: what was decided and why
[HH:MM] tried_failed: what was attempted and why it didn't work
```

Cleared at session end by save-session. Do not wait until end — write every line immediately after the action that triggered it.

---

### `CHANGELOG.md` — What shipped (never cleared)

Keep a Changelog format. Appended by save-session. Never cleared.

---

## The docs/ Folder

### `docs/INDEX.md` — Project map + agent dependency index

Two sections: Human Map (pages, features, status) + Agent Dependency Index (data model, services, critical functions, feature dependency map, guardrails).

---

## Agent Signatures

Every significant write to BRIEF.md, STATUS.md, DISCOVERIES.md, or CHANGELOG.md must include an agent label so the next agent knows who made what decision.

**Format:**
- BRIEF.md version block header: `## v1.X — YYYY-MM-DD HH:MM · Cowork`
- STATUS.md "Last updated" line: `> Last updated: YYYY-MM-DD · Claude Code`
- DISCOVERIES.md entry: `[YYYY-MM-DD] · Codex · [pattern] — what worked and why`
- CHANGELOG.md section header: `## [YYYY-MM-DD] · Claude Code`

**Agent labels:** `· Cowork` / `· Claude Code` / `· Codex`

---

## Session Start Protocol

At the start of every session:
1. Read `CLAUDE.md` — confirm you know what this project is
2. Read `STATUS.md` — know exactly where things stand; check "Needs CEO Input" section
3. If `BRAND.md` exists: read it — know what this product is and what it is NOT
4. If `BRIEF.md` exists: read it — know what was decided, what was rejected, and why
5. Read `docs/INDEX.md` — understand the feature map and dependency index (if it exists)
6. Before any UI work: read `FUNDAMENTALS.md` + `DESIGN.md`

Do NOT ask Vish what the current state is if STATUS.md exists. Read it.

---

## Pre-task Classification (mandatory before every change)

Before writing a single line of code, classify the work:

1. **NEW standalone feature** → add to docs/INDEX.md Features + create dependency map entry before session ends
2. **ADDITION to existing feature** → read its dependency map entry first, check all `shared with:` items
3. **UI CHANGE** → check Critical Functions/Components in INDEX.md for shared elements
4. **BUG FIX** → identify which feature owns the broken code, read that feature's dependency map

Do not skip classification. It takes 30 seconds and prevents breaking connected things.

---

## Session End Protocol

Before closing any session:
1. Read WORKLOG.md — your real-time log of what happened
2. Verify docs/INDEX.md was updated if any feature/page/function changed
3. Append to `CHANGELOG.md` using WORKLOG entries
4. Update STATUS.md — rolling sessions window, health section, next actions, "Last updated" with agent label
5. If significant decisions were made: append a version block to BRIEF.md with your agent signature
6. If design patterns proved out: append to DISCOVERIES.md with your agent label
7. Clear WORKLOG.md

**Non-negotiable:** A session without an updated STATUS.md and a CHANGELOG entry is incomplete.

---

## Worklog Discipline

After EVERY response where you changed a file, found a bug, made a decision, or tried something that didn't work — append one line to WORKLOG.md immediately, before your next response.

**Why:** The worklog is your real-time memory. At session end, save-session reads it to generate the CHANGELOG. If the worklog is empty, it will be incomplete.

---

## Cowork → Claude Code / Codex Handoff Pattern

After a Cowork session, Cowork writes:
- `CLAUDE.md` — what the project is, tech stack, guardrails (if new project)
- `BRAND.md` — product identity (if new project)
- `BRIEF.md` — first version block with all decisions and why (signed `· Cowork`)

STATUS.md, ROADMAP.md, WORKLOG.md, CHANGELOG.md, docs/, FUNDAMENTALS.md, DESIGN.md, and DISCOVERIES.md are created by Claude Code / Codex via `init-project` at the start of the first coding session.

When returning to Cowork mid-project: Cowork scans all context files first (BRIEF.md, STATUS.md, BRAND.md, DESIGN.md, DISCOVERIES.md) before discussing or suggesting anything. After decisions are made, Cowork appends a new version block to BRIEF.md with its signature, then hands back.

**One agent at a time.** Either Claude Code or Codex is active on a project — never both simultaneously.

---

## Codex Setup (one-time)

Codex reads instruction files from each project directory. To make Codex read `CLAUDE.md` automatically (same as Claude Code), add one line to `~/.codex/config.toml`:

```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

This is a one-time global setup. After this, every project with a `CLAUDE.md` is automatically Codex-compatible — no per-project AGENTS.md needed.

---

## gbrain MCP Integration

When gbrain MCP is connected:
- Use `gbrain get <project-slug>/<file>` for direct lookup
- Use `gbrain query "<question>"` for discovery
- Never use gbrain for session initialization — read files directly
- Mid-session knowledge gap → call gbrain silently, continue. Do NOT ask Vish unless it's a decision.

---

## What Goes Where

| Content | File |
|---------|------|
| What this project is + session rules | `CLAUDE.md` |
| Product identity, audience, what NOT to build | `BRAND.md` |
| All decisions made + reasons, versioned + signed | `BRIEF.md` |
| Design principles (6 levels) — global standard | `FUNDAMENTALS.md` |
| Project-specific tokens, colors, typography, do's/don'ts | `DESIGN.md` |
| What worked — non-obvious patterns worth keeping | `DISCOVERIES.md` |
| Current state + bugs + next actions + CEO escalation | `STATUS.md` |
| Feature phases + big picture | `ROADMAP.md` |
| Real-time session events | `WORKLOG.md` (cleared each session) |
| What shipped (product history) | `CHANGELOG.md` (never cleared) |
| Human feature map + agent dependency index | `docs/INDEX.md` |
| Complex feature deep-dives | `docs/detail/feature.md` (only when needed) |
