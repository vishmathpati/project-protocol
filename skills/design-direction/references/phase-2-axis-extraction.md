# Phase 2 — Silent axis extraction

The agent (not the user) extracts the 10 taste axes from the dump. The user never sees the axis labels — they see the synthesised diagnostic in Phase 3.

Use a Sonnet-tier sub-agent for this if the dump is long. Pure pattern-recognition on a short dump can run inline.

**Research grounding** — this axis set is calibrated to:
- **Cardamone (2025) — optimal distinctiveness**: brands win by being different enough to be remembered AND similar enough to be trusted. Both halves matter.
- **Byron Sharp — distinctive brand assets**: memorability comes from owning 1–2 non-category visual assets (color, character, shape, sound).
- **Marty Neumeier — Zag**: when everyone zigs, zag — but only in categories where zagging is allowed.
- **Jaguar 2024**: the canonical "breaking category codes backfires" case. Lost 93% of sales after the rebrand in a code-locked premium-auto category.
- **Mark & Pearson archetypes**: personality scaffolding.

**Two axes dropped from v1** — `surface_mix` (derived from product description) and `tempo` (derived from archetype + cultural anchor). Both are now treated as outputs of other axes, not independent inputs.

**Three axes added in v2.1** — `trust_stakes`, `category_maturity`, `distinctive_asset`. These come directly from the research above and answer questions the v1 set was missing: *what does failure cost?*, *is this category visually locked or fluid?*, and *what will this brand be remembered for?*

---

## The 10 axes

### 1. Trust temperature — Max / High / Medium / Low

How much warmth or coolness the visual system should carry. The single most constraining *aesthetic* axis.

- **Max** — pared-down, monochrome-leaning, almost no decoration. Banking, payments, medical, legal.
- **High** — restrained, calm, modest accent colour. Professional tools, B2B SaaS, customer-facing data.
- **Medium** — confident colour, expressive type, some texture. Consumer SaaS, design-conscious daily tools.
- **Low** — playful, saturated, motion-heavy. Entertainment, memes, social, casual creator tools.

Hints in dump: words like "serious", "professional", "compliance", "audit" push toward Max/High. Words like "fun", "playful", "vibes", "personality" push toward Medium/Low.

> Note: trust temperature is about how the brand *looks*. Trust stakes (axis 2) is about what failure *costs*. They usually correlate but not always — a payroll product (high stakes) can choose to look Medium-warm if the brand wants to feel human in a cold category. Keep them separate.

### 2. Trust stakes — Money / Health / Time-Embarrassment / Boredom

**New in v2.1.** Ask: *"If my customer loses confidence in this product, what does it COST them?"*

This determines how much *room* the brand has to break category codes. Higher stakes = stronger pull toward conforming. Lower stakes = more freedom to differentiate visibly.

- **Money** — payroll, payments, investment, tax, insurance, accounting. Failure costs real currency. Strongest pull to category codes.
- **Health** — medical, mental health, pharma, fitness-with-clinical-claims, food-safety. Failure costs wellbeing. Strong pull to category codes.
- **Time-Embarrassment** — work tools where failure costs reputation, lost hours, public-facing creative work, customer-facing collateral. Moderate pull to category codes.
- **Boredom** — entertainment, memes, casual creator tools, hobby apps, recommendation toys. Failure costs attention. Lowest pull — most freedom to break.

Heuristic: extract straight from the product description.
- "payroll software" → Money
- "tea recommendation app" → Boredom
- "tool for indie wedding photographers to share proofs" → Time-Embarrassment (their reputation is on the line)
- "mental health journal" → Health
- "meme generator" → Boredom

Hints in dump: dollar amounts, regulatory words, "their livelihood", "their data", "compliance" → Money/Health. "Just for fun", "social", "hobby", "playful" → Boredom.

### 3. Use frequency — Daily-hours / Daily-seconds / Weekly / Occasional / One-time

- **Daily-hours** — dashboards, CRMs, IDEs, design tools. The user lives in the surface. Design must be calm.
- **Daily-seconds** — quick utility apps (style picker, water tracker, mood log). Many opens, short sessions. Design can be more expressive.
- **Weekly** — review tools, planners, expense apps.
- **Occasional** — tax filing, insurance, government services.
- **One-time** — checkout, registration, surveys.

Hints in dump: "all day", "open constantly", "live in this tool" → daily-hours. "Quick check", "few seconds", "in and out" → daily-seconds. "Once a month", "every quarter" → occasional.

