# Phase 6 — Media manifest

Write `brain/marketing/MEDIA.md`. Per section in each page, declare the visual-anchor type and what it shows. This file is the spec sheet for whoever (or whatever) produces the actual assets later.

This phase also locks the **fictional-customer brand** — the single fake brand every product screenshot uses for visual coherence. Asked once, used everywhere.

MEDIA.md is a manifest, not a render. This skill does not generate images. It declares what images need to exist.

---

## The fictional-customer brand — asked once

The dub.co pattern: every product screenshot on dub.co shows "acme" as the example brand. One brand, used everywhere, creates the illusion of a single coherent customer. Three different fake brands ("Acme Inc", "Demo Corp", "Test Co") across three screenshots read as broken.

Ask the user once, before writing MEDIA.md:

> One question before I build the media manifest:
>
> Every product screenshot on the marketing site needs to show a brand inside
> the dashboard / inside the short links / in the testimonial company column.
> If we use the same fictional brand everywhere, the screenshots read as one
> coherent customer.
>
> Pick one (or propose your own):
>   - acme.link
>   - madeup.studio
>   - everyday.co
>   - linkbase.io
>   - <your own — give me a brand name + a domain>
>
> Avoid: anything that resembles a real competitor.

Lock the chosen name + domain at the top of MEDIA.md. Every screenshot, testimonial company field, and example URL in copy uses this brand.

If a real customer testimonial exists (from Phase 1 intake), the real customer is used for *that* testimonial. The fictional brand fills every other slot.

---

## File header — `brain/marketing/MEDIA.md`

```markdown
# brain/marketing/MEDIA.md
> Visual-anchor manifest for the marketing surface.
> Locked via marketing-brief on <YYYY-MM-DD>.
> This file is a SPEC — not the assets themselves. Use it to brief whoever
> produces the screenshots, photos, illustrations, and stat cards.

## Fictional customer (locked)
- Brand name: <e.g., Acme Studio>
- Domain: <e.g., acme.link>
- Used in: every product screenshot, every testimonial unless explicitly real,
  every example URL in copy, every default-state placeholder.

## Real customers (if any)
- <Real Customer 1> — used in <which testimonial / case study>.

## Style notes
- Screenshots are taken from the production app at <viewport width>, dark mode if
  the project's primary theme is dark, light otherwise.
- Photos avoid stock-photo aesthetic. Reference: <Phase 1 BRAND.md tribe>.
- Illustrations follow the BRAND.md direction. No emoji.
- Stats are real where possible. Fictional stats are flagged with [VERIFY].
```

---

## Per-page section table

For every section in every page brief, MEDIA.md adds one row.

```markdown
## Home

| section | anchor type   | shows                                                                 | dimensions    | notes                                  |
|---------|---------------|-----------------------------------------------------------------------|---------------|----------------------------------------|
| Hero    | screenshot    | Analytics dashboard, fictional brand <acme.link>, 1 active campaign.  | 1440 × 900    | Real product. Dark mode. No fake data. |
| Logos   | logo strip    | 6 logos. Fictional customer + 5 plausibly-real names.                 | 120 × 40 each | Greyscale, low opacity.                |
| Proof   | screenshot    | A/B test results pane, fictional brand, two variants 30%/70%.         | 1280 × 720    | Numbers from staging, not invented.    |
| How     | illustration  | Three numbered illustrations: link, signal, dashboard.                | 240 × 240 each| Monoline, brand-accent-color.          |
| Features| icon grid     | 6 icons from CONTENT.FEATURES.icon column.                            | 32 × 32 each  | lucide-react, stroke 1.5.              |
| Testim. | photo + logo  | One author photo + fictional-brand logo + pulled quote.               | 80 × 80 photo | Photo: real headshot or illustration.  |
| FAQ     | (none)        | (text only)                                                           | —             | —                                      |
| Final   | (none)        | (text only)                                                           | —             | —                                      |
```

Repeat per page. Pages with no visual anchors (legal pages, changelog list view) get a short note: *"no media — body text only."*

---

## Anchor types — the full set

Six types. Use exactly one per section, or "(none)".

