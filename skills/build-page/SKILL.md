---
name: build-page
description: Compose a whole page (marketing or dashboard) through a long iterative conversation against the already-locked brief and canon. Use when an entire page needs to be designed and written section by section. Use when the user says "build the homepage", "build the pricing page", "build the about page", "compose page X", "wire up the X page", "build the dashboard overview page", "build the settings page", or invokes "/build-page".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*,find:*,cat:*,grep:*,test:*,mkdir:*), AskUserQuestion, Task, Skill, WebFetch
---

# Build Page

The compositional sibling to `build-component`. Where `build-component` writes one atomic thing (a button, a card, a hero block), `build-page` composes a whole page — section by section, in a long iterative conversation — working from the marketing brief or dashboard spec that already exists in canon. Calls `build-component` as a subroutine whenever a section needs a net-new primitive. Writes the actual page file when the conversation gets there.

A single page build can span 30–50 turns. That is normal and intended. The session is long because pages deserve discussion: the user iterates on the architecture, throws external references at the agent ("here's a hero I like from Stripe"), changes their mind about sections, settles on components one at a time. The skill's job is to stay productive across that conversation, not to race toward an exit.

Everything else about this skill is the same as every other skill in the plugin. WORKLOG entries on decisions. BRIEF blocks at meaningful locks. INDEX.md updates inline when a new route ships. `design-check` chains automatically after the page file is written. No state files. No scratch folders. No special mode machinery. The canon and WORKLOG carry whatever the next session needs.

---

## When this fires

- "Build the homepage", "build the pricing page", "build the about page", "compose page X", "wire up the X page", "build the marketing homepage".
- "Build the dashboard overview page", "build the settings page", "build the team page", "build the analytics page".
- Slash command: `/build-page` (optionally with a slug: `/build-page home`).

### Does NOT fire for

- A single component request ("build a button", "I need a KPI tile", "make a hero block") → `build-component`.
- A tiny edit to an existing page ("change the H1 copy", "swap the screenshot") → direct edit + `design-check` as the post-gate.
- The first-ever bootstrap of a project (no `CLAUDE.md` / `BRAND.md` / `DESIGN.md`) → `init-project` → `design-direction` → `marketing-brief` (if marketing surface) first.

### Skip conditions

- User says "skip build-page", "just write the page file", "no gate, draft only" → single-shot mode: read canon, generate the whole page, show one preview, write on approve. Use only when the user is unblocking themselves.

---

## What it produces

