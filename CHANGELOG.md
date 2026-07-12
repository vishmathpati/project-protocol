# Changelog

All notable changes to project-protocol are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]

### Added
- **Universal Foundation.** `init-project` now inspects first, captures universal project truth once, creates only the core canon, and routes to specialist groups without asking brand, marketing, design, research, or implementation questions.
- **Universal canon templates.** Added concise templates for CLAUDE, BRIEF, STATUS, STRUCTURE ownership, WORKLOG, CHANGELOG, agenda, WONT-DO, and chapters.
- **Separated brand and visual workflows.** Added Brand Foundation and Style Lock so brand truth, research evidence, and design tokens have distinct owners. Style Lock preserves the rich real-content preview as a deterministic HTML asset.
- **Component inspection workflow.** Added Project Protocol and standalone Aside `inspect-component` skills for evidence-backed investigation of unclear external UI mechanics.
- **Adaptive marketing templates.** Added BRAND, SITEMAP, PAGE-BRIEF, and MEDIA templates and replaced the SaaS-shaped CONTENT registry with an adaptive business-neutral contract.
- **Deterministic Project Dashboard.** Added a stdlib-only generator for Project, Brand, Design, Research/Moodboard, and Build Progress tabs, with local/portable asset modes and embedded input hashes for staleness checks.
- **Tested hook scripts.** Session drift, compaction recovery, stop warnings, and post-write UI findings now live in small Python scripts instead of opaque inline shell programs.
- **Transactional migration inspector.** Added a read-only planner/target validator with fixtures for legacy, partial, and complete protocol states.
- **Structural release audit.** Release validation now checks manifests, migration presence, skill metadata, hook targets/events, retired source, and packaging debris instead of grepping historical prose or hardcoding a skill count.

### Changed
- **CEO/worker authority is chapter-scoped.** Workers may propose any chapter-required code or canon change in isolated worktrees; only CEO approval and merge establish shared canon.
- **Session continuity redesigned.** Recap is role-aware orientation; Handoff carries exact repo/worktree/branch/checkpoint identity; Save Session persists role-owned state without conflating save, completion, approval, or merge.
- **Chapter contracts expanded.** Goal, Why, Method, Done When, Plan, dependencies, constraints, carry-over, reports, and verdicts now form one durable review unit.
- **Core skill names clarified.** `session-recap` → `recap`, `audit-before-close` → `completion-check`, `audit` → `project-audit`, `discipline` → `change-check`, and `discussion-mode` → `discuss`.
- **UI research renamed and decoupled.** `calibrate` → `ui-research`; it now writes research/moodboard evidence without mutating BRAND or DESIGN and never auto-triggers for ordinary dashboards.
- **Marketing is resumable Stage A/B.** It may run whenever brand-facing work becomes relevant, owns meaning/copy/media requirements, and no longer produces layout sketches.
- **Frontend execution lanes clarified.** Brand-facing substantial pages use Build Page; conventional product/dashboard UI may follow established shadcn patterns directly; Build Component is only for a genuine missing component.
- **Design Check split into preflight/postflight.** It verifies the correct surface, existing system, changed hunks, and render evidence without replacing Style Lock or Completion Check.
- **Hooks narrowed to mechanics.** Session Start is minimal; PreCompact no longer writes timestamped backups; PostCompact routes same-role Recap; Stop only warns on likely unpersisted state; post-write scanning is centralized and deterministic.
- **Migration is fail-closed.** Legacy consolidation preserves README and customized canon, skipped semantic deltas remain incomplete, explicit files are staged, and the version is stamped only after target validation succeeds.
- **Codex metadata completed.** Every shipped skill sidecar now includes a default prompt alongside its display name and concise description.
- **Worker ownership contradiction closed.** The final worker rules now match the governing chapter-scoped authority model: required canon edits are branch proposals, while CEO approval and reconciliation establish shared truth.
- **Discovery metadata normalized.** Codex skill descriptions are concise and Build Page now advertises the substantial brand-facing lane instead of implying every dashboard page enters that workflow.
- **Git ownership rule aligned.** The Git gate now preserves chapter-scoped worker authority instead of reintroducing the retired code-plus-chapter-only restriction; the structural audit guards both authority-bearing skills against regression.

### Fixed
- **Migration semantic validation.** Full CLAUDE modernization now starts from the concise v5 structure, preserves project-specific guardrails, and rejects stale one-tool-only, per-action WORKLOG, unconditional pull/push, embedded hook-index, situation-router, and pre-task-classification rules before stamping success.
- **Custom CLAUDE instructions are protected.** Migration now inventories every existing block and asks before moving or removing user-authored, project-specific, personal, or unrecognized content. The default is to keep it verbatim; conciseness and “full modernization” never imply deletion authority.

### Removed
- **Obsolete init-project mega-flow.** Removed the old discovery/modernize/design/docs phases and `SITUATIONS.md` generation; specialized skills own those concerns.
- **Monolithic `design-direction`.** Its brand diagnosis moved to Brand Foundation, token/preview work to Style Lock, research to UI Research, and implementation to Build Page/Component. Forced three-direction generation was removed.
- **Unsafe/duplicated marketing references.** Removed layout ownership, forced SaaS structures, and fictional proof/testimonial guidance.
- **Hook noise and mutation.** Removed UserPromptSubmit classification, PreToolUse WORKLOG warnings, SubagentStart/Stop logging, cleared-WORKLOG assumptions, and backup-file accumulation.

## [4.1.0] — 2026-07-11

The research-engine release. `calibrate` grows from a single moodboard capture into a **two-round, human-relayed design-research engine** driven by an Aside browser agent — a SWEEP that maps the field into named concepts, a human checkpoint that picks or blends one, then a DEEP TEARDOWN that forensically autopsies the chosen concept's best real examples (real fonts via `document.fonts`, real palette from `:root`, real motion stack from `window` globals + network). Fixes the deepest remaining gap: directions were proposed from training-data averages; now they are grounded in a swept, forensically-verified field map. Governing law throughout — **no hardcoded counts**; every quantity is saturation-driven.

### Added
- **Aside `design-research` skill (installed once into Aside).** `aside-skill/design-research/SKILL.md` is Aside's whole brain for research: the two-round model, the saturation law, the tier map (ceiling/skeleton/parts/type-color; Pinterest texture-only), traversal moves (awards + competitors spine; agency-portfolio mining as a bonus), the technical-detection cheatsheet (GSAP/Lenis/Locomotive/Framer/Three.js signatures, `document.fonts`, `:root` palette dump, video-hero-via-network, page-builder tells), the site-autopsy checklist, robustness rules (skip bot walls/CAPTCHAs, decline cookie walls, viewport-by-viewport capture on scroll-jacked sites, incremental disk writes), and the two summary-block output contracts.
- **`mission-prompt-template.md` + `round-formats.md`.** The per-project prompt `calibrate` fills from canon (Round-1 sweep + Round-2 teardown variants, placeholders mapped to canon sources), and the shared single-source block/file formats.
- **`brain/research/` canon.** `concepts.md` (Round-1 field map) and `teardowns/<slug>.md` (forensic per-site autopsies), read by `design-direction` Phase 5 and `build-page`'s external-reference cross-check.
- **`BRAND.md` → `## Product` → Niche field** — the industry the sweep researches (previously only in prose; the engine keys off it).
- **`DESIGN.md` frontmatter `research_depth` (quick/standard/deep)** — tunes Aside's sweep appetite + teardown thoroughness. Explicitly not a count. Asked at `init-project` Phase 4 beside the archetype question.

### Changed
- **`calibrate` rewritten as the plugin-side orchestrator** of the two-round engine: generate Round-1 sweep prompt from canon → user relays to Aside → ingest concepts → checkpoint with the user (pick/blend, written to `BRAND.md` Decisions log + Locked-direction seed) → generate Round-2 teardown directive → ingest → fold into `moodboard/notes.md` + an evidence-backed FOLLOW/DEVIATE/REFUSE audit → hand back to `design-direction` Phase 5. Three transports on one file contract (manual relay primary; MCP repl and pure-paste fallbacks). Prereqs gate, skip path, sub-agent routing, and Rule 7 all preserved. Extracted reference values are evidence *for* tokens, never copied *as* tokens.
- **`design-direction` Phase 4/5 wired to the two-round pass.** Phase 5 also reads `brain/research/concepts.md` and `brain/research/teardowns/`; Rule 7 made explicit — ≥1 direction departs from every concept found.
- **`marketing-brief` gains an optional per-page convention check** at brief-writing time, sourced from a targeted saturation-driven Aside call scoped to one page type.

### Removed
- **`edit-plugin` no longer ships to users** — it moved from `skills/edit-plugin/` to the repo's workshop-only `.claude/skills/edit-plugin/`. It is a plugin-*developer* tool (the discipline gate for editing this plugin's own source); end users who install project-protocol to build their own product never edit the plugin, so shipping it was noise. It still auto-loads when a developer opens this repo. Shipped skill count is now **26** (was 27). `init-project`'s generated skill index + situation router no longer list `edit-plugin`.
- **Cowork support removed.** The plugin is now Claude Code + Codex only. Deleted: the Cowork no-push git machinery (git Step 7 setup, save-session branch (c), push-snippet emission), three-way tool detection (unknown hosts now stamp `· Agent` and are treated as full-capability), the Cowork README install section, and bump-version.sh's `--validate` Cowork-upload checks. The zip-era distribution (build.sh / install.sh / dist/) was removed in the same release. Legacy `cowork/` FOLDER references in migrate-to-brain are unaffected — that is the old layout's folder name, not the tool.

## [4.0.0] — 2026-07-11

The design-engine release. Adds an archetype-driven design rulebook, a calibration/moodboard step (`calibrate`, the 27th skill), a confidence-scored taste ledger (`TASTE.md`), motion/image/build-order/done-checklist craft canon, and fixes the orchestration wire so UI chapters actually route through the design skills. Also fixes Codex skill discovery.

### Fixed
- **Codex loaded zero skills — fixed.** `.codex-plugin/plugin.json` was missing the `"skills": "./skills/"` pointer; Codex does not auto-discover a plugin's root `skills/` the way Claude Code does (only `hooks/hooks.json` is auto-checked), so no skills reached Codex users. Added the `skills` + `hooks` pointers per the official openai/codex plugin spec. Also declared calibrate's Aside MCP dependency (`dependencies.tools`) in its `agents/openai.yaml` so Codex auto-installs and wires it.

