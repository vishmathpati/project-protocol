---
name: calibrate
description: Two-round design-research engine that sits between the reference moodboard and the three-directions step. Orchestrates an Aside-run SWEEP (named concepts) then a DEEP TEARDOWN (forensic autopsy of the chosen concept's best examples), relayed through the user as paste-able blocks, then folds the returns into an annotated moodboard and a follow/deviate/refuse conventions audit. Triggers — "calibrate", "run design research", "build the moodboard", "sweep the field", "annotate references", "conventions audit", "which conventions do we follow or break", "ground the directions in real sites".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(which:*, open:*, ls:*, cat:*, cp:*, mkdir:*, test:*, sleep:*, curl:*, nc:*), AskUserQuestion, Task, WebSearch, mcp__aside__repl
---

# Calibrate — the two-round research engine

The step that makes the three named directions land on real, forensically-verified references instead of training-data averages. Sits inside `design-direction`, between Phase 4 (the reference moodboard, a plain list of URLs) and Phase 5 (three named directions).

It runs a **two-round research engine** whose thinking is done by an Aside browser agent and **relayed through the user as paste-able text blocks**:

1. **Round 1 — SWEEP.** Aside discovers the field for the niche and groups it into **named concepts**. Calibrate ingests the summary and runs a **checkpoint with the user** — pick one concept, or blend at the component level.
2. **Round 2 — DEEP TEARDOWN.** Aside autopsies the chosen concept's best real examples with DevTools (real fonts, real palette, real motion stack). Calibrate folds the returns into an annotated moodboard and a follow/deviate/refuse conventions audit.

This skill is the **plugin-side orchestrator**. Aside is the researcher — its whole brain is the static `design-research` skill in `aside-skill/design-research/SKILL.md`, which the user installs into Aside once. Calibrate never does the browsing thinking; it composes the per-round mission prompts from canon, hands them to the user to paste, ingests what comes back, and writes canon. It does not pick a direction and does not write tokens — it calibrates the taste inputs, then hands back to `design-direction` Phase 5.

**Reference files (do not duplicate — this skill points into them):**
- `aside-skill/design-research/SKILL.md` — the static skill the user installs into Aside (rounds, saturation law, tier map, teardown checklist, technical-detection cheatsheet, the two summary-block formats, disk-write paths, comms protocol).
- `references/mission-prompt-template.md` — the per-project prompt template calibrate fills from canon (Round-1 and Round-2 variants, `<placeholders>` mapped to canon sources).
- `references/round-formats.md` — the shared block + file formats (single source of truth for both calibrate and the Aside skill).

The interface contract these all obey is the v4.1 Research-Engine Interface Spec (`docs/interface-spec-research-engine.md` in the plugin repo) — if a format changes, it changes there first.

---

## When this fires

- Invoked from `design-direction` after Phase 4, before Phase 5 (the intended path).
- User asks: "calibrate", "run design research", "sweep the field", "build the moodboard", "annotate these references", "run the conventions audit", "which conventions should we follow or break", "ground the directions in real sites".
- Slash command: `/calibrate`.

### Prerequisites — halt and route if missing

- `brain/DESIGN.md` must carry an **`archetype:`** (v4.0.0+ frontmatter field).
- `brain/BRAND.md` must carry a **register** — the diagnostic from `design-direction` Phases 1–3 (trust temperature, information density, tempo, cultural anchor).
- If either is absent, route to `design-direction` (Phases 1–3, plus init if archetype was never set) first via `Skill("design-direction")`.

### Skip conditions

User says "skip calibrate", "no moodboard", "just give me directions" — return to `design-direction` Phase 5 immediately, without running either round.

---

## What it produces

All under the project's `brain/` tier:

1. **`brain/research/concepts.md`** — Round-1 field map: the named concepts (Aside writes to disk; calibrate reconstructs from the paste block on Fallback C).
2. **`brain/research/teardowns/<slug>.md`** — one forensic teardown per site of the chosen concept (Round 2).
3. **`brain/moodboard/`** — hero / mid / end viewport screenshots per site, named `<slug>-hero.png` etc.
4. **`brain/moodboard/notes.md`** — one entry per reference, each carrying a written **"why it works"** line that now cites teardown evidence (existing v4.0.0 per-entry format). No unlabeled tiles (Zhuo/Kowalski — a tile without a stated reason is decoration, not calibration).
5. **`brain/BRAND.md`** — the concept decision: a Decisions-log line + a Locked-direction seed (calibrate writes the checkpoint outcome here so all skills see it).
6. **`brain/DESIGN.md`** — the conventions audit (FOLLOW / DEVIATE / REFUSE), now **evidence-backed** by the teardowns.

Token frontmatter, direction lock, and `BRAND.md` restructuring stay owned by `design-direction`.

---

## Step 1 — Prerequisites + first-run install check

**1a. Gate the register + archetype** (see Prerequisites above). If either is missing, route to `design-direction` and stop.

**1b. Confirm the Aside `design-research` skill is installed.** The engine's thinking lives in a static skill the user installs into Aside **once**. Check whether Aside is present at all — look for the `aside` CLI (`which aside`) or the `mcp__aside__repl` tool.

- **Aside present, skill status unknown** → ask the user once, plainly: "Have you installed the `design-research` skill into Aside? If not, install `aside-skill/design-research/SKILL.md` into your Aside skills once — it's the browser's whole brain for this and never changes per project." Point them at the file; do not paste its contents inline.
- **Aside present, skill installed** → proceed to Step 2 (Primary transport: manual skill + prompt relay).
- **Aside absent** → offer a fallback (below). This is the only browser question this skill asks — do not offer a broad menu of drivers.

### Transport methods (same file contract for all three — see `references/round-formats.md`)

- **Primary — manual skill + prompt relay.** Aside runs the installed `design-research` skill; the user relays the paste blocks between calibrate and Aside. Works for any user, any project. This is the default path Steps 2–6 describe.
- **Fallback A — MCP repl (calibrate drives Aside directly).** Used only when no human relay is available and calibrate must drive the browser itself through `mcp__aside__repl`. The tested runbook is load-bearing — follow it verbatim:
  - **Launch-and-wait for the daemon.** It listens on `127.0.0.1:21420`. If down, run `open -g -a Aside` and wait ~10s before the first REPL call. Probe with `curl` / `nc` against the port before assuming it is up.
  - **NEVER take fullPage screenshots** — fullPage disconnects CDP 100% of the time. Capture hero / mid / end viewport shots by scrolling: `mouse.wheel` then a 2s settle (4–5s on animation-heavy sites) before each shot.
  - **NEVER use `page.evaluate()` for scrolling.** Use `mouse.wheel` only.
  - **One action per REPL call.** Do not batch actions.
  - **On CDP disconnect, re-`attachBrowserTab` and retry.** Tab state survives; the retry resumes where it left off.
  - **Write to `./artifacts/`** inside the session sandbox first, then `cp` files out to `brain/moodboard/`. Never write screenshots straight to `brain/`.
  - **Tolerate auto-update session loss** — relaunch (launch-and-wait) and re-attach if Aside updates mid-run.
  - Under Fallback A, calibrate itself produces the two summary blocks (it is playing Aside's role), then continues to the same ingest steps.
- **Fallback C — pure paste (no Aside FS access).** Aside prints everything into the summary blocks; calibrate writes **all** canon — including `concepts.md` and the teardown files — from the paste blocks alone. This is why the blocks must be self-sufficient. Screenshots may be absent in this mode; annotate from the block text.

---

## Step 2 — Generate the Round-1 mission prompt (SWEEP)

Fill the **Round-1 variant** of `references/mission-prompt-template.md` with real canon values. Do not write the prompt from memory — pull every value from canon:

| Placeholder | Canon source |
|---|---|
| Niche | `brain/BRAND.md` → `## Product` → Niche |
| Register (trust temperature · density · tempo · cultural anchor) | `brain/BRAND.md` register diagnostic |
| Audience + emotional state on arrival | `brain/BRAND.md` |
| Distinctive asset (the ownable thing) | `brain/BRAND.md` |
| Look deliberately UNLIKE `<incumbent(s)>` | `brain/BRAND.md` |
| Refusals + dated anti-cliché list | `brain/BRAND.md` / `brain/DESIGN.md` refusals |
| Archetype + one-line meaning | `brain/DESIGN.md` `archetype:` |
| research_depth (quick / standard / deep) + its meaning | `brain/DESIGN.md` frontmatter `research_depth:` |
| Surfaces present | `brain/BRAND.md` |
| Absolute disk paths (`brain/research/concepts.md`, `brain/moodboard/`) | this project's `brain/` |

The header, section order, and closing "print the ROUND-1 SUMMARY BLOCK" instruction come from the template — do not reorder or rename sections. If any canon value is thin or missing, stop and ask one focused question; never invent a register value or a niche.

**Present the filled prompt in a fenced block** for the user to copy into Aside. Then **STOP** — tell the user to paste it into their Aside `design-research` chat, let it run, and paste the **ROUND-1 SUMMARY BLOCK** back here. Do not proceed until it arrives.

→ Reasoning-tier `Task` sub-agent may fill the template from a long `BRAND.md`. Fast tier for pure extraction.

---

## Step 3 — Ingest Round 1 + validate

When the user pastes the ROUND-1 SUMMARY BLOCK back:

1. **Parse the block** — read the concepts, per-concept moves, sites, register-fit lines, saturation note, and any "QUESTIONS FOR YOU". Answer or surface the questions before continuing.
2. **Validate the disk writes** (Primary / Fallback A):
   - Does `brain/research/concepts.md` exist and parse against the `references/round-formats.md` shape?
   - Are screenshots present in `brain/moodboard/`?
   - If either is missing but the paste block is intact, treat this as effectively Fallback C for this round.
3. **Fallback C reconstruction** — if Aside had no FS access, **write `brain/research/concepts.md` from the block** (the block is self-sufficient by contract). Screenshots may be absent; note that in the file's header line.

Do not checkpoint until `concepts.md` is on disk (written by Aside or reconstructed by calibrate).

---

## Step 4 — Checkpoint with the user (pick / blend)

Present the found concepts as a **conversation, not a menu dump**. Walk the user through what the field actually contains — each concept's feeling, its signature moves, and its honest register fit for this project. Then let the user:

- **Pick ONE** concept, or
- **BLEND** at the component level ("the hero of A with the type of B" — express the blend as explicit per-axis picks), or
- **Ask for more sweep** — if the map feels thin, send a follow-up back to the same Aside chat before deciding.

**Write the decision to canon** so every downstream skill sees it:
- `brain/BRAND.md` → a **Decisions-log line** (author-stamped) recording the chosen concept or blend.
- `brain/BRAND.md` → a **Locked-direction seed** capturing the concept/blend as the seed Phase 5 builds from.

**Rule 7 survives.** The chosen concept seeds Phase 5's three directions, but ≥1 later direction must still DEPART from *everything* the sweep found — the anti-old-style-trap hatch. Concepts describe the field; they never cap ambition. Note this explicitly when writing the seed so Phase 5 honors it.

---

## Step 5 — Generate the Round-2 directive (DEEP TEARDOWN)

Fill the **Round-2 variant** of `references/mission-prompt-template.md` with the chosen concept (or the explicit component-level blend). The directive names the concept, instructs Aside to go deep on its best real examples (saturation-driven, no target count), carries the full teardown checklist, gives the `brain/research/teardowns/` and `brain/moodboard/` disk paths, and closes with "print the ROUND-2 SUMMARY BLOCK" — all per the template and `references/round-formats.md`.

**Present the filled directive in a fenced block.** Tell the user to paste it into the **SAME Aside chat** as Round 1 (Aside keeps the sweep context). Then **STOP** — wait for the **ROUND-2 SUMMARY BLOCK** to be pasted back. Do not proceed until it arrives.

---

## Step 6 — Ingest Round 2 + fold into canon

When the user pastes the ROUND-2 SUMMARY BLOCK back:

1. **Validate the teardowns.** Confirm `brain/research/teardowns/<slug>.md` exists for each torn-down site and parses against the `references/round-formats.md` teardown shape. On Fallback C, write the teardown files from the block. Confirm screenshots landed in `brain/moodboard/` (or note their absence).

2. **Populate `brain/moodboard/notes.md`** (existing v4.0.0 per-entry format) from the chosen concept's torn-down sites. Every entry carries a written **"why it works"** that now cites teardown evidence — no unlabeled tiles:

   ```
   ### <Site name> — <tier: ceiling | skeleton | parts | type-color | mood>
   URL: <full url>
   Captured: <slug>-hero.png · <slug>-mid.png · <slug>-end.png
   Why it works: <one or two sentences naming the register/archetype axis it satisfies,
     citing the teardown — e.g. "real Söhne + a single warm accent from :root hits the
     high-trust + Ruler register; the type does the emotional work, not color.">
   ```

3. **Write the conventions audit to `brain/DESIGN.md`** — now evidence-backed by the teardowns (existing block shape; do not touch the universal anti-patterns above it):

   ```
   ## Conventions audit (from calibrate)

   FOLLOW — genre expectations we keep
   - <convention> — <why keeping it protects trust/legibility> (evidence: <N of M sites>)

   DEVIATE — conscious signature moves
   - <move> — <why the audience tolerates this break>

   REFUSE — patterns that violate the register
   - <pattern> — <which register axis it violates>
   ```

   FOLLOW claims are now grounded in counts from the teardowns ("9 of 12 hotels use a full-bleed video hero"), not guesses. REFUSE merges with the brand-specific refusal list; enforced downstream by `design-check` and `audit` exactly like the universal anti-patterns.

**Show the audit (and the notes.md entries) to the user before writing. One confirmation pass, then write.**

**Law:** extracted values (real fonts, real hexes, real motion stack) are **EVIDENCE FOR** our tokens — never copied **AS** tokens. `design-check` enforces this downstream.

→ Reasoning-tier `Task` sub-agent drafts the conventions audit and the "why it works" lines — the highest-judgment step in the pass.

---

## Step 7 — Handoff back to design-direction Phase 5

Both rounds are done. Phase 5 is now grounded in a swept field map, a chosen concept, forensic teardowns, an annotated board, and an evidence-backed conventions audit. Hand back explicitly:

```
Skill("design-direction")
```

Tell `design-direction` to resume at **Phase 5 (three named directions)**, now reading `brain/research/concepts.md`, `brain/research/teardowns/`, `brain/moodboard/notes.md`, and the conventions-audit block in `brain/DESIGN.md`. Each proposed direction must point at a real teardown and respect the FOLLOW / DEVIATE / REFUSE buckets — and, per Rule 7, ≥1 direction must depart from every concept the sweep found.

**No keyword auto-chain.** This handoff is an explicit `Skill()` call, per the plugin's architecture — nothing here fires on a trigger word.

---

## Hard rules

- **No hardcoded numbers — the governing law.** Nowhere in the prompts calibrate generates may a fixed count appear as a target: not "20–40 sites", not "5–8 teardowns", not "3 concepts". Every quantity is **saturation-driven** — a site earns its place only by adding a concept, a better example of one, or a convention data point. The depth dial tunes appetite, not counts. Duration is never our concern; state this in the prompts.
- **Two rounds, human-relayed. Aside sweeps → user picks/blends → Aside tears down.** Calibrate never chooses the concept for the user, and never does the browsing thinking itself except under Fallback A.
- **Reference the sibling files; never duplicate them.** Formats live in `references/round-formats.md`; the prompts in `references/mission-prompt-template.md`; Aside's brain in `aside-skill/design-research/SKILL.md`.
- **The paste blocks are the guaranteed channel.** Files on disk are an optimization; if disk is unreachable, reconstruct all canon from the self-sufficient blocks (Fallback C).
- **Fallback A runbook is verbatim** — daemon on `127.0.0.1:21420`, launch-and-wait, never fullPage, never `page.evaluate()` scroll, one action per REPL call, `./artifacts/` → `cp`, re-attach on disconnect.
- **Extracted values are evidence, never tokens to copy.** `design-check` enforces this.
- **Rule 7 survives the sweep.** ≥1 Phase-5 direction departs from every concept found — concepts describe the field, never cap ambition.
- **Only the conventions-audit block is written to `DESIGN.md`.** The universal anti-patterns above it are sacred; never edited here.
- **Show the audit + notes before writing.** One confirmation pass.
- **This skill does not pick a direction or write tokens.** It hands back to `design-direction` Phase 5.
- **Every handoff is an explicit `Skill()` call.** No auto-chains.

---

## Sub-agent routing

| Step | Tier | Why |
|------|------|-----|
| Step 2 fill Round-1 mission prompt from a long `BRAND.md` | fast | Pure extraction into the template |
| Step 3 parse + validate the Round-1 paste | fast | Mechanical parse against the fixed format |
| Step 4 checkpoint framing (present concepts as a conversation) | reasoning | Judgment tying each concept to the project's register |
| Step 5 fill Round-2 directive with chosen concept/blend | fast | Template fill from the recorded decision |
| Step 6 notes.md "why it works" + FOLLOW/DEVIATE/REFUSE audit | reasoning | Highest-judgment step — evidence-to-convention synthesis |
| Fallback A Aside capture orchestration | fast | Mechanical, runbook-driven |

Never use the most expensive model. Reasoning tier (Sonnet) is the ceiling.

---

## Difference from related skills

- **`design-direction`** — the parent. Owns Phases 1–7, picks the direction, writes tokens. `calibrate` is its Phase 4→5 bridge; it runs the research engine, hands back, and never picks a direction.
- **`build-component` / adopt-external** — normalizes a *specific* pasted component against existing tokens. `calibrate` works one layer up, on taste inputs, before any component or token exists.
- **`design-check`** — the write-time gate that later enforces the REFUSE bucket and the evidence-not-tokens law this skill establishes.
- **`discussion-mode`** — pure talk, no writes. Use it to argue about references first, then `calibrate` to research and lock them.

---

## Output shape (end of skill)

```
calibrate — summary (two rounds)

Mission: <archetype + register one-liner> · niche <niche> · depth <dial>
Transport: <manual relay | Fallback A repl | Fallback C paste>

Round 1 — SWEEP: <N> sites examined → <count> concepts
  Chosen: <concept letter/name  or  BLEND: A.hero + B.type + ...>
Round 2 — TEARDOWN: <k> sites autopsied for the chosen concept

Wrote:
  ✅ brain/research/concepts.md — field map (<count> concepts)
  ✅ brain/research/teardowns/ — <k> forensic teardowns
  ✅ brain/moodboard/ — <k>×3 viewport screenshots
  ✅ brain/moodboard/notes.md — every tile annotated, citing teardown evidence
  ✅ brain/BRAND.md — concept decision (Decisions log + Locked-direction seed)
  ✅ brain/DESIGN.md — conventions audit: FOLLOW <a> · DEVIATE <b> · REFUSE <c> (evidence-backed)

Next step: Skill("design-direction") → resume Phase 5 (three named directions),
now grounded in the swept field, the chosen concept, the teardowns, and the conventions audit.
Rule 7 stands: ≥1 direction must depart from every concept found.
```
