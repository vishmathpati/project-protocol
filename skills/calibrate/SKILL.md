---
name: calibrate
description: Calibration pass that sits between the reference moodboard and the three-directions step — turns a project's brand + register + archetype into an ANNOTATED moodboard and a follow/deviate/refuse conventions audit, grounded in real reference sites captured live. Triggers — "calibrate", "build the moodboard", "annotate references", "conventions audit", "which conventions do we follow or break", "ground the directions in real sites".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(which:*, open:*, ls:*, cat:*, cp:*, mkdir:*, test:*, sleep:*, curl:*, nc:*), AskUserQuestion, Task, WebSearch, mcp__aside__repl
---

# Calibrate

The step that makes the three named directions land on real references instead of training-data averages. Sits inside `design-direction`, between Phase 4 (the reference moodboard, a plain list of URLs) and Phase 5 (three named directions). It converts that list into a **captured, annotated moodboard** and a **follow / deviate / refuse conventions audit** written to `brain/DESIGN.md`.

Without this pass, Phase 5 proposes directions from memory and the output feels generic. With it, every direction can point at a real tile with a written reason, and the conventions the brand keeps vs. breaks are decided consciously — not by default.

This skill does not pick a direction and does not write tokens. It calibrates the taste inputs, then hands back to `design-direction` Phase 5.

---

## When this fires

- Invoked from `design-direction` after Phase 4, before Phase 5 (the intended path).
- User asks: "calibrate", "build the moodboard", "annotate these references", "run the conventions audit", "which conventions should we follow or break", "ground the directions in real sites".
- Slash command: `/calibrate`.

Prerequisites — halt and route if missing:

- `brain/DESIGN.md` must carry an **`archetype:`** (v4.0.0+ frontmatter field).
- `brain/BRAND.md` must carry a **register** — the diagnostic from `design-direction` Phases 1–3 (trust temperature, density, tempo, cultural anchor).
- If either is absent, route to `design-direction` (Phases 1–3, plus init if archetype was never set) first via `Skill("design-direction")`.

Skip conditions: user says "skip calibrate", "no moodboard", "just give me directions" — in that case return to `design-direction` Phase 5 immediately.

---

## What it produces

Three concrete outputs, all under the project's `brain/` tier:

1. **`brain/moodboard/` — captured references.** Hero / mid / end viewport screenshots per reference site, named `<slug>-hero.png` etc.
2. **`brain/moodboard/notes.md`** — one entry per reference, each carrying a written **"why it works"** line. No unlabeled tiles (the Zhuo/Kowalski rule — a moodboard tile without a stated reason is decoration, not calibration).
3. **`brain/DESIGN.md` — conventions audit block.** Three buckets appended to the DO/annotations area: **FOLLOW**, **DEVIATE**, **REFUSE**. Written only after the user has seen them.

Nothing else is touched. Token frontmatter, direction lock, and `BRAND.md` restructuring stay owned by `design-direction`.

---

## Step 1 — Build the mission file

Assemble a single `brain/moodboard/mission.md` (working scratch, not canon) that the rest of the pass reads from. Pull, verbatim where possible:

- **Brand** — product, audience, problem, surfaces, look-unlike incumbent — from `brain/BRAND.md`.
- **Register** — trust temperature, information density, tempo, cultural anchor — from the diagnostic in `brain/BRAND.md`.
- **Archetype** — the single locked `archetype:` from `brain/DESIGN.md` + its one-line meaning.

The mission file is the brief every later step answers to. If any of the three is thin or missing, stop and ask one focused question — do not invent register values.

→ Reasoning-tier `Task` sub-agent may assemble this from a long `BRAND.md`. Fast tier for pure extraction.

---

## Step 2 — The tiered inspiration source map

Never moodboard from one tier alone. A single-tier board copies one site's whole worldview; the tiers exist so craft, structure, parts, and type/color are sourced independently and recombined. Walk the tiers, collect candidate URLs against the mission file:

