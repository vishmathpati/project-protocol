# Phase 4 — Asset manifest

Goal: per section, declare the visual treatment + micro-interactions. Still chat-only, no writes.

This is where the page gets its "feel" decisions: what's an image vs an illustration vs an icon-only treatment, whether anything animates, whether anything is sticky, what scrolls and what doesn't.

## Output shape — markdown table in chat

```
| § | Section          | Visual type        | Asset id (MEDIA.md)         | Interaction notes                |
|---|------------------|--------------------|-----------------------------|----------------------------------|
| 1 | Hero             | screenshot         | home-hero-event-detail.webp | static; no scroll-link           |
| 2 | Trust strip      | text + accent rule | —                           | none                             |
| 3 | How it works     | numbered cards     | —                           | hover: card lift + accent number |
| 4 | Features grid    | icon + text rows   | lucide icons (per CONTENT)  | none                             |
| 5 | Selfie moment    | portrait mockup    | home-selfie-capture.webp    | none (was scroll-reveal, dropped — see notes) |
| 6 | Camera coverage  | icon-three-up      | lucide icons                | none                             |
| 7 | Run-the-studio   | screenshot         | home-invoice-builder.webp   | none                             |
| 8 | FAQ              | accordion          | —                           | accordion expand/collapse        |
| 9 | Final CTA        | text-only          | —                           | none                             |
```

## Visual type — the canonical list

Pick from this set; do not invent new types without a note:

- **screenshot** — a real or mocked product screenshot. Anchors trust. Cite the MEDIA.md asset id.
- **illustration** — vector art, custom illustration, abstract graphic. Anchors brand.
- **photo** — real photograph of people / places / objects. Anchors humanity.
- **portrait mockup** — phone-frame screenshot. Anchors mobile-specific stories (Selfie Search, mobile app screens).
- **icon-three-up / icon-grid** — small icons with adjacent text, repeating. Anchors scannability for feature lists.
- **numbered cards** — visually distinct cards with a step number. Anchors process narratives ("how it works", "in three steps").
- **accordion** — text-only collapsible list. Anchors FAQ-shaped content.
- **data-mock** — fake-data table, chart, or KPI tile for dashboard mockup contexts.
- **text-only** — no visual; type and color do all the work. Anchors trust strips, final CTAs, simple proof sections.
- **text + accent rule** — text-only with a single accent line, divider, or color block. Anchors calm sections that need *some* visual weight.

## Asset id

For marketing pages, cross-reference `MEDIA.md`. If a section has a declared asset there, copy its id into this column. Do not propose new asset ids in this phase — if a section needs an asset that MEDIA.md doesn't have, halt and ask: *"§<n> needs an asset that's not in MEDIA.md. Add it there first, then we'll continue."*

For dashboard pages, asset ids are mostly empty — the visual is usually data or a chart, and the asset is "render this state from real or mock data, no static image needed". For mockup sections (e.g. an onboarding empty state), name the mock data shape: *"empty-state-no-events.mock"*.

## Interaction notes — the conservatism rule

Default to `none`. Every interaction needs a reason that maps to a `tempo` or `frequency` axis call from `BRAND.md`.

Allowed interactions, lowest to highest cost:

1. **Hover state beyond default** — e.g. card lift, accent reveal, color shift. Cheap. Use freely where it earns its keep.
2. **Accordion expand/collapse** — FAQ sections, advanced-settings sections. Free if a primitive exists in the project.
3. **Carousel / horizontal scroll** — only when content count exceeds vertical real estate. Avoid for primary content.
4. **Scroll-linked reveal** — element animates in as it enters viewport. Use sparingly; never for primary headlines (they should be visible immediately).
5. **Sticky element** — sidebar, top bar, footer cta-bar. Costly: takes vertical space permanently. Justify per use.
6. **Scroll-snap section** — page snaps section-by-section as user scrolls. Brand-driven choice; only when `tempo` is high and the page is genuinely scene-by-scene.
7. **Parallax / mouse-tracked animation** — costly to perform, easy to overdo, hostile to motion-sensitive users (always pair with `prefers-reduced-motion` opt-out). Use only when distinctiveness > friction.

For each proposed interaction beyond hover-default, write a one-line justification: *"§5 scroll-reveal — brand tempo: kinetic, this is the highest-emotion section on the page, supports archetype 'Magician'."*

If the user pushes back on an interaction or just goes *"no"* — drop it without argument. Defaulting to none is correct.

## Cross-cutting concerns to declare

Also surface in this phase, as a short footer below the table:

- **Sticky elements** — does the page have a sticky nav? Sticky footer CTA bar on mobile? Sticky sidebar on dashboard? Declare or confirm none.
- **Motion preference** — for pages with non-hover motion, explicitly state: *"All scroll-linked motion respects `prefers-reduced-motion: reduce` — disabled animations show the end state."*
- **Loading states (dashboard tier)** — for each data-mock section, declare what the loading skeleton looks like (text shimmer, blank cards, spinner per cell).
- **Empty states (dashboard tier)** — for each list/table/chart, declare the empty-state copy + illustration if any.
- **Error states (dashboard tier)** — what does the page show if the data fetch fails? Inline error, toast, redirect, fallback content.

## Approval gate

End the phase with:

```
Asset manifest proposed: <N> sections.
Net-new assets needed beyond MEDIA.md: <list, or "none">.
Interactions beyond hover: <list with justifications, or "none">.

Approve / trim / restart?
```

If user trims an interaction, drop it. If user requests a different visual type for a section, swap it. Re-show the full table (it's small), then ask again.

## What NOT to do

- Do not propose specific Tailwind classes, CSS values, or animation timings. Phase 4 is about *what* the visual treatment is; Phase 6 picks the tokens.
- Do not invent new asset ids — they must come from MEDIA.md (or be deferred to a MEDIA.md update before Phase 5).
- Do not propose interactions because they're "cool" — every one needs a brand-axis justification.
- Do not skip the loading/empty/error declarations for dashboard pages — those are 80% of dashboard correctness.
- Do not declare animations the project's design system can't actually deliver. If `DESIGN.md` has no motion tokens (no duration, easing, transform definitions), interactions beyond hover are off the table without a Phase 4 amendment to add them — which would require a separate `design-direction` or `design-check` pass first.
