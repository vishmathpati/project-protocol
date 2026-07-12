# Phase 5 — Three named directions (v2.1)

Propose exactly 3 directions. They must be **meaningfully different** — sit at different points on the remaining design space. Not 3 flavours of the same thing.

v2.1 adds anti-convergence rules at proposal time. The old version drifted toward Inter + neutral grey + soft shadow on every direction. The rules below force material-first thinking and category diversity so each direction is distinctive enough to be remembered.

**Before proposing, read `brain/research/concepts.md`, the `brain/research/teardowns/` files, `brain/moodboard/notes.md`, and the FOLLOW / DEVIATE / REFUSE conventions audit `calibrate` appended to `brain/DESIGN.md`** (all produced by calibrate's two-round pass at the end of Phase 4; skip if the user skipped calibrate). The named concepts and teardown evidence describe the field the chosen concept lives in; FOLLOW items feed "Borrows from moodboard"; DEVIATE and REFUSE items sharpen "Departs from moodboard" and the distinctive asset. The concepts map the field — they never cap ambition: Rule 7 below still forces at least one direction to depart from everything found. Do NOT re-invoke `calibrate` — it already ran.

---

## Section 1 — Shape of each direction

Each direction is a structured block. Material comes first; hex codes attach last; the character/material IS the proposal.

```
Direction <N> — "<evocative name>"

  Material:    <material vocabulary — e.g. "warm parchment + oxblood ink + brass accent">
  Temperature: <warm | cool | neutral>
  Saturation:  <muted | tinted | jewel>

  Light mode:
    paper: #XXXXXX (<character>)
    ash:   #XXXXXX (<character>)
    ink:   #XXXXXX (<character>)
    character: <one line describing the felt material>

  Dark mode:
    paper: #XXXXXX (<character>)
    ash:   #XXXXXX (<character>)
    ink:   #XXXXXX (<character>)
    character: <one line — paired temperature with light mode>
    rule:    <e.g. "never pure #000 — 6% warm tint toward brand temperature">

  Type:
    display: <distinctive face, NOT from banned list> (<category>)
    body:    <Inter / Geist / Söhne etc. acceptable here>
    mono:    <mono face>

  Accent: <material name> #XXXXXX (hover: #XXXXXX)

  Reference: <one URL to model layout after>

  Why it fits: <one or two lines connecting back to locked diagnostic axes>

  Borrows from moodboard: <list which moodboard sites and what specifically — e.g.,
                          "Stitch Fix warm cream + serif headline rhythm; Vogue India
                          editorial photography hierarchy"> | "nothing literal"

  Departs from moodboard: <list what this direction deliberately does NOT do — e.g.,
                          "Stripe's cool restraint (this runs warmer)"; "Pinto's
                          editorial density (this is sparer)">

  Distinctive asset:      <one sentence — the visual thing nobody else in the
                          category owns that this direction would let the brand
                          own. e.g., "cream paper + oxblood ink + Migra display
                          — none of the 5 reference sites pair these.">
```

The third line (`Distinctive asset`) is the load-bearing one — it forces the agent to articulate what makes this direction *ownable*, not just *visible*. For the mandated outside-envelope direction (see Rule 7), `Borrows from moodboard:` should literally read "nothing literal" or "trust ceiling only — proves audience accepts ambition, no surface inheritance."

Use evocative names with material vocabulary, not technical labels:

- Good: "Editorial Cream", "Mughal Velvet", "Sage Concrete", "Brass Library"
- Bad: "Light mode", "Minimalist option", "Direction A", "#F5EFE4 theme"

Hex never appears in the name. The material does.

---

## Section 2 — Anti-convergence rules (HARD constraints)

These are gates, not suggestions. If a proposed direction fails a rule, regenerate it before showing the user.

### Rule 1 — Banned-from-display list

These fonts CANNOT appear as `font.display`. They CAN appear as `font.body` or `font.mono`:

- Inter
- Geist
- Söhne
- IBM Plex (Sans / Serif / Mono — all)
- SF Pro
- Roboto
- Space Grotesk
- Open Sans
- Public Sans
- system-ui
- Manrope
- Aeonik

**Reason**: these are statistical-center "convergence defaults" — every AI-assisted brand pitch uses them as display, so using them for DISPLAY signals "AI-generated, no taste applied." Body-role use is fine; they were designed for that.

If the locked diagnostic genuinely requires one of these (rare — e.g. dev-tool brand explicitly asking for Geist as display), note the exception explicitly and explain why the rule is being broken.

### Rule 2 — Forced font category diversity

Each of the 3 directions must pull display from a **DIFFERENT** category. Valid categories:

- **Transitional serif** — Tiempos, Lyon, Editorial New, GT Sectra, GT Super, Fraunces
- **High-contrast display serif** — Migra, Cooper, Tobias, Reckless, Domaine Display
- **Geometric grotesque distinct from defaults** — Söhne Breit, PP Right Grotesk, Migra Italic, GT America Extended
- **Humanist sans** — FF Real, Lyon Display Sans, Söhne (note: Söhne body OK, Söhne display only if not in another direction)
- **Slab serif** — Roboto Slab, Lora Slab, PP Editorial Old Slab, Caslon Slab
- **Display / expressive** — Boogy Brut, Reckless, Daydreamer, PP Right Didone, Migra
- **Mono-as-display** — Söhne Mono, PP Fraktion Mono, JetBrains Mono Display
- **Indian foundry** — Kohinoor Latin, Anek Latin, Saans, Karm (Indian Type Foundry); reserve for cultural-anchor = Indian projects

No two directions can share the same category. If two collide → regenerate one.

### Rule 3 — Forced palette character diversity (4 axes)

Each direction must vary across **4 axes**, in this order:

1. **Temperature** — warm | cool | neutral
2. **Saturation** — muted | tinted | jewel
3. **Material reference** — paper | parchment | ash | leather | velvet | stone | cream | concrete | linen | porcelain (name the material out loud)
4. **Lightness band** — high-key (light dominant) | mid-key | low-key (dark dominant)

Lightness band comes LAST. Material/temperature/saturation are the personality; lightness is just a value. The old conservative version led with lightness ("light mode option, dark mode option") and that's the convergence trap.

**Diversity threshold**: no two directions can share more than 2 of the 4 axes. If two directions collide on 3+ axes → regenerate one.

Example collisions to avoid:
- Two "warm + muted + paper" directions (3 axes shared) → regenerate.
- Two "cool + muted" directions where materials and lightness differ → fine (only 2 shared).

### Rule 4 — Each direction proposes BOTH light AND dark mode

Not one, not "we'll figure out dark later." Both. With paired characters that share the direction's temperature and material story.

- Light mode never pure `#FFFFFF`. Tint 4-8% toward brand temperature.
- Dark mode never pure `#000000`. Tint 4-8% toward brand temperature.

Examples:
- Warm direction light: `#F5EFE4` (warm cream), not `#FFFFFF`.
- Warm direction dark: `#1A0F0A` (warm near-black, leather), not `#000000`.
- Cool direction light: `#F4F6F8` (cool porcelain), not `#FFFFFF`.
- Cool direction dark: `#0A0E14` (cool near-black, ink), not `#000000`.

A jewel-saturation direction may use the jewel tone AS dark mode (burgundy `#2A0E14`, deep emerald `#0A1A12`) — the jewel tone IS the dark UI; no separate "dark mode" decision needed.

### Rule 5 — Live reference search

If web search is available (WebSearch tool), use it. Queries to run:

- `"<archetype> <cultural-anchor> brand 2026"`
- `"modern <category> design India 2026"` (or relevant region)
- `"<material-word> editorial brand site"` (e.g. "parchment editorial brand site")
- `"<display-font-category> brand identity 2026"`

Pull live references. Don't reach for training-data guesses (vogue.in, stitchfix.com etc. as muscle memory) when fresher work exists.

If web search is unavailable → default to knowledge but note "references from training data — verify they're still live before locking the direction."

### Rule 6 — Material-first proposal language

Each direction's first line is material vocabulary, not adjectives.

- Good: "warm parchment + oxblood ink + brass accent"
- Good: "sage cream + stone grey + terracotta accent"
- Good: "ivory paper + deep burgundy velvet + gold accent"
- Bad: "warm and editorial" (adjective, not material)
- Bad: "premium minimalist" (means nothing)
- Bad: "modern Indian" (cultural-anchor, not material)

Hex codes attach LAST, inside the light/dark token blocks. The character/material is the proposal; hex is a value.

### Rule 7 — Mandated departure (at least one direction outside the moodboard envelope)

Of the 3 directions:

- Up to 2 may sit **INSIDE** the moodboard envelope — borrowing material, palette intent, or type pairing from the 3–5 reference sites.
- At least 1 MUST sit **OUTSIDE** the moodboard envelope — different material, different temperature, different category code than anything in the moodboard. This is the direction that gives the brand a chance to own a distinctive asset (per Byron Sharp).

The user can still pick a safe (inside-envelope) direction — but they must be given the choice. A Phase 5 output of 3 inside-envelope directions has failed.

If the moodboard already spans the visual space well (e.g., includes both editorial-warm and clinical-cool), the "outside" direction must go somewhere even further — into territory the moodboard sites collectively avoid (e.g., cultural-anchor-specific palettes, traditional craft references, brutalist anti-design, etc.).

### Anti-moodboard-convergence

In addition to the inter-direction rules above, the 3 directions must collectively
ensure moodboard distance:

- **Pairwise material distance from moodboard.** No direction may share ALL of
  (material vocabulary + temperature + saturation tier) with any single moodboard
  site. If Direction A is "warm cream + serif" and Stitch Fix is in the moodboard,
  A must differentiate on at least one other axis (e.g., the accent material —
  "oxblood" rather than Stitch Fix's "blush coral").

- **Category-code distance.** If the moodboard is dominated by one category code
  (e.g., 4 of 5 sites are "premium fintech minimalism"), at least one direction
  must explicitly break that code — different decoration density, different type
  hierarchy, different photo treatment, different motion temperament.

- **Mandated outside-envelope direction.** As above — exactly one of the 3
  directions must have "Borrows from moodboard: nothing literal." This is the
  agent's chance to bring in cultural-anchor-specific or category-rare territory
  (Indian textile palettes, Japanese ma, brutalist anti-design, archival craft,
  etc.) that the moodboard's safety-first selection deliberately omitted.

---

## Section 3 — Worked example output

This is the format the user sees. Three directions, each block self-contained, all three satisfying the locked diagnostic.

```
Three directions — meaningfully different, all satisfy the locked diagnostic.

Direction 1 — "Editorial Cream"
  Material:    warm parchment + oxblood ink + brass accent
  Temperature: warm
  Saturation:  muted

  Light mode:
    paper: #F5EFE4 (warm cream)
    ash:   #EDE6D8 (raised paper)
    ink:   #1A1410 (warm near-black)
    character: editorial parchment, like an old book

  Dark mode:
    paper: #1A0F0A (warm near-black leather)
    ash:   #261A12 (raised leather)
    ink:   #F5EFE4 (warm ivory)
    character: leather + brass, paired with cream light mode
    rule:    never pure #000 — 6% warm tint toward brand temperature

  Type:
    display: Migra (high-contrast display serif)
    body:    Inter
    mono:    JetBrains Mono

  Accent: brass #B8895A (hover: #A07A4F)

  Reference: aesop.com layout, harpersbazaar.in for type

  Why it fits: archetype=Lover/Sage, cultural=Indian-formal, trust-stakes=medium,
  category-maturity=code-fluid (lifestyle/editorial). Material story
  (parchment+leather) matches the "premium but not corporate" emotional brief.

  Borrows from moodboard: Aesop's warm parchment paper + serif headline rhythm;
                          Harper's Bazaar India editorial type hierarchy.
  Departs from moodboard: Aesop's near-monochrome restraint (this carries an
                          oxblood ink + brass accent, not a single neutral).
  Distinctive asset:      cream parchment + oxblood ink + Migra display — none of
                          the moodboard sites pair these three.

Direction 2 — "Sage Concrete"
  Material:    sage cream + stone grey + terracotta accent
  Temperature: neutral
  Saturation:  muted

  Light mode:
    paper: #F2F1EC (sage cream)
    ash:   #E8E7E0 (raised stone)
    ink:   #1F2220 (cool near-black)
    character: studio-architect's notebook

  Dark mode:
    paper: #14171A (cool slate)
    ash:   #1E2125 (raised concrete)
    ink:   #F2F1EC (sage ivory)
    character: poured concrete at dusk, paired with sage light mode
    rule:    never pure #000 — 4% cool tint toward slate

  Type:
    display: Tobias (transitional serif)
    body:    Geist
    mono:    Geist Mono

  Accent: terracotta #C2410C (hover: #A93608)

  Reference: kontrapunkt.com for layout, klim.co.nz/blog for type-in-context

  Why it fits: archetype=Sage/Creator, category-maturity=code-fluid, trust-stakes=high.
  Neutral temperature reads as "considered, not warm-and-fuzzy." Stone material
  signals durability without going corporate-cold.

  Borrows from moodboard: Kontrapunkt's tight grid + sage-cream neutrality; Klim's
                          studio-architectural type-in-context discipline.
  Departs from moodboard: Aesop's warm parchment (this is cooler, more clinical);
                          any moodboard editorial-density (this is sparer).
  Distinctive asset:      sage cream + terracotta accent + Tobias transitional
                          serif — the "architect's notebook" voice; nobody else
                          in the moodboard pairs sage with terracotta.

Direction 3 — "Mughal Velvet"
  Material:    ivory paper + deep burgundy velvet + gold accent
  Temperature: warm
  Saturation:  jewel

  Light mode:
    paper: #FAF5EC (ivory paper)
    ash:   #F0E9D9 (raised ivory)
    ink:   #2A0E14 (burgundy ink — not black)
    character: handwritten invitation card

  Dark mode:
    paper: #2A0E14 (deep burgundy velvet — NOT black)
    ash:   #3A1820 (raised velvet)
    ink:   #FAF5EC (ivory)
    character: jewel-dark, deep but warm, ZERO neutrality
    rule:    burgundy IS the dark mode; no separate "dark" decision

  Type:
    display: Kohinoor Latin (Indian Type Foundry — slab geometric)
    body:    Inter
    mono:    Roboto Mono

  Accent: gold leaf #B8895A (hover: #A07A4F)

  Reference: goodearth.in for color/maximalism, harpersbazaararabia.com for type

  Why it fits: archetype=Ruler/Magician, cultural=Indian-celebration, trust-stakes=medium.
  The burgundy dark mode IS the distinctive asset — nobody else proposes burgundy
  as a UI background; it'll be remembered. Maximalism is the differentiator.

  Borrows from moodboard: nothing literal — trust ceiling only (the moodboard
                          proves the audience accepts editorial ambition, but no
                          surface inheritance from any single site).
  Departs from moodboard: every moodboard site — none carry jewel-saturation
                          burgundy, Indian Type Foundry display, or maximalist
                          decoration density.
  Distinctive asset:      burgundy-as-UI-background + Kohinoor Latin display +
                          gold leaf accent — nobody in the category owns this
                          combination; it would be remembered after one exposure.
  [MANDATED OUTSIDE-ENVELOPE direction — satisfies Rule 7.]

Pick one — or pick a hybrid (e.g., "Direction 1 type, Direction 3 palette").
```

### Section 3b — Snapfinder-style worked example (showing the new structure end-to-end)

Same template, applied to a fictional Snapfinder-like brand (modern Indian fashion / find-the-look product). The moodboard for this brief contains Stitch Fix, Stripe, Klarna, Pinto, and Vogue India.

```
Direction A — "Editorial Cream"  (inside-envelope, safe)
  Material:    warm cream + oxblood ink + brass accent
  Temperature: warm
  Saturation:  muted

  Borrows from moodboard: Stitch Fix's warm cream + serif headline rhythm; Vogue
                          India's editorial photo hierarchy.
  Departs from moodboard: Stripe's cool restraint (this runs warmer); Klarna's
                          flat-illustration accent system (this uses photography).
  Distinctive asset:      cream paper + oxblood ink + Migra display — none of
                          the 5 moodboard sites pair these three.

Direction B — "Premium Tech"  (inside-envelope, opposite pole)
  Material:    cool ivory + slate ink + one hot accent
  Temperature: cool
  Saturation:  muted (with one jewel accent)

  Borrows from moodboard: Stripe's cool ivory + tight grid; Klarna's single-accent
                          moment.
  Departs from moodboard: Pinto's editorial density (this is sparer); Vogue India's
                          photography weight (this leads with type).
  Distinctive asset:      the "you-found-it" moment carries the brand — one hot
                          accent on a near-neutral system; the product moment IS
                          the brand expression.

Direction C — "Bazaar Modern"  (MANDATED OUTSIDE-ENVELOPE — Rule 7)
  Material:    Khadi paper + indigo + turmeric + brick accent
  Temperature: warm
  Saturation:  jewel

  Inspired by: traditional Indian textile palettes (indigo + turmeric + brick),
               Khadi paper texture, Devanagari + Latin display pairings.

  Borrows from moodboard: nothing literal — trust ceiling only (the moodboard
                          proves the audience accepts ambitious editorial
                          execution; no surface inheritance from any site).
  Departs from moodboard: every moodboard site — none of Stitch Fix, Stripe,
                          Klarna, Pinto, or Vogue India carry traditional
                          Indian craft references.
  Distinctive asset:      nobody in the category (Myntra, Ajio, Nykaa) owns
                          "modern Indian fashion infrastructure" visually —
                          indigo + turmeric + Khadi texture + Devanagari-Latin
                          display pairing would let Snapfinder own it.
```

Notice: A and B both sit inside the moodboard envelope (the user gets a real safe choice), but C goes somewhere none of the reference sites went. The user picks — but they're picking between *inside-envelope* and *ownable*, not between three remixes of the same moodboard.

---

## Section 4 — Hard rules summary

- **Exactly 3 directions** (or 2 with explicit explanation if the diagnostic genuinely admits only 2).
- **No hex codes in NAMES.** Materials in names ("Editorial Cream", not "#F5EFE4 theme").
- **Each direction proposes BOTH light AND dark mode**, with paired characters that share temperature and material story.
- **Banned-from-display list enforced** (Rule 1). Inter / Geist / Söhne / IBM Plex / SF Pro / Roboto / Space Grotesk / Open Sans / Public Sans / system-ui / Manrope / Aeonik — body role only.
- **Font category diversity enforced** (Rule 2). 3 directions = 3 different display categories. No collisions.
- **Palette character diversity enforced** (Rule 3). 4 axes: temperature, saturation, material, lightness. No two directions share more than 2 axes.
- **Material-first language** (Rule 6). First line is material vocabulary, hex codes attach last.
- **Mandated departure enforced** (Rule 7). At least 1 of 3 directions MUST sit outside the moodboard envelope ("Borrows from moodboard: nothing literal"). 3 inside-envelope directions = Phase 5 has failed.
- **Anti-moodboard-convergence enforced.** No direction shares all of (material + temperature + saturation) with any single moodboard site. If the moodboard is dominated by one category code, at least one direction breaks the code.
- **Every direction block declares Borrows / Departs / Distinctive asset.** Distinctive asset is load-bearing — it names the ownable visual thing.
- **Light mode never pure `#FFF`. Dark mode never pure `#000`.** Tint 4-8% toward brand temperature.
- **Live reference search if available** (Rule 5). Don't lean on training-data muscle memory.
- **All references in BRAND.md refusal list respected.** If a direction would require violating a refusal, drop it.
- **Allow hybrids in Phase 6.** Don't force a single-direction pick.

---

## Why these rules exist (research notes)

Short version for the curious — grounded in the field research in `brain/research/` (concepts.md + teardowns/) when calibrate has run.

- **Impeccable benchmark (2025)**: when AI-assisted brand pitches converge on Inter + neutral grey + soft shadow at 70%+ frequency, distinctiveness drops below the threshold for brand recall. The fix is forced category divergence at proposal time, not at refinement time.
- **Klim Type Foundry case studies**: distinctive brands earn memorability through *display* face character; body face can be utility (Inter is fine). Don't waste the display slot on a convergence default.
- **Refactoring UI tinted-grey method**: pure `#FFF` / `#000` read as "untouched defaults." Tinting 4-8% toward brand temperature signals "intentional" without being loud.
- **Cardamone (2025) optimal distinctiveness**: brands need to be similar enough to category to be legible, different enough to be remembered. The 4-axis palette diversity rule keeps 3 directions inside the legible band while forcing memorable variance.

These rules trade a small amount of agent freedom at proposal time for a much larger gain in distinctiveness at lock-time. Worth it.
