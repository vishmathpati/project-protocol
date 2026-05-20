---
name: design-direction
description: Deep brand-direction diagnostic for a project. Takes a raw brand dump, silently extracts taste axes (trust, frequency, density, culture, archetype, tribe, surface, tempo, refusals), proposes 3 directions with a moodboard, and writes a richer BRAND.md + DESIGN.md Overview + brand-specific refusal list. Triggers — "design direction", "design diagnostic", "set up the design system", "re-anchor brand", "I don't know which design to pick".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Task
---

# Design Direction

The diagnostic engine that turns "I don't know what this should look like" into a locked design direction. Sits one layer upstream of `init-project`'s Phase 4 file-writing — the same files (`agents/BRAND.md`, `agents/DESIGN.md`) are populated, but from a much richer brief than the default 3-question flow can produce.

The skill exists because the default Phase 4 brand-question flow produces a thin BRAND.md (what / personality / not-this) and from that thin BRAND.md the DESIGN.md generator has to invent palettes / type pairings / DO-NOTs out of training-data averages. That's where "the AI design feels generic" comes from. This skill replaces that thin brief with a deep one.

---

## When this fires

- User asks: "design direction", "design diagnostic", "what should this look like", "set up the design system", "re-anchor the brand", "I don't know which design to pick".
- User wants to start a new project's design system from scratch with depth.
- User has an existing initiated project but feels `agents/BRAND.md` or `agents/DESIGN.md` is too thin / generic, and wants to re-anchor.
- Invoked as a sub-step from `init-project` Phase 4 (the user accepted the deep-flow handoff).
- Slash command: `/design-direction`.

Skip conditions: user says "skip", "keep the simple flow", "don't bother".

---

## What it produces

Three concrete outputs, written to the project's `agents/` tier:

1. **`agents/BRAND.md`** — populated richly. Sections: Product, Audience, Problem, Surfaces, Archetype, Reference tribe (look-like + look-unlike), Brand-specific refusal list, Locked direction (which of the 3 directions was chosen + why).
2. **`agents/DESIGN.md` Overview section** — the `[VERIFY — fill from BRAND.md or user direction]` placeholder is replaced with a one-paragraph identity statement that names tone, era, and references. Token frontmatter and the rest of the template are *not* touched by this skill — that's still Phase 4's job. This skill just makes Phase 4's input good.
3. **`agents/DESIGN.md` DO NOT section — brand-specific additions** — the `[Add brand-specific anti-patterns here]` placeholder is replaced with concrete anti-patterns derived from the chosen direction and the user-confirmed refusal list. Universal anti-patterns (no indigo, no two-stop gradients, etc.) stay intact above the brand-specific block.

Nothing else is touched. `FUNDAMENTALS.md` is global — never modified per project.

---

## Compatibility — existing projects

This skill must work on projects that already ran `init-project`. Strict rules:

- **Never silently overwrite** an existing populated section. If `agents/BRAND.md` has real content (not just `[VERIFY]` placeholders), show it to the user before any write and ask whether to replace, merge, or append.
- **Preserve user content.** If the user wrote prose into `BRAND.md` between the placeholder markers, treat that prose as canon. Move it into the right section of the new richer template, do not delete it.
- **DESIGN.md DO NOT section** — only the bottom `[Add brand-specific anti-patterns here]` block is touched. The universal anti-patterns above (indigo, gradients, emoji-icons, etc.) are never edited. If the user has already added brand-specific items there, ask before replacing — default is to merge.
- **Token frontmatter is read-only here.** This skill never edits colors / typography / spacing / radius. Those decisions belong to Phase 4's DESIGN.md flow, which runs after this skill confirms the direction. If the user wants tokens regenerated against the new direction, this skill ends with a handoff prompt: "Direction locked. Want me to regenerate `agents/DESIGN.md` tokens against this direction?" → if yes, hand off to `init-project` Phase 4 path C (fresh generation), now with a far richer brief.

---

## The 7 phases

Walk these in order. Each phase has a reference doc in `references/` for the detail.

### Phase 1 — Brand dump (one prompt, free text)

Ask the user one question, in plain language, and accept a free-form answer:

