# Mission-prompt template — what UI Research renders for the user to paste into Aside

> This is the **dynamic** half of the research engine (the static half is the installed
> `aside-skill/ui-research/SKILL.md`). UI Research fills these templates from project canon and hands the user
> a clean prompt to paste into the Aside chat — one variant per round.
>
> **How to use this file (ui-research, plugin side):**
> 1. Read the canon values named in each variant's *Placeholder sources* map.
> 2. Substitute every `<placeholder>` with the real value. Leave nothing in angle brackets.
> 3. Emit ONLY the fenced prompt (the `←` source lines and this prose are NOT pasted).
> 4. Hand the rendered prompt to the user to paste into Aside.
>
> **Spec §1 — no hardcoded counts.** Never inject a site / concept / teardown target into a rendered
> prompt. The task lines already say "saturation-driven — no target count"; keep them verbatim.
> **Self-containment (Spec §7).** The pasted prompt must stand on its own; it points to
> `round-formats.md` only for the studio-side full block shapes — Aside already carries them in its
> installed skill.

---

## Variant A — ROUND 1 (SWEEP)

Sections in the order fixed by Spec §3a: header · role pointer · project context · this round's task ·
depth · write-to-disk · return.

```
PROJECT-PROTOCOL DESIGN RESEARCH — ROUND 1 (SWEEP) — <project>

Run the ui-research skill you have installed. This prompt is the project brief.

PROJECT CONTEXT
- Niche: <niche>
- Register: trust <trust-temperature> · density <info-density> · tempo <tempo> · cultural anchor <cultural-anchor>
- Audience: <audience> — on arrival they feel <emotional-state>
- Archetype: <archetype> — <archetype-meaning>
- Surfaces present: <surfaces>
- Distinctive asset (the ownable thing): <distinctive-asset>
- Look deliberately UNLIKE: <look-unlike>
- Refusals (register-violating patterns — do NOT bring these back): <refusals>
- Dated anti-cliché (current second-order AI tells — do NOT report as fresh): <anti-cliche>

THIS ROUND'S TASK
SWEEP. Discover the field for this niche. Group what you find into named concepts (as many as the
field truly has). Saturation-driven — no target count. Tier discipline applies (ceiling sets the
craft bar; Pinterest texture-only). Agency-portfolio mining is a bonus move when a build credit
appears, never the spine — sites first.

DEPTH
research depth: <research-depth> — <depth-meaning>

WRITE TO DISK
- Concepts doc → <brain-abs>/research/concepts.md
- Screenshots → <brain-abs>/moodboard/   (name <slug>-hero.png / <slug>-mid.png / <slug>-end.png per site)

RETURN
End by printing the ROUND-1 SUMMARY BLOCK below for me to paste back — even if the disk writes
succeeded (the paste block is the guaranteed channel). Full field-by-field shape: round-formats.md
→ "ROUND-1 SUMMARY BLOCK".

═══ ROUND-1 SUMMARY · <project> · <date> ═══
Niche: <niche> | Sites examined: <N> | Depth: <research-depth>
CONCEPTS FOUND (<count>): [A] <name> — <feeling> · Sites · Moves · Register fit ; [B] … ; …
SATURATION: stopped at <N>, last <M> added nothing new.
AGENCY FINDS: <agency → k works> | none
FILES WRITTEN: brain/research/concepts.md · brain/moodboard/<k> shots
QUESTIONS FOR YOU: <blockers, or "none">
═══ END ROUND-1 ═══
```

### Placeholder sources (Variant A)

