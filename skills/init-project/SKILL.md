---
name: init-project
description: >
  Initialize or audit a project with the Arel OS protocol. Scans ALL markdown
  files in the project, asks what to do with each one, and merges everything
  into a unified protocol so no existing documentation is lost or duplicated.
  Also generates docs/INDEX.md by analyzing the codebase, and creates CHANGELOG.md.
  Triggers: "init project", "bootstrap this project", "set up protocol files",
  "create protocol files", "initialize protocol", or when starting work in any
  project directory inside ~/Arel OS/Projects/active/ that has no CLAUDE.md or STATUS.md.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*,ls:*,find:*,cat:*,cp:*), AskUserQuestion, Task
---

# Init Project

Initialize or audit the current project. Goal: ONE unified system — not two parallel systems running side by side. Every file gets acknowledged. Every protocol file gets created or updated. The docs/ folder gets generated from real codebase analysis.

---

## Sub-agent Model Routing

This skill involves two types of work with different intelligence requirements.
Use the Task tool to delegate appropriately — do NOT do heavy file analysis inline (it fills your context).

| Task | Intelligence level | Why |
|------|-------------------|-----|
| Scanning route/page files, extracting names | fast (extraction) | Pure extraction, no reasoning needed |
| Scanning .env.example, listing service keys | fast (extraction) | Pattern matching |
| Scanning package.json for stack and services | fast (extraction) | Structured read |
| Finding all exported functions used in multiple files | capable (reasoning) | Requires import graph analysis |
| Identifying which features share which functions | capable (reasoning) | Requires reasoning about relationships |
| Writing Section 1 of INDEX.md (human map) | capable (reasoning) | Requires judgment about what matters |
| Writing Section 2 of INDEX.md (agent index) | capable (reasoning) | Requires understanding dependencies |
| Writing CLAUDE.md from merged content | capable (reasoning) | Requires synthesis |
| Categorizing WORKLOG entries for CHANGELOG | fast (extraction) | Simple classification |
| Generating DESIGN.md from BRAND.md + stack | capable (reasoning) | Requires judgment about design tokens |

**Rule:** Use a fast/cheap model for extraction tasks. Use a capable reasoning model for judgment tasks. Never use the most expensive model for any init-project task.

To spawn a sub-agent: use the Task tool with a clear, self-contained prompt.
Example: `Task(prompt="Scan src/app/ for all route files. List every route path and its filename. Output as a plain list, one per line.")`

---

## Phase 1 — Full Discovery

### 1a. Find all markdown files

Use Glob to find every `.md` file in the project, excluding:
- `node_modules/`, `.git/`, `vendor/`, `dist/`, `build/`

Separate into two buckets:

**Protocol files** (handle in Phase 3):
- `CLAUDE.md`, `STATUS.md`, `ROADMAP.md`, `WORKLOG.md`, `CHANGELOG.md`

**Design system files** (handle in Phase 3.5):
- `BRAND.md`, `BRIEF.md`, `FUNDAMENTALS.md`, `DESIGN.md`, `DISCOVERIES.md`

**Other markdown files** (handle in Phase 2):
- `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `NOTES.md`, files in `docs/`, etc.

### 1b. Read and summarize each non-protocol markdown file

For every file in the "other" bucket, read and write a one-line summary.

Example summary table:
```
README.md         — project overview, setup instructions, feature list
ARCHITECTURE.md   — system design, component diagram, data flow
CHANGELOG.md      — version history, 24 entries going back to 2024-01
docs/API.md       — REST endpoint reference, 15 endpoints documented
NOTES.md          — miscellaneous scratch notes, mostly outdated
```

---

## Phase 2 — Ask About Each Non-Protocol File

Present the summary table. For each file, ask what to do using AskUserQuestion.

**Options:**
- **Merge** — extract content into a protocol file
- **Reference** — add a one-line pointer in CLAUDE.md; leave file untouched
- **Leave** — no changes, no reference added
- **Skip** — stale/generated, ignore entirely

### Merge destination mapping

| File type | Merge destination |
|-----------|------------------|
| README.md — project overview | "What this is" in `CLAUDE.md` |
| README.md — setup/install | `CLAUDE.md` Tech stack section |
| CONTRIBUTING.md — coding rules | `CLAUDE.md` Coding Standards |
| ARCHITECTURE.md, DESIGN.md | Reference in `CLAUDE.md` (too large to merge) |
| CHANGELOG.md, HISTORY.md | Extract recent decisions → new version block in `BRIEF.md` |
| TODO.md, TASKS.md | Extract open items → `STATUS.md` Next Actions |
| docs/*.md API/reference | Reference in `CLAUDE.md` |
| Any file > 100 lines | Reference, don't merge |

**Rule:** When in doubt, reference rather than merge.

---

## Phase 3 — Handle Protocol Files

### CLAUDE.md
If exists: read it, show what's in it, ask "Keep / Replace / Merge instructions?"
If missing: create from template.
Coding Standards section must be at the TOP regardless.
Add "Reference" pointers from Phase 2 results.
Add "Context files" section pointing to BRAND.md and BRIEF.md.
Limit: 300 lines.

### CLAUDE.md template
```markdown
# CLAUDE.md — [Project Name]

