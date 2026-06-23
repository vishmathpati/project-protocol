# Phase 2 — Content registry

Write `brain/marketing/CONTENT.md`. This file is the single source of truth for every marketing fact that appears in more than one place: features, audiences, comparisons, testimonials, FAQs, legal pages.

Every later marketing file — sitemap, briefs, copy, layouts — reads from this. The nav menu, the footer columns, the feature-pages index, the testimonial blocks all resolve their content by referencing CONTENT rows, never by hardcoding strings.

---

## Why a single registry

Without it, drift is inevitable. Pages diverge:

- The nav lists 6 features. The footer lists 5. The features-index page lists 7.
- The home page positions against Competitor X. The comparison-pages folder has pages for Y and Z but not X.
- The testimonial in the hero says "Acme Inc". The testimonial on the pricing page says "Demo Corp".
- One FAQ on the home page says pricing starts at $19. The pricing page says $29.

The registry forces every shared fact to live in exactly one place. Components reference it. If a feature is renamed, one row in CONTENT.md changes — nav, footer, feature pages, blurbs all pick it up.

---

## Detecting features from existing code

Before writing CONTENT.md, scan the codebase to confirm the feature list from Phase 1 is complete. Use a `Task` sub-agent at fast tier:

1. **Glob app routes:**
   - Next.js: `app/**/page.tsx`, `pages/**/*.tsx`, excluding `app/(marketing)/**`.
   - SvelteKit / Astro / Remix: equivalent route patterns.
   - Each route name is a candidate feature.

2. **Read top-level page components** for feature-name hints:
   - Page titles, `<h1>` strings, route names.
   - Recurring component names (`<Dashboard>`, `<Editor>`, `<Sharing>`, `<Inbox>`).

3. **Read `brain/ROADMAP.md`** locked features list.

4. **Read `brain/docs/INDEX.md`** feature map.

Merge the three sources. Surface any deltas to the user:

```
Features I see in code that aren't in ROADMAP:
- <feature X>  (found at app/x/page.tsx)
- <feature Y>  (found at components/blocks/Y.tsx, used in 3 places)

Features in ROADMAP that I don't see in code:
- <feature Z>  (marked "in-flight" in ROADMAP — skip for now?)

Confirm the final feature list before I write CONTENT.md.
```

After confirmation, this is the FEATURES seed.

---

## Copy the canonical template, then patch detected values

The shape of `brain/marketing/CONTENT.md` is fixed — the plugin ships a canonical template at `templates/CONTENT.md` (sections: FEATURES, AUDIENCES, COMPARISONS, TESTIMONIALS, FAQS, LEGAL_PAGES, plus the "How pages consume this file" and "Editing rules" appendices). Phase 2 fills the placeholders, it does not invent the shape.

Copy the template first:

```bash
mkdir -p brain/marketing
cp "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/CONTENT.md" brain/marketing/CONTENT.md
```

