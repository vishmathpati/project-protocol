# Round formats — UI Research and Aside shared contract

> Single source of truth for the relay/file formats used by the research engine.
> `ui-research` (plugin side) and `aside-skill/ui-research/SKILL.md` (Aside side) both point HERE so they
> never diverge. These shapes come from the Interface Spec v4.1 (`docs/interface-spec-research-engine.md`,
> Sections 3 + 5) and match `aside-skill/ui-research/SKILL.md` verbatim. If a format changes,
> it changes in the Interface Spec first, then here, then in both consumers.
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
  block is the ONLY channel and the receiving agent must be able to write canon from it alone — so it carries the
  full findings, not a pointer to a file.

---

# Round 1 — SWEEP

## `brain/research/concepts.md` — Aside writes to disk (Spec §3b)

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

## Human selection
- Status: pending
```

## ROUND-1 SUMMARY BLOCK — Aside prints for the user to relay (Spec §3c)

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

## PROVIDED-REFERENCE CONCEPT SUMMARY BLOCK

Same checkpoint contract as Round 1, but every concept must come only from the closed user-pinned
set. Existing verified teardowns/screenshots are reused before any revisit.

```
═══ PROVIDED-REFERENCE CONCEPT SUMMARY · <project> · <target> ═══
PINNED SITES: <sites represented>
EVIDENCE REUSED: <existing teardown/screenshot paths used | none>
EVIDENCE REFRESHED: <URLs revisited and material reason | none>
CONCEPTS FOUND (<count>):
[A] <name> — <feeling> · Sites <...> · Hero <...> · Navigation <...> · Rhythm <...> · Imagery/motion <...> · Strengths/risks <...> · Project fit <...>
[B] ...
FILES: brain/research/concepts.md · brain/moodboard/<evidence>
QUESTIONS: <material blockers | none>
NEXT: HUMAN SELECTION REQUIRED
═══ END PROVIDED-REFERENCE CONCEPT SUMMARY ═══
```

## Human selection record — Project Protocol writes after the checkpoint

Round 2 is forbidden until this exact block is complete. Pinned sites, locked BRAND/DESIGN, prior
moodboards, existing teardowns, or agent recommendations never substitute for it.

```
## Human selection
- Status: selected
- Focus: <concept letter/name or explicit blend>
- Selected by: <human name/identifier>
- Selected at: <YYYY-MM-DD>
- Included moves: <explicit hero/type/navigation/rhythm/etc. picks; "whole concept" when unblended>
```

---

# Round 2 — DEEP TEARDOWN

## ROUND-2 DIRECTIVE — Project Protocol composes for the SAME Aside chat (Spec §5a)

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
<observed responsive behavior · controls · reduced motion · delivery costs>
## Evidence
<direct DOM/runtime/network/computed-style/live-capture observations>
## Inference
<clearly labeled interpretations | none>
## Unresolved gaps
<failed channels and exact blockers | none>
## Conventions (this niche)
FOLLOW: <...> | DEVIATE: <...> | REFUSE: <...>
```

Law: extracted values are EVIDENCE FOR our tokens, never copied AS our tokens (design-check enforces).

## Provided-reference evidence integrity

- A live screenshot shows rendered page composition; downloaded media is a named fallback, not a shot.
- Validate mobile evidence from actual dimensions/aspect plus recorded CSS viewport, not filenames.
- Retry unstable capture through distinct light-page/native-scroll strategies, then report the blocker.
- Keep a one-row-per-site manifest with desktop/mobile status, live files, fallbacks and gaps.
- Readiness is saturation-based. Honest gaps do not block when the remaining evidence cannot materially
  change convergence; return `WITH DOCUMENTED GAPS`. Material uncertainty returns `NOT READY`.

## ROUND-2 SUMMARY BLOCK — Aside prints for the user to relay (Spec §5c)

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

## PROVIDED-REFERENCE SUMMARY BLOCK

```
═══ PROVIDED-REFERENCE SUMMARY · <project> · <target> ═══
PINNED SITES: <sites actually inspected>
BLOCKED: <blocked URLs and reason | none>
DESKTOP: LIVE COMPLETE <count> · PARTIAL <count> · MEDIA FALLBACK ONLY <count> · NO VISUAL <count>
MOBILE: VALID SCREENSHOT <count> · DOM/RUNTIME ONLY <count> · PARTIAL <count> · NOT OBSERVED <count>
CONVERGENCE: Type · Color · Motion · Hero · Rhythm · Imagery · Navigation
SITE-SPECIFIC MOVES: <site → useful evidence>
CONVENTIONS: FOLLOW <…> | DEVIATE <…> | REFUSE <…>
FILES: brain/research/concepts.md · brain/research/conventions.md · brain/research/teardowns/<k> · brain/moodboard/<k> shots
GAPS: <honest unresolved evidence gaps | none>
SATURATION: <why gaps can or cannot materially change convergence>
READY VERDICT: READY FOR STYLE LOCK/BUILD PAGE [WITH DOCUMENTED GAPS] | NOT READY — <material uncertainty>
═══ END PROVIDED-REFERENCE SUMMARY ═══
```
