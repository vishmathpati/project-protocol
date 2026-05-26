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
    a rich BRAND.md, the DESIGN.md Overview + brand-specific anti-patterns,
    AND the DESIGN.md token frontmatter (colors, typography, spacing) with
    an HTML preview for visual approval before write. Adds ~5–10 minutes.

Pick A or B.
```

- **A (default)** → continue with the existing BRAND.md flow below.
- **B (deep)** → hand off to `design-direction`. That skill writes BRAND.md, DESIGN.md Overview + brand-specific DO NOT additions, AND DESIGN.md token frontmatter (after user approves an HTML preview). When it returns, **both the BRAND.md step AND the DESIGN.md step below are skipped** — already complete. Phase 4 continues from FUNDAMENTALS.md / TOOLING.md / DISCOVERIES.md only.

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

### Step 4-pre — Monorepo detection

Before proceeding with TOOLING.md, check whether this is a monorepo. Run all four checks:

```bash
# Check 1 — root package.json with "workspaces" field
node -e "const p=require('./package.json'); process.exit(p.workspaces ? 0 : 1)" 2>/dev/null

# Check 2 — pnpm workspace manifest
ls pnpm-workspace.yaml 2>/dev/null

# Check 3 — Turborepo config
ls turbo.json 2>/dev/null

# Check 4 — Nx config
ls nx.json 2>/dev/null
```

**If any check passes → monorepo mode:**

1. Scan for app-level `package.json` files:
   ```bash
   find apps packages -name "package.json" -maxdepth 3 2>/dev/null | grep -v node_modules
   ```
2. Present the detected apps to the user via `AskUserQuestion`:
   ```
   Detected monorepo. Found the following apps/packages with their own package.json:
   - apps/web/package.json
   - apps/api/package.json
   - (etc.)

   Which apps should get their own agents/TOOLING.md rules?
   A — All of the above
   B — Web app only (apps/web)
   C — Let me specify
   ```
3. For each selected app, run Steps 4a and 4b (detect package manager, render TOOLING.md) scoped to that app's directory — read `apps/web/package.json` for lockfiles, write to `apps/web/agents/TOOLING.md` (or wherever the user designates).
4. Record the monorepo flag and app paths in `agents/STRUCTURE.md` (or queue them for Phase 4-struct below if STRUCTURE.md doesn't exist yet). These paths are read by `design-check`, `audit`, and `build-component`.

**If no check passes → single-app mode:** proceed with Steps 4a and 4b as before, writing to `agents/TOOLING.md` at project root.

---

**Detect Node (single-app path):** Node project if a `package.json` exists at the project root. If not Node (Swift, Python, plain repo): skip this section silently — do not create `agents/TOOLING.md`.

### Step 4a — Detect or ask package manager

**On first init (no `agents/TOOLING.md` exists):**

1. Scan for lockfiles at the project root:
   ```bash
   ls bun.lock pnpm-lock.yaml package-lock.json yarn.lock 2>/dev/null
   ```
2. **Exactly one detected:** propose it as the canonical manager. Ask via `AskUserQuestion`:
   ```
   Detected lockfile: {lockfile}. Use {manager} as this project's package manager?
   [Y] Yes, use {manager}  [N] Choose a different one
   ```
   One-key confirm (Y is default). If N, fall through to "none detected" flow.
3. **Multiple detected:** ask which is canonical:
   ```
   Multiple lockfiles detected: {list}. Which is the canonical package manager for this project?
   A — bun  B — pnpm  C — npm  D — yarn
   ```
4. **None detected:** ask from scratch:
   ```
   No lockfile detected. Which package manager does this project use?
   A — bun (recommended)  B — pnpm  C — npm  D — yarn
   ```

**On re-init (`agents/TOOLING.md` already exists):**

1. Read the `**Package manager:**` line from `agents/TOOLING.md` to get the current choice.
2. Re-run the lockfile scan above to detect the current lockfile.
3. Ask via `AskUserQuestion`:
   ```
   agents/TOOLING.md records {current-manager} as the package manager.
   Lockfile detected: {detected or "none"}.
   Continue with {current-manager} or switch?
   [Y] Continue with {current-manager}  [N] Switch to {detected or "choose"}
   ```
   Default is Y (keep current). If switching, follow the first-init flow above.

### Step 4b — Render and write TOOLING.md

Once the package manager is confirmed, read the plugin template from `${CLAUDE_PLUGIN_ROOT:-${CODEX_PLUGIN_ROOT}}/templates/TOOLING.md` (or use Read tool if env var unset), replace every `{bun|pnpm|npm|yarn}` placeholder with the chosen manager, replace `{bun.lock|pnpm-lock.yaml|package-lock.json|yarn.lock}` with the corresponding lockfile name, replace `{manager}` with the chosen manager name, then write to `agents/TOOLING.md`.

```bash
# Example for bun selection — sed replacements match the placeholder patterns
MANAGER="bun"; LOCKFILE="bun.lock"
sed -e "s/{bun|pnpm|npm|yarn}/$MANAGER/g" \
    -e "s/{bun.lock|pnpm-lock.yaml|package-lock.json|yarn.lock}/$LOCKFILE/g" \
    -e "s/{manager}/$MANAGER/g" \
    "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/TOOLING.md" > agents/TOOLING.md
