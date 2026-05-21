# Phase 3 — Plain-English diagnostic + one confirmation pass

Turn the locked axes object from Phase 2 into prose the user can read and correct in plain language. Do not show axis labels. One confirmation pass — no loop.

---

## The prose template

```
Reading the product:

This serves <audience descriptor — derived from dump>. They are <emotional state about the
problem — derived from trust temperature + archetype>. The product is opened
<frequency phrasing> and the content is mostly <density phrasing>.

If your customer loses confidence in this product, what it costs them is
<trust-stakes phrasing> — which means the brand <stakes-implication sentence>.

It belongs to the <cultural anchor> visual vocabulary.

The brand sits closest to the <archetype> archetype — <one-sentence archetype meaning>.
<Optional second sentence on secondary archetype if present.>

It should feel like a sibling to <look-like 1>, <look-like 2>, and <look-like 3>.
It should deliberately not look like <look-unlike>.

The category it competes in is <category-maturity phrasing>, which means
<maturity-implication sentence — conform 80/break 20, or conform 20/break 80>.

The thing this brand should be remembered for — its ownable signature — is
<distinctive asset 1>[, and <distinctive asset 2>]. Everything else can flex; these stay.

It probably should never:
  - <refusal 1>
  - <refusal 2>
  - <refusal 3>

Does this read true? Push back on anything that's off — say it in plain language
("stakes are higher, this is health not just time"; "skip the Indian anchor, this is global";
"the distinctive asset isn't the color, it's the character"),
and I'll adjust. One pass, then we proceed to references and directions.
```

---

## Phrasing conventions

### Audience descriptor

Not "users" or "customers" — describe an actual person if the dump gave you one.

- "design-conscious B2B marketing teams at modern SaaS companies"
- "Indian wedding photographers who are sick of WeTransfer and Google Drive"
- NOT "users who need to share photos" (generic)

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

### Trust-stakes phrasing

Always two parts: what failure costs them, then the implication for the brand.

| Stakes | Cost sentence | Implication sentence |
|---|---|---|
| Money | "real money — payroll missed, fees lost, capital exposed" | "needs to read as precise and accountable on every screen, not just the hero" |
| Health | "their wellbeing or someone they're caring for" | "carries a clinical responsibility that has to show up in restraint and clarity, not warmth alone" |
| Time-Embarrassment | "their reputation, their hours, and how they look in front of their own customers" | "has to feel competent and quietly confident — never amateurish, never loud" |
| Boredom | "a few minutes of attention, no more" | "has freedom to be expressive and personal — restraint here would feel like wasted air" |

Example sentence:
> "If your customer loses confidence in this product, what it costs them is real money — payroll missed, fees lost, capital exposed — which means the brand needs to read as precise and accountable on every screen, not just the hero."

### Cultural anchor phrasing

Plain-language sibling of the axis value:

- global-tech → "the global B2B tech vocabulary — Inter and Geist, monochrome with one accent"
- indian-formal → "the calm, restrained register that Indian banking and legal brands use"
- indian-casual → "the warm, expressive Indian consumer register"
- indian-celebration → "the jewel-tone, festive register — gold, peacock teal, deep red"
- japanese-minimal → "the Japanese-minimal register — aggressive whitespace, tight grid"
- western-consumer → "the bright Western-consumer register — curves, real photography, saturated colour"

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

### Category-maturity phrasing

Always two parts: name the category state, then the conform/break ratio.

- **Code-locked** → "a category where every credible player looks broadly the same — banking, payments, B2B infrastructure, healthcare, regulated work — and audiences read deviation as risk. The brand should conform on about 80% of category codes (layout, restraint, palette discipline) and break decisively on the remaining 20% — one ownable move, not ten."
- **Code-fluid** → "a category with no enforced visual language — creator tools, lifestyle, food, indie consumer — where audiences expect difference and reward it. The brand should conform on only about 20% (basic usability conventions, scanability) and break on the remaining 80%. Playing it safe here is the actual failure mode."

If trust stakes are Money or Health, double-check the maturity is code-locked and the implication sentence reads that way. Mismatches (e.g., Money + code-fluid) are usually a misread — flag for confirmation.

