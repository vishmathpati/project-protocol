# Phase 1 — Intake

Read existing canon. Surface what's already known. Ask only for missing pieces. The goal of this phase is a one-page synthesis the user confirms before any marketing file is written.

This phase exists because by the time `marketing-brief` runs, the project has been live for weeks — `agents/BRAND.md`, `agents/ROADMAP.md`, `agents/STATUS.md`, `agents/docs/INDEX.md` are populated. Re-asking the user for audience, features, or surface mix is wasteful. The intake reads first, then asks for gaps only.

---

## Files to read (in order)

Read each via `Read` tool. If absent, note the gap; do not stop.

1. **`agents/BRAND.md`**
   - Pull: audience descriptor, emotional state, archetype, reference tribe, refusal list.
   - These shape voice and which competitors / aesthetics to position against.

2. **`agents/ROADMAP.md`**
   - Pull: locked features list (shipped + in-flight). This becomes the seed for CONTENT.md's FEATURES table.
   - If a feature is shipped but marked "draft" in the roadmap, treat as shipped for marketing purposes — ask the user to confirm.

3. **`agents/docs/INDEX.md`**
   - Pull: the actual feature-to-code map. Useful for detecting features the roadmap forgot to add (and vice versa).

4. **`agents/STATUS.md`**
   - Pull: what's live now vs. in flight. Marketing claims must match reality — if a feature is "in flight", it doesn't get a feature page yet; mention it in the changelog at most.

5. **`agents/STRUCTURE.md`** (or `agents/docs/INDEX.md` if STRUCTURE.md absent)
   - Pull: declared surfaces.
   - Also used for the auto-skip check from the parent SKILL.md — if there's no `marketing` / `landing` / `web` surface, refuse and exit.

6. **`agents/BRIEF.md`**
   - Pull: locked decisions about monetisation, pricing model, primary distribution channel.
   - Pricing model decides whether `pricing` is a real page or a "talk to sales" stub.

7. **Root `README.md`**
   - Pull: tagline, one-line product description. Useful for hero-headline seed.

Do this via a `Task` sub-agent at the fast tier — pure extraction, no judgment.

---

## Synthesis — one-page summary

After reading, produce a single synthesised summary in this shape:

```
marketing-brief — intake summary

PRODUCT
- Name: <from BRAND.md or README>
- One sentence: <from README tagline or BRAND.md product line>
- Surfaces declared: <list from STRUCTURE.md>
- Monetisation: <from BRIEF.md>

AUDIENCE
- Primary: <from BRAND.md — audience descriptor>
- Emotional state on entry: <from BRAND.md — fear/want sentence>
- Reference tribe (sites they trust): <comma list>
- Look deliberately unlike: <comma list>

FEATURES (from ROADMAP + INDEX)
- Shipped: <feature 1>, <feature 2>, <feature 3>, …
- In flight (will NOT get feature pages yet): <list or "none">
- Possibly missing from roadmap (found in code but not listed): <list or "none">

COMPETITORS / POSITIONING
- From BRAND.md refusal list: <competitors to look unlike>
- From BRIEF.md: <any explicit "vs X" positioning>

SHIPPED FEATURES BY AUDIENCE
- <audience A>: <feature list>
- <audience B>: <feature list>

GAPS — I need your input on
- <gap 1, if any>
- <gap 2, if any>
```

The "GAPS" section is the only place the user has to answer questions. Common gaps:

- **No declared audience segments** beyond a single primary. Ask: are there 2–3 distinct audience cuts the marketing site should speak to separately, or one unified audience?
- **No locked competitor list** in BRAND.md refusals. Ask: name 1–3 specific competitors you want comparison pages against (or "none" if not running comparison pages).
- **Pricing model unclear** in BRIEF.md. Ask: free / per-seat subscription / per-event / usage-based / talk-to-sales / agency-only.
- **Fictional customer not yet locked.** Defer to Phase 6 — don't ask here.
- **Testimonials availability** — do you have real customer quotes, or are we writing placeholder testimonials with the fictional customer brand?
- **Blog / changelog presence** — does the site have a blog? A changelog? Both? Neither?

---

## Confirmation gate

Before exiting Phase 1, surface the synthesised summary back and ask one explicit question:

> Does this read true? Anything I should add, correct, or drop before I build out CONTENT.md?

Wait for an explicit response. Accept corrections ("no, the primary audience is X not Y", "drop comparison pages — we don't position against anyone", "add a feature I missed — it's called …").

Update the synthesised summary in-memory with corrections. Lock and proceed.

**One pass only.** Do not loop on the synthesis. After the user confirms (or corrects once and confirms), move to Phase 2.

---

## What goes forward to Phase 2

The corrected synthesis. Phase 2 consumes:

- Confirmed features list (becomes FEATURES table seed).
- Confirmed audience segments (becomes AUDIENCES table seed).
- Confirmed competitor list (becomes COMPARISONS table seed).
- Pricing model (informs pricing-page intent in Phase 3 sitemap).
- Blog / changelog presence (informs sitemap).
- Testimonials availability (real vs placeholder — informs TESTIMONIALS table in CONTENT and the fictional-customer policy in Phase 6).

---

## Hard rules

- **Read first, ask second.** If `agents/BRAND.md` has the audience, do not re-ask.
- **Do not invent a feature.** If it's not in ROADMAP, INDEX, or live code, it doesn't go in CONTENT later. Flag it; don't add it.
- **Do not invent a competitor.** If the user hasn't named one, comparison pages are skipped in Phase 3.
- **One pass on synthesis.** No looping. Correct, confirm, lock, advance.
- **Surface gaps explicitly.** Don't paper over missing audience / pricing / competitor info — ask plainly.
