# Phase 7 — Layout sketches

For each page in SITEMAP.md, write `agents/marketing/layouts/<slug>.md`. Each layout is a block-level wireframe in markdown — rectangles labelled with intent. Full-bleed vs contained, image-left vs text-right, sticky elements, alternating rhythm.

NOT a pixel-perfect mockup. NOT Figma. Structural intent only. `build-component` consumes the layout when implementing each page's actual JSX.

This phase exists because a brief + copy + media manifest still leaves "how does the page actually stack" undetermined. Two implementers reading the same brief produce wildly different page structures. The layout sketch closes that gap.

---

## What a layout sketch looks like

Each block is a rectangle in monospace, labelled with:

- Which brief section it corresponds to (`§1 Hero`, `§2 Logos`, …).
- The container width — full-bleed vs contained.
- The internal split — one column, two columns (image-left / text-right), grid, etc.
- The visual anchor type (cross-references MEDIA.md).
- Any sticky / fixed behaviour.

Rectangles use ASCII boxes. Width is not literal — these aren't pixels — but relative width within the page shows which sections are full-bleed and which are contained.

---

## Worked example — `layouts/home.md`

```markdown
# agents/marketing/layouts/home.md
> Layout sketch for the Home page. Locked via marketing-brief on 2026-05-21.
> Reads brief: agents/marketing/briefs/home.md.
> Reads copy: agents/marketing/copy/home.md.
> Reads media: agents/marketing/MEDIA.md § Home.

## Global shell

┌──────────────────────────────────────────────────────────────────────┐
│  NAV — sticky top, transparent over hero, solid after scroll         │
│  logo · Pricing · Customers · Features ▾ · vs ▾ · Blog · Sign in · CTA│
└──────────────────────────────────────────────────────────────────────┘

(All page sections sit inside this shell. Footer is shared, sketched at end.)

## §1 Hero — full-bleed, two-column on desktop, stacked on mobile

┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   [headline]                                  ┌─────────────────┐    │
│   [subhead]                                   │                 │    │
│                                               │  screenshot     │    │
│   [CTA primary]  [CTA secondary link]         │  (anchor:       │    │
│                                               │   MEDIA Home    │    │
│                                               │   hero)         │    │
│                                               └─────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Container: max-width 1280, generous side padding.
- Mobile: screenshot stacks below text, full width.
- No background pattern. Background is plain `--background`.

## §2 Logos — contained, single row

┌──────────────────────────────────────────────────────────────────────┐
│   "Used by teams at"                                                 │
│   [logo] [logo] [logo] [logo] [logo] [logo]                          │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Greyscale logos. 60% opacity.
- Mobile: 3 per row, two rows.

## §3 Proof — full-bleed background, screenshot floats over

┌──────────────────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░  [eyebrow]                                                     ░  │
│  ░  [headline]                                                    ░  │
│  ░  [subhead]                                                     ░  │
│  ░                                                                ░  │
│  ░       ┌──────────────────────────────────────────────┐         ░  │
│  ░       │  screenshot — A/B test results               │         ░  │
│  ░       │  (anchor: MEDIA Home proof)                  │         ░  │
│  ░       └──────────────────────────────────────────────┘         ░  │
│  ░                                                                ░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Section background: `--surface-2` (tinted). Provides visual rest after hero.
- Screenshot has subtle elevation (shadow token from DESIGN.md).
- Mobile: same stack, screenshot full width.

## §4 How it works — contained, three columns

┌──────────────────────────────────────────────────────────────────────┐
│  [eyebrow]                                                           │
│  [headline]                                                          │
│                                                                      │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                           │
│  │  [01]   │    │  [02]   │    │  [03]   │                           │
│  │  [illu] │    │  [illu] │    │  [illu] │                           │
│  │ [title] │    │ [title] │    │ [title] │                           │
│  │ [blurb] │    │ [blurb] │    │ [blurb] │                           │
│  └─────────┘    └─────────┘    └─────────┘                           │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Three illustrations from MEDIA Home how.
- Mobile: stacks to one column, vertical line connecting the three steps.

## §5 Features grid — contained, 3 × 2 grid (6 cards)

┌──────────────────────────────────────────────────────────────────────┐
│  [eyebrow]                                                           │
│  [headline]                                                          │
│                                                                      │
│  ┌────────┐  ┌────────┐  ┌────────┐                                  │
│  │ icon   │  │ icon   │  │ icon   │                                  │
│  │ title  │  │ title  │  │ title  │                                  │
│  │ blurb  │  │ blurb  │  │ blurb  │                                  │
│  └────────┘  └────────┘  └────────┘                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐                                  │
│  │ icon   │  │ icon   │  │ icon   │                                  │
│  │ title  │  │ title  │  │ title  │                                  │
│  │ blurb  │  │ blurb  │  │ blurb  │                                  │
│  └────────┘  └────────┘  └────────┘                                  │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Renders from CONTENT.FEATURES top 6.
- Each card is a link to /features/<key>.
- Mobile: 2 × 3 (2 columns, 3 rows). Below 480px: 1 column.

## §6 Testimonial — contained, two-column (quote left, photo+logo right)

┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   "[quote — large display type]"               ┌────────────┐        │
│                                                │  photo     │        │
│   — [author], [role]                           └────────────┘        │
│   [company logo]                                                     │
│                                                                      │
│   [secondary CTA → /customers/<slug>]                                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Quote large enough to be the section's headline.
- Mobile: photo stacks above quote, smaller.

## §7 FAQ — contained, single column, accordion

┌──────────────────────────────────────────────────────────────────────┐
│  [eyebrow]                                                           │
│                                                                      │
│  ▸ Question 1                                                        │
│  ▸ Question 2                                                        │
│  ▸ Question 3                                                        │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Renders from CONTENT.FAQS where pages contains 'home'.
- Click to expand. One open at a time.

## §8 Final CTA — full-bleed, centred

┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                          [headline]                                  │
│                          [subhead]                                   │
│                                                                      │
│                          [CTA primary]                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Section background: `--surface-3` or accent-tinted, to close the page visually.
- No secondary CTA.

## Footer — shared across all pages

┌──────────────────────────────────────────────────────────────────────┐
│  Product       Customers      Compare        Company       Legal    │
│  - features    - index        - vs items     - about       - all     │
│  - pricing     - per-cust     (auto from     - blog        LEGAL    │
│  - changelog                  CONTENT)                      rows    │
│                                                                      │
│  [logo]                                       © year, [brand]        │
└──────────────────────────────────────────────────────────────────────┘

Notes:
- Footer renders from SITEMAP.md § Footer columns.
```

