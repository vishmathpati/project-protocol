# Sub-mode — Marketing page

Fires when the page slug lands under `STRUCTURE.md`'s `marketing` / `landing` / `web` surface, or when the user's wording matches marketing intent (homepage, pricing, features, customers, about, comparisons, blog landing, changelog landing, legal pages).

Same 6 phases as the base skill — this doc captures the deltas.

## Inputs read in Phase 1

The full `agents/marketing/` canon — non-optional:

- `SITEMAP.md` row for this slug
- `briefs/<slug>.md`
- `copy/<slug>.md`
- `layouts/<slug>.md`
- `MEDIA.md` (sections matching this slug)
- `CONTENT.md` (rows referenced by this page)

Plus `BRAND.md` (archetype, tribe, refusal list, tempo) and `DESIGN.md` Overview.

If any of these are missing → halt. Marketing pages cannot be built ad-hoc without `marketing-brief` having run.

## Phase 2 emphasis — persuasion rhythm

Marketing pages tell a story: claim → trust → how → surface → moment(s) → social proof → answer → ask. The rhythm tags from the base Phase 2 doc (calm/loud) carry extra weight here. A marketing page where every section is loud reads as a sales letter; one where every section is calm reads as a manifesto. Alternate intentionally.

The `tempo` axis from `BRAND.md` is the dial:
- `tempo: slow / editorial` — more calm sections, more whitespace, longer reads per section, fewer anchors per section, no scroll-linked motion.
- `tempo: medium / pragmatic` — default arc; loud-calm alternation; one or two interaction beats per page.
- `tempo: fast / kinetic` — more loud sections, denser grids, scroll-linked reveals on moment sections, more motion-as-affordance.

## Phase 4 emphasis — MEDIA.md is load-bearing

`MEDIA.md` was the manifest that `marketing-brief` produced. Cross-reference every section's visual against it. Surface any deltas explicitly — *"MEDIA.md says §5 should be a portrait mockup but I think a landscape screenshot makes more sense — pushing back on the manifest"*. Do not silently override.

If a section needs a visual not in MEDIA.md, halt. *"§<n> needs an asset that's not in MEDIA.md. Add it to MEDIA.md first, then we'll continue."* MEDIA.md is the canonical asset registry; growing it ad-hoc during page builds defeats its purpose.

## Phase 5 emphasis — marketing tier folders only

Glob for reuse only inside the marketing tier folder (`components/landing/`, `components/marketing/`, etc. per STRUCTURE.md). Do not propose reusing app-tier components — cross-tier imports are blocked.

If a section truly needs a primitive that only exists in app-tier (e.g. a chart), route through Generic with a wrapper, not by importing from app/.

## Phase 6 emphasis — RSC + generateMetadata required

Hard rules for marketing pages:

- **No top-level `"use client"` on the page component.** Marketing pages MUST be React Server Components. SEO depends on it.
- **`export const metadata: Metadata` (or `export async function generateMetadata`) is mandatory.** Title and description come from `SITEMAP.md` or `copy/<slug>.md`.
- **Client behavior lives in child components.** Auth redirects, search inputs, dropdown menus, accordion controls — all in small client components imported into the RSC tree.
- **The canon-pointer comment points to `agents/marketing/copy/<slug>.md`** as the single source of truth for copy.
- **No `lib/marketing-content.ts` mirror.** Ever. Inline copy directly.

## Phase 6 — Open Graph and structured data

Where appropriate (homepage, pricing, top-tier features), `generateMetadata` also returns `openGraph` and `twitter` fields. Use the values from `SITEMAP.md` if it declared them, else generate from headline + description. If the page is a blog/changelog landing, include JSON-LD structured data.

This is the only marketing-page-specific Phase 6 work beyond the base wire-up rules.

## Failure modes specific to marketing pages

- **Missing `marketing-brief` output** → halt, route to `marketing-brief`.
- **Slug not in SITEMAP** → halt, ask user to add it to SITEMAP first.
- **CONTENT.md row missing** for a feature/FAQ/testimonial the page references → halt, ask user to update CONTENT.md first.
- **Banned word found in copy** during `design-check` → surface, ask for replacement, propagate fix back to `copy/<slug>.md` so canon stays in sync.
- **Pre-existing `lib/marketing-content.ts` in the project** → leave it alone. Phase 6 writes the page without it. Note in the output that the mirror file is now orphaned and recommend a follow-up cleanup pass.