Optional reference line (use sparingly, only when the user seems tempted to break codes in a code-locked category): "Jaguar 2024 is the cautionary case here — they broke codes hard in a code-locked premium-auto category and lost most of their sales. The freedom you have is real but bounded."

### Distinctive-asset phrasing

Always concrete, always describable in one sentence per asset. Frame as "the thing this brand should be remembered for."

- "Tiffany robin's-egg blue, applied to every surface that touches the customer"
- "a recurring illustrated character — Freddie at Mailchimp, the duck at Cluely — that shows up on empty states and 404s"
- "a heavy-metal-meets-mineral-water typeface paired with the tallboy can silhouette"
- "copper-on-black as the only palette — no second accent, no gradient"

If only one strong asset is locked, name only one. If two, name both — but stop at two. More than two and none of them are distinctive.

**If no distinctive asset surfaced from the dump**, the prose should say so directly:
> "There's no distinctive asset locked yet — the dump didn't surface a colour, character, or shape this brand wants to own. That's the most important gap to close before we move to directions. My suggestion is <propose one based on archetype + cultural anchor + tribe>. Push back if that's wrong."

This is the one place in the diagnostic where the agent volunteers a concrete proposal instead of just synthesising the dump.

### Refusals

Phrase as a "never" — concrete, scannable. Universal anti-patterns from FUNDAMENTALS.md (no indigo, no two-stop gradients, no emoji-icons) are NOT repeated here — they're already enforced. This list is brand-specific only.

---

## Correction merging

The user replies in plain language. Common correction shapes:

- *"Trust is higher than that."* → bump trust temperature one notch up (Medium → High → Max).
- *"Stakes are health, not just time."* → re-extract trust_stakes; rewrite the stakes sentence + implication.
- *"My users aren't anxious, they're proud."* → adjust emotional state sentence; may shift archetype Sage → Magician/Hero.
- *"Not Indian, this is global."* → switch cultural anchor to global-tech.
- *"I don't want to look like Stripe."* → move Stripe from look-like to look-unlike, find a new look-like.
- *"This category isn't locked — fintech is changing."* → re-evaluate category_maturity; if user is right, flip to code-fluid and revise the conform/break ratio. If user is wrong (e.g., regulated payments is still code-locked despite vibes), hold the line gently: *"the audience still reads deviation as risk in payments — the change is in tone, not in core codes. Want to test that in Phase 5?"*
- *"The distinctive asset isn't the color, it's the character."* → swap asset list; keep at most two.
- *"Add a refusal: no rainbow gradients."* → append refusal.

Apply the correction silently. Re-summarise the diagnostic in one short paragraph (not the full prose again) to confirm what changed. Do NOT re-show the full template.

```
Adjusted: stakes → health (not time), archetype → Caregiver (not Sage), look-like swapped Stripe
for Headspace, distinctive asset reframed as "the slow breathing-circle on every loading state"
instead of the colour. Locked. Moving to references.
```

If the user makes no correction (or says "looks good", "yes", "lock it") — say "Locked. Moving to references." and proceed.

---

## Hard rules

- **One pass.** Do not enter a multi-round correction loop. If after one correction the user is still adjusting, ask: *"Want to lock what we have and refine later, or keep iterating? My recommendation is lock — directions in Phase 5 will surface any remaining mismatch faster than re-debating axes here."* Default to lock.
- **Do not surface axis labels.** Never say "trust temperature: high" or "category maturity: code-locked". Say what each means in prose.
- **Never invent details that aren't in the dump.** If the dump didn't specify audience age / gender / income, don't guess. Phrase audience by role + relationship to the problem instead.
- **Distinctive asset is the one exception** — if the dump didn't name one, the agent proposes one and asks for confirmation, rather than leaving the slot empty. A brand with no distinctive asset cannot move to Phase 4.
- **Stakes + maturity sanity check.** Money/Health stakes paired with code-fluid maturity is almost always wrong; flag and confirm before locking. Boredom stakes paired with code-locked maturity is also almost always wrong; flag and confirm.
