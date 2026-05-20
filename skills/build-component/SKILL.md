---
name: build-component
description: Build a new component (or adopt an external one) into the project's existing design system and folder structure. Picks the right tier (Generic / Marketing / App), scans for reuse, normalizes against DESIGN.md tokens, and writes to the location dictated by STRUCTURE.md. Triggers — "build component", "create component", "new component", "make a button/card/hero/dashboard tile", "I want to use this Aceternity/Magic UI piece", "I want a component like X from Mantine/Chakra/MUI".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*,find:*,cat:*,grep:*,test:*,mkdir:*), AskUserQuestion, Task
---

# Build Component

The orchestrated path for adding a new component to an existing project. Decides where it lives, what tier it belongs to, what to reuse, what data it consumes, and which convention to write it in — then writes the code and lets `design-check` fire as the post-write gate.

This skill does not invent a design system. It assumes `agents/DESIGN.md` and `agents/FUNDAMENTALS.md` already exist (via `init-project` or `design-direction`). If either is missing, halt and route the user to `init-project` first.

---

## When this fires

- "Build a component", "create a component", "make a new component", "I need a Hero / FeatureRow / DataTable / KPI tile".
- "I want to use [Aceternity / Magic UI / shadcn block / any URL] in my project" → adopt-external sub-mode.
- "I want a component like [Mantine Combobox / Chakra Drawer / MUI Stepper]" → recreate-from-inspiration sub-mode.
- Slash command: `/build-component`.

Skip conditions: user says "skip build-component", "just write the file", or "no gate, draft only".

If the change is a tiny edit to an existing component (e.g. swap a label), do NOT fire this — it's `design-check` territory only.

---

## What it produces

One component file written to the project's existing folder structure, normalized against `agents/DESIGN.md` tokens, importing only from layers it is allowed to import from. Plus, on first ever run, a written `agents/STRUCTURE.md` capturing the project's component layout so subsequent runs do not re-detect.

Nothing else is touched. `DESIGN.md` / `FUNDAMENTALS.md` are read-only here; if a token is missing, the skill hands off to `design-check` Step 4 (propose new token, wait for confirmation).

---

## The 5 phases

Walk these in order. Each phase has a reference doc — open only when entering that phase.

### Phase 1 — Structure detection

Check for `agents/STRUCTURE.md`. If it exists, read and use it (skip the rest of this phase). If not, run first-run detection: glob common component folders, read `tsconfig.json` paths, scan `package.json` for stack indicators, detect surface route groups, propose findings, then write a confirmed `agents/STRUCTURE.md`.

→ See `references/phase-1-structure-detection.md`.

### Phase 2 — Intake and tier

Ask the user one free-text prompt: *"In one sentence, what are you building?"* Then auto-infer the tier — **Generic**, **Marketing**, or **App** — using the decision tree. Surface the inferred tier for one-line confirmation. Hide tiers that don't apply (desktop-only project → no Marketing tier; dashboard-only → no Marketing tier).

→ See `references/phase-2-intake-and-tier.md`.

### Phase 3 — Reuse scan

Glob the components folder for the locked tier. List every existing component that solves the same or a similar problem. Propose a strategy:

- **(A) Compose** existing components into the new thing — recommended for Marketing / App tiers. No cva triplet needed, just `cn` for className merging.
- **(B) Extend** an existing component with a new variant — when one existing primitive is close but missing a flag.
- **(C) Build a new primitive from scratch** — rare. Only when nothing existing fits. This is the only case where the `cva + forwardRef + cn` triplet applies (or the equivalent for the project's detected convention).

→ See `references/phase-3-reuse-scan.md`.

### Phase 4 — Data shape and location

Decide what the component consumes — props, project CONTENT registry, hardcoded copy, or data fetched via existing hooks — and confirm the write location from `STRUCTURE.md`. Enforce cross-tier import rules: marketing components cannot import from app folder, and vice-versa. Cross-tier asks route to Generic with a wrapper pattern.

→ See `references/phase-4-data-and-location.md`.

### Phase 5 — Preview and write

Show the full proposed component code to the user before writing. User can approve, edit, or restart. On approve, write to the location from `STRUCTURE.md`. After write, `design-check` fires automatically as the post-write gate.

→ See `references/phase-5-preview-and-write.md`.

---

## Sub-modes

Two non-default entry paths. Same 5 phases, but the inputs change.

### Adopt external — paste a copy-paste component

User says: *"I want to use [URL or pasted source] in my project."* Examples: an Aceternity card, a Magic UI hero, a shadcn block, a Tailwind UI snippet. The skill reads the source, identifies values that don't match `agents/DESIGN.md` tokens, proposes a normalized version using project tokens, asks for confirmation, writes to the Generic location from `STRUCTURE.md`. Unmappable values (e.g. a shadow that doesn't match any defined token) get surfaced — the user adds a new token, accepts the raw value as a one-off (cardinal-sin violation), or simplifies.

