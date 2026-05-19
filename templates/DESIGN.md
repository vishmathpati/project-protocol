---
version: alpha
name: "[Project Name]"
colors:
  bg: "#[hex]"
  surface: "#[hex]"
  surface-2: "#[hex]"
  text: "#[hex]"
  text-muted: "#[hex]"
  border: "#[hex]"
  primary: "#[hex]"
  primary-hover: "#[hex]"
  success: "#[hex]"
  warning: "#[hex]"
  error: "#[hex]"
typography:
  display:
    fontFamily: "[font]"
    fontSize: "[size]"
    fontWeight: "[weight]"
  heading:
    fontFamily: "[font]"
    fontSize: "[size]"
    fontWeight: "[weight]"
  body:
    fontFamily: "[font]"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.5"
  small:
    fontFamily: "[font]"
    fontSize: "14px"
spacing:
  base: "4px"
  scale: [4, 8, 12, 16, 24, 32, 48, 64]
radius:
  sm: "4px"
  md: "8px"
  lg: "12px"
shadow:
  sm: "0 1px 3px rgba(0,0,0,0.08)"
  md: "0 4px 12px rgba(0,0,0,0.10)"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "{radius.sm}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    borderColor: "{colors.border}"
    rounded: "{radius.sm}"
  input:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.border}"
    textColor: "{colors.text}"
    rounded: "{radius.sm}"
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.border}"
    rounded: "{radius.md}"
---

# DESIGN.md — [Project Name]

> The brand layer. Specifies WHICH colors, fonts, and sizes this project uses.
> Universal craft rules (the "how") live in `FUNDAMENTALS.md`.
> Read both before any UI work.

---

## Overview

A one-paragraph description of the visual identity — tone, era, references.
Example: "Editorial, warm, considered. Slightly formal. References: Stripe Press, A24, Notion editorial pages."

[VERIFY — fill from BRAND.md or user direction]

---

## Colors

### Roles

| Token | Where it appears | Notes |
|-------|------------------|-------|
| `--bg` | Page background — the 70%+ of pixels | Foundation neutral |
| `--surface` | Cards, panels, dropdowns | One step up from bg |
| `--surface-2` | Elevated surface, hover states | Subtle separation |
| `--text` | Main copy | High contrast against bg (4.5:1) |
| `--text-muted` | Supporting copy, labels, metadata | 4.5:1 minimum against bg |
| `--border` | 1 px hairlines | Subtle, not heavy |
| `--primary` | The ONE accent — CTAs, links, selected state, value proof | Max 2 visible uses per screen |
| `--primary-hover` | Hover state for primary | Derive: darken primary ~8% lightness |
| `--success` `--warning` `--error` | Status only, never decoration | Semantic |

### Derived values — don't add new colors

Hover, disabled, and tints come from base tokens via OKLCH math, not new hex codes:

```css
--primary-hover:    oklch(from var(--primary) calc(l - 0.08) c h);
--primary-disabled: oklch(from var(--primary) l calc(c * 0.5) h);
--surface-tinted:   oklch(from var(--primary) calc(l + 0.40) calc(c * 0.30) h);
```

One color decision → all variants automatic. Adding a new hex code requires the extension protocol below.

### Accent discipline

- At most **2 visible uses of `--primary` per screen.** Typical pair: one CTA + one selected state. Or one chip + one accent card. Not a flood.
- Links count as accent. If a screen has both an accent CTA and inline links, demote the links to underlined `--text`.
- Hover and focus rings count as accent. Ration accordingly.

---

## Typography

[Fill: which fonts, which sizes, which weights. Token shape lives in frontmatter above.]

### Letter-spacing (non-negotiable)

| Context | Letter-spacing |
|---|---|
| Body (14–18 px) | `0` |
| Small text (11–13 px) | `0.01em` to `0.02em` |
| UI labels and button text | `0.02em` |
| **ALL CAPS** | **`0.06em` to `0.1em` — required** |
| Headings 32 px+ | `-0.01em` to `-0.02em` |
| Display 48 px+ | `-0.02em` to `-0.03em` |

