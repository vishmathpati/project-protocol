# Phase 4 — Design system files

Create `agents/BRAND.md`, `agents/FUNDAMENTALS.md`, `agents/TOOLING.md` (Node only), `agents/DESIGN.md`, `agents/DISCOVERIES.md`. Also confirm `agents/BRIEF.md` from Phase 3 is the right shape.

Never silently overwrite. Always read first, ask before replacing.

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

Most important file in Phase 4. Decision process must be open — never force two options.

DESIGN.md follows the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec: YAML frontmatter (machine-readable tokens) + markdown body (human rationale).

### Step 1 — Detect existing tokens

Read `agents/DESIGN.md` if it exists. Check for YAML frontmatter (starts with `---` and contains `colors:` or `name:` before the closing `---`).

- Has frontmatter → already new format. Branch: "Existing DESIGN.md".
- No frontmatter → legacy format. Branch: "Legacy upgrade".
- Doesn't exist → scan codebase:
  - `src/app/globals.css` / `app/globals.css` — CSS custom properties
  - `tailwind.config.{js,ts}` — `theme.extend`
  - `src/styles/`, `tokens.css`, `design-tokens.ts`, `theme.ts`

### Step 2 — Ask the open question

If existing tokens found, present them and ask:

```
Found design tokens in: [files]
Sample: [5–10 CSS variables or Tailwind values]

What would you like to do with agents/DESIGN.md?

A — Transfer existing system as-is (document what's there, no visual change)
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

### Step 3 — Execute

All paths produce the same output: YAML frontmatter + 9-section markdown body.

- **A (transfer)**: Haiku sub-agent extracts CSS vars and Tailwind config. Sonnet sub-agent structures them into DESIGN.md format.
- **B (transfer + add)**: extract as A, then ask "What to add or change?" Apply additions.
- **C (fresh)**: use BRAND.md + user description; Sonnet sub-agent generates both layers from scratch.

### Step 4 — Lint after writing

```bash
npx @google/design.md lint agents/DESIGN.md
```

Report errors (must fix), warnings (show, ask), info (silent).

If linter not available: note "Linter not available — install `@google/design.md` to validate."

### DESIGN.md format

**Layer 1 — YAML frontmatter:**

```yaml
---
version: alpha
name: [Project Name]
colors:
  primary: "#[hex]"
  secondary: "#[hex]"
  background: "#[hex]"
  foreground: "#[hex]"
  muted: "#[hex]"
  border: "#[hex]"
typography:
  heading: { fontFamily: ..., fontSize: ..., fontWeight: ... }
  body: { fontFamily: ..., fontSize: ..., fontWeight: ... }
  caption: { fontFamily: ..., fontSize: ... }
rounded: { sm: ..., md: ..., lg: ... }
spacing: { sm: ..., md: ..., lg: ... }
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.sm}"
  # etc.
---
```

Rules:
- All color values `#` + 6-digit hex (sRGB)
- Use `{token.reference}` syntax in components
- Mark uncertain values with `[VERIFY]` inline comment

**Layer 2 — Markdown body, 9 sections:**

```
## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Components
## Do's and Don'ts
## Responsive Behavior
## Agent Prompt Guide (one paragraph for agents — written last)
```

Generate all 9 sections even if some need [VERIFY] placeholders.

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
