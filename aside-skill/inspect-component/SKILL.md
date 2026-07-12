---
name: inspect-component
description: Inspect one exact component or visual region on a supplied website using browser and DevTools evidence, then return an adaptation report. Use only when the mission supplies the URL, target region, liked behavior, and target stack.
runtime: aside-browser
managed-by: project-protocol
---

# Inspect Component — Aside

Investigate one region. Do not redesign it and do not copy proprietary implementation.

## Mission inputs

Require URL, page/region, liked behavior, target stack, target breakpoints, and any locating screenshot. If the region cannot be identified reliably, request clarification.

## Evidence pass

Capture relevant desktop and mobile behavior. Inspect DOM hierarchy and semantics; computed layout/type/color/stacking/clipping; responsive changes; image/video/SVG/font assets and delivery; libraries and runtime signals; motion triggers/timing/easing/scroll coupling/transforms/reduced-motion; interaction states; accessibility; and performance implications.

Separate observed evidence from inference. Never extract credentials, bypass access controls, reproduce proprietary source code, or download assets for reuse.

## Return contract

Return source URL/date/page/viewport/region/method, observed behavior, DOM/style/network/asset/library evidence, responsive/motion/state/accessibility/performance notes, labeled inference, likely implementation model, adaptation guidance for the target stack, required replacement assets, unresolved questions, and evidence screenshot names.