1. **`screenshot`** — A real product screenshot. Must use the fictional-customer brand for data. Numbers should be plausible (not "1,000,000 clicks" on a brand-new product).
2. **`photo`** — A real or near-real photograph. Author headshots, customer-team photos. Never generic stock.
3. **`stat`** — A big number with a one-line label. ("3.2× higher conversion" / "From 4 hours to 8 minutes"). Source the number — fictional ones are flagged `[VERIFY]`.
4. **`pull quote`** — A testimonial pulled from CONTENT.TESTIMONIALS, rendered large. Often paired with a photo + logo.
5. **`code block`** — A code snippet, syntax-highlighted. Used for developer-facing features. Real code, not pseudocode.
6. **`illustration`** — Monoline or flat-style illustration. Brand-accent colour. No 3D, no glassmorphism, no AI-generic shapes.

Compositional types are also allowed:

- **`logo strip`** — row of customer logos. Greyscale.
- **`icon grid`** — features grid. Pulls icons from CONTENT.FEATURES.icon.
- **`comparison table`** — side-by-side rows. Pulls from CONTENT.COMPARISONS.

---

## What MEDIA.md does NOT contain

- **No actual image files.** This is a spec. The assets are produced separately (by the user, a designer, or a follow-up tool that reads this manifest).
- **No file paths to images.** Once assets exist, their paths live in the component, not in MEDIA.md. MEDIA.md is the brief, not the index.
- **No invented numbers passed off as real.** If a stat is fictional, flag `[VERIFY]`.
- **No emoji as icons.** Banned across the project (`brain/FUNDAMENTALS.md`, `brain/DESIGN.md` DO NOT section).

---

## Worked example — final MEDIA.md shape (excerpt)

```markdown
# brain/marketing/MEDIA.md
> Visual-anchor manifest. Locked 2026-05-21.

## Fictional customer (locked)
- Brand name: Acme Studio
- Domain: acme.link
- Tagline (for screenshots if a tagline appears in-product): "Tiny tools, big launches."

## Style notes
- Screenshots: production app, light mode, 1440 viewport. Real data from a staging tenant
  populated with the Acme Studio fictional brand.
- Photos: real headshots from team or pexels. No AI photos. No stock business handshakes.
- Illustrations: monoline, single accent colour (BRAND.md terracotta). No gradients.
- Stats: real where possible. Fictional stats flagged [VERIFY].

## Home

| section  | anchor       | shows                                                  | dimensions   | notes                |
|----------|--------------|--------------------------------------------------------|--------------|----------------------|
| hero     | screenshot   | Analytics dashboard, acme.link tenant, 1 live campaign | 1440×900     | Light mode           |
| logos    | logo strip   | Acme Studio + 5 plausible brands                       | 120×40 each  | Greyscale            |
| proof    | screenshot   | A/B test result, 2 variants, 30%/70% split             | 1280×720     | Staging numbers      |
| how      | illustration | 3 monoline scenes: paste, share, read                  | 240×240 each | Terracotta accent    |
| features | icon grid    | 6 icons from CONTENT.FEATURES                          | 32×32 each   | lucide, stroke 1.5   |
| testim.  | quote+photo  | t-001 testimonial, author photo, Acme Studio logo      | 80×80 photo  | Real photo if avail  |
| faq      | (none)       | text                                                   | —            | —                    |
| final    | (none)       | text                                                   | —            | —                    |

## Pricing

| section    | anchor       | shows                                              | dimensions | notes                  |
|------------|--------------|----------------------------------------------------|------------|------------------------|
| hero       | (none)       | text                                               | —          | Pricing pages don't open with a screenshot — opens with the tier table |
| tier table | comparison   | 3 tiers from CONTENT pricing data                  | —          | Reads from CONTENT     |
| testim.    | pull quote   | Different testimonial than home — tagged 'pricing' | —          | From CONTENT           |
| faq        | (none)       | text — pricing FAQs from CONTENT                   | —          | —                      |

(… one block per page in SITEMAP.md …)
```

---

## Hard rules

- **Fictional customer is asked once.** Locked at top of MEDIA.md. Reused everywhere. Never two fictional brands on the same site.
- **One anchor type per section.** No "screenshot AND illustration" in the same block.
- **`(none)` is a real declaration**, not a missing field. It tells Phase 7 not to leave space for media.
- **Screenshots use real product UI.** No mockups, no Figma screenshots passing as the real app. The marketing surface that lies about the product loses trust fast.
- **No emoji-as-icon.** Use the BRAND.md icon system (lucide or whichever the project picked).
- **Numbers without sources are `[VERIFY]`.** `project-audit` will surface every unflagged number for spot-check.
- **Real customer trumps fictional.** If a real customer signed a testimonial, that testimonial uses the real company. Fictional fills only the unfilled slots.
- **This file does not generate images.** It briefs them.
