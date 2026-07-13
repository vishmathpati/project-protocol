# UI Research Interface Spec — v5 (single source of truth)

> Committed home of the spec referenced by `skills/ui-research/` and `aside-skill/`. If a format
> changes, change it HERE first, then `skills/ui-research/references/round-formats.md`, then both
> consumers (`skills/ui-research/SKILL.md` and `aside-skill/ui-research/SKILL.md`).

> This is the CONTRACT. The Aside skill, the mission-prompt template, and the UI Research
> orchestrator must all use these exact formats. Authors: obey this verbatim. Do not invent
> alternative field names or block shapes.

## Shared page-recommendation packet

Aside writes this derived relay to `brain/research/page-recommendations.json` in the active checkout
and prints the identical JSON as the manual fallback. Markdown research remains canon; this packet
contains evidence-backed recommendations only and never human selections or build locks.

<!-- PAGE_RECOMMENDATIONS_V1_START -->
```json
{
  "schema_version": "project-protocol.page-recommendations.v1",
  "mission_id": "<stable mission id>",
  "project": "<project name>",
  "generated_at": "<ISO-8601 timestamp>",
  "entry_mode": "open-discovery | provided-reference-discovery | selected-focus-teardown | focused-followup",
  "derived_path": "brain/research/page-recommendations.json",
  "checkout": {
    "checkout_root": "<absolute active checkout/worktree root>",
    "brain_root": "<absolute active brain path>",
    "branch": "<branch or detached-head>",
    "head": "<git commit or unavailable>"
  },
  "input": {
    "site_goal": "<plain-language site goal>",
    "page_families": [{"family_id": "<stable id>", "label": "<label>", "routes": ["<route>"], "kind": "unique | repeated-family | special | utility | legal"}],
    "targets": [{"target_id": "<stable id>", "family_id": "<stable id>", "label": "<label>", "content_goal": "<goal>", "content_jobs": ["<job>"]}],
    "available_media": [{"asset_id": "<stable id>", "kind": "image | video | icon | illustration | logo-mark | other", "status": "owned | client-provided | licensed | generated | temporary | missing"}],
    "reference_scope": {"mode": "open | pinned", "urls": ["<exact URL>"]}
  },
  "site_direction": {"recommendation_id": "<stable id>", "summary": "<plain-language recommendation>", "fit": "<why it serves the site>", "alternatives": ["<alternative>"], "evidence_refs": ["<evidence id>"], "confidence": {"level": "high | medium | low", "reason": "<reason>", "material_gaps": ["<gap>"]}},
  "global_shell": {"target_id": "global-shell", "state": "recommended | not_needed", "recommendations": [{"recommendation_id": "global-shell--<stable recommendation slug>", "scope": "global-shell", "title": "<navigation/footer/header treatment>", "dependencies": ["<page/hero recommendation id>"], "evidence_refs": ["<evidence id>"]}]},
  "targets": [{
    "target_id": "<stable id from input>",
    "recommendations": [{
      "recommendation_id": "<target id>--<stable recommendation slug>",
      "scope": "whole-page | connected-sections | one-section | repeated-page-family | global-shell",
      "affected_blocks": ["<stable page-map block id>"],
      "title": "<plain-language name>",
      "description": "<what the human will see and experience>",
      "fit": "<how the project content and goal map to this option>",
      "alternatives": ["<recommendation id>"],
      "compatibility_notes": {"dependencies": ["<recommendation id>"], "notes": "<research evidence that may affect combination review; no verdict>"},
      "evidence": [{"evidence_id": "<stable id>", "site": "<site>", "page": "<page/region>", "live_url": "<exact URL>", "screenshot_paths": ["<worktree-local path>"], "capture_status": "live-complete | live-partial | media-fallback-only | no-visual", "viewport": "<size>", "video": {"role": "<role or none>", "provider_or_page_url": "<URL or none>", "delivery": "<type or unknown>", "playback": "<flags or unknown>", "reduced_motion_fallback": "<observed, absent, or unknown>", "official_embed": "<yes, no, or unknown>"}, "motion": {"behavior": "<plain behavior>", "implementation_evidence": "<observed stack/triggers or unknown>"}, "teardown_path": "<path or none>", "evidence": "<direct observation>", "inference": "<labeled inference or none>"}],
      "asset_requirements": [{"asset_id": "<stable slot id>", "kind": "image | video | bespoke-icon | illustration | logo-mark | other", "purpose": "<slot job>", "quantity": "<actual required quantity>", "orientation_or_dimensions": "<need>", "responsive_need": "<desktop/mobile need>", "poster_or_fallback": "<need or none>", "safe_source_routes": ["existing", "client", "licensed", "generated", "commissioned", "temporary"], "replacement_or_rights_state": "<state>"}],
      "confidence": {"level": "high | medium | low", "reason": "<reason>", "material_gaps": ["<gap>"]},
      "focused_followup": {"eligible": true, "question": "<narrow page/block question or none>"}
    }]
  }],
  "unresolved_gaps": ["<honest gap>"],
  "saturation": "<why further discovery would or would not change recommendations>",
  "evidence_readiness": "ready | ready_with_documented_gaps | not_ready"
}
```
<!-- PAGE_RECOMMENDATIONS_V1_END -->

