# project-protocol v2.5.0 — Redesign Plan

Date: 2026-05-26
Audit input: `AUDIT-2026-05-26.md` (32 findings — 6 HIGH, 14 MEDIUM, 12 LOW)
Locked decisions: 7 (see §2)

---

## 1. Goal

Collapse the 32 audit findings + Vish's seven locked architectural decisions into one coherent v2.5.0 release plan. Stop fixing things one-by-one. Build the right architecture once, then map every existing finding onto it.

The root cause across the audit is consistent: **the plugin describes what should happen and hopes the agent picks it up.** Description-match triggering, implicit prerequisites, undefined defaults, single-stack assumptions — all variants of "we trusted the agent's good judgment instead of making it deterministic." v2.5.0 fixes that by separating the plugin into three explicit layers, each with a different guarantee.

---

## 2. The three-layer architecture

| Layer | What it is | Guarantee | Used for |
|---|---|---|---|
| **Rules** | Root `CLAUDE.md` — always-loaded brain | The agent reads it every session. No selection logic. | Catalogs (skill index, hooks index, situation router) + hard rules |
| **Enforcement** | Hooks (`hooks/hooks.json`) | Runs deterministically on the matching event. No model judgment. | Post-write scans, version-drift detection, WORKLOG bookkeeping |
| **Workflow** | Skills | Rich, invokable. Some auto-fire, some called by slash, some explicit-called by other skill bodies. | Multi-step tasks the agent walks through |

**The rule that ties them together:** any cross-skill chain that today relies on "description match auto-fires the next skill" must convert to one of: an explicit `Skill(name)` invocation inside the parent's body, OR a hook that dispatches the next skill on a deterministic event. Zero auto-chains by keyword in v2.5.0.

---

## 3. Locked decisions (from the conversation)

1. **CLAUDE.md = brain.** Full skill index (every skill, one line each: name + when to use). Full hooks index (what fires on what event). Situation → skill router. All hard rules. Always loaded so the agent never has to discover capabilities.
2. **TOOLING.md** — ask at init for package manager (bun / pnpm / npm / yarn). On re-init, detect existing lockfile, ask "continue with X or switch." Personal path comes out completely.
3. **save-session** auto-detects environment (main / worktree / Cowork). Three deterministic branches. In Cowork, generates a copy-paste shell snippet because the runtime can't `git push`.
4. **Explicit `Skill` calls** replace description-match auto-chains in every skill body. Hooks back up where the chain is event-driven (e.g. PostToolUse design scan).
5. **No master skill.** Rejected — would add a new failure surface dependent on the same description-match it was meant to escape.
6. **Hybrid shadcn-first component rule.** Default: always shadcn primitive. Exception: native semantic elements (`<a href>`, `<button type="submit">` in forms, `<input type="hidden">`). When no shadcn primitive exists for the need, stop and ask user.
7. **Drift-detector + `migrate-project` skill + per-release migration manifests.** SessionStart hook detects plugin-version drift in the project; `migrate-project` applies version-by-version deltas from `migrations/vX.Y.Z.md` manifests. Every release from v2.5.0 onward ships its own manifest.

---

## 4. New artifacts being created

### 4.1 Root `CLAUDE.md` template — complete rewrite

Location: `skills/init-project/references/phase-3-three-folder-create.md` (the template block).

Structure of the new template:

```
# CLAUDE.md — [Project Name]

> Always loaded by every agent. The brain. Read top to bottom every session.

## Coding Standards
(keep current 4)

## Non-negotiable rules
(keep 1–8; add #9 shadcn-first; possibly compact rule #10 for "use the skills below, don't improvise workflows")

## Skill index — what's available and when to use it
(table: skill name | when to use it | how to invoke)

## Hooks index — what runs automatically
(table: hook event | what it does | what to do if it warns)

## Situation router — common requests → which skill
(table: "User asks for X" → "use skill Y, read Z first")

## Folder map
(keep current)

## Pre-task classification
(keep current)
```