## Coding Standards

**1. Think Before Coding** — Don't assume. Don't hide confusion. Surface tradeoffs.
**2. Simplicity First** — Minimum code that solves the problem. Nothing speculative.
**3. Surgical Changes** — Touch only what you must. Match existing style.
**4. Verify Before Closing** — Define what "done" looks like before touching code.

---

## What this is
[from README.md or user-provided description]

## Tech stack
[from package.json / README.md]

## What NOT to do
[guardrails]

## Context files
- Read BRAND.md before any work — product identity and what NOT to build.
- Read BRIEF.md at session start — every major decision made in Cowork and why, including rejected options.
- Before any UI work: read FUNDAMENTALS.md + DESIGN.md first.
- No hardcoded visual values. All colors, radii, shadows must use CSS variables from DESIGN.md.
- Show plan before building any new UI component. No code before confirmation.

## Reference files
[list any "Reference" files from Phase 2]

## Extended Context
(none yet — add with the add-context skill)

## Session rules
- Follow the project-protocol plugin skill.
- Read STATUS.md before doing anything each session.
- Read docs/INDEX.md for the feature map and dependency index.
- Update STATUS.md and write a session file before closing every session.
- After every response with a change, bug, or decision — append one line to WORKLOG.md immediately.
```

### STATUS.md, ROADMAP.md, WORKLOG.md
Same behavior: create if missing, keep if exists and current, flag if stale.

For STATUS.md, use this template (note the "Needs CEO Input" section):

```markdown
# Status — [Project Name]
> Last updated: YYYY-MM-DD · Claude Code

## Current Sprint
[fill in]

## Health
- ✅ Working:
- 🔴 Broken:
- 🔒 Blocked:

## Needs CEO Input
(none)

## Recent Sessions (rolling — keep last 5)
- YYYY-MM-DD · Claude Code: init-project run

## Next Actions
1. Fill in BRAND.md — product identity fields
2. Fill in BRIEF.md — after first Cowork session
3. Verify docs/INDEX.md — check [VERIFY] items
4. Review DESIGN.md — verify color tokens
```

### CHANGELOG.md
If missing, create:
```markdown
# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---
```
If exists: leave as-is. CHANGELOG.md is never overwritten.

---

## Phase 3.5 — Design System Files

These five files form the design context layer. They prevent agents from making visual decisions without grounding. Create them after the protocol files are handled.

Never silently overwrite any existing file. Always read first, always ask before replacing.

---

### BRAND.md

**If exists:** Read it. Use as context for DESIGN.md generation. Do not overwrite.

**If missing:** First, silently scan the codebase for brand signals (spawn a Haiku sub-agent):
- `README.md` — product name, description, tagline, who it's for
- `package.json` — `name` and `description` fields
- `index.html` or `layout.tsx` / `layout.js` — `<title>`, `<meta name="description">`, Open Graph tags
- Any landing page copy (`page.tsx`, `index.tsx`, `Home` component)
- Any `about`, `hero`, or marketing section text in components

After scanning, present what was found and ask via AskUserQuestion:

```
Here's what I found about this product from the codebase:
- Name: [detected or "not found"]
- What it does: [detected or "not found"]
- Who it's for: [detected or "not found"]

