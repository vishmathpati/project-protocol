# Sub-mode — Dashboard page

Fires when the page slug lands under `STRUCTURE.md`'s `dashboard` / `app` / `admin` surface, or when the user's wording matches app intent (dashboard, overview, settings, team, billing, analytics, projects, tickets).

Same 6 phases as the base skill — this doc captures the deltas.

## Inputs read in Phase 1

Narrower than marketing:

- `STRUCTURE.md` — app folder path, dashboard layout primitives (sidebar, topbar, content area).
- A page brief — either a row in `ROADMAP.md`, a file at `agents/specs/<slug>.md`, or a one-paragraph spec the user types inline.
- `DESIGN.md` — surface tier (usually `dashboard` with ratio 1.125), KPI tile tokens, chart palette.
- `FUNDAMENTALS.md` — banned words, density guidance, dashboard cardinal sins.
- Existing dashboard components — glob `components/dashboard/` (or whatever STRUCTURE.md says) and note: PageHeader, KpiStrip / KpiTile, ChartCard, DataTable, EmptyState, ErrorState, Skeleton primitives.

**If no brief exists, halt.** Ask the user inline: *"This page has no brief. Type a one-paragraph spec (what is it for, who uses it, what's the primary action) and I'll continue."* Do not invent the spec.

## Phase 2 emphasis — tool-shaped, not narrative

Dashboard pages are not stories. They're tools. The section list is usually:

1. **Page header** — title, breadcrumbs, page-level actions (button group, dropdown).
2. **Status / KPI strip** — 3–6 KPI tiles, scannable in 2 seconds.
3. **Primary work area** — the chart, table, form, canvas, or list that's the reason to be on this page.
4. **Secondary content** — recent activity, related items, suggested actions, drill-down links.
5. **Footer / debug info** — rarely; "data last updated X minutes ago", "Showing N of M".

Some pages collapse: a Settings page might be just (header + form). A Billing page might be (header + plan card + invoice table). Do not invent narrative sections (no Hero on a dashboard page, no FAQ on a dashboard page, no Final CTA on a dashboard page).

Rhythm tags from the base Phase 2 doc are replaced with information-density tags:
- `scan` — KPI strips, status bars, recent-activity lists. Designed to be read in seconds.
- `focus` — primary work area. Designed to be read for minutes.
- `meta` — header, footer, debug. Designed to be glanced at.

## Phase 3 emphasis — scan path, not eye-landing

Hierarchy in dashboard pages is about scan paths (Z-pattern, F-pattern, sidebar-anchored-then-right), not about which headline lands first.

- **Primary** — the data the user came to see. The chart's main metric, the table's first column, the form's first required field.
- **Secondary** — supporting data, the chart's legend, the table's secondary columns, form helper text.
- **Tertiary** — actions (export, filter, refresh), metadata (last-updated, row count), settings drawers.

## Phase 4 emphasis — loading, empty, error states

For every data-mock section, declare all four states explicitly:

| State | What it looks like |
|-------|--------------------|
| Loading | Skeleton shimmer / spinner / blank cards |
| Empty | EmptyState component with copy + optional illustration + primary CTA |
| Error | ErrorState component with error message + retry button |
| Partial | Some sections loaded, some still loading — declare the per-section skeleton |

Dashboard pages without explicit empty/error/loading states fail 50% of real user encounters. This is the single most important Phase 4 output for dashboard tier.

Also declare:
- **Refresh behavior** — does the data poll? Refetch on focus? Manual refresh button only?
- **Optimistic updates** — does the page apply changes locally before the server confirms?
- **Pagination / infinite scroll** — for tables and lists.

Animations are usually `none` for dashboard pages. The only allowed defaults: hover-state on rows / tiles, transition on accordion expand, transition on tab switch. Anything more requires a brand-axis justification (rare for dashboards).

## Phase 5 emphasis — app tier folders only

Glob for reuse only inside the app tier folder (`components/dashboard/`, `components/app/`, etc. per STRUCTURE.md). Cross-tier imports from marketing/ are blocked. Reuse-bias is even stronger for dashboard tier — most dashboard pages should be 90%+ composition of existing primitives.

Common pattern: a new dashboard page builds zero new components; it's pure composition of PageHeader + KpiStrip + ChartCard + DataTable.

If Phase 5 wants to "build new" for a dashboard page, push back hard. Confirm with the user: *"This page is proposing N new components — usually dashboard pages reuse 100%. Are you sure these primitives don't already exist?"*

## Phase 6 emphasis — client components are fine

Dashboard pages are usually client components. Top-level `"use client"` is acceptable — most need state, hooks, data fetching.

- **No `generateMetadata` required.** Dashboard pages live behind auth; SEO is irrelevant.
- **Data hooks at the top.** All `useX` hooks called early; loading / error / empty branches gate the main render.
- **The canon-pointer comment** points to the page brief or spec file.

## Failure modes specific to dashboard pages

- **No brief / spec** → halt and ask user to type a one-paragraph spec.
- **Proposing more than 1–2 new components** → push back on Phase 5 reuse scan; the project's dashboard primitives probably cover it.
- **Loading/empty/error states not declared in Phase 4** → cannot advance; these are non-optional for any data-bound section.
- **Marketing-style narrative sections proposed** (Hero, FAQ, Final CTA) → reject in Phase 2; that's the wrong shape for a tool.
- **Cross-tier import from marketing/** → blocked by `design-check`. If a dashboard page genuinely needs a primitive only in marketing/, route through Generic.
