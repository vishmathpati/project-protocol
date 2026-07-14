# Round formats — UI Research and Aside shared contract

> Single source of truth for the relay/file formats used by the research engine.
> `ui-research` (plugin side) and `aside-skill/ui-research/SKILL.md` (Aside side) both point HERE so they
> never diverge. These shapes come from the Interface Spec v4.1 (`docs/interface-spec-research-engine.md`,
> Sections 3 + 5) and match `aside-skill/ui-research/SKILL.md` verbatim. If a format changes,
> it changes in the Interface Spec first, then here, then in both consumers.
>
> **Fill the `<...>` slots; keep the headers, fences, and field names exactly.** Do not rename a
> field or invent a block shape — the studio parses these.

## Shared page-recommendation packet

Aside writes this derived relay to `brain/research/page-recommendations.json` in the active checkout
and prints the identical JSON as the manual fallback. Markdown research remains canon; this packet
contains evidence-backed recommendations only and never human selections or build locks.

<!-- PAGE_RECOMMENDATIONS_V1_START -->
```json
{
  "schema_version": "project-protocol.page-recommendations.v2",
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
    "targets": [{"target_id": "<stable id>", "family_id": "<stable id>", "label": "<label>", "content_goal": "<goal>", "content_jobs": [{"job_id": "<target-id>--job-<slug>", "label": "<job>", "copy_excerpt": "<verbatim approved copy for this job, max ~200 chars, empty string when none exists>", "copy_ref": "<brain/marketing/copy/<file>#<job-id> or empty>"}]}],
    "available_media": [{"asset_id": "<stable id>", "kind": "image | video | icon | illustration | logo-mark | other", "status": "owned | client-provided | licensed | generated | temporary | missing", "description": "<what the asset shows, one line>"}],
    "reference_scope": {"mode": "open | pinned", "urls": ["<exact URL>"]}
  },
  "site_direction": {"recommendation_id": "<stable id>", "summary": "<plain-language recommendation>", "fit": "<why it serves the site>", "alternatives": ["<alternative>"], "evidence_refs": ["<evidence id>"], "confidence": {"level": "high | medium | low", "reason": "<reason>", "material_gaps": ["<gap>"]}},
  "global_shell": {"target_id": "global-shell", "state": "recommended | not_needed", "recommendations": [{"recommendation_id": "global-shell--<stable recommendation slug>", "scope": "global-shell", "title": "<navigation/footer/header treatment>", "dependencies": ["<page/hero recommendation id>"], "evidence_refs": ["<evidence id>"]}]},
  "targets": [{
    "target_id": "<stable id from input>",
    "recommendations": [{
      "recommendation_id": "<target id>--<stable recommendation slug>",
      "scope": "whole-page | connected-sections | one-section | repeated-page-family | global-shell",
      "affected_blocks": ["<supplied job_id>"],
      "serves_jobs": ["<job_id>"],
      "title": "<plain-language name>",
      "description": "<what the human will see and experience>",
      "fit": "<how the project content and goal map to this option>",
      "alternatives": ["<recommendation id>"],
      "compatibility_notes": {"dependencies": ["<recommendation id>"], "notes": "<research evidence that may affect combination review; no verdict>"},
      "evidence": [{"evidence_id": "<stable id>", "site": "<site>", "page": "<page/region>", "live_url": "<exact URL>", "screenshot_paths": ["<worktree-local path>"], "capture_status": "live-complete | live-partial | media-fallback-only | no-visual", "first_impression": true|false, "viewport": "<size>", "video": {"role": "<role or none>", "provider_or_page_url": "<URL or none>", "delivery": "<type or unknown>", "playback": "<flags or unknown>", "reduced_motion_fallback": "<observed, absent, or unknown>", "official_embed": "<yes, no, or unknown>"}, "motion": {"behavior": "<plain behavior>", "implementation_evidence": "<observed stack/triggers or unknown>"}, "teardown_path": "<path or none>", "evidence": "<direct observation>", "inference": "<labeled inference or none>"}],
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
is locked, no selected teardown or build is authorized. Job IDs are authored upstream in Marketing Stage A and are
immutable; copy excerpts are verbatim quotes from existing canon — Aside and the mission renderer never
invent or paraphrase them. `affected_blocks` and `serves_jobs` may reference ONLY supplied job IDs — never a
block ID that was not supplied. At most one `evidence` item per recommendation may set `first_impression` to
true; it must be the capture that best represents the site's felt look.

---

## Two governing laws (apply to every block below)

- **No hardcoded counts (Spec §1).** Nowhere in any block is a fixed target allowed — not a site
  count, not a concept count, not a teardown count. Every `<count>` / `<N>` / `<k>` slot is the
  number the field *actually* produced, saturation-driven. A `<count>` is a report of what happened,
  never a goal that was aimed at. The depth dial (quick / standard / deep) tunes appetite, not counts.
- **Paste blocks must be self-sufficient (Spec §7, fallback C).** Disk writes are an optimization; the
  guaranteed channel is the **pair** — the paste SUMMARY BLOCK plus the complete PAGE_RECOMMENDATIONS
  packet JSON. Aside prints the summary block **every round, even when the disk writes succeed**, and when
  the disk write failed it also pastes the complete packet JSON as a second block. If Aside cannot reach the
  `brain/` paths in some environment, that pair is the ONLY channel and the receiving agent must be able to
  write canon from it alone — so together they carry the full findings, not a pointer to a file.

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
IF DISK WRITE FAILED: paste the COMPLETE PAGE_RECOMMENDATIONS packet JSON as a second block below this summary.
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
NEXT: SITE-WIDE REVIEW REQUIRED
═══ END PROVIDED-REFERENCE CONCEPT SUMMARY ═══
```

## Site-wide review and approval boundary

Project Dashboard persists provisional choices only to `brain/research/ui-decision-draft.json` after the
human uses the universal submit action. Claude or Codex then checks the full combination as `compatible`,
`compatible_with_adaptation`, or `conflicting`. A draft does not authorize Round 2 or a build. Only explicit human approval,
recorded by Project Protocol in the active chapter with approved target and recommendation IDs, crosses
the gate. Aside never writes the draft, the approval, a human selection, or a build lock.

---

# Round 2 — DEEP TEARDOWN

## ROUND-2 DIRECTIVE — Project Protocol composes for the SAME Aside chat (Spec §5a)

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
## Video evidence
<role · provider/page URL · delivery type · poster/frame · autoplay/muted/loop/playsinline/controls · responsive behavior · reduced-motion/static fallback · official embed availability | none>
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
- Before a complete capture, await `document.fonts.ready`, decode visible images with `decode()`, require
  hero-video metadata and `readyState >= 2`, clear skeleton/loaders, and observe two stable layout
  samples inside a bounded wait. Network idle alone is insufficient; timeout means PARTIAL/loading-state.
- Observe live motion before pausing it for a stable representative capture. Record video role,
  provider/page URL, delivery, poster/frame, playback flags, responsive/reduced-motion behavior, and
  official embed availability. Never download a reference stream or classify its frame as an image concept.
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
