# Sub-mode — Recreate from inspiration

The user wants a component "like X from [installable library]" — Mantine Combobox, Chakra Drawer, MUI Stepper, Ant Design DatePicker. Adopting the whole library isn't an option (it's a different design system, locks tokens, increases bundle size, and conflicts with the project's existing primitives). The skill studies the named API and behavior, then generates a brand-new Generic primitive in the project's own design system.

This is different from adopt-external (copy-paste source). Here there is no source to paste — the source is buried inside `node_modules` of a library the project doesn't install, and the goal is conceptual replication, not literal copy.

---

## When this fires

Triggers:

- "I want a Combobox like Mantine's."
- "Make me a Drawer that works like Chakra's."
- "Like MUI's Stepper, but in our style."
- "I want React Aria's DatePicker behavior — but using our components."

The signal is "**like X from [library]**". The library is named, and it's an installable design system, not a copy-paste site.

---

## Phase 1 — Structure detection

Same as default. Read or write `agents/STRUCTURE.md`. The recreated component lands in **Generic** (it's a primitive — variants + ref + className merge will apply).

---

## Phase 2 — Intake = API + behavior study

Ask one focused question:

> Which specific behaviors do you want from [library]'s [component]? E.g. for Combobox: searchable, multi-select, keyboard navigation, async loading, custom render?

Why this matters: design-system components like Mantine's Combobox bundle ~20 features. You probably want 3–5 of them. Listing what you actually need lets the skill build a minimal primitive instead of a 600-line god-component.

If the user names a specific subset, lock it. If they say "everything", push back: "Mantine's Combobox has ~20 props. Building all of them takes hours. The most-used core is: searchable, multi-select, async options, keyboard nav. Start with those?"

---

## Phase 3 — Reuse scan

Glob the Generic folder for anything close. Often the project already has half of what's needed:

```
recreate-from-inspiration — looking for prior art:

  Found in ui/:
    - Select   — single-select dropdown, keyboard nav. No search, no multi.
    - Popover  — generic floating positioning, used by Select.
    - Input    — text input, used everywhere.
    - Checkbox — for multi-select rows.

  Plan:
    - Build Combobox by composing Popover + Input + Checkbox (for multi).
    - Borrow keyboard-nav patterns from existing Select.
    - Reuse the floating positioning logic, don't re-implement it.

  Strategy: C — new primitive (Combobox doesn't exist), but it leans heavily
  on existing primitives. The new file is small.
```

Strategy is almost always **C — new primitive** in this sub-mode (the user said the project doesn't have this component yet). But the implementation should reuse every existing primitive it can.

---

## Phase 4 — Headless layer decision

Big choice in this sub-mode: do you build the keyboard nav / accessibility / focus-trap / aria-* logic from scratch, or sit on top of a headless library?

### Headless library is the right call when:

The component has substantial accessibility surface area:

- Combobox (ARIA combobox pattern, listbox role, keyboard nav, screen-reader announcements).
- Dialog / Drawer (focus trap, scroll lock, escape handling, return-focus).
- DatePicker (date math, locale handling, keyboard grid nav).
- Menu (roving tabindex, type-ahead).
- Tabs (arrow keys, automatic vs manual activation).

For these, surface:

```
recreate-from-inspiration — headless layer

  Building Combobox correctly requires ARIA combobox + listbox patterns,
  keyboard nav with type-ahead, screen-reader announcements. Implementing
  these from scratch is ~400 lines and easy to get wrong.

  Recommended: install a headless package and style on top.

  Options:
    A — @radix-ui/react-* (if you're already on Radix — already in package.json)
    B — react-aria / react-aria-components (Adobe, AA out of the box)
    C — @headlessui/react (Tailwind Labs, lighter)
    D — Roll our own from scratch (faster initial build, slower long-term)

  Recommend A — Radix is already installed for your Select.
```

User picks. The recreated component imports the headless layer for behavior, applies the project's tokens for visuals.

### Headless library is NOT needed when:

The component is mostly visual with a tiny behavior surface:

- Stepper (just a list with progress).
- BreadCrumb (just a list with separators).
- StatTile / KPITile (no interaction).
- Avatar (no interaction).
- Pagination (a few buttons).

For these, skip the headless layer. Build directly.

---

## Phase 5 — Generate + preview + write

### 5a — Sub-agent generation rules

Pass the locked object to a reasoning sub-agent:

```yaml
intake: "Combobox like Mantine — searchable, multi-select, async options, keyboard nav"
tier: generic
strategy: C
proposed_name: Combobox
location: src/components/ui/combobox.tsx
new_primitive: true
headless_layer: "@radix-ui/react-popover"
prior_art_used:
  - Popover from @radix-ui/react-popover (re-export pattern used in existing Select)
  - Input from @/components/ui/input
  - Checkbox from @/components/ui/checkbox
  - cn from @/lib/utils
behaviors_required:
  - searchable
  - multi-select
  - async options
  - keyboard navigation
convention: shadcn-style
```

Sub-agent rules:

1. Build the API to match the project's existing primitive conventions, not the source library's. If your Select uses `value` / `onValueChange`, your Combobox should too — don't copy Mantine's `data` / `onChange`.
2. Use project tokens for every visual value. The source library's tokens are not allowed in the output.
3. Emit the full triplet (cva + forwardRef + cn) since this IS a new primitive.
4. Compose the headless layer for behavior. Style the slots with project tokens.
5. Include the 5 required UI states (default, hover, focus, active, disabled).

### 5b — Show preview

Same shape as default Phase 5. Full code block. User approves / edits / restarts.

### 5c — Side-effect tracking

If a new headless package was added (Phase 4 picked option A/B/C), surface it in the output:

```
recreate-from-inspiration — done

  Wrote: src/components/ui/combobox.tsx
  Tier: Generic
  Strategy: C — new primitive
  Headless layer: @radix-ui/react-popover (already installed, no new dep)
  Lines: 137

  API (matches project's existing Select):
    value: string[] | string
    onValueChange: (next) => void
    multiple?: boolean
    options: Array<{label, value}> | (q: string) => Promise<...>
    placeholder?: string

  Behaviors covered:
    ✓ search input filters options
    ✓ multi-select via Checkbox rows
    ✓ async options (debounced)
    ✓ keyboard nav (↑ ↓ Enter Esc) inherited from Radix Popover + roving tabindex

  Behaviors NOT covered (vs Mantine):
    ✗ grouped options          — add later if needed
    ✗ creatable (add new on enter) — add later if needed
    ✗ custom item renderer     — punt — most use cases don't need it

  Next:
    → design-check auto-fires.
    → Use: import { Combobox } from "@/components/ui/combobox"
```

The list of "behaviors NOT covered" is important — sets expectations for the user about what's intentionally absent vs accidentally missing.

---

## Library-specific tips

### Mantine

API style is `data` / `value` / `onChange`. Their components are heavily prop-driven with lots of variants. When recreating: pick the 3–5 behaviors that matter, drop the rest, match the project's prop naming.

### Chakra

API style uses composition (e.g. `<Modal><ModalOverlay /><ModalContent>...`) much like Radix. Recreation is straightforward when the project already uses a similar primitive split.

### MUI (Material UI)

API style is a single big component with deep prop trees. The visual language is Material Design — DO NOT copy the Material visual. Just the behavior. The project's `DESIGN.md` is the source of truth for look.

### Ant Design

Same as MUI — copy behavior, not visuals. Ant components have very specific spacing/border patterns that don't transfer.

### React Aria / Adobe Spectrum

These ARE headless libraries. If the user is asking for "a DatePicker like React Aria's", recommend just installing `react-aria-components` and styling on top — that IS the recreate pattern.

### Radix UI

Already a headless library. If the user wants "a Dialog like Radix's", they want Radix Dialog with project styles on top. Recommend installing `@radix-ui/react-dialog` and building the styled wrapper.

### Headless UI (Tailwind Labs)

Similar to Radix. Install the headless package, style on top.

---

## Hard rules for recreate-from-inspiration

- **Never install the inspiration library itself.** Recreating Mantine's Combobox means do NOT add `@mantine/core` to dependencies. The point is a project-tokens-native version.
- **Match the project's API naming, not the source library's.** Consistency inside the project beats fidelity to an outside reference.
- **Headless layers are encouraged for high-accessibility components.** Rolling your own ARIA is a long road.
- **Surface the behaviors NOT covered.** The user should know what's intentionally smaller-scope.
- **Tokens only.** Same rule as everywhere — no raw hex / px / font.

---

## When recreate-from-inspiration is the wrong tool

- If the user actually wants to install the library: this isn't the right skill. Their package manager covers it.
- If they pasted code from the library's docs: that's adopt-external, not recreate.
- If the project already has a near-identical primitive (Select exists, they want Combobox): strategy might be B (extend Select with search + multi flags) instead of C. Phase 3's reuse scan should catch this.
