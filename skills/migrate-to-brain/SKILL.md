---
name: migrate-to-brain
description: ONE-TIME layout migration — moves a project from the old three-folder layout (cowork/, agents/, human/) to the new single-folder layout (brain/). Triggers — "migrate to brain", "migrate layout", "/migrate-to-brain", or when SessionStart detects the old three-folder layout.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*,cat:*,find:*,mkdir:*,mv:*,cp:*,rm:*,echo:*,date:*)
---

> ⚠️  TEMPORARY SKILL — DISPOSABLE MIGRATION TOOL
> This skill exists solely to migrate projects off the old three-folder layout.
> Once all active projects have been migrated, DELETE this skill before public launch.
> Do NOT document it in user-facing materials or link to it from other skills.

# Migrate to Brain — Project Protocol

Migrates a project from the legacy three-folder layout (`cowork/`, `agents/`, `human/`) to the unified `brain/` folder. This is a one-time, destructive-but-reversible operation — nothing is silently overwritten and nothing is lost.

The migration does not just move files. It also brings the project fully onto the v3.0.0 layout: it sets `brain/.plugin-version` to `3.0.0`, regenerates the always-loaded structural files (root `CLAUDE.md`, `brain/SITUATIONS.md`, and the `README.md` layout section) from the current templates while preserving project-specific content, creates the new canon files that didn't exist before (`brain/WONT-DO.md`, `brain/chapters/README.md`, `brain/chapters/_TEMPLATE.md`), and rewrites old-layout `.gitignore` paths. So a migrated project ends up consistent — never describing the old layout it just left.

---

## When this fires

- User runs `/migrate-to-brain` or says "migrate to brain" / "migrate layout".
- SessionStart detects `cowork/`, `agents/`, or `human/` folders (or the `agents/.session-type` marker) and the user chooses to migrate now.

**Does NOT fire if:** `brain/` already exists and no old folders are present (already migrated).

---

## Step 1 — Detect the layout

Run:

```bash
ls -d cowork/ agents/ human/ brain/ 2>/dev/null
cat agents/.session-type 2>/dev/null || true
```

Evaluate:

- **Old layout present** — any of `cowork/`, `agents/`, `human/` exists (or `agents/.session-type` file is present): proceed to Step 2.
- **Already migrated** — `brain/` exists and none of the old folders are present:

  > Already migrated. `brain/` is present and no legacy folders remain. Nothing to do.

  Exit cleanly.

- **Partial state** — `brain/` exists AND old folders still exist: warn the user that a previous migration may have been interrupted. Ask:
  > "A partial migration was detected — `brain/` exists alongside legacy folders. Resume migration (re-run from the plan step) or abort?"
  Only continue with explicit user confirmation.

---

## Step 2 — Inventory

Scan and build a complete inventory of every file that will move. Run:

```bash
find agents/ cowork/ human/ -type f 2>/dev/null | sort
```

Categorize each file into one of three buckets:

**Bucket A — Move only (exists in one tier):**
Files that exist only in `agents/` or only in `human/` — no merge needed.

- All files from `agents/` move to `brain/` at the same relative path (e.g. `agents/docs/INDEX.md` → `brain/docs/INDEX.md`).
- `human/agenda.md` → `brain/agenda.md`.
- Any other `human/` files → `brain/` at their relative path (without the `human/` prefix).

**Bucket B — Merge required (same filename in both cowork/ and agents/):**
Files with matching names that exist in both tiers. These require content merging, not simple overwriting. Common candidates:

- `STATUS.md`
- `BRIEF.md`
- `WORKLOG.md`
- `CHANGELOG.md`
- Any other `.md` file present in both `cowork/` and `agents/`.

Detect them:

```bash
comm -12 \
  <(ls cowork/ 2>/dev/null | sort) \
  <(ls agents/ 2>/dev/null | sort)
```

**EXCEPTION — `CLAUDE.md` is NOT a Bucket B merge.** The old layout has a root `CLAUDE.md` plus per-tier copies (`cowork/CLAUDE.md`, and possibly `agents/CLAUDE.md`). The new layout has ONLY the root `CLAUDE.md` (the front page / rules index) and NO `brain/CLAUDE.md`. So never merge a `CLAUDE.md` into `brain/CLAUDE.md`. Instead, treat ALL `CLAUDE.md` files (root + every tier copy) as inputs to the structural regeneration step (Step 6), then delete the tier copies. The same applies to any tier `SITUATIONS.md` — it is regenerated, not merged into a tier path.

