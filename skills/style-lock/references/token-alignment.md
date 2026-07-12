# Style Lock — token alignment reference

Compare the approved brand/research direction against existing `brain/DESIGN.md`
and the live theme before proposing changes.

This is the phase that closes the gap between "I locked a new brand direction"
and "my project looks different." Without it, the locked direction lives only
in BRAND.md and Overview — the visual tokens stay as they were.

---

## When this applies

Use when Style Lock proposes token changes. Skip token generation when the existing
system already satisfies the confirmed direction and surface needs.

---

## What it does

1. **Detect surface tier(s) for this project.** From `brain/BRAND.md` Product.Surfaces
   field (or ask the user if absent), classify as one of:
   - dashboard / app only — internal tool, product UI
   - marketing only — landing site, no product chrome
   - both — marketing site + product app

   This drives downstream choices:
   - dashboard-only: type scale ratio 1.125, sober saturation, Inter/Geist/IBM
     Plex acceptable as display (since display is rare on dashboards)
   - marketing-only: type scale ratio 1.25 (or 1.333 for editorial brands),
     more accent saturation; prefer an editorial or expressive display family when
     it materially supports the brand, with intentional exceptions allowed
   - both: generate a single shared body family + separate display family for
     marketing; type scales differ per surface (encode both in DESIGN.md type_scale)

2. **Detect cultural anchor + script requirements.** From `brain/BRAND.md`
   Cultural anchor field, decide whether the brand needs non-Latin script
   support. If brand mentions India / Hindi / Tamil / Devanagari / Bengali /
   Gujarati / Gurmukhi — Latin alone is wrong. The body font MUST pair with:
   - Devanagari / Gujarati / Gurmukhi / Tamil → Mukta (Google Fonts, free)
     OR Hind (Devanagari only, Google Fonts, free)
   - Tamil specifically → Noto Sans Tamil + a Latin pair
   - Bengali → Noto Sans Bengali + a Latin pair
   - Arabic / Hebrew → Noto Sans Arabic / Noto Sans Hebrew + Latin pair

   If no non-Latin signal, default Latin-only stack.