### Changed
- **`build-component` now classifies buy-vs-build by component kind.** Phase 3 first asks whether the piece is a commodity/accessibility-critical primitive (→ reuse or a proven headless base, never hand-rolled a11y) or a brand-expressive component (→ built bespoke on marketing/content archetypes; external references inform craft level only, never installed as the aesthetic).
- **`build-page` gains composition-variety, a self-critique gate, and TASTE application.** Marketing pages must vary layout grammar per section (no two adjacent sections share a shape — the anti-"bootstrap-era" rule); dashboards still repeat one grammar. A new self-critique gate (step 12.5) renders + screenshots the page and critiques it against the moodboard/brief before the user sees it (Gate 2, between token-clean and the owner's rating). Step 3 reads TASTE.md and applies high-confidence entries to the first draft.
- **`save-session` now writes `TASTE.md`.** New Step 6.5 folds the session's design taste signals (ratings, rejects, edits) into the ledger — appending new entries, reinforcing recurring ones, revising contradicted ones — and routes durable cross-project preferences to the global ledger. save-session is the sole writer of confidence values.
- **`design-check` now reads `TASTE.md` and enforces it.** Step 1 loads high-confidence taste entries (≥ `apply_threshold`); Step 8 flags any change that violates one (removing a "sacred" element, reintroducing a rejected pattern) as human-judgment — never a silent override.
- **`init-project` now sets the archetype, scaffolds TASTE.md, and scopes the shadcn rule.** Phase 4 asks the one archetype classification (dashboard / marketing / content / commerce / app) that fills DESIGN.md's `archetype:` and selects the design rulebook; it also scaffolds `brain/TASTE.md` from the new template. Root CLAUDE.md rule 9 is now **archetype-scoped**: shadcn-first for dashboard/app, bespoke expressive components for marketing/content (libraries as references, not installed aesthetics). `calibrate` added to the generated skill index; TASTE.md added to the README file catalog.
- **`design-direction` now invokes `calibrate` and commits a point-of-view.** Phase 4 hands off to `Skill("calibrate")` exactly once (captures the moodboard, writes the FOLLOW/DEVIATE/REFUSE conventions audit); Phase 5 reads those outputs and must not re-invoke it. Phase 7 now writes a committed POV paragraph ("could not be mistaken for anyone else's" + one named aesthetic risk) and a dated anti-cliché list of current second-order AI tells. Phase 2 reads the `archetype:` from DESIGN.md; Phase 3 writes the register diagnostic to BRAND.md where `calibrate` reads it. `Skill` added to allowed-tools.
- **Orchestration now routes UI work through the design skills (the broken wire, fixed).** `worker` and `solo` must route any page/component work through explicit `Skill("build-page")` / `Skill("build-component")` calls (the UI analog of `test-driven-development`), so `design-check` fires; `ceo` gains a selective-deep-check trigger that refuses to merge UI work that bypassed the design skills — the same way it rejects a missing test. Previously a "UI pass" had no design routing at all.

### Added
- **FUNDAMENTALS.md — `## Image Pipeline`, `## Build Order`, `## Definition of Done` sections.** The image source ladder (client real → shoot shot-list → framed stand-ins → never-list) + treatment + format performance; the build-order doctrine (tokens → shell → home → internal → polish, with the "nav breaks everywhere" and "≤2 new shapes per internal page" rules); and three explicit done-checklists (component / page / site). Universal craft.
- **FUNDAMENTALS.md — `## Motion Spec` section.** Extends the existing Motion Principles with the productive-vs-expressive archetype split (70–240ms vs up to 700ms, with IBM Carbon / Kowalski easing curves), the easing decision order, the frequency law (100×/day and keyboard actions get no animation), never-`scale(0)`, stagger bands, replay-on-rescroll, and reduced-motion. Universal craft, applies to every project.
- **DESIGN.md template — `archetype:` field + `## Archetype` section.** The single classification (dashboard / marketing / content / commerce / app) that selects the design rulebook: component source, composition grammar, motion class, era-sensitivity. Replaces the implicit dashboard-first assumption with an explicit per-project decision.
- **DESIGN.md template — `motion:` block + `## Motion` section.** Motion register per brand (still → cinematic), duration bands, easing order, frequency law, replay-on-rescroll, reduced-motion. Motion was previously undefined outside a single tempo axis.
- **DESIGN.md template — `icon:` field + `## Icons` section.** One family chosen at lock time, matched to the letterforms; the icon law (Lucide default, no emoji, label rules) promoted from STRUCTURE conventions into the brand layer.
- **`TASTE.md` template (new).** A confidence-scored learned-preferences ledger — per-project (client identity) and global (the owner's accumulating eye), fed by `save-session` from ratings / accept / reject / edit signals, read by `build-page` and `design-check` so high-confidence preferences apply before the user re-asks. Scaffolded by `init-project`; wiring lands in a later v4.0.0 commit.
- **`calibrate` skill (27th skill).** The calibration bridge between `design-direction` Phase 4 (reference list) and Phase 5 (three directions): builds a mission file from brand + register + archetype, walks a tiered inspiration source map, captures an annotated moodboard via the Aside browser (tested runbook), and writes a FOLLOW / DEVIATE / REFUSE conventions audit to `DESIGN.md`. Hands back to `design-direction` via an explicit `Skill()` call. `design-direction` invocation of `calibrate` is wired in a later v4.0.0 commit.

## [2.5.0] — 2026-05-26

Major release. Three-layer architectural redesign. The biggest single release since the three-folder protocol shipped.

### What changed in the architecture

Until v2.4.0, the plugin described what should happen and hoped the agent picked it up. That worked in casual sessions and broke quietly the rest of the time: agents hardcoded design values, picked native `<select>` over shadcn `<Select>` inconsistently, projects on older plugin versions silently skipped new rules, skill-to-skill chains relied on description-match keyword luck. A 32-finding edge-case audit (`AUDIT-2026-05-26.md`) traced every variant back to the same root cause: skills are reactive — the agent has to *choose* to invoke them — and the plugin had no deterministic enforcement layer to back them up.

v2.5.0 separates the plugin into three explicit layers, each with a different guarantee:

- **Rules** — root `CLAUDE.md` is now the always-loaded brain. Full skill index (one row per skill with when-to-use + how-to-invoke), full hooks index (what fires when), situation router (common requests → which skill), all non-negotiable rules. The agent never has to guess what's available; the catalog is always in front of it.
- **Enforcement** — hooks. Three new ones: PostToolUse design-scan (greps every write to UI files for raw hex/px/font/native-when-shadcn/cardinal sins), PostToolUse design-check dispatcher (fires after writes to component-tier files), SessionStart drift-detector (reads `agents/.plugin-version`, prompts `/migrate-project` when behind). Hooks don't rely on the agent choosing to read anything.
- **Workflow** — skills, but every skill-to-skill chain now uses explicit `Skill(name)` calls in the parent's body. Zero description-match auto-chains. The chain runs no matter how the user phrased the request.

### New things added

- **`migrate-project` skill (16th skill).** Walks the manifest chain between the project's recorded plugin version and the installed plugin version, proposes each delta, confirms per change, never silent-overwrites a customized file. Refuses to run in Cowork (Cowork can't `git push`); exits with instructions to open the project in Claude Code or terminal.
- **`migrations/vX.Y.Z.md` manifests.** One per release from v2.5.0 onward. Each lists files added, files modified (with previous-template snapshot reference for diff-against-current detection), rules added, files renamed/removed. Backfill `migrations/v2.4.0.md` documents the rule #8 delta so projects on v2.3.0 can catch up cleanly.
- **`agents/.session-type` marker.** Written by `init-project` at bootstrap (`cowork` / `claude-code` / `codex`). All hooks now read it to pick the correct WORKLOG path; env-var heuristic is the fallback only.
- **`agents/.plugin-version` + `agents/.plugin-version-skip`.** Per-project drift state. Skip is per-version (re-prompts on next plugin update) — no permanent-skip option, by design.
- **`agents/SITUATIONS.md`.** The situation router was pre-emptively split out of CLAUDE.md to keep the brain under 280 lines.
- **Two new non-negotiable rules in root CLAUDE.md.** Rule #9 — hybrid shadcn-first component selection (default to shadcn primitive; named-list of native exceptions; stop and ask when no primitive exists). Rule #10 — use the skill index, don't improvise a workflow when a skill exists for it.
- **`## Extended Context` stub** in root CLAUDE.md template — `add-context` appends here cleanly; 280-line ceiling check added.

### Behavioral changes — skill chain determinism

- `build-component` Phase 5 explicitly calls `Skill("design-check")` after each write. Belt-and-suspenders with the new PostToolUse dispatcher hook.
- `build-page` explicitly calls `Skill("build-component")` for new primitives and `Skill("design-check")` after each section write. Canon-modification hard rule rewritten to name protected files (DESIGN/STRUCTURE/BRAND/FUNDAMENTALS/marketing) and explicitly permit BRIEF/INDEX updates. `layouts/<slug>.md` softened from hard prerequisite to warn-and-continue.
- `save-session` Step 10 fully rewritten with three deterministic branches keyed on `agents/.session-type`: `main` direct → simple add+commit+push; worktree branch → existing merge flow; Cowork → copy-paste fenced shell snippet (no git execution). Step 9.5 adds explicit `Skill("audit-before-close")` call.
- `build-component` and `build-page` both add explicit `Skill("discipline")` calls when the change is structural (BRIEF, ROADMAP, or cross-tier).
- `edit-plugin` gets Step 5 (Manifest discipline): version bumps must ship a `migrations/vX.Y.Z.md` in the same commit or the commit halts. L11 hot-copy activation path is now platform-conditional (env-var first, falls back to macOS / Linux paths).

### Behavioral changes — multi-stack robustness

- `init-project` detects monorepos (`workspaces` / `pnpm-workspace.yaml` / `turbo.json` / `nx.json`), writes per-app `agents/TOOLING.md`, records `**Monorepo:**` + `**App paths:**` in `STRUCTURE.md`.
- `init-project` Phase 4 asks for package manager at first init (default to detected lockfile, one-key confirm); re-init reads existing `agents/TOOLING.md` and asks continue-or-switch.
- `templates/TOOLING.md` personal `~/Arel OS/Projects/` path stripped entirely. Template now renders from chosen package manager.
- `build-component` Phase 1 adds `src-tauri/tauri.conf.json` as a desktop surface signal regardless of frontend location. Tauri-at-root projects are no longer misclassified.
- `design-check` Step 2 reads `agents/STRUCTURE.md` for tier paths instead of hardcoded globs. Step 6 diff scan scoped to `STRUCTURE.md` paths with exclude list (`node_modules`, `.git`, `dist`, `build`, `.next`, `.turbo`, `coverage`). Monorepo-aware: scans each app separately.
- `audit` design-system scan does the same. New Step 4 garbage-collects `agents/preview/` HTMLs (keep 2 most recent per direction-slug, surfaces deletion list to user).
- `build-component` Phase 5 treats `[VERIFY]` markers in `STRUCTURE.md` as "not detected" instead of authoritative.
- `build-component` 2-round edit cap qualified as standalone-only; lifted when inline-called from `build-page`.

### Cleanup sweep

- `marketing-brief` `allowed-tools` no longer lists unused WebSearch; Codex sidecar now names `build-page` as primary consumer.
- `init-project` Codex sidecar expanded from 7 words to ~50 words naming all five modes.
- `design-direction` `allowed-tools` now includes WebSearch (Phase 4 moodboard actually uses it).
- `add-context` Step 3 adds Cowork vs Claude Code / Codex qualifier for the type-DONE pattern. Step 5 counts CLAUDE.md lines before appending; warns at 280-line ceiling.
- `session-recap` `allowed-tools` scoped from `Bash(git:*)` wildcard to read-only `Bash(ls / pwd / date / git status / git worktree / git log)`. Dead `sessions/` directory read removed.
- `templates/CONTENT.md` link-shortener example rows wrapped in `<!-- EXAMPLE — DELETE BEFORE USE -->` markers.
- `phase-4-design-system.md` dead `npx @google/design.md lint` step removed.
- `init-project` SKILL.md `STRUCTURE.md` creation-path note expanded to list all three paths.
- `agents/preview/` added to `init-project` output layout and root README template.

### Migration

Existing projects: run `/migrate-project` to backfill the new files (`.session-type`, `.plugin-version`, etc.) and apply the deltas from `migrations/v2.4.0.md` and `migrations/v2.5.0.md`. The SessionStart drift-detector hook will prompt automatically on first session after upgrading.

Cowork projects: the drift-detector still detects and warns, but `migrate-project` itself refuses to run in Cowork. Open the project in Claude Code (or your terminal) and run `/migrate-project` there — Cowork can't `git push` the version bump, and silently no-op'ing the migration would leave the project in an unknown state.

### Known runtime notes

- The PostToolUse design-scan hook depends on the runtime exposing a tool-input file-path env var. If your host runtime uses a different env var name, the hook silently no-ops (safe). Verify in the Claude Code / Codex hook spec for your version.
- The SessionStart drift-detector uses `python3 packaging.version` to compare semvers (Python 3.8+, standard on macOS / Linux). If `packaging` is unavailable, the warning still fires but without the specific manifest list. A pure-bash version comparison could replace this if needed.

### Stats

5 implementation commits (Phases A–E) under one redesign plan (`REDESIGN-PLAN-2026-05-26.md`). 32 audit findings closed (6 HIGH / 14 MEDIUM / 12 LOW). 28 files modified, 4 files created.

## [2.4.0] — 2026-05-24

Patch release. Closes a long-standing gap in the design-system gate: agents kept hardcoding hex / px / font values in UI files because the always-loaded root `CLAUDE.md` template said nothing about tokens or `design-check`. The rules existed only in `DESIGN.md`, `FUNDAMENTALS.md`, and the `design-check` skill — files the agent only opens if it independently decides to. Even an obedient agent reading root `CLAUDE.md` cover-to-cover got zero signal that hardcoding was forbidden.

### Changed

- **Root `CLAUDE.md` template (`skills/init-project/references/phase-3-three-folder-create.md`)** — added Non-negotiable rule #8: "UI work uses the design system. No hardcoded values, ever." Names the file extensions (`.tsx` / `.jsx` / `.vue` / `.svelte` / `.swift` / styles), points to `DESIGN.md` and `FUNDAMENTALS.md` as required reading, requires `design-check` before and after the edit, lists the forbidden patterns (raw hex, raw px, raw `font-family`, emoji-as-icon, cardinal sins), and tells the agent to halt and propose token additions instead of improvising.
- Every project initialized by `init-project` from this version on will get the rule in its root `CLAUDE.md`. Existing projects need a manual backfill — copy rule 8 into their root `CLAUDE.md` under "Non-negotiable rules".

### Why

`design-check` is a skill — reactive, agent must choose to invoke. The trigger keywords ("edit UI", "change styles", "add page") miss the way users actually phrase UI work ("fix this bug", "tweak the hero"). The hooks layer has no PostToolUse scan for raw values. So the gate is self-policed by the agent's discipline, and the bulk of day-to-day work — `Edit` on existing components — bypasses `design-check` entirely. Putting the rule in the always-loaded file is the cheapest leverage: from now on the agent knows the rule before it reads any other canon. Hooks-level enforcement (a PostToolUse diff scan) remains the next-leverage move and is tracked separately.

## [2.3.0] — 2026-05-23

Minor release. `build-page` redesign — the v2.2.0 shape was a 6-phase pipeline pretending to be a conversation, racing toward approval gates instead of staying open across a long iterative session. v2.3.0 throws that out and rebuilds the skill as a normal-shaped plugin skill that happens to have a longer-than-usual session, following the same protocols every other skill uses (WORKLOG entries on decisions, BRIEF appends on locks, INDEX update on new routes, no state files, no scratch folders, no special mode machinery). Reference files cut from 8 → 2.

### Why the redesign

The v2.2.0 model was wrong in three structural ways:

1. **It was a pipeline pretending to be a conversation.** Six phases, each ending in an approval gate the skill raced toward. That's the opposite of how a homepage actually gets built — you sit in it, iterate, throw references at the agent, change your mind. v2.2.0 made that feel like fighting the gates.

2. **It invented mid-session state machinery that no other skill in the plugin needs.** Proposed scratch folders, state files, tool-palette restrictions, defer-lists for other skills. None of that exists for `design-direction`, `marketing-brief`, or any other long-running skill — they rely on the conversation transcript + canon files + WORKLOG. The same pattern works fine for page builds.

3. **It didn't talk to the rest of the plugin.** Zero references to WORKLOG, BRIEF, STATUS, CHANGELOG, INDEX, or the cleared-state PreToolUse hook. Would have false-positive-warned on every first Edit, missed every CHANGELOG entry, and left INDEX.md unmaintained. The skill was invisible to its own ecosystem.

### Changed

- **`build-page` SKILL.md fully rewritten** (~350 lines) — flat protocol shape, no phase numbering, no formal gates. Single "what fires this" section, single "what it produces" section, single "protocol" section that walks the agent through the long conversation, single "hard rules" section. Reads like every other skill in the plugin.
  - On invocation: asks "which page?" if not in the user's message, reads the full canon for the tier, appends a session-open line to WORKLOG (which disarms the cleared-state PreToolUse hook for the rest of the session), surfaces a starting analysis, proposes a starting plan as a numbered section list, then iterates freely with the user — no 5-iteration cap, no formal gates.
  - When the user locks the plan, appends a BRIEF block per the cardinal "lock-before-cascade" rule from `agents/CLAUDE.md`, then works through sections sequentially.
  - For each section: surfaces content, proposes strategies (reuse / adapt / compose / build new / adopt external), accepts external references when the user drops them, calls `build-component` inline for net-new primitives, appends a WORKLOG line on close.
  - When all sections have real component paths, writes the actual page file (RSC + `generateMetadata` for marketing, client component for dashboard), inlines copy directly from `copy/<slug>.md` with a top-of-file canon-pointer comment, updates `agents/docs/INDEX.md` inline, and lets `design-check` chain automatically.
  - Closing: prints the end-of-skill summary. The session ends when the user closes the chat or types "save". No special handoff — STATUS.md Next Actions + WORKLOG carry the breadcrumbs.

- **Reference files cut 8 → 2.** Old `phase-1-read-brief.md` through `phase-6-wire-up.md` plus `sub-mode-marketing-page.md` and `sub-mode-dashboard-page.md` are deleted. The phase-based content was wrong shape; what remains is folded into the SKILL.md body or into the two new references:
  - `references/conversational-shape.md` — how the long session stays productive without inventing new machinery. Documents WORKLOG cadence (one line per decision, canonical prefix vocabulary), BRIEF append rules, INDEX update rules, save-session interaction (suspended-state breadcrumbs in STATUS Next Actions), and explicitly what does NOT happen (no scratch folder, no state file, no iteration history files, no tool palette restriction, no multi-page tracking, no defer-list).
  - `references/per-section-workflow.md` — the conversation shape for one section: enter, surface content, propose strategies, accept external references with full cross-check protocol against DESIGN.md + BRAND.md + section content (verdict: adopt / adapt / reject), hand off to `build-component` for net-new, close section, move on.

- **External reference adoption is now a documented sub-section of per-section-workflow**, not a separate sub-mode. The pattern: fetch (WebFetch first, escalate to Chrome MCP if the page is client-rendered), identify the visual pattern, cross-check tokens against DESIGN.md, cross-check voice against BRAND.md archetype + tempo + refusal list, cross-check content fit, give a one-word verdict (adopt / adapt / reject) with reasoning, then hand off to `build-component`'s existing `adopt-external` sub-mode if accepted.

- **`build-component` and `marketing-brief` cross-references unchanged from v2.2.0** — both already reference `build-page` correctly in their "Difference from related skills" sections. The conductor/player relationship and the marketing-brief → build-page handoff in marketing-brief's "Next step" output both still read correctly under the v2.3.0 shape.

- **Codex sidecar (`skills/build-page/agents/openai.yaml`)** — short description updated to reflect the long-iterative-conversation model instead of the 6-phase pipeline.

- **README** — build-page paragraph rewritten. Skill count stays at 15.

- **Plugin manifests** — version bumped 2.2.0 → 2.3.0 in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Minor bump: same skill, redesigned shape, no new files in the plugin's own surface (the skill's internal file count went 11 → 5 due to reference consolidation).

