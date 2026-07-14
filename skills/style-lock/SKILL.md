---
name: style-lock
description: Convert approved brand, content needs, UI research, existing design-system truth, project surfaces, and taste into one coherent visual system. Use when colors, typography, modes, spacing, radius, shadow, motion, icons, or per-surface expression must be established or changed. Requires visual preview and approval before writing DESIGN.md.
---

# Style Lock

Own the transition from brand/research evidence to approved design tokens. User approval outranks research.

## Sequence position

For research-led brand-facing work, Style Lock runs after the `## Approved Site Direction` exists and before Marketing Stage B final copy and Build Page implementation. An existing strong DESIGN may satisfy this slot through explicit reuse rather than a rerun. UI Research reads DESIGN only as optional pre-existing evidence, so no circular requirement exists.

## Read inputs

Read BRIEF, STRUCTURE, BRAND, relevant marketing content, research/conventions/teardowns, existing DESIGN, FUNDAMENTALS, TASTE, current theme/CSS, and actual surfaces. Preserve successful tokens; propose only what must change. UI Research is optional evidence.

## Propose one coherent system

Present one recommended direction. Alternatives appear only when requested. Define shared identity plus per-surface expression for the surfaces that exist. Cover only applicable type roles/scripts, material colors, modes, spacing, radius, shadows, motion, icons, components, extensions, and refusals. Treat font avoid-lists and archetype mappings as heuristics with intentional exceptions.

## Render a throwaway style proof before approval

The mandatory preview is a **throwaway style proof**: a rendered slice of the project's lead page hero — or its single most important surface — built with the project's real approved or draft copy pulled from the PAGE-COPY files, expressed in the approved research direction. Use `assets/preview-template.html` with only the relevant surface layouts, and show token ramps, modes, contrast, states, components, imagery treatment, and motion character within that real-content slice.

The style proof is explicitly non-canonical scratch output. It is deleted after the human's verdict and never becomes a source of truth. Taste is judged on real content in the real surface — never on token swatches or lorem specimens alone. Never ask approval from raw token values alone, and refuse approval while load-bearing WCAG pairs fail. Only after the human approves the style proof may DESIGN be written.

## Write and synchronize

After explicit approval: update DESIGN; lint with `npx @google/design.md lint`; export/synchronize safely into the actual theme target without overwriting unrelated CSS; render the app; verify changed surfaces; run Design Check postflight.

Do not write BRAND, marketing, research, or page composition. Read `references/token-alignment.md` when generating or comparing tokens.