3. **Read the existing token frontmatter** in `brain/DESIGN.md`. Extract:
   - `font.display`, `font.body`, `font.mono`
   - `accent.primary`, `accent.secondary` (if present)
   - `surface.paper`, `surface.ash`, `surface.ink` (or legacy `--bg`, `--surface`, `--ink` for projects on the old shape)
   - `light_mode` and `dark_mode` blocks (or detect that they don't exist yet — older shape)
   - `radius`, `spacing`

4. **Compare each token category against the locked direction**. For each, decide MATCH or MISMATCH:

   | Token category | MATCH if... | MISMATCH if... |
   |---|---|---|
   | `font.display` | existing role serves the approved direction | a different family is required to express the approved direction |
   | `font.body` | both practical sans (Inter/Geist family) | locked specifies a body font that doesn't match |
   | `surface.paper` (light) | hex hue family matches direction's temperature | direction is "warm cream", existing is pure white or cool ivory |
   | `surface.paper` (dark) | hex hue family matches | direction is "warm dark", existing is pure black or cool dark |
   | `accent.primary` | hue family matches direction's accent intent | direction is "terracotta", existing is "electric green" |
   | `radius` scale | numeric scale within ±2px of direction's intent | direction is "soft/generous" (12-16px), existing is "sharp" (2-4px) |
   | `spacing` | scale shape matches | usually MATCH unless direction explicitly calls for different rhythm |

### Archetype → palette starting point

The approved brand foundation may carry an archetype. Use
this as the starting hypothesis for surface paper/ink/accent hex generation.
Tune from there using the direction's specific material reference and
temperature.

| Archetype | Paper temperature | Ink temperature | Accent character | Saturation ceiling (OKLCH chroma) |
|---|---|---|---|---|
| Sage | warm parchment or cool ivory | warm near-black (≠#000) | brass, oxblood, slate-blue | 0.12 |
| Magician | violet near-white or deep cream | deep ink, slight violet hue | iridescent — teal, copper, gold | 0.18 |
| Caregiver | warm cream, peach-tinted | soft brown-black, never harsh | terracotta, sage, dusty rose | 0.10 |
| Rebel | hot near-white or stark cream | warm near-black | hot red, acid yellow, electric (one only) | 0.25 |
| Creator | bright off-white | confident ink | saturated multi-hue — can carry 2 accents | 0.20 |
| Hero | confident ivory | deep navy-ink or oxblood | bold primary (blue / red / gold) | 0.18 |
| Explorer | warm cream, weathered | forest or earth ink | ochre, forest, sky | 0.14 |
| Innocent | very light cream | soft ink, never harsh | sky blue, sunny yellow, blush | 0.10 |
| Lover | blush, champagne, dusty rose | warm wine-ink | burgundy, brass, dusty rose | 0.12 |
| Jester | bright + unexpected (lime cream, peach) | confident ink | playful clash — lime, magenta, cobalt | 0.22 |
| Ruler | ivory or oxblood-tinted cream | deep oxblood or navy-ink | gold, oxblood, deep navy | 0.16 |
| Everyman | honest off-white | mid-warm ink | honest blue or warm orange | 0.14 |

These are starting points, not formulas. The direction's named material
reference (parchment / leather / stone / velvet / ash / saffron / sage /
burgundy) is more specific than the archetype — use it to pick the actual
hex within the temperature band.

### Archetype → typography pairing

| Archetype | Display starting point (free where possible) | Body font | Mono |
|---|---|---|---|
| Sage | Source Serif 4 (Google) or Tiempos Headline (commercial — note cost) | Inter | JetBrains Mono |
| Magician | Fraunces (Google, variable, opsz + SOFT axes) | Geist Sans (Google) | Geist Mono / JetBrains Mono |
| Caregiver | Recoleta (commercial — Source Serif fallback) | Inter | JetBrains Mono |
| Rebel | JetBrains Mono display weight | Inter | JetBrains Mono |
| Creator | PP Editorial New (Pangram free-to-try — Fraunces fallback) | Inter | JetBrains Mono |
| Hero | Geist Sans (Google) across (display + body same family, weight contrast) | Geist Sans | Geist Mono |
| Explorer | Fraunces (Google) | Inter | JetBrains Mono |
| Innocent | Fraunces SOFT axis (Google) | Inter | JetBrains Mono |
| Lover | Source Serif 4 (Google) or Tiempos Headline (commercial) | Inter | JetBrains Mono |
| Jester | Recursive casual + Recursive mono (Google — same family) | Recursive | Recursive Mono |
| Ruler | Cormorant Garamond (Google) or Lyon (commercial) | Inter | JetBrains Mono |
| Everyman | Inter Display (Google) | Inter | JetBrains Mono |

Rules:
- Never pair two geometric sans (Geist + Inter, Söhne + Inter as display).
- DESIGN's `avoid_by_default` list is a heuristic. Intentional exceptions are allowed
  when the surface, existing system, script coverage, or brand strategy justifies them.
- Variable fonts preferred when available.
- For Indic-script brands, pair the Latin body with the Indic body (see Step 2).

### Categorical chart palette (dashboard surfaces only)

If surface tier is dashboard or both AND the project has data visualization
needs (the user mentioned charts/graphs/dashboards/metrics), generate a
categorical palette of 8–12 perceptually-spaced hues for chart series.

Use OKLCH-stepped hues at constant L=60% (light mode) / L=70% (dark mode):
- hue 30, 60, 120, 180, 210, 270, 300, 340 (8 stops)
- add hue 0, 90, 150, 240 for 12-stop (extends contiguous data series)

Constant L and constant C (~0.15) ensure perceptual spacing — no single hue
dominates by saturation alone. Output as `chart_palette:` block in DESIGN.md
frontmatter (a new optional block added in the template update).

If no dashboard surface, omit the chart_palette generation entirely.

5. **Report alignment summary** to user. Three possible outcomes:

   - **All MATCH** → existing tokens still fit. Tell the user no token changes are needed.
   - **Partial MISMATCH** → some categories need updating. Show diff per category. Ask user: "these N tokens need to change to match the locked direction. Apply the proposed values?"
   - **Full MISMATCH** → locked direction doesn't match any existing tokens (typical for first-time `brand-foundation` + `style-lock` run, or major re-anchor). Propose full new token frontmatter.

6. **Generate new token values** for MISMATCH categories using the locked direction's:
   - Material reference (parchment, leather, stone, velvet, ash) → surface paper/ash/ink hex
   - Temperature (warm/cool/neutral) → adjust hex hue toward the matching family
   - Saturation (muted/tinted/jewel) → adjust chroma
   - Type pairing (display/body/mono families) → font.display, font.body, font.mono
   - Accent material (brass/terracotta/oxblood/burgundy/etc) → accent.primary hex
   - Light+dark mode characters from the direction → light_mode and dark_mode blocks
   - For dark mode: don't invert. Apply these rules:
     - paper: shift the light mode paper to its dark complement, keeping
       temperature (warm cream → warm leather; cool ivory → blue-black);
       never #000; tint 4–8% toward the brand's temperature.
     - ink: shift to ~92–95% lightness, keeping temperature (warm parchment
       on warm leather); never pure #FFF.
     - accent.primary: desaturate by 20–35% OKLCH chroma (a vibrant brand
       colour that worked on white burns on near-black). Shift lightness up
       slightly (~+5–10%) so it doesn't recede on dark.
     - hairline: lighter than the dark paper, not darker. Borders are
       highlights on dark canvas, not depressions.

### Validation — WCAG contrast check (refuse to write on fail)

Before showing the preview, compute WCAG contrast ratios for these load-bearing pairs. Use the standard relative-luminance formula: ratio = (L1 + 0.05) / (L2 + 0.05) where L1 is the lighter colour's relative luminance.

Required minimums:
- ink on paper (light mode) — 4.5:1 (body text)
- ink on ash (light mode) — 4.5:1 (body text on raised surface)
- ink on paper (dark mode) — 4.5:1
- ink on ash (dark mode) — 4.5:1
- paper on accent.primary (both modes) — 4.5:1 (text on CTA buttons)
- accent.primary on paper (both modes) — 3:1 (link colour visibility)
- hairline on paper (both modes) — 3:1 (border visibility)
- status.error on paper (both modes) — 4.5:1

If ANY pair fails:
- Do not skip the preview — render it with red FAIL badges on the failing rows.
- Do not let the user approve. The preview itself shows the failing pairs.
- Auto-suggest a fix: darken the ink (light mode) / lighten the ink (dark mode) / shift accent to a more contrasting hue.
- Re-run generation with the suggested fix, re-validate, re-preview.

The skill must not write a palette that fails WCAG AA. Hard rule.

### Generate the HTML preview

Before showing the text diff, write a self-contained HTML preview page that
renders the proposed tokens applied to BOTH (a) the project's actual surface
layout (dashboard or marketing or both), and (b) the individual component
catalogue below.

The layout view is the load-bearing section — it's what tells the user whether
their PRODUCT looks good, not just whether the tokens are individually pretty.
Use the surface tier detected in step 1 to pick which layout(s) to render:

- tier == "dashboard"  → render the dashboard mockup ONLY. Skip the marketing
                         mockup. Skip the standalone hero (Section 20 in the
                         component catalogue) — dashboards don't ship with one.
- tier == "marketing"  → render the marketing landing mockup ONLY. The hero
                         lives inside that mockup. Skip the standalone Section
                         20 hero to avoid duplication.
- tier == "both"       → render dashboard FIRST, then a visible section divider
                         labelled "MARKETING PREVIEW", then the marketing
                         mockup. Skip the standalone Section 20 hero.

→ See `references/phase-6-5-preview-html.md` for the full spec — Section 0
  (surface layouts), the 21 component sections, the literal HTML template
  with placeholders, font-loading rules (Google Fonts only — substitute with
  notice for everything else), file path conventions
  (`brain/preview/<slug>-<date>.html`), and the iteration loop semantics.

Always render the preview when tokens are changing. Skip only when alignment
result is `match` (no token changes).

7. **Preview the proposed token diff** before Style Lock writes. Format:

```
Token alignment — comparing locked direction "Editorial Cream" vs existing DESIGN.md:

font.display:    Inter         →  Migra              [MISMATCH — approved direction needs a more distinctive display role]
font.body:       Inter         →  Inter              [MATCH]
font.mono:       (not set)     →  JetBrains Mono     [NEW]

light_mode.paper:  #FFFFFF     →  #F5EFE4 (warm cream)        [MISMATCH — pure white doesn't fit "warm parchment"]
light_mode.ink:    #000000     →  #1A1410 (warm ink)           [MISMATCH — pure black]
dark_mode.paper:   #000000     →  #1A0F0A (warm near-black)    [MISMATCH — pure black, no warm tint]
dark_mode.ink:     #FFFFFF     →  #F5EFE4 (warm ivory)         [MISMATCH]

accent.primary:    #F97316     →  #B8895A (brass)              [MISMATCH — orange doesn't fit "brass + parchment"]

radius.sm/md/lg:   4/8/12       →  6/10/14                     [MISMATCH — direction calls for slightly softer]

spacing:           [4,8,12,16,24,32,48,64]  →  same             [MATCH]

👀 Preview rendered: file:///<absolute-project-path>/brain/preview/editorial-cream-2026-05-22.html

Open it in your browser to see the tokens applied to real components.
Light/dark toggle is in the top-right.

When you're ready:
  approve / apply all  — write the new tokens to brain/DESIGN.md
  iterate              — tell me what to change in plain language
  reject               — keep existing tokens, only write Overview + DO NOT
```

8. **On user approval**, write the accepted values through Style Lock.

---

## Hard rules

- **Never silently overwrite tokens.** Always show the diff. Always ask.
- **If a token category MATCHES, never propose a change** just for the sake of changing it. Respect user's existing work.
- **The user's explicit approval is authoritative.** Research and diagnostic mappings are evidence and starting points, never a reason to overrule the owner.
- **Numeric scales (spacing, radius)** only change if the direction has a strong opinion on rhythm. Default to MATCH for these.
- **Always render the preview HTML when tokens change.** The text diff is not
  a sufficient approval surface. The preview is non-skippable when
  alignment_result is `full_mismatch` or `partial_mismatch`.
- **Refuse to write a palette that fails WCAG AA.** Auto-iterate with a fix,
  re-validate, re-preview. The skill never asks the user to approve a
  failing palette.
- **Surface detection drives type-scale + display-font selection.** Dashboard
  surfaces get 1.125 ratio + relaxed display banning. Marketing surfaces get
  1.25/1.333 + intentional display-role selection using DESIGN's `avoid_by_default` heuristic.

---

## Output

A structured alignment object for Style Lock:

```yaml
alignment_result: full_mismatch | partial_mismatch | match
mismatched_categories: [font.display, surface.paper, accent.primary, ...]
new_token_values:
  font:
    display: "Migra"
    body: "Inter"
    mono: "JetBrains Mono"
  light_mode:
    paper: "#F5EFE4"
    ink: "#1A1410"
    ...
  dark_mode:
    paper: "#1A0F0A"
    ...
  accent:
    primary: "#B8895A"
  radius: { sm: "6px", md: "10px", lg: "14px" }
user_choice: apply_all | apply_subset | keep_existing
```

Style Lock writes this only after approval.

---

## When the user picks "keep existing"

Tell them explicitly: "Tokens unchanged. Your project will NOT visually change
from this `brand-foundation` + `style-lock` run. Only BRAND.md and DESIGN.md Overview will
update. If you wanted visual change, restart the skill and reconsider the
approved direction."

Don't soft-pedal this. The user needs to know that picking "keep existing"
means they ran the skill for documentation, not for visual change.

---

## When the user picks "iterate"

User comes back with a plain-language correction ("accent feels too orange",
"display is too heavy", "dark mode is muddy"). Style Lock:

1. Translate the correction into a token-level change:
   - "too orange" → shift accent hue cooler (lower H value toward red or
     toward neutral)
   - "too heavy" → switch display to a lighter weight cut, or to a different
     family with less contrast
   - "dark mode muddy" → increase dark mode paper lightness by 3–5%, or
     reduce accent saturation further

2. Re-run step 6 (generate new token values) with the correction applied.

3. Re-run the WCAG validation sub-step.

4. Re-run the HTML preview generation sub-step — write to a NEW filename with
   a -v2, -v3 suffix. Don't overwrite the prior preview — the user may
   want to compare.

5. Re-surface the new preview path with the diff (step 7). Loop until approve or reject.

Soft limit: at 5 iterations, surface a meta-prompt — "We're on iteration 5.
The direction itself might be wrong — want to step back and
reconsider?"
