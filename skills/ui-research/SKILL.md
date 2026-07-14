---
name: ui-research
description: "Optional real-site UI research for inspiration-dependent marketing work. Map a site and its page families to evidence-backed recommendations, support open or pinned discovery and focused follow-ups, and stop for site-wide human review. Does not auto-trigger for ordinary dashboards."
---

# UI Research

Ground a marketing site's direction in real evidence before Build Page. Research recommends; the
human decides; Claude or Codex validates the submitted combination; only approved Markdown becomes canon.

## Resolve project state

Read BRIEF, STRUCTURE, BRAND, DESIGN, TASTE, Marketing Stage A outputs, sitemap, page briefs/copy,
available MEDIA, current chapter, and the user's stated scope. The user's explicit target and reference
constraint outrank STATUS/ROADMAP next actions. Never redirect homepage research to the next queued page.

Build a **site and page map** before composing the mission. Preserve stable family and target IDs from
the sitemap; when absent, create deterministic slug IDs without changing routes. Represent every unique
page or repeated page family once, including special, utility, and legal groups when they require visual
review. Each target carries its routes, content goal, and content jobs. A single-page project has one
target. Do not invent missing content strategy; ask only when a missing goal would change the research.

Use the five scope labels exactly: `whole-page`, `connected-sections`, `one-section`,
`repeated-page-family`, and `global-shell`. A header that depends on a hero is a declared dependency,
not an automatic global choice. Routine design-system icons are not asset questions; bespoke marks are.

Choose the entry mode without a menu dump:

- **Open discovery** — search the field to saturation and create site-wide/page-aware recommendations.
- **Provided-reference concept discovery** — use every pinned URL and no others, reuse verified evidence,
  group the closed set, and create the same page-aware recommendations.
- **Selected-focus teardown** — after an approved site-wide direction exists, inspect the selected page,
  connected sequence, or section deeply enough to support its eventual build.
- **Focused pattern follow-up** — find additional alternatives for one exact target/block whose current
  recommendations are insufficient. Preserve all other target recommendations and site direction.

A supplied URL list, existing design system, old moodboard, current homepage, or agent recommendation is
a constraint—not concept selection. Aside must never create a human selection or build lock.

Ask only for genuinely missing target/scope, pinned URLs, material page goal, or research depth
(`quick | standard | deep`). Recommend `standard` when unstated. Manual Aside paste-prompt is the default
transport. Do not offer another browser unless requested or Aside is unavailable.

## Worktree identity and relay

Resolve the current checkout with `git rev-parse --show-toplevel`, branch, and HEAD. `<brain-abs>` is that
checkout plus `/brain`. In a worktree, always point Aside at that worktree; never a sibling or main checkout.
Include a stable mission ID and the checkout identity in the mission and packet.

Aside writes canonical Markdown evidence under `brain/research/` and `brain/moodboard/`. It also writes
the optional derived relay `brain/research/page-recommendations.json` using the exact packet in
`references/round-formats.md`, preserving stable IDs on update. It prints the identical packet every time;
if disk access fails, the paste packet is self-sufficient and Project Protocol writes it into this checkout.

## Discovery — site-wide recommendation pass

Render Variant A for open discovery or Variant C for a pinned set. Append the PAGE_RECOMMENDATIONS packet
contract to the rendered mission. Aside first identifies field concepts, then maps evidence-backed options
to every target in the site/page map. Recommendations explain content fit in plain language and attach live
URLs, grouped screenshots, video/motion evidence, confidence, material gaps, dependencies, and required
images/videos/bespoke icons/other assets. Research stops by saturation, never a target count.

For every target, return at least one base recommendation with `whole-page` scope, or
`repeated-page-family` when the target represents a repeated family. Connected sequences and
`one-section` recommendations are optional refinements after that base; they never replace it.

Ingest and validate:

- `brain/research/concepts.md`, `conventions.md`, and `teardowns/` where produced;
- `brain/moodboard/manifest.md` and local evidence;
- `brain/research/page-recommendations.json` as derived relay data.

Reject a packet with a wrong checkout root, missing target IDs, missing recommendation scope, dangling
evidence/dependency IDs, absent material-gap classification, a global-shell target other than exactly
`global-shell`, or a global-shell state outside `recommended | not_needed`. Every target must have a base
whole-page/page-family recommendation or an explicit material blocker; section-only output is incomplete.
`evidence_readiness` reports research-evidence readiness
only; it never authorizes teardown or implementation.

## Site-wide human checkpoint

After discovery, explicitly invoke Project Dashboard. It presents the overall direction, global shell,
and every page/page-family recommendation before any page build. The dashboard may collect provisional
review state, but Aside and the derived recommendation packet never record human choices.

The checkpoint is a visual decision interface, not a raw Markdown mirror. It shows each recommendation
at a useful viewing scale, one recommendation at a time within its target, with grouped site evidence,
live links, scope, content fit, dependencies, asset needs, confidence, and gaps.

The human reviews the entire site and uses one universal submit action. Project Dashboard writes the
provisional `brain/research/ui-decision-draft.json`; Claude or Codex reads it and owns the exact combination
statuses `compatible`, `compatible_with_adaptation`, and `conflicting`, asking only about material conflicts.
Recommendation-level research carries notes and dependencies, not this verdict. After explicit human
approval, write and validate the canonical `## Approved Site Direction` Markdown record using
`source/skills/build-page/references/site-direction-lock.md`. It must be complete and locked; canonical
research evidence is not an approved design selection. Until then, no selected-focus teardown or Build Page
is authorized.

## Focused follow-up and selected teardown

Use Variant E when the user requests another pattern for one exact target/block. Carry the current mission
ID, checkout identity, target/block IDs, content job, current candidates, constraints, and narrow question.
Do not reopen the site-wide direction, replace unrelated recommendations, or broaden into a new sweep.
Merge new candidates by stable recommendation/evidence IDs.

Use selected-focus teardown only for approved target/recommendation IDs and the named page/region. Require
honest desktop/mobile capture states; loaded fonts/images/video/layout; live URL; screenshot paths; actual
video role/playback/fallback; motion behavior; evidence versus inference; and confidence/material gaps.

If the human already has an exact URL and wants to know how one region works, route to **Inspect Component**
instead. UI Research finds alternatives; Inspect Component performs exact-URL implementation forensics.

## Finish

Report entry mode, checkout identity, site/page coverage, recommendation count, evidence gaps, packet path,
dashboard path, and the single next human action. Never auto-chain to Style Lock, Build Page, or a build.
