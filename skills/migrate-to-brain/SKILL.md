---
name: migrate-to-brain
description: Safely consolidate a legacy flat or three-folder Project Protocol layout into the single brain folder. Use only when `cowork/`, `agents/`, `human/`, or legacy root protocol files are detected. Preserves duplicates for semantic merge and hands back to migrate-project for the final version upgrade.
---

# Migrate to Brain

Legacy structural compatibility for public users. It is retained, explicit, and never auto-invoked.

## 1. Detect

Inventory root, `cowork/`, `agents/`, and `human/` files. If the project already has only `brain/`, return without changes. Capture Git branch/worktree and require CEO/solo authority on the integration branch.

## 2. Plan without writing

Classify files:

- Unique protocol file → proposed destination under `brain/`.
- Duplicate basename → semantic merge required; show every version and diff.
- Root/tier CLAUDE → inputs to one concise root CLAUDE; preserve project guardrails and context pointers.
- SITUATIONS → extract unique routing into root CLAUDE; do not create `brain/SITUATIONS.md`.
- README → preserve as the project's README; do not regenerate it as a protocol catalog.
- Non-protocol/unknown → leave in place until the user chooses.

Show proposed creates, merges, archives, and removals. Nothing writes before approval.

## 3. Checkpoint and consolidate

Create a checkpoint commit. Create `brain/` and copy unique files. For duplicates, write the approved merged result with provenance; never choose one silently. Ensure the v5 Universal Foundation files and chapter guide/template exist without fabricating history or real chapters.

Do not stamp `3.0.0` or `5.0.0`; Migrate Project owns the final version stamp after all pending migrations validate.

## 4. Reconcile and clean safely

Update exact old paths in root CLAUDE and `.gitignore` after review. Archive uncertain legacy files. Remove an old source folder only after `find` proves it contains no unhandled files and the user approved the removal. Never use broad `rm -rf` against populated folders.

## 5. Verify and hand back

Confirm one root CLAUDE, one `brain/` canon, no stray `brain/CLAUDE.md`, no new SITUATIONS, preserved README, chapter guide/template, and a clean inventory reconciliation. Then return to Migrate Project to apply the remaining version contract and stamp the installed version.

Report every moved, merged, archived, preserved, and unresolved file plus checkpoint/commit state.
