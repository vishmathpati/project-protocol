# Approved site direction contract

This chapter block is the only canonical unlock for a research-led marketing build. A recommendation
packet, dashboard choice, or submitted draft is evidence/proposal only.

```markdown
## Approved Site Direction
- Status: locked
- Submission ID: <ui-decision-draft submission.id>
- Submission revision: <integer>
- Project root: <active git toplevel or declared non-git root>
- Branch: <active branch or n/a>
- HEAD: <active commit or n/a>
- Approved by: <human identifier>
- Approved at: <ISO date/time>
- Site direction recommendation ID: <stable recommendation id>
- Global shell: <approved recommendation ids | not_needed>
- Unresolved conflicts: none

### Approved page and family matrix

| Target ID | Family ID | Routes | Approved recommendation IDs | Compatibility | Required adaptations | Exceptions |
|---|---|---|---|---|---|---|
| <stable id> | <stable id or n/a> | <all routes> | <stable ids> | compatible | none | none |
```

Compatibility uses only `compatible`, `compatible_with_adaptation`, or `conflicting`.

Every unique page and page family from the submitted sitemap must appear exactly once. Every family row
lists all member routes and any composition-changing exception. `conflicting` cannot be locked; resolve it
or change the selection first. `compatible_with_adaptation` requires concrete adaptations in the matrix.
The active checkout identity and submission ID/revision must match the reviewed provisional packet.

The global shell may be `not_needed` only when navigation, footer, and header treatment genuinely do not
apply. Otherwise list the reviewed global-shell recommendation IDs. A hero/header dependency remains an
explicit shell decision and never becomes approved implicitly.

Claude or Codex writes this block only after it has checked the complete submitted combination and the
human explicitly approves the reviewed result. Build Page rejects partial locks, including a Home-only
record when other unique pages or families remain absent.
