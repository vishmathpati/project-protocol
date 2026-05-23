---
name: build-page
description: Compose a whole page (marketing or dashboard) from already-locked content + design system. Layout-first, code-last — discusses architecture, hierarchy, assets, and component reuse BEFORE any write, then delegates atomic-component creation to build-component and wires the final page in a single approval. Triggers — "build the homepage", "build the pricing page", "compose page X", "wire up the X page", "build the dashboard overview page", "build the settings page", "/build-page".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*,find:*,cat:*,grep:*,test:*,mkdir:*), AskUserQuestion, Task, Skill
---

# Build Page

The compositional sibling to `build-component`. Where `build-component` writes one atomic thing (a button, a tile, a hero block) and gates it through `design-check`, `build-page` orchestrates an entire page — architecture, section rhythm, hierarchy, asset manifest, component selection — and only generates code at the very end, after every architectural question has been answered in chat.

It exists because pages are not big components. A page is a *composition*: which sections, in what order, with what rhythm, drawn from which canonical content, anchored by which visuals, built from which existing components (and which net-new ones), and finally wired together in a layout. Forcing that work through `build-component`'s atomic gate produces a 400-line code drop the user cannot meaningfully review — no layout conversation, no asset planning, no reuse audit, no hierarchy debate. This skill is the layout-first, code-last alternative.

---

## When this fires

- "Build the homepage", "build the pricing page", "build the about page", "compose page X", "wire up the X page", "build the marketing homepage".
- "Build the dashboard overview page", "build the settings page", "build the team page", "build the analytics page".
- Slash command: `/build-page`.

### Does NOT fire for

