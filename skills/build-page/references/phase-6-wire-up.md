# Phase 6 — Wire-up

Goal: compose all the approved components into the final page file. Inline the copy directly from `agents/marketing/copy/<slug>.md` (marketing) or the dashboard brief. Leave a single canon-pointer comment at the top. One preview, one approval, one write.

## What gets written

One file at the location dictated by `STRUCTURE.md`:

- Marketing tier: typically `src/app/(marketing)/<slug>/page.tsx` (or `src/pages/<slug>.tsx` for older Next, or the framework's equivalent).
- Dashboard tier: typically `src/app/(dashboard)/<slug>/page.tsx`.

Page tier and routing convention come from `STRUCTURE.md`. Do not assume Next App Router unless STRUCTURE.md confirms it.

## File structure — marketing page

Marketing pages are React Server Components by default. No top-level `"use client"`. SEO metadata is exported. Client behavior (auth redirects, search inputs, modal triggers) lives in small child components imported into the RSC tree.

```tsx
// src/app/(marketing)/<slug>/page.tsx
//
// Copy mirrors agents/marketing/copy/<slug>.md — when that file changes,
// propagate the update here. Do NOT inline new copy without updating the
// canon first.

import type { Metadata } from "next";
import { PublicSiteChrome } from "@/components/layout/PublicSiteChrome";
import { Hero } from "@/components/landing/Hero";
import { TrustStrip } from "@/components/landing/TrustStrip";
// … other section components

import { AuthRedirect } from "./AuthRedirect"; // small client child if needed

export const metadata: Metadata = {
  title: "<from SITEMAP.md or copy/<slug>.md>",
  description: "<from SITEMAP.md or copy/<slug>.md>",
};

export default function <PageName>Page() {
  return (
    <PublicSiteChrome>
      <AuthRedirect />
      <Hero
        headline="<inline from copy/<slug>.md>"
        subhead="<inline from copy/<slug>.md>"
        primaryCta={{ label: "Start free", href: registerHref }}
      />
      <TrustStrip claims={[
        { title: "<inline from copy/<slug>.md>", body: "<inline>" },
        { title: "<inline>", body: "<inline>" },
        { title: "<inline>", body: "<inline>" },
      ]} />
      {/* … other sections in approved order */}
    </PublicSiteChrome>
  );
}
```

## File structure — dashboard page

Dashboard pages are client components by default (most need interactivity — fetches, state, mutations). No SEO metadata required. Loading/empty/error states declared in Phase 4 are wired in.

```tsx
// src/app/(dashboard)/<slug>/page.tsx
//
// Page spec lives in agents/specs/<slug>.md — keep in sync.

"use client";

import { PageHeader } from "@/components/dashboard/PageHeader";
import { KpiStrip } from "@/components/dashboard/KpiStrip";
// … other section components
import { useXxxData } from "@/lib/hooks/useXxxData";

export default function <PageName>Page() {
  const { data, isLoading, error } = useXxxData();

  if (isLoading) return <PageSkeleton />;
  if (error) return <PageError error={error} />;
  if (!data) return <PageEmpty />;

  return (
    <>
      <PageHeader
        title="<inline from spec>"
        breadcrumbs={[...]}
        actions={[...]}
      />
      <KpiStrip kpis={data.kpis} />
      {/* … other sections in approved order */}
    </>
  );
}
```

## Copy inlining — the rules

- **Take copy verbatim from `copy/<slug>.md`** for marketing pages. Do not paraphrase, abbreviate, or re-tone. If the copy file says "The operating system for event-photography businesses." that is the H1, character-for-character.
- **For repeating shared content** (FAQS, FEATURES lists where the list appears on multiple pages), inline the array directly in the page where it's used. Define the array right above the JSX that maps it. Do not extract to a separate file.
- **Type the inline arrays** if they'll be consumed by a typed component prop. A `const FEATURES: Feature[]` declaration above the component is fine — `Feature` is imported from the component file itself, not a separate types file.
- **The canon-pointer comment is mandatory.** Always at the top of the file, before imports. This is the sync contract — future agents see it and know to update `copy/<slug>.md` first, then propagate.
- **Hardcoded environment values** (`process.env.NEXT_PUBLIC_APP_URL`, CTA destinations like `/register`) are fine; that's not copy, that's infrastructure.

## What NOT to extract into a separate file

- Hero headline, subhead, section H2s — inline.
- Trust-strip claims, How-it-works steps, Selfie-moment paragraph, Camera-coverage path descriptions, Final-CTA copy — inline.
- One-off copy that appears only on this page — inline.

## What MAY be extracted (and the rule)

Extract only when the same array is consumed by 3+ different pages. Even then, extract into a `const` inside the file that defines the component that uses it most — not into a separate `lib/content.ts` mirror file. Example: if a `<HomeFaqList>` component uses the FAQ array on the homepage and on the /faq page, define `const HOMEPAGE_FAQS = […]` in the component file itself and import it into the second consumer.

**Never create `lib/marketing-content.ts`, `data/copy.ts`, `lib/content.ts`, or any equivalent runtime mirror of `CONTENT.md`.** That pattern is explicitly out.

## The preview

Show the full proposed file to the user. Format:

````
File: <absolute path>
Lines: <approx N>

```tsx
<full file content>
```

Approve / edit / restart?
````

Approve → write the file.
Edit → user describes the change in chat, you revise and re-preview.
Restart → drops back to Phase 2 (architecture). Rare — usually means something earlier was wrong and we should have caught it.

## After write

1. Write the file via `Write`.
2. Announce the path.
3. `design-check` fires automatically as the post-write gate. Let it run its 8 steps.
4. Surface any `design-check` outputs in this phase's summary (raw-value violations, missing tokens, etc.).
5. Print the end-of-skill output shape (see SKILL.md).

## Failure modes

- **`design-check` fails on a raw-value violation** — fix in place via `design-check`'s Step 8 auto-fix where possible; otherwise surface to the user and ask whether to add a token (which routes to `design-check` Step 4) or revise the page to use an existing token.
- **`design-check` flags a banned-word** — surface, ask the user for a replacement. Do not auto-fix banned words.
- **The written file imports a component that doesn't exist** — this should never happen if Phase 5 was done correctly. If it does, roll back: delete the page file, re-do Phase 5 for the missing row.
- **The page imports across a forbidden tier boundary** — `design-check` (or build-component's own gate) should have caught this in Phase 5. If it leaks to Phase 6, revise the imports to route through Generic primitives.

## What NOT to do

- Do not inline `"use client"` on a marketing page. Auth/search/modal client behavior goes into small child components.
- Do not create a `marketing-content.ts` mirror. Period.
- Do not extract one-off copy into props files or constants files.
- Do not write the page without the canon-pointer comment at the top.
- Do not write the page if any Phase 5 row still says "to create" — that row was not executed.
- Do not propose styling changes here. If the components don't compose well visually, that's a `build-component` revision (run it through that skill, not inline edits during wire-up).
- Do not run `design-check` manually after Phase 6 — it auto-fires per the hooks config. Manual invocation duplicates the run.
