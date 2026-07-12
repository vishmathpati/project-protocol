---
name: build-page
description: Compose and implement a substantial brand-facing page through an iterative conversation using locked content, design canon, optional UI research, and existing components. Also usable explicitly for unusual product UI, but does not auto-trigger for ordinary dashboard CRUD, settings, tables, or detail pages.
---

# Build Page

Own page composition and implementation. Marketing owns meaning; Style Lock owns tokens; Build Page decides how one page becomes a coherent experience.

## Route correctly

- Brand-facing marketing/content page → Build Page is required.
- Conventional dashboard/product UI using an established system → role/chapter may build directly with shadcn and existing patterns; Build Page is optional.
- Standard CRUD/settings/table/detail work → never trigger UI Research or Aside automatically.
- A substantial page normally belongs to one chapter. Small page edits may stay inside an existing chapter.

## Read the contract

Read the chapter, BRIEF, STRUCTURE, BRAND, DESIGN, FUNDAMENTALS, TASTE, applicable marketing brief/copy/media, relevant UI research, and existing route/component system. Follow the project's actual architecture.

## Lock page intent

Confirm page goal, audience state, primary conversion, required content, real assets, constraints, and definition of done. Do not re-ask Foundation, Brand, or Marketing questions already answered.

## Compose with the user

Propose one coherent section sequence tied to real content. Work section by section in a long iterative conversation. For each section, identify its job, content source, visual anchor, selected research evidence if any, existing component reuse, and responsive/motion behavior.

External references provide layout or behavior evidence; adapt them to our content, tokens, assets, accessibility, and stack. Never copy proprietary code/assets. If implementation mechanics are unclear, use Inspect Component. If a genuinely missing component is needed, call Build Component.

Record approved page-specific choices in the chapter under `## Page Execution Decisions`: selected research patterns, composition, assets, component paths, and meaningful deviations. Do not create a separate page-state file or append page plans to BRIEF.

## Implement and verify

Reuse existing components first. For configured shadcn product/dashboard systems, use existing project components, then shadcn primitives, then compose an accessible project-system component only when neither exists. Brand-expressive marketing sections may be bespoke over accessible primitives.

Render at relevant viewports, self-critique rhythm/hierarchy/content fit, run Design Check postflight, run applicable tests, and then Completion Check against the chapter. Report evidence and untouched regions.
