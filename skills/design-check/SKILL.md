---
name: design-check
description: Pre-action gate for any UI work. Reads DESIGN.md + FUNDAMENTALS.md, searches existing components for reuse, identifies tokens needed, halts on missing tokens, scans diff for raw hex/px/font values. Fires on — "edit UI", "change styles", "add page", any visual change; also auto-chains after build-component finishes writing a new component.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Design Check

The 8-step gate fired before any UI work. The skill walks the agent through a sequence before, during, and after the change. Steps 1–7 are detection. Step 8 offers auto-fixes for mechanical violations and surfaces human-judgment ones.

---

## When this fires

- Editing a component (`.tsx`, `.jsx`, `.vue`, `.svelte`, `.swift` with `View`).
- Editing CSS / Tailwind / styles files.
- Adding a new page or route with visible UI.
- Adjusting layout, spacing, colors, typography anywhere.
- Auto-chains after `build-component` finishes writing a new component (that skill owns the create path; this skill owns the post-write audit).
- Slash command: `/design-check`.

If the file does not produce visible UI (config, types, pure utility logic), this skill is a no-op.

---

## The 8 steps

**1. Read the canon.**
- `agents/DESIGN.md` — the brand tokens.
- `agents/FUNDAMENTALS.md` — universal craft rules (token rule, 7 cardinal sins, 5 required states, banned words, icon discipline, pre-ship checklist).

If either file is missing → STOP. Run `init-project` first.

**2. Search existing components — reuse over create.**
- First, read `agents/STRUCTURE.md` to get the actual component paths for this project:
  - Read the `## Component locations` table — use the paths listed there for each tier (Generic, Marketing, App, Desktop).
  - Read the `## Project layout` section — if `**Monorepo:** true`, read the `**App paths:**` list and scan each app's component paths separately.
  - Fall back to default globs only if `agents/STRUCTURE.md` is missing: `components/ui/*`, `components/primitives/*`, `components/blocks/*` (web) or `Views/*.swift` (Swift).
- Glob each detected component path for the surface being built; list every component that solves the same or a similar problem.
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
  - Once confirmed: add the token to `DESIGN.md` AND the project's CSS token file. To find the correct token file, check `agents/STRUCTURE.md` `## Conventions detected` section for `Token chain:` — the file after the `→` arrow (e.g. `globals.css`, `global.css`, `tokens.css`) is where CSS vars live. For Swift projects, the token file is `DesignTokens.swift`. For monorepos, each app may have its own token file — write to the app path that matches the surface being edited.
- Only proceed once every needed token exists.

**5. Write code using approved tokens only.**
- Every color, every spacing value, every font reference uses a token (`var(--token)` on web; `Color.tokenName` on Swift).
- Never write raw hex, raw px, raw font-family strings in component files.
- Apply the 7 cardinal sins check from `FUNDAMENTALS.md` while writing — never emit indigo, two-stop gradients, emoji icons, etc.

