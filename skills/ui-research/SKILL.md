---
name: ui-research
description: "Optional two-round visual research for brand-facing or inspiration-dependent UI. Use when a user needs real-site concepts before choosing a landing-page, marketing, mobile, or desktop direction: sweep a niche into concepts, let the human pick or blend, then deeply tear down the selected concept. Does not auto-trigger for ordinary dashboards."
---

# UI Research

Ground a visual direction in real sites before Style Lock or Build Page. Research is evidence, not authority.

## Inputs

Read BRIEF, STRUCTURE, BRAND, Marketing Stage A outputs, target surface/page, DESIGN refusals, and TASTE. Ask for research depth (`quick | standard | deep`) here only; it tunes appetite, never a fixed site count.

Do not run automatically for standard dashboards, CRUD/settings/table/detail pages, or work where the existing system is sufficient.

## Round 1 — Sweep

Render the Round 1 mission from `references/mission-prompt-template.md` for the standalone Aside UI Research skill. Aside explores until saturation and returns named concepts grounded in real sites.

Capture representative hero and signature evidence—not every page and component. Ingest into:

- `brain/research/concepts.md`
- `brain/moodboard/manifest.md`
- local screenshots under `brain/moodboard/`

## Human checkpoint

Show the concepts and evidence. The human picks one, blends explicit parts, or requests more sweep. Record the Round 2 focus inside `research/concepts.md`; do not write BRAND or DESIGN and do not create a global selected-decisions file.

## Round 2 — Deep teardown

Use the same Aside chat. Deeply inspect the selected concept until saturation. Capture hero, meaningful middle/end sections, navigation, mobile, imagery/video, type, palette, motion, and inner pages/components only when they add materially new evidence.

Write:

- `brain/research/conventions.md`
- `brain/research/teardowns/<slug>.md`
- updated moodboard manifest/screenshots

Each teardown records URL, date, page, viewport, capture method, evidence, and clearly labeled inference. Extracted values inform our system; never copy another site's tokens, code, or assets.

## Finish

Report concepts, selected focus, convergence, disagreements, gaps, and paths written. Recommend Style Lock or Build Page as appropriate; never auto-chain.

The relay and file shapes live in `references/round-formats.md`. If Aside cannot write project files, the paste blocks remain the guaranteed transport.