- A single component request ("build a button", "I need a KPI tile", "make a hero block") → `build-component`.
- A tiny edit to an existing page ("change the H1 copy", "swap the screenshot") → direct edit + `design-check` as post-gate.
- The first-ever bootstrap of a project (`CLAUDE.md`, `BRAND.md`, `DESIGN.md` don't exist) → `init-project` → `design-direction` → `marketing-brief` (if marketing surface) first.

### Skip conditions

- User says "skip build-page", "just write the page file", "no gate, draft only" → drops into a single-shot build-component-style flow with one approval at the end.

---

## What it produces

One page file written to the location dictated by `agents/STRUCTURE.md`, plus zero-to-many net-new component files written by inline `build-component` calls during Phase 5. Copy is inlined directly in the page's JSX (sourced from `agents/marketing/CONTENT.md` + `agents/marketing/copy/<slug>.md` for marketing pages, or from the relevant brief for dashboard pages). **No intermediate content mirror file is ever created.**

The page file imports only from layers it is allowed to import from per `STRUCTURE.md`'s cross-tier rules. After Phase 6 writes the page, `design-check` fires automatically as the post-write gate.

Nothing else is touched. `DESIGN.md` / `FUNDAMENTALS.md` / `STRUCTURE.md` / `agents/marketing/*` are read-only here.

---

## Required canon

Before Phase 1 can run, these must exist:

- `agents/CLAUDE.md`, `agents/BRAND.md`, `agents/DESIGN.md`, `agents/FUNDAMENTALS.md`, `agents/STRUCTURE.md`.
- For **marketing pages**: `agents/marketing/CONTENT.md`, `agents/marketing/SITEMAP.md`, `agents/marketing/briefs/<slug>.md`, `agents/marketing/copy/<slug>.md`, `agents/marketing/MEDIA.md`, `agents/marketing/layouts/<slug>.md`.
- For **dashboard pages**: at minimum a brief or spec describing what the page is for. If absent, the skill halts and asks the user to write one (one-paragraph intent + KPI list is enough; this is not a full marketing-brief).

If marketing canon is missing for a marketing-tier page, the skill halts with: *"Marketing canon missing for `<slug>`. Run `marketing-brief` first (or add the missing files), then re-invoke `build-page`."*

---

## The 6 phases

Walk in order. Each phase has a reference doc — open only when entering that phase (progressive disclosure keeps context lean).

**No file writes before Phase 6.** Phases 1–5 happen entirely in chat. Each phase ends with a single-sentence approval gate (`approve / push back / restart`). If the user pushes back, that phase repeats; the skill does not advance to the next phase until approval is explicit.

### Phase 1 — Read the brief

Detect the page's tier (marketing or dashboard) from the user's request + `STRUCTURE.md` declared surfaces. Read the canon for that tier:

- **Marketing tier** → `CONTENT.md`, `SITEMAP.md` (find the row for this slug), `briefs/<slug>.md`, `copy/<slug>.md`, `layouts/<slug>.md`, `MEDIA.md`. Also read `BRAND.md` and `DESIGN.md` Overview.
- **Dashboard tier** → the page brief (or the relevant section of `ROADMAP.md`), `STRUCTURE.md` for the app folder's component inventory, `DESIGN.md`, `FUNDAMENTALS.md`.

Surface a one-paragraph synthesis back to the user — *"This page is for X audience, single intent Y, primary CTA Z, with these content blocks already specified in the brief: …"* — and wait for *"yes, that's right"* before Phase 2.

→ See `references/phase-1-read-brief.md`.

### Phase 2 — Layout architecture

Propose the page's section list — count, order, rhythm — drawn from the brief's content blocks. Show it as a vertical outline in chat, not as code. Example shape:

```
1. Hero        — claim + primary CTA + visual anchor (image)
2. Trust strip — 3 short claims, dense
3. How it works — 3-step narrative, calm
4. Features    — workflow-stage grid (Capture / Deliver / Approve / Run-studio)
5. Moment 1    — Selfie Search story, image-left
6. Moment 2    — Camera coverage, three-column
7. Moment 3    — Run-the-studio, image-right
8. FAQ         — 8 questions, accordion
9. Final CTA   — single ask, centered
```

Annotate the rhythm (which sections are calm vs loud, where the eye rests, where it accelerates). User approves the section list, the order, and the rhythm — or pushes back. Approval is required before Phase 3.

→ See `references/phase-2-layout-architecture.md`.

### Phase 3 — Hierarchy

For each approved section, propose what's primary, secondary, and tertiary within that section — where the eye lands first, what's the load-bearing claim, what's supporting. One short paragraph per section. Example:

```
§1 Hero — primary: H1 claim ("The operating system for event-photography businesses"). Secondary: one-line subhead. Tertiary: pair of CTAs (Start free / See how it works). Visual anchor sits beside text at lg+, below at md and under.
```

User approves the hierarchy per section — or pushes back on specific sections. Approval is required before Phase 4.

→ See `references/phase-3-hierarchy.md`.

### Phase 4 — Asset manifest

Per section, declare the visual treatment: image / screenshot / illustration / animation / micro-interaction / icon-only / no-visual. For marketing pages, cross-reference `MEDIA.md` (which already declared per-section anchors during `marketing-brief`) and propose any deltas. For dashboard pages, declare any data-viz / chart / mock-data requirements.

Also surface micro-interactions the page wants: hover states beyond defaults, scroll-linked reveals, accordion behavior, sticky elements, scroll-snap, etc. Be conservative — propose only interactions that earn their keep against the brand's `tempo` axis from `BRAND.md`.

Output is a markdown table in chat — section / visual type / asset id (matches MEDIA.md) / interaction notes. User approves or trims. Approval is required before Phase 5.

→ See `references/phase-4-asset-manifest.md`.

### Phase 5 — Component selection

Per section, decide one of three strategies:

- **Reuse** — an existing component in the project matches exactly. Cite its path.
- **Adapt** — an existing component is close but needs one new variant or prop. Cite the path + describe the delta.
- **Build new** — no existing component fits. Delegate to `build-component` inline (auto-invoked), build the component end-to-end in its own scoped sub-flow, then return to `build-page` with the new component's path in hand.

Show the per-section decisions as a table in chat — section / strategy / component path / notes. User approves the table. **The build-new entries are then executed sequentially**, one `build-component` call per row, each with its own preview + approval inside `build-component`'s Phase 5. The user is not asked to approve the whole page's worth of components in one giant code drop — each net-new component gets its own focused conversation.

Once every section has a real component path (whether reused, adapted, or freshly built), Phase 5 is done. Approval is required before Phase 6.

→ See `references/phase-5-component-selection.md`.

### Phase 6 — Wire-up

Compose all the components into the final page file. Copy is inlined directly in the JSX, sourced from `agents/marketing/copy/<slug>.md` (marketing) or the page brief (dashboard). At the top of the file, leave a single-line comment pointing back to the canonical source so future agents know where the truth lives:

```tsx
// Copy mirrors agents/marketing/copy/home.md — when that file changes,
// propagate the update here. Do NOT inline new copy without updating the
// canon first.
```

Show the full proposed page file to the user. They approve, edit, or restart. On approve, write to the location from `STRUCTURE.md`. After write, `design-check` fires automatically as the post-write gate.

→ See `references/phase-6-wire-up.md`.

---

## Sub-modes

Same 6 phases, but the inputs and emphases differ.

### Marketing page

Default for any page under `STRUCTURE.md`'s `marketing` / `landing` / `web` surface. Reads the full `agents/marketing/*` canon. Emphasis in Phase 2 is on persuasion rhythm — calm/loud, claim/proof/social-proof/ask. Phase 4 leans heavily on `MEDIA.md`'s pre-declared anchors. Phase 6 enforces RSC + `generateMetadata` for SEO (no `"use client"` on the page-level component; client behavior moves to small child components like `<AuthRedirect />`).

→ See `references/sub-mode-marketing-page.md`.

### Dashboard page

For any page under `STRUCTURE.md`'s `dashboard` / `app` / `admin` surface. Inputs are narrower (no marketing canon required, but a page brief is mandatory — even a one-paragraph spec). Emphasis in Phase 2 is on information density and scan paths (Z-pattern, F-pattern, sidebar-anchored). Phase 4 leans on data shape — what's the loading state, the empty state, the error state, the partial-data state. Phase 6 is client-component-friendly (most dashboard pages need interactivity).

→ See `references/sub-mode-dashboard-page.md`.

---

## Hard rules

- **No file writes before Phase 6.** Phases 1–5 happen entirely in chat. Any urge to write a "plan file" or "scratch doc" mid-flow is wrong — the chat conversation IS the plan, and the page file IS the final artifact.
- **No intermediate content mirror file.** Copy is inlined directly in the page JSX, sourced from `agents/marketing/copy/<slug>.md`. Do NOT create `marketing-content.ts`, `lib/copy.ts`, `data/content.ts`, or any similar runtime mirror. The canonical markdown is the source; the agent propagates changes when the user asks.
- **Cross-tier imports are blocked** (inherited from `build-component`). Marketing pages never import from `app/`. App pages never import from `marketing/`. Cross-tier needs go to Generic + wrapper.
- **One approval per phase.** Each phase ends with an explicit gate. Skipping ahead is forbidden — even if the user seems to imply approval, ask once.
- **Phase 5 build-new calls run sequentially, not in parallel.** Each net-new component gets its own focused conversation inside `build-component`. Bundling them produces the exact code-dump pathology this skill exists to prevent.
- **Marketing pages are RSC + `generateMetadata` by default.** The page-level component is a Server Component. Client behavior (auth redirects, search inputs, modal triggers) lives in small child components. No top-level `"use client"` on marketing pages.
- **Inline copy carries a canon-pointer comment.** Phase 6 always writes the `// Copy mirrors agents/marketing/copy/<slug>.md …` comment at the top of the file. This is the sync contract.
- **`design-check` fires automatically after Phase 6.** Don't duplicate its 8 steps here. `build-page` is the path-of-compose; `design-check` is the gate-of-correctness for what got composed.
- **Never modify canon from this skill.** No edits to `DESIGN.md`, `FUNDAMENTALS.md`, `STRUCTURE.md`, `BRAND.md`, or any `agents/marketing/*` file. If canon needs to change, the user is told to update the canon first, then re-invoke `build-page`.
- **Skip the marketing-content.ts pattern entirely.** If the project already has a `lib/marketing-content.ts` (or similar) from earlier ad-hoc work, do not write to it. Phase 6 inlines copy directly in the page and leaves the mirror file alone. A follow-up cleanup pass (separate skill or manual edit) can retire the mirror once all pages migrate.

---

## Sub-agent routing

Heavy reasoning steps delegate to Task tool sub-agents to keep orchestration context lean:

| Step | Tier | Why |
|------|------|-----|
| Phase 1 canon-read + synthesis | fast | Pure extraction |
| Phase 2 layout architecture proposal | reasoning | Judgment on section order + rhythm |
| Phase 3 hierarchy proposal | reasoning | Judgment on emphasis per section |
| Phase 4 asset manifest proposal | reasoning | Judgment on visual treatment + interactions |
| Phase 5 reuse scan (glob + read-similar) | fast | Pattern matching |
| Phase 5 strategy proposal per section | reasoning | Reuse / adapt / build judgment |
| Phase 5 inline build-component calls | (delegated) | build-component handles its own routing |
| Phase 6 wire-up code generation | reasoning | Composition + token discipline |

Never the most expensive model. Reasoning tier (Sonnet) is the ceiling.

---

## Output shape (end of skill)

```
build-page — summary

Built: <page slug> (<tier>)
Sections: <N>
Strategies: <N reused, N adapted, N built new>
Location: <file path written>

Components used:
  - <component 1> from <path>  [reused]
  - <component 2> from <path>  [adapted — added variant `compact`]
  - <component 3> from <path>  [built new via build-component]
  - <component 4> from <path>  [built new via build-component]

Copy sourced from: <agents/marketing/copy/<slug>.md | dashboard brief>
Canon-pointer comment: written at file top.

Tokens used:
  - <token 1>, <token 2>, <token 3>, …

Next:
  → design-check will run automatically against the written page file.
  → If any net-new components had missing tokens, those remain pending until
    you confirm in design-check Step 4.
```

---

## Difference from related skills

- **`marketing-brief`** — the planning pass that locks the marketing-site canon (CONTENT, SITEMAP, briefs, copy, MEDIA, layouts) ONCE near the end of a project. `build-page` is the execution pass that turns those plans into real pages. `build-page` is invoked per page; `marketing-brief` is invoked once for the whole site.
- **`build-component`** — atomic. One component, one file, one approval gate. `build-page` orchestrates composition and calls `build-component` inline whenever Phase 5 decides "build new" for a section. They chain: `build-page` is the conductor, `build-component` is the player. Atomic component requests from the user still go directly to `build-component`.
- **`design-direction`** — locks brand identity (`BRAND.md` + `DESIGN.md` Overview + refusal list) ONCE at the start. Upstream of every page build.
- **`design-check`** — UI write-time gate. Fires automatically after `build-page`'s Phase 6 (and after every inline `build-component` call inside Phase 5).
- **`discussion-mode`** — pure conversation, no writes. If the user wants to talk through a page idea without committing to architecture, use that first, then `build-page` to actually compose.
- **`init-project`** — bootstraps the three-folder layout. `build-page` assumes init-project + design-direction + (for marketing pages) marketing-brief have already run.

Chain: `init-project` → `design-direction` → `build-component` (per atomic piece, ongoing) → `marketing-brief` (once, end of project) → **`build-page`** (per page, ongoing) → `design-check` (auto, after each write) → `audit` (periodic).

---

## Why it exists

A page is not a big component. Forcing page-scale work through `build-component`'s atomic gate produces a code drop the user cannot meaningfully review: no layout conversation, no hierarchy debate, no asset plan, no reuse audit — just 400 lines of TSX and an "approve / edit / restart" button. The architectural decisions get buried inside the code and either get rubber-stamped or rejected wholesale.

`build-page` separates the architectural conversation from the code generation. The user makes one decision per phase, in chat, against a clear proposal — section count, then hierarchy, then assets, then component selection — and only sees code after every architectural question has been answered. The final wire-up is a single approval gate on a file that just composes already-decided pieces.

This also fixes the canonical-truth problem. With `build-component` swallowing whole pages, agents started inventing intermediate mirror files (`marketing-content.ts` etc.) to hold the copy that didn't fit cleanly in the JSX. Those mirrors became a third source of truth and drifted from `CONTENT.md`. `build-page` kills the mirror entirely: copy is inlined in the JSX, sourced from `agents/marketing/copy/<slug>.md`, and a comment at the top of the page file documents the canon-pointer for future agents. The propagation mechanism when canon changes is just *"agent, update the affected pages"* — no codegen, no build step, no drift.