**Ownership boundary.** `evidence_readiness` means research-evidence readiness only; it never means
ready to build. Recommendation `compatibility_notes` carry observed dependencies and cautions, never an
agent combination verdict. Claude or Codex owns the exact review statuses `compatible`,
`compatible_with_adaptation`, and `conflicting`. Canonical research evidence is not an approved design
selection. Final human approval must produce and validate the `## Approved Site Direction` Markdown
record defined by `source/skills/build-page/references/site-direction-lock.md`; until that complete record
is locked, no selected teardown or build is authorized.

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
   dashboard reads packet ──▶ human submits whole-site draft ──▶ Claude/Codex checks ──▶ human approves
   approved target/recommendation IDs ──▶ focused Round-2 directive ──▶ paste ──▶ same Aside chat
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
- Teardown count is however many good examples the approved target and recommendation scope has.
Usefulness is the only bar: a site earns its place by adding a concept, a better example of one,
or a convention data point. Duration is never our concern — state this explicitly.
Depth dial (quick/standard/deep) tunes *appetite/thoroughness*, NOT hard counts.

A user-pinned reference list is not a hardcoded research count. It is an explicit scope boundary:
inspect every supplied URL and discover no additional sites.

## 1.1 Entry modes and precedence (v5 amendment)

There are four entry modes:

- **Open discovery** — no pinned set and no approved site-wide direction. Run the site-wide/page-aware
  discovery pass, then stop at the dashboard-backed human checkpoint.
- **Provided-reference concept discovery** — the user supplies/pins websites but has not explicitly
  approved a site-wide direction. Use only the pinned set, group it into concepts, produce page-aware
  recommendations, generate the dashboard, and stop for site-wide review. Discover no additional websites.
- **Selected-focus teardown** — the active chapter contains approved target and recommendation IDs
  after compatibility review and explicit human approval. Inspect only that target/region.
- **Focused pattern follow-up** — one target/block lacks suitable options. Find alternatives for that
  immutable ID without reopening site direction or modifying unrelated recommendations.

A pinned set, "find no more sites", existing BRAND/DESIGN direction, prior moodboard, or completed
teardowns are constraints/evidence—not approval. They never authorize Round 2. Existing verified
teardowns/screenshots should be reused during provided-reference concept discovery before browsing;
revisit a pinned URL only for a material classification gap.

The user's explicit target page/surface and reference constraints outrank STATUS, ROADMAP, prior
next-actions, and inferred opportunities. Ask only for a missing target, missing pinned URLs, and
research depth. Manual Aside prompt relay is the default transport; do not offer another browser
unless the user requests an alternative or Aside is unavailable.

Resolve disk paths from the active session checkout. A worktree mission writes to that worktree's
`brain/`; it never redirects to the main checkout or another worktree because older dirty research
lives there.

Every mission carries a stable mission ID; checkout root, brain root, branch and HEAD; site goal;
stable family/target/block IDs; routes; content goals/jobs; available media; and reference law. Aside
writes the derived `brain/research/page-recommendations.json` packet and prints the identical fallback.
It never writes `brain/research/ui-decision-draft.json`, a human selection, approval, or build lock.

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
5. **Write to disk**: canonical evidence plus derived `brain/research/page-recommendations.json`.
6. **Page-aware output**: a site direction, global-shell candidates, and a recommendation or material
   blocker for every unique page/repeated family, using shared scope labels and evidence/asset fields.
7. **Return**: print the identical recommendation packet and summary block.

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