**Bucket C — Markers:**
- `agents/.session-type` — delete after migration (no longer used; authorship is now per-entry author-stamps).
- `agents/.plugin-version` — do NOT move the old value. The migration upgrades the project to the v3.0.0 layout, so `brain/.plugin-version` is SET (overwritten) to `3.0.0`. Moving the old value (e.g. `2.5.0`) would leave it stale and re-trigger the drift-detector.
- `agents/.plugin-version-skip` — move to `brain/.plugin-version-skip` if present.

---

## Step 3 — Show the plan and require approval

Print a structured migration plan. Do NOT touch any files until the user approves.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration plan: three-folder → brain/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bucket A — Move (no merge needed):
  agents/ROADMAP.md             → brain/ROADMAP.md
  agents/DISCOVERIES.md         → brain/DISCOVERIES.md
  agents/docs/INDEX.md          → brain/docs/INDEX.md
  agents/docs/...               → brain/docs/...
  agents/marketing/...          → brain/marketing/...
  agents/preview/...            → brain/preview/...
  human/agenda.md               → brain/agenda.md
  (... full list of files ...)

Bucket B — Merge (both tiers have this file — content from both will be preserved):
  cowork/STATUS.md  +  agents/STATUS.md    → brain/STATUS.md
  cowork/BRIEF.md   +  agents/BRIEF.md     → brain/BRIEF.md
  cowork/WORKLOG.md +  agents/WORKLOG.md   → brain/WORKLOG.md
  cowork/CHANGELOG.md + agents/CHANGELOG.md → brain/CHANGELOG.md
  (... any others ...)

  Merge format: agent-tier content first, then a divider, then cowork-tier content.
  Nothing is discarded. Both blocks are author-stamped.

  NOTE: CLAUDE.md is NOT merged here — root + tier copies feed the regenerate step.

Bucket C — Markers:
  agents/.session-type        → DELETE (no longer used)
  brain/.plugin-version        = SET to 3.0.0 (overwrite — project is now on v3.0.0 layout)
  agents/.plugin-version-skip → brain/.plugin-version-skip (if present)

Regenerate (structural protocol files — rebuilt from current templates, project content preserved):
  root CLAUDE.md (root + cowork/agents/stray-brain CLAUDE.md → new front page)
  brain/SITUATIONS.md (situation router refreshed to brain/ paths + current skills)
  README.md (structure section updated to brain/, if it maps the old layout)

  PRESERVED, not regenerated: Coding Standards, project name, project-specific
  rules, Extended Context, and the merged STATUS/BRIEF/WORKLOG/CHANGELOG content.
  Only the structural / skill-index / routing scaffolding is rebuilt from templates.
  Any stray brain/CLAUDE.md is folded into the root CLAUDE.md, then removed.

