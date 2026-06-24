---
name: migrate-project
description: Apply version-by-version plugin migration deltas to bring a project up to the current plugin version. Use when SessionStart drift-detector flags a plugin-version gap, or manually via /migrate-project. Triggers — "migrate project", "update plugin files", "apply pending migrations", "/migrate-project", or when the SessionStart drift-detector prints a version-gap warning.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(cat:*,ls:*,find:*,git:*,sed:*,python3:*,diff:*)
---

# Migrate Project — project-protocol

Brings a project's protocol files up to the current plugin version by walking the ordered chain of `migrations/vX.Y.Z.md` manifests and applying each delta with explicit confirmation.

---

## When this fires

- SessionStart drift-detector printed a version-gap warning (`brain/.plugin-version` is behind the current plugin).
- User runs `/migrate-project` or says "migrate project" / "apply pending migrations".
- User is on-boarding an existing project after a plugin update.

**Does NOT fire for:** projects that are already up to date. Does NOT touch any project code (`src/`, `app/`, `components/`, etc.) — only protocol files (`brain/`, root CLAUDE.md, root README.md).

---

## Steps

### 1. Detect the tool environment

Check environment variables to determine which tool is running this skill:

- `$CLAUDE_PLUGIN_ROOT` is set → **Claude Code**
- `$CODEX_PLUGIN_ROOT` is set → **Codex**
- Neither is set → **Cowork**

There is no `.session-type` file — do not look for one.

### 2. Read the project's recorded plugin version

```bash
cat brain/.plugin-version 2>/dev/null || echo "pre-2.5.0"
```

If the file is absent, treat the recorded version as `pre-2.5.0`. This means all manifests from `v2.4.0.md` onward need to be checked.

Call this value `PROJECT_VERSION`.

### 3. Read the current plugin version

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-${CODEX_PLUGIN_ROOT:-}}"
cat "${PLUGIN_ROOT}/.claude-plugin/plugin.json" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

Call this value `PLUGIN_VERSION`.

### 4. Check if already up to date

If `PROJECT_VERSION` == `PLUGIN_VERSION`: report "Project is up to date on v${PLUGIN_VERSION}. Nothing to migrate." and exit cleanly.

### 5. Check the per-version skip marker

```bash
cat brain/.plugin-version-skip 2>/dev/null
```

If the file exists and its contents equal `PLUGIN_VERSION`: the user has deferred this migration. Report:

> Migrations deferred (skip marker found for v${PLUGIN_VERSION}). Nothing applied. Remove `brain/.plugin-version-skip` to re-enable the prompt.

Exit cleanly.

### 6. Resolve the manifest chain

List all `migrations/vX.Y.Z.md` files from the plugin root:

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-${CODEX_PLUGIN_ROOT:-}}"
ls "${PLUGIN_ROOT}/migrations/" 2>/dev/null | sort -V
```

Filter to manifests strictly newer than `PROJECT_VERSION` and at or before `PLUGIN_VERSION`. Process them in ascending version order.

If no manifests are found for the gap: report "No migration manifests found for the gap between v${PROJECT_VERSION} and v${PLUGIN_VERSION}. Nothing to apply." and exit.

### 7. Walk each manifest — propose, confirm, apply

For each manifest in the chain:

**7a. Read and display the manifest.**

Print a clear header:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration: vX.Y.Z  (project is on: PROJECT_VERSION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then list each delta from the manifest with a short label:
- `[ADD]` — file to be created
- `[MODIFY]` — file to be changed
- `[RULE]` — rule to be added to CLAUDE.md
- `[SKIP]` — delta already detected as present

**7b. Detect already-applied deltas.**

For each delta, run the detection check described in the manifest:
- If the manifest says "Detection: if root CLAUDE.md already contains `X`…", grep for that string.
- Mark the delta `[SKIP]` if already present.

**7c. Confirm before applying.**

Ask: "Apply the above deltas for vX.Y.Z? (all / skip-this-version / abort)"

- `all` — proceed with applying all non-skipped deltas.
- `skip-this-version` — write `PLUGIN_VERSION` into `brain/.plugin-version-skip` and stop. (This skips the entire migration until the next plugin update; per-version only — no permanent skip.)
- `abort` — stop without writing anything.

**7d. Apply each delta.**

For each delta marked for application:

- **[ADD] file added:** if the target file does not exist, create it from the template described in the manifest. If it already exists and is non-empty, surface a diff and ask: "File exists — overwrite / skip / view diff?"
- **[MODIFY] file modified:** diff the project's current file against the description in the manifest. If the project file diverges from the expected v(previous) base (i.e., user has customized it), surface the diff clearly:

  ```
  [project-protocol] Customization detected in <file>.
  Diff between your current file and the v(previous) template base:
  ---
  <diff output>
  ---
  Options: (a) apply delta on top — preserve your customizations, (b) full overwrite from new template, (c) skip this file
  ```

  Never silent-overwrite a customized file. Wait for explicit user choice.

- **[RULE] rule added:** if the rule text (or its detection string) is not already present in the target file, append the rule in the correct position. If present, mark as `[SKIP]`.

### 8. Write `brain/.plugin-version`

After all manifests in the chain have been processed (even if some deltas were skipped by the user):

```bash
echo "PLUGIN_VERSION" > brain/.plugin-version
```

This advances the project's recorded version to the current plugin version. Skipped deltas are the user's responsibility — they are surfaced in the summary.

### 9. Commit the changes

**Claude Code or Codex:** commit and push.

```bash
git add -A
git commit -m "chore: migrate protocol files to v${PLUGIN_VERSION}"
git push
```

**Cowork:** commit locally, then emit the push command for the user to run.

```bash
git add -A
git commit -m "chore: migrate protocol files to v${PLUGIN_VERSION}"
```

Then print:

> Protocol files committed locally. Run the following to push:
> `git push`

Do not refuse to run in Cowork. Apply the migration, commit, and hand the push to the user.

### 10. End-of-skill summary

Print a structured summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration complete — v${PROJECT_VERSION} → v${PLUGIN_VERSION}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Applied:   N deltas
Skipped:   M (already present — no action needed)
User action needed: K (listed below)

[If K > 0, list each skipped-by-user delta with the file name and why it was skipped.]

brain/.plugin-version updated to v${PLUGIN_VERSION}.

Next: run /save-session to confirm the protocol file changes are committed.
```

---

## Strict rules

- **Never touch project code.** Only protocol files under `brain/`, root `CLAUDE.md`, root `README.md`.
- **Never silent-overwrite a customized file.** Surface the diff; let the user decide.
- **No permanent skip.** The skip marker in `brain/.plugin-version-skip` stores the current plugin version. It re-prompts on the next plugin update because the new version won't match. There is no "skip forever" option.
- **Write `brain/.plugin-version` as the last act**, after applying (or user-confirming-skip of) every delta. Do not write it mid-chain.
- **Manifest chain is version-ordered.** Always walk from oldest-pending to newest. Never skip a manifest in the middle of the chain — each manifest's diff-base depends on the previous one having been applied.

---

## Difference from `init-project`

`init-project` bootstraps a brand-new project from scratch (or audits / modernizes an existing one interactively). `migrate-project` applies narrow, version-specific deltas to an already-initialized project — no re-asking of foundational questions, no full canon rebuild unless the manifest specifically requires it.