| Tier | Sources | What it supplies |
|------|---------|------------------|
| **Ceiling** | Awwwards, Godly, siteinspire | Sets the craft bar — the level of finish the brand is allowed to reach for. |
| **Skeleton** | Mobbin, Land-book, Lapa Ninja, SaaSFrame | Supplies layout patterns and page structure for the surfaces this product has. |
| **Parts** | 21st.dev | Component-level building blocks (nav, hero, pricing, cards). |
| **Type / color** | Typewolf, Fonts In Use | Real type pairings and palettes in the wild, with attribution. |
| **Texture / photography mood ONLY** | Pinterest | Mood, grain, photographic direction. **Never** layout — Pinterest boards flatten structure into pretty tiles and will mislead the skeleton. |

Rules:
- **Never source layout from Pinterest.** Texture and photographic mood only.
- **Pull from at least three tiers** before assembling the board. A board that is all-ceiling has no structure; all-skeleton has no craft ceiling.
- Prefer sites the audience already trusts and the look-unlike incumbent's *opposites*. Honor any site the user named in the brand dump.
- Use `WebSearch` to resolve current, openable URLs. Do not invent URLs.

→ Reasoning-tier `Task` sub-agent selects candidates; it knows design-conscious sources.

---

## Step 3 — Browser capture (Aside)

The board is captured live so the annotations describe what is actually on screen today, not a remembered version.

### Detect Aside

Check whether Aside is installed — look for the `aside` CLI (`which aside`) or the `mcp__aside__repl` tool.

- **Installed** → use it silently. Do not narrate the browser plumbing to the user.
- **Not installed** → ask the user to install Aside. That is the **only** browser question this skill asks — do not offer a three-way "Aside / Chrome MCP / manual" menu. If the user declines, fall back to listing the reference URLs with their why-it-works lines (unannotated-by-capture) and continue to Step 4 without screenshots.

### Runbook (tested — follow exactly)

Drive Aside through `mcp__aside__repl`. This runbook is load-bearing; deviating from it disconnects CDP.

- **Launch-and-wait for the daemon.** The daemon listens on `127.0.0.1:21420`. If it is down, run `open -g -a Aside` and wait ~10s before the first REPL call. Probe with `curl` / `nc` against the port before assuming it is up.
- **NEVER take fullPage screenshots.** FullPage capture disconnects CDP 100% of the time. Instead capture **hero / mid / end** viewport screenshots by scrolling: `mouse.wheel` then a **2s settle** (4–5s on animation-heavy sites) before each shot.
- **NEVER use `page.evaluate()` for scrolling.** Use `mouse.wheel` only.
- **One action per REPL call.** Do not batch actions into a single call.
- **On CDP disconnect, re-`attachBrowserTab` and retry.** Tab state survives the disconnect, so the retry resumes where it left off.
- **Write to `./artifacts/`** inside the session sandbox first, then `cp` the files out to `brain/moodboard/`. Do not write screenshots straight to `brain/`.
- **Tolerate auto-update session loss** — if Aside auto-updates mid-run and drops the session, relaunch (launch-and-wait) and re-attach.
- **Close visible tabs after** the board is captured.

---

## Step 4 — Assemble the annotated moodboard

`cp` the captured shots from `./artifacts/` into `brain/moodboard/` and write `brain/moodboard/notes.md`.

**Every reference carries a written "why it works."** No unlabeled tiles — a tile without a stated reason is decoration, not calibration (Zhuo/Kowalski). Each entry:

```
### <Site name> — <tier: ceiling | skeleton | parts | type-color | mood>
URL: <full url>
Captured: <slug>-hero.png · <slug>-mid.png · <slug>-end.png
Why it works: <one or two sentences naming the register/archetype axis it satisfies —
  e.g. "restraint + one warm accent hits the high-trust + Ruler register; the type
  does the emotional work, not color.">
```

### Optional gut-test

If the user wants to pressure-test the board, show ~6–8 references and have them score each **1–5**. The scores position the register dials: a consistently high-scored cluster tells you which register corner the audience actually leans toward, and Step 5's buckets follow that lean. One pass — do not loop the scoring.

---

## Step 5 — Conventions audit → FOLLOW / DEVIATE / REFUSE

From the annotated board + register + archetype, decide which genre conventions the brand keeps, which it consciously breaks, and which it refuses. Write three buckets to `brain/DESIGN.md`:

