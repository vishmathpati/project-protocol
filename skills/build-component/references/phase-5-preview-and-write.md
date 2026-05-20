# Phase 5 — Preview and write

Everything is decided: tier, strategy, data shape, location, convention. Phase 5 generates the actual component code, shows it to the user, and writes the file on approval. After the write, `design-check` fires as the post-write gate — do not duplicate its 7 steps here.

---

## 5.1 — Detect convention (silently)

Before generating code, lock the project's convention. Use `STRUCTURE.md` if it recorded one. Otherwise re-detect from `package.json`:

| Detected | Convention | Code shape |
|----------|-----------|------------|
| `class-variance-authority` + `tailwindcss` + `clsx` + `tailwind-merge` | shadcn-style | cva + forwardRef + cn (for primitives only) |
| `styled-components` | styled-components | `styled.div\`…\`` with `props.theme.tokens` |
| `@emotion/styled` | Emotion | similar to styled-components |
| `@vanilla-extract/css` | vanilla-extract | tokens from `*.css.ts` |
| `*.module.css` files present | CSS modules | `.module.css` file alongside component |
| None of the above | Vanilla CSS-with-tokens | `<style>` block or external `.css` consuming CSS variables |

Only ask the user if **no clear convention can be detected**. Default to vanilla CSS-with-tokens in that ambiguous case, and offer them to override.

For Swift: convention is always SwiftUI with `Color.tokenName` / `Spacing.tokenName` references from `DesignTokens.swift`.

---

## 5.2 — Generate the code

Delegate to a reasoning sub-agent. Pass it the locked object from Phases 1–4:

```yaml
intake_sentence: "..."
tier: marketing
strategy: A
proposed_name: PricingCard
location: src/components/marketing/pricing-card.tsx
data_shape: registry
data_source: agents/marketing/CONTENT.md#pricing
prior_art_used:
  - Card from @/components/ui/card
  - Heading, Text from @/components/ui/typography
  - Button from @/components/ui/button
  - Badge from @/components/ui/badge
  - Separator from @/components/ui/separator
convention: shadcn-style
new_primitive: false
tokens_required:
  - --primary (highlight border)
  - --border (default border)
  - --space-4, --space-6 (gaps)
```

Sub-agent rules:

1. Use only the imports in `prior_art_used` + `cn` from utilities. No new dependencies.
2. Use only the tokens in `tokens_required`. If you need a token that's not there, stop and report it for `design-check` Step 4 to handle. Do not improvise.
3. If `new_primitive: false`, do NOT emit cva, do NOT emit `forwardRef`. Just a function component.
4. If `new_primitive: true`, emit the full triplet (or convention-equivalent).
5. Five required UI states for any interactive component (per `FUNDAMENTALS.md`): default, hover, focus, active, disabled. Loading where applicable. Skipping a state is a violation `design-check` will catch.
6. No raw hex, no raw px, no raw font-family. Token references only.

---

## 5.3 — Show the full preview

Surface the complete generated file to the user before any write:

````
build-component — preview

  Will write: src/components/marketing/pricing-card.tsx

```tsx
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Heading, Text } from "@/components/ui/typography";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { getPlan } from "@/lib/content";
import { cn } from "@/lib/utils";

type PricingCardProps = {
  planSlug: "free" | "pro" | "team";
  highlighted?: boolean;
  className?: string;
};

export function PricingCard({ planSlug, highlighted, className }: PricingCardProps) {
  const plan = getPlan(planSlug);
  return (
    <Card className={cn(highlighted && "border-primary", className)}>
      <CardHeader>
        {highlighted ? <Badge>Most popular</Badge> : null}
        <Heading level={3}>{plan.name}</Heading>
        <Text muted>
          {plan.price}{plan.cadence ? ` / ${plan.cadence}` : null}
        </Text>
      </CardHeader>
      <Separator />
      <CardContent>
        <ul className="space-y-2">
          {plan.features.map(f => <li key={f}><Text>{f}</Text></li>)}
        </ul>
      </CardContent>
      <CardFooter>
        <Button asChild className="w-full">
          <a href={plan.cta.href}>{plan.cta.label}</a>
        </Button>
      </CardFooter>
    </Card>
  );
}
```

  Approve? (y / edit / restart)