### Pairing

Max 2 typefaces per project. Display + body, or one variable face at multiple weights. Never `font-family: system-ui` alone on a heading.

---

## Spacing

4 px base. Scale: 4, 8, 12, 16, 24, 32, 48, 64. Never mix arbitrary values.

---

## Radius

| Token | Use |
|-------|-----|
| `--radius-sm` | Buttons, inputs, small cards |
| `--radius-md` | Cards, panels |
| `--radius-lg` | Modals, sheets (rare) |

No `rounded-full` / pill shapes unless explicitly intentional and named as an exception.

---

## Shadow

| Token | Use |
|-------|-----|
| `--shadow-sm` | Cards, subtle elevation |
| `--shadow-md` | Modals, dropdowns, popovers |

Single-layer shadows only. No multi-layer "elevation" stacks unless brand explicitly calls for it.

---

## Components

The component list this project commits to. Built once in `components/ui/` (web) or `Views/` (Swift), reused everywhere.

- [ ] Button (default / destructive / outline / ghost / link)
- [ ] Input (text / textarea / select)
- [ ] Card
- [ ] Dialog / Modal
- [ ] Dropdown / Menu
- [ ] Toast (Sonner on web)
- [ ] Table
- [ ] Tabs
- [ ] Badge
- [ ] Sheet / Drawer
- [ ] Form (with validation)
- [ ] Tooltip

[Mark which ones already exist in this project. New components must extend or compose these — don't create a second Button. If you need something not on this list, follow the Extension protocol.]

---

## DO NOT

Hard constraints. Any of these in a diff = stop and reconsider.

- No indigo / violet hex codes (`#6366f1`, `#4f46e5`, `#7c3aed`, `#a855f7`). The Tailwind default palette is the textbook AI-slop tell.
- No two-stop "trust" gradients (purple→blue, blue→cyan, indigo→pink) on heroes.
- No emoji-as-icons (✨ 🚀 🎯 ⚡ 🔥 💡) inside buttons, headings, or feature lists. Use monoline SVG with `currentColor`.
- No sans-serif on display when this brand binds a serif (and vice versa).
- No rounded card + colored left-border accent ("AI dashboard tile" shape).
- No invented metrics ("10× faster", "99.9% uptime"). Either real or labelled placeholder.
- No `lorem ipsum`, "feature one / two / three", "placeholder text" in shipped UI.
- No `outline: none` without a `:focus-visible` replacement.
- No `<div onClick>` for what should be `<button>` or `<a>`.
- No images without `width` / `height` attributes — causes layout shift.
- No paste-blocking on form fields.
- No `text-align: justify` on body copy.
- No more than 3 type sizes visible above the fold.

[Add brand-specific anti-patterns here — "no cream backgrounds", "no slab serif", etc.]

---

## Extension protocol

When a UI task needs a value that isn't in this file:

1. **Stop.** Don't improvise. Don't write the value as a raw hex / px.
2. **Propose the addition** — name the new token, point at related existing tokens it derives from, explain why it's needed.
3. **Wait for explicit user confirmation** ("go", "do it", "approved").
4. **Add the token here AND in `global.css`** (or `DesignTokens.swift` for Swift projects).
5. **Then use it.**

The `design-check` skill enforces this on every UI task. Skipping the protocol = the agent shipped raw values, which the audit-before-close gate will flag.

---

## Agent prompt guide

When asked to design any surface in this project:
- Read this file first, then `FUNDAMENTALS.md` for universal craft rules.
- Use only the tokens defined here. If something's missing, follow the Extension protocol above.
- Prefer reuse over creation — search `components/` before making anything new.
- Apply the DO NOT rules without being asked.
- Surface any rule conflict to the user before writing code.