### Compatibility

- **Drop-in upgrade from v2.2.0.** No file shape changes in user projects. No canon file changes. Existing components untouched. Existing `marketing-content.ts` / `lib/content.ts` mirror files in user projects continue to be left alone (hard rule preserved from v2.2.0); build-page Phase 6 wire-up still inlines copy directly and notes the orphaned mirror in the output.

- **WORKLOG / BRIEF / INDEX / STATUS interaction is now correct.** v2.2.0 was silently violating the WORKLOG discipline declared in `hooks/session-start-context.md`. v2.3.0 follows it. Projects upgrading from v2.2.0 will see better save-session behavior immediately (proper CHANGELOG categorization, proper BRIEF version blocks, proper STATUS Next Actions when a build-page session is suspended).

- **`build-component` continues to work standalone** for atomic component requests. The user invokes it directly for one-off components; `build-page` calls it inline during per-section work. Both paths are first-class.

- **Hooks unchanged.** The cleared-state PreToolUse warning, the SubagentStart/Stop appenders, the PreCompact / PostCompact context injectors, the Stop hook's save-session reminder — all unchanged. `build-page` now plays nicely with all of them.

- **No interaction protocol with `discussion-mode`, `discipline`, `audit-before-close`, or `verify-by-reading`.** v2.2.0 (and the failed v2.3.0 draft) proposed an explicit defer-list. v2.3.0 drops that — other skills' triggers work normally. If the user invokes `/audit` mid-build, audit runs and returns; build-page picks up from the conversation. The agent stays oriented across that the same way it would for any other skill.

