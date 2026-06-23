# Phase 5 — Per-page copy

For each page in SITEMAP.md, write the final copy file at `brain/marketing/copy/<slug>.md`. Every headline, subhead, button label, section copy, footer text — finalised, ready to paste into JSX.

Phase 4 produced the brief (intent). Phase 5 turns intent into strings. The two-pass split exists because writing copy and structuring intent at the same time always loses one of them.

---

## What goes in a copy file

Every visible string the page renders, organised by section, in the same order as the brief.

```markdown
# brain/marketing/copy/<slug>.md
> Final copy for the <page name> page. Locked via marketing-brief on <YYYY-MM-DD>.
> Reads from: brain/marketing/CONTENT.md (features, testimonials, FAQs).
> Reads brief: brain/marketing/briefs/<slug>.md.

## Section 1 — <section name>
- Eyebrow: "<final string or (none)>"
- Headline: "<final string>"
- Subhead: "<final string>"
- CTA primary: "<button label>" → <link>
- CTA secondary: "<link label>" → <link>
- Body copy:
  > <paragraph>

## Section 2 — …
```

Strings only. No commentary inside the copy. Commentary belongs in the brief.

---

## Reading from CONTENT.md — never duplicate

Copy files MUST NOT inline feature names, customer names, or FAQ answers. They reference CONTENT rows by `key`.

```markdown
## Section 5 — Features grid
- Eyebrow: "Everything you need."
- Headline: "Six features. One ship."
- Subhead: (none — the grid is the proof.)
- Body copy: (none — cards render from CONTENT.FEATURES, top 6 by audience overlap.)
- Per-card render template:
  - icon: from CONTENT.FEATURES.<key>.icon
  - title: from CONTENT.FEATURES.<key>.name
  - blurb: from CONTENT.FEATURES.<key>.blurb
  - link: from CONTENT.FEATURES.<key>.page_slug
```

When `build-component` implements this section, it iterates over CONTENT rows. The copy file does not name a single feature — if it did, the file would drift from CONTENT and the bug would be invisible until a comparison failed.

Same rule for testimonials, FAQs, audiences, comparisons.

---

## Headline rule — every headline is a claim

Description headlines are banned. Claim headlines are required.

| ❌ Description (banned)                          | ✅ Claim (required)                            |
|--------------------------------------------------|------------------------------------------------|
| "Our analytics platform"                         | "See what's working before lunch."             |
| "A modern link shortener"                        | "Short links that don't outlive your brand."   |
| "Pricing for every team"                         | "Start free. Pay nothing until it pays back."  |
| "About us"                                       | "We build for the team of one."                |
| "Real-time analytics"                            | "Watch the conversion happen."                 |

Test for a headline:
- Could the headline appear on three competitors' sites unchanged? → It's a description. Rewrite.
- Does it claim a user outcome, a contrarian stance, or a specific number? → It's a claim. Keep.

Exceptions: legal pages, list pages with no fold (blog landing, changelog), section eyebrows. Eyebrows are labels, not claims.

---

## Banned-words enforcement

Read `brain/FUNDAMENTALS.md` § banned words before writing. Scan every line of every copy file against the list. Common entries — these illustrate the pattern; the live list lives in FUNDAMENTALS.md:

- "seamless", "seamlessly"
- "robust"
- "leverage" (as a verb)
- "empower", "empowering"
- "unleash", "unlock the power of"
- "revolutionary", "revolutionising"
- "synergy"
- "best-in-class"
- "world-class"
- "enterprise-grade"
- "AI-powered" (unless the page is specifically about an AI feature and the claim is concrete)
- "delight", "delightful" (as a marketing adjective)
- "elevate"
- "transform" (as a verb of effort, not outcome)

When a banned word appears: rewrite. Don't apologise — replace it with a concrete claim or remove the sentence entirely. "Seamless integration" almost always means "we don't want to say what actually happens."

Also banned across the board:

- **Em-dash overuse** — Allowed sparingly. Two em-dashes in one section is a flag. Use periods.
- **Three-adjective stacks** — "fast, simple, powerful" reads as AI slop. Pick one adjective and earn it.
- **Hyphenated buzz-compounds** — "next-generation", "game-changing", "purpose-built". Cut.
- **Trailing exclamation marks** outside legal CTAs.

---

## Section copy rules

