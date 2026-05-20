# Phase 4 — Per-page briefs

For each page in SITEMAP.md, write one brief file at `agents/marketing/briefs/<slug>.md`. The brief is the structural skeleton for the page — what the page is *for*, who's reading it, what the story arc is, what sections appear and what each section does.

Briefs do NOT contain final copy. That's Phase 5. Briefs contain intent.

This separation exists because copy without a brief drifts into list-of-features mode; brief without copy stays abstract. The two-pass shape keeps headlines tied to story arc and visual anchors tied to section intent.

---

## Brief shape — every brief has these sections

```markdown
# agents/marketing/briefs/<slug>.md
> Brief for the <page name> page. Locked via marketing-brief on <YYYY-MM-DD>.
> Reads from: agents/marketing/CONTENT.md (features, audiences, testimonials, FAQs).

## Audience state on entry
What does the reader fear or want before they open this page? One paragraph.

## Single intent
One sentence — what this page is for. Verb + object.

## Primary CTA
Verb + object. Match SITEMAP.md row.

## Story arc
The flow this page walks through. Default is the classic five-beat:
1. Claim — the strongest version of what we do.
2. Proof — concrete evidence (screenshot, stat, quote).
3. How — show the mechanic in 3 steps or less.
4. Social proof — who else uses this.
5. Ask — the CTA again, with the lowest possible friction.

Per-page arcs can vary. Pricing skips "how", inserts "what you get per tier".
Comparison pages skip "how", insert "side-by-side breakdown".

## Sections

### Section 1 — <section name>
- **Eyebrow** — kicker text intent (e.g., "category label", or "(none)").
- **Headline intent** — what the headline *claims*. Not the final words.
- **Blurb intent** — what the supporting sentence proves.
- **Visual anchor type** — screenshot / photo / stat / quote / code / illustration / (none).
- **CTA spec** — verb + object, or "(none)".
- **Reads from** — any CONTENT row keys this section pulls.

### Section 2 — …

(repeat per section)
```

Each section gets all six fields. Missing field → "(none)" explicitly, never blank.

---

## Worked example — `briefs/home.md`

