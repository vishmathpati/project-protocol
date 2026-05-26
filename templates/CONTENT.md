# agents/marketing/CONTENT.md
> Single source of truth for marketing content.
> Every marketing page reads from this — nav menus, footer columns, feature
> pages, comparison pages, testimonial sections, FAQ sections, legal nav.
> Updated only by user (or `marketing-brief` skill with explicit confirmation).
> Never duplicate this content into copy files — always reference by id/slug.
>
> Rule of thumb: if a name, slug, blurb, audience, or quote appears on more
> than one page, it lives here and pages render it by id. If it only appears
> on one page, it can stay in that page's copy file in `agents/marketing/copy/`.

---

## FEATURES

Every product surface area the marketing site sells. `id` is the stable key
referenced by nav, footer, comparison pages, and per-feature pages. `icon`
must match a Lucide icon name. `blurb` is the one-liner used in nav and
feature grids — keep it ≤ 120 chars. `audiences` is a comma-separated list
of audience ids (see AUDIENCES below).

| id | name | icon (Lucide) | blurb (≤120 chars) | page_slug | audiences |
|----|------|---------------|---------------------|-----------|-----------|
<!-- EXAMPLE — DELETE BEFORE USE -->
| short-links | Short Links | Link | Create branded short links with custom domains, QR codes, and deep links. | /links | marketers, developers |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| analytics   | Analytics   | BarChart3 | Real-time conversion analytics with full attribution. | /analytics | marketers |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| partners    | Partners    | Users  | Build embedded affiliate programs that scale with you. | /partners | marketers, product-teams |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| api         | API         | Code2  | First-class developer API with SDKs in 6 languages. | /api | developers |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| qr-codes    | QR Codes    | QrCode | Branded QR codes with logos, colors, and tracking. | /qr | marketers |
<!-- /EXAMPLE -->

---

## AUDIENCES

Who the marketing site is talking to. Used to filter nav, set the page
hero, and shape per-feature copy emphasis. Every feature should map to at
least one audience; every audience should anchor at least one comparison
page or proof point.

| id | name | descriptor | fear (one sentence) | want (one sentence) |
|----|------|------------|----------------------|----------------------|
<!-- EXAMPLE — DELETE BEFORE USE -->
| marketers       | Marketing teams | Design-conscious modern SaaS marketers | Vanity metrics that don't tie to revenue. | Attribution they can trust. |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| developers      | Developers | API-first builders at high-growth companies | Bloated link APIs with hidden quotas. | Programmatic short-link infra they can drop into a CLI. |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| product-teams   | Product teams | Growth + product folks running referral / affiliate motions | Building partner programs in-house with brittle scripts. | Embedded program infra with revenue share built in. |
<!-- /EXAMPLE -->

---

## COMPARISONS

Direct head-to-head pages. Each row becomes one `/compare/<slug>` page.
Tone: honest, never bash competitors — list real strengths on both sides.
`our_strength` and `their_strength` are the one-line summaries used in the
hero comparison card; the page itself expands each into a section.

| vs_competitor | our_strength | their_strength | page_slug |
|---------------|--------------|----------------|-----------|
<!-- EXAMPLE — DELETE BEFORE USE -->
| Bitly         | Modern API + conversion tracking. | Brand recognition, long history. | /compare/bitly |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| Rebrandly     | All-in-one with partner programs. | Custom domain volume at very large scale. | /compare/rebrandly |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| TinyURL       | Branded domains + analytics. | Free forever for casual use. | /compare/tinyurl |
<!-- /EXAMPLE -->

---

## TESTIMONIALS

Customer quotes. `customer` is the person's name, `role` + `company` make
the attribution line. `quote` is verbatim — never paraphrased. `photo_url`
is the path under `agents/marketing/media/` (managed by `marketing-brief`
media manifest, never a remote URL hot-linked from a competitor).

