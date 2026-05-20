# Phase 2 — Intake and tier

Phase 1 told us what the project looks like. Phase 2 figures out what the user wants and which tier it belongs to. One free-text question, one auto-inferred tier, one-line confirmation. Two prompts maximum.

---

## 2.1 — The intake prompt

Exactly one open question:

> In one sentence, what are you building?

No multiple-choice menus. No "describe the props." The user writes prose. Examples of valid answers:

- "A pricing card for the marketing page that shows three plans."
- "A KPI tile that pulls last 7 days revenue from the dashboard API."
- "A Hero with a headline, a sub-headline, and a CTA, plus a screenshot on the right."
- "A button. Just a button."
- "Something like Mantine's Combobox — searchable dropdown with multi-select."
- "I want to drop in this Aceternity card."

If the user already said it in the trigger ("make a hero for the landing page"), do NOT re-ask. Skip the prompt and use what they said.

---

## 2.2 — The three tiers (plain English)

The project has three tiers. Each lives in a different folder, has different rules, and has different downstream behavior. Internalize these definitions — they drive every later phase.

### Generic

Components used anywhere, with no business knowledge baked in, no copy baked in, no API calls baked in. Pure presentation primitives.

Examples:

- `Button`, `Card`, `Input`, `Tabs`, `Dialog`, `Tooltip` (shadcn primitives).
- A custom `Stepper`, a custom `RatingStars`, a custom `EmptyState` you built — still Generic, because they don't know your business.
- Headless / data-agnostic wrappers like `DataTable` (the skeleton) — Generic. The instance that displays "Customer Revenue" is App.

The Generic folder is where shadcn primitives go and where any new primitive belongs. Generic components import nothing tier-specific — only utilities (`cn`, icons, low-level libs).

### Marketing

Components that live on the public website and have copy / headlines / imagery / brand-voice baked in. They are not reusable on the dashboard side without being rewritten.

Examples:

- `Hero` (the landing-page hero with its headline and screenshot).
- `FeatureRow` (a feature description with title + sub + illustration).
- `PricingCard` (a plan card with name, price, feature list, CTA).
- `Testimonial` (a quote + author + company).
- `LogoBar` (the customer logos strip).
- `FAQAccordion` (the marketing FAQ list with the project's actual questions baked in).

Marketing components can read from `agents/marketing/CONTENT.md` if it exists (features list, comparisons, testimonials registry). Otherwise they take props or use ad-hoc copy.

### App

Components that live inside the dashboard / desktop app, are data-aware, and can talk to the project's API / database / state. They are not safe to drop onto the marketing site — they assume an authenticated user, a backend, a session.

Examples:

- `RevenueKPITile` (fetches `/api/metrics/revenue/7d`).
- `OrdersTable` (data-bound table with sortable columns and a query hook).
- `BillingPlanCard` (the in-app version, shows the user's current plan + downgrade button).
- `UserMenu` (shows the logged-in user's avatar + workspace switcher).
- Dashboard widgets, in-product onboarding flows, settings panels.

App components consume hooks (`useQuery`, `useSWR`, `useUser`, etc.) or props with real domain types.

---

## 2.3 — The decision tree

Walk top-down. First answer wins.

```
1. Does the component know your business data (calls API, uses domain hook,
   accepts a typed business model like Order/Subscription/User)?
     YES → App.
     NO  → continue.

2. Does the component have copy / headlines / imagery / brand-voice baked in,
   and live on the public website?
     YES → Marketing.
     NO  → continue.

3. Otherwise → Generic.
```

A few sharper edge calls:

- "A pricing card" → almost always **Marketing** (it has plan names and prices baked in). The Generic version of that is just `Card` (which already exists).
- "A button with a loading spinner" → **Generic**. No copy, no data.
- "A KPI tile" → **App** if it fetches data; **Generic** if it just takes a `value` prop.
- "An empty state for the inbox" → **App** if it has inbox-specific copy ("No new messages — invite a teammate to get started"); **Generic** if it's a generic `<EmptyState title="..." />`.
- "A logo bar of customer logos" → **Marketing**. The logos ARE the content.

---

## 2.4 — Surface filtering

Use the `Surfaces` set from `STRUCTURE.md` (Phase 1) to hide tiers that don't apply.

| Surface set | Tiers available |
|-------------|----------------|
| `{marketing, app-web}` | Generic, Marketing, App |
| `{app-web}` only (dashboard-only SaaS) | Generic, App |
| `{marketing}` only (landing-page project) | Generic, Marketing |
| `{app-desktop}` only (Tauri / Electron desktop) | Generic, App |
| `{app-web, app-desktop}` (web + desktop, no marketing) | Generic, App |

If the user requests a Marketing component in a desktop-only project, do not silently route it to App. Halt and surface:

```
You asked for a Hero, but this project has no marketing surface (no app/(marketing)/
or apps/marketing/). Options:
  A — Build it as a Generic primitive (composable, no copy baked in).
  B — I can add a marketing surface to STRUCTURE.md if you intend to add one.
  C — Skip.
```

---

## 2.5 — One-line confirmation

After inferring the tier, surface it for the user to confirm in one line. Do NOT list all three tiers and ask them to choose — that's overkill and most users won't recognize the distinctions.

Shape:

```
build-component — reading "a pricing card for the marketing page that shows three plans"

  Tier: Marketing
  Reason: lives on public site, has plan names / prices / CTAs baked in.
  Location (from STRUCTURE.md): src/components/marketing/pricing-card.tsx

  Proceed? (y / change tier / restart)
```

If the user replies `y` or nothing, proceed. If they say "no, make it generic" or "this should be app", switch tier and re-state the location. One change is allowed; if they keep flipping, surface the decision tree above and let them pick.

---

## 2.6 — What the locked tier drives downstream

The locked tier determines:

| Tier | Reads | Writes to | Allowed imports | Convention applies |
|------|-------|-----------|-----------------|-------------------|
| Generic | `DESIGN.md`, `FUNDAMENTALS.md` | `{generic-folder}/` from STRUCTURE.md | Utilities only (cn, icons, headless libs) | Yes — full triplet if new primitive |
| Marketing | `DESIGN.md`, `FUNDAMENTALS.md`, optionally `agents/marketing/CONTENT.md` | `{marketing-folder}/` | Generic + utilities | Triplet not required — composition first |
| App | `DESIGN.md`, `FUNDAMENTALS.md`, project hooks / API layer | `{app-folder}/` | Generic + utilities | Triplet not required — composition first |

Marketing and App tiers should be compositions in almost all cases. The `cva + forwardRef + cn` triplet applies to NEW Generic primitives, not to a `Hero` that's stitching together a `<Heading>`, `<Text>`, `<Button>`, and `<Image>`. Phase 3 makes that distinction explicit.

---

## 2.7 — Lock and continue

Once the tier is confirmed:

```yaml
intake_sentence: "a pricing card for the marketing page that shows three plans"
tier: marketing
location_hint: src/components/marketing/pricing-card.tsx
proposed_name: PricingCard
```

This object is the input to Phase 3 (reuse scan). The proposed name is a draft — Phase 3 might rename if a similar existing component suggests a better naming pattern.
