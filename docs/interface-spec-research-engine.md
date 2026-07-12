# UI Research Interface Spec — v5 (single source of truth)

> Committed home of the spec referenced by `skills/ui-research/` and `aside-skill/`. If a format
> changes, change it HERE first, then `skills/ui-research/references/round-formats.md`, then both
> consumers (`skills/ui-research/SKILL.md` and `aside-skill/ui-research/SKILL.md`).

> This is the CONTRACT. The Aside skill, the mission-prompt template, and the UI Research
> orchestrator must all use these exact formats. Authors: obey this verbatim. Do not invent
> alternative field names or block shapes.

---

## 0. The architecture in one picture

```
                 STATIC (installed once in Aside)          DYNAMIC (regenerated per project/round)
                 ┌───────────────────────────┐            ┌──────────────────────────────┐
                 │  ui-research skill          │            │  mission prompt (from canon) │
                 │  (rounds, saturation, tiers,│            │  niche/register/refusals/... │
                 │   teardown checklist, output│            │  + this round's task         │
                 │   formats, comms protocol)  │            └──────────────────────────────┘
                 └───────────────────────────┘
                                                RELAY (human = the wire)
   ui-research (plugin) ──gen prompt──▶ human ──paste──▶ Aside chat ──research──▶ summary block
                                        ▲                                          │
                                        └──────────── paste summary ◀──────────────┘
   ui-research reads summary ──▶ decide/pick concept (with human) ──▶ gen Round-2 directive ──▶ paste ──▶ same Aside chat
```

Two lanes:
- **Thinking travels through the human as paste-able text blocks** (Section 3 + 5). Rich enough that
  the plugin can write canon from the text ALONE.
- **Files (screenshots + full research docs) travel to disk.** The mission prompt gives Aside the
  absolute `brain/` paths; Aside's skill writes there directly (it runs locally). If Aside cannot
  reach those paths in some environment, the paste blocks are the fallback and the plugin reconstructs
  canon from them. Guaranteed channel = paste; disk = optimization.

## 1. No hardcoded numbers — the governing law

NOWHERE in any authored file may a fixed count appear as a target: not "20–40 sites", not
"5–8 teardowns", not "3 concepts". Every quantity is **saturation-driven**:
- Sweep ends when new sites stop revealing new concepts (last few added nothing).
- Concept count is whatever the field actually contains — 2, 4, 6, free.
- Teardown count is however many good examples the chosen concept has.
Usefulness is the only bar: a site earns its place by adding a concept, a better example of one,
or a convention data point. Duration is never our concern — state this explicitly.
Depth dial (quick/standard/deep) tunes *appetite/thoroughness*, NOT hard counts.

A user-pinned reference list is not a hardcoded research count. It is an explicit scope boundary:
inspect every supplied URL and discover no additional sites.

## 1.1 Entry modes and precedence (v5 amendment)

- **Discovery mode** — use when the user wants the field explored or has not selected references.
  Run Round 1, human checkpoint, then Round 2.
- **Provided-reference mode** — use when the user supplies/pins websites or explicitly requests a
  locked set. Skip discovery and render the provided-reference teardown mission. Record the locked
  focus and pinned URLs in `research/concepts.md`; do not invent alternative concepts or sites.

The user's explicit target page/surface and reference constraints outrank STATUS, ROADMAP, prior
next-actions, and inferred opportunities. Ask only for a missing target, missing pinned URLs, and
research depth. Manual Aside prompt relay is the default transport; do not offer another browser
unless the user requests an alternative or Aside is unavailable.

Resolve disk paths from the active session checkout. A worktree mission writes to that worktree's
`brain/`; it never redirects to the main checkout or another worktree because older dirty research
lives there.

## 2. Canon field additions

### 2a. niche (load-bearing; the sweep keys off it)
In `brain/BRAND.md` under `## Product`:
```
- Niche: [industry in plain words — e.g. "luxury hospitality — hotel, fine-dine, banquet, rooftop"]
```
Brand Foundation or migration may populate it from existing verified project truth. Mark `[VERIFY]`
when inferred; UI Research does not rewrite BRAND.

### 2b. research depth (the invocation dial)
Ask per UI Research invocation; do not store it in DESIGN. Quick is a fast confident pass,
standard is the default, and deep chases edge variants. It tunes thoroughness, never counts.

## 3. Round 1 — SWEEP

