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

## Required context for every site-wide mission

Every rendered discovery mission includes these sections before its task. Use concise canon summaries,
not raw file dumps, and append the PAGE_RECOMMENDATIONS packet contract to the paste prompt.

```
ACTIVE CHECKOUT IDENTITY
- Mission ID: <mission-id>
- Checkout root: <checkout-root>
- Brain root: <brain-abs>
- Branch: <branch>
- HEAD: <head>

SITE AND PAGE MAP
- Site goal: <site-goal>
- Page families and routes: <page-families>
- Targets with stable target IDs, content goals, and content jobs: <targets>

ASSET AVAILABILITY
<available-media>

RECOMMENDATION LAW
Return an evidence-backed site direction, global shell candidates, and at least one base whole-page
recommendation (or repeated-page-family recommendation for a repeated family), or an explicit material
blocker, for every target. Connected-sections and one-section candidates are optional refinements after
that base and never replace it. Use only these scopes: whole-page, connected-sections, one-section,
repeated-page-family, global-shell. Preserve every supplied family, target, and block ID.
Write the derived packet to <brain-abs>/research/page-recommendations.json and print the identical packet.
Never create a human selection or build lock.
```

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
- Derived recommendation packet → <brain-abs>/research/page-recommendations.json

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

## Variant B — ROUND 2 (APPROVED TARGET TEARDOWN)

Paste into the SAME Aside chat only after site-wide review, Claude/Codex compatibility checking, and
explicit human approval identify the exact approved target and recommendation IDs.

```
PROJECT-PROTOCOL DESIGN RESEARCH — ROUND 2 (TEARDOWN) — <project>

Run the ui-research skill you have installed (same chat as Round 1). This directive is the task.

═══ ROUND-2 DIRECTIVE · <project> ═══
APPROVED TARGET: <target-id>
APPROVED RECOMMENDATION IDS: <recommendation-ids>
SCOPE: <scope> · BLOCK IDS: <block-ids>
CONTENT GOAL/JOB: <content-job>
GO DEEP only on the approved target/region and the selected evidence. Do not reopen the site-wide
direction or another page family. Stop by saturation, not a target count.

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

═══ ROUND-2 SUMMARY · <project> · target <target-id> ═══
Sites torn down (<count>): <name, name, …>
CONVERGENCE: Type · Color · Motion · Hero · Rhythm · Imagery (what the best examples share)
CONVENTIONS: FOLLOW <…> | DEVIATE <…> | REFUSE <…>
FILES: brain/research/teardowns/<k> · brain/moodboard/<k> shots
═══ END ROUND-2 ═══
```

### Placeholder sources (Variant B)

```
<project>         ← brain/BRAND.md ## Product · Name  (also brain/DESIGN.md frontmatter name:)
<target-id> <recommendation-ids> <scope> <block-ids> <content-job>
                  ← approved site-wide/page decision recorded in the active chapter after review of
                     brain/research/ui-decision-draft.json; a draft alone is invalid
<brain-abs>       ← this project's brain/ absolute path (e.g. /Users/…/<project>/brain)
<slug> <count> <k>  ← Aside fills at run time — never a preset target (Spec §1)
```

---

## Variant C — PROVIDED REFERENCES (CONCEPT DISCOVERY)

Use when the user pins the complete reference set but has not explicitly selected a research concept
or blend. This is a closed Round 1: concepts come only from the supplied sites.