### Hero
- Headline: 5–10 words. Claim, not description.
- Subhead: 12–22 words. One sentence. Removes one objection or one ambiguity.
- CTA button: 2–4 words. Verb + object. "Start free", "Book a demo", "See pricing".
- No secondary "Learn more" link. Either name the secondary action, or drop it.

### Body sections
- Eyebrow: 1–3 words. Category label, not a sentence.
- Headline: claim about the section's specific point. Same 5–10 word target.
- Subhead: optional. If present, ≤ 22 words.
- Body paragraph: ≤ 60 words. One idea.

### Pricing
- Tier name: 1 word ideally ("Free", "Pro", "Business"). Avoid "Starter", "Enterprise" unless they map to a real distinction.
- Price line: number + cadence. Nothing else.
- Tier description: one sentence on who this is for, not what's in it.
- Feature list per tier: pulled from CONTENT.FEATURES with per-tier flag (TBD per project — note in CONTENT).
- CTA per tier: same verb across tiers if possible. "Start free" / "Start free" / "Talk to sales" is fine; "Get started" / "Sign up now" / "Begin your journey" is not.

### FAQ
- Question: as the user would type it into search.
- Answer: pulled from CONTENT.FAQS, ≤ 35 words. Direct. No hedging.

---

## Worked example — `copy/home.md`

```markdown
# brain/marketing/copy/home.md
> Final copy for the Home page. Locked via marketing-brief on 2026-05-21.
> Reads from: brain/marketing/CONTENT.md.
> Reads brief: brain/marketing/briefs/home.md.

## Section 1 — Hero
- Eyebrow: (none)
- Headline: "See what's working before lunch."
- Subhead: "Real-time analytics for short links and experiments — without the dashboard tax."
- CTA primary: "Start free" → /signup
- CTA secondary: "See how it works" → #how
- Body copy: (none)

## Section 2 — Logo strip
- Eyebrow: "Used by teams at"
- Headline: (none — logos are the headline)
- Body copy: (none — renders from CONTENT.TESTIMONIALS.company deduped)

## Section 3 — Proof screenshot
- Eyebrow: "Live in 90 seconds"
- Headline: "From paste to insight without a setup call."
- Subhead: "Drop a link in. Numbers move within the minute."
- CTA primary: (none)
- Body copy: (none — screenshot is the proof)

## Section 4 — How it works
- Eyebrow: "How it works"
- Headline: "Paste. Share. Read the room."
- Subhead: (none)
- Body copy: (none — three numbered steps render below)
- Per-step (3 steps):
  - Step 1 title: "Paste a link."
  - Step 1 blurb: "Or import a hundred. We branded them on the way in."
  - Step 2 title: "Share it anywhere."
  - Step 2 blurb: "Email, ads, in-product. Same URL, same brand, every channel."
  - Step 3 title: "Read the room."
  - Step 3 blurb: "Live clicks, conversions, and who's actually buying."

## Section 5 — Features grid
- Eyebrow: "Everything you need"
- Headline: "Six features. One ship."
- Subhead: (none)
- Body copy: (none — renders from CONTENT.FEATURES top 6 by audience overlap)

## Section 6 — Testimonial
- Eyebrow: (none)
- Headline: (none — quote is the headline)
- Body copy: (renders from CONTENT.TESTIMONIALS, key=t-001 tagged for home)
- CTA secondary: "Read the full story" → /customers/<from CONTENT.TESTIMONIALS.t-001.company slug>

## Section 7 — FAQ
- Eyebrow: "Common questions"
- Headline: (none)
- Body copy: (renders from CONTENT.FAQS where pages contains 'home')

## Section 8 — Final CTA
- Eyebrow: (none)
- Headline: "Stop guessing what's working."
- Subhead: "Free forever for the first thousand clicks. No card."
- CTA primary: "Start free" → /signup
- Body copy: (none)
```

---

## Hard rules

- **Every visible string is in the copy file.** Buttons, eyebrows, footer links — all of them.
- **No string is duplicated across copy files.** Shared facts live in CONTENT.md and are referenced.
- **Every headline is a claim.** Test against the three-competitor swap. If it could appear on three sites, rewrite.
- **Banned-words scan runs after writing.** Re-grep the final file against FUNDAMENTALS.md banned list. Each hit is a fix.
- **One voice across all pages.** Same tense, same person, same energy. If home is in second person, pricing is in second person.
- **No "Learn more" link without a specific noun.** Either "See pricing" or no secondary link.
- **Legal pages skip the marketing voice.** Plain. Boring. Accurate. No claims.