If neither `CODEX_PLUGIN_ROOT` nor `CLAUDE_PLUGIN_ROOT` is set (some agents don't expose the env var): use the Read tool to fetch the template content from the plugin install path, then Write it to `brain/marketing/CONTENT.md`.

Once the copy is in place, patch the detected/elicited values into the existing tables. The template ships with realistic example rows (short-links / analytics / partners, marketers / developers / product-teams, etc.) — **delete those example rows** and replace with rows derived from the FEATURES seed above plus the user's answers in Phase 1.

What to patch per table:

- **FEATURES** — one row per confirmed feature from the seed. `key` is the slug used by the code; `name` is the display label; `icon` must be a Lucide name (the template uses Pascal-case like `BarChart3` — match that style); `blurb` ≤ 120 chars per the template header; `page_slug` is the route; `audiences` is a comma-separated list of `key`s from the AUDIENCES table.
- **AUDIENCES** — replace example rows with the audiences elicited in Phase 1. Each row needs `id`, `name`, `descriptor`, `fear`, `want` (single-sentence each).
- **COMPARISONS** — drop the entire table if Phase 1 confirmed no comparison pages. Otherwise one row per competitor with `vs_competitor`, `our_strength`, `their_strength`, `page_slug`.
- **TESTIMONIALS** — if Phase 1 said "real quotes available", fill with real attributions. Otherwise use the locked fictional-customer brand for `company` and plausible-but-fake names for `customer`. `quote` is verbatim.
- **FAQS** — one row per question. Each row binds to a `page_slug`; same question across pages = duplicate the row with a different `page_slug`.
- **LEGAL_PAGES** — keep the universal rows (`/terms`, `/privacy`, …) if the project will need them. Set `last_updated` to `[VERIFY]` so `audit` surfaces them later. Drop rows the project explicitly doesn't have.

Hard rules for the patch:

- Do not delete the file header (the `> Single source of truth …` blockquote) or the "How pages consume this file" / "Editing rules" appendices. They're contract, not example.
- Do not invent features that don't trace to code or `brain/ROADMAP.md`.
- Mark any auto-detected row that wasn't explicitly confirmed by the user with `[VERIFY]` in one of its cells.
- Banned-words list applies to blurbs and FAQ answers — scan against `brain/FUNDAMENTALS.md` § banned words before writing.

---

## Table shapes (reference)

Below is the canonical shape each section in the template uses. Use these when patching rows so you don't drift from the template's column order.

### FEATURES

```markdown
## FEATURES

| key            | name                  | icon         | blurb (≤ 12 words)                                       | page slug          | audiences         |
|----------------|-----------------------|--------------|----------------------------------------------------------|--------------------|-------------------|
| analytics      | Real-time analytics   | line-chart   | See traffic, conversions, and drop-off as they happen.   | /features/analytics| founders, growth  |
| short-links    | Short links           | link         | Branded short URLs with QR codes and click tracking.     | /features/links    | growth, agencies  |
| ab-tests       | A/B tests             | sliders      | Run experiments without code. Ship the winner in a click.| /features/ab-tests | growth            |
```

Rules:
- **`key`** is a stable slug. Code references this key, not the display name.
- **`name`** is the display string. Rename without breaking references.
- **`icon`** is a lucide-style name. Drives the icon system. Never an emoji.
- **`blurb`** is 12 words max. Used in nav dropdowns, feature-index cards, footer.
- **`page slug`** is the route the per-feature page lives at.
- **`audiences`** is a comma-separated list of `key`s from the AUDIENCES table.

### AUDIENCES

```markdown
## AUDIENCES

| key       | name             | descriptor                              | top-of-mind pain                              | primary CTA         |
|-----------|------------------|-----------------------------------------|-----------------------------------------------|---------------------|
| founders  | Solo founders    | Building, marketing, and shipping alone.| "I can't tell what's working."                | Start free          |
| growth    | Growth teams     | 3–10 person growth squads at Series A+. | "I waste a week per experiment on tooling."   | Book a 20-min demo  |
| agencies  | Agencies         | Marketing agencies running ~10 clients. | "I'm rebuilding the same dashboard per client."| See agency pricing |
```

### COMPARISONS

```markdown
## COMPARISONS

| key          | competitor name   | page slug              | we win on                          | they win on                       |
|--------------|-------------------|------------------------|------------------------------------|-----------------------------------|
| vs-bitly     | Bitly             | /vs/bitly              | Real-time analytics, A/B tests     | Brand recognition, enterprise SSO |
| vs-rebrandly | Rebrandly         | /vs/rebrandly          | Modern UI, API, free tier          | Custom-domain breadth             |
```

Skip this table entirely if Phase 1 confirmed no comparison pages.

### TESTIMONIALS

```markdown
## TESTIMONIALS

| key   | quote                                                          | author        | role           | company         | audience tag |
|-------|----------------------------------------------------------------|---------------|----------------|-----------------|--------------|
| t-001 | "Cut our analytics setup from a week to one afternoon."        | Maya Iyer     | Head of Growth | <fictional 1>   | growth       |
| t-002 | "Finally a dashboard I can give to a client without blushing." | Daniel Park   | Founder        | <fictional 2>   | agencies     |
```

If Phase 1 said "real customer quotes available", populate with real names and real companies. Otherwise use the fictional-customer brand (locked in Phase 6) for `company` and plausible-but-fake names for `author`.

### FAQS

```markdown
## FAQS

| key   | question                                       | answer (≤ 35 words)                                                          | pages              |
|-------|------------------------------------------------|------------------------------------------------------------------------------|--------------------|
| f-001 | How is this different from Google Analytics?   | We focus on links and conversions, not full-site behavioural analytics.      | home, vs-bitly     |
| f-002 | Do you have a free plan?                       | Yes — up to 1,000 clicks per month, no card required.                        | home, pricing      |
| f-003 | Can I use a custom domain?                     | Yes, on every paid plan. Free plan uses our subdomain.                       | pricing, features  |
```

`pages` is the list of page slugs that surface this FAQ.

### LEGAL_PAGES

```markdown
## LEGAL_PAGES

| key      | name              | slug            | owner       | last reviewed |
|----------|-------------------|-----------------|-------------|---------------|
| privacy  | Privacy Policy    | /legal/privacy  | Vish        | 2026-04-01    |
| terms    | Terms of Service  | /legal/terms    | Vish        | 2026-04-01    |
| dpa      | DPA               | /legal/dpa      | Vish        | 2026-04-01    |
```

If the project doesn't have legal pages yet, write the rows with `last reviewed: [VERIFY]` so they show up in `audit` later.

---

## File header

CONTENT.md opens with a short header so a human opening the file knows what it is:

```markdown
# brain/marketing/CONTENT.md
> Single source of truth for every shared marketing fact.
> Locked via marketing-brief on <YYYY-MM-DD>.
> All marketing components must read from this file. Never hardcode a feature
> name, customer, or FAQ entry in a copy file or component.

## How to use
- Add a new feature → one new row in FEATURES.
- Rename a feature → edit `name`, leave `key` alone.
- Add a competitor → one new row in COMPARISONS, then generate a new
  comparison page in Phase 3+.
- Real customer signs a testimonial → replace the matching row's `company`
  with the real brand (and drop the fictional-customer reference).
```

---

## Merging into an existing CONTENT.md

If `brain/marketing/CONTENT.md` already exists:

1. Read it. Parse each table.
2. Surface every existing row to the user one table at a time:
   > FEATURES — existing rows (N). Keep all? Drop any? Add new ones I detected?
3. Default action is **merge** — keep all existing rows, add detected-but-missing rows. Never silently drop a row.
4. Conflicts (same `key`, different `name` or `blurb`) — surface side-by-side and ask which wins. Default is "keep existing".

---

## Hard rules

- **One row per fact.** Two rows for the same feature is a bug.
- **`key` is stable.** Code and other marketing files reference `key`. Renaming `key` breaks references.
- **Blurbs cap at 12 words.** Headlines cap at 8. Enforce on write.
- **No emoji icons.** Icon column names a lucide-style symbol or "none". `audit` and `design-check` will flag emoji icons downstream.
- **No invented features.** Every FEATURES row must trace to code or ROADMAP.
- **No invented testimonials with real-looking author + real-looking company together.** Either both are clearly fictional (using the locked fictional-customer brand from Phase 6) or both are real with the customer's permission.
- **Banned-words list applies** to blurbs and FAQ answers. Scan against `brain/FUNDAMENTALS.md` § banned words before writing.
