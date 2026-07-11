# Round formats — the shared block & file contract

> Single source of truth for the relay/file formats used by the research engine.
> `calibrate` (plugin side) and `aside-research-skill.md` (Aside side) both point HERE so they
> never diverge. These shapes come from the Interface Spec v4.1 (Sections 3 + 5) and match
> `aside-research-skill.md` verbatim. If a format changes, it changes in the Interface Spec first,
> then here, then in both consumers.
>
> **Fill the `<...>` slots; keep the headers, fences, and field names exactly.** Do not rename a
> field or invent a block shape — the studio parses these.

---

## Two governing laws (apply to every block below)

- **No hardcoded counts (Spec §1).** Nowhere in any block is a fixed target allowed — not a site
  count, not a concept count, not a teardown count. Every `<count>` / `<N>` / `<k>` slot is the
  number the field *actually* produced, saturation-driven. A `<count>` is a report of what happened,
  never a goal that was aimed at. The depth dial (quick / standard / deep) tunes appetite, not counts.
- **Paste blocks must be self-sufficient (Spec §7, fallback C).** Disk writes are an optimization;
  the paste SUMMARY BLOCK is the guaranteed channel. Aside prints the block **every round, even when
  the disk writes succeed.** If Aside cannot reach the `brain/` paths in some environment, the paste
  block is the ONLY channel and Claude must be able to write canon from it alone — so it carries the
  full findings, not a pointer to a file.

---

# Round 1 — SWEEP

## `brain/research/concepts.md` — Aside writes to disk (Spec §3b)

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

## ROUND-1 SUMMARY BLOCK — Aside prints → Vish pastes to Claude (Spec §3c)

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

---

# Round 2 — DEEP TEARDOWN

## ROUND-2 DIRECTIVE — Claude composes → Vish pastes into the SAME Aside chat (Spec §5a)

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

## `brain/research/teardowns/<slug>.md` — Aside writes to disk (Spec §5b)

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

## ROUND-2 SUMMARY BLOCK — Aside prints → Vish pastes to Claude (Spec §5c)

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