| customer | role | company | quote | photo_url |
|----------|------|---------|-------|-----------|
<!-- EXAMPLE — DELETE BEFORE USE -->
| Maya Chen | Head of Growth | Vercel-ish startup | "We replaced three tools with this. Attribution is finally honest." | /media/testimonials/maya-chen.jpg |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| Theo Patel | Staff Engineer | Series-B fintech | "The API is what Bitly's should have been ten years ago." | /media/testimonials/theo-patel.jpg |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| Lena Ström | VP Marketing | DTC brand | "Our affiliate program went from spreadsheet to revenue line in a week." | /media/testimonials/lena-strom.jpg |
<!-- /EXAMPLE -->

---

## FAQS

Questions used in per-page FAQ sections and the global `/faq` page.
`page_slug` is where this FAQ primarily lives. Same question can appear
on multiple pages — duplicate the row with different `page_slug` values
rather than splitting the answer.

| question | answer | page_slug |
|----------|--------|-----------|
<!-- EXAMPLE — DELETE BEFORE USE -->
| Do you offer a free plan? | Yes — 1,000 clicks/month, one custom domain, full analytics. No card required. | /pricing |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| Can I use my own domain? | Yes, on every paid plan. Connect via DNS in under 60 seconds. | /pricing |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| Is the API rate-limited? | 1,000 req/min on Pro, 10,000 req/min on Business. Hard quotas only on Free. | /api |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| How does conversion tracking work? | We pixel-track clicks then match against your analytics provider via webhook or SDK. | /analytics |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| Do you support SAML SSO? | Yes, on Business and Enterprise. Okta, Google Workspace, Microsoft Entra. | /pricing |
<!-- /EXAMPLE -->

---

## LEGAL_PAGES

Footer legal nav. Each row renders one `/<slug>` page sourced from
`agents/marketing/copy/legal/<slug>.md`. `last_updated` shows in the page
footer and is the only field humans hand-edit between releases.

| slug | title | last_updated |
|------|-------|--------------|
<!-- EXAMPLE — DELETE BEFORE USE -->
| /terms       | Terms of Service     | 2026-04-15 |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| /privacy     | Privacy Policy       | 2026-04-15 |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| /dpa         | Data Processing Addendum | 2026-04-15 |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| /security    | Security             | 2026-03-01 |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| /cookies     | Cookie Policy        | 2026-04-15 |
<!-- /EXAMPLE -->
<!-- EXAMPLE — DELETE BEFORE USE -->
| /acceptable-use | Acceptable Use Policy | 2026-04-15 |
<!-- /EXAMPLE -->

---

## How pages consume this file

- **Top nav** — reads `FEATURES` (filter by `audiences` if the nav is
  audience-split) for the product menu; reads `COMPARISONS` for the
  "compare" submenu.
- **Footer** — reads `FEATURES` for the Product column, `LEGAL_PAGES`
  for the Legal column, `COMPARISONS` for the Compare column.
- **Per-feature page** (`/links`, `/analytics`, …) — looks itself up in
  `FEATURES` by `page_slug`, pulls `audiences` to set the hero variant,
  reads matching `TESTIMONIALS` + `FAQS` by feature association.
- **Comparison pages** — render one row of `COMPARISONS`.
- **Global FAQ page** — renders all of `FAQS`, grouped by `page_slug`.
- **Legal pages** — render `LEGAL_PAGES` row + the matching markdown file
  in `agents/marketing/copy/legal/`.

## Editing rules

1. **Never delete a row that's referenced by a live page.** Mark it
   stale, replace, or migrate the page first.
2. **`id` and `slug` fields are immutable** once a page is live — they
   become URLs and cross-references. Rename only via a migration.
3. **Audiences must exist in the AUDIENCES table** before being used in
   a FEATURES row — `marketing-brief` enforces this.
4. **Testimonial quotes are verbatim.** If you need to shorten one, get
   the customer's written approval and log it in `agents/DECISIONS.md`.
