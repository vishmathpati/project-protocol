---
version: alpha
name: "[Project Name]"
surfaces:
  "[part-id]":
    kind: "[marketing | product | dashboard | content | commerce | mobile | desktop]"
    expression: "[productive | restrained | editorial | expressive | cinematic]"
# Identity tokens are shared. Each real surface declares its own expression; research depth belongs to UI Research, not DESIGN.

# UNIVERSAL TOKENS — applied to all surfaces (marketing, dashboard, desktop, etc.)

font:
  display:                       # MEMORY job — must be distinctive
    family: "[font]"             # e.g. "Migra", "Editorial New", "Tobias", "Cooper"
    fallback: "[font], serif"
    role: "headlines, hero, brand moments"
    avoid_by_default: ["Inter", "Geist", "Söhne", "IBM Plex", "SF Pro", "Roboto", "Space Grotesk", "Open Sans", "Public Sans", "system-ui"]  # heuristic; intentional surface-specific exceptions allowed
  body:                          # WAYFINDING job — must be invisible
    family: "[font]"             # Inter/Geist/Söhne acceptable here
    fallback: "[font], sans-serif"
    role: "body, UI, forms, tables"
  mono:                          # data / code
    family: "[font]"             # e.g. "JetBrains Mono", "Geist Mono", "Berkeley Mono"
    role: "code, numeric data, tabular"

icon:                            # ONE family, chosen at Style Lock, matched to the letterforms
  family: "[library]"            # default "Lucide"; alternatives "Phosphor", "Radix Icons", or a custom set
  style: "[stroke/weight]"       # e.g. "line, 1.5px stroke, rounded" — must echo the display/body character
  # never mix families · never emoji-as-icon (see DO NOT) · currentColor, sized on the 16/20/24 grid

type_scale:                       # optional but recommended — picked per surface tier
  base: 16                        # px — page body baseline
  ratio: 1.25                     # modular scale; dashboard 1.125, marketing 1.25, editorial 1.333
  steps:                          # rendered px values from base × ratio^n
    xs: 12
    sm: 14
    md: 16                        # = base
    lg: 20
    xl: 25
    "2xl": 31
    "3xl": 39
    "4xl": 49
    "5xl": 61
    display: 76                   # hero — hand-tuned, not derived from ratio
  hero_max: 96                    # optional cap for very large displays

surface:                         # named by MATERIAL, not by index
  paper: "[hex]"                 # the primary canvas — e.g. cream, ivory, leather
  ash: "[hex]"                   # raised surface (cards, panels) — one step up from paper
  ink: "[hex]"                   # text / dark canvas
  hairline: "[hex]"              # 1px borders, dividers

accent:
  primary: "[hex]"               # named by material — e.g. brass, terracotta, oxblood, jewel-green
  primary_hover: "[hex]"
  secondary: "[hex]"             # optional 2nd accent for pattern-2 brands (two-warm, two-cool, no accent)

status:                          # semantic only — never decoration
  success: "[hex]"
  warning: "[hex]"
  error: "[hex]"

chart_palette:                   # optional — only when dashboard surface has data viz needs
                                 # 8 hue stops, perceptually spaced via OKLCH at constant L+C
  light_mode:                    # L=60% C=0.15
    - "[hex]"                    # hue 30  — warm orange-red
    - "[hex]"                    # hue 60  — yellow
    - "[hex]"                    # hue 120 — green
    - "[hex]"                    # hue 180 — teal
    - "[hex]"                    # hue 210 — blue
    - "[hex]"                    # hue 270 — violet
    - "[hex]"                    # hue 300 — magenta
    - "[hex]"                    # hue 340 — rose
  dark_mode:                     # L=70% C=0.15 — slightly lighter for dark backgrounds
    - "[hex]"                    # hue 30
    - "[hex]"                    # hue 60
    - "[hex]"                    # hue 120
    - "[hex]"                    # hue 180
    - "[hex]"                    # hue 210
    - "[hex]"                    # hue 270
    - "[hex]"                    # hue 300
    - "[hex]"                    # hue 340

# LIGHT MODE block — separate from dark mode, paired by temperature

