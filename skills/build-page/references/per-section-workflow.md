# Per-section workflow

After the page plan is locked (BRIEF block written, WORKLOG line appended), the skill works through sections sequentially. This file documents the conversation shape for one section, including external-reference adoption.

## Entering a section

Read the section's material from canon. For marketing pages:
- The relevant block from `agents/marketing/copy/<slug>.md` (headlines, body, CTAs).
- The corresponding MEDIA.md entry (visual anchor type).
- The corresponding row in `agents/marketing/layouts/<slug>.md` (block-level wireframe intent).
- The CONTENT.md rows it references (FEATURES, FAQS, TESTIMONIALS as applicable).

For dashboard pages:
- The relevant slice of the page brief (`agents/specs/<slug>.md` or the relevant ROADMAP row).
- Existing dashboard primitives the section might compose (PageHeader, KpiStrip, ChartCard, DataTable, EmptyState, ErrorState, Skeleton).

Then surface the section to the user, one paragraph:

```
§<n> — <section name>

Content (from copy/<slug>.md or brief):
  Headline: "<exact copy>"
  Body: "<exact copy>"
  CTA: "<label>" → <href>

Visual anchor (MEDIA.md): <type — e.g. portrait mockup, screenshot, text-only>
Intent (briefs/<slug>.md): <what this section is for>

Existing components in <tier-folder> that could fit:
  - <ComponentName> @ <path>  — <one-line about why it fits>
  - <ComponentName> @ <path>  — <one-line about why it fits>

Existing primitives (components/ui/, components/dashboard/) that could compose:
  - <name>, <name>, <name>

Existing shadcn primitives if not already installed: <list>
  (drop a URL or paste source if you want me to evaluate an external reference)

Strategies on the table:
  A. Reuse <ComponentName>
  B. Adapt <ComponentName> with <delta>
  C. Compose <PrimitiveA> + <PrimitiveB>
  D. Build new via build-component (with intent spec)
  E. Adopt an external reference (drop URL / paste / screenshot)

Which one?
```

Wait for the user's pick. They can also iterate — *"reuse, but with the image on the right not left"*, *"compose, plus a small accent strip below"*. Apply the iteration, re-surface the strategies if needed, ask again.

## When the user picks Reuse or Compose

Confirm the component path(s). Write the WORKLOG line:
```
[HH:MM] decided: §<n> strategy — reuse <ComponentName> @ <path>
```
or
```
[HH:MM] decided: §<n> strategy — compose <PrimitiveA> + <PrimitiveB>
```

No `build-component` call needed. Move to the next section.

## When the user picks Adapt

Adaptation means editing an existing component to add a variant, prop, or behavior. This goes through `build-component` because the cross-tier and token rules still apply.

1. Confirm the delta: *"Adapting <ComponentName> — add `numbered` variant that prepends a step number above the title. Other variants untouched. Confirm?"*
2. Invoke `build-component` explicitly:
   ```
   Skill("build-component")
   ```
   Pass sub-mode "extend existing primitive". `build-component` runs its own preview-and-approve flow inside its Phase 5, gates through `design-check` (explicit Skill call within build-component), returns control.
3. Write WORKLOG line:
   ```
   [HH:MM] decided: §<n> built — adapted <ComponentName> (added <delta>)
   ```
4. Move to the next section.

## When the user picks Build new

1. Confirm the intent: *"Building new <ComponentName> for §<n> — a <one-sentence shape>. Tier: <marketing | app | generic>. Composes <existing primitives>. Confirm?"*
2. Invoke `build-component` explicitly:
   ```
   Skill("build-component")
   ```
   Pass the intent spec. `build-component` runs its full 5-phase flow inside its own conversation:
   - Phase 1: structure detection (skipped if STRUCTURE.md exists, which it should).
   - Phase 2: intake + tier (parent-skill provides; no question to user).
   - Phase 3: reuse scan (already done by build-page, but build-component re-runs in its scope — that's fine, it's fast).
   - Phase 4: data shape + location.
   - Phase 5: preview + write, with its own approval gate.
   - `design-check` is explicitly invoked post-write (via `Skill("design-check")` inside build-component section 5.5).
3. `build-component` returns the file path.
4. Write WORKLOG line:
   ```
   [HH:MM] decided: §<n> built — new <ComponentName> @ <path>
   ```
5. Move to the next section.

**Sequential, not parallel.** Even if two sections are independent, the user gets one focused `build-component` conversation per net-new component. Bundling them produces the page-wide code drop pathology this skill exists to prevent.

## External reference adoption

When the user says *"here's a Stripe hero I like — https://..."*, *"use this Aceternity block — [paste]"*, *"build it like this screenshot — [image]"*:

### 1. Fetch / parse

- **URL** — use `WebFetch` first. If the page is client-rendered (the response looks like a shell with no real content), escalate to the Chrome MCP per the system rules on escalating unhelpful WebFetch results.
- **Pasted code / JSX / HTML** — read it directly.
- **Screenshot** — examine the image (multimodal read).