```
<project>            ← brain/BRAND.md ## Product · Name  (also brain/DESIGN.md frontmatter name:)
<niche>              ← brain/BRAND.md ## Product · Niche
<trust-temperature>  ← brain/BRAND.md register diagnostic · trust temperature  (Max / High / Medium / Low)
<info-density>       ← brain/BRAND.md register diagnostic · information density (Data-dense / Content-light / Mixed)
<tempo>              ← brain/BRAND.md register diagnostic · tempo              (Motion-led / Static / Mixed)
<cultural-anchor>    ← brain/BRAND.md ## Brand · Cultural anchor              (part of the register diagnostic)
<audience>           ← brain/BRAND.md ## Audience · Who it's for
<emotional-state>    ← brain/BRAND.md ## Audience · Emotional state before our product
<archetype>          ← brain/BRAND.md primary brand archetype
<archetype-meaning>  ← brain/BRAND.md archetype meaning
<surfaces>           ← brain/BRAND.md ## Product · Surfaces
<distinctive-asset>  ← brain/BRAND.md · distinctive asset (the ownable signature)
<look-unlike>        ← brain/BRAND.md ## Reference tribe · Look deliberately unlike
<refusals>           ← brain/DESIGN.md ## DO NOT · brand-specific anti-patterns block
<anti-cliche>        ← brain/DESIGN.md ## DO NOT · dated anti-cliché block      (refresh at calibration — these date)
<research-depth>     ← chosen for this UI Research invocation (quick / standard / deep)
<depth-meaning>      ← derived from <research-depth>: quick = fast, confident map of the obvious concepts ·
                       standard = default, sweep to real saturation · deep = exhaustive, chase the long tail
<brain-abs>          ← this project's brain/ absolute path (e.g. /Users/…/<project>/brain)
<date> <slug> <N> <M> <count> <k>  ← Aside fills these at run time — never a preset target (Spec §1)
```

---

## Variant B — ROUND 2 (DEEP TEARDOWN)

Pasted into the SAME Aside chat as Round 1 after the user picks or blends a concept at the
checkpoint. Body follows the ROUND-2 DIRECTIVE order fixed by Spec §5a.

```
PROJECT-PROTOCOL DESIGN RESEARCH — ROUND 2 (TEARDOWN) — <project>

Run the ui-research skill you have installed (same chat as Round 1). This directive is the task.

═══ ROUND-2 DIRECTIVE · <project> ═══
CHOSEN CONCEPT: <chosen-concept>   [or BLEND: <blend-picks>]
GO DEEP on this concept. Find and tear down its best real examples (saturation-driven —
as many as are genuinely good; no target count). For each site run the full teardown.

TEARDOWN CHECKLIST (per site):
- Type: fonts ACTUALLY loaded (document.fonts) + weights + pairing + scale
- Color: palette from :root / computed styles (real hex) + usage split
- Motion: detected stack (window.gsap / Lenis / Locomotive / Framer / video-hero via network)
  + behaviors (scroll reveals, parallax, hover, hero mechanics)
- Hero: exactly what it does and how
- Rhythm: section-by-section grammar (does it vary or repeat?)
- Imagery: photography vs render, grain, masking, aspect conventions
- Conventions: FOLLOW / DEVIATE / REFUSE observations for this niche

Write each to <brain-abs>/research/teardowns/<slug>.md ; screenshots to <brain-abs>/moodboard/.
End by printing the ROUND-2 SUMMARY BLOCK — even if the disk writes succeeded. Full field-by-field
shape: round-formats.md → "ROUND-2 SUMMARY BLOCK".
═══ END DIRECTIVE ═══

═══ ROUND-2 SUMMARY · <project> · concept <chosen-concept> ═══
Sites torn down (<count>): <name, name, …>
CONVERGENCE: Type · Color · Motion · Hero · Rhythm · Imagery (what the best examples share)
CONVENTIONS: FOLLOW <…> | DEVIATE <…> | REFUSE <…>
FILES: brain/research/teardowns/<k> · brain/moodboard/<k> shots
═══ END ROUND-2 ═══
```

### Placeholder sources (Variant B)

```
<project>         ← brain/BRAND.md ## Product · Name  (also brain/DESIGN.md frontmatter name:)
<chosen-concept>  ← Round-2 focus recorded in brain/research/concepts.md. Single concept letter/name.
<blend-picks>     ← same focus when the user blended explicit component-level picks, e.g. "A.hero + B.type"
<brain-abs>       ← this project's brain/ absolute path (e.g. /Users/…/<project>/brain)
<slug> <count> <k>  ← Aside fills at run time — never a preset target (Spec §1)
```