One real page file at the location dictated by `brain/STRUCTURE.md` (typically `src/app/(marketing)/<slug>/page.tsx` for marketing or `src/app/(dashboard)/<slug>/page.tsx` for dashboard, but read STRUCTURE.md — don't assume). Plus zero-to-many net-new component files written by inline `build-component` calls during the per-section work. Plus an INDEX.md entry for the new route.

Copy is inlined directly in the page JSX, sourced verbatim from `brain/marketing/copy/<slug>.md` (marketing) or the dashboard brief. **No intermediate content mirror file is ever created** — not `lib/marketing-content.ts`, not `data/copy.ts`, nothing.

---

## Required canon

Before this skill can do useful work, these must exist:

- `brain/CLAUDE.md`, `brain/BRAND.md`, `brain/DESIGN.md`, `brain/FUNDAMENTALS.md`, `brain/STRUCTURE.md`.
- For **marketing pages**: `brain/marketing/CONTENT.md`, `brain/marketing/SITEMAP.md`, `brain/marketing/briefs/<slug>.md`, `brain/marketing/copy/<slug>.md`, `brain/marketing/MEDIA.md`, `brain/marketing/layouts/<slug>.md` *(soft prerequisite — see below)*.
- For **dashboard pages**: a brief (a row in `brain/ROADMAP.md`, a file at `brain/specs/<slug>.md`, or a one-paragraph spec the user types inline).

**Marketing canon prerequisite logic:**
- **Hard halt** if `brain/marketing/briefs/<slug>.md` OR `brain/marketing/copy/<slug>.md` is missing → *"Marketing brief/copy missing for `<slug>`. Run `marketing-brief` first (or add the missing files), then re-invoke."*
- **Warn and continue** if `brain/marketing/layouts/<slug>.md` is missing but brief + copy exist → surface a warning: *"Note: `layouts/<slug>.md` not found — proceeding without block-level wireframe intent. Layout decisions will be made in conversation."* The per-section workflow skips the layouts read step and relies on brief + copy alone. This covers the common case where `marketing-brief` has run through Phase 6 (copy written) but Phase 7 (layouts) is not yet complete.

If a dashboard page has no brief → halt and ask the user to type a one-paragraph spec inline. Do not invent the spec.

---

## The protocol

When this skill fires:

1. **Ask which page** (if not in the user's message). Use AskUserQuestion with options drawn from `brain/marketing/SITEMAP.md` rows (for marketing tier) or from existing dashboard routes (for dashboard tier).

2. **Detect tier** from the slug location in STRUCTURE.md + user wording. Confirm once if ambiguous.

3. **Read everything for that page.** Full canon for the tier — see "Required canon" above. **If `brain/STRUCTURE.md` is missing, do not proceed blind:** run `build-component`'s Phase 1 structure detection first (`Skill("build-component")` structure-detection pass, or replicate its detection — glob folders, read tsconfig paths, confirm with user, write STRUCTURE.md), then continue. **Also read `brain/TASTE.md` (if present) and the global ledger (`~/.claude/TASTE.md`):** apply entries at or above `apply_threshold` (default 0.8) to the first-draft plan and every section — the whitespace, the accent choice, the voice, the beloved elements — so the owner sees their taste already applied instead of correcting it a fifth time. Mid-band entries (0.4–0.8) become questions to ask up front. Sub-delegate the read to a fast Task agent so the orchestration context stays lean.

4. **Append the session-open line to WORKLOG.** Single line in the canonical format:
   ```
   [HH:MM] decided: build-page started for /<slug> (<tier>)
   ```
   This serves two purposes: it disarms the cleared-state PreToolUse hook warning that would otherwise fire on the first Edit/Write later in the session, and it gives `save-session` something to consume even if the build doesn't complete this session.

5. **Surface a starting analysis** — one paragraph in chat. Template:
   ```
   Page: <name> · /<slug> · tier: <marketing | dashboard>
   For: <audience>
   Intent: <single intent from brief>
   Primary CTA: <button label → href>

   Content blocks already locked in the brief:
     1. <section name> — <one-line intent>
     2. <section name> — <one-line intent>
     …

   Visual anchors from MEDIA.md (marketing only):
     §1 hero → <anchor>
     …

   Existing components that look reusable for this page:
     <component name> @ <path>
     …
   ```
   Wait for "yes, that's right" or a correction before proposing a starting plan.

6. **Propose a starting plan** — numbered section list with rhythm tags. NOT as code, NOT as JSX, just a vertical outline:
   ```
   1. Hero        — claim + primary CTA + visual anchor       · loud
   2. Trust strip — 3 short claims, answer trust early        · calm
   3. How it works — 3-step narrative                         · calm
   4. Features   — workflow-stage grid (Capture / Deliver…)   · loud
   …
   ```
   Marketing pages use calm/loud rhythm tags. Dashboard pages use scan/focus/meta density tags.

   **Composition-variety rule (marketing archetype):** no two adjacent sections may share the same layout grammar. Vary across the vocabulary — split (text/media two-col) · full-bleed band · bento/grid · editorial-centered · sticky/scroll-linked — and alternate direction (image-left → image-right → centered). Two identical section shapes back-to-back read as monotone (the "bootstrap-era" tell). The `layouts/<slug>.md` rhythm rules (container width, background, direction) already encode this — honor them. **Dashboard archetype is the opposite:** repeat one grammar for scannability. (Which applies is set by DESIGN.md `archetype:`.)

7. **Iterate freely with the user.** No phase gates. No 5-iteration cap. The conversation goes as long as it needs to. Push-back examples: *"drop §6"*, *"swap §5 and §6"*, *"split §4 into two sections"*, *"add a logo wall after the hero"*. Revise the plan, re-show it, ask again.

8. **When the user locks the plan, append a BRIEF block.** This is the cardinal "lock-before-cascade" rule. Format per `save-session` Step 6:
   ```markdown
   ---

   ## v1.X — YYYY-MM-DD HH:MM · Claude Code

   build-page locked architecture for /<slug>:
   <N> sections — <one-line rhythm summary>
   Strategy will be drawn from these existing components: <list>
   Net-new components anticipated: <count, names>
   ```
   Also append a WORKLOG line: `[HH:MM] decided: build-page plan locked for /<slug> — N sections`.

9. **Per-section work** — see `references/per-section-workflow.md`. For each section, in order: surface content, propose components, accept external references if dropped, decide strategy (reuse / adapt / build new). When a section requires a net-new primitive, invoke `build-component` explicitly:
   ```
   Skill("build-component")
   ```
   After each section write completes (whether reuse, adapt, or new-build), invoke `design-check` explicitly:
   ```
   Skill("design-check")
   ```
   Both calls are unconditional — no "if host supports it" guard. Sequential, one section at a time, even if two are independent.

10. **When all sections have real component paths**, do the wire-up. Write the actual page file:
    - **Marketing tier**: React Server Component, `export const metadata` for SEO, no top-level `"use client"`. Client behavior in small child components.
    - **Dashboard tier**: client component is fine; loading / empty / error / partial state branches per data hook.
    - **Copy inlined directly** from `copy/<slug>.md` or the dashboard brief.
    - **Top-of-file canon-pointer comment** as the sync contract:
      ```tsx
      // Copy mirrors brain/marketing/copy/<slug>.md — when that file changes,
      // propagate the update here. Do NOT inline new copy without updating
      // the canon first.
      ```
    - **No `lib/marketing-content.ts` mirror.** Ever.

11. **Update `brain/docs/INDEX.md` inline** — add the new page route to the index in the appropriate section. This satisfies the `save-session` Step 4 contract so the next save doesn't plant a reminder.

12. **`design-check` is explicitly invoked** after the page file is written via `Skill("design-check")` (backed by the PostToolUse hook — double-fire accepted, design-check is idempotent). Let it run its 8 steps. Surface any flagged tokens, banned words, or cross-tier violations to the user. Fix in place where mechanical; ask where it's a judgment call.

12.5. **Self-critique gate — look at it before the user does.** Before closing, review your own output against the design *intent*, not just the token scan.
    - **If a render/preview is available** (the Aside browser per `calibrate`'s detection, the Claude Code preview pane, or the Codex browser): render the page, screenshot it, and critique the screenshot against `brain/moodboard/` and the page brief — hierarchy, spacing, rhythm (did two adjacent sections come out the same shape?), text-over-image contrast, whether it delivers the register. Fix what you find **before** surfacing to the user.
    - **If no render capability:** do a structured self-review against the brief, the `FUNDAMENTALS.md` pre-ship checklist, and `brain/moodboard/notes.md`.
    This is the gate between "compiles + token-clean" (design-check, step 12) and the owner's own reaction. Report what you caught and fixed — don't hand over output you haven't looked at.

13. **Closing.** Append the skill-complete line to WORKLOG, matching the canonical phrasing from `references/conversational-shape.md`:
    ```
    [HH:MM] decided: build-page complete for /<slug> — N components used (R reused, A adapted, N built)
    ```
    Then print the end-of-skill summary (see "Output shape" below). The session ends when the user closes the chat or types "save" / "save session". No special handoff machinery — STATUS.md Next Actions + WORKLOG carry whatever a future session needs.

---

## External references

When the user drops a URL, pasted component code, or a screenshot during section work — see `references/per-section-workflow.md`, section "External reference adoption". Short version: fetch / parse, analyze the visual pattern + tokens it uses, cross-check against DESIGN.md (do our tokens cover it?) + BRAND.md (does the voice fit our archetype?) + the section's content (does the layout serve what we're saying?), recommend adopt / adapt / reject, and hand off to `build-component`'s existing `adopt-external` sub-mode if accepted.

---

## Structural-change gate

Before proceeding when the planned page build is **structural** — defined as: touches `brain/BRIEF.md` (beyond the plan-lock append), touches `brain/ROADMAP.md`, or involves writing files across multiple tiers simultaneously — invoke the discipline skill first:

```
Skill("change-check")
```

Normal single-page builds with a plan-lock BRIEF append do NOT trigger this gate. It fires when the scope has expanded to affect the project's roadmap, cross-tier refactors, or multi-file canon changes beyond the expected BRIEF.md append + INDEX.md update.

---

## Hard rules

- **No content mirror file.** Copy is inlined in the page JSX, sourced verbatim from `copy/<slug>.md` or the dashboard brief. NEVER create `lib/marketing-content.ts`, `data/copy.ts`, `lib/content.ts`, or any equivalent runtime mirror. If the project already has one from earlier ad-hoc work, leave it alone — note it as orphaned in the output for follow-up cleanup.
- **Marketing pages are RSC + `generateMetadata` by default.** No top-level `"use client"`. Client behavior in small child components imported into the RSC tree.
- **Cross-tier imports are blocked** (inherited from `build-component`). Marketing pages never import from `app/`. App pages never import from `marketing/`. Cross-tier needs route through Generic + wrapper.
- **`build-component` is invoked for net-new components only**, not for atomic edits to the page itself. Wire-up is done directly by this skill.
- **Per-section work is sequential.** One section at a time. Even when two sections are independent, do them in order — that's the conversation shape that keeps the user oriented.
- **Lock-before-cascade.** Plan-lock writes a BRIEF block BEFORE any per-section work begins. (Cardinal rule from `brain/CLAUDE.md`.)
- **One decision per WORKLOG line.** Canonical prefix vocabulary: `decided: / fixed: / tried_failed: / found_bug:`. No multi-line entries. Timestamp `[HH:MM]` at the start of every line.
- **Canon protection — explicit list.** The following files are read-only from this skill: `brain/DESIGN.md`, `brain/STRUCTURE.md`, `brain/BRAND.md`, `brain/FUNDAMENTALS.md`, and all files under `brain/marketing/` (CONTENT.md, SITEMAP.md, briefs/, copy/, MEDIA.md, layouts/). If any of these need to change, halt and tell the user: they update canon, we resume. **Permitted writes from this skill:** appending a version block to `brain/BRIEF.md` (Step 8 plan-lock), and updating `brain/docs/INDEX.md` with the new route (Step 11). These are not "canon modifications" — they are the expected output of this skill.
- **The conversation is the state.** No state file. No scratch folder. If the session is interrupted, WORKLOG entries + STATUS Next Actions are the only resume mechanism — same as every other skill in the plugin.
- **`design-check` is explicitly invoked after wire-up** via `Skill("design-check")` and after each per-section build. Don't duplicate its 8 steps here.
- **Composition varies per section (marketing).** No two adjacent sections share a layout grammar; honor the `layouts/<slug>.md` rhythm rules. Dashboards repeat one grammar instead. Set by DESIGN.md `archetype:`.
- **Self-critique before the user sees it.** After wire-up, render + screenshot (or structured self-review if no render is available), critique against the moodboard + brief, fix, then surface. Never hand over output you haven't looked at.
- **Skip the marketing-content.ts pattern entirely.** Phase rule worth repeating: if it already exists, do not write to it.

---

## Sub-agent routing

Heavy reasoning steps delegate to Task tool sub-agents to keep the orchestration context lean:

| Step | Tier | Why |
|------|------|-----|
| Canon read + initial analysis | fast | Pure extraction |
| Reuse scan (glob + read-similar) | fast | Pattern matching |
| Plan proposal | reasoning | Judgment on section order + rhythm |
| Per-section component strategy | reasoning | Reuse / adapt / build judgment |
| External reference analysis | reasoning | Map foreign values to project tokens; voice fit |
| Wire-up code generation | reasoning | Composition + token discipline |
| Inline `build-component` calls | (delegated) | `build-component` handles its own routing |

Reasoning tier (Sonnet) is the ceiling. Never the most expensive model.

---

## Output shape (end of skill)

```
build-page — summary

Built: <page slug> (<tier>)
Sections: <N>
Strategies: <N reused, N adapted, N built new via build-component>
File written: <absolute path>

Components used:
  - <component 1> @ <path>  [reused]
  - <component 2> @ <path>  [adapted — <delta>]
  - <component 3> @ <path>  [built new via build-component]
  …

Copy source: brain/marketing/copy/<slug>.md (or dashboard brief)
Canon-pointer comment: written at file top.
INDEX.md updated: yes
WORKLOG appends: <N>
BRIEF blocks appended: <N>

design-check ran (via explicit Skill call + PostToolUse hook) — <findings or "clean">.

Next:
  → Save the session with /save-session when ready.
  → If any net-new components had missing tokens, those remain pending
    until you confirm in design-check Step 4.
```

---

## Difference from related skills

- **`marketing-brief`** — the planning pass that locks the marketing-site canon (CONTENT, SITEMAP, briefs, copy, MEDIA, layouts) ONCE near the end of a project. `build-page` is the execution pass that turns those plans into real pages — invoked per page, ongoing.
- **`build-component`** — atomic. One component at a time. `build-page` calls it inline whenever a section needs a net-new primitive. Atomic component requests from the user still go directly to `build-component`. They chain: `build-page` is the conductor, `build-component` is the player.
- **`design-direction`** — locks brand identity ONCE at the start. Upstream of every page build.
- **`design-check`** — UI write-time gate. Explicitly invoked via `Skill("design-check")` after this skill's wire-up and after each inline `build-component` call. Backed by PostToolUse hook (double-fire accepted).
- **`discuss`** — pure conversation, no writes. If the user wants to think about a page WITHOUT committing to architecture, use that first, then `build-page` to actually compose.
- **`init-project`** — bootstraps the three-folder layout. `build-page` assumes init-project + design-direction + (for marketing pages) marketing-brief have already run.
- **`save-session`** — closes the session cleanly. Consumes the WORKLOG entries this skill wrote. If a build-page session ends mid-flow, save-session writes a `Resume /build-page <slug>` line to STATUS Next Actions automatically (because WORKLOG will show an open `decided: build-page started` line with no matching `decided: build-page complete` line).

Chain: `init-project` → `design-direction` → `build-component` (per atomic piece) → `marketing-brief` (once, end of project) → **`build-page`** (per page) → `design-check` (auto) → `project-audit` (periodic).
