# Phase 3 — Sitemap

Propose the page list. The user adds, removes, or renames. Output is `brain/marketing/SITEMAP.md` — every other phase iterates over rows from this file.

The sitemap exists because per-page work (briefs, copy, layouts) needs a locked set of targets. Without it, Phase 4 invents pages, Phase 5 misses pages, the nav builds against one list and the footer against another.

---

## Default proposed shape (SaaS)

Start from this template, then prune / extend based on Phase 1 and Phase 2 outputs.

```
home                           — primary entry, broad audience
pricing                        — pricing tiers + FAQ
customers                      — index of case studies
customers/<customer-slug>      — one per real or fictional customer (one or two only at launch)
features                       — index of all FEATURES rows from CONTENT
features/<feature-slug>        — one per row in CONTENT.FEATURES
vs/<competitor-slug>           — one per row in CONTENT.COMPARISONS
blog                           — blog landing
changelog                      — release notes
about                          — team / mission
legal/<legal-slug>             — one per row in CONTENT.LEGAL_PAGES
```

### Pruning rules

- **No `features/<slug>` pages** if a feature is too small to deserve its own page. The features-index page absorbs it. Ask the user per-feature when in doubt.
- **No `vs/<slug>` pages** if Phase 1 confirmed no comparison positioning.
- **No `blog`** if the user said no blog. Often a v2 surface.
- **No `changelog`** if the project doesn't ship visible-to-users releases (internal tools, agency builds).
- **No `customers/<slug>` pages** at launch if there are zero real customers AND the user opted out of fictional case studies. Keep the `customers` index as a "coming soon" stub, or drop entirely.
- **`pricing` is conditional on monetisation** — drop if monetisation is "talk to sales" (and replace with a `contact` or `request-access` page instead).

### Extending rules

Add pages when Phase 1 surfaced them:

- `careers` — if the project is hiring publicly.
- `security` — if Phase 1 mentioned compliance / SOC2 / GDPR as a positioning angle.
- `integrations` — if the product has a meaningful integration story.
- `docs` — if docs live on the marketing domain rather than a separate subdomain.
- `enterprise` — if there's a separate enterprise sales motion.

Never add pages just because they're standard. Each new page must answer "what's the single intent of this page?" — if the answer is vague, drop it.

---

## Per-page row shape

Each row in SITEMAP.md captures the minimum a brief needs to start.

| Field | Description |
|-------|-------------|
| `slug` | URL path. Lowercase, hyphenated. |
| `name` | Display name in nav / breadcrumbs. |
| `intent` | One sentence — what this page does for the user. |
| `primary CTA` | The single action this page asks for. Verb + object. |
| `audience descriptor` | One line — who's reading this page. |
| `brief file` | Path to the brief in `brain/marketing/briefs/`. |

---

## Output file shape — `brain/marketing/SITEMAP.md`

```markdown
# brain/marketing/SITEMAP.md
> Page list for the marketing surface. Every brief, copy file, and layout sketch
> references a row here by slug.
> Locked via marketing-brief on <YYYY-MM-DD>.

## Pages

| slug                         | name                  | intent                                                                | primary CTA           | audience descriptor                  | brief file                          |
|------------------------------|-----------------------|-----------------------------------------------------------------------|-----------------------|--------------------------------------|-------------------------------------|
| /                            | Home                  | Convince a new visitor we solve their problem and get them to sign up.| Start free            | First-time visitor, broad mix.       | briefs/home.md                      |
| /pricing                     | Pricing               | Resolve the "is this affordable" question and surface the free tier.  | Start free            | Mid-funnel visitor evaluating cost.  | briefs/pricing.md                   |
| /customers                   | Customers             | Show who else uses this and what changed for them.                    | Read a case study     | Social-proof seeker.                 | briefs/customers.md                 |
| /customers/<fictional-brand> | <Fictional Brand>     | One concrete story — before / change / result.                        | Start free            | Audience matching this customer.     | briefs/customer-<fictional>.md      |
| /features                    | Features              | Quick-scan grid of every feature with a one-line claim each.          | See <top-feature>     | Visitor researching capabilities.    | briefs/features.md                  |
| /features/analytics          | Real-time analytics   | Sell the analytics feature specifically.                              | Start free            | Founder or growth lead.              | briefs/feature-analytics.md         |
| /vs/bitly                    | vs Bitly              | Win the "we evaluated Bitly" comparison search.                       | Start free            | Active evaluator with a competitor.  | briefs/vs-bitly.md                  |
| /blog                        | Blog                  | Show recent writing; build search and credibility.                    | Read latest post      | Newsletter / referral visitor.       | briefs/blog.md                      |
| /changelog                   | Changelog             | Demonstrate active development; reduce abandonment.                   | Subscribe to updates  | Returning user / evaluator.          | briefs/changelog.md                 |
| /about                       | About                 | Establish who's behind this and why.                                  | Start free            | Trust-checking visitor.              | briefs/about.md                     |
| /legal/privacy               | Privacy Policy        | Legal compliance.                                                     | (none)                | Compliance, auditors, EU users.      | briefs/legal-privacy.md             |
| /legal/terms                 | Terms of Service      | Legal compliance.                                                     | (none)                | Compliance, signing customers.       | briefs/legal-terms.md               |

## Nav menu (top-level)
- Pricing
- Customers
- Features (dropdown — auto-built from CONTENT.FEATURES)
- vs (dropdown — auto-built from CONTENT.COMPARISONS)
- Blog
- Changelog
- (right) → Sign in, Start free

## Footer columns
- Product → Features (dropdown items), Pricing, Changelog
- Customers → Customers index, per-customer pages
- Compare → vs items (auto from CONTENT.COMPARISONS)
- Company → About, Blog
- Legal → all LEGAL_PAGES rows
```

The nav and footer sections are explicit because they're the two surfaces most likely to drift. Locking them in SITEMAP.md gives `build-component` (or the user) a clear reference when implementing the layout shell.

---

## Confirmation gate

Surface the proposed sitemap and ask:

> Sitemap proposal — <N> pages. Add, remove, or rename any? Common edits:
> - Drop `vs/*` if not running comparison pages.
> - Drop `customers/<slug>` pages if no case studies for launch.
> - Add `security`, `integrations`, `careers`, `enterprise` if relevant.
> - Rename anything.
>
> Say "go" to lock, or list the edits.

After confirmation, write `brain/marketing/SITEMAP.md`. Lock and proceed to Phase 4.

---

## Hard rules

- **One intent per page.** If the intent string contains "and" linking two different goals, the page should split into two.
- **One primary CTA per page.** No "Start free OR book a demo" on the same page — pick one. Secondary CTAs allowed in footer / nav, not in the page body.
- **Slugs match conventions** — kebab-case, lowercase, no trailing slash, no double slashes.
- **`brief file` paths must be unique** — no two pages share a brief.
- **Auto-generated dropdowns reference CONTENT** — features dropdown reads `CONTENT.FEATURES`, vs dropdown reads `CONTENT.COMPARISONS`. Never hardcode the list in SITEMAP.md.
- **Sitemap is locked, not iterated.** After Phase 3 confirmation, do not re-edit SITEMAP.md silently in later phases. If a brief reveals a missing page, return to Phase 3, get user confirmation, then proceed.
