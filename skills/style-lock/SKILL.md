---
name: style-lock
description: Convert approved brand, content needs, UI research, existing design-system truth, project surfaces, and taste into one coherent visual system. Use when colors, typography, modes, spacing, radius, shadow, motion, icons, or per-surface expression must be established or changed. Requires visual preview and approval before writing DESIGN.md.
---

# Style Lock

Own the transition from brand/research evidence to approved design tokens. User approval outranks research.

## Read inputs

Read BRIEF, STRUCTURE, BRAND, relevant marketing content, research/conventions/teardowns, existing DESIGN, FUNDAMENTALS, TASTE, current theme/CSS, and actual surfaces. Preserve successful tokens; propose only what must change. UI Research is optional evidence.

## Propose one coherent system

Present one recommended direction. Alternatives appear only when requested. Define shared identity plus per-surface expression for the surfaces that exist. Cover only applicable type roles/scripts, material colors, modes, spacing, radius, shadows, motion, icons, components, extensions, and refusals. Treat font avoid-lists and archetype mappings as heuristics with intentional exceptions.

## Render before approval

Use `assets/preview-template.html` with representative real content and only relevant surface layouts. Show token ramps, modes, contrast, states, components, imagery treatment, and motion character. Never ask approval from raw token values alone. Refuse approval while load-bearing WCAG pairs fail.

## Write and synchronize

After explicit approval: update DESIGN; lint with `npx @google/design.md lint`; export/synchronize safely into the actual theme target without overwriting unrelated CSS; render the app; verify changed surfaces; run Design Check postflight.

Do not write BRAND, marketing, research, or page composition. Read `references/token-alignment.md` when generating or comparing tokens.