Target length: 200–250 lines. Stays under the 300-line ceiling (relevant to M11).

### 4.2 New rule #9 — hybrid shadcn-first component selection

Inserted into the Non-negotiable rules block:

> **9. UI components — shadcn first when shadcn is in `package.json`.** Default: always use the shadcn primitive (`<Button>`, `<Input>`, `<Select>`, `<Dialog>`, `<Popover>`, `<Tooltip>`, `<Sheet>`, `<Drawer>`, `<Tabs>`, `<Accordion>`, `<DropdownMenu>`, `<Command>`, `<Toast>`, `<Alert>`, `<Checkbox>`, `<Radio>`, `<Switch>`, `<Slider>`, `<Textarea>`). Never silently fall back to the native element because it's faster to type. Allowed native elements: `<a href>` for navigation, `<button type="submit">` inside a `<form>` when no styled `<Button>` is needed, `<input type="hidden">`. If a needed primitive doesn't exist in shadcn (e.g. date-range picker), stop and ask: build one in `components/ui/` following shadcn conventions, install a community block, or use another library.

### 4.3 New hooks

**`PostToolUse` design-scan** — fires after every `Edit|Write` whose target path matches a UI file extension (`.tsx`, `.jsx`, `.vue`, `.svelte`, styles, `.swift` with `View`). Greps the diff for raw hex, raw px, raw `font-family` strings, native form elements when shadcn is in `package.json`, banned cardinal-sin patterns. Output is a stderr report the agent must respond to. Deterministic. No keyword guessing.

**`SessionStart` drift-detector** — reads `agents/.plugin-version` (created by `init-project` and updated by `migrate-project`). Compares to the current plugin version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. If project's recorded version is behind: prints a clear stop-block listing which manifests need to be applied, suggests running `migrate-project`, and writes a "skip-until-next-version" acknowledgement option. Does not nag within a session once acknowledged.

**`PostToolUse` design-check dispatcher** — fires after `build-component` writes a new component file. Explicitly invokes `design-check` on the new file. This is the deterministic replacement for the description-match auto-chain (H2). Also handles "anyone else writes to `components/ui/*`" — not just build-component.

### 4.4 New skill — `migrate-project`

Location: `skills/migrate-project/SKILL.md` (+ `agents/openai.yaml` sidecar).

Behavior:
1. Read `agents/.plugin-version` (or treat as "pre-2.5.0" if missing).
2. Read current plugin version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.
3. Read every `migrations/vX.Y.Z.md` manifest between recorded version (exclusive) and current version (inclusive), in order.
4. For each manifest: list the deltas, propose each change, confirm per change (or "apply all"), apply, mark applied.
5. Write the new plugin version to `agents/.plugin-version` when done.
6. Print a summary: applied N deltas, skipped M (already present), need user action on K.

Safety: every delta proposes before applying. The agent never silently overwrites. If a delta target file has been manually customized (detected by diff), surface the diff and let the user decide.

### 4.5 Per-release migration manifests

New folder: `migrations/`. One file per release from v2.5.0 onward: `migrations/v2.5.0.md`, `migrations/v2.6.0.md`, etc.

Manifest schema (per release):

```markdown
# Migration — v2.5.0

## Project-side deltas
Applied by `migrate-project` to projects on an older recorded plugin version.

### Files added
- `agents/.plugin-version` — records which plugin version this project is on.

### Files modified
- `agents/CLAUDE.md` (root) — full rewrite to the new "brain" structure. See template at [path]. Diff base: v2.4.0 template; preserve any custom sections under `## Project-specific notes`.
- `agents/TOOLING.md` — re-ask package manager question, regenerate from new template.
- `agents/STRUCTURE.md` — add `monorepo: true|false` field if not present.

