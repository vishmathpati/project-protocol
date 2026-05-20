# Phase 7 — Write outputs

The skill finishes by writing:

1. `agents/BRAND.md` — full, rich.
2. `agents/DESIGN.md` — Overview section + brand-specific DO NOT block. Token frontmatter is **not** touched.

Then surfaces the optional token-regeneration handoff to `init-project` Phase 4.

---

## Hard rules (do not violate)

1. **Never silently overwrite populated content.** Read each target file first. If a section contains user-written content (anything beyond `[VERIFY]` placeholders), show the diff to the user and ask before applying.
2. **Universal anti-patterns in DESIGN.md are sacred.** The DO NOT section's existing items (no indigo, no two-stop gradients, no emoji-as-icons, etc.) are never deleted. Only the bottom `[Add brand-specific anti-patterns here]` placeholder is replaced.
3. **Token frontmatter in DESIGN.md is read-only here.** This skill does not touch `colors:`, `typography:`, `spacing:`, `radius:`, `shadow:`, or `components:` in the YAML frontmatter.
4. **No invented details.** Every fact in BRAND.md must trace to the dump or a confirmed correction.

---

## `agents/BRAND.md` — full template after this skill

```markdown
# agents/BRAND.md — <Project Name>
> What every agent must know before touching this project visually.
> Locked via design-direction on <YYYY-MM-DD>.

## Product
- Name: <name>
- One sentence: <product description from dump>
- Surfaces: <web / app / email / docs / mobile — comma list>
- Monetisation: <free / subscription / per-event / etc>

## Audience
- Who it's for: <audience descriptor from Phase 3>
- Emotional state before our product: <fear/want sentence>
- What they already trust visually: <look-like sites, comma list>

## Brand
- Archetype (primary): <archetype + one-line meaning>
- Archetype (secondary, optional): <archetype or "none">
- Tone of voice: <derived from archetype + dump>
- Cultural anchor: <e.g., "Indian-casual, fashion-conscious urban">

## Reference tribe
- Look like: <site 1>, <site 2>, <site 3>
- Look deliberately unlike: <look-unlike site>

## Locked direction — <YYYY-MM-DD>
**<Direction name>** — <one-sentence personality>

- Palette intent: <words, not hex>
- Type pairing: <display + body>
- Reference layout to model after: <URL>
- Why this direction won: <one sentence linking back to diagnostic>

## Refusal list (brand-specific)
Universal AI-slop refusals (indigo, gradients, emoji-icons, etc.) live in `DESIGN.md` and `FUNDAMENTALS.md`. This list is brand-specific only.

- <refusal 1>
- <refusal 2>
- <refusal 3>
- <refusal 4 — if any>
- <refusal 5 — if any>

## Decisions log

| Date | Decision | Reason |
|------|----------|--------|
| <YYYY-MM-DD> | Locked direction "<name>" | <one-line reason> |
```

### Merging into an existing BRAND.md

- Read the existing file.
- If existing sections are populated, do a 3-way merge: existing content + new content + agent judgment on conflict.
- On conflict: keep the existing user-written prose, append the new structured fields below it under their canonical headings.
- Show the proposed merged file to the user before writing. Wait for "go" / "do it" / "approved".

---

## `agents/DESIGN.md` — Overview section

The template has:

```markdown
## Overview

A one-paragraph description of the visual identity — tone, era, references.
Example: "Editorial, warm, considered. Slightly formal. References: Stripe Press, A24, Notion editorial pages."

[VERIFY — fill from BRAND.md or user direction]
```

Replace the `[VERIFY — fill from BRAND.md or user direction]` line with one real paragraph derived from the locked direction. Sample:

```markdown
## Overview

Editorial, warm, photography-led. Premium without being austere. Calm enough to
support content-light Daily-seconds use, confident enough to express a Magician
brand. References — Stitch Fix and Vogue India for editorial type and
photography hierarchy; Aesop for restraint in sensory subject matter.
```

Keep everything else in the Overview section as-is.

### Merging into an existing populated Overview

If the existing Overview is not the `[VERIFY]` placeholder — show the proposed replacement and ask. Default is *replace only if the existing text reads as auto-generated boilerplate*; *append as a "v2 — <date>" paragraph below* if it reads as user-considered prose.

---

## `agents/DESIGN.md` — brand-specific DO NOT block

The template has, at the bottom of the DO NOT section:

```markdown
[Add brand-specific anti-patterns here — "no cream backgrounds", "no slab serif", etc.]
```

Replace that placeholder line with the locked refusal list, formatted as bullets:

```markdown
**Brand-specific anti-patterns (this project only):**

- No stock photographs of generic Western models — use real Indian people only.
- No clinical Pantone-software swatch UI — swatches must feel editorial, not lab-technical.
- No body-shaming copy. Ever.
- No traffic-light approve/reject patterns ("this works ✓ / this doesn't ✗").
- No competing with Myntra's information density — restraint is the differentiator.
```

The universal anti-patterns above this block (no indigo, no two-stop gradients, no emoji-icons, etc.) are **not edited**. Only the placeholder line is replaced.

### Merging into an existing brand-specific block

If the placeholder has already been replaced (the user added brand-specific items previously), show both lists side-by-side and ask: replace / merge / append. Default = merge (dedupe, preserve user wording).

---

## After writing — the optional handoff

Output:

```
✅ Direction locked: <name>
✅ Wrote agents/BRAND.md (full).
✅ Wrote agents/DESIGN.md Overview.
✅ Added <N> brand-specific anti-patterns to agents/DESIGN.md.

Token frontmatter (colors, typography, spacing, radius) was not regenerated.
The existing tokens may still be valid, or they may need to be re-derived from
the locked direction.

Want me to regenerate the token frontmatter now?
- "yes" → hand off to init-project Phase 4 path C (fresh generation) with the
  new BRAND.md as the brief. Existing custom tokens preserved where they fit.
- "no" → done. The next UI work will use the existing tokens; design-check
  will flag any token misses against the new Overview.
```

If the user says yes → invoke `init-project` Phase 4 path C ("Generate a completely fresh design system"). The sub-agent now has a far richer brief — BRAND.md is populated, the Overview reads coherently, the refusal list is concrete. Token generation accuracy goes up sharply.

If no → end skill cleanly. Update `cowork/WORKLOG.md` and `agents/WORKLOG.md` (per project-protocol session discipline) with a one-line entry: "design-direction: locked direction '<name>'".
