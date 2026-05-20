# Phase 3 — Reuse scan

Tier is locked. Now find what already exists so the new thing doesn't duplicate it. Reuse beats create — every time. This phase also picks the **strategy** for the build: compose, extend, or new primitive. The strategy decides whether the cva triplet applies at all.

---

## 3.1 — Glob the relevant tier folder

Use the location from `STRUCTURE.md` for the locked tier. Glob it for component files (`*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.swift`).

Also glob the **Generic** folder unconditionally — Marketing and App components are allowed to compose Generic primitives, so the user's available kit always includes Generic.

Example glob set for a Marketing build:

```
{marketing-folder}/**/*.{ts,tsx}    — same-tier prior art
{generic-folder}/**/*.{ts,tsx}      — available primitives to compose with
```

Read file names + (cheaply) the first export of each. Delegate to a fast sub-agent if there are more than ~40 files. Build a flat list:

```
Existing in marketing/:
  - hero.tsx                (Hero)
  - feature-row.tsx         (FeatureRow)
  - testimonial.tsx         (Testimonial)
  - logo-bar.tsx            (LogoBar)

Existing primitives in ui/:
  - button.tsx              (Button — variants: default/secondary/ghost/destructive)
  - card.tsx                (Card, CardHeader, CardContent, CardFooter)
  - badge.tsx               (Badge)
  - separator.tsx           (Separator)
  - tabs.tsx                (Tabs)
  - typography             (Heading, Text)
```

---

## 3.2 — Find same-or-similar prior art

Score each existing component for relevance to the intake sentence. Use lightweight heuristics:

- Exact name match (intake says "pricing card", existing has `pricing-card.tsx`) → near-certain match. Halt and ask: extend or rename?
- Synonyms or sibling words ("plan card" ≈ "pricing card", "stat tile" ≈ "metric tile") → probable overlap.
- Same family ("FAQAccordion" exists, user wants "PricingFAQ") → composition candidate.
- Nothing related → strategy = new build.

Surface findings:

```
build-component — looking for existing prior art:

  Same-tier matches in marketing/:
    (none — no pricing-card-like component yet)

  Composable primitives available in ui/:
    - Card                → for the outer surface
    - Heading, Text       → for plan name + price + feature list
    - Button              → for the CTA
    - Badge               → for "Most popular" highlight
    - Separator           → between feature groups

Strategy proposal: compose existing primitives. No new primitive needed.
```

If a same-tier match is found, halt and ask:

```
build-component — found existing prior art:

  marketing/pricing-card.tsx already exists.

  Options:
    A — Extend it (add a new variant / prop).
    B — Rename your new one (e.g. PricingCardPro) and live alongside.
    C — Replace it (destructive — show me the diff first).
    D — Stop, I'll edit the existing one instead.
```

---

## 3.3 — Propose a strategy

Three strategies. Pick exactly one. The strategy drives Phase 5 (preview and write).

### Strategy A — Compose

The new component is built by stitching together existing primitives. No new primitive is created. Just JSX (or equivalent) + `cn` for className merging + props.

**This is the default for Marketing and App tiers.** Most marketing blocks and app widgets are compositions. They don't have variants in the cva sense — they have content. They don't need ref-forwarding because nothing imperatively focuses a marketing hero from the outside.

What strategy A produces:

```tsx
// src/components/marketing/pricing-card.tsx
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Heading, Text } from "@/components/ui/typography";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

type PricingCardProps = {
  name: string;
  price: string;
  cadence?: string;
  features: string[];
  cta: { label: string; href: string };
  highlighted?: boolean;
  className?: string;
};

export function PricingCard({
  name, price, cadence, features, cta, highlighted, className,
}: PricingCardProps) {
  return (
    <Card className={cn(highlighted && "border-primary", className)}>
      <CardHeader>
        {highlighted ? <Badge>Most popular</Badge> : null}
        <Heading level={3}>{name}</Heading>
        <Text muted>{price}{cadence ? ` / ${cadence}` : null}</Text>
      </CardHeader>
      <Separator />
      <CardContent>
        <ul className="space-y-2">
          {features.map(f => <li key={f}><Text>{f}</Text></li>)}
        </ul>
      </CardContent>
      <CardFooter>
        <Button asChild className="w-full">
          <a href={cta.href}>{cta.label}</a>
        </Button>
      </CardFooter>
    </Card>
  );
}
```

No cva. No `forwardRef`. Just composition. This is the right shape for the overwhelming majority of marketing and app components.