---

## Rhythm rules

A good marketing page alternates:

- **Container width** — full-bleed → contained → full-bleed → contained. Two consecutive full-bleed sections lose rhythm.
- **Background** — base → tinted → base → accent. Avoid four consecutive sections on the same background.
- **Direction** — image-left → image-right → centred → grid. Avoid three consecutive image-left sections.
- **Density** — sparse hero → busier proof → grid breadth → sparse testimonial. The eye needs breathing room.

The layout sketch is where rhythm gets locked. `build-component` follows it.

---

## Cross-references — every block points at brief, copy, media

Every block in the sketch references its source files:

- `§N Hero` → maps to brief's Section N → copy's Section N → MEDIA's `<page> § Hero`.
- Visual anchors point at MEDIA rows: `(anchor: MEDIA Home hero)`.
- Data sources point at CONTENT tables: `renders from CONTENT.FEATURES top 6`.

This is what makes `build-component` work mechanically. The implementer reads the layout block, follows the references, and produces JSX without having to invent anything.

---

## Hard rules

- **One layout file per page in SITEMAP.md.** No fewer, no more.
- **Each block names its brief section.** `§1`, `§2`, … matching the brief's section order.
- **Each block declares container behaviour** — full-bleed vs contained.
- **Each block declares mobile behaviour** — how it stacks.
- **Visual anchors reference MEDIA.md** — never restate what the anchor is, point at the manifest row.
- **Data sources reference CONTENT.md** — never inline a feature or testimonial.
- **No pixels.** ASCII boxes show relative width, not absolute. The implementer picks the actual values from `agents/DESIGN.md` tokens.
- **Footer + nav are sketched once** in `layouts/home.md` (or a dedicated `layouts/_shell.md`) and reused. Not redrawn per page.
- **Rhythm check before locking** — full-bleed / contained alternation, background alternation, image-side alternation. If three consecutive sections are identical in those axes, re-arrange.