> Tell me about this product in your own words. What is it, who's it for, what problem does it solve, where does it live (web / app / both), how does it make money, what surfaces will it have (marketing, dashboard, email, docs, mobile), and anything you already know it should NOT look like. As much or as little as you have — I'll work with what you give me.

No structured form. No multiple-choice. The dump is the input.

If the user has run `init-project` already, also read `agents/BRAND.md` and `agents/STATUS.md` first — they may answer most of the dump questions silently. Only ask for what's missing.

→ See `references/phase-1-brand-dump.md` for the exact prompt + how to merge existing canon.

### Phase 2 — Silent axis extraction

The agent (not the user) extracts the 9 taste axes from the dump:

1. **Trust temperature** — Max / High / Medium / Low. Derived from cost-of-failure to the user (money, health, time, embarrassment).
2. **Use frequency** — Daily-hours / Daily-seconds / Weekly / Occasional / One-time. Derived from product nature.
3. **Information density** — Data-dense / Content-light / Mixed. Derived from primary surfaces.
4. **Cultural anchor** — Global-tech / Indian-formal / Indian-casual / Japanese-minimal / Western-consumer / etc. Derived from audience and language hints.
5. **Brand archetype** — One of Sage / Magician / Caregiver / Rebel / Creator / Hero / Explorer / Innocent / Lover / Jester / Ruler / Everyman. Derived from problem + tone.
6. **Reference tribe** — 3 sites the audience already trusts (look-like) + 1 incumbent to deliberately look unlike. Derived from category.
7. **Surface mix** — Single-surface / Marketing+app / Multi-surface. Derived from what the user listed.
8. **Tempo** — Motion-led / Static / Mixed. Derived from product nature (fashion → motion; finance → static).
9. **Refusal list** — 3–5 things this brand never does. Mix of user-stated "shouldn't look like" + agent-inferred from archetype and tribe.

Do not surface the axis names to the user. They will see the synthesised diagnostic in Phase 3, not the labels.

→ See `references/phase-2-axis-extraction.md` for the heuristic per axis.

### Phase 3 — Plain-English diagnostic + one confirmation pass

Return a short plain-English summary, NOT a list of axis labels. Sample shape:

```
Reading the product:

This serves <audience descriptor>. They are <emotional state about the problem>.
The product is opened <frequency phrasing> and the content is <density phrasing>.
It belongs to the <cultural anchor> vocabulary.

The brand sits closest to the <archetype> archetype — <one-sentence archetype meaning>.

It should feel like a sibling to <look-like site 1, 2, 3> and deliberately not look like <look-unlike>.

It probably should never: <refusal 1>, <refusal 2>, <refusal 3>.

Does this read true? Anything off — say so in plain language and I'll adjust.
```

The user replies with corrections in plain English ("no, trust is higher than that — these are anxious users", "not Indian-casual, this is global"). The agent updates the locked axes. One pass — do not loop on this step. After the correction, lock and proceed.

→ See `references/phase-3-diagnostic-summary.md` for the prose template + correction-merging rules.

### Phase 4 — Reference moodboard

Propose 3–5 real sites that satisfy the locked axes. For each: name, URL, one-sentence why-it-fits.

Use `WebSearch` if the host supports it; otherwise list from knowledge. If you cannot reach the live sites for screenshots, list them with their URLs and one-line descriptions — the user can open them themselves.

→ See `references/phase-4-moodboard.md` for the heuristic mapping (which axis-combinations point at which reference sites).

### Phase 5 — Three named directions

Propose exactly 3 directions. Each must be **meaningfully different** — they sit at different points on the design space. Not 3 flavours of minimalist black.

Each direction has:

- **Name** — a short evocative label (e.g., "Editorial cream", "Color lab", "Warm modern Indian").
- **Palette intent** — described in words, not hex codes. ("Cream and ink with one terracotta accent." Not `#F5EFE4 + #1A1A1A + #C2410C`.)
- **Type pairing** — one display family + one body family, both named. ("Editorial serif display + clean sans body, like Stripe Press's pairing.")
- **One personality sentence** — what the product feels like in this direction.
- **A reference URL** — model the layout after this.
- **Why this fits the diagnostic** — one or two sentences connecting the direction back to the locked axes.

