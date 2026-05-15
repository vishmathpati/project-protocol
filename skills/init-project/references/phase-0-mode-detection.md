# Phase 0 — Mode detection

Decide which init mode applies before doing anything else. The mode determines whether the run continues into the empty-bootstrap path (Phase 0a), the old-version migration path (Phase 0b), the standard fresh init (Phase 1 onward), or audit mode.

This phase reads only — it does NOT create, move, or modify any files. It produces a single `mode` value and any context flags Phases 0a / 0b / 1 will need.

---

## 0.1 — Scan the project root

Run a quick, non-recursive scan first:

```bash
ls -la
ls cowork/ agents/ human/ 2>/dev/null
```

Then a full markdown glob (exclude `node_modules/`, `.git/`, `vendor/`, `dist/`, `build/`):

```
Glob: **/*.md
```

For projects with more than ~200 markdown files, delegate the glob to a Haiku sub-agent so the path list does not bloat your own context.

Record three things:

- Does the three-folder layout exist? (`cowork/`, `agents/`, `human/` all present as directories)
- Which root protocol files are present? — checking against `{CLAUDE.md, README.md, STATUS.md, BRIEF.md, WORKLOG.md, CHANGELOG.md, ROADMAP.md, BRAND.md, DESIGN.md, DISCOVERIES.md, FUNDAMENTALS.md, agenda.md}`
- Total markdown count across the whole project (used to detect the empty-project case)

---

## 0.2 — Classify mode (first match wins)

### Mode A — `audit` (three-folder layout already in place)

**Condition:** Root has `CLAUDE.md` + `README.md` AND directories `cowork/` + `agents/` + `human/` all exist.

**Action:** This project is already on the current protocol. Skip Phases 0a and 0b. Continue to Phase 1 with `audit_flag = true`. Phase 1 only buckets new / unrecognized files; Phases 3–6 fill missing files but never overwrite populated content.

### Mode B — `migration` (old-version flat layout)

**Condition:** Root has `CLAUDE.md` AND at least one of `{STATUS.md, BRIEF.md, WORKLOG.md, CHANGELOG.md, ROADMAP.md, BRAND.md, DESIGN.md, DISCOVERIES.md, agenda.md}`, BUT no three-folder layout (one or more of `cowork/`, `agents/`, `human/` missing).

**Action:** Run Phase 0b. The user's existing protocol content is preserved and ported into the three-folder layout. Phases 3–6 then layer in any new files this plugin version adds without overwriting migrated content.

### Mode C — `empty` (no markdown in the project)

**Condition:** Total markdown count is 0, or only auto-generated files like `LICENSE.md` / nested `node_modules/**/README.md`.

**Action:** Run Phase 0a (empty-project bootstrap) to gather basic project info from the user. Phase 1 is skipped (nothing to discover). Phases 3–6 use the bootstrap answers to populate templates with real content instead of placeholders.

### Mode D — `fresh` (existing codebase, no protocol files)

**Condition:** Project has source code and possibly some markdown (`README.md`, `CONTRIBUTING.md`, `docs/*.md`, etc.) but none of the protocol files at root and no three-folder layout.

**Action:** Standard fresh init. Continue to Phase 1 normally — Phase 1 buckets the existing markdown, Phase 2 asks per-file what to do (with the updated cowork / agents/docs / merge / reference / leave options), Phases 3–6 build out the three-folder layout.

---

## 0.3 — Announce the mode and confirm

Tell the user which mode you've detected. One paragraph + a plan.

For **Mode A (audit)** — no confirmation needed; announce and proceed:

```
Detected: three-folder layout already in place. Running in audit mode — I'll fill any missing files and report drift, but won't overwrite anything you've already populated.
```

For **Mode D (fresh)** — no confirmation needed; announce and proceed:

```
Detected: fresh project (existing codebase, no protocol files yet). I'll bucket your existing markdown in Phase 1, then ask per file what to do.
```

For **Mode C (empty)** — confirm before asking the bootstrap questions:

```
Detected: empty project (no markdown found). To populate the three-folder layout with real content instead of placeholders, I'll ask you a short set of questions about the project first.

Proceed?
  A — Yes, ask the questions
  B — Skip questions and just write placeholder templates I can fill in later
```

If A → Phase 0a. If B → jump straight to Phase 3 with placeholder templates.

For **Mode B (migration)** — confirm before any move:

```
Detected: older project-protocol layout (flat root, no cowork/ + agents/ + human/ folders). I can migrate it to the three-folder layout and layer in any new files this plugin version adds.

What I'll preserve: every line of content you already wrote.
What I'll move: mechanical moves for files with a clear destination; I'll ask about anything ambiguous.
What I'll add: only files this version introduces that don't exist yet.

Proceed?
  A — Yes, show me the migration plan and confirm again before any file moves
  B — Cancel
```

If A → Phase 0b. If B → stop and exit cleanly.

---

## Output of Phase 0

A single `mode` value plus context:

```
{
  mode: "audit | migration | empty | fresh",
  audit_flag: true | false,
  root_protocol_files_present: [<list>],
  total_md_count: <N>,
  has_three_folder: true | false,
  user_confirmed_to_proceed: true | false
}
```

Route to the next phase:
- `audit` → Phase 1 with `audit_flag = true`
- `migration` → Phase 0b
- `empty` → Phase 0a
- `fresh` → Phase 1 with `audit_flag = false`

If the user declined to proceed at any prompt, stop the skill cleanly — no error, no partial state.