→ See `references/adopt-external.md`.

### Recreate from inspiration — installable libraries

User says: *"I want a component like [Mantine Combobox / Chakra Drawer / MUI Stepper / React Aria Calendar]."* Adopting the whole library isn't an option (different design system, locked tokens, runtime overhead). The skill studies the named API and behavior, generates a brand-new Generic primitive in the project's own design system using the project's detected convention. Headless-library cases (Radix, React Aria, Headless UI) get a different note: install the headless package, build styling on top.

→ See `references/recreate-from-inspiration.md`.

---

## Hard rules

- **No write without preview.** Phase 5 always shows the full code before saving.
- **No raw hex / px / font-string in the output.** Every visual value resolves through `agents/DESIGN.md` via the project's token system (CSS variables → Tailwind alias, or `styled-components` theme, or Swift `Color`).
- **Cross-tier imports are blocked.** Marketing never imports from app/. App never imports from marketing/. Cross-tier needs go to Generic + wrapper.
- **`cva + forwardRef + cn` triplet applies only to new primitives (Generic + Strategy C).** Compositions and variant-extensions don't need it. Imposing the triplet on a composition is over-engineering and produces noise.
- **STRUCTURE.md is written once, read forever.** First run writes it after user confirmation. Subsequent runs read it and skip detection.
- **Convention is detected, not asked.** If `shadcn-ui` / `class-variance-authority` is in `package.json` → cva+forwardRef+cn. If `styled-components` → styled-components. If `*.module.css` files exist → CSS modules. If none detected → ask the user, default to vanilla CSS-with-tokens.
- **`design-check` runs automatically after Phase 5.** Don't duplicate its 7 steps here — `build-component` is the path-of-build, `design-check` is the gate-of-correctness. They chain.
- **Never modify `DESIGN.md` or `FUNDAMENTALS.md` from this skill.** Missing tokens route through `design-check` Step 4.

---

## Sub-agent routing

Heavy reasoning steps delegate to Task tool sub-agents to keep orchestration context lean:

| Step | Tier | Why |
|------|------|-----|
| Phase 1 codebase scan (folders, package.json, tsconfig) | fast | Pure extraction |
| Phase 3 reuse-scan glob + read-similar | fast | Pattern matching |
| Phase 3 strategy proposal (A / B / C) | reasoning | Judgment on whether existing primitives compose |
| Phase 5 code generation (new primitive) | reasoning | Convention application + token discipline |
| Adopt-external normalization | reasoning | Mapping foreign values to project tokens |
| Recreate-from-inspiration generation | reasoning | API study + new-primitive synthesis |

Never use the most expensive model. Reasoning tier (Sonnet) is the ceiling.

---

## Output shape (end of skill)

```
build-component — summary

Built: <component name>
Tier: <Generic | Marketing | App>
Strategy: <A compose | B extend | C new primitive>
Convention: <cva+forwardRef+cn | styled-components | CSS modules | vanilla CSS>
Location: <file path written>

Dependencies imported:
  - <component 1> from <path>
  - <component 2> from <path>
  - cn from <path>

Tokens used:
  - <token 1>, <token 2>, <token 3>

Next:
  → design-check will run automatically against the written file.
  → If new tokens were proposed, they remain pending until you confirm.
```

---

## Difference from related skills

- **`init-project`** — bootstraps the project layout and writes the canon files (`DESIGN.md`, `FUNDAMENTALS.md`, `STRUCTURE.md` if requested). `build-component` assumes those exist and writes components against them.
- **`design-direction`** — sets brand-level direction and writes `BRAND.md` + `DESIGN.md` Overview. Upstream of any component work.
- **`design-check`** — the 7-step UI gate. `build-component` is the path-of-build, `design-check` is the gate-of-correctness. `design-check` fires automatically after Phase 5.
- **`discussion-mode`** — pure conversation, no writes. If the user wants to talk through a component idea without committing, use that first, then `build-component` to actually ship.
- **`audit`** — periodic consistency scan across canon. Will catch drift between `STRUCTURE.md` and the actual filesystem if it happens.

All five chain: `init-project` → `design-direction` (optional) → `build-component` → `design-check` (auto) → `audit` (periodic).