### 3a. Mission prompt (Round 1) — sections IN ORDER
Header line: `PROJECT-PROTOCOL DESIGN RESEARCH — ROUND 1 (SWEEP) — <project name>`
1. **Role pointer**: "Run the ui-research skill you have installed. This prompt is the project brief."
2. **Project context** (from canon, verbatim values):
   - Niche
   - Register: trust temperature · information density · tempo · cultural anchor
   - Audience + emotional state on arrival
   - Archetype (marketing/dashboard/content/commerce/app) + one-line meaning
   - Surfaces present
   - Distinctive asset (the ownable thing)
   - Look deliberately UNLIKE: <incumbent(s)>
   - Refusals (register-violating patterns) + dated anti-cliché list (do NOT bring these back)
3. **This round's task**: "SWEEP. Discover the field for this niche. Group what you find into
   named concepts (as many as the field truly has). Saturation-driven — no target count.
   Tier discipline applies (ceiling sets craft bar; Pinterest texture-only). Agency-portfolio
   mining is a bonus move when a build credit appears, never the spine — sites first."
4. **Depth**: invocation depth value + its meaning.
5. **Write to disk** (absolute paths given): `brain/research/concepts.md`, screenshots to `brain/moodboard/`.
6. **Return**: "End by printing the ROUND-1 SUMMARY BLOCK below for me to paste back."

### 3b. `brain/research/concepts.md` (Aside writes to disk)
```
# Field concepts — <niche>
> Aside ui-research · Round 1 sweep · <date> · <N> sites examined · depth: <dial>

## Concept <A>: <name>
Feeling: <one line — the emotional read>
Sites: <name — url> · <name — url> · <name — url> ...
Signature moves:
- Hero: <pattern>
- Motion: <what moves, how>
- Type: <display/body character>
- Imagery: <treatment>
- Rhythm: <section grammar>
Evidence: <slug>-hero.png · <slug>-mid.png ...
Register fit: <does this concept serve OUR trust/tempo/anchor — or fight it?>

## Concept <B>: <name>
... (repeat — AS MANY as the field has, no fixed number)

## Saturation note
Examined <N>. Last <M> sites added no new concept → field mapped.
## Agency finds (bonus, if any)
<agency name — url> → <k> same-niche works surfaced
```

### 3c. ROUND-1 SUMMARY BLOCK (Aside prints → human pastes to the plugin)
Compact, paste-friendly, NO images. Fenced so it copies clean:
```
═══ ROUND-1 SUMMARY · <project> · <date> ═══
Niche: <niche> | Sites examined: <N> | Depth: <dial>

CONCEPTS FOUND (<count>):
[A] <name> — <feeling>
    Sites: <name, name, name>
    Moves: hero <x> · motion <y> · type <z> · imagery <w>
    Register fit: <line>
[B] <name> — ...
[C] ...

SATURATION: stopped at <N>, last <M> added nothing new.
AGENCY FINDS: <agency → k works> | none
FILES WRITTEN: brain/research/concepts.md · brain/moodboard/<k> shots
QUESTIONS FOR YOU: <any blockers Aside hit, or "none">
═══ END ROUND-1 ═══
```

## 4. CHECKPOINT (plugin-side, with the human)

The plugin receives the paste, validates (does concepts.md parse? screenshots present?), then
presents the concepts for a decision. The human picks ONE, or BLENDS ("hero of A + type of B"),
or asks for more. The decision is written to canon so all skills see it:
- Record the Round-2 focus inside `brain/research/concepts.md`; do not mutate BRAND or DESIGN.
- Express a blend as explicit page/component-level picks.
This is a conversation, not a menu dump. Research describes evidence and never becomes design authority.

## 5. Round 2 — DEEP TEARDOWN

### 5a. ROUND-2 DIRECTIVE (plugin composes → human pastes into SAME Aside chat)
```
═══ ROUND-2 DIRECTIVE · <project> ═══
CHOSEN CONCEPT: <letter/name>   [or BLEND: <A.hero> + <B.type> + ...]
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

Write each to brain/research/teardowns/<slug>.md ; screenshots to brain/moodboard/.
End by printing the ROUND-2 SUMMARY BLOCK.
═══ END DIRECTIVE ═══
```

