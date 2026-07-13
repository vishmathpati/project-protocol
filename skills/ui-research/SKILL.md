---
name: ui-research
description: "Optional real-site UI research for brand-facing or inspiration-dependent work. Discover concepts openly or within user-pinned sites, require explicit human selection, then tear down the selected focus. Does not auto-trigger for ordinary dashboards."
---

# UI Research

Ground a visual direction in real sites before Style Lock or Build Page. Research is evidence, not authority.

## Resolve the invocation

Read BRIEF, STRUCTURE, BRAND, Marketing Stage A outputs, the user-stated target surface/page, DESIGN refusals, and TASTE. The user's explicit target and reference constraint outrank STATUS/ROADMAP next actions. Never redirect homepage research to the next queued page.

Choose without a menu dump. There are exactly three entry modes:

- **Open discovery** — no pinned reference set and no explicit human-selected research concept. Sweep the field into concepts.
- **Provided-reference concept discovery** — the user supplies or limits research to websites, but has not explicitly selected a research concept or blend. Analyze only that closed set, group it into concepts, then stop for the human checkpoint.
- **Selected-focus teardown** — `brain/research/concepts.md` contains an explicit human selection record with status, focus, selected by, date, and included moves. Tear down that selected concept; when its reference set is pinned, inspect only those URLs.

A supplied URL list, a prohibition on finding more sites, or an existing BRAND/DESIGN direction is a constraint—not concept selection. Never infer selection from words such as `locked`, an existing design system, a prior moodboard, STATUS/ROADMAP, or the presence of teardowns. If the explicit selection record is missing or incomplete, route to concept discovery or the human checkpoint, never teardown.

Ask only for information that is genuinely missing: target page/surface, exact pinned URLs when the set is closed, and research depth (`quick | standard | deep`). Recommend `standard` when the user has no preference. Do not ask the user whether a concept was selected when canon lacks the explicit record: it was not selected. Manual Aside paste-prompt is the default transport. Do not offer the in-app browser or another transport unless the user asks or Aside is unavailable.

Resolve `<brain-abs>` from the current session checkout (`git rev-parse --show-toplevel` + `/brain`). In a worktree, always point Aside at that worktree. Never redirect writes to the main checkout or another worktree merely because it contains older uncommitted research; recover that research into the current checkout deliberately first.

Do not run automatically for standard dashboards, CRUD/settings/table/detail pages, or work where the existing system is sufficient.

## Open discovery — Round 1 sweep

Render the Round 1 mission from `references/mission-prompt-template.md` for the standalone Aside UI Research skill. Aside explores until saturation and returns named concepts grounded in real sites.

Capture representative hero and signature evidence—not every page and component. Ingest into:

- `brain/research/concepts.md`
- `brain/moodboard/manifest.md`
- local screenshots under `brain/moodboard/`

## Provided-reference concept discovery — closed Round 1

Render Variant C from `references/mission-prompt-template.md`. Aside inspects or reuses evidence from every pinned URL, discovers no additional websites, and groups only that closed set into named concepts. A fixed website list constrains where concepts come from; it does not remove concept discovery.

When verified teardowns and screenshots already exist, reuse them before browsing. Browse again only for a material concept-classification gap and report why. Preserve the existing evidence; do not overwrite teardown conclusions merely to create concepts.

Write the same Round-1 concept and moodboard outputs as open discovery, with `## Human selection` initialized to `Status: pending`.

## Human checkpoint

After ingesting either Round-1 mode, explicitly invoke Project Dashboard to generate or refresh `brain/project-dashboard.html`. Report its path and present the Research / Moodboard tab before asking for a decision. Dashboard generation is part of this checkpoint, not a hook or Save Session side effect. If generation fails, report the blocker and do not advance to teardown.

Show the concepts and evidence. The human picks one, blends explicit parts, or requests more sweep. Never choose, recommend-and-assume, or translate an old brand direction into a selection on the human's behalf.

Record this exact block inside `brain/research/concepts.md`:

```markdown
## Human selection
- Status: selected
- Focus: <concept letter/name or explicit blend>
- Selected by: <human name/identifier>
- Selected at: <YYYY-MM-DD>
- Included moves: <explicit hero/type/navigation/rhythm/etc. picks; "whole concept" when unblended>
```

Before selection the block must say `Status: pending` and leave the other fields absent. Do not write BRAND or DESIGN and do not create a global selected-decisions file.

## Selected-focus teardown — Round 2

Read and validate the complete `## Human selection` record before rendering any teardown mission. Missing status, focus, selector, date, or included moves blocks Round 2 and returns to the human checkpoint. Use the same Aside chat. Deeply inspect the selected concept until saturation. Capture hero, meaningful middle/end sections, navigation, mobile, imagery/video, type, palette, motion, and inner pages/components only when they add materially new evidence.

Write:

- `brain/research/conventions.md`
- `brain/research/teardowns/<slug>.md`
- updated moodboard manifest/screenshots

Each teardown records URL, date, page, viewport, capture method, evidence, and clearly labeled inference. Extracted values inform our system; never copy another site's tokens, code, or assets.

### Selected focus with a closed reference set

Confirm the exact URLs once. Render Variant D from `references/mission-prompt-template.md`. The pinned list is a user-defined boundary, not a target count: inspect every supplied site, discover none, and do not follow competitor/award/agency trails. Scope evidence to the user's named page or region; inspect inner pages only when the user included them.

Preserve prior moodboard/research and the human selection record, then write the same teardown/conventions/manifest outputs as open-discovery Round 2. If a pinned site is blocked, report it; do not replace it with a different site.

Require evidence integrity from the first pass: distinguish live viewport captures, partial captures, media fallbacks, and no visual capture; validate mobile evidence rather than trusting filenames; separate visible brand colors from framework/widget noise; label evidence, inference, and unresolved gaps. Use the recovery and readiness contract embedded in Variant D. Completion is saturation-based: documented capture gaps may still yield `READY ... WITH DOCUMENTED GAPS` when they cannot materially change the converged direction.

## Finish

Report entry mode, concepts, human-selected focus, convergence, disagreements, gaps, dashboard path, and paths written. Recommend Style Lock or Build Page as appropriate; never auto-chain.

The relay and file shapes live in `references/round-formats.md`. If Aside cannot write project files, the paste blocks remain the guaranteed transport.