- **FOLLOW** — genre expectations the brand honors because breaking them costs trust or legibility. (E.g. "pricing page shows a comparison table" for SaaS; "hero states the offer above the fold".) Each is an expectation the audience already has.
- **DEVIATE** — the conscious signature moves, each with a one-line justification for *why the audience tolerates the break*. This is where the brand earns distinctiveness. A deviation without a justification is a mistake, not a signature.
- **REFUSE** — patterns that violate the register and are banned outright. These merge with the brand-specific refusal list; enforced downstream by `design-check` and `audit` exactly like the universal anti-patterns.

Write shape appended to `brain/DESIGN.md` (do not touch the universal anti-patterns above it):

```
## Conventions audit (from calibrate)

FOLLOW — genre expectations we keep
- <convention> — <why keeping it protects trust/legibility>

DEVIATE — conscious signature moves
- <move> — <why the audience tolerates this break>

REFUSE — patterns that violate the register
- <pattern> — <which register axis it violates>
```

Show all three buckets to the user before writing. One confirmation pass, then write.

→ Reasoning-tier `Task` sub-agent drafts the buckets — this is the highest-judgment step in the pass.

---

## Handoff — back to design-direction Phase 5

Calibration is done. The three-directions step is now grounded in a captured, annotated board and an explicit conventions audit. Hand back explicitly:

```
Skill("design-direction")
```

Tell `design-direction` to resume at **Phase 5 (three named directions)**, now reading `brain/moodboard/notes.md` and the conventions audit block in `brain/DESIGN.md`. Each proposed direction must be able to point at a real tile and respect the FOLLOW / DEVIATE / REFUSE buckets.

**No keyword auto-chain.** This handoff is an explicit `Skill()` call, per the plugin's v2.5.0 architecture — nothing here fires on a trigger word.

---

## Hard rules

- **Never moodboard from one tier alone.** Pull from at least three tiers of the source map.
- **Pinterest is texture/photography mood only — never layout.**
- **No unlabeled tiles.** Every reference in `notes.md` carries a written "why it works" (Zhuo/Kowalski).
- **Aside is the one browser question.** Detect it; if missing, ask to install — no three-way menu.
- **Never fullPage-screenshot, never `page.evaluate()` to scroll, one action per REPL call.** These disconnect CDP.
- **Write to `./artifacts/` then `cp` to `brain/moodboard/`.** Never straight to `brain/`.
- **Only the conventions-audit block is written to `DESIGN.md`.** The universal anti-patterns above it are sacred; never edited here.
- **This skill does not pick a direction or write tokens.** It hands back to `design-direction` Phase 5.
- **Every handoff is an explicit `Skill()` call.** No auto-chains.

---

## Sub-agent routing

| Step | Tier | Why |
|------|------|-----|
| Step 1 mission-file assembly from a long `BRAND.md` | fast | Pure extraction |
| Step 2 tiered source selection | reasoning | Knowledge of design-conscious sources across tiers |
| Step 3 Aside capture orchestration | fast | Mechanical, runbook-driven |
| Step 4 "why it works" annotations | reasoning | Judgment tying each tile to a register/archetype axis |
| Step 5 FOLLOW / DEVIATE / REFUSE buckets | reasoning | Highest-judgment step in the pass |

Never use the most expensive model. Reasoning tier (Sonnet) is the ceiling.

---

## Difference from related skills

- **`design-direction`** — the parent. Owns Phases 1–7, picks the direction, writes tokens. `calibrate` is its Phase 4→5 bridge; it hands back and never picks a direction.
- **`build-component` / adopt-external** — normalizes a *specific* pasted component against existing tokens. `calibrate` works one layer up, on taste inputs, before any component or token exists.
- **`design-check`** — the write-time gate that later enforces the REFUSE bucket this skill writes.
- **`discussion-mode`** — pure talk, no writes. Use it to argue about references first, then `calibrate` to capture and lock them.

---

## Output shape (end of skill)

```
calibrate — summary

Mission: <archetype + register one-liner>
Board: <N> references across <tiers used> — captured via <Aside | URL-list fallback>

Wrote:
  ✅ brain/moodboard/ — <N>×3 viewport screenshots
  ✅ brain/moodboard/notes.md — every tile annotated
  ✅ brain/DESIGN.md — conventions audit: FOLLOW <a> · DEVIATE <b> · REFUSE <c>

Next step: Skill("design-direction") → resume Phase 5 (three named directions),
now grounded in the captured board + conventions audit.
```