```
PROJECT-PROTOCOL UI RESEARCH — PROVIDED REFERENCES CONCEPT ROUND — <project>

Run the ui-research skill you have installed. This prompt is the complete project mission.

PROJECT CONTEXT
- Target page/surface: <target>
- Brand/design constraints (not a selected concept): <design-summary>
- Audience and page goal: <audience-goal>
- Refusals: <refusals>

PINNED REFERENCE SET — CLOSED CONCEPT DISCOVERY
<pinned-urls>

SCOPE LAW
Use every pinned URL and no other website. Do not discover replacements, competitors, award
examples, agency work, or adjacent references. The supplied sites constrain the evidence pool; they
do not mean a concept has been selected. Group only these sites into as many genuinely distinct
homepage/page concepts as the evidence supports.

REUSE FIRST
Existing verified teardowns and screenshots may already live under <brain-abs>/research/ and
<brain-abs>/moodboard/. Reuse them before browsing. Browse a pinned URL again only when a material
concept-classification gap remains, and state the gap. Never reopen or weaken verified evidence just
to produce concept groups.

FOR EACH CONCEPT
- Name and emotional read
- Representative pinned sites and evidence files
- Hero pattern
- Navigation pattern
- Page rhythm
- Imagery/video treatment
- Type and motion character
- Strengths, risks, and fit against the project constraints

DEPTH
research depth: <research-depth> — <depth-meaning>

WRITE TO DISK
- Concepts → <brain-abs>/research/concepts.md (preserve existing evidence history)
- Evidence → <brain-abs>/moodboard/
- Derived recommendations → <brain-abs>/research/page-recommendations.json

RETURN
Print the PROVIDED-REFERENCE CONCEPT SUMMARY even when disk writes succeed. Stop after the summary.
Do not select, blend, tear down a chosen concept, write conventions, run Style Lock, or build a page.

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

### Placeholder sources (Variant C)

```
<project> <target> <audience-goal> <design-summary> <refusals> <pinned-urls>
<research-depth> <depth-meaning> <brain-abs> ← same canon/invocation sources as the other variants
<count> <evidence> ← Aside reports actual output; never preset
```

---

## Variant D — SELECTED PROVIDED REFERENCES (CONSTRAINED TEARDOWN)

Use only when the user pins the complete reference set AND the active chapter records explicit human
approval of the exact target and recommendation IDs after compatibility review. A submitted draft alone
is insufficient. This is selected-focus teardown, not concept discovery.

```
PROJECT-PROTOCOL UI RESEARCH — PROVIDED REFERENCES — <project>

Run the ui-research skill you have installed. This prompt is the complete project mission.

PROJECT CONTEXT
- Target page/surface: <target>
- Approved target/recommendation IDs: <approved-focus>
- Audience and page goal: <audience-goal>
- Existing design system: <design-summary>
- Refusals: <refusals>

PINNED REFERENCE SET — CLOSED
<pinned-urls>

SCOPE LAW
Inspect every pinned URL and no other website. Do not discover replacements, competitors, award
examples, agency work, or adjacent references. A pinned list is the user's scope boundary, not a
target count. If a site is blocked, report the blocker and continue with the remaining pinned sites.
Scope each teardown to <target>; do not inspect unrelated inner pages.

DEPTH
research depth: <research-depth> — <depth-meaning>

TEARDOWN CHECKLIST (per pinned site)
- Type: fonts actually loaded (`document.fonts`), weights, pairing, scale
- Color: computed colors from visible representative elements; separate brand-used colors from
  framework/plugin defaults and widget/consent/form noise
- Motion: detected libraries/network/runtime plus actual behaviors
- Hero: medium, composition, interaction, responsive changes
- Rhythm: section sequence and transitions for the target page
- Imagery/video: treatment, crops, masking, delivery
- Navigation, mobile, accessibility, reduced motion, performance implications
- FOLLOW / DEVIATE / REFUSE evidence for this project

EVIDENCE INTEGRITY
- Before a `LIVE VIEWPORT COMPLETE` capture, pass a bounded VISUAL READINESS gate: await
  `document.fonts.ready`; ensure visible hero/content images are complete and `decode()` succeeds;
  ensure hero video has metadata and `readyState >= 2` with a representative frame; confirm no
  visible skeleton/loader; and observe two stable layout/viewport samples. Network idle alone is insufficient.
  If readiness times out, label the capture PARTIAL/loading-state and record why.
- Observe and record live motion before pausing animations/media for a stable representative frame.
- Record target page, inspection date, desktop/mobile viewport, capture method and capture status.
- Classify visual evidence as `LIVE VIEWPORT COMPLETE`, `LIVE VIEWPORT PARTIAL`,
  `MEDIA FALLBACK ONLY`, or `NO VISUAL CAPTURE`. Downloaded media is not a screenshot.
- Name fallbacks `<slug>-<position>-media-fallback.png`; never count them as live captures.
- Validate mobile from real dimensions/aspect plus the recorded CSS viewport, not the filename.
  Preserve but rename an invalid one `*-mobile-invalid-desktop-capture.png`.
