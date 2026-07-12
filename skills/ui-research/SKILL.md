---
name: ui-research
description: "Optional real-site UI research for brand-facing or inspiration-dependent work. Use discovery mode to sweep a field into concepts before direction selection, or provided-reference mode to deeply inspect only user-pinned websites for a locked page/direction. Does not auto-trigger for ordinary dashboards."
---

# UI Research

Ground a visual direction in real sites before Style Lock or Build Page. Research is evidence, not authority.

## Resolve the invocation

Read BRIEF, STRUCTURE, BRAND, Marketing Stage A outputs, the user-stated target surface/page, DESIGN refusals, and TASTE. The user's explicit target and reference constraint outrank STATUS/ROADMAP next actions. Never redirect homepage research to the next queued page.

Choose without a menu dump:

- **Discovery mode** — the user wants new concepts, broad inspiration, or has no pinned reference set.
- **Provided-reference mode** — the user supplies websites, says to use only selected/existing sites, or asks to formalize a locked direction from a fixed set.

Ask only for information that is genuinely missing: target page/surface, exact pinned URLs in provided-reference mode, and research depth (`quick | standard | deep`). Recommend `standard` when the user has no preference. Manual Aside paste-prompt is the default transport. Do not offer the in-app browser or another transport unless the user asks or Aside is unavailable.

Resolve `<brain-abs>` from the current session checkout (`git rev-parse --show-toplevel` + `/brain`). In a worktree, always point Aside at that worktree. Never redirect writes to the main checkout or another worktree merely because it contains older uncommitted research; recover that research into the current checkout deliberately first.

Do not run automatically for standard dashboards, CRUD/settings/table/detail pages, or work where the existing system is sufficient.

## Discovery mode — Round 1 sweep

Render the Round 1 mission from `references/mission-prompt-template.md` for the standalone Aside UI Research skill. Aside explores until saturation and returns named concepts grounded in real sites.

Capture representative hero and signature evidence—not every page and component. Ingest into:

- `brain/research/concepts.md`
- `brain/moodboard/manifest.md`
- local screenshots under `brain/moodboard/`

## Human checkpoint

Show the concepts and evidence. The human picks one, blends explicit parts, or requests more sweep. Record the Round 2 focus inside `research/concepts.md`; do not write BRAND or DESIGN and do not create a global selected-decisions file.

## Discovery mode — Round 2 deep teardown

Use the same Aside chat. Deeply inspect the selected concept until saturation. Capture hero, meaningful middle/end sections, navigation, mobile, imagery/video, type, palette, motion, and inner pages/components only when they add materially new evidence.

Write:

- `brain/research/conventions.md`
- `brain/research/teardowns/<slug>.md`
- updated moodboard manifest/screenshots

Each teardown records URL, date, page, viewport, capture method, evidence, and clearly labeled inference. Extracted values inform our system; never copy another site's tokens, code, or assets.

## Provided-reference mode — constrained teardown

Confirm the exact URLs once. Render Variant C from `references/mission-prompt-template.md`. The pinned list is a user-defined boundary, not a target count: inspect every supplied site, discover none, and do not follow competitor/award/agency trails. Scope evidence to the user's named page or region; inspect inner pages only when the user included them.

Preserve prior moodboard/research. Record the locked/provided focus and pinned URLs in `brain/research/concepts.md` without inventing alternatives, then write the same teardown/conventions/manifest outputs as discovery Round 2. If a pinned site is blocked, report it; do not replace it with a different site.

Require evidence integrity from the first pass: distinguish live viewport captures, partial captures, media fallbacks, and no visual capture; validate mobile evidence rather than trusting filenames; separate visible brand colors from framework/widget noise; label evidence, inference, and unresolved gaps. Use the recovery and readiness contract embedded in Variant C. Completion is saturation-based: documented capture gaps may still yield `READY ... WITH DOCUMENTED GAPS` when they cannot materially change the converged direction.

## Finish

Report concepts, selected focus, convergence, disagreements, gaps, and paths written. Recommend Style Lock or Build Page as appropriate; never auto-chain.

The relay and file shapes live in `references/round-formats.md`. If Aside cannot write project files, the paste blocks remain the guaranteed transport.
