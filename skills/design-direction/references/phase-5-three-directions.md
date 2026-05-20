# Phase 5 — Three named directions

Propose exactly 3 directions. They must be **meaningfully different** — sit at different points on the remaining design space. Not 3 flavours of the same thing.

---

## Shape of each direction

```
Direction <N> — <evocative name>

  Personality: <one sentence on what this feels like>.
  Palette intent: <in words, no hex codes>.
  Type pairing: <display family + body family, both named>.
  Reference: <one URL to model layout after>.
  Why this fits: <one or two sentences linking back to the locked diagnostic>.
```

Use evocative names, not technical labels:

- ✅ "Editorial cream", "Color lab", "Warm modern Indian"
- ❌ "Light mode", "Dark mode", "Minimalist option"

---

## What "meaningfully different" means

The 3 directions must span the viable design space defined by the locked axes. Practical rules:

1. **At least 2 different palette intents.** Cream vs ink vs jewel-tones is different. Three flavours of monochrome is not.
2. **At least 2 different type personalities.** Editorial-serif vs geometric-sans vs grotesque-condensed is different. Three sans-serifs is not.
3. **At least 2 different layout densities.** Generous-whitespace vs compact-grid is different. Three medium layouts is not.
4. **All 3 satisfy the locked refusals.** If a direction would require violating a refusal, it's not viable — drop it.

If only 1 or 2 viable directions exist after applying the locked refusals → present those and explicitly say "the diagnostic only admits 2 viable directions; here they are." Don't pad with a weak third.

---

## Palette intent — how to describe in words

Never use hex codes at this stage. The user is picking *intent*, not exact values. Hex codes happen in Phase 4 of init-project (token generation).

Good palette-intent descriptions:

- "Warm cream and deep ink, with one terracotta accent that appears once per fold."
- "Pure white surfaces, full-bleed photography, no chrome colour at all."
- "Dark navy ground with a single warm gold accent — institutional feel."
- "Soft sage green and warm grays, no harsh blacks, modern Caregiver mood."

Bad palette-intent descriptions:

- "Use #F5EFE4, #1A1A1A, and #C2410C." (hex codes — premature)
- "Minimalist." (vague — what colours?)
- "Modern." (means nothing visually)

---

## Type-pairing language

Name both faces. Be specific about category and weight intention.

- ✅ "Editorial serif display (something in the Tiempos / Fraunces / Lora family) + clean humanist sans body (Inter, Geist, or Söhne)."
- ✅ "One variable face — Söhne Variable — at three weights, no display second family."
- ❌ "Some kind of serif." (no.)

If the user has font budget concerns (open source only, etc.), note an open-source equivalent: "Fraunces (open-source alternative to Tiempos)".

---

## Reference URL per direction

One URL per direction — the layout the agent recommends modeling after. Should be one of the moodboard sites from Phase 4 OR a closely-related sibling. Do not introduce a wildly new reference here.

---

## Sample output (matching the StyleFit diagnostic example: high trust + daily-seconds + content-light + Indian-casual + Magician + look-unlike Myntra)

```
Three directions — meaningfully different, all satisfy the locked diagnostic.

Direction 1 — Editorial Cream
  Personality: Vogue meets product app. Calm, premium, photography-led.
  Palette intent: Warm cream surface with deep ink type. One terracotta accent
    used sparingly on CTAs and selected state.
  Type pairing: Editorial serif display (Fraunces or Tiempos) + humanist sans
    body (Inter at 16px / 1.5).
  Reference: vogue.in for type hierarchy, stitchfix.com for product surface.
  Why this fits: Magician archetype expressed through editorial confidence;
    cream/ink hits Indian-formal without being institutional; photography-led
    leans into content-light density.

Direction 2 — Color Lab
  Personality: A technical-but-warm laboratory for personal style. Clean,
    confident, slightly playful.
  Palette intent: Pure white surfaces. Oversized colour-swatches act as the
    visual hero — colour comes from the *content*, not the chrome. Monoline
    SVG icons throughout.
  Type pairing: Geometric sans display (something in the Söhne / Geist family)
    + same family for body at lower weight.
  Reference: whering.com (closest existing execution).
  Why this fits: Daily-seconds use frequency → fast scan; content-light density
    → colour swatches as hero; Magician archetype expressed through clarity
    rather than mystique.

Direction 3 — Warm Modern Indian
  Personality: Confidently Indian. Terracotta and rose with cream. Real Indian
    skin tones as the visual anchor, no Western stock models.
  Palette intent: Cream base + terracotta and dusty rose accents. Real
    photography of real Indian people doing the styling — that's the colour.
  Type pairing: Modern Indian display (Karnak / Anek or similar) + clean sans
    body (Inter or Geist).
  Reference: fabindia.com for warmth, vogue.in for editorial polish.
  Why this fits: Cultural anchor explicitly leaned into; differentiates hard
    from Myntra (the look-unlike); Magician archetype works on "the version of
    you that looks at home in your own culture."

Pick one — or pick a hybrid (e.g., "Direction 1 palette, Direction 3 photography").
```

---

## Hard rules

- **Exactly 3 directions** (or 2 with explicit explanation if the space is tight).
- **No hex codes.**
- **No "minimalist" as a personality** — every brand thinks it's minimalist; the word means nothing.
- **Each direction must reference back to the diagnostic** in its "Why this fits" line. If you can't explain why a direction satisfies the locked axes, drop it.
- **Allow hybrids in Phase 6.** Don't force a single-direction pick.
