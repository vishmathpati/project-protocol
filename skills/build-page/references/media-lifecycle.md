# Media lifecycle for page building

`brain/marketing/MEDIA.md` is the single asset-status source of truth. The chapter records only the page-specific mapping and approvals.

## Source routes

- `owned/client-supplied` — preferred; record the human's ownership or permission attestation.
- `commissioned` — turn the approved slots into a shot list.
- `ai-generated` — create a prompt packet; generate only when the host supports it and the human approves, otherwise return the prompt.
- `licensed-stock/render` — record the source and license.
- `neutral-placeholder` — safe layout-only stand-in.
- `reference-only` — research evidence; never an implementation asset.
- `not-needed` — the section works without media.

Never download, hotlink, embed, or ship a competitor's image/video as an implementation shortcut unless the user owns it or has explicit permission. A research screenshot may remain in the private moodboard. Recreate the behavior with owned, licensed, generated, or neutral media.

## Implementation-ready slot

For each required slot record: page/section job; still/video/icon/illustration type; what it must communicate; aspect/orientation; focal point and text-safe area; responsive crop; alt/description; source route; rights/provenance; current path; stage; and replacement gate.

Video additionally records duration, poster, autoplay/muted/loop, sound, controls, mobile treatment, reduced-motion/static fallback, and hosting source.

Stages are `required`, `awaiting-source`, `prototype-ready`, `final-ready`, `blocked`, or `retired`. Replacement gates are `none`, `before visual approval`, or `before completion`.

## Acquisition packets

### Photographer / videographer

Create a shot list only after page composition is approved: subject/action, placement, aspect/orientation, focal point and negative-space safe area, time/light, still/video duration, responsive variants, and exclusions.

### AI generation

Create a paste-ready packet containing purpose/message, subject/action, composition, aspect/orientation, focal point and negative-space safe area, light/time, brand treatment, realism/material, responsive variants, and exclusions such as no text/logos.

Record provider/model/date and representation risk. AI can be final for approved illustrative texture or non-factual artwork. It is prototype-only when it would fabricate a real property, room, restaurant, product, customer, or proof. Human approval and the project's rights policy are still required.

## Gates

1. **Blueprint gate** — every requirement says what it communicates, not merely “beautiful image.”
2. **Prototype gate** — every slot has a safe provisional route.
3. **Visual-approval gate** — load-bearing/full-bleed media is final, or approval is explicitly structural only.
4. **Completion gate** — final path, permission/provenance, crop, alt, poster/fallback, responsive behavior, and performance are verified. Required replacements cannot silently pass.

Routine UI icons come from the locked DESIGN family or existing component system and do not require a MEDIA row. A logo, custom glyph, illustration, or other bespoke brand mark does.