Create (new canon files — didn't exist in old layout):
  brain/WONT-DO.md
  brain/chapters/README.md
  brain/chapters/_TEMPLATE.md

.gitignore:
  Rewrite any agents/ , cowork/ , human/ ignore paths → brain/ equivalents
  (e.g. agents/preview/ → brain/preview/)

Cleanup after migration:
  Remove cowork/, agents/, human/ once all files have been moved/merged.

⚠️  Recommendation: ensure you have a clean git state or a backup before proceeding.
     This operation MOVES files — not copies. The old folders will be removed on success.
     The regenerated CLAUDE.md / SITUATIONS.md / README.md are shown for approval before writing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceed with migration? (yes / abort)
```

Wait for explicit "yes" before continuing. Any other response aborts cleanly with no files changed.

---

## Step 4 — Execute Bucket A: move files

Create `brain/` and all needed subdirectories. Then move each Bucket A file:

```bash
mkdir -p brain/
```

**Do NOT move `CLAUDE.md` or `SITUATIONS.md` here.** Any `agents/CLAUDE.md`, `cowork/CLAUDE.md`, `agents/SITUATIONS.md`, or `cowork/SITUATIONS.md` is an input to the regenerate step (Step 6) and is deleted there, not moved into `brain/`. Read them now (so their project-specific content is captured) but leave them in place until Step 6.

For each remaining file from `agents/`:

```bash
# Preserve directory structure
src="agents/path/to/file"
dst="brain/path/to/file"
mkdir -p "$(dirname "$dst")"
mv "$src" "$dst"
```

For `human/agenda.md`:

```bash
mv human/agenda.md brain/agenda.md
```

For any other `human/` files (preserving subfolder structure, stripping the `human/` prefix):

```bash
find human/ -type f ! -name 'agenda.md' | while read f; do
  rel="${f#human/}"
  mkdir -p "brain/$(dirname "$rel")"
  mv "$f" "brain/$rel"
done
```

---

## Step 5 — Execute Bucket B: merge files

For each file that exists in both `cowork/` and `agents/`, produce ONE merged file in `brain/`.

**Merge format:**

```markdown
<!-- migrated-to-brain: merged from agents/ and cowork/ on YYYY-MM-DD -->

<!-- ─── · Codex / Claude Code tier ──────────────────────────────────── -->

<full contents of agents/<file>>

---
<!-- ─── · Cowork tier ────────────────────────────────────────────────── -->

<full contents of cowork/<file>>
```

Rules:
- Agent-tier content (from `agents/`) appears FIRST — it is the canonical engineering record.
- Cowork-tier content (from `cowork/`) appears SECOND after a divider.
- The author stamps (`· Codex / Claude Code tier` and `· Cowork tier`) are HTML comments so they are invisible in rendered markdown but fully preserved in raw text.
- Nothing from either file is omitted, truncated, or summarized.
- If one file is empty or contains only the cleared-state placeholder, include it as-is under its stamp so the record is complete. The standardized cleared marker is `> WORKLOG cleared — last session closed cleanly.`; tolerate the old marker `# Worklog — cleared after each session.` too (old projects may carry either).

Write the merged result to `brain/<filename>`. Then delete both source files:

```bash
rm cowork/<file> agents/<file>
```

---

## Step 6 — Execute Bucket C: markers

Set the version and handle the other markers. **Always SET `brain/.plugin-version` to `3.0.0`** — the migration upgrades the project to the v3.0.0 layout. Do NOT move the old value (e.g. `2.5.0`); a stale value would re-trigger the drift-detector on next session.

```bash
mkdir -p brain/

# SET the version — overwrite, regardless of any old value
echo "3.0.0" > brain/.plugin-version

# Move skip marker if present (preserve a deliberate skip)
[ -f agents/.plugin-version-skip ] && mv agents/.plugin-version-skip brain/.plugin-version-skip

# Discard the old version file — its value is superseded by 3.0.0 above
rm -f agents/.plugin-version

# Delete .session-type — no longer used
rm -f agents/.session-type
```

---

## Step 7 — Regenerate the structural protocol files

These files describe the layout + skills and are loaded every session, so they cannot be left describing the old layout. Regenerate each from the **current** canonical templates in `init-project/references/phase-3-brain-create.md`, preserving project-specific content. **Show the user the proposed result (or a diff) for each, and only write after confirmation** — these are always-loaded files.

### 7a. Root `CLAUDE.md` (regenerate — do not merge)

Rebuild from the canonical root-`CLAUDE.md` template. The new file MUST carry, from the current template:

- The "front page / rules index — NOT the brain" framing (the brain is the `brain/` folder; this file points into it). Do **not** describe the old three-folder layout or call this file "the brain".
- The `## Folder map` describing `brain/` (single canon folder) and `brain/chapters/`.
- The FULL current **Skill index** table — including `ceo`, `worker`, `solo`, `git`, `grill`, `bug-fixing`, `handoff`, `migrate-project` (and the rest in the template).
- The **Hooks index** table.
- The Non-negotiable rules, Git rules, Pre-task classification, and Situation-router pointer to `brain/SITUATIONS.md`.

PRESERVE from the OLD root `CLAUDE.md` + `cowork/CLAUDE.md` (the orchestration-tier front page) + `agents/CLAUDE.md` (if present):

- The **project name** (in the `# CLAUDE.md — [Project Name]` heading).
- The **Coding Standards** section if the project customized it.
- Any **project-specific rules** the project added beyond the template defaults.
- Any still-useful **orchestration-tier guidance** from `cowork/CLAUDE.md` (e.g. Cowork-specific workflow notes) — fold it into the regenerated root file rather than dropping it.
- The **Extended Context** section (everything under the `<!-- add-context appends here -->` marker).

**Stray `brain/CLAUDE.md` — fold and remove.** If an earlier or partial migration moved a tier `CLAUDE.md` into `brain/CLAUDE.md`, treat that file as one more input to this regeneration (fold its project-specific content in alongside the others), then delete it. The new layout has ONLY a root `CLAUDE.md` — there is no `brain/CLAUDE.md`.

```bash
# Capture any stray brain/CLAUDE.md as a regeneration input, then remove it.
[ -f brain/CLAUDE.md ] && cat brain/CLAUDE.md   # read it before deleting
```

Show the rebuilt `CLAUDE.md` (or a diff against the old root file) and wait for approval. On approval, write root `CLAUDE.md` and delete every tier / stray copy:

```bash
rm -f cowork/CLAUDE.md agents/CLAUDE.md brain/CLAUDE.md
```

### 7b. `brain/SITUATIONS.md` (regenerate)

The moved/old situation router still routes to old skills and old `cowork/`·`agents/`·`human/` paths. Regenerate the routing table from the current `brain/SITUATIONS.md` template (all `Read first` paths point into `brain/`). PRESERVE any genuinely project-specific routes the old router added (re-pointed to `brain/` paths). Show the result, then on approval write `brain/SITUATIONS.md` and remove any tier copy:

```bash
rm -f cowork/SITUATIONS.md agents/SITUATIONS.md
```

### 7c. Project `README.md` (update if it maps the old layout)

If the root `README.md` describes the old three-folder structure (a `cowork/` / `agents/` / `human/` file catalog or layout section), update its structure/layout section to the `brain/` catalog from the current README template. PRESERVE all project-specific content (project-specific file entries, notes, cascade customizations). If the README does not map the layout, leave it untouched. Show the diff, then write on approval.

---

## Step 8 — Create the new canon files

These did not exist in the old layout, so there is no old content to migrate — write fresh stubs from the current templates in `phase-3-brain-create.md`. Create only if absent (never overwrite content that already arrived via a move):

```bash
mkdir -p brain/chapters
```

- `brain/WONT-DO.md` — from the `brain/WONT-DO.md` template.
- `brain/chapters/README.md` — from the `brain/chapters/README.md` template.
- `brain/chapters/_TEMPLATE.md` — from the `brain/chapters/_TEMPLATE.md` template.

```bash
[ -f brain/WONT-DO.md ] || cat > brain/WONT-DO.md <<'EOF'
# brain/WONT-DO.md — Rejected Decisions
> A running list of things we deliberately decided NOT to do, each with a one-line reason.
> Append-only. When you reject an option during any session, add it here instead of burying it in chat.
> Format: YYYY-MM-DD · [Cowork | Codex | Claude Code] — what we rejected — one-line reason.

## Log
(none yet — add a line each time an option is killed)
EOF

[ -f brain/chapters/README.md ] || cat > brain/chapters/README.md <<'EOF'
# brain/chapters/ — Delegated-Work Units

One file per chapter, named `NN-name.md` (e.g. `01-auth.md`).

## Lifecycle

1. **CEO** opens a new file, fills in `## Goal` and `## Plan`, then hands it off.
   (Use the `ceo` skill — it scaffolds the file and delegates to a worktree.)
2. **Worker** executes the work on a branch, then appends `## Completion Report`.
   (Use the `worker` skill — it defines the exact report format.)
3. **CEO** reads the report and fills in `## CEO Verdict` (approved → merge, or returned → reason).

## Template

Copy `_TEMPLATE.md` when creating a new chapter.
EOF

[ -f brain/chapters/_TEMPLATE.md ] || cat > brain/chapters/_TEMPLATE.md <<'EOF'
# Chapter NN — <name>

## Goal
<CEO: what this chapter delivers>

**Method:** solo | CEO+worker | CEO+specialists

## Plan
<CEO: approach; how it splits across workers if multi-specialist>

---
<!-- Completion Reports append below — one per worker pass (e.g. backend, then UI, then wire-up). Never overwrite a prior report. -->

<!-- CEO Verdicts append below, one per report verified. -->
EOF
```

---

## Step 9 — Fix `.gitignore`

If `.gitignore` ignores any old-layout paths, rewrite them to the `brain/` equivalents so the right things stay ignored (notably `brain/preview/`):

```bash
if [ -f .gitignore ]; then
  sed -i.bak -E 's#(^|/)agents/#\1brain/#g; s#(^|/)cowork/#\1brain/#g; s#(^|/)human/#\1brain/#g' .gitignore
  rm -f .gitignore.bak
fi
```

This turns e.g. `agents/preview/` into `brain/preview/`. Review the result; if a rewrite collapses two old entries onto the same `brain/` path, de-duplicate.

---

## Step 10 — Clean up empty source folders

After all moves, merges, and regenerations (the tier `CLAUDE.md` / `SITUATIONS.md` copies were removed in Step 7), remove the now-empty old folders:

```bash
rm -rf cowork/ agents/ human/
```

Before running this, verify the folders are actually empty (no files remain):

```bash
find cowork/ agents/ human/ -type f 2>/dev/null | wc -l
```

If the count is non-zero: **STOP**. List the remaining files and ask the user what to do. Do not `rm -rf` if files remain.

---

## Step 11 — Verify the result

Confirm the migration succeeded:

```bash
find brain/ -type f | sort
cat brain/.plugin-version   # should print 3.0.0
ls CLAUDE.md README.md      # root front page + file map
ls brain/SITUATIONS.md brain/WONT-DO.md brain/chapters/README.md brain/chapters/_TEMPLATE.md
[ -e brain/CLAUDE.md ] && echo "WARNING: stray brain/CLAUDE.md still present" || echo "OK: no brain/CLAUDE.md"
```

Print the full tree so the user can confirm everything arrived. Confirm there is NO `brain/CLAUDE.md` (the front page is the root `CLAUDE.md` only) and that `brain/.plugin-version` reads `3.0.0`. If a stray `brain/CLAUDE.md` is still reported, go back to Step 7a — its content must be folded into the root `CLAUDE.md` and the stray file removed before the migration is complete.

---

## Step 12 — Final summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration complete — three-folder → brain/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Moved:       N files  (Bucket A — no merge)
Merged:      M files  (Bucket B — both tiers combined, nothing lost)
Regenerated: CLAUDE.md · brain/SITUATIONS.md · README.md (from current templates)
Created:     brain/WONT-DO.md · brain/chapters/README.md · brain/chapters/_TEMPLATE.md
Version:     brain/.plugin-version set to 3.0.0
.gitignore:  old-layout paths rewritten to brain/
Removed:     cowork/  agents/  human/  (+ tier / stray-brain CLAUDE.md + SITUATIONS.md copies)

brain/ contents:
  [full tree output from Step 11]

Next steps:
  1. Review brain/ and the regenerated CLAUDE.md / SITUATIONS.md / README.md to confirm
     everything looks right. (These were regenerated automatically and shown for approval
     before writing — no manual CLAUDE.md surgery needed.)
  2. Run `git add -A && git commit -m "chore: migrate layout to brain/"` to commit.
  3. Delete the migrate-to-brain skill before public launch.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Rules

- **Never overwrite silently.** Every destructive action requires user approval (Step 3). Nothing writes before "yes". The regenerated always-loaded files (`CLAUDE.md`, `brain/SITUATIONS.md`, `README.md`) are additionally shown for approval before they are written (Step 7).
- **Nothing may be lost.** If a file exists in both tiers, merge it — do not choose one and discard the other. When regenerating `CLAUDE.md` / `SITUATIONS.md` / `README.md`, preserve every piece of project-specific content (project name, Coding Standards, custom rules, Extended Context, custom routes, custom README entries).
- **Author stamps are mandatory.** Every merged file must carry the `· Codex / Claude Code tier` and `· Cowork tier` stamps so future readers know the provenance of each block.
- **Land the project on v3.0.0.** `brain/.plugin-version` is SET to `3.0.0` — never carry the old value forward, or the drift-detector re-fires.
- **No `brain/CLAUDE.md`.** The front page is the root `CLAUDE.md` only; tier copies — and any stray `brain/CLAUDE.md` left by a prior/partial migration — are inputs to regeneration (their content is folded into the root file) and are then deleted.
- **Abort on any unexpected state.** If folders or files appear that are not in the plan, surface them to the user before proceeding.
- **This is a one-time operation.** Running it twice on an already-migrated project is a no-op (Step 1 exits cleanly). It is safe to re-check.
- **Delete this skill before launch.** After all known projects are migrated, remove `skills/migrate-to-brain/` from the plugin.