- On an unstable screenshot channel, save DOM/runtime evidence, retry in a fresh light page/context,
  dismiss overlays, pause media/animation, restore native scrolling, and use stable section targets.
  After distinct recovery strategies fail, record the exact blocker instead of looping.
- Separate `EVIDENCE`, `INFERENCE`, and `UNRESOLVED GAPS`; never promote inference into convergence.
- In each Color section write `BRAND-USED COLORS`, `FRAMEWORK/PLUGIN DEFAULTS`, and
  `WIDGET/CONSENT/FORM NOISE` explicitly.
- Maintain one manifest row per pinned URL with desktop/mobile status, live files, fallbacks and gaps.
- For video record role, provider or page URL, delivery type, poster/frame, autoplay/muted/loop/
  playsinline/controls, responsive behavior, reduced-motion/static fallback, and whether an official
  embed is permitted. Never download a reference stream or treat its screenshot as an image concept.

WRITE TO DISK
- Preserve research history + pinned URLs → <brain-abs>/research/concepts.md
- Teardowns → <brain-abs>/research/teardowns/<slug>.md
- Conventions → <brain-abs>/research/conventions.md
- Screenshots + manifest → <brain-abs>/moodboard/

RETURN
Print the PROVIDED-REFERENCE SUMMARY block even when disk writes succeed.

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

### Placeholder sources (Variant D)

```
<project>        ← BRAND/DESIGN project name
<target>         ← user's explicit page/surface/region; never STATUS next action when they differ
<approved-focus> ← approved target and recommendation IDs from active chapter; BRAND/DESIGN or
                    brain/research/ui-decision-draft.json alone is invalid
<audience-goal>  ← target page brief/content plus relevant BRAND audience
<design-summary> ← concise approved DESIGN identity/expression; never raw full-file paste
<refusals>       ← relevant DESIGN/BRAND refusals
<pinned-urls>    ← exact user-confirmed URL list; no inferred additions
<research-depth> <depth-meaning> <brain-abs> ← same sources as Variants A/B
<slug> <k>       ← Aside reports actual output counts
```

---

## Variant E — FOCUSED PATTERN FOLLOW-UP

Use only after the dashboard/user identifies one target or page-map block whose current alternatives are
insufficient. This searches for additional suitable patterns; an exact known URL/region whose mechanics are
unclear belongs to Inspect Component instead.

```
PROJECT-PROTOCOL UI RESEARCH — FOCUSED PATTERN FOLLOW-UP — <project>

Run the ui-research skill you have installed. This is a narrow update to an existing recommendation packet.

ACTIVE CHECKOUT IDENTITY
- Mission ID: <mission-id>
- Checkout root: <checkout-root>
- Brain root: <brain-abs>
- Branch: <branch>
- HEAD: <head>

FOCUSED PATTERN FOLLOW-UP
- Target ID: <target-id>
- Block IDs: <block-ids>
- Scope: <scope>
- Content goal/job: <content-job>
- Current recommendation IDs: <current-recommendation-ids>
- Narrow question: <followup-question>
- Reference boundary: <reference-boundary>
- Brand/design constraints: <design-summary>

Find only materially different, evidence-backed alternatives for this target/block. Do not reopen the
site-wide direction, modify another target, silently replace an existing candidate, or broaden into a new
sweep. Preserve all stable IDs already present. New recommendation and evidence IDs must be deterministic
under the target ID. Return live URLs, screenshot/video/motion evidence, content fit, dependencies, asset
requirements, confidence, and material gaps.

UPDATE + RETURN
Merge by stable IDs into <brain-abs>/research/page-recommendations.json. Print the complete updated
PAGE_RECOMMENDATIONS packet so paste fallback remains self-sufficient. Never create a human selection or
build lock.
```

### Placeholder sources (Variant E)

```
<project> <mission-id> <checkout-root> <brain-abs> <branch> <head>
<target-id> <block-ids> <scope> <content-job> <current-recommendation-ids> <followup-question>
<reference-boundary> <design-summary> ← active worktree packet + approved canon + user's exact request
```
