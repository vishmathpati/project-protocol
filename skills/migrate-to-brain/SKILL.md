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

**Bucket C — Markers to remove:**
- `agents/.session-type` — delete after migration (replaced by `brain/.plugin-version`).
- `agents/.plugin-version` — move to `brain/.plugin-version` (or create fresh if absent).
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

Bucket C — Markers:
  agents/.session-type      → DELETE (not needed in brain/ layout)
  agents/.plugin-version    → brain/.plugin-version
  agents/.plugin-version-skip → brain/.plugin-version-skip (if present)

Cleanup after migration:
  Remove cowork/, agents/, human/ once all files have been moved/merged.

⚠️  Recommendation: ensure you have a clean git state or a backup before proceeding.
     This operation MOVES files — not copies. The old folders will be removed on success.
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

For each file from `agents/`:

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
- If one file is empty or contains only the cleared-state placeholder (`# Worklog — cleared after each session.`), include it as-is under its stamp so the record is complete.

Write the merged result to `brain/<filename>`. Then delete both source files:

```bash
rm cowork/<file> agents/<file>
```

---

## Step 6 — Execute Bucket C: markers

Move or remove markers:

```bash
# Move .plugin-version
if [ -f agents/.plugin-version ]; then
  mv agents/.plugin-version brain/.plugin-version
else
  echo "3.0.0" > brain/.plugin-version   # set a known post-migration version if absent
fi

# Move skip marker if present
[ -f agents/.plugin-version-skip ] && mv agents/.plugin-version-skip brain/.plugin-version-skip

# Delete .session-type — not needed in brain/ layout
rm -f agents/.session-type
```

---

## Step 7 — Clean up empty source folders

After all moves and merges, remove the now-empty old folders:

```bash
rm -rf cowork/ agents/ human/
```

Before running this, verify the folders are actually empty (no files remain):

```bash
find cowork/ agents/ human/ -type f 2>/dev/null | wc -l
```

If the count is non-zero: **STOP**. List the remaining files and ask the user what to do. Do not `rm -rf` if files remain.

---

## Step 8 — Verify the result

Confirm the migration succeeded:

```bash
find brain/ -type f | sort
```

Print the full tree so the user can confirm everything arrived.

---

## Step 9 — Final summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration complete — three-folder → brain/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Moved:   N files  (Bucket A — no merge)
Merged:  M files  (Bucket B — both tiers combined, nothing lost)
Removed: cowork/  agents/  human/

brain/ contents:
  [full tree output from Step 8]

Next steps:
  1. Review brain/ to confirm everything looks right.
  2. Run `git add -A && git commit -m "chore: migrate layout to brain/"` to commit.
  3. Update your CLAUDE.md, root plugin config, and any skills that reference
     agents/, cowork/, or human/ to point to brain/ instead.
  4. Delete the migrate-to-brain skill before public launch.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Rules

- **Never overwrite silently.** Every destructive action requires user approval (Step 3). Nothing writes before "yes".
- **Nothing may be lost.** If a file exists in both tiers, merge it — do not choose one and discard the other.
- **Author stamps are mandatory.** Every merged file must carry the `· Codex / Claude Code tier` and `· Cowork tier` stamps so future readers know the provenance of each block.
- **Abort on any unexpected state.** If folders or files appear that are not in the plan, surface them to the user before proceeding.
- **This is a one-time operation.** Running it twice on an already-migrated project is a no-op (Step 1 exits cleanly). It is safe to re-check.
- **Delete this skill before launch.** After all known projects are migrated, remove `skills/migrate-to-brain/` from the plugin.
