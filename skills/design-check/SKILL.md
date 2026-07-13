---
name: design-check
description: Preflight and postflight gate for visual changes. Use before UI work to confirm surface, design canon, reuse, tokens, and component-system routing; use after changes to inspect only changed hunks and rendered evidence for token, accessibility, state, responsive, motion, and taste violations.
---

# Design Check

Keep UI changes on-system. This skill does not choose the brand, approve Style Lock, or prove the whole chapter complete.

## Preflight

1. Identify the target surface from STRUCTURE and chapter.
2. Read DESIGN, applicable FUNDAMENTALS, TASTE precedence, and brand/page refusals.
3. Search existing components and configured libraries.
4. Identify existing tokens and any missing token/component decision.
5. Route ordinary dashboard UI through existing project components and shadcn when configured. Do not auto-trigger UI Research.

Stop when DESIGN is genuinely required but absent. A conventional existing product system may proceed from its established tokens/components while Style Lock is scheduled only if the project needs a new visual direction.

## Postflight

Inspect the changed hunks and rendered output, not entire large files. Check:

- Raw or unmapped visual values.
- Component-system bypass and native substitutes where shadcn/project primitives exist.
- Typography, spacing, radius, shadow, color, modes, and per-surface expression.
- Focus, keyboard, labels, contrast, states, responsive behavior, imagery/video crop and treatment, controls, posters/fallbacks, and reduced motion.
- Media source stage, permission/provenance, and replacement gates. A required factual or load-bearing placeholder cannot pass as final visual evidence.
- High-confidence TASTE and explicit BRAND/DESIGN refusals.
- Unintended changes outside the target region.

Mechanical fixes may be proposed or applied within the authorized scope. Human-judgment issues require a recommendation and user/owner decision. New tokens route through Style Lock; do not silently edit DESIGN.

Return `PASS`, `PASS WITH FOLLOW-UP`, or `FAIL` with file/line or render evidence. Completion Check separately compares the finished work with the chapter contract.