### 5b. `brain/research/teardowns/<slug>.md` (Aside writes)
```
# Teardown — <site name>
URL: <url> | Captured: <date> | Target: <page/region> | Concept: <letter>
Desktop viewport: <size> | Mobile viewport: <size/not observed> | Capture method: <method>
Capture status: <LIVE VIEWPORT COMPLETE | LIVE VIEWPORT PARTIAL | MEDIA FALLBACK ONLY | NO VISUAL CAPTURE>

## Type system
Loaded fonts: <family (weight) · family (weight)>   (from document.fonts — actual, not guessed)
Pairing + scale: <observed>
## Color
BRAND-USED COLORS: <visible element/selector → computed value → usage>
FRAMEWORK/PLUGIN DEFAULTS: <excluded values | none>
WIDGET/CONSENT/FORM NOISE: <excluded values | none>
## Motion
Stack detected: <libs from window globals + network>
Behaviors: <reveals · parallax · hero mechanic · hover moves>
## Hero mechanics
<what it does, how it's built>
## Section rhythm
<section-by-section grammar; varies or repeats>
## Imagery treatment
<photography/render · grain · masking · aspect>
## Mobile, accessibility and performance
<observed behavior and costs>
## Evidence
<direct observations>
## Inference
<labeled interpretations | none>
## Unresolved gaps
<exact blockers | none>
## Conventions (this niche)
FOLLOW: <...> | DEVIATE: <...> | REFUSE: <...>
```
Law: extracted values are EVIDENCE FOR our tokens, never copied AS our tokens (design-check enforces).

### 5d. Evidence integrity and readiness

- Rendered viewport screenshots, media fallbacks, partial captures and no-visual states are distinct.
- Validate mobile from actual dimensions/aspect and recorded CSS viewport, not a filename.
- Visible computed use establishes brand color; root/framework/widget variables alone do not.
- Capture recovery uses fresh light contexts, native scroll and stable section targets, then records
  exact blockers rather than looping indefinitely.
- A per-site manifest records desktop/mobile status, files, fallbacks and gaps.
- Readiness is saturation-based. Return `WITH DOCUMENTED GAPS` when gaps cannot materially change
  convergence; return `NOT READY` only for material unresolved uncertainty.

### 5e. Provided-reference summary

The final relay reports pinned sites and blockers; desktop and mobile capture-status counts;
convergence, site-specific moves and conventions; files and honest gaps; saturation reasoning; and
one readiness verdict: ready, ready with documented gaps, or not ready with the material uncertainty.
The block shape lives in `skills/ui-research/references/round-formats.md` and is rendered verbatim by
Variant C.

### 5c. ROUND-2 SUMMARY BLOCK (Aside prints → human pastes to the plugin)
```
═══ ROUND-2 SUMMARY · <project> · concept <X> ═══
Sites torn down (<count>): <name, name, ...>

CONVERGENCE (what the best examples share):
- Type: <the pattern across sites — real font families seen>
- Color: <palette tendency + real hexes>
- Motion: <stack + behaviors that recur>
- Hero: <the dominant mechanic>
- Rhythm: <how sections are sequenced>
- Imagery: <treatment>

CONVENTIONS:
FOLLOW: <...> | DEVIATE: <...> | REFUSE: <...>

FILES: brain/research/teardowns/<k> · brain/moodboard/<k> shots
═══ END ROUND-2 ═══
```

## 6. Ingest without changing design authority

UI Research validates and preserves the returned evidence under `brain/research/` and
`brain/moodboard/`. It does not mutate BRAND or DESIGN. Page-specific choices belong in the
relevant chapter; Style Lock or Build Page consumes the evidence later only when explicitly invoked.

## 7. Transport

- **Default: manual skill + prompt relay** (this spec). Aside runs the installed skill; the human
  relays the paste blocks. Works for any user, any project.
- Do not present a transport-choice menu. Use another browser only when the user asks or Aside is unavailable.
- **Fallback: pure paste** (no Aside FS access) — Aside prints everything; the plugin writes ALL
  canon from the paste blocks. This is why the blocks must be self-sufficient.

## 8. Where each piece lives

- **`aside-skill/ui-research/SKILL.md`** (standalone, installed into Aside once): everything in
  Aside's head — round structure, saturation law, tier map, traversal moves (awards→agency-portfolio
  bonus→competitors), teardown checklist, technical-detection cheatsheet (window.gsap/Lenis/Framer/
  document.fonts/:root palette/video-network), bot-wall + cookie-wall handling (skip, never fight),
  the two SUMMARY BLOCK formats to print, the disk-write paths convention, the "no hardcoded counts"
  law. NO project specifics — those come in the prompt.
- **`skills/ui-research/references/mission-prompt-template.md`**: the fill-in-the-blanks template
  UI Research renders from canon, discovery Round-1/Round-2 and provided-reference variants
  sources.
- **`skills/ui-research/references/round-formats.md`**: the relay/file formats shared by both sides.
- **`skills/ui-research/SKILL.md`**: selects the entry mode, renders the Aside mission, ingests
  evidence, and stops before Style Lock or Build Page.