````

User options:

- **y** → write.
- **edit** → "what to change?" — accept free-text instructions, regenerate, re-preview.
- **restart** → drop the current generation, return to Phase 2.

Allow at most 2 edit rounds. After that, recommend taking it to discussion-mode for deeper rework.

---

## 5.4 — Write

On approve, do the actual write. One file, one path:

```bash
mkdir -p $(dirname src/components/marketing/pricing-card.tsx)
```

Then `Write` the contents. Do not touch any other file. Do not modify `DESIGN.md`. Do not add to a barrel `index.ts` — let the user import the component directly.

If the parent folder didn't exist before this (e.g. `src/components/marketing/` is brand new):

- Create it.
- Surface it: "Created src/components/marketing/ — first marketing component in this project."
- Do NOT scaffold an `index.ts` barrel or a `README.md` for the folder.

---

## 5.5 — Hand off to `design-check`

After the write, the `design-check` skill should fire automatically (it's registered to trigger on "created component" / "edited component" patterns).

If the host environment doesn't auto-fire skills, surface the prompt:

```
build-component — wrote src/components/marketing/pricing-card.tsx.

  Next: design-check will sweep the file against DESIGN.md tokens, the 7 cardinal
  sins, and the 5 required states. Run it now? (y / skip)
```

Do not duplicate `design-check`'s 7 steps here. The two skills chain — `build-component` writes, `design-check` audits.

---

## 5.6 — Output summary

Final message:

```
build-component — done

  Wrote: src/components/marketing/pricing-card.tsx
  Tier: Marketing
  Strategy: A — compose
  Convention: shadcn-style
  New primitive: no
  Lines: 41

  Imports used:
    - Card, CardHeader, CardContent, CardFooter from @/components/ui/card
    - Heading, Text from @/components/ui/typography
    - Button from @/components/ui/button
    - Badge from @/components/ui/badge
    - Separator from @/components/ui/separator
    - getPlan from @/lib/content
    - cn from @/lib/utils

  Tokens used:
    - --primary, --border, default Tailwind spacing scale

  No new tokens proposed. No cross-tier imports. No raw values.

  Next:
    → design-check (auto-fires)
    → To use: import { PricingCard } from "@/components/marketing/pricing-card"
```

---

## 5.7 — Failure paths

What to do when something blocks the write:

| Blocker | Response |
|---------|----------|
| User says "no" after preview | Halt. Return to Phase 2 OR end the skill, user's choice. |
| Required token missing from DESIGN.md | Halt write. Surface "design-check Step 4 — propose new token: \<token\>. Add it before I write the component?" Wait for confirmation. Then re-enter Phase 5. |
| Prior-art file got modified between Phase 3 and Phase 5 | Re-glob and re-confirm. Don't write against stale imports. |
| Convention can't be detected | Ask once: "Couldn't infer convention. Use: A — cva+forwardRef+cn / B — styled-components / C — CSS modules / D — vanilla CSS." Save the choice into `STRUCTURE.md` so it's never asked again. |
| File path collision (target file already exists) | Halt. "src/components/marketing/pricing-card.tsx already exists. Options: A — overwrite (show diff) / B — write as pricing-card-v2.tsx / C — abort." |

---

## 5.8 — One concrete walk-through (strategy C, new primitive)

For contrast — what Phase 5 emits for a Generic, new-primitive build:

````
build-component — preview

  Will write: src/components/ui/stepper.tsx

```tsx
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

  This is a new primitive — emits the full triplet (cva + forwardRef + cn).
  Approve? (y / edit / restart)
````

Same flow, different shape. The triplet appeared because `new_primitive: true`. For the PricingCard composition above, it didn't.