The plugin receives the paste, validates (does concepts.md parse? screenshots present?), explicitly
invokes Project Dashboard to generate/refresh `brain/project-dashboard.html`, presents its Research /
Moodboard view, then stops for a decision. Dashboard generation is required at this checkpoint; the
dashboard renders evidence and never chooses. It shows one concept and one site at a time with large
grouped captures, live-site links, capture-quality warnings, and first-class video evidence. A full
Markdown dump or flat image gallery does not satisfy this checkpoint. Browser-local review notes are
explicitly non-canonical. Hooks and Save Session remain non-generators.

The dashboard presents site direction, global shell, and every unique page/repeated family. The human
reviews everything, then uses one universal submit action. Dashboard writes provisional
`brain/research/ui-decision-draft.json`; Claude or Codex reports the full combination as `compatible`,
`compatible_with_adaptation`, or `conflicting` and discusses material conflicts. A draft is not canon
and authorizes nothing.
Explicit human approval records final target/recommendation IDs in the active chapter's Markdown owner.

## 5. Round 2 — DEEP TEARDOWN

Round 2 begins only after the active chapter records approved target and recommendation IDs following
Section 4 review. A draft, design direction, pinned list, or prior teardown is insufficient.

### 5a. ROUND-2 DIRECTIVE (plugin composes → human pastes into SAME Aside chat)
```
═══ ROUND-2 DIRECTIVE · <project> ═══
APPROVED TARGET: <target-id>
APPROVED RECOMMENDATION IDS: <recommendation-ids>
SCOPE: <scope> · BLOCK IDS: <block-ids>
CONTENT GOAL/JOB: <content-job>
GO DEEP only on the approved target/region and selected evidence. Do not reopen the site-wide direction
or another page family. Stop by saturation, not a target count.

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
## Video evidence
<role · provider/page URL · delivery · poster/frame · autoplay/muted/loop/playsinline/controls · responsive and reduced-motion fallback · official embed availability | none>
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
- `LIVE VIEWPORT COMPLETE` requires a bounded visual-readiness gate: `document.fonts.ready`, decoded
  visible images, hero-video metadata and a usable frame (`readyState >= 2`), no visible loader/skeleton,
  and two stable layout samples. Network idle alone is insufficient. Timeout becomes PARTIAL/loading-state.
- Observe live motion before pausing it for a stable representative frame. Record video role, provider/page
  URL, delivery, poster/frame, playback flags, responsive and reduced-motion fallback, and official embed
  availability. Never download a reference stream or classify its frame as an image-led concept.
- Validate mobile from actual dimensions/aspect and recorded CSS viewport, not a filename.
- Visible computed use establishes brand color; root/framework/widget variables alone do not.
- Capture recovery uses fresh light contexts, native scroll and stable section targets, then records
  exact blockers rather than looping indefinitely.
- A per-site manifest records desktop/mobile status, files, fallbacks and gaps.
- Readiness is saturation-based. Return `WITH DOCUMENTED GAPS` when gaps cannot materially change
  convergence; return `NOT READY` only for material unresolved uncertainty.

### 5e. Provided-reference summaries

Before approval, the provided-reference discovery relay reports concept groups sourced only from the
pinned set, reused/refreshed evidence, page-aware recommendations, and `NEXT: SITE-WIDE REVIEW REQUIRED`.
After approval, the provided-reference teardown relay reports pinned sites and blockers; desktop and mobile capture-status counts;
convergence, site-specific moves and conventions; files and honest gaps; saturation reasoning; and
one readiness verdict: ready, ready with documented gaps, or not ready with the material uncertainty.
The block shapes live in `skills/ui-research/references/round-formats.md` and are rendered verbatim by
Variants C and D.

### 5c. ROUND-2 SUMMARY BLOCK (Aside prints → human pastes to the plugin)
```
═══ ROUND-2 SUMMARY · <project> · target <target-id> ═══
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

### 5f. Focused pattern follow-up

When one exact target/block needs more alternatives, compose Variant E with its immutable IDs, content
job, current candidates, constraints, reference boundary and narrow question. Merge by stable IDs into the
same packet. Do not reopen site direction. An exact known URL/region whose mechanics are unclear belongs
to Inspect Component, not focused discovery.

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
  UI Research renders from canon: open discovery, pinned-site discovery, approved-target teardown,
  selected provided-reference teardown, and focused pattern follow-up variants plus their sources.
- **`skills/ui-research/references/round-formats.md`**: the relay/file formats shared by both sides.
- **`skills/ui-research/SKILL.md`**: selects the entry mode, renders the Aside mission, ingests
  evidence, and stops before Style Lock or Build Page.
