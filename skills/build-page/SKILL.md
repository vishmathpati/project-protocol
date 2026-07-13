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

UI Research remains optional. But when `brain/research/concepts.md` exists for this page/surface, verify its `## Human selection` block before claiming the composition is research-grounded. `Status: pending`, a missing block, or an incomplete focus/selector/date/included-moves record means the human checkpoint was not completed: stop and route back to UI Research. A BRAND/DESIGN lock, pinned URL list, existing dashboard, or completed teardowns cannot substitute for explicit human selection.

## Lock page intent

Confirm page goal, audience state, primary conversion, required content, real assets, constraints, and definition of done. Do not re-ask Foundation, Brand, or Marketing questions already answered.

## Create the Page Blueprint with the user

Do not begin by asking the user to pick components, and do not make a generic wireframe independently of the selected concept. Use this order:

1. **Content inventory** — identify what the page must communicate and what proof/CTA/content is already locked.
2. **Section jobs and narrative order** — propose the smallest coherent sequence based on meaning. No card/carousel/layout choice yet.
3. **Concept expression** — map the human-selected concept or blend to the page's hierarchy, rhythm, navigation, imagery, type, and motion.
4. **Pattern choice** — for each section, offer at most three relevant options grounded in selected research and existing project components (for example editorial band vs cards vs carousel), explain the trade-off in plain language, and let the human choose. Recommend one but never silently assume it.
5. **Media plan** — convert the approved sections into implementation-ready media slots before promising visual completeness.

Work section by section. For each section record its job, content source, approved presentation pattern, visual anchor, selected research evidence, reuse/build decision, media slot, and responsive/motion behavior. The Page Blueprint is a decision conversation, not a separate source-of-truth file.

External references provide layout or behavior evidence; adapt them to our content, tokens, assets, accessibility, and stack. Never copy proprietary code/assets. If implementation mechanics are unclear, use Inspect Component. If a genuinely missing component is needed, call Build Component.

Use `references/media-lifecycle.md` for every meaningful image, video, illustration, or bespoke mark. `brain/marketing/MEDIA.md` owns requirements/source/status. Routine icons come from the locked DESIGN family or existing component system without asking the human; only bespoke marks need an asset decision.

Safe prototypes may use owned/licensed media, approved AI generations, or neutral placeholders. Competitor/reference media remains research-only. A full-bleed or load-bearing placeholder means human approval is structural, not final visual approval. When real photography/video is missing, produce the approved AI prompt packet or photographer/videographer shot list rather than asking vaguely for “some images.”

Record approved page-specific choices in the chapter under `## Page Execution Decisions`: content inventory, section jobs/order, concept mapping, chosen patterns, media-slot IDs and replacement gates, component paths, and meaningful deviations. Do not create a separate page-state file or append page plans to BRIEF.

## Implement and verify

Reuse existing components first. For configured shadcn product/dashboard systems, use existing project components, then shadcn primitives, then compose an accessible project-system component only when neither exists. Brand-expressive marketing sections may be bespoke over accessible primitives.

Render at relevant viewports, self-critique rhythm/hierarchy/content fit, run Design Check postflight, run applicable tests, and then Completion Check against the chapter. Report evidence and untouched regions.
