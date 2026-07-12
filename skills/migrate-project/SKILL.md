---
name: migrate-project
description: Transactionally migrate an initialized Project Protocol project to the installed plugin version. Use when Session Start reports version drift or the user asks to update protocol files. Produces one consolidated plan, applies deterministic changes safely, pauses for semantic review, validates, and stamps the version only after mandatory deltas pass.
---

# Migrate Project

Migration belongs to CEO or solo authority on the integration worktree. It never touches application code or auto-merges worker branches.

## 1. Inspect and consolidate

Resolve the plugin root, project root, current branch/worktree, recorded project version, installed version, and ordered pending manifests. Run `scripts/inspect_migration.py <project-root> --plugin-root <plugin-root>`.

If a legacy `cowork/`, `agents/`, or `human/` layout exists, run Migrate to Brain first, then return here. Do not apply the old version manifests blindly after a superseding structural migration; inspect their still-relevant deltas and present one consolidated plan.

Classify every delta: `ADD | RENAME | MODIFY | GENERATE | ARCHIVE | REMOVE | MANUAL | PLUGIN-ONLY`. Show affected files, detection evidence, customization risk, and whether it is mandatory.

## 2. Protect the checkout

- Require CEO/solo authority and the declared integration branch.
- Refuse overlapping dirty protocol files. Preserve unrelated dirty/untracked work.
- Create a checkpoint commit before mutation when protocol files already exist.
- Never use `git add -A`, stage a whole directory, switch branches, merge, or delete a worktree implicitly.

## 3. Apply deterministic deltas

Apply only transformations whose meaning is unambiguous: missing-file additions, exact skill-reference renames, safe path updates, plugin-owned template additions, and generated artifacts. Existing customized content is preserved. Show diffs.

## 4. Resolve semantic deltas

For BRIEF consolidation, CLAUDE routing preservation, STATUS history reduction, BRAND/DESIGN normalization, SITUATIONS reconciliation, marketing layout retirement, and other meaning-dependent work: produce a proposed diff, explain what moves where, and wait for approval. Archive before removing uncertain content.

`skip` leaves the migration incomplete. It never counts as success and never permits the version stamp.

## 5. Validate transactionally

Run the inspector again with `--validate-target`. Confirm:

- Required v5 files and routing exist.
- Retired current-source names are gone.
- No meaningful source was silently deleted.
- No application code changed.
- Optional files remain conditional.
- No mandatory delta is unresolved.
- Only migration-owned files are staged.

If validation fails, report exact blockers and leave the recorded version unchanged.

## 6. Stamp, commit, and push

Only after validation succeeds, write the installed version to `brain/.plugin-version`, remove the matching skip marker, stage explicit migration-owned files, commit, and push the integration branch. Do not call Save Session merely to complete migration.

## Report

Return versions, mode, checkpoint, applied/already-present/manual/archived counts, semantic decisions, validation evidence, explicit staged files, commit/push result, remaining dirty files, and exact next action.

## Guarantees

- Dry-run plan before mutation.
- Idempotent detection.
- No success stamp after skip or failure.
- No silent overwrite or deletion of customized canon.
- No application-code edits.
- No `git add -A`.
