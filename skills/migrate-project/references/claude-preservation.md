# CLAUDE preservation contract

Use this procedure before rewriting an existing root `CLAUDE.md`.

## 1. Capture the baseline

Read the checkpoint version of CLAUDE and the current working copy. Split all content into accountable blocks: headings with their bodies, standalone rules, comments/markers, tables, and unheaded text. Do not treat text outside a known heading as disposable.

## 2. Classify every block

- **Known plugin boilerplate** — text traceable to an old Project Protocol template, hook table, generic skill router, generic Git procedure, or retired operating rule. Propose `replace` or `remove` and name the v5 owner.
- **Custom** — project, business, personal, coding, safety, tooling, design, privacy, communication, or preference instructions not supplied by the plugin. Recommend `keep`.
- **Uncertain** — provenance or intent cannot be proven. Treat as custom and recommend `keep`.

Repeated or awkward wording is not evidence that a block is plugin boilerplate. Never classify from style alone.

## 3. Ask once, with an inventory

Show known boilerplate changes separately. Then show each custom/uncertain block with a short verbatim excerpt and these choices:

1. **Keep in CLAUDE (Recommended)** — preserve verbatim in the modernized front page.
2. **Move with pointer** — write the full block to an approved `brain/docs/<name>.md` destination and leave a concise CLAUDE trigger/pointer.
3. **Remove** — delete only after explicit approval for that block.

Accept a bulk answer, but never convert silence, “full modernization,” or approval of boilerplate cleanup into permission to delete custom content.

## 4. Write without loss

Build the concise v5 structure, insert every keep block verbatim, create approved move destinations, and replace only identified boilerplate. Preserve comments and markers that tools may depend on, including extended-context insertion markers.

If keeping all custom instructions makes CLAUDE long, keep them anyway. Conciseness is a default architecture, not authority to discard user rules.

## 5. Reconcile before stamping

Compare the checkpoint CLAUDE with the proposed result and report every original block as:

- preserved verbatim;
- moved to `<path>` with approval and pointer;
- replaced as `<identified old protocol source>`;
- removed with the user's explicit decision.

Any unaccounted block or unresolved choice is a mandatory migration blocker. Do not stamp the target plugin version.
