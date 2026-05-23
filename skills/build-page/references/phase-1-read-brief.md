# Phase 1 — Read the brief

Goal: understand what this page is for, who it's for, and what content already exists for it — without writing anything.

## Tier detection

Pick marketing or dashboard by looking at:

1. **User's wording.** *"homepage / landing / pricing / about / features / customers / comparison / FAQ"* → marketing. *"dashboard / settings / overview / admin / analytics / team / billing"* → dashboard.
2. **STRUCTURE.md declared surfaces.** If the project only declares `dashboard` / `app` / `admin` and no `marketing` surface → dashboard regardless of wording. (Or halt and ask the user to add the marketing surface before continuing.)
3. **The slug.** A slug under `app/(marketing)/`, `pages/`, `web/`, `landing/` → marketing. A slug under `app/(dashboard)/`, `app/dashboard/`, `app/(app)/`, `admin/` → dashboard.

If two signals conflict, ask the user once: *"This looks like a [tier] page based on [reason], but the wording suggests [other tier]. Which is it?"*

## What to read — marketing tier

In this order, with `Task` sub-agent delegation for the heavy reads:

1. `agents/STRUCTURE.md` — surface list, marketing folder path, component folder path, cross-tier import rules.
2. `agents/marketing/SITEMAP.md` — find the row for this page slug. Extract: name, slug, single intent, primary CTA, audience descriptor.
3. `agents/marketing/briefs/<slug>.md` — audience state, single intent, story arc, section-by-section breakdown.
4. `agents/marketing/copy/<slug>.md` — every headline, subhead, button label, body paragraph.
5. `agents/marketing/layouts/<slug>.md` — block-level wireframe.
6. `agents/marketing/MEDIA.md` — find the section entries that match this page; note the visual-anchor type for each.
7. `agents/marketing/CONTENT.md` — only the rows referenced by this page (FEATURES, AUDIENCES, COMPARISONS, TESTIMONIALS, FAQS, LEGAL_PAGES as applicable).
8. `agents/BRAND.md` — archetype, tribe, refusal list, tempo axis.
9. `agents/DESIGN.md` Overview — surface tier, type scale, chart palette (rarely needed for marketing), section rhythm guidance.

## What to read — dashboard tier

1. `agents/STRUCTURE.md` — app folder path, component folder path, layout primitives (sidebar, topbar, content area).
2. The page brief — either a row in `agents/ROADMAP.md`, a dedicated file (e.g. `agents/specs/<slug>.md`), or a one-paragraph intent the user types in chat. If none exists, halt and ask: *"This page has no brief. Type a one-paragraph spec (what is it for, who uses it, what's the primary action) and I'll proceed."*
4. `agents/DESIGN.md` — surface tier, type scale (dashboard usually 1.125 ratio), chart palette, sidebar/topbar tokens.
5. `agents/FUNDAMENTALS.md` — banned words, density guidance, dashboard cardinal sins.
6. Existing dashboard components in the component folder — note what primitives exist (KPI tile, chart card, data table, sidebar nav, page header).

## Synthesis — what to surface

Write one short paragraph in chat. Template:

```
Page: <name> · slug: /<slug> · tier: <marketing | dashboard>

Audience: <one line — who's reading this>
Single intent: <one line — what we want them to do>
Primary CTA: <button label → href>

Content blocks already specified in the brief:
  1. <section name> — <one-line intent>
  2. <section name> — <one-line intent>
  …

Visual anchors from MEDIA.md (marketing only):
  §1 hero → screenshot of event detail
  §3 selfie moment → portrait-mode capture
  …

Components already in the project that look reusable:
  <component name> at <path>
  <component name> at <path>
  …

Ready to propose the section list (Phase 2)? Push back on anything above first.
```

Wait for an explicit *"yes, proceed"* or *"actually, this section needs…"* before advancing. Do not advance on a non-response. Do not advance on a question — answer it, then ask again.

## Failure modes — what to halt on

- **Marketing canon missing.** Halt: *"Marketing canon missing for `<slug>` — `briefs/<slug>.md` / `copy/<slug>.md` / `layouts/<slug>.md` not found. Run `marketing-brief` first (or add the missing files), then re-invoke `build-page`."*
- **Slug not in SITEMAP.** Halt: *"`<slug>` is not in `agents/marketing/SITEMAP.md`. Add it to SITEMAP (with intent + primary CTA + audience), then re-invoke."*
- **No STRUCTURE.md.** Halt: *"`agents/STRUCTURE.md` not found. Run `build-component` first (it writes STRUCTURE.md on first run) or `init-project` to bootstrap."*
- **No DESIGN.md or BRAND.md.** Halt: *"Canon missing — run `init-project` and `design-direction` first."*
- **Dashboard page with no brief.** Halt and ask the user to type a one-paragraph spec inline. Do not invent the spec.

## What NOT to do

- Do not skim the brief and proceed — read every section.
- Do not propose copy changes — the copy is locked in `copy/<slug>.md`. If the user wants to change copy, that's a separate edit to the canon, not a `build-page` concern.
- Do not propose CONTENT.md changes — same rule.
- Do not start sketching layouts in your head. Phase 1 ends with synthesis + approval, not with proposals.
- Do not skip the BRAND.md read for marketing pages — the archetype + tempo axis materially shape Phase 2's rhythm proposal.