## [2.2.0] — 2026-05-23

Minor release. New `build-page` skill — the compositional sibling to `build-component`. Closes the gap revealed by the v2.1.x Snapfinder runs where `build-component` was being used for whole-page work and producing 400-line code drops with no layout conversation, no hierarchy debate, no asset planning, and no reuse audit — just a code dump and an approve/edit/restart button. `build-page` separates the architectural conversation from the code generation so the user makes one decision per phase, in chat, before seeing any code.

### Added

- **`build-page` skill** — 15th skill in the plugin. Compositional page builder for marketing pages (homepage, pricing, features, customers, comparisons, about, legal) and dashboard pages (overview, settings, team, analytics, billing). Triggers — "build the homepage", "build the pricing page", "compose page X", "wire up the X page", "build the dashboard overview page", "/build-page". Sits between `marketing-brief` (planning) and `build-component` (atomic execution) in the skill chain: `init-project` → `design-direction` → `build-component` (per atomic piece) → `marketing-brief` (once, end of project) → **`build-page`** (per page) → `design-check` (auto, post-write) → `audit` (periodic).

- **6-phase layout-first, code-last flow.** No file writes before Phase 6. Each phase ends with an explicit approval gate in chat:
  - Phase 1 — Read the brief (full canon read for the page's tier; halts on missing canon).
  - Phase 2 — Layout architecture (numbered section list with rhythm tags `calm` / `loud` for marketing, density tags `scan` / `focus` / `meta` for dashboard).
  - Phase 3 — Hierarchy (per-section primary / secondary / tertiary).
  - Phase 4 — Asset manifest (per-section visual treatment + micro-interactions, cross-referenced against `MEDIA.md`; dashboard pages additionally declare loading / empty / error / partial states for every data-bound section).
  - Phase 5 — Component selection (per-section reuse / adapt / build-new strategy table; build-new entries execute sequentially via inline `build-component` calls — one focused conversation per net-new component, not bundled).
  - Phase 6 — Wire-up (compose all components into the final page file; copy inlined directly from `agents/marketing/copy/<slug>.md` or dashboard brief; mandatory canon-pointer comment at file top).

- **Two sub-modes — marketing-page and dashboard-page.** Detected from `STRUCTURE.md` declared surfaces + user wording + slug location. Same 6 phases, different inputs and emphases:
  - Marketing sub-mode enforces React Server Component default (no top-level `"use client"`), mandatory `generateMetadata` export for SEO, full `agents/marketing/*` canon read, and the persuasion-arc section ordering (claim → trust → how → surface → moment → social-proof → answer → ask).
  - Dashboard sub-mode requires a page brief (halts and asks user to type one if missing), client-component-friendly Phase 6, tool-shaped section ordering (header → KPIs → primary work area → secondary → meta), and strict reuse bias (most dashboard pages should be 90%+ composition of existing primitives).

- **Hard rule: no intermediate content-mirror file.** `build-page` will NEVER create `lib/marketing-content.ts`, `data/copy.ts`, `lib/content.ts`, or any equivalent runtime mirror of `CONTENT.md`. The canonical markdown is the source; copy is inlined directly in the page JSX; the agent is the propagation mechanism when canon changes. Existing mirror files in projects are left alone — Phase 6 inlines copy without touching them and notes them as orphaned in the output for follow-up cleanup. Closes the third-source-of-truth drift bug that ad-hoc `build-component` page builds were introducing.

- **Reference files (8)** — `references/phase-1-read-brief.md`, `references/phase-2-layout-architecture.md`, `references/phase-3-hierarchy.md`, `references/phase-4-asset-manifest.md`, `references/phase-5-component-selection.md`, `references/phase-6-wire-up.md`, `references/sub-mode-marketing-page.md`, `references/sub-mode-dashboard-page.md`. Progressive disclosure — each opened only when entering its phase to keep orchestration context lean.

- **Codex sidecar** — `skills/build-page/agents/openai.yaml` with display name, short description, brand color `#475569` matching the build-component/design-check tier, implicit invocation enabled.

### Changed

- **`build-component` skill "Difference from related skills" section** updated to reference `build-page` — atomic component requests still go directly to `build-component`, but page-scale composition routes through `build-page` which calls `build-component` inline per net-new component. Clarifies the conductor / player relationship.

- **`marketing-brief` skill "Difference from related skills" section** updated to reference `build-page` — `marketing-brief` plans the marketing-site canon once; `build-page` is now the per-page execution skill that reads those plans. The "Next step" output also points to `build-page` (not `build-component`) for marketing-page work.

- **README** — skill count bumped 14 → 15, build-page added to the "Discipline skills" list with a one-paragraph explanation of the layout-first / code-last model and the no-mirror-file rule.

- **Plugin manifests** — version bumped 2.1.1 → 2.2.0 in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Minor bump: new skill is additive; existing skills, hooks, and canon files are untouched.

### Compatibility

- **Drop-in upgrade from v2.1.x.** No file shape changes — `CLAUDE.md`, `BRAND.md`, `DESIGN.md`, `FUNDAMENTALS.md`, `STRUCTURE.md`, all `agents/marketing/*` files retain their existing shape. Existing components are untouched.

- **Existing `marketing-content.ts` / `lib/content.ts` mirror files in projects are left alone.** `build-page` Phase 6 inlines copy directly and notes the orphaned mirror in its output. Migration to "no mirror" is opt-in per page; nothing forces a rewrite.

- **`build-component` continues to work standalone** for atomic component requests. The user invokes `build-component` directly for one-off components; `build-page` calls it inline during Phase 5. Both paths are first-class.

- **Hooks unchanged.** `design-check` continues to fire automatically after `build-page` Phase 6's write (via the existing post-write hook chain).

## [2.1.1] — 2026-05-22

Patch release. Two refinements to `design-direction` after first real-world v2.1.0 run on Snapfinder surfaced (a) the moodboard outweighing the brand's own distinctive asset, and (b) the preview HTML rendering decontextualized components instead of the actual product surface. Both fixes are additive and backwards-compatible — no schema changes, no breaking changes.

### Added

- **Mandated outside-envelope direction in Phase 5.** At least one of the three proposed directions must now sit OUTSIDE the moodboard envelope — different material, different temperature, different category code than anything in the moodboard. Forces the agent to invent distinctive territory rather than remix reference sites. Up to two of the three may stay inside the envelope (safe picks); the user always sees at least one distinctive bet so the pick is conscious, not defaulted. New "Anti-moodboard-convergence" sub-section in `phase-5-three-directions.md` defines pairwise material distance + category-code distance + mandated-outside rules. Includes a Snapfinder-style worked example showing Editorial Cream / Premium Tech (inside) + Bazaar Modern (outside, traditional Indian textile palettes) so the agent has a concrete reference for what "outside the envelope" looks like.

- **Borrow / depart / distinctive-asset structure per direction.** Every direction block in Phase 5 now carries three required lines: `Borrows from moodboard:` (what it inherits — anchor in trust), `Departs from moodboard:` (what it deliberately doesn't do — distance from category default), `Distinctive asset:` (one sentence — the ownable visual thing nobody else in the category has). The third line is the load-bearing one — it forces articulation of what makes the direction *ownable*, not just *visible*. The mandated outside-envelope direction reads `Borrows from moodboard: nothing literal — trust ceiling only.`

- **Section 0 — surface layout (tier-aware) in preview HTML.** New section added at the TOP of every preview page, before the 21 component sections. Renders the project's actual product surface using the proposed tokens — not isolated components. Tier-aware:
  - `dashboard` tier → renders a full dashboard mockup: sidebar (logo + 5 nav items + new-button + user card), topbar (breadcrumb + search + bell + avatar), main content with page header, 4 KPI tiles with sparklines and trend deltas, a revenue-trend chart card with filter pills and dual-line SVG, a 5-row activity table with status badges.
  - `marketing` tier → renders a full marketing landing mockup: nav with brand + product/pricing/customers/docs links + sign-in + CTA, expanded hero (consumes the prior standalone Section 20), customer-logo trust bar, 6-tile features grid with icon swatches, 3-card testimonial row with avatar attributions, 3-tier pricing grid with featured-card styling, 4-column footer with brand mark and copyright.
  - `both` tier → renders both layouts stacked top-to-bottom with a visible "MARKETING PREVIEW" divider between them.

  Standalone Section 20 ("Real-content example — hero") is now SKIPPED when tier is `marketing` or `both` (hero lives inside the marketing mockup) and when tier is `dashboard` (no marketing surface). It only renders as a legacy fallback when tier is unknown. All Section 0 rendering uses the same tokens as the component catalogue below — change a hex in Phase 6.5, both the layout view and the component swatches update together.

- **Section 0 substitution placeholders.** `{{project_initial}}` (uppercase first letter for logo box), `{{project_slug}}` (lowercased no-spaces for email placeholders), `{{feature_1_title}}…{{feature_6_title}}` (six brand-fitting feature titles per archetype), `{{feature_1_body}}…{{feature_6_body}}` (one-sentence bodies, ~80–120 chars each), `{{testimonial_1_quote}}…{{testimonial_3_quote}}` (realistic testimonial quotes, ~80–140 chars, specific verbs and named outcomes — not "changed my life" generic). Phase 6.5 generates these from `agents/BRAND.md` Product + Audience + archetype, with archetype-fitting fallbacks.

### Changed

- **`phase-4-moodboard.md` reframed.** Moodboard's job is now explicit: "trust-ceiling check, not a template." Added an IS / IS NOT pair clarifying that the moodboard is *permission to be ambitious* (audience already accepts this much), NOT *a menu of styles to remix*. New hard rule: "Do not propose Phase 5 directions that read as a percentage mix of moodboard sites — if a direction can be summarized as 'mostly site X + a bit of site Y', it has failed." Updated the user-facing sample prompt at moodboard-presentation time so the framing carries through to the user, not just the agent. Cross-references the new Phase 5 mandated-departure rule.

- **`phase-5-three-directions.md` — anti-moodboard-convergence sub-section.** Parallel to the existing inter-direction anti-convergence rules (which force the 3 directions to differ from each other), this adds rules that force collective distance FROM the moodboard. Pairwise: no direction may match ALL of (material + temperature + saturation tier) with any single moodboard site. Category-code: if the moodboard is dominated by one category code (e.g., 4 of 5 are premium fintech minimalism), at least one direction must break that code. Mandated: exactly one direction has `Borrows from moodboard: nothing literal.`

- **`phase-6-5-preview-html.md` — Section 0 spec + HTML/CSS templates.** Comprehensive spec for the dashboard and marketing layout blocks, including the full HTML markup with `{{placeholder}}` substitutions, the matching inline CSS (organized under "/* Section 0 — Dashboard layout */" and "/* Section 0 — Marketing layout */" comments), and a "Tier-based conditional rendering" rules block in the substitution section.

- **`phase-6-5-token-alignment.md` — "Generate the HTML preview" step updated.** Now explicitly mentions both (a) the project's actual surface layout (Section 0) AND (b) the component catalogue. Branches rendering on the surface tier detected in step 1. The "layout view is the load-bearing section" framing carries through so the agent doesn't treat Section 0 as optional polish.

- **Plugin manifests** — version bumped 2.1.0 → 2.1.1 in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Patch bump: refinements to v2.1.0 behaviour, no schema changes, no new files.

### Compatibility

- **Drop-in upgrade from v2.1.0.** No file shape changes — `agents/BRAND.md`, `agents/DESIGN.md`, `agents/preview/*.html` all retain their v2.1.0 shape. Projects on v2.1.0 pick up the new direction-block structure (borrow/depart/distinctive-asset lines) on the next `design-direction` run and the new Section 0 layout view on the next Phase 6.5 preview render — both additive, never destructive.

- **No effect on already-locked directions.** Projects that already ran `design-direction` and have a locked direction in `agents/BRAND.md` are untouched until the next re-anchor run. The mandated-outside rule applies to NEW direction proposals only.

- **CSS-side architecture unchanged.** Material naming (paper/ash/ink/hairline), OKLCH derivations, `light-dark()` function, `npx @google/design.md lint` sync layer — all unchanged. Section 0 uses the same CSS variables as the component catalogue, so any token edit propagates to both views automatically.

## [2.1.0] — 2026-05-22

Minor release. `design-direction` now generates concrete tokens (colours, typography, spacing) and ships a self-contained HTML preview the user opens in their browser to visually approve before any write. Closes the v2.0.x gap where the skill produced rich brand prose but never updated the actual design tokens — projects ran `design-direction`, got beautiful BRAND.md updates, and looked identical afterwards because `DESIGN.md`'s token frontmatter stayed at defaults.

### Added

- **`design-direction` Phase 6.5 — token alignment + visual preview.** New phase inserted between Phase 6 (pick direction) and Phase 7 (write outputs). Reads existing `agents/DESIGN.md` token frontmatter, classifies MATCH / partial-MISMATCH / full-MISMATCH per category, generates concrete hex / font / spacing / radius values for mismatched categories using the locked direction's material reference + temperature + saturation, runs WCAG AA contrast validation on 8 load-bearing pairs (refuses to write a palette that fails), renders a self-contained HTML preview page, surfaces a `file://` link the user opens in their browser, then asks for approve / iterate / reject. Iteration loop translates plain-language corrections ("too orange", "display feels heavy", "dark mode is muddy") into token-level changes and re-previews. Soft 5-iteration limit triggers a step-back-to-Phase-6 meta-prompt. Files: `skills/design-direction/references/phase-6-5-token-alignment.md` (token logic), `skills/design-direction/references/phase-6-5-preview-html.md` (preview HTML spec + template + font-loading rules + iteration semantics).

- **HTML preview page** — written to `agents/preview/<direction-slug>-<date>.html` on every Phase 6.5 run with token changes. Single self-contained file, no build step, ~400 lines including inline CSS. Loads Google Fonts via `<link>` when fonts are available; falls back to nearest Google cousin for Pangram / commercial fonts and notes the substitution in the footer. Renders 21 sections: top bar with light/dark toggle, surface swatches (paper/ash/ink/hairline), accent swatches, status swatches, WCAG contrast pairs panel with PASS/FAIL badges, display ramp (72/56/40/28 px), body ramp (18/16/14 px), mono code sample, letter-spacing test, spacing scale visualization (bars at 4/8/12/16/24/32/48/64), radius squares, all 12 components from DESIGN.md's component list (buttons / form / card / dialog / table / tabs / badges / toast) styled with the proposed tokens, and a real-content hero section that surfaces typography pairing fights. Display headlines and body paragraphs are brand-fitting prose drawn from the locked archetype, not lorem ipsum.

- **Archetype → palette + typography heuristic tables in Phase 6.5.** Two 12-row tables in `phase-6-5-token-alignment.md`: (1) archetype → paper temperature, ink temperature, accent character, OKLCH chroma ceiling (Sage 0.12, Magician 0.18, Caregiver 0.10, Rebel 0.25, Creator 0.20, Hero 0.18, Explorer 0.14, Innocent 0.10, Lover 0.12, Jester 0.22, Ruler 0.16, Everyman 0.14); (2) archetype → display / body / mono font picks, biased toward Google Fonts (Source Serif 4, Fraunces, Inter, Geist, JetBrains Mono, Recursive) with commercial fonts (Tiempos, Lyon, Recoleta) flagged with cost notes for the user to opt into.

- **Surface tier detection (new Phase 6.5 step 1).** Classifies project as `dashboard` / `marketing` / `both` from `agents/BRAND.md` Product.Surfaces field. Drives type scale ratio (dashboard 1.125, marketing 1.25, editorial 1.333), display-font banning strictness (strict on marketing, relaxed on dashboard-only), and whether to generate a categorical chart palette.

- **Cultural anchor + script detection (new Phase 6.5 step 2).** Detects Indic / Arabic / Hebrew brand context from `agents/BRAND.md` Cultural anchor field. Pairs Latin body font with the matching script font (Devanagari / Gujarati / Gurmukhi → Mukta or Hind; Tamil → Noto Sans Tamil; Bengali → Noto Sans Bengali; Arabic → Noto Sans Arabic). Skill refuses to ship a Latin-only stack for an Indic-market brand.

- **WCAG contrast validation gate.** New Phase 6.5 substep computes WCAG ratios for 8 load-bearing pairs (ink/paper in both modes, ink/ash in both modes, paper-on-accent for CTAs, accent-on-paper for links, hairline visibility, status.error/paper) using the standard relative-luminance formula. Hard rule: refuse to write a palette that fails AA. Auto-suggests a fix (darken ink, shift accent hue, increase chroma) and re-validates before re-previewing.

- **Dark-mode generation rules.** Explicit rules added to Phase 6.5 step 6: don't invert; desaturate accent chroma by 20–35% for dark mode; shift accent lightness up 5–10% so it doesn't recede; hairline becomes lighter than paper on dark canvas (highlights, not depressions); never `#000`, always 4–8% temperature tint.

- **Categorical chart palette generator.** When surface tier includes dashboard AND the project has data viz needs, Phase 6.5 emits an 8-stop categorical palette in OKLCH at constant L=60% (light) / L=70% (dark) and C=0.15. Hues spaced at 30 / 60 / 120 / 180 / 210 / 270 / 300 / 340 for perceptual evenness. Skipped entirely when no dashboard surface.

- **`design-direction` Phase 5 — anti-convergence rules (v2.1).** Earlier session work, shipped in this release. Each of the three proposed directions now carries concrete hex codes per material role, dark/light pairing, type pairing with named families, and is forced to be meaningfully different from the other two via material-first thinking (parchment vs leather vs stone vs velvet) and category-diversity rules. Eliminates the v1 drift toward "three flavours of Inter + neutral grey + soft shadow."

- **Phase 2 — three research-backed axes added.** Earlier session work. v1's 9 axes → v2.1's 10 axes: dropped `surface_mix` and `tempo` (derived from other axes), added `trust_stakes` (Cardamone 2025), `category_maturity` (Neumeier Zag), `distinctive_asset` (Byron Sharp). Phase 3 diagnostic prose updated to surface all three new axes for user confirmation.

- **`type_scale:` block in DESIGN.md template.** New optional frontmatter block: base size + modular ratio + named step list (xs / sm / md / lg / xl / 2xl–5xl / display) + hero_max cap. Phase 6.5 picks ratio per surface (dashboard 1.125, marketing 1.25, editorial 1.333).

- **`chart_palette:` block in DESIGN.md template.** New optional frontmatter block: 8 OKLCH-stepped hues per mode for categorical data viz. Present only when generated.

- **Per-surface override blocks in DESIGN.md template.** Optional `dashboard:` and `marketing:` blocks for projects that need meaningfully different palettes per surface. Most projects leave blank — top-level tokens apply to everything.

### Changed

- **`design-direction/SKILL.md` — full reconciliation with references.** Previously contradictory: SKILL.md said "Token frontmatter is read-only here" and ended with a handoff prompt to `init-project` Phase 4 path C; references already encoded token-writing behaviour. Now consistent. Phase list updated 7 → 8 phases (1–7 plus 6.5). "What it produces" expanded from 3 to 5 outputs (added token frontmatter + preview HTML). "Compatibility" block rewrites the token-edit rule to "via Phase 6.5 preview-then-approve, never silent." Phase 7 body rewritten — writes whatever Phase 6.5 approved, no handoff. Hard rule line 181 replaced: "Token frontmatter is written by Phase 6.5 + 7 only after explicit user approval via the HTML preview. Never write tokens silently; never skip the preview when changes are proposed." Sub-agent routing table adds Phase 6.5 row at reasoning tier. Output shape replaces the old regenerate-prompt with a clean wrote-list + `npx @google/design.md lint` next-step.

- **`design-direction/references/phase-7-write-outputs.md`** — deleted the "After writing — the optional handoff" section that asked "Want me to regenerate token frontmatter? hands off to init-project Phase 4 path C". Replaced with "After writing — clean exit" listing what was written (conditional on Phase 6.5 returning approved values) and pointing at the lint sync step. Hard rule line 18 already correctly stated "Token frontmatter is read-only UNLESS Phase 6.5 returned new token values" — preserved unchanged.

- **`init-project/references/phase-4-design-system.md` lines 9–32** — the "Optional handoff to design-direction (deep flow)" block updated. Path B description now mentions "DESIGN.md token frontmatter with an HTML preview for visual approval." When path B returns control, BOTH the BRAND.md step AND the DESIGN.md step in Phase 4 are skipped — `design-direction` owns them. Phase 4 continues from FUNDAMENTALS.md / TOOLING.md / DISCOVERIES.md only.

- **`templates/DESIGN.md`** — added the `type_scale:`, `chart_palette:`, `dashboard:`, `marketing:` blocks listed under Added. Body section grows a "Size scale" subsection in Typography pointing at the new `type_scale:` block with surface-ratio guidance.

- **Plugin manifests** — version bumped 2.0.1 → 2.1.0 in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Minor bump: behavioural expansion of `design-direction` (now writes tokens + renders preview) plus Phase 2/5 quality upgrades from earlier session work, no breaking changes.

### Compatibility

- **Existing projects on v2.0.x** — drop-in upgrade. The `design-direction` skill on existing initialized projects will detect the existing token shape and offer the alignment diff + preview only when the locked direction actually mismatches current tokens. Projects whose tokens already match the new direction get an "all MATCH — no token changes needed" report (silent re-confirmation, no preview). Pre-v2.1 projects without `type_scale:` or `chart_palette:` blocks get them added only on the next `design-direction` run that approves token changes — additive, never destructive.

- **`agents/preview/` directory** — new folder, only created when Phase 6.5 actually renders a preview. Each direction-level approval writes a new file; iteration writes a new `-v2`, `-v3` file alongside (never overwrites). Recommended to add `agents/preview/` to `.gitignore` — previews are throwaway approval surfaces, not canon. Phase 6.5 does the `.gitignore` add automatically on first preview generation if the line isn't present.

- **`init-project` Phase 4 path B handoff** — backwards-compatible. Projects bootstrapping via the deep flow now skip both BRAND.md and DESIGN.md steps in Phase 4 (previously skipped only BRAND.md and ran path C for DESIGN.md). The path C generator is no longer invoked from the path B handoff — `design-direction` owns DESIGN.md fully. Path A (quick flow) unchanged.

- **CSS-side architecture unchanged.** The `light_mode:` / `dark_mode:` paired blocks, material naming (`paper` / `ash` / `ink` / `hairline`), `oklch(from var(--token) calc(l - 0.08) c h)` derivations, and `npx @google/design.md lint` sync layer are all unchanged. v2.1 just fixes the upstream brain that picks the values feeding into them.

## [2.0.1] — 2026-05-21

Patch release. Correctness fixes across hooks, installer, build script, skill content, and templates. No new features. Skill count 15 → 14 (the `project-protocol` reference-doc skill was removed — see Removed below).

### Fixed
- **`hooks/hooks.json` — WORKLOG.md path now tool-aware.** Cowork sessions write to `cowork/WORKLOG.md`, Claude Code and Codex sessions write to `agents/WORKLOG.md`. Detection via `${CLAUDE_PLUGIN_ROOT}` / `${CODEX_PLUGIN_ROOT}` env vars. Previously, hooks referenced an unqualified `WORKLOG.md` at cwd root — silently no-op'd on every protocol-conformant project (the three-folder layout never creates a root `WORKLOG.md`). The discipline engine now correctly writes a real-time audit trail on protocol-conformant projects.
- **`hooks/hooks.json` — Stop / PreToolUse / SubagentStart / SubagentStop "cleared state" regex updated.** Previous regex `^# Worklog — cleared` did not match what `save-session` actually writes (`# Worklog — <tier>` on line 1, `> Cleared after each session.` on line 2). Regex now matches both the legacy heading and the current `save-session` output. Result: the Stop hook no longer fires false "unsaved work" warnings immediately after a clean `save-session`.
- **`install.sh` — added `--cowork` flag** (and `INSTALL_FLAVOR=cowork` env var) so Cowork users can install the stripped Cowork zip via the curl one-liner. Default behavior unchanged (FULL build for Claude Code / Codex).
- **`build.sh` — Cowork strip pass now relocates `templates/TOOLING.md`, `templates/STRUCTURE.md`, and `templates/CONTENT.md`** alongside the existing `FUNDAMENTALS.md` / `DESIGN.md` relocation. Previously, those three templates were absent from the Cowork build — Node projects via Cowork failed Phase 4 (`TOOLING.md` not found), and `build-component` / `marketing-brief` had no way to bootstrap their canonical files. Templates now ship into `skills/<consuming-skill>/references/` with paths patched at build time.
- **`build.sh` — STAGE_FULL tmpdir now covered by trap cleanup.** Previously, a `set -e` exit mid-full-build leaked the tmpdir. Both stages (FULL and Cowork) are now cleaned regardless of failure path.
- **`build-component` SKILL.md and phase-5 reference** — three stale "7 steps" references for `design-check` updated to "8 steps". This was missed when `design-check` Step 8 (auto-fix) shipped in v2.0.
- **`build-component` Codex sidecar** — `short_description` trimmed from 223 chars to under 200 to satisfy Cowork's validator cap.
- **`design-check`** — removed the "create component" trigger phrase to eliminate routing collision with `build-component`. Both skills still auto-chain in practice (`build-component` fires first, `design-check` fires post-write), but description-match arbitration is no longer ambiguous.
- **`discipline` SKILL.md** — added a `Triggers — ...` clause to the description for consistency with other gate skills (`audit-before-close`, `verify-by-reading`, `design-check`, `edit-plugin`).
- **`edit-plugin` SKILL.md** — removed a dead reference to a non-existent `commands/*` directory. The plugin has no `commands/` tree; the file set is `skills/`, `hooks/`, `templates/`, `.claude-plugin/`, `.codex-plugin/`.
- **`audit` SKILL.md** — added a `STRUCTURE.md` drift check (declared surfaces vs. actual codebase folders). Surfaces declared in `agents/STRUCTURE.md` that have no corresponding folder, and folders present in the codebase that aren't declared in `STRUCTURE.md`, are reported as drift.
- **`init-project` SKILL.md** — the output-layout block now lists `STRUCTURE.md` alongside the other `agents/`-tier files. Previously, `STRUCTURE.md` was referenced by `build-component` and `audit` but not surfaced in `init-project`'s own layout map.
- **`hooks/session-start-context.md`** — the `STRUCTURE.md` required-read line is now qualified with "(if present — created by `build-component` on first invocation)" so the SessionStart context injection does not imply the file is mandatory on every project.
- **`templates/TOOLING.md`** — added a one-line note that the author's `~/Arel OS/Projects/` example is illustrative; other users adapt the path prefix to their own project layout.
- **`templates/STRUCTURE.md` and `templates/CONTENT.md`** — previously dead templates (no skill cp'd from them). `build-component`'s phase-1-structure-detection now cps `STRUCTURE.md` → `agents/STRUCTURE.md` as the initial template, and `marketing-brief`'s phase-2-content-registry cps `CONTENT.md` → `agents/marketing/CONTENT.md`. Both templates now serve their intended bootstrap role.

### Removed
- **`project-protocol` skill** — pure reference doc that duplicated `README.md` and the `init-project` SKILL.md. Its triggers (`project start`, `init project`, `session start`, `read protocol`) caused routing ambiguity with `init-project` and `session-recap`. Any unique content was merged into `README.md` and `init-project` before deletion. Skill count 15 → 14.

### Changed
- **`README.md`** — skill count updated 15 → 14. "Session lifecycle (the core 5)" heading updated to "(the core 4)" with the `project-protocol` bullet removed.
- **Plugin manifests** — version bumped 2.0.0 → 2.0.1 in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Patch bump: correctness fixes only, no new features. Both manifest descriptions updated to reference 14 skills and to drop `project-protocol` from the listed skills.

### Compatibility
- Drop-in upgrade from v2.0.0. No file-format changes, no template-shape changes, no breaking changes to consumer projects. Existing projects pick up the corrected hook behaviour on next session start and the corrected Cowork build on next install.
- Removal of the `project-protocol` skill is invisible to consumer projects (the skill was a reference doc, never wrote files). Users who relied on `/project-protocol` as a slash invocation should use `init-project` or `session-recap` instead, depending on intent.

## [2.0.0] — 2026-05-20

### Added
- **`build-component` skill** — 14th skill. Per-component build skill with a 5-phase flow: (1) structure detection — reads `agents/STRUCTURE.md` or runs first-run detection to create it (surfaces present, component locations per tier, stack per surface, conventions detected); (2) intake & tier — silently infers Generic / Marketing / App tier from the request, surface-aware so dashboard-only projects never see the Marketing tier in prompts; (3) reuse scan — greps existing components for reusable primitives, proposes one of three strategies (compose existing primitives, extend an existing component, build a new primitive); (4) data shape & location — locks the component's props contract and the exact file path under the tier's folder; (5) preview & write — shows the diff before writing, then fires `design-check` automatically after. Detects existing project convention silently (cva + forwardRef + cn triplet or the project's own pattern — never imposes shadcn on a non-shadcn codebase). Supports adopt-external sub-mode (paste an Aceternity / Magic UI / 21st.dev snippet, normalize to project tokens and naming) and recreate-from-inspiration sub-mode (for installable libraries like shadcn — installs the canonical version rather than recreating it from a screenshot). Cross-tier import enforcement: Marketing components cannot import App components and vice-versa; both can freely import Generic primitives. Ships with Codex sidecar.
- **`marketing-brief` skill** — 15th skill. One-time deep marketing-site brief that runs ONCE, near the end of a project after features ship — not during early product work. Builds `agents/marketing/CONTENT.md` as the single source of truth for marketing content (FEATURES, AUDIENCES, COMPARISONS, TESTIMONIALS, FAQS, LEGAL_PAGES tables). Every marketing page reads from this registry — nav, footer, per-feature pages, comparison pages, FAQ sections, legal nav — so content updates happen in one place. Then proposes a sitemap (`agents/marketing/SITEMAP.md`), writes per-page briefs to `agents/marketing/briefs/`, per-page copy to `agents/marketing/copy/`, a media manifest to `agents/marketing/MEDIA.md` with a fictional-customer brand name asked once at the start and used throughout (the dub.co "acme" pattern), and per-page layout sketches to `agents/marketing/layouts/`. Auto-skips on dashboard-only / internal-tool projects (no marketing surface detected in `agents/STRUCTURE.md`). Never overwrites existing canon — offers a 3-way merge (replace / merge / append) for any conflict.
- **`templates/STRUCTURE.md`** — new template. Per-project structural map auto-generated by `build-component` on first run. Captures surfaces present (Marketing, Web app, Desktop app, Docs, Mobile), component locations per tier (Generic / Marketing / App-web / App-desktop), stack per surface, conventions detected (style system, file naming, folder structure, token chain, icon library), and cross-tier import rules enforced by `audit`. Edited by hand only when project structure changes (folder rename, new app added).
- **`templates/CONTENT.md`** — new template for the marketing content registry. Defines the canonical shape of the FEATURES / AUDIENCES / COMPARISONS / TESTIMONIALS / FAQS / LEGAL_PAGES tables that `marketing-brief` writes and every marketing page reads from. Includes per-table editing rules (immutable ids and slugs, audiences must exist before reference, verbatim testimonial quotes).
- **`init-project` modernize mode** — new Phase 0c. Fifth mode alongside `audit | migration | empty | fresh`. For already-initiated projects on v1.x, runs an interactive upgrade pass: per-canon-file confirmation loop (the user sees a diff against the current global template and approves or skips, file by file), silent global-standard updates to `FUNDAMENTALS.md` and `TOOLING.md` (same silent-overwrite rule as `init-project` Phase 4), a codebase design-system sweep via the upgraded `design-check` Step 8, `STRUCTURE.md` reconciliation (existing folder structure detected and written back), waste archival (any deprecated file is moved to `archive/<date>-modernize/` — never deleted silently), and an optional design-direction handoff for projects whose brand needs a rebuild. Triggered by user invoking with intent to upgrade, or by audit-mode detecting significant drift from the current global standard.

### Changed
- **`design-check` Step 8 (auto-fix)** — Step 8 now splits findings into two buckets. Auto-fixable (mechanical, low-risk): raw hex matching a defined token (`#0a0a0a` → `bg-background`), missing image dimensions, `<div onClick>` → `<button>`, three-period `...` → ellipsis `…`, unit non-breaking-space (`10 MB` → `10&nbsp;MB`), `outline: none` → `:focus-visible` rule. Human-judgment (still surfaced for user input only): cardinal sins (indigo accent, two-stop trust gradient, emoji-as-icon, hardcoded display font, AI-dashboard tile, invented metric, filler copy), banned words, raw hex with no matching token, missing meaningful alt text. Auto-fixes apply only on a single user batch confirmation — never per-file silent edits. **Safety rule:** never auto-fix when the target token isn't defined in `agents/DESIGN.md` (would silently create a broken reference). Batched per file for large codebases (one diff per file, user can accept all / skip file / accept individual). `allowed-tools` expanded to include `Edit, Write`.
- **`init-project` Phase 0 (mode detection)** — fifth mode `modernize` added alongside `audit | migration | empty | fresh`. Triggered by user invoking with intent to upgrade, or by audit-mode detecting significant drift from the current global standard (templates ahead of the in-project copies).
- **README skill count** — 13 → 15.
- **Plugin manifests** — version bumped 1.5.0 → 2.0.0 in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Major bump: behavioural expansion of `design-check` (now writes) and `init-project` (now modernizes already-initiated projects), two new skills (`build-component`, `marketing-brief`) closing the per-component-build and marketing-content gaps, mature end-to-end lifecycle coverage from bootstrap through ship through marketing handoff.

### Compatibility
- **Existing projects on v1.5.x** — fully compatible. `build-component` runs first-run detection inline and creates `agents/STRUCTURE.md` on first invocation; existing folder structure is detected, never imposed. `marketing-brief` auto-skips on dashboard-only / internal-tool projects (no marketing surface detected). `design-check` upgrade is additive — Step 8 auto-fix is opt-in (user must approve the fix batch, never applied silently). `init-project` modernize mode is opt-in (explicit invoke or user opt-in from the audit drift report).
- **`design-check` Edit capability** — the skill now has `Write`, `Edit` in its `allowed-tools` to apply auto-fixes. Cowork build still strips the `allowed-tools` line at package time, so no breaking change for any consumer.
- **`STRUCTURE.md`** — new file in `agents/`. Projects without one get it created on first `build-component` invocation; nothing else is affected (the audit / design-check / save-session flows tolerate its absence).
- **`agents/marketing/`** — new folder, only created when `marketing-brief` runs. Projects that never invoke `marketing-brief` never see it.

## [1.5.0] — 2026-05-20

### Added
- **`design-direction` skill** — 13th skill. Deep brand-direction diagnostic that sits one layer upstream of `init-project` Phase 4. Takes a single free-text brand dump (product, audience, problem, surfaces, monetisation, what-it-should-not-look-like) and silently extracts 9 taste axes — trust temperature, use frequency, information density, cultural anchor, brand archetype, reference tribe (look-like + look-unlike), surface mix, tempo, brand-specific refusal list. Returns a plain-English diagnostic for one-pass confirmation, proposes a 3–5 site reference moodboard, then offers 3 *meaningfully different* named design directions (e.g. "Editorial Cream", "Color Lab", "Warm Modern Indian") each with palette intent in words, type pairing, reference URL, and a "why this fits" line tied back to the diagnostic. After the user picks (hybrids allowed), writes a rich `agents/BRAND.md`, fills the `agents/DESIGN.md` Overview, and adds brand-specific anti-patterns to the DO NOT block — universal anti-patterns above are never edited, token frontmatter is never touched. Ends with an optional handoff to `init-project` Phase 4 path C to regenerate tokens against the locked direction. Works standalone on already-initiated projects to re-anchor brand. Ships with Codex sidecar; 7-phase skill structure with each phase in `references/` for progressive disclosure.
- **`templates/FUNDAMENTALS.md` — small Vercel-derived craft items.** Appended under existing sections: loading-state timing (150–300ms show-delay + 300–500ms minimum visible window to avoid flicker), stable skeletons (must mirror final layout exactly), loading buttons preserve label (`Save…` with spinner, never replaced by just a spinner), tooltip timing (first delayed, peers no-delay), ellipsis character (`…` not `...`), curly quotes, non-breaking spaces for glued terms (`10&nbsp;MB`, `⌘&nbsp;+&nbsp;K`, `Next.js&nbsp;16`), `scroll-margin-top` on anchored headings, `color-scheme` on `<html>`, `theme-color` meta for mobile address-bar / OS-task-switcher polish.

### Changed
- **`init-project` Phase 4 reference** — new "Optional handoff to `design-direction`" sub-section added before the existing BRAND.md A/B/C flow. Phase 4 now offers two paths: A (quick — existing 3-question BRAND.md flow), B (deep — hand off to `design-direction`). Default remains A. If the deep skill is unavailable on disk, silently falls through to A. When B is chosen, `design-direction` populates BRAND.md and DESIGN.md Overview + brand-specific DO NOT additions; Phase 4 then runs as path C with the much richer brief.
- **`README.md`** — skill count updated from 12 to 13; `design-direction` listed under Discipline skills.

### Compatibility
- **Existing projects on v1.4.x** — no breaking change. `design-direction` can be invoked standalone (`/design-direction` or trigger phrase like "re-anchor brand") against an already-initiated project. It reads existing `agents/BRAND.md` / `agents/STATUS.md` first and only asks for missing pieces. Existing populated sections are never silently overwritten — shown to user with a 3-way merge offer (replace / merge / append). DESIGN.md universal anti-patterns block is never touched; only the bottom brand-specific placeholder is filled. Token frontmatter is read-only in this skill — projects keep their existing tokens unless the user explicitly accepts the optional handoff to Phase 4 path C at the end.
- **Existing `FUNDAMENTALS.md` files** in initiated projects get the small Vercel-derived additions on next `init-project` run (silent overwrite — same global-standard rule as before).
- **Phase 4 handoff** — old `init-project` SKILL flow still works exactly as before for path A. Path B is opt-in via the new question.

## [1.4.0] — 2026-05-20

### Added
- **`edit-plugin` skill** — 12th skill. Self-discipline gate for any change to this plugin's own source (skills, hooks, manifests, templates, README, build scripts). 7-step protocol that chains `git add` → `commit` → `push` to every edit so the plugin source repo on disk stays in lockstep with `origin/main` on GitHub. Fixes the gap where an agent edited a skill, the user thanked them, and the change was never pushed — so the next pull / reinstall would lose it. Same gate-skill shape as `discipline` and `audit-before-close`; ships with a Codex sidecar.

### Changed
- **`save-session` skill** — added Step 10 "Git sync (commit, push, auto-merge into `main`)". After the WORKLOG → CHANGELOG/STATUS/BRIEF cascade, save-session now stages protocol .md changes, commits with a structured message, pushes the current branch to GitHub, and auto-merges into `main` via the worktree path resolved from `git worktree list`. Asks before staging anything outside `cowork/`, `agents/`, `human/`. Stops cleanly on detached HEAD / push failure / merge conflict with an exact recovery command. `allowed-tools` expanded to include `git:*`. Step 11 (Confirm) now reports the git outcome.
- **`README.md`** — skill count updated from 11 to 12; `edit-plugin` listed under Discipline skills.

### Compatibility
- Existing projects on v1.3.x: `save-session` works without configuration as long as the project's working directory is a git repo with a remote. Repos with no remote skip the push step and still merge locally.
- `edit-plugin` fires only for edits to this plugin's source repo — has no effect on consumer projects.

## [1.3.0] — 2026-05-19

### Added
- **`design-check` skill** — UI-work gate (new, 11th skill). Fires on any visual change (creating/editing components, styles, pages). Walks the agent through a 7-step sequence: read `DESIGN.md` + `FUNDAMENTALS.md`, search existing components for reuse, identify tokens needed, **halt on missing tokens** (propose addition, wait for user confirmation), write code using approved tokens only, scan diff for raw hex / px / font / `outline: none` / `<div onClick>` / images without alt-width-height, halt on violations. Same gate-skill shape as `discipline` and `audit-before-close`; ships with a Codex sidecar.
- **`templates/DESIGN.md` (new shaped template)** — Phase 4 now fills a complete scaffold instead of generating the shape from scratch. Token categories, accent-discipline rule (≤ 2 visible uses of `--primary` per screen), DO NOT section with universal anti-patterns, Extension protocol (need a missing value? stop, propose, wait, then add), and an Agent prompt guide are all baked in. The scaffold also formalises OKLCH-based derivation for hover/disabled tints so adding a "fourth color" isn't a new hex code, it's `oklch(from var(--primary) ...)`.

### Changed
- **`templates/FUNDAMENTALS.md` significantly tightened.** Existing 6 Levels / Ratio Rule / Motion Principles / Token Rule kept verbatim. Added: the **7 cardinal sins** (indigo hex, two-stop trust gradients, emoji-as-icons, hardcoded display fonts, AI-dashboard-tile shape, invented metrics, filler copy), the **5 required states** table (loading / empty / error / populated / edge) with loading-duration thresholds and error/empty composition rules, a **craft-details** section (focus / forms / images / touch / semantic HTML / URL state / performance), a **banned-words** list (hype / filler / corporate zombie / AI-slop openers), **icon discipline** (one library, `currentColor`, 3:1 contrast, semantic alt), **copy rules**, and a **pre-ship checklist** that `audit-before-close` runs. Type 2 of the Token Rule ("missing token") now reads **STOP and propose to the user; do not improvise** — the language change converts the rule from agent judgment into a halt-and-confirm enforced by `design-check`.
- **`init-project` Phase 4 reference** — DESIGN.md generation refactored. The skill no longer invents the shape per project; it reads `templates/DESIGN.md` and fills the placeholders (A: transfer existing, B: transfer + add, C: fresh). Hard rules: never delete the template's sections, never edit the DO NOT universals (only add brand-specific items), never edit the Extension protocol wording (it's enforced by `design-check`).
- **`audit` skill** — added a design-system scan step (UI projects only). Greps component files for raw hex / px / `font-family` strings, cardinal-sin patterns, accessibility floor violations (`outline: none` without `:focus-visible`, `<img>` missing alt/width/height, `<div onClick>`), and banned-words in shipped copy. Findings reported as category (A) — real violations.
- **`README.md`** — skill count updated from 10 to 11; `design-check` listed under Discipline skills; `audit` description notes the new design-system scan.

### Compatibility
- Existing projects on v1.2.x get the richer `FUNDAMENTALS.md` written on next `init-project` run (silent overwrite — global standard, same rule as before). DESIGN.md handling: if the project's existing DESIGN.md has the new format already (YAML frontmatter), Phase 4 fills gaps only; if it has the legacy format, Phase 4 re-shapes it into the template. No silent destruction of existing content.
- `design-check` fires on description match in any project that has both `agents/DESIGN.md` and `agents/FUNDAMENTALS.md` present. Projects without those files: the skill stops at step 1 and tells the user to run `init-project` first.

## [1.2.0] — 2026-05-15

### Added
- **Global Node tooling standard** — new `templates/TOOLING.md` template, locked 2026-05-15. Covers bun as the only package manager, Node 24 LTS via Homebrew, required project files (`.nvmrc`, `.npmrc`, `package.json` fields), and the Next.js / Turbopack defaults for Next 16. Same global-standard pattern as `FUNDAMENTALS.md` — overwritten verbatim from the plugin template on every `init-project` run.
- **`init-project` Phase 4 — `agents/TOOLING.md` step** — copies the new template into `agents/TOOLING.md` **only for Node projects** (detected by a `package.json` at the project root). Swift / Python / non-Node projects skip silently. If the project's actual `package.json` / `.nvmrc` / `.npmrc` drift from the standard, the mismatch surfaces as a `[VERIFY]` item at Phase 7 — never auto-fixed.

### Changed
- **`init-project` SKILL.md Hard rules** — `agents/TOOLING.md` added as a second explicit silent-overwrite exception alongside `agents/FUNDAMENTALS.md`. Both are global locked standards, neither is per-project.
- **Phase 3 root `CLAUDE.md` template** — non-negotiable rules gain rule #7: "If Node project: read `agents/TOOLING.md` before any package, install, or dev-server work. Use `bun` only — never `npm`, `pnpm`, or `yarn`." Gives the standard teeth at session start for Node projects without polluting Swift/Python ones.
- **Phase 3 root `README.md` template** — `agents/TOOLING.md` entry added to the agents/ catalog with the "Node only · never edited per project" cascade note.
- **Plugin README.md** — project-layout block now shows `TOOLING.md (Node only)` in the agents/ tier so installers see the addition before installing.

### Compatibility
- Existing Node projects on the v1.1.x layout get `agents/TOOLING.md` written on next `init-project` run (silent overwrite — global standard).
- Non-Node projects are unaffected: no new file is created and the root `CLAUDE.md` Node-only rule is a no-op for them.

## [1.1.0] — 2026-05-12

### Added
- **`init-project` Phase 0 (mode detection)** — runs first on every invocation and classifies the project as one of `audit | migration | empty | fresh`. Replaces the old inline audit-mode check inside Phase 1. See `skills/init-project/references/phase-0-mode-detection.md`.
- **`init-project` Phase 0a (empty bootstrap)** — when the project has no markdown anywhere, ask the user a short set of questions (project name, one sentence, target user, tech stack, stage, locked decisions, first direction) and use the answers to populate templates with real content instead of `[Project Name]` placeholders. See `skills/init-project/references/phase-0a-empty-bootstrap.md`.
- **`init-project` Phase 0b (old-version migration)** — when the project is on the older flat-root layout (root `CLAUDE.md` + protocol files at root, no `cowork/` / `agents/` / `human/` folders), migrate every old-layout file into the three-folder layout. Clean moves are mechanical (no user questions); ambiguous files (`STATUS.md`, `BRIEF.md`, `WORKLOG.md`, `CHANGELOG.md`) get a Haiku sub-agent classification. Root `CLAUDE.md` is split via sub-agent into root rules + `cowork/CLAUDE.md` + `agents/BRIEF.md`. All user content is preserved; new-version files are layered in only where missing. See `skills/init-project/references/phase-0b-migration.md`.

### Changed
- **Phase 2 (non-protocol merge)** now offers six routing options instead of four: **Cowork** (move into `cowork/`), **Agent docs** (move into `agents/docs/` or `agents/docs/detail/` and auto-register in `agents/docs/INDEX.md` + root `CLAUDE.md` `## Extended Context` — same pattern as the `add-context` skill), Merge, Reference, Leave, Skip. Closes the gap where extra markdown files (`ARCHITECTURE.md`, `NOTES.md`, team conventions, internal docs) had no clean tier-aware destination.
- **Phase 1 (discovery)** — layout detection moved upstream to Phase 0. Phase 1 still buckets every `.md` file but the mode + audit flag are passed in from Phase 0.
- **Phase 7 (final summary)** — output now varies by mode. Migration mode reports clean moves + sub-agent classifications + root `CLAUDE.md` split destinations + which new-version files were layered in. Empty mode reports the bootstrap answer object and surfaces `[VERIFY]` items. Audit mode lists filled-vs-untouched files and runs the `audit` skill's drift report.
- **`init-project` SKILL.md** — phase list expanded from 7 to 10 logical phases (0, 0a, 0b, 1–7). The mode-detection section replaces the old "Audit-mode detection" inline block.

### Build
- **`build.sh` now produces two zips per release.** Restoring the dual-zip shape that v1.0.2 dist had but the v1.0.2 build script had collapsed into one:
  - `project-protocol-vX.Y.Z.zip` — FULL build for Claude Code + Codex. Includes `hooks/`, `templates/`, `.codex-plugin/`, every `skills/<name>/agents/openai.yaml` Codex sidecar, and the `allowed-tools:` SKILL.md frontmatter line.
  - `project-protocol-vX.Y.Z-cowork.zip` — STRIPPED build for Cowork. Only `.claude-plugin/` + `skills/<name>/SKILL.md` (with `allowed-tools:` stripped) + `references/` / `examples/`. `FUNDAMENTALS.md` relocated into `skills/init-project/references/` and SKILL.md path reference patched at build time.

### Compatibility
- Existing projects on the v1.0.x three-folder layout are unaffected — they get classified as `audit` mode and the flow is the same as before.
- Old flat-root projects can now be migrated automatically via `init-project` instead of needing manual file moves.
- Empty repos can now be initialised meaningfully without writing placeholder-heavy templates the user has to clean up after.

## [1.0.2] — 2026-05-12

### Fixed
- **Cowork install:** `build.sh` now produces a Cowork-spec-compliant zip — the same zip also installs in Claude Code and Codex. Previously Cowork rejected the zip with "Plugin validation failed" because the build shipped components outside Anthropic's documented plugin spec.

### Changed
- Build artifact is stripped at build time to the Cowork plugin shape:
  - Kept: `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md` (+ `references/`, `examples/` sub-folders).
  - Stripped: `.codex-plugin/`, `hooks/`, `templates/`, `skills/<name>/agents/openai.yaml` (Codex sidecars), and the `allowed-tools:` SKILL.md frontmatter line.
  - `templates/FUNDAMENTALS.md` is relocated into `skills/init-project/references/` and the init-project SKILL.md path reference is patched at build time.
- Source repo still contains `.codex-plugin/`, `hooks/`, `templates/`, and `agents/openai.yaml` sidecars — they're just excluded from the shipped artifact. Re-enable them later if/when Cowork's validator loosens.
- Removed `keywords` field from both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Cowork's validator accepts only the four fields documented in Anthropic's plugin manifest schema (`name`, `version`, `description`, `author`).
- Shortened every SKILL.md frontmatter `description` for cleaner triggering. Previous: 287–589 chars. New: 160–198 chars. (The 200-char cap I had been "fixing for" turned out to be wrong — Anthropic's `create-cowork-plugin` SKILL ships a 340-char description and works — but shorter is still better.)
- `init-project` description retains the "or when a project has no root CLAUDE.md" auto-trigger hint.

## [1.0.1] — 2026-05-11

### Changed
- Updated plugin.json descriptions in both manifests to describe the three-folder layout (cowork/agents/human) + 10 skills + 8 hooks, replacing the stale legacy flat-layout file list.

## [1.0.0] — 2026-05-11

Initial public release. Clean v1.0.0 baseline.

### Skills (10)

**Session lifecycle:**
- `init-project` — bootstrap or audit a project with the standard three-folder layout.
- `save-session` — close a session: WORKLOG → CHANGELOG, update STATUS, clear WORKLOG (tier-aware).
- `session-recap` — mid-session snapshot of what's been done and what's still open.
- `add-context` — add extended context files (data contracts, domain reference, integrations).
- `project-protocol` — reference document defining the file set + session discipline.

**Discipline (new):**
- `discipline` — pre-action gate: pause, declare, cascade, verify, confirm.
- `verify-by-reading` — read-before-answer enforcement.
- `audit-before-close` — spec-vs-implementation check before marking work done.
- `discussion-mode` — read-only conversation mode when user signals thinking.
- `audit` — cross-file consistency check across canon.

### Hooks (8)

- `SessionStart` — inject required reading.
- `UserPromptSubmit` — pre-task classification reminder.
- `PreToolUse` (Edit|Write filter) — WORKLOG-cleared warning.
- `PreCompact` — back up WORKLOG before context compaction.
- `PostCompact` — re-orient context after compaction.
- `SubagentStart` / `SubagentStop` — log sub-agent invocations to WORKLOG.
- `Stop` — warn if WORKLOG has unsaved lines.

### Project layout

`init-project` creates a three-folder structure in target projects:

- Root `CLAUDE.md` (rules + folder map) + root `README.md` (file-and-dependency map).
- `cowork/` — orchestration tier (Cowork's files).
- `agents/` — project canon tier (Codex / Claude Code read here).
- `human/` — human-facing tier (daily steering file at `agenda.md`).

### Compatibility

- Skills follow [agentskills.io](https://agentskills.io) core spec — portable across Claude Code, Codex, Gemini CLI, Cursor, and other tools that adopt the standard.
- Every skill ships with a Codex `agents/openai.yaml` sidecar for polished Codex UX.
- Dual manifest: `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json`.
- Worktree detection in `session-recap` covers both Codex and Claude Code worktree paths.
