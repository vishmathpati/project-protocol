---
name: design-check
description: Pre-action gate for any UI work. Reads DESIGN.md + FUNDAMENTALS.md, searches existing components for reuse, identifies tokens needed, halts on missing tokens, scans diff for raw hex/px/font values. Fires on — "create component", "edit UI", "change styles", "add page", any visual change.
allowed-tools: Read, Glob, Grep
---

# Design Check

The 7-step gate fired before any UI work. The skill does not write code — it forces a sequence the agent walks through before and during the change.

---

## When this fires

- Creating or editing a component (`.tsx`, `.jsx`, `.vue`, `.svelte`, `.swift` with `View`).
- Editing CSS / Tailwind / styles files.
- Adding a new page or route with visible UI.
- Adjusting layout, spacing, colors, typography anywhere.
- Slash command: `/design-check`.

If the file does not produce visible UI (config, types, pure utility logic), this skill is a no-op.

---

## The 7 steps

**1. Read the canon.**
- `agents/DESIGN.md` — the brand tokens.
- `agents/FUNDAMENTALS.md` — universal craft rules (token rule, 7 cardinal sins, 5 required states, banned words, icon discipline, pre-ship checklist).

If either file is missing → STOP. Run `init-project` first.

**2. Search existing components — reuse over create.**
- Glob `components/ui/*`, `components/primitives/*`, `components/blocks/*` (web) or `Views/*.swift` (Swift).
- For the surface being built, list every component that solves the same or a similar problem.
- If a usable component exists: extend or compose it. Do not create a duplicate.
- Surface to the user: "I'll reuse `<Button>` and `<Card>`. Need to extend `<Card>` with a `compact` variant. Confirm?"

**3. Identify tokens needed.**
- List every visual value the task requires: colors, spacing, radius, font sizes, weights, shadows.
- For each, name the token from `DESIGN.md` that supplies it.

**4. Halt on missing tokens.**
- If any required value is not in `DESIGN.md`:
  - **STOP.** Do not improvise. Do not write a raw hex / px.
  - Propose the addition: name the new token, point at related existing tokens it derives from, explain why it's needed.
  - Wait for explicit user confirmation ("go", "do it", "approved").
  - Once confirmed: add the token to `DESIGN.md` AND `global.css` (or `DesignTokens.swift`).
- Only proceed once every needed token exists.

**5. Write code using approved tokens only.**
- Every color, every spacing value, every font reference uses a token (`var(--token)` on web; `Color.tokenName` on Swift).
- Never write raw hex, raw px, raw font-family strings in component files.
- Apply the 7 cardinal sins check from `FUNDAMENTALS.md` while writing — never emit indigo, two-stop gradients, emoji icons, etc.

**6. Scan the diff.**
- After writing, grep the diff for:
  - Raw hex: `#[0-9a-fA-F]{3,8}` outside `:root` / token definition files.
  - Raw px in component files (not utility classes).
  - Raw `font-family` strings.
  - `outline: none` without an accompanying `:focus-visible` replacement.
  - `<div onClick>` or `<span onClick>`.
  - `<img>` without `alt`, `width`, or `height`.
- Each hit is a violation.

**7. Halt on violations.**
- If step 6 found anything: **STOP.**
- Show the user each violation with file + line.
- Fix or escalate. Do not declare done.
- After fixes, re-run step 6 until clean.

---

## Output shape

At step 2 (component reuse):

```
design-check — existing components to reuse:
- <Button variant="primary"> for the CTA
- <Card> with new "compact" variant (extension needed)
- <Input type="email"> as is

Proceed?
```

At step 4 (missing token):

```
design-check — missing token:
- Task needs a warning-tinted surface background.
- DESIGN.md has --bg, --surface, --surface-2, --warning — but no warning-tinted surface.
- Proposing: --surface-warning, derived from --warning at ~10% opacity.

Add to DESIGN.md + global.css?
```

At step 7 (violation):

```
design-check — raw values in diff:
- src/components/Pricing.tsx:42 — raw hex #1a1a1a → should be var(--surface)
- src/components/Pricing.tsx:67 — raw padding 17px → use 16 (--space-4) or 20 (--space-5)
- src/components/Hero.tsx:28 — <div onClick> → use <button>

Fix before continuing.
```

---

## Skip conditions

The user can override with explicit phrases like "skip design-check, just do it" or "no gate, proceed". Default is the full 7 steps.

---

## Why it exists

`DESIGN.md` and `FUNDAMENTALS.md` already encode what the project commits to visually. Agents drift when they aren't forced to consult those files. This skill makes the consultation mechanical — the agent walks the same 7 steps every time, can't skip, can't improvise tokens, can't ship raw values silently.

The Extension protocol in `DESIGN.md` is enforced here at step 4. The pre-ship checklist in `FUNDAMENTALS.md` is enforced here at steps 6–7 and again by `audit-before-close`.

---

## Difference from `discipline` and `audit-before-close`

- `discipline` — universal pre-action gate for any non-trivial change.
- `audit-before-close` — universal end-of-work gate.
- `design-check` — UI-specific gate. Runs at both moments (pre-write at steps 1–4, post-write at steps 6–7). More concrete because the rules are pixel-level.

All three can fire on the same task. `design-check` is the UI-specific layer.
