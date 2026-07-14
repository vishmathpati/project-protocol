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

Resolve the project root with `git rev-parse --show-toplevel` when Git is available. Read the recommendation packet, submitted draft, approved chapter record, assets, and implementation only from that same active checkout. Never mix state from a sibling or main checkout merely because it has newer-looking files.

UI Research remains optional. When `brain/research/page-recommendations.json` exists for this site/surface, validate its checkout identity and stable target/recommendation IDs, then use only IDs approved in the chapter's locked site-direction record. A recommendation packet, `ui-decision-draft.json`, dashboard state, BRAND/DESIGN lock, pinned URL list, existing page, or completed teardown cannot substitute for the approved chapter record. Legacy concept-selection notes may remain as evidence but do not bypass the site-wide gate.

### Site-wide decision gate

For a research-led marketing website, read the exact `## Approved Site Direction` block defined in `references/site-direction-lock.md`. A dashboard submission is a proposal: **submitted is not locked**. Before the first page build, require human-approved site direction, reviewed global-shell decisions (including an explicit `not_needed` where applicable), and a reviewed direction for every unique page and page family in the sitemap. Missing, submitted, reopened, partial, or `conflicting` decisions stop before implementation and route to the site-wide review. This gate does not apply to ordinary product/dashboard work that did not enter the research-led marketing workflow.

### Activate one page

Activate only the page or representative family page named by the chapter. Load the locked global shell, approved homepage when it exists, previously approved or built pages, page-family siblings, and the current component inventory. Before page-specific decisions, return one compatibility status using the same machine vocabulary as the site lock:

- `compatible` — proceed without changing the approved direction.
- `compatible_with_adaptation` — explain and record the smallest changes that preserve the shared system.
- `conflicting` — stop and resolve the conflict with the human; never normalize it silently.

For the homepage chapter, follow FUNDAMENTALS: implement and verify the **shell slice first** (navigation structure, footer, page skeleton, and base primitives), then compose homepage sections. A page-coupled header may be reviewed with its hero, but it must still honor the locked navigation architecture and other-page behavior.

Read any validated `deferred_component_intents` in the approved submission. A deferred component intent is not a component choice and never bypasses the site-wide gate. Ask the human to provide it **only when its exact page or representative family becomes active** and the named affected block is reached. Then compare it with the locked site direction, global shell, approved homepage and prior pages, page-family siblings, design system, active content job, responsiveness, accessibility, and media needs. Reuse or adapt it when compatible; use Inspect Component when exact mechanics are unclear; use Build Component only when the project genuinely lacks the required component. Record the outcome in the active page's execution decisions.

For a page family, build and verify the representative page/template first, check its shared pattern against every member and recorded exception, then apply the approved family to the remaining members without reopening the direction. A member whose exception changes the composition becomes its own active page decision.

## Lock page intent

Confirm page goal, audience state, primary conversion, required content, real assets, constraints, and definition of done. Do not re-ask Foundation, Brand, or Marketing questions already answered.

## Create the Page Blueprint with the user

Do not begin by asking the user to pick components, and do not make a generic wireframe independently of the selected concept. Use this order:

1. **Content inventory** — identify what the page must communicate and what proof/CTA/content is already locked.
2. **Section jobs and narrative order** — propose the smallest coherent sequence based on meaning. No card/carousel/layout choice yet.
3. **Whole-page direction** — apply the approved site/page-family direction to the page's hierarchy, rhythm, navigation, imagery, type, and motion.
4. **Connected-section sequences** — identify sections whose shared background, transition, scroll behavior, or narrative depends on staying together. Approve each connected-section sequence as one composition before discussing its parts.
5. **Pattern choice — optional section overrides** — only where a section genuinely needs a different expression, offer at most three options grounded in selected research and existing project components. Explain the trade-off in plain language and let the human choose; never mechanically slice a coherent page into unrelated components.
6. **Media plan** — convert the approved composition into implementation-ready media slots before promising visual completeness.

For each whole page, connected sequence, and optional section override, record its scope, job, content source, approved presentation pattern, visual anchor, selected research evidence, reuse/build decision, media slots, and responsive/motion behavior. A reference may propose a coupled **hero/header** treatment; present that dependency to the human and global-shell review, but never silently select it or change global navigation on the hero's behalf. The Page Blueprint is a decision conversation, not a separate source-of-truth file.

External references provide layout or behavior evidence; adapt them to our content, tokens, assets, accessibility, and stack. Never copy proprietary code/assets. If implementation mechanics are unclear, use Inspect Component. If a genuinely missing component is needed, call Build Component.

Use `references/media-lifecycle.md` for every meaningful image, video, illustration, or bespoke mark. `brain/marketing/MEDIA.md` owns requirements/source/status. Routine icons come from the locked DESIGN family or existing component system without asking the human; only bespoke marks need an asset decision.

Safe prototypes may use owned/licensed media, approved AI generations, or neutral placeholders. Competitor/reference media remains research-only. A full-bleed or load-bearing placeholder means human approval is structural, not final visual approval. When real photography/video is missing, produce the approved AI prompt packet or photographer/videographer shot list rather than asking vaguely for “some images.”

### Page Asset Request

Before implementation, present one consolidated human-readable request grouped into available, required, provisional, and blocked assets. Include all page **images**, **videos**, video **posters**, **illustrations**, **logos**, **bespoke marks**, and any **other load-bearing assets** such as 3D, audio, maps, embeds, or documents. For every slot state the quantity, page/section purpose, required dimensions/behavior, existing path, source route and rights, availability / next action, responsive variant, and replacement gate. Routine icons are automatic from the locked icon family and must not become user questions.

Record approved page-specific choices in the chapter under `## Page Execution Decisions`: locked site-direction revision, active page/family, global-shell and prior-page context, compatibility verdict/adaptations, content inventory, whole-page/connected/override scopes, media-slot IDs and replacement gates, component paths, and meaningful deviations. Do not create a competing page-state file or append page plans to BRIEF.

## Implement and verify

Reuse existing components first. For configured shadcn product/dashboard systems, use existing project components, then shadcn primitives, then compose an accessible project-system component only when neither exists. Brand-expressive marketing sections may be bespoke over accessible primitives.

Render at relevant viewports, self-critique rhythm/hierarchy/content fit, run Design Check postflight, run applicable tests, and then Completion Check against the chapter. Report evidence and untouched regions.