### Rules added to CLAUDE.md
- Rule #9 (hybrid shadcn-first component selection).
- Rule #10 (use the skill index — don't improvise workflows).

### Files renamed / removed
(none in v2.5.0)
```

Backfill: also create `migrations/v2.4.0.md` (the only delta is "rule #8 added to root CLAUDE.md") so projects last touched on v2.3.0 can catch up cleanly.

### 4.6 `edit-plugin` discipline update

Add to the protocol: every release that changes user-visible behavior must include a `migrations/vX.Y.Z.md` manifest in the same commit. The skill enforces this — when bumping the version, check the manifest exists. If not, halt.

---

## 5. Findings → fixes mapping

### HIGH

| ID | Title | Layer / mechanism | Concrete change |
|---|---|---|---|
| **H1** | TOOLING.md personal path | Template + new init step | Strip personal path from rule body. `init-project` asks package-manager question; renders TOOLING.md from chosen flavor. Re-init detects lockfile, asks "continue with X." |
| **H2** | design-check auto-chain non-deterministic | **Hook + explicit Skill call** | Add `PostToolUse` design-check dispatcher (fires on writes to UI paths). In parallel, `build-component` Phase 5 explicitly invokes `Skill("design-check")` — belt and suspenders. |
| **H3** | design-check trigger keywords miss real phrasing | **Hook + CLAUDE.md catalog** | PostToolUse hook (A2/A3) fires deterministically on UI-file writes regardless of how the user phrases the request. CLAUDE.md skill catalog tells the agent design-check exists for any UI work. **No description-keyword broadening** — keeps the trigger surface simple and avoids over-fire. |
| **H4** | save-session Step 10 worktree assumption | **Skill rewrite** | save-session Step 10 detects environment: (a) on `main` directly → simple add+commit+push, (b) on worktree branch → existing merge-to-main flow, (c) Cowork → output copy-paste shell snippet. Silent auto-detection. |
| **H5** | build-page required-canon halt on missing layouts | **Skill rewrite** | Make `layouts/<slug>.md` a soft prerequisite. Warn-and-continue if brief + copy exist. Hard-halt only if brief or copy missing. |
| **H6** | monorepo detection missing | **Skill + template** | `init-project` Phase 0 / Phase 4 detect monorepo (root `package.json` with `workspaces` field or `pnpm-workspace.yaml` or `turbo.json`). Route TOOLING.md install to per-app `package.json` instead of root. STRUCTURE.md records `monorepo: true` + app paths. `design-check`, `audit`, `build-component` read this. |

### MEDIUM

| ID | Title | Layer / mechanism | Concrete change |
|---|---|---|---|
| **M1** | WORKLOG path env-var heuristic fragile | **Hook + new marker** | Add an explicit `agents/.session-type` marker file written at init (one of `cowork`, `claude-code`, `codex`). Hooks read this first; fall back to env-var heuristic only if marker missing. |
| **M2** | design-direction triggers miss "design feels off" | **CLAUDE.md catalog** | No description broadening. CLAUDE.md situation router includes "user expresses dissatisfaction with design quality (looks generic, palette feels off, etc.)" → design-direction. Agent reads the router every session and routes correctly. |
| **M3** | Tauri frontend-at-root not detected | **Skill update** | `build-component` Phase 1 adds `src-tauri/tauri.conf.json` as a "desktop app" signal regardless of frontend location. STRUCTURE.md records both surfaces. |
| **M4** | `agents/preview/` unreferenced in output map | **Template + audit skill update** | Add `agents/preview/` to `init-project` output layout map and root `README.md` template. Update `audit` to garbage-collect old preview HTMLs (keep most recent N per direction-slug). |
| **M5** | session-recap reads `sessions/` (doesn't exist in protocol) | **Skill cleanup** | Remove the dead `sessions/` read from session-recap Step 1. Replace with the actual orientation flow. |
| **M6** | design-check step 2 hardcodes glob paths | **Skill update** | design-check Step 2 reads `agents/STRUCTURE.md` for component locations (same pattern as `build-component` Phase 1). Falls back to default globs only if STRUCTURE.md missing. |
| **M7** | audit grep doesn't read STRUCTURE.md | **Skill update** | audit reads STRUCTURE.md for component paths. Adds exclude list (`node_modules`, `.git`, `dist`, `build`, `.next`). |
| **M8** | discussion-mode slash command inconsistent | **Manifest + description** | Standardize on `/discussion-mode` (matches skill name). If `/discuss` should be an alias, register it in the manifest's `commands` field. |
| **M9** | save-session `git:*` stripped by Cowork build | **Skill update + graceful degrade** | Step 10 detects whether `Bash(git:*)` is available. In Cowork (no git), output copy-paste snippet (H4's Cowork branch). Header notes Cowork limitation. |
| **M10** | marketing-brief sidecar names build-component as consumer | **Sidecar update** | Update `marketing-brief/agents/openai.yaml` to name `build-page` as primary consumer, `build-component` as secondary. |
| **M11** | add-context can push CLAUDE.md past 300-line ceiling | **Template + skill update** | Add stub `## Extended Context` section to phase-3 CLAUDE.md template. add-context checks line count before appending; if would exceed 300, warns and proposes summarizing older entries. |
| **M12** | discipline skill not invoked by agent self-action | **Documentation + explicit invocation** | Clarify discipline as user-invoked. In build-component / build-page, add explicit `Skill("discipline")` call when the change is structural (touches BRIEF, ROADMAP, or multiple files). |
| **M13** | build-page "never modify canon" rule conflicts with own steps 8 + 11 | **Skill rewrite** | Rewrite hard rule: name protected files explicitly (DESIGN.md, STRUCTURE.md, BRAND.md, FUNDAMENTALS.md, marketing/*). Explicitly permit BRIEF.md appends and INDEX.md updates. |
| **M14** | phase-4 uses npx `@google/design.md lint` (not in any dep list) | **Skill cleanup** | Either remove the lint step or document the optional dep in TOOLING.md under "optional dev tools" with install instruction. Recommended: remove. |

### LOW

| ID | Title | Layer / mechanism | Concrete change |
|---|---|---|---|
| **L1** | audit-before-close description has no `Triggers —` clause | **Description update** | Add `Triggers — "audit before close", "/audit-close", before any chapter close`. |
| **L2** | build-component 2-round cap conflicts with build-page no-cap | **Skill update** | Qualify build-component cap as standalone-only. When inline-called from build-page (detected via call-context or new flag), cap is lifted. |
| **L3** | design-direction uses WebSearch but not in allowed-tools | **Frontmatter update** | Add `WebSearch` to design-direction allowed-tools. |
| **L4** | marketing-brief lists WebSearch but doesn't use it | **Frontmatter cleanup** | Remove `WebSearch` from marketing-brief allowed-tools (no phase calls it). |
| **L5** | build-component fallback "vanilla CSS-with-tokens" conflicts with STRUCTURE.md template default "Tailwind v4 + shadcn" | **Skill update** | build-component Phase 1 treats STRUCTURE.md `[VERIFY]` markers as "not detected." Only treats values without the marker as authoritative. |
| **L6** | init-project Codex sidecar description too short | **Sidecar update** | Expand to 20–30 words describing the five modes (audit / migration / empty / fresh / modernize). |
| **L7** | add-context "type DONE" pattern UX-broken in Cowork | **Skill update** | Qualify Step 3: "Paste all content in a single message and end with DONE on the last line. In Cowork, you send one message at a time." |
| **L8** | session-recap `Bash(git:*)` allowlist too broad | **Frontmatter scoping** | Scope to `Bash(ls:*, pwd:*, git status:*, git worktree:*)`. |
| **L9** | build-page output says "design-check just ran" as fact | **Skill update** | Once H2 hook+Skill-call fix lands, the chain IS deterministic and this becomes accurate. No separate fix needed. (Or rephrase as "design-check ran via PostToolUse hook" for clarity.) |
| **L10** | CONTENT.md template has link-shortener example data | **Template cleanup** | Wrap every example row in `<!-- EXAMPLE — DELETE BEFORE USE -->` HTML comments, or replace with `[placeholder]` markers. |
| **L11** | edit-plugin hot-copy path hardcodes macOS | **Skill update** | Make platform-conditional. Detect OS or derive from `$CLAUDE_PLUGIN_ROOT`. |
| **L12** | init-project notes STRUCTURE.md created only by build-component | **Documentation fix** | Update note to: "created on first build-component run, OR during Phase 0c modernize." |

**Cross-cutting findings from §3 of audit** addressed by the locked architecture:

- *"Plugin assumes single-app, single-checkout, macOS-bun-Next.js"* → resolved by H1 + H4 + H6 + M3 + the new monorepo/Swift handling in §4.
- *"Skill-to-skill chains rely on description-match"* → resolved by §2's hook-OR-explicit-Skill-call rule, applied in H2 + H3 + L9 + the broader rewrite.
- *"Undefined behavior in small defaults"* → addressed per finding (L2, L5, M12, M13) plus the new CLAUDE.md situation router that gives the agent a deterministic decision tree.
- *"Swift / non-web structurally unsupported"* → tracked separately; not fully closed by this release. v2.5.0 adds STRUCTURE.md Swift surface detection and naming the Swift token file convention, but FUNDAMENTALS.md Swift section + Swift DesignTokens.swift template are deferred to v2.6.0 (called out in §8 below).
- *"audit and design-check have no memory"* → out of scope for v2.5.0 (would require persistence layer). Tracked in §8.

---

## 6. Execution order — phased

### Phase A — Foundation (must come first)
Everything downstream depends on the new CLAUDE.md brain and the new hook layer.

A1. Rewrite root `CLAUDE.md` template in `skills/init-project/references/phase-3-three-folder-create.md` per §4.1. Includes new rule #9 (§4.2).
A2. Add new PostToolUse design-scan hook (§4.3). Greps for hex, px, font-family, native-when-shadcn-exists.
A3. Add new PostToolUse design-check dispatcher hook (§4.3).
A4. Strip personal path from TOOLING.md template. Add ask-at-init logic to `init-project` for package manager. (Fixes H1.)
A5. Add `agents/.session-type` marker writing to `init-project`; update hooks to read it first (M1).

### Phase B — Skill chain determinism
Replace description-match auto-chains with explicit `Skill()` calls in skill bodies.

B1. `build-component` Phase 5 — explicit `Skill("design-check")` invocation after write (H2 belt-and-suspenders).
B2. `build-page` — explicit `Skill("build-component")` for new primitives (already there in spirit), explicit `Skill("design-check")` after each section write. Rewrite the conflicting "never modify canon" rule (M13). Soften `layouts/<slug>.md` to warn-and-continue (H5).
B3. `save-session` — explicit `Skill("audit-before-close")` invocation before Step 10. Cowork-aware Step 10 rewrite (H4, M9).
B4. Standardize slash commands across all skills (M8). Add `Triggers —` clause to skills missing it (L1). (Note: no description-keyword broadening — locked decision; CLAUDE.md catalog + hooks handle discoverability.)

### Phase C — Multi-stack robustness
B's deterministic chains assume STRUCTURE.md is right. C makes STRUCTURE.md right across stacks.

C1. `init-project` Phase 0 / Phase 4 monorepo detection (H6). STRUCTURE.md records monorepo flag + per-app paths.
C2. `build-component` Phase 1 Tauri-at-root detection (M3). STRUCTURE.md records desktop surface.
C3. `design-check` Step 2, `audit` step 3 — read STRUCTURE.md for component paths instead of hardcoding globs (M6, M7). Add exclude list.
C4. `build-component` Phase 1 — `[VERIFY]` markers in STRUCTURE.md treated as "not detected" (L5).

### Phase D — Drift system
With Phase A–C complete, projects can be brought up to the new baseline.

D1. Write `migrations/v2.4.0.md` (backfill) and `migrations/v2.5.0.md` (this release's deltas).
D2. New `migrate-project` skill (§4.4) + Codex sidecar.
D3. SessionStart drift-detector hook (§4.3).
D4. Update `edit-plugin` to require a migration manifest in every release commit (§4.6).
D5. Run `migrate-project` against each of the 15+ active projects on Vish's machine. (User-driven; not part of the plugin release.)

### Phase E — Cleanup sweep
Lower-stakes fixes; can run in parallel with D after A is done.

E1. Codex sidecar audit (M10, L6 + parity check across all skills).
E2. Template content cleanup (L10 — CONTENT.md examples).
E3. Frontmatter cleanups (L3, L4, L7, L8, L11).
E4. add-context ceiling check + stub section in CLAUDE.md template (M11).
E5. Remove dead `sessions/` read from session-recap (M5). Remove `agents/preview/` from audit blindspot (M4).
E6. Remove `npx @google/design.md lint` step (M14).
E7. Documentation fixes (L12).
E8. Discipline-mode explicit invocation in build-component/build-page for structural changes (M12).

### Phase F — Release
F1. Bump version 2.4.0 → 2.5.0 in both manifests.
F2. CHANGELOG entry with the full v2.5.0 story (architectural shift, not just a feature list).
F3. README skill-count update (+1 for `migrate-project`).
F4. `edit-plugin` commit + push + verify (per existing discipline).
F5. After release lands: backfill manifests cleanly, then test `migrate-project` on a sacrificial project before recommending it to the 15+ active ones.

---

## 7. Decisions locked from prior risk-review

These were §7 open risks in v1 of this plan. Locked by Vish, 2026-05-26.

**Risk 1 — CLAUDE.md size ceiling. LOCKED.**
Keep each catalog row to one line; use links to detailed docs instead of inlining. **If CLAUDE.md hits 280 lines, split the situation router into `agents/SITUATIONS.md` and leave a one-line pointer in CLAUDE.md.** The 300-line ceiling from M11 still applies.

**Risk 2 — Hooks + skill bodies double-firing design-check. LOCKED.**
Accept the double-fire. design-check is idempotent (just scans the diff). No deduplication machinery; simpler, safer.

**Risk 3 — `migrate-project` overwriting customizations. LOCKED.**
Each `migrations/vX.Y.Z.md` manifest references the previous version's template files (available in plugin git history). `migrate-project` diffs the project's current file against the previous template to detect user customization. If diverged, surface the diff and propose merge — **never silent overwrite.**

**Risk 4 — Cowork can't `git push` during `migrate-project`. LOCKED — Cowork does not run migrations.**
`migrate-project` detects Cowork (via `.session-type` marker; fallback to env-var heuristic) and **refuses to run.** Exit message: *"Migration must be run from Claude Code or your terminal — Cowork can't commit the version bump. Open this project in Claude Code and re-run `/migrate-project`."* Regular `save-session` Cowork-aware copy-paste-snippet path (H4 / M9) is unaffected — that's for normal saves.

**Risk 5 — Trigger keyword broadening (H3). LOCKED — no broadening.**
**Do not broaden description keywords anywhere.** CLAUDE.md catalog handles discoverability (agent reads it every session); PostToolUse hooks handle deterministic firing on file events. Dropping keyword broadening drops a whole class of complexity — no over-fire risk because we're not adding keywords. Surface stays simple.

**Risk 6 — 15+ projects flagging drift at next open. LOCKED.**
Drift hook respects per-version skip stored in `agents/.plugin-version-skip`. Next plugin update re-prompts. **No permanent skip option** — would let users suppress forever and never migrate. Release notes for v2.5.0 include guidance: "run `migrate-project` on each project at your own pace."

**Risk 7 — `audit-before-close` double-call. LOCKED.**
Accept. Idempotent. Same rationale as Risk 2.

---

## 8. Out of scope for v2.5.0 — deferred to v2.6.0

These came up but the release is already large.

- **Full Swift / SwiftUI design system support.** v2.5.0 detects Swift surfaces and names `DesignTokens.swift` as the token file. A complete Swift FUNDAMENTALS.md section + `DesignTokens.swift` template + Swift-aware design-check grep patterns ship in v2.6.0.
- **Audit / design-check memory.** Cross-cutting finding #5 from the audit. Requires a `agents/DISCOVERIES.md`-like persistence layer for "deliberately not fixed." Tracked separately.
- **Vue / Svelte first-class support.** STRUCTURE.md will detect them (Phase C3), but the design-check primitive list (rule #9) currently names only shadcn React components. A parallel shadcn-vue / svelte-shadcn rule needs a separate design pass.
- **Web-search-driven moodboard for design-direction in Cowork.** Cowork has WebFetch but not the full WebSearch API. Phase 4 of design-direction degrades gracefully but the experience is worse in Cowork.

---

## 9. Supplemental decisions — all locked

1. **TOOLING.md re-init flow:** detect existing lockfile, default to detected, one-key confirm. Asked on first init; on re-init the detected value is the default and user just confirms.
2. **CLAUDE.md split mitigation:** if CLAUDE.md exceeds 280 lines, split situation router to `agents/SITUATIONS.md` with a one-line pointer remaining in CLAUDE.md.
3. **Drift-hook acknowledgement persistence:** per-version skip (re-prompts on next plugin update). No permanent-skip option.
4. **CHANGELOG style for v2.5.0:** detailed architectural narrative (like v2.3.0's build-page story). This release is the architectural shift; a bullet list won't carry the meaning.

---

## 10. Effort estimate

Rough — for planning, not commitment.

| Phase | Scope | Estimated session count (each ~1 hour) |
|---|---|---|
| A | Foundation (CLAUDE.md rewrite, new hooks, TOOLING.md ask-flow, session-type marker) | 3–4 |
| B | Skill chain determinism (5 skills rewritten + trigger broadening + slash standardization) | 4–5 |
| C | Multi-stack (monorepo + Tauri + STRUCTURE.md reads in design-check/audit + [VERIFY] handling) | 2–3 |
| D | Drift system (migrate-project skill + 2 manifests + SessionStart hook + edit-plugin update) | 3–4 |
| E | Cleanup sweep (12 small fixes) | 2 |
| F | Release | 1 |
| **Total** | | **15–19 sessions** |

Parallelism: D and E can run in parallel with B/C after A is done. With focused sessions and one chunk per session, this is a 2–3 week release at current cadence.

---

## 11. Execution — parallel where possible

Phase A is sequential (foundational; everything downstream depends on it). Phases B / C / D / E run in parallel after A commits. Phase F is the release wrap.

- **Phase A** — 1 Sonnet agent does the full foundation in one session: rewrite CLAUDE.md template (A1, A2 rule #9), add PostToolUse design-scan hook (A3a), add PostToolUse design-check dispatcher hook (A3b), strip personal path from TOOLING.md + add ask-at-init for package manager (A4), add `.session-type` marker writing (A5). Single coherent commit.
- **Phases B + C + D + E** — 4 parallel Sonnet agents, disjoint file slices. Each commits its own slice. Brief coordination at slice boundaries (build-component is touched by both B1 and C2 — split at file level).
- **Phase F** — manual: version bump 2.4.0 → 2.5.0, detailed CHANGELOG narrative, README skill-count update, final commit + push, verify `origin/main`.

This plan is now definitive. Proceeding to dispatch.