### 2. Identify the visual pattern

In one paragraph, describe what the reference IS:
- Layout structure (e.g. *"two-column hero, headline + subhead + dual CTA on left, full-bleed product screenshot on right, contained 1200px max-width, vertical padding ~96px top / 80px bottom"*).
- Typography choices (display weight, body weight, scale jumps).
- Color usage (paper color, ink color, accent color count, accent placement).
- Motion / interaction (any hover states, scroll-linked, sticky).

This paragraph is what you cross-check against canon.

### 3. Cross-check against DESIGN.md

For every value in the reference, ask: *does our DESIGN.md have a token for this?*

Build a quick table in chat:

```
Reference value           → Our token (or "no match")
#0a2540 (paper)           → var(--paper)  [match]
#425466 (ink)             → var(--ink)    [match]
#635bff (accent)          → no match — closest is var(--accent-primary) (#5f4ad4)
Inter 600 (display)       → var(--font-display) (Source Serif 4 600)  [voice mismatch]
8px / 16px / 32px spacing → var(--space-*) values  [match]
```

Any "no match" or "voice mismatch" row is a friction point. Surface them.

### 4. Cross-check against BRAND.md

Read the archetype, tribe, tempo, and refusal list from BRAND.md. Ask:
- Does the reference's voice fit our archetype? (A Stripe hero is *Magician/Sage*. If our archetype is *Caregiver*, the reference is too clinical.)
- Does the reference's tempo match our tempo axis? (A kinetic scroll-linked hero on a `tempo: slow/editorial` brand is wrong.)
- Does the reference violate our refusal list? (If our refusal list says "no two-stop trust gradients" and the reference is a two-stop gradient, that's a hard no.)

Surface fit / mismatch in one paragraph.

### 5. Cross-check against the section's content

The reference is a visual pattern; our section has specific copy. Ask:
- Does the headline length fit the reference's headline slot? (A 4-word headline in a 12-word slot looks lonely.)
- Does the body length fit? (A 60-word body in a 15-word slot will overflow.)
- Does the CTA count match? (Reference has one CTA, our copy has two — pick which to drop or change the reference.)

### 6. Verdict

One of three:

- **Adopt as-is** — every value maps cleanly, voice fits, content fits. Rare for high-distinction brands; common when the reference is itself well-tokenized (a shadcn block, a Tailwind UI snippet).
- **Adapt** — most values map, one or two need substitution (e.g. swap the reference's accent for our `var(--accent-primary)`, swap the display font, simplify the gradient). Most common outcome.
- **Reject** — voice mismatch is unfixable, or violates refusal list, or the layout doesn't serve the content. Explain why. Propose an alternative — usually "let's compose our own from the existing primitives with the layout intent from the reference".

Write the verdict to chat. Wait for the user to accept the verdict or push back.

### 7. Execute

If adopt or adapt: invoke `build-component`'s `adopt-external` sub-mode explicitly:
```
Skill("build-component")
```
Pass:
- The source (URL / pasted code / image path)
- The normalization table from step 3
- Any user-confirmed substitutions ("yes, use our accent not theirs")
- The target location (per STRUCTURE.md)

`build-component` runs its adopt-external sub-mode, writes the component, `design-check` fires.

Write WORKLOG line:
```
[HH:MM] decided: §<n> adopted external from <source> → <component path>
```

If reject: append to WORKLOG:
```
[HH:MM] tried_failed: §<n> external <source> — <reason>
```
Then return to the strategy menu and let the user pick again.

## When all sections are decided + built

Confirm in chat:
```
All <N> sections have real component paths:
  §1 <name> → <component path>  [<strategy>]
  §2 <name> → <component path>  [<strategy>]
  …

Ready to wire the page file?
```

Wait for "yes". Then proceed to wire-up (covered in SKILL.md step 10).

## What does NOT happen during per-section work

- **Don't propose copy changes.** Copy is locked in `copy/<slug>.md`. If the user wants to change copy mid-build, that's a separate edit to canon, not a build-page concern. Halt: *"Copy is canon. Update `agents/marketing/copy/<slug>.md` first, then resume."*
- **Don't propose CONTENT.md changes.** Same rule. CONTENT changes go through a separate update to canon.
- **Don't propose new DESIGN.md tokens.** If the section genuinely needs a token we don't have, that's a `design-check` Step 4 conversation (and it'll fire automatically). Don't anticipate by editing DESIGN.md yourself.
- **Don't bundle two sections into one `build-component` call.** One component per call. Even if two sections both need a hero-shaped thing, build them separately — they probably differ in ways that matter.
- **Don't skip the existing-component scan.** Reuse-bias is real, especially for dashboard tier. If you're proposing "build new" for a dashboard section, the user should push back, and you should welcome the push-back.
