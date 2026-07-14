---
name: marketing-brief
description: Build or resume the brand-and-marketing content foundation for a brand-facing project. Use after Universal Foundation and Brand Foundation when offers, audiences, proof, conversion goals, sitemap, page intent, copy, or media requirements must be established. Runs adaptive Stage A before UI Research; Stage B splits into B1 (shared/site-wide copy locked after the site direction is approved) and B2 (each page's remaining copy finalized inside that page's Build Page conversation).
---

# Marketing Brief

One resumable marketing workflow with two stages. It is adaptive to the business and never assumes SaaS, English, pricing, competitors, or a large website.

## Read first

Read BRIEF, STRUCTURE, BRAND, WONT-DO, existing marketing canon, relevant product code/docs, and real proof sources. For Stage B, also read research outputs under `brain/research/` and DESIGN when they exist. Reuse universal and brand answers; ask only marketing gaps.

## Stage A — content foundation

Resolve applicable objectives and primary conversion; offers/services/products/features; audiences, problems, objections, and outcomes; differentiation and proof; pricing presentation when relevant; competitors only when useful; pages, page intent, primary CTA, and supporting CTA; content and media requirements.

Classify each sitemap entry as a **unique page or page family** from its communication job and repeatable content contract—not from a guessed visual layout. For a page family, list every member, choose one representative page for research/review, state the shared pattern requirement, and record genuine exceptions. Similar parentage alone does not create a family.

Write or update:

- `brain/marketing/CONTENT.md` — adaptive shared registry for offers, audiences, proof, messages, FAQs, and applicable business-specific material.
- `brain/marketing/SITEMAP.md` — page hierarchy, unique-page/page-family scope, representative page, shared requirement, exceptions, intent, primary conversion, and supporting CTA.
- `brain/marketing/briefs/<slug>.md` — page goal and content contract, not layout.
- `brain/marketing/copy/<page-or-family-id>.md` — initial draft copy where enough evidence exists, in the PAGE-COPY format. Stage A drafts are organized by content jobs, never by visual sections (hero/band/carousel and similar layout naming is forbidden before an approved direction).
- `brain/marketing/MEDIA.md` — source-agnostic asset requirements and their source route, permission/provenance, treatment, stage, and replacement gate. Marketing states what the media must communicate; Build Page later makes each approved slot implementation-ready.

Then UI Research may run for inspiration-dependent brand-facing UI. It is optional.

## Stage B — final content lock (split)

Stage B is split into B1 and B2. It supersedes the earlier single-pass lock; do not finalize all copy in one pass against the approved direction.

### B1 — lock shared/site-wide copy

Once the `## Approved Site Direction` block exists, read the research outputs under `brain/research/` and that exact block, then lock the copy that multiple pages reuse: global-shell copy, cross-page proof, shared CTAs, and anything reused site-wide. A submitted draft is not locked; do not finalize copy against an unapproved direction. Keep the submitted≠locked guard.

### B2 — finalize each page's copy inside its Build Page conversation

Each page's remaining copy is finalized **inside that page's active Build Page conversation**, in the PAGE-COPY format. Marketing still owns the words and their source traceability; the human may rewrite anything and human edits win; Build Page implements only finalized copy. Do not choose page composition or component layout; Build Page owns that conversation.

## Content integrity

- One primary conversion per page; a secondary supporting CTA is allowed.
- Every headline must do meaningful work, but not every phrase needs a citation.
- Testimonials and proof must be real and attributable. Never fabricate them.
- Fictional/demo brands are allowed only inside clearly labeled software screenshot data, never as customers, testimonials, or proof.
- Legal content is an inventory/requirement unless supplied or reviewed by an appropriate owner.
- Preserve source traceability for claims, proof, media rights, and customer language.

## Ownership

Marketing owns meaning, message, page intent, copy, and media requirements. It does not write DESIGN, research, `layouts/`, page composition, components, routes, or code. Build Page is the primary consumer; Build Component consumes only genuinely missing component requirements.

Use the shipped CONTENT, SITEMAP, PAGE-BRIEF, PAGE-COPY, and MEDIA templates. When writing marketing files, preserve each template's format stamp line. Preserve useful existing project marketing canon, but do not preserve unsafe placeholder-proof rules from older plugin versions.