### 4. Information density — Data-dense / Content-light / Mixed

- **Data-dense** — tables, charts, lists, lots of metadata per row (Linear, Bloomberg, GitHub, Stripe Dashboard).
- **Content-light** — large images, big type, single subject per screen (Apple.com, Airbnb, marketing sites).
- **Mixed** — content-light marketing + data-dense product.

Hints: "analytics", "reports", "every event", "logs" → data-dense. "Photos", "videos", "showcase", "feel" → content-light.

### 5. Cultural anchor — Global-tech / Indian-formal / Indian-casual / Indian-celebration / Japanese-minimal / Western-consumer / etc.

Where does the audience live, and what visual vocabulary do they already trust?

- **Global-tech** — monochrome, Inter/Geist, sharp grid, dark mode optional. Default for B2B SaaS targeting international developers.
- **Indian-formal** — calm cream and ink, restrained, suitable for banks/insurance/legal aimed at urban India.
- **Indian-casual** — warm color, expressive, suitable for consumer apps (food, fashion, travel) in India.
- **Indian-celebration** — jewel tones (gold, peacock teal, deep red), warmth, ornament. Weddings, events, festivals.
- **Japanese-minimal** — aggressive whitespace, tight grid, monospace accents.
- **Western-consumer** — bright colour, curves, real-people photography.

Hints: customer geography in the dump, language register, examples named (Stripe → global-tech, MasterJi → Indian).

### 6. Brand archetype — pick one of 12

Use the Jungian / Mark & Pearson archetypes. Pick the *primary*. A secondary is allowed but the primary dictates personality.

| Archetype | Promise | Voice | Example brands |
|---|---|---|---|
| Sage | "I help you understand" | Calm, clear, evidence-based | Stripe, Linear, Notion |
| Magician | "I transform you" | Confident, almost mystical | Apple, Tesla |
| Caregiver | "I look after you" | Warm, reassuring | Airbnb, Headspace |
| Rebel | "I break the rules with you" | Sharp, irreverent | Liquid Death, Patagonia |
| Creator | "I help you make things" | Inspiring, craft-focused | Figma, Adobe |
| Hero | "I help you win" | Driven, results-focused | Nike, Salesforce |
| Explorer | "I help you discover" | Open, adventurous | Airbnb, Patagonia |
| Innocent | "Everything is simple here" | Optimistic, plain | Dove, Coca-Cola |
| Lover | "Beauty matters" | Sensory, intimate | Aesop, Chanel |
| Jester | "Let's have fun" | Witty, light | Mailchimp, Slack |
| Ruler | "Authority and order" | Stately, classical | Rolex, IBM |
| Everyman | "I'm one of you" | Friendly, accessible | Target, IKEA |

Hints: tone in the dump ("we want to feel like" / "we are not corporate" / "we should feel like a luxury brand").

### 7. Reference tribe — 3 look-like + 1 look-unlike

Pick 3 sites the audience already trusts and respects. Pick 1 incumbent the product should deliberately *not* resemble.

- Look-like sites = visual vocabulary the audience recognises → trust transfer.
- Look-unlike incumbent = forces visible differentiation → memorability.

Hints: any sites named in the dump, market the product is in (figure the canonical sites for that market).

### 8. Category maturity — Code-locked / Code-fluid

**New in v2.1.** Is the brand's category VISUALLY LOCKED or CODE-FLUID? This decides whether the brand should *conform* or *break*.

- **Code-locked** — categories where every player looks alike for a reason, and breaking codes LOSES trust. Banking, payments, B2B SaaS infrastructure, healthcare, govt, insurance, legal, enterprise compliance. The 80/20 rule applies: conform on ~80% of category codes (layout, restraint, palette discipline) and differentiate on ~20% (one ownable asset, one signature move).
- **Code-fluid** — categories with no enforced visual language, where breaking IS the competitive edge. Creator tools, fashion, food, hospitality, lifestyle, indie media, music. Conform on ~20% (basic usability conventions) and differentiate on ~80%.

The canonical cautionary case: **Jaguar 2024** broke codes hard in a code-locked premium-auto category (pastel pink, sans-serif, no cars in launch creative) and lost an estimated 93% of UK sales. The lesson is not "don't break codes" — it's "know which category you're in before you do."

Heuristic: ask "would the audience be unsettled if this looked nothing like the incumbents?"
- Bank that looks like a creator tool → unsettling → code-locked
- Recipe app that looks like a bank → unsettling but in a fun way → code-fluid