The 3 must span the viable space. If two of them feel like the same direction in different shades, replace one.

→ See `references/phase-5-three-directions.md` for the variation rules.

### Phase 6 — Pick (or hybrid)

User picks one. Hybrid is allowed ("direction A's palette with direction B's typography") and the agent merges. If the user is genuinely torn, the agent picks based on the diagnostic and explains why — no infinite indecision loop. The user can override.

Lock the chosen direction.

### Phase 7 — Write outputs

Write `agents/BRAND.md` and the two `agents/DESIGN.md` sections (Overview, brand-specific DO NOT block) per the rules in **What it produces** + **Compatibility** above.

After writing, surface:

```
✅ Direction locked: <name>
✅ Wrote: agents/BRAND.md (full), agents/DESIGN.md Overview + brand-specific DO NOT additions.

Token frontmatter (colors, typography, spacing, radius) was NOT regenerated.
Want me to regenerate it now against the locked direction? — runs init-project Phase 4 path C with the new brief.
```

If user says yes → hand off to the existing Phase 4 flow. If no → done.

→ See `references/phase-7-write-outputs.md` for the exact write rules + diff format.

---

## Sub-agent routing

Heavy reasoning steps go to Task tool sub-agents to keep the orchestration context lean:

| Step | Tier | Why |
|------|------|-----|
| Phase 2 axis extraction from a long brand dump | reasoning | Judgment on archetype / tribe / refusals |
| Phase 4 moodboard candidate selection | reasoning | Knowledge of design-conscious sites |
| Phase 5 generating 3 *meaningfully different* directions | reasoning | Highest-judgment step — must not produce 3 flavours of the same thing |
| Phase 7 writing the BRAND.md / DESIGN.md edits | reasoning | Preserves user content while restructuring |
| Reading existing `agents/BRAND.md` / `agents/STATUS.md` for context | fast | Pure extraction |

Never use the most expensive model. Reasoning tier (Sonnet) is the ceiling.

---

## Hard rules

- **One free-text prompt to the user, not nine questions.** The 9-axis extraction is the agent's job, not the user's.
- **One confirmation pass at Phase 3.** Don't loop. After correction, lock and proceed.
- **3 directions, not 5.** Five overwhelms; one is too tight; three forces meaningful difference.
- **Never overwrite existing user-written content.** Read first, ask, merge.
- **Token frontmatter is read-only in this skill.** This skill ends at the direction lock + Overview + DO NOT block. Token regeneration is a separate handoff to Phase 4.
- **No hex codes in direction proposals.** Direction names + palette intent in words. Hex codes are the next step (Phase 4 path C), not this one.
- **Refusal list lives in DESIGN.md's brand-specific block,** not in a new file. Same enforcement chain as the universal anti-patterns — `design-check` and `audit` will scan against the merged list automatically.

---

## Difference from related skills

- **`init-project`** — bootstraps the whole project layout (3 folders + all canon files). Phase 4 inside it creates BRAND.md / DESIGN.md / FUNDAMENTALS.md with the lightweight flow. `design-direction` is a *deeper* alternative for Phase 4, or a re-anchor for projects already initiated.
- **`design-check`** — UI write-time gate. Reads the DESIGN.md that this skill helped populate. They don't overlap; they chain.
- **`discussion-mode`** — pure conversation, no writes. `design-direction` writes files. If you want to talk through direction without committing, use `discussion-mode` first, then `design-direction` to lock.
- **`audit`** — periodic consistency scan. Will catch any drift between BRAND.md / DESIGN.md after this skill runs.

---

## Output shape (end of skill)

```
design-direction — summary

Brand dump: <one-line of what user provided>
Locked diagnostic: <one sentence — archetype + tribe + emotional temperature>
Chosen direction: <name> — <one-line description>

Wrote:
  ✅ agents/BRAND.md (full)
  ✅ agents/DESIGN.md — Overview filled
  ✅ agents/DESIGN.md — brand-specific DO NOT additions: <N items>

Next step:
  ? Regenerate token frontmatter against the locked direction (hands off to init-project Phase 4 path C)
  ? Or proceed to first UI work, which will fire design-check using the new brief
```
