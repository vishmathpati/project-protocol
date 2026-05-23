---
name: marketing-brief
description: Deep marketing-site brief that runs ONCE near the end of a project, after features are built. Writes a comprehensive set of canonical files to `agents/marketing/` (CONTENT registry, SITEMAP, per-page briefs, per-page copy, MEDIA manifest, layout sketches) that the `build-component` skill consumes when implementing marketing-tier components. Triggers — "marketing brief", "write marketing site", "build marketing copy", "create marketing pages", "set up the marketing site", "/marketing-brief".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Task, WebSearch
---

# Marketing Brief

The end-of-project skill that turns a built product into a marketing-site execution plan. Runs ONCE, after features exist on disk and `agents/ROADMAP.md` reflects what shipped. Produces a complete set of canonical files in `agents/marketing/` that the `build-component` skill reads when implementing marketing pages, components, and copy.

It exists because writing marketing pages ad-hoc — one section at a time, copy invented per file, features hardcoded into headlines — produces drift: the nav menu lists features the footer doesn't; the comparison page mentions a competitor the home page never positions against; the screenshot on one page shows "Acme Inc" and another shows "Demo Corp". This skill is the single planning pass that locks the inputs so every later marketing component reads from the same source of truth.

---

## When this fires

- User asks: "marketing brief", "write marketing site", "build marketing copy", "create marketing pages", "set up the marketing site", "I want to write the marketing site now", "do the landing pages".
- Project has shipped enough features that the marketing surface has something to claim. (If features aren't built yet, the skill warns and asks the user to confirm anyway.)
- Slash command: `/marketing-brief`.

### Auto-skip conditions

Read `agents/STRUCTURE.md` (or `agents/docs/INDEX.md` if STRUCTURE.md is absent) and look for declared surfaces. If the only surfaces are dashboard / internal-tool / admin-console / CLI and no `marketing` / `landing` / `web` surface is declared, refuse politely with one line:

> This project's declared surfaces are <list>. No marketing surface — skipping. If you do want a marketing site, add it to `agents/STRUCTURE.md` first and re-invoke.

Then exit. Do not write anything.

User override: phrases like "force it", "I know, do it anyway", "marketing brief — anyway" bypass the skip and proceed.

---

## What it produces

All files land under `agents/marketing/`. Nothing outside that folder is touched.

```
agents/marketing/
├── CONTENT.md              ← single source of truth (features, audiences, comparisons, testimonials, FAQs, legal)
├── SITEMAP.md              ← page list with slug, intent, primary CTA, audience descriptor
├── MEDIA.md                ← per-section visual-anchor manifest + fictional-customer brand
├── briefs/
│   ├── home.md
│   ├── pricing.md
│   ├── customers.md
│   ├── features.md
│   └── … one per page in SITEMAP
├── copy/
│   ├── home.md
│   ├── pricing.md
│   └── … one per page (every headline, subhead, button label)
└── layouts/
    ├── home.md
    ├── pricing.md
    └── … one per page (block-level wireframe in markdown)
```

`build-component` then reads these when implementing each page's actual code.

---

## Compatibility — never overwrite

Strict rules:

- **Never touch existing page files** (`app/page.tsx`, `pages/index.tsx`, `app/(marketing)/**`). This skill only writes to `agents/marketing/`. Implementation is a separate step.
- **Existing `agents/marketing/` content** — if any of the canonical files already exist with real content (not empty stubs), show them to the user and offer a 3-way merge:
  - `replace` — overwrite (rare; only when user explicitly says "throw it out, start over").
  - `merge` — read existing entries, fold them into the new structure, dedupe, keep user prose.
  - `append` — leave existing content intact, add new sections below under a `## v2 — <date>` heading.
  - Default is `merge`. Wait for explicit confirmation before any write.
- **No silent rewrites** of user-considered prose. If a brief, copy file, or layout already has prose that reads as user-authored (not boilerplate), keep it. Restructure around it.
- **CONTENT.md is special** — even on `replace`, the existing FEATURES / TESTIMONIALS / FAQS tables are surfaced for review row-by-row before any line is dropped.

---

## The 7 phases

Walk in order. Each phase has a reference doc in `references/`. Open the reference doc only when entering that phase — progressive disclosure keeps context lean.

### Phase 1 — Intake

Read existing canon and synthesise what's already known. Ask only for missing pieces. Specifically:

- `agents/BRAND.md` — audience, archetype, tribe, refusal list.
- `agents/ROADMAP.md` — locked features (shipped + in-flight).
- `agents/docs/INDEX.md` — current code-and-feature map.
- `agents/STATUS.md` — what's actually live vs. in progress.
- `agents/STRUCTURE.md` — declared surfaces (also used for auto-skip detection above).

Surface a one-page summary back to the user and wait for "looks right, proceed" before Phase 2.

→ See `references/phase-1-intake.md`.

### Phase 2 — Content registry

Write `agents/marketing/CONTENT.md`. This is the single source of truth for every shared marketing fact. Structured markdown tables for:

- **FEATURES** — name, icon, blurb, page slug, audiences served.
- **AUDIENCES** — segment name, descriptor, top-of-mind pain, primary CTA.
- **COMPARISONS** — competitor name, where we win, where they win, comparison-page slug.
- **TESTIMONIALS** — quote, author, role, company (use the fictional-customer brand from Phase 6), audience tag.
- **FAQS** — question, answer, page tag (home / pricing / per-feature).
- **LEGAL_PAGES** — name, slug, owner, last-reviewed date.

Every other marketing file reads from this. The nav menu, the footer feature columns, the per-feature pages, the comparison pages, the testimonial blocks — all of them resolve their content by referencing rows in CONTENT.md, not by inlining strings.

→ See `references/phase-2-content-registry.md`.

### Phase 3 — Sitemap

Propose the page list. Standard SaaS shape, edited by user:

- `home` — primary entry, broad audience.
- `pricing`.
- `customers` — index + per-customer case study pages.
- `features` — index + per-feature pages (one per FEATURES row from CONTENT).
- `comparisons` — one per COMPARISONS row.
- `blog` landing + `changelog` landing.
- `about`.
- `legal/*` — one per LEGAL_PAGES row (privacy, terms, DPA, etc.).

User adds / removes / renames. Write `agents/marketing/SITEMAP.md` with each page's name, slug, single intent, primary CTA, and a one-line audience descriptor.

→ See `references/phase-3-sitemap.md`.

### Phase 4 — Per-page briefs

For each page in SITEMAP, write `agents/marketing/briefs/<slug>.md`. Each brief contains:

- **Audience state on entry** — what they fear / want before opening this page.
- **Single intent** — one CTA per page. Pages with two intents fail.
- **Story arc** — claim → proof → how → social proof → ask is the classic, but per-page can vary.
- **Section-by-section breakdown** — for each section: eyebrow, headline, blurb, visual-anchor type, CTA spec.

Briefs are skeletons — what each section is *for*, not the final copy.

→ See `references/phase-4-briefs.md`.

### Phase 5 — Per-page copy

For each page in SITEMAP, write `agents/marketing/copy/<slug>.md`. Every headline, subhead, button label, section copy, footer text — finalised, ready to paste into JSX.

Rules:

- **Read from CONTENT.md** for shared data (features, customer names, FAQ entries). Never hardcode a feature name or customer name in a copy file.
- **Apply the FUNDAMENTALS banned-words list** (`agents/FUNDAMENTALS.md` § banned words). Scan every line.
- **Every headline is a claim**, never a description. ✅ "Turn clicks into revenue." ❌ "Our analytics platform."

→ See `references/phase-5-copy.md`.

### Phase 6 — Media manifest

Write `agents/marketing/MEDIA.md`. Per section in each page, declare the visual-anchor type: screenshot / photo / stat / pull quote / code block / illustration.

Ask the user ONCE for the fictional-customer brand name. This is the dub.co "acme" pattern — every product screenshot uses the same fake brand for visual coherence ("acme.link" appearing in three screenshots reads as one brand; "Acme Inc" + "Demo Corp" + "Test Co" reads as broken). Save the fictional-customer name to MEDIA.md and reuse everywhere.

This is a manifest, not actual assets. The user or a follow-up tool produces the real screenshots / photos / illustrations using this manifest as the spec.

→ See `references/phase-6-media.md`.

### Phase 7 — Layout sketches

For each page in SITEMAP, write `agents/marketing/layouts/<slug>.md`. Block-level wireframe in markdown — rectangles labelled with intent (full-bleed vs contained, image-left/text-right, sticky elements, etc.). Not pixels, not Figma — structural intent only.

Each block references the corresponding brief section by name so `build-component` can connect "section 2 in the layout" to "section 2 in the copy" to "section 2's visual anchor in MEDIA.md".

→ See `references/phase-7-layouts.md`.

---

## Output shape (end of skill)

```
marketing-brief — summary

Project: <name>
Surfaces: <list from STRUCTURE.md>
Fictional customer locked: <brand name + domain>

Sitemap: <N> pages
Briefs written: <N>
Copy files written: <N>
Layout sketches written: <N>

Wrote:
  ✅ agents/marketing/CONTENT.md         (features: N, audiences: N, comparisons: N, FAQs: N)
  ✅ agents/marketing/SITEMAP.md         (N pages)
  ✅ agents/marketing/MEDIA.md           (N sections, fictional customer: <brand>)
  ✅ agents/marketing/briefs/*.md        (N files)
  ✅ agents/marketing/copy/*.md          (N files)
  ✅ agents/marketing/layouts/*.md       (N files)

Next step:
  → Invoke build-page per page (start with home).
  → build-page reads SITEMAP + the page's brief + copy + layout + MEDIA + CONTENT,
    runs 6-phase layout-first composition (architecture → hierarchy → assets →
    component selection → wire-up), and delegates net-new component creation to
    build-component inline. design-check fires automatically after wire-up.
```

---

## Hard rules

- **Run once.** This skill is not a loop. If marketing files already exist, the 3-way merge is the only re-entry path.
- **Never overwrite existing page files** (`app/page.tsx` etc.) — only writes to `agents/marketing/`.
- **Surfaces-aware skip** — refuse cleanly on dashboard-only / internal-tool / CLI projects unless the user forces.
- **Fictional customer is asked once, reused everywhere.** Locked in MEDIA.md; every screenshot, every testimonial, every example URL uses it.
- **Language is English.** All of this user's projects are English-default. No translation phase here.
- **CONTENT.md is the source of truth.** No marketing file hardcodes a feature name, customer name, or FAQ entry — they reference CONTENT rows.
- **Every headline is a claim.** Enforced in Phase 5; flagged again in `audit` and `qa` skills downstream.
- **FUNDAMENTALS banned-words list applies** to every copy file. Scan before writing, scan after.
- **One CTA per page.** Two-CTA pages fail intent.

---

## Sub-agent routing

Heavy reasoning steps go to Task tool sub-agents to keep orchestration context lean:

| Step | Tier | Why |
|------|------|-----|
| Phase 1 — reading existing canon (BRAND, ROADMAP, INDEX, STATUS, STRUCTURE) | fast | Pure extraction |
| Phase 2 — detecting features from `app/` routes and components | fast | Glob + name extraction |
| Phase 2 — writing CONTENT.md tables | reasoning | Judgment on categorisation |
| Phase 3 — proposing sitemap from features + comparisons | reasoning | Judgment on page set |
| Phase 4 — per-page briefs | reasoning | Highest-judgment step (story arc, audience state) |
| Phase 5 — per-page copy | reasoning | Claim-style headlines + banned-words enforcement |
| Phase 6 — media manifest | fast | Per-section type declaration |
| Phase 7 — layout sketches | reasoning | Structural intent per page |

Never the most expensive model. Reasoning tier (Sonnet) is the ceiling.

---

## Difference from related skills

- **`design-direction`** — locks brand identity (BRAND.md + DESIGN.md Overview + refusal list) ONCE at the start of a project. Marketing-brief locks the marketing-site execution plan ONCE at the end. Different file targets, different phase of the project.
- **`build-page`** *(new in v2.2)* — the per-page execution skill that reads marketing-brief's outputs. Invoked once per page (home, pricing, /features/x, /comparisons/y, etc.). Reads SITEMAP + the page's brief + copy + layout + MEDIA + CONTENT, runs layout-first / code-last 6-phase flow (architecture → hierarchy → assets → component selection → wire-up), delegates net-new component creation to `build-component` inline. Marketing-brief is the planning pass for the whole site; build-page is the execution pass per page.
- **`build-component`** — atomic. One component at a time. Called inline by build-page when a page section needs a net-new primitive. For one-off component requests (no page context), invoke directly.
- **`design-check`** — UI-write-time gate. Fires inside every build-component call and after build-page's wire-up.
- **`init-project`** — bootstraps the three-folder layout. Marketing-brief assumes init-project has already run (`agents/BRAND.md`, `agents/ROADMAP.md`, `agents/STATUS.md` all exist).
- **`audit`** — periodic consistency scan. Will catch drift between CONTENT.md and the actual nav / footer / feature pages after marketing-brief runs.

---

## Why it exists

Without this skill, marketing pages get written ad-hoc. Each page invents its own headlines, picks its own visual anchors, hardcodes feature names that the rest of the site doesn't agree with. Six pages in, the nav lists features the footer doesn't, the comparison page positions against a competitor the home page never mentions, and the screenshots show three different fake customers.

This skill is the single planning pass that prevents that drift. Every later marketing component reads from the same registry. The fictional customer is one brand, the feature list is one list, the headlines are one voice. `build-component` becomes mechanical execution rather than per-page improvisation.
