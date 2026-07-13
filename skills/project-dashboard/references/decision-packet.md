# Provisional UI decision packet

Read this when serving the dashboard, ingesting a submitted review, or changing its state contract.

## Boundaries

- UI Research owns the upstream derived `brain/research/page-recommendations.json`. Its exact `PAGE_RECOMMENDATIONS_V1` schema lives in `../../ui-research/references/round-formats.md`; do not duplicate or modify that schema here.
- Project Dashboard owns the downstream provisional `brain/research/ui-decision-draft.json`.
- Candidate clicks use browser storage only. Submit/Update is the only disk-write boundary.
- The JSON is an agent-readable proposal, not Markdown canon. The server always writes `canonical: false`, `agent_review.status: pending`, and `build_gates.site_wide_locked: false`.
- Claude/Codex owns compatibility review and canonical recording after final human approval.

## Submitted shape

```json
{
  "schema_version": 1,
  "canonical": false,
  "project": {"name": "", "root": "", "git_toplevel": "", "branch": "", "head": ""},
  "submission": {"id": "", "revision": 1, "status": "submitted", "submitted_at": "", "updated_at": ""},
  "research": {"mission_id": "", "mode": "", "evidence_readiness": "ready | ready_with_documented_gaps | not_ready", "derived_path": "brain/research/page-recommendations.json", "documented_gaps": []},
  "site_direction": {"recommendation_id": "", "status": "selected", "candidate_ids": []},
  "global_shell": {"target_id": "global-shell", "state": "recommended | not_needed", "recommendations": [], "decisions": []},
  "page_families": [],
  "pages": [{"id": "", "family_id": "", "label": "", "decisions": []}],
  "asset_requirements": [],
  "focused_research_requests": [],
  "provided_references": [],
  "agent_review": {"status": "pending", "allowed_compatibility_statuses": ["compatible", "compatible_with_adaptation", "conflicting"], "compatibility": [], "conflicts": [], "required_adaptations": []},
  "build_gates": {"site_wide_locked": false, "enabled_pages": []}
}
```

Each decision contains a stable recommendation ID, normalized scope, status, candidate IDs, affected blocks when applicable, and an optional human note. Allowed scopes are `whole_page`, `connected_sections`, `section`, `page_family`, and `global_shell`. Browser-authored human statuses are exactly `recommended`, `shortlisted`, `selected`, `not_using`, and `needs_more_research`. The browser never invents a compatibility verdict. Claude or Codex later uses exactly `compatible`, `compatible_with_adaptation`, or `conflicting` in its review and records the final result in the `## Approved Site Direction` contract.

## Validation and lifecycle

1. Bind the draft to the active checkout's `brain/research/page-recommendations.json`: checkout root, brain root, mission, mode, derived path, site direction, global shell, page families, targets, recommendation IDs, candidate IDs, and scopes must match that packet exactly.
2. Require every UI Research target exactly once. Each target must review a `whole_page` or `page_family` baseline before any `connected_sections` or `section` override can supplement it; a rejected baseline can still carry a focused-research or provided-reference request for the next revision.
3. Require every supplied global-shell option when `state: recommended`. When `state: not_needed`, shell recommendations and decisions must both be empty.
4. Require stable, unique page/family/decision IDs and valid family references.
5. On Submit, create revision 1 atomically. Refuse Submit when a packet exists.
6. On Update, require an existing packet and increment its revision atomically. Invalid updates leave the previous packet byte-for-byte intact.
7. Stamp the active root, Git top-level, branch, and HEAD on the server. Ignore browser-supplied path/Git authority.
8. After agent review and final human approval, record the exact `## Approved Site Direction` block in `brain/chapters/<active-chapter>.md`; this active chapter block is the only approval owner and build unlock. Record page execution decisions in the applicable chapter and asset state in `brain/marketing/MEDIA.md`. Research Markdown remains evidence, never design selection. Do not promote this JSON into a second canon.