```markdown
# agents/marketing/briefs/home.md
> Brief for the Home page. Locked via marketing-brief on 2026-05-21.
> Reads from: agents/marketing/CONTENT.md (features, audiences, testimonials, FAQs).

## Audience state on entry
First-time visitor, arrived from a search like "<category> tool" or a referral.
They have a vague version of the problem we solve — they're losing time on
link analytics or shipping experiments — and they're inside their normal
"evaluate three options in 90 seconds" scan. They will leave fast if the first
fold doesn't make a single, specific claim they recognise.

## Single intent
Convince a new visitor we solve their specific problem, then move them to the
free tier without friction.

## Primary CTA
Start free.

## Story arc
1. Claim — name the problem and our claim in one fold.
2. Proof — one product screenshot showing the claim in action.
3. How — three-step mechanic (set up → use → see results).
4. Features grid — visible breadth, scannable in 8 seconds.
5. Social proof — one testimonial + customer logos.
6. FAQ — top 3 objections.
7. Ask — final CTA fold, mirrored from hero.

## Sections

### Section 1 — Hero
- Eyebrow: (none).
- Headline intent: One-line claim that names the user's win, not our category.
- Blurb intent: One sentence framing the problem we remove. ≤ 18 words.
- Visual anchor type: product screenshot (the main dashboard, using the
  fictional-customer brand locked in MEDIA.md).
- CTA spec: Start free → /signup. Secondary link "See how it works" → in-page anchor.
- Reads from: (none — hero is page-specific).

### Section 2 — Logo strip
- Eyebrow: "Used by".
- Headline intent: (none — the logos are the headline).
- Blurb intent: (none).
- Visual anchor type: customer logos, 5–7 entries.
- CTA spec: (none).
- Reads from: CONTENT.TESTIMONIALS.company (deduped) — or fictional customer + 4 others if no real customers.

### Section 3 — Proof screenshot
- Eyebrow: "Live in 90 seconds".
- Headline intent: Claim restated with a number ("X teams ship 3× faster").
- Blurb intent: Concrete proof — what specifically gets faster, by how much.
- Visual anchor type: full-bleed product screenshot showing the analytics view.
- CTA spec: (none — this is proof, not ask).
- Reads from: (none).

### Section 4 — How it works
- Eyebrow: "How it works".
- Headline intent: Three-word summary of the loop.
- Blurb intent: (none — the steps are the blurb).
- Visual anchor type: three small illustrations or three numbered cards.
- CTA spec: (none).
- Reads from: (none).

### Section 5 — Features grid
- Eyebrow: "Everything you need".
- Headline intent: Claim about breadth, not list of features.
- Blurb intent: (none — the grid is the proof).
- Visual anchor type: 6-card grid, one card per top FEATURES row.
- CTA spec: each card links to its feature page.
- Reads from: CONTENT.FEATURES (top 6 rows by `audiences` overlap with primary audience).

### Section 6 — Testimonial
- Eyebrow: (none).
- Headline intent: The quote itself is the headline.
- Blurb intent: (none).
- Visual anchor type: pull quote + author photo + company logo.
- CTA spec: "Read the full story" → /customers/<slug>.
- Reads from: CONTENT.TESTIMONIALS (highest-impact row tagged `home`).

### Section 7 — FAQ
- Eyebrow: "Common questions".
- Headline intent: (none — questions are headlines).
- Blurb intent: (none).
- Visual anchor type: (none — text only).
- CTA spec: (none).
- Reads from: CONTENT.FAQS rows where `pages` contains `home`.

### Section 8 — Final CTA
- Eyebrow: (none).
- Headline intent: Mirror of hero headline, slightly stronger.
- Blurb intent: One sentence — remove last friction ("free forever, no card").
- Visual anchor type: (none).
- CTA spec: Start free → /signup.
- Reads from: (none).
```

---

## Per-page-type guidance

- **Home** — full 5-beat arc. Wide audience. Headlines aim at the broadest claim.
- **Pricing** — skip "how", insert tier comparison + "what you get" + objection-handling FAQ. The CTA is the same as home (Start free) but the page assumes the visitor is further down funnel.
- **Customers index** — grid of cards, one per case study. Single ask is "read one".
- **Per-customer (case study)** — narrative arc: who they are → what was broken → what changed → what's better now (with a stat). One CTA: Start free.
- **Features index** — scannable grid. No story arc — pure breadth. Each card links to its feature page.
- **Per-feature** — claim → screenshot of that feature → 3 use cases → testimonial tagged to this feature's audience → CTA.
- **vs/<competitor>** — side-by-side table from CONTENT.COMPARISONS + "when to pick us" + "when to pick them" (honesty wins trust here) + CTA.
- **Blog landing** — list view; no story arc.
- **Changelog** — list view; no story arc.
- **About** — narrative: why this exists → who's building → what we believe → CTA (start free or "follow along").
- **Legal pages** — pure body text. No CTA. No marketing voice.

---

## Hard rules

- **One CTA per brief.** Period. Secondary links allowed; secondary CTAs are not.
- **Headlines in the brief are *intent*, not final copy.** Phase 5 writes the final string. If you find yourself writing "Turn clicks into revenue" in the brief, move it to the copy file.
- **Every section declares a visual anchor type.** Even "(none)" is a declaration — it tells Phase 7 not to leave space for one.
- **"Reads from" is required.** Every section either pulls from a CONTENT table (with the table name) or declares "(none — page-specific)". This forces the registry-first discipline.
- **Audience state on entry is concrete.** "First-time visitor from a search" is concrete. "Potential customer" is not.
- **Story arc is named.** Don't write a brief without naming the beats. Sections that don't serve a beat usually shouldn't exist.
- **Banned-words list is not enforced here.** Briefs talk about intent, which sometimes uses words the final copy can't. Phase 5 enforces banned words on the actual copy.
