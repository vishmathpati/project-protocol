# Phase 3 — Hierarchy

Goal: for each approved section from Phase 2, declare what's primary, secondary, and tertiary — where the eye lands first, what the load-bearing claim is, what's supporting.

Still no code, no JSX. Output is a short paragraph per section, in chat.

## What to propose per section

One paragraph per section, three lines:

```
§<n> <section name>
  Primary   — <what the eye lands on first; the load-bearing element>
  Secondary — <what supports the primary>
  Tertiary  — <fine print, CTAs, links, decorations>
```

Example:

```
§1 Hero
  Primary   — H1 claim ("The operating system for event-photography businesses")
  Secondary — one-line subhead + visual anchor (event detail screenshot)
  Tertiary  — primary + secondary CTA pair; "1 event free for life" reassurance line
```

```
§4 Features grid
  Primary   — the four workflow-stage column headers (Capture / Deliver / Approve / Run-studio) — these carry the positioning ("galleries are one column out of four")
  Secondary — feature name + icon per row
  Tertiary  — feature blurb (one line each)
```

## How to decide primary

The primary element answers *"what's the one thing the reader takes away from this section if they only look at it for one second?"* It's almost always:

- The headline (for narrative sections).
- The visual anchor (for image-led sections where the image is the proof).
- The data point (for stat / trust-strip sections).
- The price (for pricing tier cards).
- The CTA (for the final-CTA section only).

One primary per section. If a section has two equally-weighted things competing for the eye, the section is broken — flag it and propose a split or a re-rank.

## How to decide secondary

Secondary supports primary. Subheads, visual anchors paired with headlines, supporting copy, the second-most-important data point. If primary is a claim, secondary is the proof or the illustration. If primary is a screenshot, secondary is the caption that tells you what to notice in it.

## How to decide tertiary

Tertiary is the fine print, the third-rank CTAs, the reassurance lines ("no card required"), the legal microcopy, the decorative elements. Cuttable in a tight redesign.

## Cross-section consistency

After per-section hierarchy is proposed, do a quick consistency pass:

- Are there two competing H1s on the page? There should be one — the hero. Everything else is H2.
- Does every section that needs a CTA have one declared as primary or tertiary? (Sections without a CTA are fine — they're the calm middle. But if Phase 2 tagged a section as `loud` with intent "drive action", it needs a CTA at primary or tertiary.)
- Does the "one CTA per page" rule from `marketing-brief` hold? Each section can have its own section-level CTA (text link, "Learn more" arrow), but only one section is the *page's* primary CTA recipient — usually the hero and the final CTA, pointing to the same destination.

## Approval gate

End the phase with:

```
Hierarchy proposed for all <N> sections.

Approve / push back on specific sections / restart?
```

If user pushes back on one section ("§4 — primary should be the icons, not the headers"), revise that section's paragraph, re-show, ask again. Don't re-show every section if only one changed.

## What NOT to do

- Do not propose specific font sizes here. The type scale is in `DESIGN.md` and Phase 6 will resolve "primary" to the right scale step automatically.
- Do not propose colors or backgrounds. That's Phase 4 territory (asset manifest declares the visual treatment) and Phase 6 territory (the actual token application).
- Do not propose specific component choices ("use the existing Hero component"). That's Phase 5.
- Do not write hierarchy paragraphs for sections that don't exist in Phase 2's approved list. If hierarchy work suggests a missing section, surface that as a Phase 2 amendment: *"While working on hierarchy I noticed §6 has no place to surface the camera list — should we add a §6.5 'Coverage at a glance'? Or roll it into §6 secondary?"*
- Do not skip sections. Even a calm trust-strip section gets a 3-line paragraph; its primary might just be the three claims read as a unit.