light_mode:
  paper: "[hex]"                 # e.g. "#F5EFE4" warm cream, "#FAFAFB" cool ivory, "#FBF4E6" saffron-tinted, "#EFF2EA" sage cream
  ash: "[hex]"
  ink: "[hex]"                   # text color on paper, NOT pure black
  hairline: "[hex]"
  character: "[describe]"        # e.g. "warm parchment + warm ink — editorial"

# DARK MODE block — paired character with light mode, same temperature

dark_mode:
  paper: "[hex]"                 # e.g. "#1A0F0A" warm dark, "#0A0F1A" cool dark, "#14101F" violet dark, "#2A0E14" jewel burgundy
  ash: "[hex]"
  ink: "[hex]"                   # text color on dark paper
  hairline: "[hex]"
  character: "[describe]"        # e.g. "warm near-black like leather"
  rule: "[explanation]"          # one-line rule, e.g. "never pure #000 — always 4-8% warm tint"

spacing:
  base: "4px"
  scale: [4, 8, 12, 16, 24, 32, 48, 64]

radius:
  sm: "[size]"                   # e.g. 4px
  md: "[size]"                   # e.g. 8px
  lg: "[size]"                   # e.g. 12px

shadow:
  sm: "[value]"
  md: "[value]"

motion:                          # the motion REGISTER — how much, how fast, what character. A dial per brand, not a doctrine.
  register: "[still | subtle | lively | cinematic]"  # still=law firm · subtle=clinic · lively=consumer app · cinematic=luxury/hospitality
  ui_duration: "150-300ms"       # functional UI moves — never exceed 300ms for UI (dashboard/app leans 70-240ms)
  expressive_duration: "[ms]"    # brand/hero moments — marketing only, up to 700ms; leave blank for dashboard/app
  easing: "[curve]"              # entrances ease-out (e.g. cubic-bezier(0.23,1,0.32,1)); exits accelerate; never ease-in on UI
  rules: "[one line]"            # e.g. "soft & brief, nothing bounces, nothing loops" · or "slow & ceremonial, one signature moment"

components:
  button-primary:
    backgroundColor: "{accent.primary}"
    textColor: "{surface.paper}"
    rounded: "{radius.sm}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{surface.ink}"
    borderColor: "{surface.hairline}"
    rounded: "{radius.sm}"
  input:
    backgroundColor: "{surface.ash}"
    borderColor: "{surface.hairline}"
    textColor: "{surface.ink}"
    rounded: "{radius.sm}"
  card:
    backgroundColor: "{surface.ash}"
    borderColor: "{surface.hairline}"
    rounded: "{radius.md}"

# Optional per-surface overrides
# Most projects don't need these — they apply when dashboard and marketing
# require meaningfully different palettes (e.g., marketing carries more accent
# saturation, dashboard runs sober). Leave blank if surface stack is shared.

dashboard:                       # optional — applied to product/app surfaces only
  type_scale:
    ratio: 1.125                 # tighter ratio for data-dense screens
    base: 14
  accent:
    primary: "[hex]"             # often slightly less saturated than marketing
  # surface, font, status — inherit from top-level unless overridden

marketing:                       # optional — applied to landing/marketing surfaces only
  type_scale:
    ratio: 1.25                  # bigger contrast for hero hierarchy
    base: 16
  font:
    display:                     # marketing display may differ from app display
      family: "[font]"
      role: "marketing headlines only — banned from app chrome"
  accent:
    primary: "[hex]"             # often the more saturated of the two
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

## Archetype

The single classification that selects everything below. Set once, at init.

| Archetype | Component source | Composition | Motion | Era-sensitivity | "Done" feels like |
|---|---|---|---|---|---|
| **dashboard / app** | shadcn primitives, re-skinned | repeat one grammar (repetition = usability) | functional micro-motion only | low — patterns are stable | invisible, zero friction |
| **marketing / brand** | bespoke expressive components; libraries are craft *references*, never installed aesthetics | vary grammar per section (repetition = boredom) | register-driven, still → cinematic | **high — dated is fatal** | a feeling the visitor can name |
| **content / editorial** | typography system + a few patterns | one strong column, rhythmic breaks | minimal; never between reader and text | medium | reader forgets the interface |
| **commerce** | product-grid + trust patterns | scannable, consistent | restrained | medium | frictionless path to buy |