**6. Scan the diff.**
- Scope the scan to the component paths recorded in `agents/STRUCTURE.md` (same paths used in Step 2). If STRUCTURE.md is missing, fall back to scanning from the project root. For monorepos, scan each app's component paths separately — do not scan the workspace root.
- Exclude from the scan: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.turbo/`, `coverage/`.
- After writing, grep the scoped paths for:
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

**8. Offer fixes.**

After step 7 surfaces violations, do not just halt and hand back. Sort every finding into one of two buckets and present them as a structured report.

**Auto-fixable** (mechanical, low-risk, the agent can apply directly):
- Raw hex that matches an exact known token value in `agents/DESIGN.md` frontmatter → replace with the corresponding Tailwind class (e.g. `bg-[#0a0a0a]` → `bg-background` if `--bg: #0a0a0a` is defined).
- Raw `...` (three periods) in user-facing strings → replace with `…` (U+2026).
- `10MB` / `10 GB` style unit pairs → replace with `10&nbsp;MB`.
- `<div onClick>` for what should be a button → swap to `<button type="button">`.
- `<img>` missing `width` / `height` and the image file exists locally → read its dimensions, set them on the tag.
- `<img>` decorative-only with no `alt` → add `alt=""` plus `aria-hidden="true"`.
- `outline: none` without a `:focus-visible` replacement → add `outline-none focus-visible:ring-2 focus-visible:ring-ring` (or the project equivalent).
- `transition: all` → ask the user which properties were intended; only auto-fix if it's obviously safe (rare).

**Human-judgment** (never auto-fix — surface only, ask the user):
- Raw hex with NO matching token in `DESIGN.md` → "which token should this map to?"
- Cardinal sin #1: indigo accent → "which color should replace it?"
- Cardinal sin #3: emoji-as-icon → "which Lucide icon?"
- Cardinal sin #6: invented metric → "real source or remove?"
- Cardinal sin #7: filler / lorem ipsum copy → user rewrites.
- Banned words from `FUNDAMENTALS.md` (hype / filler / corporate zombie / AI-slop openers) in shipped copy → user rewrites.
- Cardinal sin #2: two-stop trust gradient on hero → user decides (could be intentional brand choice).
- Cardinal sin #5: AI-dashboard-tile shape (rounded card + colored left-border accent) → user decides.
- `<img>` missing `alt` AND clearly meaningful (used in a hero, has descriptive surrounding text) → user must write alt text.

**Safety rule.** Never auto-fix a finding when the proposed fix can't be verified. Before applying any raw-hex → token replacement, confirm the matching token is actually defined in the `DESIGN.md` frontmatter. If it isn't, that finding moves to human-judgment with the prompt "this raw hex has no matching token — what should this map to?" — not a silent guess.

**Batching for large diffs.** If there are more than 20 findings, group them by file. Show the top 10 first by severity (cardinal sins > raw values > craft details), with a `show N more` affordance. Apply auto-fixes in batches of one-confirmation-per-file, not one-confirmation-per-finding.

**Interaction shape.** Output a single report and ask for one decision per bucket:

```
design-check — found 7 violations

Auto-fixable (4 findings):
  • src/Pricing.tsx:42  bg-[#0a0a0a] → bg-background
  • src/Hero.tsx:28     <div onClick> → <button type="button">
  • src/Hero.tsx:51     <img> missing dimensions (will read from /public/hero.jpg)
  • src/Footer.tsx:67   "..." → "…"

Apply all auto-fixes?
  [yes — apply all]
  [pick — choose which to apply]
  [no — leave for me to fix manually]

Human-judgment (3 findings — surfacing for your input):
  • src/Hero.tsx:18  raw hex #6366f1 (indigo accent — cardinal sin #1)
      → which token should this map to? (--primary / new token / different fix)
  • src/Hero.tsx:34  emoji 🚀 inside <button> (cardinal sin #3)
      → which Lucide icon? (rocket / send / play / other)
  • src/Footer.tsx:12  "supercharge your marketing" (banned word)
      → rewrite (suggest: "see real campaign performance")
```

**After applying fixes.** Re-run step 6 (diff scan) to confirm every auto-fix target is now clean. If any auto-fix introduced a new violation, surface it and stop — do not loop silently.

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

At step 8 (offer fixes):

```
design-check — found 5 violations

Auto-fixable (3 findings):
  • src/Pricing.tsx:42  bg-[#1a1a1a] → bg-surface  (matches --surface in DESIGN.md)
  • src/Hero.tsx:28     <div onClick> → <button type="button">
  • src/Footer.tsx:67   "Loading..." → "Loading…"

Apply all auto-fixes?
  [yes — apply all]
  [pick — choose which to apply]
  [no — leave for me to fix manually]

Human-judgment (2 findings — surfacing for your input):
  • src/Hero.tsx:18  raw hex #6366f1 (indigo accent — cardinal sin #1)
      → which token should this map to? (--primary / new token / different fix)
  • src/Pricing.tsx:67  raw padding 17px (no matching --space token)
      → 16 (--space-4) or 20 (--space-5)?
```

After auto-fixes apply, step 6 re-runs:

```
design-check — re-scan after auto-fix:
- 3 of 3 auto-fix targets now clean.
- 2 human-judgment findings still open — awaiting your input.
```

---

## Skip conditions

The user can override with explicit phrases like "skip design-check, just do it" or "no gate, proceed". Default is the full 8 steps.

---

## Why it exists

`DESIGN.md` and `FUNDAMENTALS.md` already encode what the project commits to visually. Agents drift when they aren't forced to consult those files. This skill makes the consultation mechanical — the agent walks the same 8 steps every time, can't skip, can't improvise tokens, can't ship raw values silently.

The Extension protocol in `DESIGN.md` is enforced here at step 4. The pre-ship checklist in `FUNDAMENTALS.md` is enforced here at steps 6–7 and again by `audit-before-close`.

---

## Difference from `discipline` and `audit-before-close`

- `discipline` — universal pre-action gate for any non-trivial change.
- `audit-before-close` — universal end-of-work gate.
- `design-check` — UI-specific gate. Runs at both moments (pre-write at steps 1–4, post-write at steps 6–7). More concrete because the rules are pixel-level.
- `design-check` now also offers auto-fixes (via Step 8). `audit-before-close` and `audit` remain detection-only and do not modify files.

All three can fire on the same task. `design-check` is the UI-specific layer.