Hints in dump: trust stakes already extracted. Money/Health stakes → almost always code-locked. Boredom stakes → almost always code-fluid. Time-Embarrassment can go either way; check the named look-like tribe — if they all look alike (Notion, Linear, Height, Asana) the category is code-locked; if they all look different (Mailchimp, Slack, Figma, Loom) it's code-fluid.

### 9. Distinctive asset — 1–2 ownable, non-category visual assets

**New in v2.1.** Following Byron Sharp: memorability is built by owning 1–2 things that are NOT category-default. Required field — every brand needs at least one. If the user can't name one, surface that gap explicitly: *"your brand has no distinctive asset yet; pick one before we lock the direction."*

Format: name the asset concretely. Not "a colour" — "Tiffany robin's-egg blue applied to every surface that touches the customer." Not "a typeface" — "monospaced lowercase wordmark inspired by IBM Plex Mono."

Reference examples of distinctive assets that print money:

| Brand | Distinctive asset |
|---|---|
| Tiffany | The specific robin's-egg blue (Pantone 1837) |
| Mailchimp | Freddie the chimp wink + Cooper Light wordmark |
| Liquid Death | The tallboy can shape + heavy-metal type |
| CRED | Copper-on-black palette |
| Cadbury | Pantone 2865C purple |
| Stripe | Three-stop gradient + clean black wordmark |
| Linear | Hard square corners + monochrome grid |
| Mercury | Spinning iridescent orb + serif headline pairing |
| Patagonia | The mountain-skyline logo + earth-tone restraint |
| Coca-Cola | Spencerian script + the bottle silhouette |

Pick assets that are:
- **Ownable** — not already used by 5 incumbents in the category.
- **Non-category** — they don't appear in the default visual vocabulary of the market.
- **Applicable across surfaces** — work on a landing page, a button, an email, a t-shirt.

Hints in dump: anything the user is precious about ("the green has to stay", "we want a mascot", "I'd love an interactive element on the hero"). If nothing is offered, propose one and confirm in Phase 3.

### 10. Refusal list — 3–5 things this brand never does

Mix of:

- **User-stated refusals** — anything they said in "what should it NOT look like".
- **Archetype-derived refusals** — e.g., Sage archetype refuses emojis-as-icons; Lover archetype refuses generic stock photography; Rebel archetype refuses corporate-blue.
- **Tribe-derived refusals** — anti-patterns visible in the look-unlike incumbent.
- **Category-derived refusals** — if code-locked, refuse the dominant cliché (e.g., banking refuses "stock photo of suited men shaking hands"). If code-fluid, refuse the safest default (e.g., consumer creator tool refuses generic gradient hero).

Aim for 3–5 concrete refusals. Not "no bad design" — "no two-stop blue→purple gradients", "no clip-art-style illustrations", "no body-shaming copy".

---

## Output shape (passed to Phase 3)

A locked object like:

```yaml
trust_temperature: high
trust_stakes: money              # NEW — what does failure cost the customer
use_frequency: daily-hours
info_density: data-dense
cultural_anchor: global-tech
archetype: sage
secondary_archetype: caregiver   # optional, can be empty
reference_tribe:
  look_like: [stripe.com, mercury.com, linear.app]
  look_unlike: bitly.com
category_maturity: code-locked   # NEW — brand should conform 80%, break 20%
distinctive_asset:               # NEW — 1–2 ownable, non-category assets
  - "single uppercase status color (electric green) for all positive states"
  - "monospaced legal copy in footer"
refusals:
  - no two-stop gradients
  - no stock photos of suits in glass offices
  - no traffic-light approve/reject patterns
  - no emoji-as-icon
```

Or for a code-fluid consumer example:

```yaml
trust_temperature: medium
trust_stakes: boredom
use_frequency: daily-seconds
info_density: content-light
cultural_anchor: indian-casual
archetype: jester
secondary_archetype: explorer
reference_tribe:
  look_like: [liquiddeath.com, oatly.com, magicspoon.com]
  look_unlike: zomato.com
category_maturity: code-fluid
distinctive_asset:
  - "hand-drawn marker illustrations of every tea leaf"
  - "deliberate typos in headlines as a voice signature"
refusals:
  - no minimalist global-tech sans-serif
  - no flat product photography on grey
  - no wellness clichés (hands holding mugs, sunrise gradients)
```

Do not surface this raw object to the user. Phase 3 turns it into prose.