The identity layer (fonts, palette, tokens) is shared. Each declared surface selects its own expression—how loud, varied, dense, or motion-led it should be—without pretending the whole project has one archetype.

---

## Colors

### Surface roles (named by material, not by index)

| Token | Where it appears | Notes |
|-------|------------------|-------|
| `--paper` | Page background — the 70%+ of pixels | The primary canvas (cream, ivory, leather). Never `#FFF` in light mode, never `#000` in dark mode. |
| `--ash` | Cards, panels, dropdowns | Raised surface — one step up from paper |
| `--ink` | Main copy, dark canvas | High contrast against paper (4.5:1). Tinted toward brand temperature, never pure black. |
| `--hairline` | 1 px borders, dividers | Subtle, not heavy |

### Accent roles

| Token | Where it appears | Notes |
|-------|------------------|-------|
| `--accent-primary` | The ONE accent — CTAs, links, selected state, value proof | Named by material (brass, terracotta, oxblood, jewel-green). Max 2 visible uses per screen. |
| `--accent-primary-hover` | Hover state for primary | Derive: darken primary ~8% lightness |
| `--accent-secondary` | Optional 2nd accent | Only for pattern-2 brands (two-warm, two-cool). Most projects leave blank. |

### Status (semantic only — never decoration)

| Token | Use |
|-------|-----|
| `--success` | Confirmation, on-track |
| `--warning` | Needs attention |
| `--error` | Failed, blocked |

### Derived values — don't add new colors

Hover, disabled, and tints come from base tokens via OKLCH math, not new hex codes:

```css
--accent-primary-hover:    oklch(from var(--accent-primary) calc(l - 0.08) c h);
--accent-primary-disabled: oklch(from var(--accent-primary) l calc(c * 0.5) h);
--surface-tinted:          oklch(from var(--accent-primary) calc(l + 0.40) calc(c * 0.30) h);
```

One color decision → all variants automatic. Adding a new hex code requires the extension protocol below.

### Accent discipline

- At most **2 visible uses of `--accent-primary` per screen.** Typical pair: one CTA + one selected state. Or one chip + one accent card. Not a flood.
- Links count as accent. If a screen has both an accent CTA and inline links, demote the links to underlined `--ink`.
- Hover and focus rings count as accent. Ration accordingly.

---

## Typography (role-split)

Three font roles, each with a distinct job. Not interchangeable.

### Display — the MEMORY job

The face the user remembers. Must be distinctive. Used on headlines, hero, brand moments.

**Banned from display** (these are wayfinding fonts, not memory fonts):
`Inter`, `Geist`, `Söhne`, `IBM Plex`, `SF Pro`, `Roboto`, `Space Grotesk`, `Open Sans`, `Public Sans`, `system-ui`.

Acceptable display choices: editorial serifs (Migra, Editorial New, Tobias), distinctive sans (Cooper, Antarctica, Authentic), or a custom face. If unsure, the brand probably needs a serif.

### Body — the WAYFINDING job

The face that disappears. Must be invisible so the user reads content, not type. Used on body, UI, forms, tables.

Inter / Geist / Söhne / IBM Plex / SF Pro are acceptable here — that's what they're built for.

### Mono — data / code

Used on code blocks, numeric data, tabular figures. JetBrains Mono / Geist Mono / Berkeley Mono / IBM Plex Mono are all fine.

### Where each role appears

- **Marketing surfaces** use display aggressively — hero, section headers, callouts, big numbers.
- **Dashboard / app surfaces** rarely use display. Body face does almost all the work; display reserved for empty-state heroes or onboarding moments.
- **Mono** appears wherever a number is comparing to another number (tables, dashboards, code).

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

Max 2 typefaces per project (display + body), or one variable face used at multiple weights. Mono is the third role and doesn't count against the pairing budget. Never `font-family: system-ui` alone on a heading.

### Size scale

The `type_scale:` frontmatter block sets the modular scale. Ratios per surface:

| Surface | Ratio | Base | Rationale |
|---|---|---|---|
| Dashboard / app | 1.125 (minor third) | 14 px | Tight steps — many sizes stack in a small area; headings shouldn't dominate data |
| Marketing (standard) | 1.25 (major third) | 16 px | Real hierarchy — hero feels like a hero |
| Editorial / publication | 1.333 (perfect fourth) | 18 px | Magazine cadence — only when the brand earns the drama |

Hand-tune the top two steps (`display`, `hero_max`) — modular scales overshoot
at the extremes. Line-height is inverse to size: ~1.6 at body, ~1.1 at display.

---

## Light + Dark mode pairing

Light and dark are **paired modes**, not opposites. They share temperature and material story — switching modes should feel like dimming a lamp, not flipping a switch.

### Rules

- **Light mode never uses `#FFF`.** Pure white is sterile and reads as "browser default", not "brand". Tint 4–8% toward the brand's temperature: cream, ivory, saffron, sage, parchment.
- **Dark mode never uses `#000`.** Pure black flattens the surface and crushes anti-aliasing on type. Tint 4–8% toward the brand's temperature: warm near-black, blue-black, violet-black, burgundy-black.
- **Both modes share temperature.** A warm light mode (cream paper, brown ink) pairs with a warm dark mode (leather paper, parchment ink) — not with a cool blue-black.
- **Surfaces are named by material, not by index.** `--paper`, `--ash`, `--ink`, `--hairline` — not `--bg`, `--surface-1`, `--surface-2`, `--surface-3`. Material names force a story; index names invite a flood of generic surface levels.
- **Light and dark each get their own block in the frontmatter** (`light_mode:` and `dark_mode:`). Both blocks must declare a `character` line so the pairing intent is legible.

### Examples of paired character

| Light character | Dark character |
|---|---|
| Warm parchment + warm ink (editorial) | Warm leather + parchment ink (library at night) |
| Cool ivory + slate ink (clinical) | Deep navy + ice ink (operations room) |
| Saffron + oxblood ink (heritage) | Burgundy near-black + saffron ink (jewel box) |
| Sage cream + forest ink (botanical) | Forest near-black + sage ink (greenhouse) |

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

## Motion

Motion is a **register dial set per brand**, not a fixed rule — a law firm is nearly still, a clinic is subtle, a consumer app is lively, a luxury property is cinematic. The `motion:` frontmatter block records this project's setting.

- **UI motion stays under 300ms** (dashboard/app leans 70–240ms). Brand/hero moments (marketing only) may run up to ~700ms.
- **Entrances ease-out; exits accelerate; never ease-in on UI.** One easing family so everything feels related.
- **Frequency law:** the more often an action fires, the less it animates. Keyboard-initiated / 100×-a-day actions get no animation.
- **Never `scale(0)`** — enter from `scale(0.95)` + opacity. Press feedback `scale(0.97)`.
- Scroll replay is chosen per surface and motion register. Never leave content invisible or interactions broken after re-entry.
- Under `prefers-reduced-motion`, remove or substantially reduce nonessential movement; preserve necessary state communication without forced animation.
- **Animate `transform` / `opacity` only.** Never `transition: all`.

Map productive or expressive motion per surface, not per project.

---

## Icons

One family for the whole project, chosen at Style Lock and matched to the letterforms — geometric type takes geometric icons, humanist type takes softer ones. Default **Lucide**; alternatives Phosphor / Radix / a custom set.

- One library only — mixed sets betray themselves via stroke weight and corner radius.
- Stroke weight matches the type; size on the 16 / 20 / 24 grid; `currentColor`.
- Icons need visible text labels (only home / search / cart are truly universal); never hide the label behind hover.
- Never emoji-as-icon (see DO NOT).

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

The `design-check` skill enforces this on every UI task. Skipping the protocol = the agent shipped raw values, which the completion-check gate will flag.

---

## Agent prompt guide

When asked to design any surface in this project:
- Read this file first, then `FUNDAMENTALS.md` for universal craft rules.
- Use only the tokens defined here. If something's missing, follow the Extension protocol above.
- Prefer reuse over creation — search `components/` before making anything new.
- Apply the DO NOT rules without being asked.
- Surface any rule conflict to the user before writing code.
