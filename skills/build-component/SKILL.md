---
name: build-component
description: Build or adopt one genuinely missing UI component within the project's existing design system and architecture. Use after reuse search when no suitable project component or configured library primitive exists, or when adapting an inspected external behavior to project tokens, content, assets, accessibility, and stack.
---

# Build Component

Create the smallest missing piece without inventing a parallel design system.

## 1. Read and classify

Read STRUCTURE, DESIGN, FUNDAMENTALS, relevant TASTE, chapter/page decisions, and any `research/components/<slug>.md`. Identify the target surface and whether the need is a commodity/accessibility-critical primitive or a brand-expressive composition.

Consume the approved page narrative, pattern, and media-slot decision; never choose the page story or acquire media on the component's behalf. `reference-only` research assets cannot enter implementation. Use only owned/client-authorized, licensed, approved generated, or explicitly temporary neutral media, and preserve its replacement gate.

## 2. Selection ladder

Use this order:

1. Existing project component.
2. Compose existing components.
3. Extend an existing component without breaking consumers.
4. Configured design-system primitive (shadcn/Radix or project equivalent).
5. Proven accessible base.
6. New component.

When shadcn is configured, never hand-roll native/default substitutes for Calendar/Date picker, Select, Dialog, Popover, Tooltip, Dropdown, Tabs, Accordion, Toast, Form, Command, Sheet, Drawer, Checkbox, Radio, Switch, or Slider. Compose shadcn/Radix primitives if the exact composite is absent.

Marketing components may be visually bespoke, but accessibility-critical behavior still comes from proven primitives.

## 3. Preview the strategy

For visually meaningful work, show a rendered preview or focused mockup rather than asking a nontechnical user to approve full source code. State reuse choice, location, public API, states, responsive behavior, and token mapping.

Use Inspect Component only when an external component's mechanics are genuinely unclear. Adapt evidence; never copy proprietary code or assets.

## 4. Implement and verify

Place the component according to STRUCTURE. Cover applicable loading, empty, error, disabled, focus, hover, selected, and reduced-motion states. Run Design Check postflight, relevant tests, and render verification. Update STRUCTURE only when the physical architecture genuinely changed; Build Component never creates STRUCTURE from scratch.

Retained references describe external adoption, reuse scanning, and implementation evidence. This file governs when older examples conflict.
