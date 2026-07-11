# Phase 4 — Reference moodboard

Propose 3–5 real sites that satisfy the locked diagnostic. The user reads these to anchor taste before seeing the 3 named directions in Phase 5.

---

## Purpose — read this before doing anything else

The moodboard is a **trust-ceiling check, not a template.** It proves the audience can handle this level of design ambition — it does NOT define what kind of ambition this brand should reach for. The brand's distinctive asset must sit OUTSIDE pure homage to these sites.

- **What the moodboard IS:** permission to be ambitious. The audience already accepts this much design rigour, so we know we won't lose them by reaching.
- **What the moodboard is NOT:** a menu of styles to remix or pick from. If Phase 5 treats these sites as ingredients, the brand ends up generic.

### Hard rule — no percentage-mix directions

Do not propose directions in Phase 5 that read as "mostly site X + a bit of site Y". If a Phase 5 direction can be summarized as a percentage mix of moodboard sites, it has failed. The moodboard sets a *trust ceiling*; directions must invent new distinctive territory under that ceiling.

---

## What to output

For each reference:

- **Site name** — bold.
- **URL** — full URL the user can open.
- **One-sentence why-it-fits** — name the axis it satisfies. ("Calm typography + zero accent colour, hits the daily-hours + Sage axes.")

Plain prose list. No screenshots required — if `WebSearch` or live fetching is available, include one descriptive line per site about what they'll see. If not, the URL plus the why-it-fits line is enough.

---

## Heuristic mapping — axes to candidate sites

The agent picks 3–5 from this candidate pool based on the locked diagnostic. Prefer real, current sites the user can open today.

### By archetype

| Archetype | Strong candidates |
|---|---|
| Sage | stripe.com, linear.app, notion.so, mercury.com, vercel.com |
| Magician | apple.com, tesla.com, arc.net, framer.com |
| Caregiver | airbnb.com, headspace.com, calm.com, oscar.com |
| Rebel | liquiddeath.com, patagonia.com, off—white.com, mschf.com |
| Creator | figma.com, adobe.com, framer.com, dribbble.com |
| Hero | nike.com, salesforce.com, asana.com |
| Explorer | airbnb.com, hipcamp.com, rei.com |
| Innocent | dove.com, mailchimp.com, oatly.com |
| Lover | aesop.com, lelabofragrances.com, chanel.com |
| Jester | mailchimp.com, slack.com, duolingo.com |
| Ruler | rolex.com, bloomberg.com, the-economist.com |
| Everyman | target.com, ikea.com, costco.com |

### By cultural anchor

| Anchor | Strong candidates |
|---|---|
| Global-tech | stripe.com, linear.app, vercel.com, dub.co |
| Indian-formal | mercury.com (style ref), groww.in, smallcase.com |
| Indian-casual | swiggy.com, zomato.com, cred.club |
| Indian-celebration | wedmegood.com (for content), nykaa.com, fabindia.com |
| Japanese-minimal | studio-anatomy.com, monocle.com, muji.com |
| Western-consumer | airbnb.com, allbirds.com, glossier.com |

### By information density

| Density | Strong candidates |
|---|---|
| Data-dense | linear.app, bloomberg.com, github.com, stripe.com/dashboard (in product screenshots) |
| Content-light | apple.com, stripe.com (marketing), aesop.com, dub.co |
| Mixed | vercel.com, notion.so, framer.com |

---

## Selection rules

- **3 to 5 sites.** Below 3 the user can't triangulate; above 5 they overwhelm.
- **At least one Indian / regional anchor** if cultural anchor is Indian-anything.
- **At least one site already named by the user** (in dump or correction) if they named any.
- **No duplicates with the look-unlike incumbent.** If the user said "not Stripe", don't include Stripe even if it matches axes.
- **Open-able sites only.** No now-defunct portfolios or links that need login.

---

## Sample output (matching a locked diagnostic: high trust + daily-seconds + content-light + Indian-casual + Magician + look-unlike Myntra)

```
References — 3 to 5 sites your audience already trusts. These prove the
audience accepts design-conscious work; they're your trust ceiling, not your
template. In the next step I'll propose 3 directions, and at least one will
sit OUTSIDE this envelope — because copying these sites means you can't own
anything distinctive.

  • Stitch Fix (stitchfix.com) — editorial, photography-led, Magician archetype
    expressed through transformation imagery. Content-light layout, premium feel.
  • Whering (whering.com) — direct competitor by category, but executed with the
    confidence and restraint of a Lover/Magician brand. The visual benchmark for
    "fashion app that's not Myntra".
  • Aesop (aesop.com) — for the Lover-archetype influence in typography and
    space. Reference for how to handle sensory subject matter without going
    overwrought.
  • Nykaa (nykaa.com) — Indian-context fashion/beauty execution. Look at how
    they balance product density with brand chrome.
  • Vogue India (vogue.in) — editorial Indian fashion. Reference for type
    hierarchy and photography treatment in the Indian market.

Read these to calibrate the ceiling, then we'll go to directions.
```

---

## Hard rules

- **Do not invent URLs.** Every URL must be a real site you're confident exists. If unsure, drop it.
- **Do not link to design-system documentation pages** (e.g., material.io, polaris.shopify.com). Link to the actual brand surface — that's what's being benchmarked.
- **One-line why each.** Two lines max if needed. Not paragraphs.

---

## Handoff to calibrate (once, before Phase 5)

After presenting the moodboard, make an explicit `Skill("calibrate")` call. `calibrate` now runs a **two-round** sweep→concept→teardown pass, not a single capture:

- **Round 1 (sweep)** — discovers the niche's field and groups it into named concepts, written to `brain/research/concepts.md`. You pick or blend one concept.
- **Round 2 (deep teardown)** — tears down the chosen concept's best real examples, written to `brain/research/teardowns/`.
- It then folds both rounds' returns into `brain/moodboard/notes.md` (per-site observations Phase 5 reads) and appends a FOLLOW / DEVIATE / REFUSE conventions audit to `brain/DESIGN.md`.

It hands back with "resume design-direction at Phase 5." Call it **exactly once** — Phase 5 consumes its outputs but must never re-invoke `calibrate` (that would loop). Skip path: if the user says "skip calibrate," proceed straight to Phase 5 with the moodboard as-is.

---

Phase 5 enforces this with a "mandated departure" rule — see `phase-5-three-directions.md`.
