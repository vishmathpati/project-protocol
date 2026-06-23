# Sub-mode — Adopt external

A copy-paste component from a ship-the-source library (Aceternity, Magic UI, shadcn blocks, Tailwind UI snippets, any random GitHub gist) gets pulled into the project. The skill's job: normalize it against `brain/DESIGN.md` tokens before it lands.

Adopt-external uses the same 5 phases as the default flow, but the inputs come from the source (URL or pasted code), not from intake.

---

## When this fires

Triggers:

- "I want to use this Aceternity card: `https://ui.aceternity.com/components/...`"
- "Drop this into the project" (followed by pasted source).
- "Use this Magic UI component."
- "Convert this Tailwind UI snippet to our tokens."
- "I copied this from a GitHub example, normalize it."

If the user mentions a headless / installable library (Mantine, Chakra, MUI, React Aria, Radix), that is NOT adopt-external — that's recreate-from-inspiration. Different sub-mode.

---

## Phase 1 — Structure detection

Identical to the default flow. Read or write `brain/STRUCTURE.md`. The adopted component will almost always land in the **Generic** folder (it's a primitive, brought in for reuse), so the Generic location is what matters.

---

## Phase 2 — Intake = the source

Instead of asking "what are you building", ask "where's the source?". Three input shapes:

1. **URL**. Fetch with `WebFetch` if available. Aceternity / Magic UI / shadcn typically serve a code block in the page; extract it.
2. **Pasted code block**. The user gave you the file. Use it directly.
3. **GitHub raw link**. Fetch the raw file.

Tier is locked to **Generic** by default. If the source is clearly a marketing block (`Hero`, `Pricing`, `Testimonial` with copy already in it), surface the choice:

```
Adopting: an Aceternity Hero block.
  This source has copy + imagery baked in. Two ways to bring it in:
    A — Generic primitive: strip the copy, make it accept props (headline, sub, cta).
        Lands in components/ui/. Reusable across marketing pages.
    B — Marketing component: keep the copy as-is, lands in components/marketing/.

Pick A or B.
```

Default to A unless the user pushes back.

---

## Phase 3 — Reuse scan (still applies)

Glob the Generic folder. If a near-identical component already exists (e.g. project already has a `BentoGrid` and the user pasted another bento grid), halt:

```
adopt-external — found existing prior art:

  components/ui/bento-grid.tsx already exists.
  Options:
    A — Replace it with the new source (show me the diff first).
    B — Add the new one as bento-grid-v2.tsx and keep both.
    C — Merge: take the variants from the new source, keep the existing shell.
    D — Abort, I'll edit the existing one instead.
```

If no overlap, continue.

---

## Phase 4 — Normalize values against `DESIGN.md` tokens

This is the heart of adopt-external. Read the source line by line. Classify every visual value:

| Found in source | Action |
|----------------|--------|
| Raw hex (`#1a1a1a`, `#fff`) | Look up the closest token in `DESIGN.md`. Replace. |
| Raw spacing (`p-4`, `gap-2`) on Tailwind classes that already use the project's scale | Keep — these resolve through Tailwind tokens. |
| Raw spacing in inline styles (`style={{ padding: "17px" }}`) | Round to the nearest scale value. Replace. |
| Raw font-family in inline styles | Look up `--font-display` / `--font-body`. Replace. |
| Hardcoded shadow (`shadow-[0_10px_40px_rgba(...)]`) | If `DESIGN.md` has a matching shadow token → replace. If not → surface as unmappable. |
| Hardcoded gradient (`bg-gradient-to-r from-purple-500 to-pink-500`) | Two-stop gradient is a cardinal sin per FUNDAMENTALS.md. Surface, propose: collapse to a single color OR add a single-direction `--gradient-X` token. |
| Animation timing (`duration-1000`, custom keyframes) | If outside motion-token range (150–300ms by default), surface. |
| `style={{ ... }}` blocks with computed values | Often the only way Aceternity ships physics-y effects. Keep, but extract magic numbers into named consts at the top of the file. |
| Third-party library imports (`framer-motion`, `gsap`, `lottie`) | Surface. The user has to confirm each new dependency. |
| Class names matching the project's existing convention | Keep as-is. |

Walk the source, build a normalization map:

```
Source raw value           →  Project token (or unmappable)
--------------------------    ---------------------------------
#0a0a0a                       var(--bg) (Tailwind: bg-background)
#fafafa                       var(--surface-2) (close approximation)
17px padding                  var(--space-4) (16px, off by 1)
"Inter, sans-serif"           var(--font-body)
shadow-[0_20px_60px_...]      UNMAPPABLE — propose --shadow-floating
bg-gradient-to-r from-purple  CARDINAL SIN — two-stop gradient
framer-motion import          NEW DEPENDENCY — needs user approval
```

---

## Phase 5 — Surface unmappables, generate normalized version, write

### 5a — Surface unmappables BEFORE writing

```
adopt-external — values that don't map to your DESIGN.md:

  1. Shadow: shadow-[0_20px_60px_rgba(0,0,0,0.3)]
     Closest existing token: --shadow-md (0 4px 12px). Not a match.
     Options:
       A — Add new token --shadow-floating to DESIGN.md (recommended).
       B — Keep raw value as a one-off exception (cardinal-sin violation).
       C — Simplify to existing --shadow-md (loses the effect).

  2. Gradient: bg-gradient-to-r from-purple-500 to-pink-500
     This is a two-stop blue/purple gradient — DESIGN.md DO NOT list bans it.
     Options:
       A — Collapse to solid --primary (recommended).
       B — Replace with a token-defined single-direction gradient (you'll need
           to define --gradient-hero in DESIGN.md first).
       C — Keep as-is (cardinal-sin violation).

  3. New dependency: framer-motion
     Not currently in package.json.
     Options:
       A — Add it (npm install framer-motion).
       B — Strip the motion, keep static.
       C — Abort.

Decide each before I generate the normalized file.
```

Wait for decisions. For each:

- If **A** on a token — halt write, hand off to `design-check` Step 4 (propose new token, wait for user confirmation, then the user adds to `DESIGN.md` + `globals.css`). Once added, resume.
- If **C** that's a cardinal-sin violation — surface that loud, get a second explicit "yes I know" confirmation. Annotate the line with an `eslint-disable-next-line no-restricted-syntax -- explicit override` comment.

### 5b — Generate the normalized component

After all unmappables are resolved, render the normalized file. Example:

````
adopt-external — preview

  Will write: src/components/ui/spotlight-card.tsx

```tsx
"use client";

import * as React from "react";
import { motion, useMotionValue } from "framer-motion";
import { cn } from "@/lib/utils";

export interface SpotlightCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const SpotlightCard = React.forwardRef<HTMLDivElement, SpotlightCardProps>(
  ({ className, children, ...props }, ref) => {
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    return (
      <motion.div
        ref={ref}
        className={cn(
          "relative rounded-lg border border-border bg-card p-6 shadow-md",
          "transition-shadow hover:shadow-floating",
          className
        )}
        onMouseMove={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          mouseX.set(e.clientX - rect.left);
          mouseY.set(e.clientY - rect.top);
        }}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);
SpotlightCard.displayName = "SpotlightCard";
```

  Imports: framer-motion (newly added), cn from @/lib/utils
  Tokens normalized:
    - #0a0a0a       → bg-card (--surface)
    - #1a1a1a       → border-border (--border)
    - shadow-[...]  → shadow-md, hover:shadow-floating (new token, just added)

  Approve? (y / edit / restart)
````

### 5c — Write to the Generic folder

On approve, write to the Generic location from `STRUCTURE.md`. After write, `design-check` runs as usual.

---

## Hard rules for adopt-external

- **Never write the raw source.** Always normalize first. The whole point of this sub-mode is the normalization.
- **Surface every unmappable.** Silent acceptance of a raw value is a failure of this skill.
- **New dependencies are a separate ask.** Even one new package needs explicit confirmation.
- **One file in, one file out.** Don't blow up the source into multiple files. If the source is a 200-line monster that should be 3 components, surface that as a follow-up: "After writing, want me to split this into Card + CardHeader + CardContent? Separate skill run."
- **Attribution comment at the top.** Add a one-line comment: `// Adapted from <source URL>. Normalized against project DESIGN.md.` for license traceability.
- **License check.** If the source page declares a license (MIT / Apache / "free to use"), good. If unclear, surface: "Couldn't find a clear license on the source page. Confirm you have rights to use this code in this project."

---

## When adopt-external is the wrong tool

- If the user wants the WHOLE component library (every primitive Aceternity ships), they should install a package — adopt-external is for one-off pulls, not bulk imports.
- If the source is from an installable library that's already in node_modules (e.g. they pasted a Mantine snippet but Mantine is installed), route to recreate-from-inspiration instead — building a project-tokens version on top of the headless layer, not copy-paste.
- If the source uses a completely different paradigm (CSS-in-JS source but project is Tailwind), the conversion is heavy enough to warrant a manual rewrite. Surface that — don't pretend to auto-convert across paradigms.
