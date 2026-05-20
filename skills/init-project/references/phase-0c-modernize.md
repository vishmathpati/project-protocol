# Phase 0c — Modernize an already-initiated project

Runs only when Phase 0 classifies the project as **modernize** (Mode A) — either the user invoked init-project with explicit upgrade intent, or audit mode detected significant drift and the user opted in. The goal is to upgrade an existing project to the latest plugin version, re-confirm canon with the user, sweep the codebase for design-system drift, and clean up waste.

This phase is **interactive**. It does not silently rewrite canon. Each populated file gets a "confirm or edit" pass. The only silent rewrites are the locked global standards (FUNDAMENTALS.md, TOOLING.md) — same rule as every other init mode.

---

## Non-negotiable principles

1. **Re-confirm, don't overwrite.** Every populated canon file is summarized back to the user in plain English; the user picks keep / edit / rebuild. No silent rewrites.
2. **Archive, never delete.** Waste files move to a timestamped `archive/<YYYY-MM-DD>-modernize/` folder. The user opts out per file.
3. **Surface human-judgment work, auto-fix only the safe stuff.** Design-system drift sweep separates mechanical fixes from items needing judgment.
4. **Global standards stay locked.** FUNDAMENTALS.md and TOOLING.md are copied from the plugin templates silently. DESIGN.md tokens are preserved — only the structural envelope is checked.
5. **No partial state on cancel.** If the user cancels mid-phase, every change made up to that point is reversible (archive moves can be undone; canon rewrites are gated behind explicit confirmation).

---

## 0c.1 — Audit current state

Read-only sweep. Produce a state report; do not modify anything yet.

Check and record:

- **Three-folder protocol present?** — confirmed by Mode A condition. Note the structure.
- **STRUCTURE.md present at `agents/STRUCTURE.md`?** If missing, schedule first-run detection in sub-phase 5.
- **For each canon file** in `{cowork/STATUS.md, cowork/BRIEF.md, agents/STATUS.md, agents/BRIEF.md, agents/ROADMAP.md, agents/BRAND.md, agents/DESIGN.md, agents/DISCOVERIES.md, README.md, CLAUDE.md}`:
  - Exists? Populated with real content (>50% non-placeholder — heuristic: ratio of non-`[VERIFY]` non-stub lines)?
  - Stale? Last modified >30 days ago (`stat` or `git log -1 --format=%ct <file>` — but `git` is out of bounds here; use filesystem mtime).
- **Plugin version markers:** parse the project's README, root CLAUDE.md, and any `agents/CHANGELOG.md` for plugin-version mentions. Note current version.
- **Waste candidates:**
  - WORKLOG backups: `cowork/WORKLOG.md.bak*`, `agents/WORKLOG.md.bak*`, any `WORKLOG-YYYY-MM-DD.md` older than 7 days that has already been rolled into CHANGELOG.
  - Files in `archive/`, `_archived/`, `legacy/`, `_old/`, `.deprecated/` folders.
  - Stale docs in `agents/docs/detail/` — last modified >90 days AND not referenced by `agents/docs/INDEX.md`.
  - Abandoned design files: `DESIGN.md.bak`, `BRAND-old.md`, screenshot dumps in `agents/` root (PNGs, JPGs).

Output a state report to the user:

```
Modernize state report

  Plugin version detected:   <version or "unknown">
  Three-folder protocol:     present
  STRUCTURE.md:              <present | missing>

  Canon files:
    cowork/STATUS.md         populated, last touched <N> days ago
    cowork/BRIEF.md          thin (mostly placeholder), last touched <N> days ago
    agents/BRIEF.md          populated, last touched <N> days ago
    agents/BRAND.md          populated, last touched <N> days ago
    agents/DESIGN.md         populated, last touched <N> days ago
    agents/ROADMAP.md        stale (>30d), populated
    agents/STATUS.md         populated, last touched <N> days ago
    ...

  Waste candidates:           <K> files (will list before archiving)
  Codebase design-drift scan: pending

Press any key to continue, or "cancel" to stop.
```

---

## 0c.2 — Per-canon-file confirmation loop

For each populated canon file detected in sub-phase 1, run a confirm-or-edit pass.

Iterate in this order: `agents/BRAND.md`, `agents/BRIEF.md`, `agents/ROADMAP.md`, `agents/STATUS.md`, `agents/DESIGN.md`. (Cowork-tier files are not re-confirmed here — their content is session-driven, not user-curated.)

For each file:

1. **Summarize via a Haiku sub-agent:**

   ```
   Task(
     prompt="Read this canon file. Produce a single plain-English paragraph (max 4 sentences) describing what it says — the user's product, intent, scope, and any locked decisions. No bullet points. No file structure. Just the substance, as if you were explaining the project to a new teammate.",
     subagent_type="general-purpose",
     model="haiku"
   )
   ```

2. **Present to the user via AskUserQuestion:**

   ```
   I read your <file> as:

     "<summary paragraph from the sub-agent>"

   Matches your intent?

     A — Yes, keep as is
     B — Edit (you tell me corrections)
     C — Rebuild from scratch (will hand off to design-direction)
   ```

3. **Apply the choice:**
   - **A** — mark the file `confirmed = true`. No changes.
   - **B** — ask "What corrections?" via a free-text follow-up. A Sonnet sub-agent applies the corrections in place, preserving structure and unmodified sections. Show the diff before writing. User confirms before write.
   - **C** — mark the file `rebuild = true`. Do not touch it now. Queue for the design-direction handoff in sub-phase 7.

4. **Default behavior on no response / "skip":** treat as A (keep as is). Never silently overwrite.

Record the per-file decision for the modernize report.

---

## 0c.3 — Update global standards silently

Same rule as every other init mode — these are locked plugin standards, not per-project content.

1. **`agents/FUNDAMENTALS.md`** — copy verbatim from `${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/FUNDAMENTALS.md`. Silently overwrite.

   ```bash
   cp "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/FUNDAMENTALS.md" agents/FUNDAMENTALS.md
   ```

2. **`agents/TOOLING.md`** — only if `package.json` exists at project root (Node project). Copy verbatim from the plugin template. Silently overwrite.

   ```bash
   if [ -f package.json ]; then
     cp "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/TOOLING.md" agents/TOOLING.md
   fi
   ```

3. **`agents/DESIGN.md`** — DO NOT silently overwrite token frontmatter. Tokens are per-project. Instead, verify the structural envelope:
   - YAML frontmatter present (starts and ends with `---`)?
   - Required sections present in body: Overview, Colors, Typography, Spacing, Radius, Shadow, Components, **DO NOT**, **Extension protocol**, **Agent prompt guide**.
   - If any section is missing, surface to the user via AskUserQuestion: "Your DESIGN.md is missing the `<section>` section. I can copy the missing scaffold from the template and leave your existing content untouched. Apply?" — A yes / B skip.

   If the user picks A, splice the missing section in from the plugin template's `templates/DESIGN.md`. Never modify existing sections.

Record what was applied for the modernize report.

---

## 0c.4 — Codebase design-system sweep

Hand off to the upgraded `design-check` skill in **scan-all-files mode** (not diff mode).

```
Task(
  prompt="Run design-check in scan-all-files mode. Walk every component / page / style file in the codebase. Compare each against agents/DESIGN.md tokens. Categorize findings per file as (a) auto-fix-safe — hardcoded hex / px / font values that map cleanly to a known token, and (b) human-judgment — values without a clean token mapping, ambiguous accent usage, or anything the design system doesn't yet cover. Return findings grouped by file, sorted by severity (highest first).",
  subagent_type="general-purpose",
  model="sonnet"
)
```

Process the findings:

1. Categorize per file: `auto_fix_count`, `human_judgment_count`.
2. Show the top 10 files by total severity to the user:

   ```
   Design-system drift — top 10 files

     1. src/components/Hero.tsx           — 8 auto-fix, 2 human-judgment
     2. src/app/dashboard/page.tsx        — 5 auto-fix, 4 human-judgment
     ...
   ```

3. **Auto-fix safe violations** with batched confirmation — one confirmation per file:

   ```
   src/components/Hero.tsx — 8 safe fixes:
     bg-[#0a0a0a]          →  bg-background
     text-[#ededed]        →  text-foreground
     border-[#1a1a1a]      →  border-border
     ...

   Apply all 8?
     A — Yes
     B — Show me each one
     C — Skip this file
   ```

4. **Human-judgment violations** are listed in the modernize report for follow-up. Do not auto-fix.

Record auto-fix and pending counts for the modernize report.

---

## 0c.5 — STRUCTURE.md reconciliation

`agents/STRUCTURE.md` documents the codebase's surface map (marketing / dashboard / desktop, component conventions, styling approach). It must reflect the actual codebase.

### If `agents/STRUCTURE.md` is missing — first-run detection

Use Glob + a Haiku sub-agent to detect the project's structure:

- Top-level surfaces: any of `apps/`, `packages/`, `src/marketing/`, `src/dashboard/`, `src/desktop/`, `web/`, `mobile/`, `extension/`.
- Component convention: shadcn (`components/ui/`), styled-components, CSS modules, Tailwind raw, Swift UI, etc.
- Styling source of truth: `globals.css`, `tailwind.config.{js,ts}`, `tokens.ts`, Swift asset catalog.

Generate a draft STRUCTURE.md and show to the user before writing.

### If `agents/STRUCTURE.md` is present — verify against reality

Glob the current codebase. Diff each documented surface against the filesystem:

- Surfaces removed? (folder in STRUCTURE.md no longer exists)
- Surfaces added? (folder exists but isn't documented)
- Conventions drifted? (STRUCTURE.md says styled-components, codebase is now Tailwind)

Surface mismatches via AskUserQuestion:

```
STRUCTURE.md mismatches:

  Documented but missing:
    - apps/desktop (removed)

  Present but not documented:
    - apps/extension (added)

  Convention drift:
    - STRUCTURE.md says styled-components; codebase has migrated to Tailwind v4.

How to resolve?
  A — Apply all reconciliations (I'll show the diff first)
  B — Walk me through each
  C — Skip — leave STRUCTURE.md as-is
```

Record outcome for the modernize report.

---

## 0c.6 — Waste archival

For each waste candidate detected in sub-phase 1, present the list to the user before any move:

```
Waste candidates — will move to archive/2026-05-21-modernize/ (never deleted):

  [ ] cowork/WORKLOG.md.bak               (12 days old, rolled into CHANGELOG)
  [ ] agents/docs/detail/old-spec.md      (143 days old, not in INDEX.md)
  [ ] DESIGN-old.md                       (legacy file, replaced)
  [ ] agents/screenshot-2024-12-04.png    (orphaned, not referenced)

Proceed?
  A — Yes, archive all of the above
  B — Walk me through each one (opt-in per file)
  C — Skip archival entirely
```

If A: move each file to `archive/<YYYY-MM-DD>-modernize/<original-path-preserved>`. Create the archive folder if missing.

If B: per-file AskUserQuestion — keep / archive / skip.

If C: record "skipped by user" for the modernize report.

Never use shell `rm` or `unlink`. Only `mv` to the archive folder.

Record what was moved (and where) for the modernize report.

---

## 0c.7 — design-direction handoff

For any canon file the user chose **C — Rebuild** in sub-phase 0c.2: hand off to the `design-direction` skill with a re-anchor note.

```
Task(
  prompt="Re-anchor the brand for an existing project. The user marked <file> for rebuild during a modernize pass. Run the full design-direction flow but preserve all user-locked content already in agents/BRIEF.md. Treat this as a re-anchor, not a fresh init.",
  subagent_type="general-purpose",
  model="sonnet"
)
```

`design-direction`'s existing "preserve user content" rules apply. The skill will write the new BRAND.md / DESIGN.md Overview / refusal additions and return control to Phase 0c when done.

If no files were marked for rebuild, skip this sub-phase.

---

## 0c.8 — Modernize report

Final output. One screen. No preamble.

```
Modernize report — <project name>

  Canon re-confirmed (kept as-is):
    - agents/BRAND.md
    - agents/STATUS.md

  Canon edited per user input:
    - agents/BRIEF.md     (scope tightened, 2 locked decisions added)

  Canon marked for design-direction re-anchor:
    - agents/DESIGN.md    (handed off — see design-direction output above)

  Global standards updated (silent):
    - agents/FUNDAMENTALS.md
    - agents/TOOLING.md
    - agents/DESIGN.md structure verified (no sections missing)

  Codebase design-drift sweep:
    - Files scanned:           <N>
    - Auto-fixes applied:      <M>
    - Pending human judgment:  <K>   (see list below)

  STRUCTURE.md:
    - <created from first-run detection | reconciled <N> mismatches | left as-is>

  Waste archived (→ archive/<YYYY-MM-DD>-modernize/):
    - cowork/WORKLOG.md.bak
    - agents/docs/detail/old-spec.md
    - DESIGN-old.md

  Next steps for you:
    - Review the <K> human-judgment design findings in <follow-up file or list>.
    - Confirm the design-direction output for agents/DESIGN.md.
    - <any [VERIFY] items raised during the canon confirmation loop>
```

---

## End of Phase 0c

After the modernize report, the skill ends. Phases 1–7 of the standard flow are **skipped** — modernize handles all the substantive work, and Phase 7 is replaced by the report above.

Exception: if sub-phases 0c.2–0c.7 surface a need that maps to a standard phase (e.g., user asks to add an extended-context file, which is Phase 6), invoke just that phase, then stop. Do not re-run Phases 1–5 on a project that already has them.
