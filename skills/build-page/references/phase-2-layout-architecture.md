# Phase 2 — Layout architecture

Goal: propose the page's section list (count, order, rhythm) drawn from the brief — and get explicit approval before any further work.

This phase is conversational. No code, no JSX, no file writes. The output is a vertical outline in chat that the user can read in 20 seconds.

## What to propose

A numbered section list. Each section gets:

1. **Section name** — descriptive, not invented. Pull from the brief's section names if they exist; otherwise infer from the content blocks.
2. **One-line intent** — what this section is *for*. Not a description of what's in it, but what job it does for the reader.
3. **Visual anchor type** — image / screenshot / illustration / icon-grid / accordion / data-mock / text-only.
4. **Rhythm tag** — `calm` (open spacing, low contrast, single anchor) or `loud` (dense, high contrast, multiple anchors, motion).

Example:

```
1. Hero          — claim + primary CTA          · image          · loud
2. Trust strip   — answer the trust question early · text + accent  · calm
3. How it works  — 3-step narrative              · numbered cards · calm
4. Features grid — workflow-stage breakdown      · icon grid (4 cols) · loud
5. Moment 1      — Selfie Search story           · portrait image · calm
6. Camera coverage — kit list + 3 paths          · icon-three-up  · calm
7. Moment 2      — Run-the-studio                · screenshot     · loud
8. FAQ           — 8 questions                   · accordion      · calm
9. Final CTA     — single ask                    · text-only      · loud
```

## How to decide section count

Marketing pages: 5–10 sections is the safe band. Below 5 the page feels thin; above 10 the page feels like a sales letter. Homepage skews toward the upper end (8–10), feature/comparison pages toward the lower (5–7).

Dashboard pages: usually 2–5 zones (page header, KPI strip, primary content, secondary content, table/list). Dashboard pages are not narratives; they're tools. Do not invent narrative sections.

## How to decide section order

Marketing pages — classic arc:

1. **Claim** (hero) — what this is.
2. **Trust** (trust strip / proof bar) — why we don't fall over.
3. **How** (3-step or workflow) — what using this looks like.
4. **Surface** (features grid / coverage / scope) — what's in the box.
5. **Moments** (one or more story sections) — the specific scenes the product unlocks.
6. **Social proof** (testimonials / logos / case studies) — others vouching.
7. **Answer** (FAQ) — pre-empt the objections.
8. **Ask** (final CTA) — close.

Not every page needs all eight. Pricing pages collapse most into a tier table + FAQ. Comparison pages reorder around a side-by-side. About pages drop the FAQ and lean on story.

Dashboard pages — no narrative arc. Order by user task:

1. **Header** — page title + breadcrumbs + page-level actions.
2. **Status / KPIs** — what does the user need to know in 2 seconds.
3. **Primary work area** — the chart, the table, the form, the canvas.
4. **Secondary** — supporting widgets, recent activity, suggested actions.

## Rhythm — the calm/loud pattern

A page with all-loud sections is exhausting; all-calm is forgettable. Alternate. Look at the proposed list and ask: *does the eye get a place to rest every 1–2 sections?*

Typical rhythm: `loud → calm → calm → loud → calm → calm → loud → calm → loud`. Bookended loud, eased middle.

The `tempo` axis from `BRAND.md` modulates this: a brand with `tempo: slow / editorial` skews more calm sections, fewer anchors per page, more whitespace. A brand with `tempo: fast / kinetic` allows more loud sections, denser grids, more motion.

## How to read MEDIA.md into this phase

For marketing pages, `MEDIA.md` already declared a visual-anchor type per section during `marketing-brief`. Use those declarations as the *starting point* for the visual-anchor column. If you propose a different type for a section, call it out explicitly: *"MEDIA.md declares 'screenshot' for §5 but I'm proposing 'portrait-mode mockup' because [reason] — confirm or revert."*

Do not silently override MEDIA.md. The user wrote it once and should approve changes consciously.

## Approval gate

End the phase with:

```
Section count: <N>
Rhythm: <e.g. "loud-calm-calm-loud-calm-calm-loud-calm-loud" or "tool-shaped: header / KPIs / primary / secondary">

Approve / push back / restart?
```

If user pushes back ("drop section 3", "swap 5 and 6", "add a logo wall after the hero") — apply the change, re-show the full list, ask again. Do not advance to Phase 3 on partial approval.

## What NOT to do

- Do not propose copy changes — copy is locked.
- Do not propose visual styling or token choices — that's Phase 4's job.
- Do not generate sketches in HTML/ASCII art — a numbered list is enough and faster to read.
- Do not propose sections that have no source in the brief. If the brief doesn't mention testimonials and TESTIMONIALS in CONTENT.md is empty, do not invent a testimonial section.
- Do not skip the rhythm tags — a page list without rhythm is the most common cause of feature-bag pages.