### Strategy B — Extend

An existing primitive is close to what's needed, but missing one prop or variant. Add the variant in-place; do NOT clone the component.

What strategy B produces:

```tsx
// Before — components/ui/button.tsx
const buttonVariants = cva(base, {
  variants: {
    variant: { default: ..., secondary: ..., ghost: ..., destructive: ... },
    size: { sm: ..., md: ..., lg: ... },
  },
});

// After — adding a "loading" state variant
const buttonVariants = cva(base, {
  variants: {
    variant: { default: ..., secondary: ..., ghost: ..., destructive: ... },
    size: { sm: ..., md: ..., lg: ... },
    loading: { true: "cursor-wait opacity-80" },
  },
});
```

Phase 5 surfaces the diff, not a new file. `design-check` then re-runs against `button.tsx`.

### Strategy C — New primitive

Nothing existing fits. The build is a brand-new presentation primitive (e.g. project doesn't have a `Stepper` yet, and the user wants one). **This is rare** — most "I need a new component" requests are actually compositions.

This is the only case where the **convention triplet** applies in full:

- **`cva`** (or the project's detected equivalent) — for variants.
- **`forwardRef`** — so consumers can attach refs.
- **`cn`** for className merging.

What strategy C produces (shadcn convention):

```tsx
// src/components/ui/stepper.tsx
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const stepperVariants = cva(
  "flex items-center gap-2 text-muted-foreground",
  {
    variants: {
      orientation: {
        horizontal: "flex-row",
        vertical: "flex-col items-start",
      },
      size: {
        sm: "text-sm",
        md: "text-base",
      },
    },
    defaultVariants: { orientation: "horizontal", size: "md" },
  }
);

export interface StepperProps
  extends React.HTMLAttributes<HTMLOListElement>,
    VariantProps<typeof stepperVariants> {}

export const Stepper = React.forwardRef<HTMLOListElement, StepperProps>(
  ({ className, orientation, size, ...props }, ref) => (
    <ol
      ref={ref}
      className={cn(stepperVariants({ orientation, size }), className)}
      {...props}
    />
  )
);
Stepper.displayName = "Stepper";
```

If the project's detected convention is NOT cva (e.g. `styled-components`), generate the equivalent in that convention. The principle is the same: variants + ref + className merge.

---

## 3.4 — Why the triplet doesn't apply to compositions

This is the most common mistake the skill is designed to prevent.

A `Hero` does not need variants — it has props (`title`, `subtitle`, `cta`). It does not need `forwardRef` — nothing outside the marketing page is going to imperatively focus the hero. It does not need cva — the only conditional class is "highlighted? add border-primary", which is one ternary inside `cn`.

Imposing the triplet on a composition produces dead code:

```tsx
// WRONG — over-engineered for a composition
const heroVariants = cva("...", { variants: { variant: { default: "" } } });
export const Hero = React.forwardRef<HTMLDivElement, HeroProps>(({ ...props }, ref) => (
  <section ref={ref} className={cn(heroVariants({ variant: "default" }), className)}>
    ...
  </section>
));
```

There's only one variant. The ref is unused. The cva wrapper adds nothing. Just write the function.

The principle:

| Strategy | Triplet applies? | Why |
|----------|------------------|-----|
| A — Compose | No | No variants, no ref need |
| B — Extend | Touches the existing primitive's triplet | Modify, don't add |
| C — New primitive | Yes | This is what the triplet is for |

---

## 3.5 — Surface the strategy and proceed

Show the user the chosen strategy in one block and ask for one confirmation:

```
build-component — strategy

  Tier:     Marketing
  Strategy: A — compose
  Plan:
    Build PricingCard as a composition of Card / Heading / Text / Button / Badge / Separator.
    No new primitive. No cva. No forwardRef.
    Props: name, price, cadence, features[], cta, highlighted.

  Proceed to data shape (Phase 4)? (y / change strategy / restart)
```

If the user wants to flip strategy ("no, make it a primitive — we'll need variants later"), accept once and re-state. After confirmation, lock and move to Phase 4.

---

## 3.6 — Output passed to Phase 4

```yaml
strategy: A
prior_art_used:
  - Card from @/components/ui/card
  - Heading, Text from @/components/ui/typography
  - Button from @/components/ui/button
  - Badge from @/components/ui/badge
  - Separator from @/components/ui/separator
  - cn from @/lib/utils
proposed_name: PricingCard
proposed_location: src/components/marketing/pricing-card.tsx
new_primitive: false
```