How would you like to create BRAND.md?

A — Auto-generate from what I found (I'll show it to you first for confirmation)
B — I'll answer 3 quick questions instead
C — Skip for now (blank stub)

Or type your own description and I'll build it from that.
```

**If A (auto-generate):** Generate BRAND.md from the scanned signals, show the draft, ask "Does this look right? Anything to change?" Apply corrections and write the file.

**If B (questions):** Ask one at a time:
1. "What is this product in one sentence? Who is it for?"
2. "What is the personality/tone? (e.g. fast and opinionated / calm and professional / premium and cinematic)"
3. "What is it NOT? What should agents never build into this?"
Build from answers.

**If C (skip):** Create blank stub, move on.

**If custom text typed:** Build BRAND.md from what the user described.

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

**Rule:** One page max. Mark any auto-detected fields with [VERIFY] so the user knows to confirm them. Never silently write values you're uncertain about.

---

### BRIEF.md

**If exists:** Read it. Use as context for DESIGN.md generation. Do not overwrite — it's a versioned human record.
**If missing:** Tell the user explicitly: "BRIEF.md doesn't exist yet. I'll create the stub — but any important decisions we make during this init session should be added there by you afterward. I'll remind you at the end with a list of what's worth capturing."

Create the stub:

```markdown
# BRIEF.md — [Project Name]
> Distilled from Cowork sessions. The why behind every decision.
> 500-line limit — when reached, create BRIEF-2.md and add pointer here.

---

## v1.0 — YYYY-MM-DD HH:MM · Cowork

### What we're building
[fill in — one paragraph]

### Tech stack — chosen
| Technology | Why |
|------------|-----|

### Tech stack — rejected
| Technology | Why rejected |
|------------|-------------|

### Architecture decisions
[fill in after first Cowork session]

### Scope — in / out
[fill in]

### Open questions
[fill in]
```

**Rules:**
- When decisions change, append a new version block — never overwrite history.
- Every block header: `## vX.Y — YYYY-MM-DD HH:MM · [Agent]` where agent is `· Cowork`, `· Claude Code`, or `· Codex`.
- At the end of Phase 3.5, collect any significant decisions made during init and tell the user: "Here's what's worth adding to BRIEF.md: [list]." Don't write it yourself — surface it, let the user decide.

---

### FUNDAMENTALS.md

**Always:** Write FUNDAMENTALS.md with the standard content below. This is a fixed global standard — same content on every project.

Use the Write tool to create `./FUNDAMENTALS.md` with exactly this content:

```markdown
# FUNDAMENTALS.md — Design Principles
> Global. Read before any UI work. Same content on every project.

---

## The 6 Levels (in order of importance)

Build in this order. Do not skip levels.

### Level 1 — Space

Consistent spacing is more important than any color, gradient, or animation.
Use a scale based on multiples of 4px: 4, 8, 12, 16, 24, 32, 48, 64.
Never mix arbitrary values. Random gaps make UIs feel amateurish even when the colors are good.

### Level 2 — Hierarchy

Every screen must answer: what do I look at first? Second? Third?
Hierarchy is created through size, weight, and color contrast — nothing else.
If everything is the same visual weight, the eye has nowhere to go.

### Level 3 — Color Foundation

For dark UIs, you need at least 4 distinct dark values:
- Page background (darkest)
- Card background (slightly lighter)
- Elevated card / hover state (slightly lighter again)
- Border (just barely visible)

Do not use the same dark value everywhere. Depth comes from these separations.
Accent/brand color is separate from these foundation levels.

### Level 4 — Typography

One font family. Two weights (regular + medium, or medium + semibold).
Maximum 5 size steps. Consistent line-height throughout.
Typography problems make everything else look worse — fix them early.

### Level 5 — Depth and Elevation

Use shadows, borders, or background-lightness to show z-axis hierarchy:
background → cards → elevated cards → modals → tooltips.
Elements should feel like they exist on different layers, not a flat plane.

### Level 6 — Decoration (last, earned, rare)

Gradients, glows, animations, blur effects, grain textures.
Only add decoration after Levels 1–5 are solid.
Decoration amplifies whatever is underneath — good foundation + decoration = premium, weak foundation + decoration = noise.

---

## The Ratio Rule

90% of the screen should be plain. 10% can have decoration.
Decoration earns its impact by being rare. One gradient in a sea of plain = striking. Gradients everywhere = wallpaper.
Vercel, Linear, and every premium product follow this ratio intentionally. Their plain moments create contrast for the moments that aren't.

---

## Motion Principles

1. **Purpose-driven only** — animation informs, it does not decorate
2. **Ease-out** for entering elements (feels like they arrived from somewhere)
3. **Ease-in** for exiting elements (feels like they're leaving)
4. **150–300ms** for most interactions (faster = snappy, slower = sluggish)

---

## The Token Rule

Every visual value must have a name. No exceptions.

```css
/* WRONG — hardcoded, invisible to your design system */
background: #1a1a1a;
border-radius: 12px;

/* CORRECT — named, inheritable, changeable in one place */
background: var(--card);
border-radius: var(--radius);
```

When you see a component you want to add:
1. Does it use CSS variables or hardcoded values?
2. If CSS variables → import it, it inherits your tokens automatically. Nothing to do.
3. If hardcoded → find the 2–3 hardcoded values, replace with your tokens. Five minutes.

### The 3 types of "different" (when adding a component you like)

- **Type 1 — Token difference**: component uses tokens, your values differ → your tokens override automatically
- **Type 2 — Missing token**: gradient, glow, blur not in your token set → add it as a new named token, now it's inside your system
- **Type 3 — Structural intention**: sharp corners vs rounded — decide once: update your whole token, or document as a named exception with a reason

---

## Quality Questions (ask before finishing any UI work)

1. **Does this decoration earn its place?** Is it rare enough to have impact?
2. **Is the visual hierarchy immediately clear?** Can someone tell in 2 seconds what's most important?

If either answer is no, fix the foundation before adding more.
```

If FUNDAMENTALS.md already exists: overwrite it silently. This file is never project-specific — it is a global standard that must stay in sync with this plugin version. No need to ask.

**Rule:** Do not modify FUNDAMENTALS.md per project. Never use `${CLAUDE_PLUGIN_ROOT}` paths or file copy commands — the content is embedded above for maximum portability across all agents.

---

### DESIGN.md

This is the most important file in Phase 3.5. The decision process here must be open — never force the user into two options.

DESIGN.md follows the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec: YAML frontmatter for machine-readable tokens + markdown body for human rationale. Agents read both layers — exact values from the YAML, context from the prose.

**Step 1 — Detect existing design tokens and format**

Check for an existing DESIGN.md first:
- If it exists: read it and check whether it has YAML frontmatter (starts with `---` and contains a `colors:` or `name:` key before the first `---` close)
- If DESIGN.md has frontmatter → it is already in the new format. Go to "If DESIGN.md already exists" block.
- If DESIGN.md exists but has NO frontmatter → it is a **legacy format file**. Go to "Legacy upgrade" block.
- If no DESIGN.md → scan for tokens:
  - `src/app/globals.css` or `app/globals.css` — CSS custom properties (`:root { --color: ... }`)
  - `tailwind.config.js` or `tailwind.config.ts` — `theme.extend` color/spacing/typography
  - `src/styles/` or `styles/` — any theme or token file
  - `tokens.css`, `design-tokens.ts`, `theme.ts`

**Step 2 — Ask the question (open-ended, never locked)**

If existing codebase tokens were found, present what was found and ask via AskUserQuestion:

```
Found design tokens in: [list files]
Here's a sample: [show 5–10 CSS variables or tailwind values]

What would you like to do with DESIGN.md?

A — Transfer existing system as-is (document what's already there, nothing changes visually)
B — Transfer existing + I'll tell you what to add or change on top
C — Generate a completely fresh design system (based on BRAND.md + your direction)

Or type your own direction — e.g. "skip for now", "use existing but make it darker",
"here's the vibe I want: [describe]", "I'll paste the tokens I want"
```

If no tokens were found:

```
No existing design tokens detected.

A — Generate a fresh design system from your product description
B — I'll describe the vibe and you generate from that

Or type your own direction — paste tokens, describe a reference site, say "skip for now", etc.
```

**Step 3 — Execute based on choice**

All paths produce the same output format: YAML frontmatter + 9-section markdown body (see standard below).

**Option A (transfer existing):**
Spawn a Haiku sub-agent to extract all CSS variables and Tailwind config values from the codebase. Then spawn a Sonnet sub-agent to structure them into DESIGN.md format: token values go into YAML frontmatter, prose rationale goes into the 9-section body. Nothing is invented — only what already exists is named and organized.

**Option B (transfer + add):**
Same extraction as A, then ask: "What would you like to add or change? (e.g. 'add gradient tokens for the hero', 'change the primary to violet', 'we need a glow variable')" Apply the additions and generate the complete DESIGN.md.

**Option C / fresh / custom direction:**
Use the context available — in priority order:
1. BRAND.md (if exists and filled) → full context
2. User's typed description → use as design brief
3. Neither exists → ask one more question: "Describe the vibe in a few words. What product is this? What should it feel like?"

Then spawn a Sonnet sub-agent to generate DESIGN.md with both layers from scratch.

**If user typed something custom:** interpret it as best as possible, execute, then confirm: "Here's what I generated — does this match what you had in mind?"

**Step 4 — Lint after writing**

After writing DESIGN.md, always run:
```bash
npx @google/design.md lint DESIGN.md
```

Report findings to the user:
- errors → must fix before closing (broken token references)
- warnings → show and ask if they want to fix now or later (contrast ratio issues, orphaned tokens)
- info → show silently in summary

If the linter is not available (no Node/npx), skip and note: "Linter not available — install `@google/design.md` to validate token references."

**If DESIGN.md already exists (new format with frontmatter):**
Read it first. Then ask via AskUserQuestion:

```
Found existing DESIGN.md (new format). What would you like to do?

A — Keep it as-is (no changes)
B — Keep it but I want to add or update something specific
C — Regenerate it completely

Or type your direction.
```

**Legacy upgrade (DESIGN.md exists but has no YAML frontmatter):**

Tell the user:

```
Found existing DESIGN.md in legacy format (prose-only, no token frontmatter).

The new format adds a YAML frontmatter block at the top with machine-readable token
values — agents get exact hex codes and sizes instead of guessing from prose.
The existing prose sections are kept exactly as-is.

A — Upgrade it now (I'll extract token values from your prose and add frontmatter)
B — Keep legacy format for now (no changes)
```

If A: spawn a Haiku sub-agent to scan the DESIGN.md prose and extract all hex values, px/rem sizes, and font names. Then spawn a Sonnet sub-agent to write the YAML frontmatter block and prepend it to the existing file. Run the linter. Show result.

If B: leave as-is. Note in STATUS.md: "DESIGN.md is legacy format — upgrade with init-project when ready."

---

### DESIGN.md — Standard Format

Every generated or upgraded DESIGN.md must follow this exact structure.

**Layer 1 — YAML frontmatter (machine-readable tokens):**

```yaml
---
version: alpha
name: [Project Name]
colors:
  primary: "#[hex]"        # main brand / interactive color
  secondary: "#[hex]"      # supporting color
  background: "#[hex]"     # page background
  foreground: "#[hex]"     # primary text
  muted: "#[hex]"          # subtle backgrounds, disabled states
  border: "#[hex]"         # dividers, outlines
  # add project-specific tokens: accent, success, warning, error, surface-2, etc.
typography:
  heading:
    fontFamily: [font name]
    fontSize: [e.g. 2rem]
    fontWeight: [e.g. 700]
  body:
    fontFamily: [font name]
    fontSize: [e.g. 1rem]
    fontWeight: [e.g. 400]
  caption:
    fontFamily: [font name]
    fontSize: [e.g. 0.75rem]
rounded:
  sm: [e.g. 4px]
  md: [e.g. 8px]
  lg: [e.g. 16px]
spacing:
  sm: [e.g. 8px]
  md: [e.g. 16px]
  lg: [e.g. 32px]
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.sm}"
  button-secondary:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.sm}"
  card:
    backgroundColor: "{colors.muted}"
    rounded: "{rounded.md}"
  input:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.sm}"
---
```

Rules:
- All color values must be `#` + 6-digit hex (sRGB)
- Component properties must use `{token.reference}` syntax — never hardcode values in components
- Mark uncertain values with `[VERIFY]` comment — e.g. `primary: "#475569"  # [VERIFY]`
- Use `{path.to.token}` references, not string copies — if `colors.primary` changes, all components update automatically

**Layer 2 — Markdown body (human rationale), 9 sections:**

Section headings use `##`. Canonical order:

```
## Overview
One paragraph: overall visual feeling, dark/light, minimal/expressive, emotion it should evoke.
Write so an agent reading it immediately understands what this product looks and feels like.

## Colors
Narrative on the palette — why these colors, what each communicates.
Reference YAML tokens by name: "Primary (#475569) is used for..."
Do not repeat hex values here — they live in the frontmatter.

## Typography
Font choices and rationale. Max 2 font families. Reference typography tokens.
Include line-height and letter-spacing notes for headings vs body.

## Layout
Spacing scale rationale (4px base), max content width, grid system, sidebar dimensions.
Reference spacing tokens.

## Elevation & Depth
How each z-axis layer is created: background → cards → elevated → modals → tooltips.
Gradient and glow tokens if the product calls for them.

## Components
Reference each component token group. Describe hover/active/disabled states.
Format: component-name — description of visual behavior.

## Do's and Don'ts
5–8 specific rules for this project. What to always do, what to never do.
Make these concrete: "Never use raw hex values — always reference a token."

## Responsive Behavior
Breakpoints and what changes at each. Mobile-first or desktop-first decision.

## Agent Prompt Guide
One paragraph FOR Claude agents. Copy-paste this at the top of any UI task prompt.
Written last — summarizes all sections into one dense agent-readable brief.
Include: theme, primary colors (with hex), font, key component behaviors, top 2 rules.
```

Mark uncertain values with [VERIFY]. Generate all 9 sections even if some need [VERIFY] placeholders.

---

### DISCOVERIES.md

**If exists:** Keep as-is. Append-only.
**If missing:** Create stub.

```markdown
# DISCOVERIES.md — [Project Name]
> What worked. Updated per session, not per feature.
> Format: [date] [component/pattern] — what worked and why

## Log
(empty — add entries as you build)
```

**Rule:** Append-only. Never clear or reorganize.

---

### End of Phase 3.5 — BRIEF.md Reminder

If BRIEF.md was missing (stub was just created), output a reminder:

```
📋 BRIEF.md was created as a stub. Here's what's worth adding from this init:
- [Design system choice made: A / B / C / custom — and why]
- [Any stack or architecture decisions surfaced during init]
- [Any scope constraints mentioned]

You fill it in — I won't write BRIEF.md for you. Drop the key decisions in there when you have a moment.
```

This reminder keeps BRIEF.md human-curated without blocking the init flow.

---

## Phase 4 — Generate docs/INDEX.md

This is the most important new phase. Analyze the codebase and generate a real, populated INDEX.md — not a blank template.

```bash
mkdir -p docs/detail
```

### 4a. Detect project shape (spawn Haiku sub-agent)

Spawn a Haiku sub-agent to detect project shape:
- Check for `apps/` or `packages/` directory → monorepo
- Check for separate `backend/`, `server/`, `api/` directories → split frontend/backend
- Check `package.json` for framework (next, react, express, fastapi, etc.)
- Check for `.env.example` or `.env.local` for external service keys
- Report: project shape, framework, list of env var prefixes found

### 4b. Extract structure (spawn Haiku sub-agents, one per concern)

**Routes sub-agent:** Scan `app/`, `pages/`, `src/app/`, `src/pages/`, `routes/` for route files.
List every route path. For Next.js App Router: directory names = routes. For pages/: filename = route.
Output: plain list of routes with one-line description of what each renders.

**API routes sub-agent:** Scan `app/api/`, `pages/api/`, `routes/`, `src/routes/` for API handlers.
List: HTTP method + path + one-line purpose. Flag webhook handlers (stripe, clerk, etc.) explicitly.

**Services sub-agent:** Read `.env.example` or `.env.local` (keys only, not values).
Group by prefix (SUPABASE_, STRIPE_, CLERK_, R2_, OPENAI_, etc.) → each prefix = one external service.
Also scan for MCP config files, check package.json devDependencies for CLI tools.
Output: service name + env prefix + how to access it (MCP, CLI command, or API).

**Dependencies sub-agent:** Read `package.json`. Extract: framework + version, key libraries (auth, db, ui, payments, email, storage). Skip dev tooling (eslint, prettier, typescript, etc.). Output: clean list of production dependencies that matter for understanding the project.

### 4c. Identify shared functions and components (spawn Sonnet sub-agent)

This requires reasoning, not just extraction. Spawn a Sonnet sub-agent:

"Analyze this codebase. Find functions and components that are:
1. Imported in 3 or more different files
2. Used across multiple features or pages
3. Central to data flow (auth, database writes, storage uploads, etc.)

For each one found, list: name, file it lives in, rough list of where it's imported/used.
Also identify: which functions would cause widespread breakage if changed?
Output as a structured list."

Give the sub-agent access to the codebase root. It should use Grep and Read to find imports.

### 4d. Infer features (spawn Sonnet sub-agent)

"Based on the routes, components, and API handlers in this codebase, infer the list of user-facing features. A feature is something a user can DO — not a technical implementation detail.

For each feature, identify:
- Which page/route it lives on
- Whether it's clearly complete (live), partially built (in-progress), or referenced but not implemented (planned)
- Which shared functions or components it depends on (use the shared functions list I'll provide)
- What external service it touches (if any)

Output as a structured list suitable for a dependency map."

Provide this sub-agent with the routes list, shared functions list, and services list from previous steps.

### 4e. Write docs/INDEX.md (spawn Sonnet sub-agent)

Provide all gathered data to a Sonnet sub-agent and ask it to write the complete INDEX.md:

```
Write docs/INDEX.md with exactly two sections.

SECTION 1 — HUMAN MAP (no code, no file paths, no function names):
- Project: one sentence + stack line
- Pages: one line per page/route, what it shows, what features it hosts
- Features: one line per feature — name, page, status (live/in-progress/planned)

SECTION 2 — AGENT DEPENDENCY INDEX:
- Data Model: entity/table names + one-line purpose + how to get schema (MCP command or file path)
- External Services: name + what it does + exact access method (MCP tool name, CLI command, or URL)
- Key Files: non-obvious entry points only — auth config, middleware, shared utils, main DB client. Skip obvious files.
- Critical Functions/Components: name + what features depend on them. Format: name → used by: feature-a, feature-b
- Feature Dependency Map: for each feature:
    feature-name:
      flow: <Component> → POST /api/route → function() → ExternalService [config note]
      data: table.field (type)
      guards: auth requirements, limits, constraints
      shared with: other-feature (if any)
- Guardrails: 3-5 specific rules about what must not be changed or assumed in this project

Flag anything uncertain with [VERIFY] so the user can correct it.
Keep every entry to one line maximum. No prose paragraphs anywhere.
```

### 4f. Create docs/detail/README.md

```markdown
# docs/detail/

Deep-dive documentation for features too complex for a single dependency map entry.

## Creation rule
Only create a file here when a feature's flow cannot be captured in the INDEX.md entry.
Examples of when to create: OAuth flow, Stripe webhook pipeline, multi-step file processing.
Examples of when NOT to create: basic CRUD, simple UI components, standard API routes.

When created, the INDEX.md entry links here: `→ docs/detail/feature-name.md`

## Files
(none yet — created as needed)
```

---

## Phase 5 — Create Folders

```bash
mkdir -p docs/detail
```

No sessions/ folder. No tasks/ folder. The protocol is lean — WORKLOG.md is the real-time log; BRIEF.md + STATUS.md carry forward all context.

---

## Phase 6 — Extended Context Files

After all protocol and design files are created, offer this optional phase.

Ask via AskUserQuestion:

```
Does this project need any extended context files beyond the standard protocol?

Extended context files are deep-reference documents specific to this project:
  • Data contracts — API response shapes, DB table schemas, type definitions
  • Domain reference — business rules, terminology, product spec, "how this works"
  • Architecture supplements — detailed infra diagrams, service maps, sequence flows
  • External integrations — third-party API docs, webhook shapes, rate limits

Y — Yes, let's add some
N — No, standard files are enough
```

If N: skip to Phase 7 (final summary).

If Y: run the extended context loop.

### Extended context loop

Repeat until the user says no more:

**Step 1 — File type**

Ask via AskUserQuestion:

```
What type of extended context file?

A — Data contracts (API shapes, DB schemas, response types)
B — Domain reference (business rules, terminology, product spec)
C — Architecture supplement (infra diagram, service map, sequence flow)
D — External integration (third-party API docs, webhook shapes, rate limits)

Or describe in plain English.
```

**Step 2 — Filename**

Ask via AskUserQuestion:

```
What should this file be called?
(examples: data-contracts.md, tcld-domain.md, stripe-integration.md)

It will live in docs/.
```

**Step 3 — Context collection**

Tell the user:

```
Paste the context for [filename] now. This can be multiple pages — paste everything at once.
Type DONE on a new line when finished.
```

Wait for the paste. Accumulate all content until "DONE" appears on its own line.

**Step 4 — Summarize and write**

Based on file type, structure the raw paste into a clean document:

**Data contracts** → sections: Request shapes | Response shapes | Error types | DB schema | Type definitions.
Each entry: `name → fields (types) — one-line purpose`.

**Domain reference** → sections: Glossary (term: definition) | Business rules (numbered) | Key workflows (step-by-step) | Edge cases.

**Architecture supplement** → sections: Overview | Components (name: role + connections) | Data flows (numbered steps) | Decisions (why this shape) | Open questions.

**External integration** → sections: What it does | Auth method | Key endpoints/webhooks (method + path + purpose) | Rate limits | Error codes we handle | Env vars required.

Show a preview: "Here's what I'll write to docs/[filename] — does this look right?"
Apply any corrections, then write the file to `docs/[filename]`.

**Step 5 — Cross-reference immediately**

After writing the file, update two places:

1. **docs/INDEX.md** — add a row to the Key Files table:
   ```
   | docs/[filename] | [type]: [what it contains] — read before [trigger condition] |
   ```

2. **CLAUDE.md** — append to the `## Extended Context` section:
   ```
   - docs/[filename] — [type]: [one-line description]. Read before [trigger condition].
   ```

   If the `## Extended Context` section doesn't exist yet, create it at the bottom of CLAUDE.md.

If the file is architecture- or decisions-related, also add to **BRIEF.md** (create a `## Reference files` section at the bottom if it doesn't exist):
   ```
   - docs/[filename] — [description]
   ```

**Step 6 — Loop**

Ask via AskUserQuestion:

```
Written and referenced. Do you need another extended context file?

Y — Yes, add another
N — Done
```

Repeat from Step 1 if Y.

---

### Extended Context — populated CLAUDE.md example

```markdown
## Extended Context
> These files go beyond the standard protocol. Read when their trigger applies.

- docs/data-contracts.md — data contracts: API response shapes + Supabase table schemas. Read before any data layer work.
- docs/tcld-domain.md — domain reference: cable TV terminology + channel classification rules. Read before any feature touching channel data.
```

---


## Phase 7 — Final Summary

Give a clear summary:
- Protocol files: created / updated / unchanged
- Design system files: created / updated / unchanged (list which ones need manual fill-in)
- docs/INDEX.md: generated (list [VERIFY] items that need user confirmation)
- Extended context files: list any added (filename + type), or "none added"
- Any files that need attention

The project now has one unified system. Every file is either part of the protocol, referenced from it, or deliberately excluded.

**Important reminders for the user:**
1. "BRAND.md and BRIEF.md were created as stubs — fill them in before the first coding session."
2. "DESIGN.md was generated from context — review the color tokens and mark [VERIFY] items as correct or wrong."
3. "docs/INDEX.md is a first draft — items marked [VERIFY] need your confirmation."
4. "FUNDAMENTALS.md is a global standard — never edit it. It updates with the plugin."
5. "Extended context files in docs/ are referenced in CLAUDE.md §Extended Context — check those entries are accurate."

**Codex setup reminder (one-time, if not already done):**
"If you're using Codex on this project, add one line to `~/.codex/config.toml`:
```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```
This makes Codex read CLAUDE.md automatically — same as Claude Code. One-time setup, applies to all projects."
