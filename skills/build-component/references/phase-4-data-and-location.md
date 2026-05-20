# Phase 4 — Data shape and location

Strategy is locked. Now decide what the component consumes — props, registry, hooks, or hardcoded copy — and confirm the file path it writes to. Phase 4 also enforces the cross-tier import rules. Nothing is written until Phase 5; this phase still reads only.

---

## 4.1 — Three data shapes

Every component reads its data from one of three sources. Pick one (or a mix).

### Shape 1 — Props

The component is a pure function of its props. Caller passes everything in.

- Best for: Generic primitives, reusable App widgets, anything that needs to be testable in isolation.
- Trade-off: caller has to know the type, has to fetch / supply data.

```tsx
<RevenueKPITile value={7234.50} delta={+0.12} period="last 7 days" />
```

### Shape 2 — Project registry (Marketing only)

The component reads from a project-level content registry — `agents/marketing/CONTENT.md`. If a marketing-content workflow exists in the project (typically created by a separate `marketing-brief` skill), it stores authoritative versions of:

- Feature list (name, one-line description, illustration ref).
- Audience segments (designer / engineer / PM).
- Comparison matrix (vs competitor X / Y).
- Testimonials (quote, author, company, role).
- Pricing plans.
- FAQ.

Marketing components can import a typed accessor (e.g. `getFeatures()`, `getPlans()`) instead of accepting `features={[…]}` as props. Single source of truth — change a feature description in one place, every marketing block updates.

Check for `agents/marketing/CONTENT.md`. If present, propose registry-driven. If absent, fall back to props or ad-hoc copy with a user prompt.

### Shape 3 — Hook-driven (App only)

The component fetches its own data via existing project hooks. Glob the project for hook patterns first:

- `src/hooks/use-*.ts` — custom hooks.
- `src/lib/api/*.ts` — API wrappers.
- `useQuery` / `useSWR` / `useFetcher` / `useUser` usage in existing App components.

Propose the hook the new component will use. If no matching hook exists yet, ask whether to extend an existing one or fall back to props.

```tsx
export function RevenueKPITile({ period = "7d" }: { period?: "7d" | "30d" | "90d" }) {
  const { data, isLoading } = useMetrics(period);
  // …
}
```

### Shape 4 — Hardcoded copy (Marketing only, rarely)

For one-off marketing blocks where the copy is genuinely fixed forever (legal footer, copyright line, single landing-page hero with locked copy), inlining the strings is acceptable. Surface the trade-off: "This copy will be hardcoded. To change it later you'll need to edit this file. Confirm?"

---

## 4.2 — Decision table

| Tier | Default shape | Allowed | Forbidden |
|------|---------------|---------|-----------|
| Generic | Props | Props only | Registry, hooks |
| Marketing | Registry if CONTENT.md exists, else props | Props, registry, hardcoded | Hooks (no data fetching on marketing) |
| App | Props OR hook | Props, hooks | Marketing registry |

If the user's intake suggests a mismatch (e.g. a Marketing component that needs to fetch live data), halt and surface:

```
You asked for a marketing block that displays the current user's plan.
Marketing components don't fetch authenticated data — that crosses tiers.

Options:
  A — Move this to App tier (becomes a dashboard widget).
  B — Take the plan as a prop (server-rendered value passed in by the marketing page).
  C — Skip data-binding; build as a generic stub.
```

---

## 4.3 — Confirm the location

Phase 1 wrote `STRUCTURE.md` with the canonical folder for each tier. Use it.

```
Tier:     Marketing
Folder:   src/components/marketing/    (from STRUCTURE.md)
File:     pricing-card.tsx             (kebab-case, matches existing convention)
Import:   @/components/marketing/pricing-card

Looks right? (y / rename / nested folder)
```

File-naming rules (auto-detect from the existing folder):

- `kebab-case.tsx` (default if more than half of existing files are kebab) → `pricing-card.tsx`.
- `PascalCase.tsx` (if existing files are PascalCase) → `PricingCard.tsx`.
- `Component/index.tsx` (folder-per-component) → `PricingCard/index.tsx`.

For Swift: `PricingCardView.swift` following SwiftUI convention.

---

## 4.4 — Cross-tier import enforcement

