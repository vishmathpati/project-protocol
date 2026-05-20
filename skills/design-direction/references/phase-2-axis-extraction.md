# Phase 2 — Silent axis extraction

The agent (not the user) extracts the 9 taste axes from the dump. The user never sees the axis labels — they see the synthesised diagnostic in Phase 3.

Use a Sonnet-tier sub-agent for this if the dump is long. Pure pattern-recognition on a short dump can run inline.

---

## The 9 axes

### 1. Trust temperature — Max / High / Medium / Low

The single most constraining axis. Ask: *"If my customer loses confidence in this product, what does it cost them?"*

- **Max** — money (banking, payments, investment), health (medical, drugs, mental health), legal (contracts, immigration), safety (security cameras, ride-hailing for women). Cost of failure: irrecoverable.
- **High** — work reputation, professional output, public-facing creative work, customer-facing data. Cost of failure: embarrassment + lost time.
- **Medium** — personal productivity, hobby work, consumer SaaS, design-conscious daily tools. Cost of failure: friction.
- **Low** — entertainment, memes, social, casual creator tools. Cost of failure: boredom.

Hints in dump: words like "secure", "private", "compliance", "regulated", "audit", "guests can see", "billing", "wedding" push toward Max/High. Words like "fun", "share", "casual", "vibes" push toward Low/Medium.

### 2. Use frequency — Daily-hours / Daily-seconds / Weekly / Occasional / One-time

- **Daily-hours** — dashboards, CRMs, IDEs, design tools. The user lives in the surface. Design must be calm.
- **Daily-seconds** — quick utility apps (style picker, water tracker, mood log). Many opens, short sessions. Design can be more expressive.
- **Weekly** — review tools, planners, expense apps.
- **Occasional** — tax filing, insurance, government services.
- **One-time** — checkout, registration, surveys.

Hints in dump: "all day", "open constantly", "live in this tool" → daily-hours. "Quick check", "few seconds", "in and out" → daily-seconds. "Once a month", "every quarter" → occasional.

### 3. Information density — Data-dense / Content-light / Mixed

- **Data-dense** — tables, charts, lists, lots of metadata per row (Linear, Bloomberg, GitHub, Stripe Dashboard).
- **Content-light** — large images, big type, single subject per screen (Apple.com, Airbnb, marketing sites).
- **Mixed** — content-light marketing + data-dense product.

Hints: "analytics", "reports", "every event", "logs" → data-dense. "Photos", "videos", "showcase", "feel" → content-light.

### 4. Cultural anchor — Global-tech / Indian-formal / Indian-casual / Indian-celebration / Japanese-minimal / Western-consumer / etc.

Where does the audience live, and what visual vocabulary do they already trust?

- **Global-tech** — monochrome, Inter/Geist, sharp grid, dark mode optional. Default for B2B SaaS targeting international developers.
- **Indian-formal** — calm cream and ink, restrained, suitable for banks/insurance/legal aimed at urban India.
- **Indian-casual** — warm color, expressive, suitable for consumer apps (food, fashion, travel) in India.
- **Indian-celebration** — jewel tones (gold, peacock teal, deep red), warmth, ornament. Weddings, events, festivals.
- **Japanese-minimal** — aggressive whitespace, tight grid, monospace accents.
- **Western-consumer** — bright colour, curves, real-people photography.

Hints: customer geography in the dump, language register, examples named (Stripe → global-tech, MasterJi → Indian).

### 5. Brand archetype — pick one of 12

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

### 6. Reference tribe — 3 look-like + 1 look-unlike

Pick 3 sites the audience already trusts and respects. Pick 1 incumbent the product should deliberately *not* resemble.

- Look-like sites = visual vocabulary the audience recognises → trust transfer.
- Look-unlike incumbent = forces visible differentiation → memorability.

Hints: any sites named in the dump, market the product is in (figure the canonical sites for that market).

### 7. Surface mix — Single-surface / Marketing+app / Multi-surface

- **Single-surface** — marketing site only, or app only. Can afford bespoke flourishes.
- **Marketing+app** — most SaaS. The classic split (expressive marketing + restrained product).
- **Multi-surface** — marketing + dashboard + email + docs + mobile + extension + Slack + invoices. Discipline required — bespoke moments break at seams.

Hints: how many surfaces the user listed.

### 8. Tempo — Motion-led / Static / Mixed

- **Motion-led** — animation is part of brand identity (Linear loaders, Cursor cursor, Stripe gradient, Vercel deploy logs).
- **Static** — almost no animation. Apple marketing, Notion, most B2B.
- **Mixed** — purposeful motion on key moments (page transitions, success states) but otherwise calm.

Hints: product nature — fashion / interactive / creative tools tend motion-led; finance / medical / serious B2B tend static.

### 9. Refusal list — 3–5 things this brand never does

Mix of:

- **User-stated refusals** — anything they said in "what should it NOT look like".
- **Archetype-derived refusals** — e.g., Sage archetype refuses emojis-as-icons; Lover archetype refuses generic stock photography; Rebel archetype refuses corporate-blue.
- **Tribe-derived refusals** — anti-patterns visible in the look-unlike incumbent.

Aim for 3–5 concrete refusals. Not "no bad design" — "no two-stop blue→purple gradients", "no clip-art-style illustrations", "no body-shaming copy".

---

## Output shape (passed to Phase 3)

A locked object like:

```yaml
trust: high
frequency: daily-seconds
density: content-light
culture: indian-casual
archetype: magician
secondary_archetype: caregiver  # optional, can be empty
look_like: [stitch-fix.com, whering.com, vogue.in]
look_unlike: myntra.com
surface_mix: marketing+app
tempo: mixed
refusals:
  - no stock photos of generic Western models
  - no clinical Pantone-software swatch UI
  - no body-shaming copy
  - no traffic-light approve/reject patterns
```

Do not surface this raw object to the user. Phase 3 turns it into prose.
