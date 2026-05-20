# Phase 4 — Design system files

Create `agents/BRAND.md`, `agents/FUNDAMENTALS.md`, `agents/TOOLING.md` (Node only), `agents/DESIGN.md`, `agents/DISCOVERIES.md`. Also confirm `agents/BRIEF.md` from Phase 3 is the right shape.

Never silently overwrite. Always read first, ask before replacing.

---

## Optional handoff to `design-direction` (deep flow)

Before running the standard A/B/C flow for BRAND.md and DESIGN.md below, offer the user the deeper alternative — the `design-direction` skill produces a much richer BRAND.md by extracting 9 taste axes from a raw brand dump and proposing 3 named directions to choose from.

Ask via `AskUserQuestion`:

```
Design system bootstrap — two paths:

A — Quick (default): 3 questions for BRAND.md, then A/B/C for DESIGN.md.
    Good when you already have a clear design direction in mind.

B — Deep (design-direction skill): one free-text brand dump, then I extract
    the taste axes and propose 3 named directions with a moodboard. Produces
    a much richer BRAND.md. Adds ~5 minutes.

Pick A or B.
```

- **A (default)** → continue with the existing BRAND.md flow below.
- **B (deep)** → hand off to `design-direction`. That skill writes a populated BRAND.md and DESIGN.md Overview + brand-specific DO NOT additions, then returns control here. When it returns, the BRAND.md step below is skipped (already done) and the DESIGN.md step runs as path C (fresh generation) using the newly-populated BRAND.md as the brief.

If `design-direction` is unavailable (older plugin version, or skill missing on disk): silently fall through to path A.

---

## `agents/BRAND.md`

**If exists:** read, use as context for DESIGN.md generation, do not overwrite.

**If missing:** silently scan the codebase for brand signals via a Haiku sub-agent:
- `README.md` — product name, description, tagline
- `package.json` — `name` and `description` fields
- `index.html` / `layout.tsx` — `<title>`, `<meta name="description">`, OG tags
- Any landing page copy (`page.tsx`, `index.tsx`, `Home` component)

Present findings via AskUserQuestion:

```
Found about this product from the codebase:
- Name: [detected or "not found"]
- What it does: [detected or "not found"]
- Who it's for: [detected or "not found"]

How would you like to create BRAND.md?

A — Auto-generate from what I found (I'll show you first for confirmation)
B — I'll answer 3 quick questions
C — Skip for now (blank stub)
```

**If A:** generate, show preview, apply corrections, write.

**If B:** ask one at a time:
1. "What is this product in one sentence? Who is it for?"
2. "What's the personality/tone?"
3. "What is it NOT? What should agents never build into this?"

**If C:** create blank stub:

```markdown
# agents/BRAND.md — [Project Name]
> What every agent must know before touching this project.

## Product
- Name:
- Domain:
- One sentence:

## User
- Who it's for:
- Problem it solves:
- What it is NOT:

## Personality
- Tone:
- Values:
```

Mark auto-detected fields with `[VERIFY]`.

---

## `agents/FUNDAMENTALS.md`

**Always:** copy verbatim from the plugin template at `${CLAUDE_PLUGIN_ROOT}/templates/FUNDAMENTALS.md` to `agents/FUNDAMENTALS.md`. Silently replace any existing version — this is a global standard.

```bash
cp "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/FUNDAMENTALS.md" agents/FUNDAMENTALS.md
```

