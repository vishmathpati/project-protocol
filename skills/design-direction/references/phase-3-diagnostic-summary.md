# Phase 3 — Plain-English diagnostic + one confirmation pass

Turn the locked axes object from Phase 2 into prose the user can read and correct in plain language. Do not show axis labels. One confirmation pass — no loop.

---

## The prose template

```
Reading the product:

This serves <audience descriptor — derived from dump>. They are <emotional state about the
problem — derived from trust temperature + archetype>. The product is opened
<frequency phrasing> and the content is mostly <density phrasing>.

It belongs to the <cultural anchor> visual vocabulary.

The brand sits closest to the <archetype> archetype — <one-sentence archetype meaning>.
<Optional second sentence on secondary archetype if present.>

It should feel like a sibling to <look-like 1>, <look-like 2>, and <look-like 3>.
It should deliberately not look like <look-unlike>.

It probably should never:
  - <refusal 1>
  - <refusal 2>
  - <refusal 3>

Does this read true? Push back on anything that's off — say it in plain language
("trust is higher, my users are anxious"; "skip the Indian anchor, this is global"),
and I'll adjust. One pass, then we proceed to references and directions.
```

---

## Phrasing conventions

### Audience descriptor

Not "users" or "customers" — describe an actual person if the dump gave you one.

- ✅ "design-conscious B2B marketing teams at modern SaaS companies"
- ✅ "Indian wedding photographers who are sick of WeTransfer and Google Drive"
- ❌ "users who need to share photos" (generic)

### Emotional state about the problem

Lead with the *fear* or *want* the user has before they find this product. This is the single biggest signal for visual temperature.

- High trust + anxious problem → "anxious, in a hurry, and need to be made to feel calm"
- Low trust + light problem → "bored, half-attentive, and need to be made to feel something"
- High trust + competence problem → "competent, time-constrained, and need the product to get out of their way"

### Frequency phrasing

- daily-hours → "lived in for hours at a time"
- daily-seconds → "opened many times a day for seconds at a time"
- weekly → "opened a few times a week"
- occasional → "opened once a quarter at most"
- one-time → "used once and never again"

### Density phrasing

- data-dense → "tables, numbers, and small text — information-heavy"
- content-light → "photographs and large type — image-heavy"
- mixed → "image-heavy marketing leading into information-heavy product"

### Archetype meaning sentences (one-liners)

| Archetype | Meaning sentence |
|---|---|
| Sage | the trustworthy guide who explains and clarifies |
| Magician | the brand that transforms how the user feels about themselves |
| Caregiver | the warm protector who looks after the user |
| Rebel | the sharp outsider who fights the status quo |
| Creator | the studio for makers |
| Hero | the brand that helps the user win |
| Explorer | the brand that helps the user discover |
| Innocent | the brand that keeps things plain and optimistic |
| Lover | the brand that elevates beauty and sensory experience |
| Jester | the brand that brings lightness and wit |
| Ruler | the brand of authority and order |
| Everyman | the brand that's one of the user, not above them |

### Refusals

Phrase as a "never" — concrete, scannable. Universal anti-patterns from FUNDAMENTALS.md (no indigo, no two-stop gradients, no emoji-icons) are NOT repeated here — they're already enforced. This list is brand-specific only.

---

## Correction merging

The user replies in plain language. Common correction shapes:

- *"Trust is higher than that."* → bump trust one notch up (Medium → High → Max).
- *"My users aren't anxious, they're proud."* → adjust emotional state sentence; may shift archetype Sage → Magician/Hero.
- *"Not Indian, this is global."* → switch cultural anchor to global-tech.
- *"I don't want to look like Stripe."* → move Stripe from look-like to look-unlike, find a new look-like.
- *"Add a refusal: no rainbow gradients."* → append refusal.

Apply the correction silently. Re-summarise the diagnostic in one short paragraph (not the full prose again) to confirm what changed. Do NOT re-show the full template.

```
Adjusted: trust → max, archetype → Sage (not Magician), look-like swapped Stripe for Mercury.
Locked. Moving to references.
```

If the user makes no correction (or says "looks good", "yes", "lock it") — say "Locked. Moving to references." and proceed.

---

## Hard rules

- **One pass.** Do not enter a multi-round correction loop. If after one correction the user is still adjusting, ask: *"Want to lock what we have and refine later, or keep iterating? My recommendation is lock — directions in Phase 5 will surface any remaining mismatch faster than re-debating axes here."* Default to lock.
- **Do not surface axis labels.** Never say "trust temperature: high". Say what that means in prose.
- **Never invent details that aren't in the dump.** If the dump didn't specify audience age / gender / income, don't guess. Phrase audience by role + relationship to the problem instead.