```

If the plugin-root env var is unset: use the Read tool to fetch the template, apply substitutions in the Write content, then Write to `agents/TOOLING.md`.

When written, confirm the project's actual `package.json` / `.nvmrc` / `.npmrc` match the declared manager. If they drift, surface as a `[VERIFY]` item at Phase 7 — do not auto-fix.

---

## `agents/DESIGN.md`

Most important file in Phase 4. The shape is fixed — `templates/DESIGN.md` is a complete scaffold with token categories, DO NOT section, and Extension protocol already filled in. **Phase 4 fills the placeholders, it does not invent the shape.**

DESIGN.md follows the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec: YAML frontmatter (machine-readable tokens) + markdown body (human rationale).

### Token shape (v2.1 — role-split + paired modes)

The template's frontmatter is organised into seven top-level blocks. Fill each one — never collapse them back into a flat `colors:` map.

- `font:` — three roles. `display` (MEMORY job, distinctive, has a `banned:` list that disallows Inter / Geist / Söhne / IBM Plex / SF Pro / Roboto / Space Grotesk / Open Sans / Public Sans / system-ui as a display face), `body` (WAYFINDING job, those Inter/Geist/Söhne fonts are acceptable here), `mono` (data / code).
- `surface:` — material-named tokens, not indexed. `paper` (primary canvas), `ash` (raised surface like cards), `ink` (text / dark canvas), `hairline` (1 px borders).
- `accent:` — `primary`, `primary_hover`, optional `secondary` (only for two-accent brands).
- `status:` — `success`, `warning`, `error`. Semantic only.
- `light_mode:` and `dark_mode:` — **two separate blocks**, each with its own `paper` / `ash` / `ink` / `hairline` plus a `character:` line describing the pairing intent. `dark_mode` also gets a `rule:` line (e.g. "never pure #000 — always 4–8% warm tint"). Both modes must share temperature and material story.
- `spacing:`, `radius:`, `shadow:`, `components:` — unchanged in shape, but `components:` references now point at the new tokens (`{accent.primary}`, `{surface.paper}`, `{surface.ash}`, `{surface.ink}`, `{surface.hairline}`).

When filling placeholders, name surfaces by **material** (cream, leather, parchment, slate) not by **index** (surface-1, surface-2). Name accents by **material** (brass, terracotta, oxblood, jewel-green) not by hue position. Index naming invites a flood of generic levels; material naming forces a story.

### Step 1 — Read the template

Source: `${CLAUDE_PLUGIN_ROOT:-${CODEX_PLUGIN_ROOT}}/templates/DESIGN.md`.

This file is the contract for what every project's DESIGN.md must contain — the role-split font block, material-named surfaces, paired light/dark blocks, accent-discipline rules, DO NOT section, Extension protocol, and Agent prompt guide. Do not strip or shorten any section. Only fill placeholders.

If the plugin-root env var is unset: use the Read tool to fetch the template content from the plugin install path.

### Step 2 — Detect existing tokens in the project

Read `agents/DESIGN.md` if it exists. Check for YAML frontmatter (starts with `---` and contains `name:` and a recognisable token block before the closing `---`).

- Has frontmatter with `font:` + `surface:` + `light_mode:` + `dark_mode:` blocks → already v2.1 shape. Branch: "Existing DESIGN.md — fill gaps only".
- Has frontmatter with the old flat `colors:` / `typography:` blocks → legacy v1 shape. Branch: "Legacy upgrade — re-shape into v2.1 template" (split fonts into display/body/mono, rename `bg`/`surface`/`surface-2`/`text`/`border` to `paper`/`ash`/`ink`/`hairline`, derive `light_mode` + `dark_mode` blocks).
- No frontmatter → legacy markdown-only format. Branch: "Legacy upgrade — re-shape into v2.1 template".
- Doesn't exist → scan codebase:
  - `src/app/globals.css` / `app/globals.css` — CSS custom properties (look for both `:root` and `.dark` blocks to populate the paired modes)
  - `tailwind.config.{js,ts}` — `theme.extend`
  - `src/styles/`, `tokens.css`, `design-tokens.ts`, `theme.ts`
  - Swift: `DesignTokens.swift`, asset catalog colors, `Color` extensions, light/dark appearance variants

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

All paths produce the same output: the `templates/DESIGN.md` scaffold with placeholders replaced by real values, in the v2.1 token shape (role-split fonts, material-named surfaces, paired light/dark blocks).

- **A (transfer):** Haiku sub-agent extracts CSS vars / Tailwind config / Swift tokens, including both `:root` and `.dark` variants when present. Sonnet sub-agent maps them onto the template's frontmatter and body placeholders — splitting any single `font-family` into display/body/mono roles (asking the user if only one font is defined), renaming flat `bg`/`surface`/`text`/`border` tokens to material-named `paper`/`ash`/`ink`/`hairline`, and populating both `light_mode:` and `dark_mode:` blocks. Sections without source values stay as `[VERIFY]` placeholders.
- **B (transfer + add):** extract as A, then ask "What to add or change?" Apply additions while preserving the template structure and the role-split / paired-mode shape.
- **C (fresh):** use `BRAND.md` + user description; Sonnet sub-agent generates token values for the template. Pick a display face that is NOT in the `banned:` list, pick paired light/dark characters that share temperature, name accents by material. Never skip a section — fill or `[VERIFY]`.

**Hard rules for any path:**
- Do not delete sections from the template (Overview, Colors, Typography, Light + Dark mode pairing, Spacing, Radius, Shadow, Components, DO NOT, Extension protocol, Agent prompt guide).
- Do not collapse the role-split `font:` block back into a single font field. Display, body, and mono are three distinct roles.
- Do not collapse `light_mode:` and `dark_mode:` into a single block. They are paired but separate.
- Do not rename material-named surface tokens (`paper`, `ash`, `ink`, `hairline`) back to index names (`bg`, `surface-1`, `surface-2`).
- Do not change the DO NOT section's universal items — only **add** brand-specific anti-patterns.
- Do not edit the Extension protocol wording — it's enforced by the `design-check` skill.

### Step 4-struct — Write monorepo flag to STRUCTURE.md

If `agents/STRUCTURE.md` already exists (written by a prior `build-component` run), append or update the following block at the top of the file (after the header comment, before `## Surfaces present`):

```markdown
## Project layout

**Monorepo:** true | false
**App paths:** apps/web, apps/api, packages/ui   ← list only if monorepo: true; remove this line if false
```

If `agents/STRUCTURE.md` does not exist yet, queue this data for when it is first created (by `build-component` or Phase 0c modernize). The monorepo flag and app paths must appear in STRUCTURE.md so `design-check`, `audit`, and `build-component` all read the same source of truth.

---

### Step 5 — Custom DESIGN.md lint (optional)

If you have a custom DESIGN.md linter configured for this project, run it here.

No linter is shipped with project-protocol. The `@google/design.md` package is not a project-protocol dependency and is not installed by default. If you want to lint `agents/DESIGN.md`, install and configure your own linter and document it under "optional dev tools" in `agents/TOOLING.md`.

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