If the plugin-root env var is unset (some agents don't expose it): use the Read tool to fetch the template content from the plugin install path, then Write it to `agents/FUNDAMENTALS.md`. Do not modify per project.

---

## `agents/TOOLING.md` (Node projects only)

**Detect:** Node project if a `package.json` exists at the project root. If not Node (Swift, Python, plain repo): skip this section silently — do not create `agents/TOOLING.md`.

**If Node and `agents/TOOLING.md` exists:** silently overwrite from the plugin template. Same rule as `FUNDAMENTALS.md` — this is a global locked standard, not per-project.

**If Node and missing:** copy verbatim from the plugin template at `${CLAUDE_PLUGIN_ROOT}/templates/TOOLING.md` to `agents/TOOLING.md`.

```bash
if [ -f package.json ]; then
  cp "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/TOOLING.md" agents/TOOLING.md
fi
```

If the plugin-root env var is unset: use the Read tool to fetch the template content from the plugin install path, then Write it to `agents/TOOLING.md`. Do not modify per project.

When copied, also confirm the project's actual `package.json` / `.nvmrc` / `.npmrc` match the standard. If they drift, surface the mismatch as a `[VERIFY]` item at Phase 7 — do not auto-fix.

---

## `agents/DESIGN.md`

Most important file in Phase 4. The shape is fixed — `templates/DESIGN.md` is a complete scaffold with token categories, DO NOT section, and Extension protocol already filled in. **Phase 4 fills the placeholders, it does not invent the shape.**

DESIGN.md follows the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec: YAML frontmatter (machine-readable tokens) + markdown body (human rationale).

### Step 1 — Read the template

Source: `${CLAUDE_PLUGIN_ROOT:-${CODEX_PLUGIN_ROOT}}/templates/DESIGN.md`.

This file is the contract for what every project's DESIGN.md must contain — token categories, the accent-discipline rules, the DO NOT section, the Extension protocol, and the Agent prompt guide. Do not strip or shorten any section. Only fill placeholders.

If the plugin-root env var is unset: use the Read tool to fetch the template content from the plugin install path.

### Step 2 — Detect existing tokens in the project

Read `agents/DESIGN.md` if it exists. Check for YAML frontmatter (starts with `---` and contains `colors:` or `name:` before the closing `---`).

- Has frontmatter → already new format. Branch: "Existing DESIGN.md — fill gaps only".
- No frontmatter → legacy format. Branch: "Legacy upgrade — re-shape into template".
- Doesn't exist → scan codebase:
  - `src/app/globals.css` / `app/globals.css` — CSS custom properties
  - `tailwind.config.{js,ts}` — `theme.extend`
  - `src/styles/`, `tokens.css`, `design-tokens.ts`, `theme.ts`
  - Swift: `DesignTokens.swift`, asset catalog colors, `Color` extensions

### Step 3 — Ask the open question

If existing tokens found, present them and ask:

```
Found design tokens in: [files]
Sample: [5–10 CSS variables or Tailwind values]

What would you like to do with agents/DESIGN.md?

A — Transfer existing system as-is into the template (document what's there, no visual change)
B — Transfer existing + I'll tell you what to add or change
C — Generate a completely fresh design system (based on BRAND.md + your direction)

Or type your own direction.
```

If no tokens found:

```
No existing design tokens detected.

A — Generate a fresh design system from your product description
B — I'll describe the vibe and you generate from that

Or type your own direction.
```

### Step 4 — Execute

All paths produce the same output: the `templates/DESIGN.md` scaffold with placeholders replaced by real values.

- **A (transfer):** Haiku sub-agent extracts CSS vars / Tailwind config / Swift tokens. Sonnet sub-agent maps them onto the template's frontmatter and body placeholders. Sections without source values stay as `[VERIFY]` placeholders.
- **B (transfer + add):** extract as A, then ask "What to add or change?" Apply additions while preserving the template structure.
- **C (fresh):** use `BRAND.md` + user description; Sonnet sub-agent generates token values for the template. Never skip a section — fill or `[VERIFY]`.

**Hard rules for any path:**
- Do not delete sections from the template (Overview, Colors, Typography, Spacing, Radius, Shadow, Components, DO NOT, Extension protocol, Agent prompt guide).
- Do not change the DO NOT section's universal items — only **add** brand-specific anti-patterns.
- Do not edit the Extension protocol wording — it's enforced by the `design-check` skill.

### Step 5 — Lint after writing

```bash
npx @google/design.md lint agents/DESIGN.md
```

Report errors (must fix), warnings (show, ask), info (silent).

If linter not available: note "Linter not available — install `@google/design.md` to validate."

---

## `agents/DISCOVERIES.md`

**If exists:** keep as-is. Append-only.

**If missing:** create stub.

```markdown
# agents/DISCOVERIES.md — [Project Name]
> What worked. Updated per session, not per feature.
> Format: [date] · [agent] · [component/pattern] — what worked and why

## Log
(empty — add entries as you build)
```

---

## End of Phase 4 — BRIEF.md reminder

If `agents/BRIEF.md` was created as a stub during Phase 3, surface:

```
📋 agents/BRIEF.md was created as a stub. Worth adding from this init:
- [Design system choice: A / B / C / custom — and why]
- [Stack or architecture decisions surfaced during init]
- [Scope constraints mentioned]

You fill it in — I won't write BRIEF.md for you. Drop key decisions there when you have a moment.
```

This keeps BRIEF.md human-curated without blocking the init flow.
