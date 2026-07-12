# Research-Engine Interface Spec — v4.1 (single source of truth)

> Committed home of the spec referenced by `skills/calibrate/` and `aside-skill/`. If a format
> changes, change it HERE first, then `skills/calibrate/references/round-formats.md`, then both
> consumers (`skills/calibrate/SKILL.md` and `aside-skill/design-research/SKILL.md`).

> This is the CONTRACT. The Aside skill, the mission-prompt template, and the calibrate
> orchestrator must all use these exact formats. Authors: obey this verbatim. Do not invent
> alternative field names or block shapes.

---

## 0. The architecture in one picture

```
                 STATIC (installed once in Aside)          DYNAMIC (regenerated per project/round)
                 ┌───────────────────────────┐            ┌──────────────────────────────┐
                 │  design-research skill      │            │  mission prompt (from canon) │
                 │  (rounds, saturation, tiers,│            │  niche/register/refusals/... │
                 │   teardown checklist, output│            │  + this round's task         │
                 │   formats, comms protocol)  │            └──────────────────────────────┘
                 └───────────────────────────┘
                                                RELAY (human = the wire)
   calibrate (plugin) ──gen prompt──▶ human ──paste──▶ Aside chat ──research──▶ summary block
                                        ▲                                          │
                                        └──────────── paste summary ◀──────────────┘
   calibrate reads summary ──▶ decide/pick concept (with human) ──▶ gen Round-2 directive ──▶ paste ──▶ same Aside chat
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

## 2. Canon field additions

### 2a. niche (load-bearing; the sweep keys off it)
In `brain/BRAND.md` under `## Product`:
```
- Niche: [industry in plain words — e.g. "luxury hospitality — hotel, fine-dine, banquet, rooftop"]
```
Deep path (design-direction Phase 7) and Quick path (init Phase 4) both populate it.
`[VERIFY]` if auto-detected.

### 2b. research_depth (the depth dial)
Asked once at kickoff (init Phase 4, alongside archetype). Stored in `brain/DESIGN.md` frontmatter:
```
research_depth: "[quick | standard | deep]"   # tunes sweep appetite + teardown thoroughness; NOT a count
```
quick = fast map, few concepts confirmed; standard = default; deep = exhaustive field map.

## 3. Round 1 — SWEEP

### 3a. Mission prompt (Round 1) — sections IN ORDER
Header line: `PROJECT-PROTOCOL DESIGN RESEARCH — ROUND 1 (SWEEP) — <project name>`
1. **Role pointer**: "Run the design-research skill you have installed. This prompt is the project brief."
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
4. **Depth**: research_depth value + its meaning.
5. **Write to disk** (absolute paths given): `brain/research/concepts.md`, screenshots to `brain/moodboard/`.
6. **Return**: "End by printing the ROUND-1 SUMMARY BLOCK below for me to paste back."

### 3b. `brain/research/concepts.md` (Aside writes to disk)
```
# Field concepts — <niche>
> Aside design-research · Round 1 sweep · <date> · <N> sites examined · depth: <dial>

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
- `brain/BRAND.md` → Decisions log line + Locked direction seed.
- Concept choice recorded; blend expressed as explicit component-level picks.
This is a conversation, not a menu dump. Phase 5's three directions are then built FROM the
chosen concept — and Rule 7 still forces ≥1 direction to DEPART from everything found
(the escape hatch from the old-style trap: concepts describe the field, never cap ambition).

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
URL: <url> | Captured: <date> | Concept: <letter> | Evidence: <slug>-*.png

## Type system
Loaded fonts: <family (weight) · family (weight)>   (from document.fonts — actual, not guessed)
Pairing + scale: <observed>
## Color
Palette: <#hex · #hex · #hex>   (from :root / computed) | Usage: <split>
## Motion
Stack detected: <libs from window globals + network>
Behaviors: <reveals · parallax · hero mechanic · hover moves>
## Hero mechanics
<what it does, how it's built>
## Section rhythm
<section-by-section grammar; varies or repeats>
## Imagery treatment
<photography/render · grain · masking · aspect>
## Conventions (this niche)
FOLLOW: <...> | DEVIATE: <...> | REFUSE: <...>
```
Law: extracted values are EVIDENCE FOR our tokens, never copied AS our tokens (design-check enforces).

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

## 6. Fold into canon (calibrate, plugin-side, after Round 2 paste)

calibrate maps the returns onto EXISTING consumers (unchanged formats downstream):
- `brain/moodboard/notes.md` — existing v4.0.0 per-entry format, now populated from the chosen
  concept's torn-down sites (tier tag stays; "why it works" line now cites teardown evidence).
- `brain/DESIGN.md` conventions audit (FOLLOW/DEVIATE/REFUSE) — existing block, now EVIDENCE-BACKED
  (e.g. "9 of 12 hotels use full-bleed video hero" not a guess).
- `brain/research/` files already on disk from Aside — the deep evidence Phase 6.5 (tokens) and
  build-page's external-ref cross-check read.
Then hand back to design-direction Phase 5 exactly as today (explicit `Skill()` call).

## 7. Three transport methods (same file contract for all three)

- **Primary: manual skill + prompt relay** (this spec). Aside runs the installed skill; the human
  relays the paste blocks. Works for any user, any project.
- **Fallback A: MCP repl** (the tested runbook — never fullPage, one action/call, ./artifacts→cp).
  Used when the plugin must drive Aside directly (no human relay available).
- **Fallback C: pure paste** (no Aside FS access) — Aside prints everything; the plugin writes ALL
  canon from the paste blocks. This is why the blocks must be self-sufficient.

## 8. Where each piece lives

- **`aside-skill/design-research/SKILL.md`** (standalone, installed into Aside once): everything in
  Aside's head — round structure, saturation law, tier map, traversal moves (awards→agency-portfolio
  bonus→competitors), teardown checklist, technical-detection cheatsheet (window.gsap/Lenis/Framer/
  document.fonts/:root palette/video-network), bot-wall + cookie-wall handling (skip, never fight),
  the two SUMMARY BLOCK formats to print, the disk-write paths convention, the "no hardcoded counts"
  law. NO project specifics — those come in the prompt.
- **`skills/calibrate/references/mission-prompt-template.md`**: the fill-in-the-blanks template
  calibrate renders from canon, Round-1 and Round-2 variants, with `<placeholders>` mapped to canon
  sources.
- **`skills/calibrate/references/round-formats.md`**: the four block formats + two file formats above,
  as the shared reference both calibrate and the Aside skill point to (single source, no divergence).
- **`skills/calibrate/SKILL.md`**: the plugin-side orchestrator — gen Round-1 prompt from canon →
  present to the human to paste → ingest Round-1 paste + validate → checkpoint (pick/blend, write
  decision to canon) → gen Round-2 directive → ingest Round-2 paste + validate → fold into
  moodboard/notes.md + DESIGN.md conventions audit → hand back to design-direction Phase 5.