This is the most important rule in Phase 4. The locked tier determines what the component can import from. Violations halt Phase 5.

| Locked tier | Allowed imports | Forbidden imports |
|-------------|-----------------|-------------------|
| Generic | Utilities (cn, icons, headless libs) | Anything in `marketing/`, anything in `app/` |
| Marketing | Generic primitives, utilities, marketing CONTENT registry | Anything in `app/`, app hooks, API calls |
| App | Generic primitives, utilities, project hooks, API layer | Anything in `marketing/` |

If the intake or strategy implies a forbidden import — for example, "a marketing pricing card that hides the upgrade button if the user is already on Pro" — surface the violation and route to Generic + wrapper pattern.

### Wrapper pattern — when cross-tier seems needed

The clean fix for "I need a thing that knows the user but feels like a marketing card":

1. Build a **Generic** primitive: `<PlanCardShell name price features cta highlighted />`. No data, no auth, no marketing copy.
2. In the **Marketing** page, render `<PlanCardShell {...marketingCopy}>` with hardcoded plans.
3. In the **App** page, render `<PlanCardShell {...currentUserPlan}>` with data from a hook.

Both surfaces use the same Generic shell. Neither crosses tiers. Each owns its own data binding.

Surface this if the intake demands it:

```
build-component — cross-tier conflict

  You asked for a pricing card that shows hidden upgrade options based on
  the logged-in user's plan. That's a marketing component that needs app data —
  not allowed.

  Recommended: build PlanCardShell as a Generic primitive. Then:
    - Marketing page renders <PlanCardShell ...> with public plan data.
    - App billing page renders <PlanCardShell ...> with the user's actual plan.

  Switch to Generic + wrapper? (y / show me alternatives)
```

If the user accepts, re-enter Phase 2 with `tier: generic` and continue. If they decline, halt and surface why.

---

## 4.5 — Detect existing hooks (App tier)

If the locked tier is App and the user wants hook-driven data:

```
Existing hooks in src/hooks/:
  - useUser         → current authenticated user
  - useWorkspace    → current workspace context
  - useMetrics(p)   → metric series for period p
  - useOrders(opts) → paginated orders query

Existing API wrappers in src/lib/api/:
  - api.metrics.get(period)
  - api.orders.list(opts)
  - api.billing.getPlan()

For your KPI tile, the natural fit is useMetrics("7d"). Use it?
  A — Yes, use useMetrics.
  B — Take the value as a prop instead (caller fetches).
  C — Need a new hook (out of scope here — handoff to the API/hook owner).
```

If C, halt Phase 4 and tell the user to add the hook first. Building a component against a hook that doesn't exist creates broken code.

---

## 4.6 — Detect marketing CONTENT registry (Marketing tier)

If the locked tier is Marketing:

```bash
test -f agents/marketing/CONTENT.md
```

If present, read its structure (typical headings: Features, Audiences, Comparisons, Testimonials, Pricing, FAQ). Map the intake to a registry section:

```
build-component — found agents/marketing/CONTENT.md

  Sections available:
    - Features (12 entries)
    - Audiences (3: designer, engineer, PM)
    - Comparisons (2: vs Linear, vs Jira)
    - Testimonials (5 quotes)
    - Pricing (3 plans: Free, Pro, Team)
    - FAQ (8 questions)

  For your PricingCard, propose reading from CONTENT.md Pricing section.
    A — Yes, read from registry (props become {planSlug: "pro"} only).
    B — Take props directly (caller passes full plan data).
    C — Hardcode copy in the component.
```

If CONTENT.md is missing, default to props (Shape 1) without asking.

---

## 4.7 — Output passed to Phase 5

```yaml
data_shape: registry        # one of: props | registry | hook | hardcoded
data_source: agents/marketing/CONTENT.md#pricing
hook_used: null
props_signature:
  - planSlug: "free" | "pro" | "team"
  - highlighted?: boolean
  - className?: string
location: src/components/marketing/pricing-card.tsx
import_allowlist:
  - "@/components/ui/*"
  - "@/lib/utils"
  - "@/lib/content"          # the CONTENT.md accessor
cross_tier_violations: []
```

Phase 5 takes this and produces the actual code preview.
