---
name: add-context
description: >
  Add extended context files to an already-initialized project. Use when a project
  needs deep-reference documentation beyond the standard protocol — data contracts,
  domain reference, architecture supplements, or external integration docs. After
  writing each file, automatically cross-references it in CLAUDE.md and docs/INDEX.md
  so the system knows it exists.
  Triggers: "add context", "add context file", "I need a data contracts file",
  "add domain reference", "create an integration doc", or any request to add
  a deep-reference markdown file to a project.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*,ls:*,cat:*)
---

# Add Context

Add one or more extended context files to an already-initialized project. Each file
is written into `docs/` and immediately cross-referenced in CLAUDE.md and docs/INDEX.md
so no file is orphaned.

---

## Pre-flight — Read existing protocol

Before adding anything, silently read:
1. `CLAUDE.md` — check if `## Extended Context` section already exists; note its current contents
2. `docs/INDEX.md` — locate the Key Files table; note its current entries

If either file is missing, stop and tell the user:
"This project doesn't appear to have a protocol set up yet — run init-project first."

---

## The Loop

Repeat until the user says done.

### Step 1 — File type

Ask via AskUserQuestion:

```
What type of extended context file do you need?

A — Data contracts (API response shapes, DB table schemas, type definitions)
B — Domain reference (business rules, terminology, product spec, "how this works")
C — Architecture supplement (infra diagram, service map, sequence flow)
D — External integration (third-party API docs, webhook shapes, rate limits)

Or describe in plain English — I'll categorize it.
```

### Step 2 — Filename

Ask via AskUserQuestion:

```
What should this file be called?
(examples: data-contracts.md, tcld-domain.md, stripe-integration.md)

It will live in docs/.
```

Check whether `docs/[filename]` already exists. If it does, ask:

```
docs/[filename] already exists. What would you like to do?

A — Append new content to the existing file
B — Replace it entirely
C — Cancel — pick a different name
```

### Step 3 — Context collection

Tell the user:

```
Paste the context for [filename] now.
This can be multiple pages — paste everything at once.
Type DONE on a new line when finished.
```

Wait for the paste. Accumulate all lines until "DONE" appears on its own line.
Strip the "DONE" line from the content before processing.

### Step 4 — Summarize and write

Based on file type, structure the raw paste into a clean document:

**Data contracts** → organize into sections:
- Request shapes: `name → fields (types) — purpose`
- Response shapes: `name → fields (types) — purpose`
- Error types: `code — meaning — when it occurs`
- DB schema: `table_name: field (type) — purpose`
- Type definitions: any shared TypeScript/Python types

**Domain reference** → organize into:
- Glossary: `term: definition`
- Business rules: numbered list, one rule per line
- Key workflows: step-by-step numbered flows
- Edge cases: what behaves differently from expected

**Architecture supplement** → organize into:
- Overview: one paragraph
- Components: `name: role — connects to: X, Y`
- Data flows: numbered steps
- Decisions: why this shape was chosen
- Open questions: anything unresolved

**External integration** → organize into:
- What it does for this project
- Auth method (API key / OAuth / webhook secret)
- Key endpoints/webhooks: `METHOD /path — purpose`
- Rate limits
- Error codes this project handles
- Env vars required

Add a header to every file:
```markdown
# [filename stem] — [type]
> Last updated: YYYY-MM-DD
> [one-line description of what this file contains]

---
```

Show a preview: "Here's what I'll write to docs/[filename] — does this look right?"
Apply any corrections, then write the file.

Create `docs/` if it doesn't exist: `mkdir -p docs`

### Step 5 — Cross-reference immediately

After writing the file, update two places without asking:

**docs/INDEX.md** — find the Key Files table and add:
```
| docs/[filename] | [type]: [what it contains] — read before [trigger condition] |
```
If no Key Files table exists, create a `## Key Files` section.

**CLAUDE.md** — find `## Extended Context` and append:
```
- docs/[filename] — [type]: [one-line description]. Read before [trigger condition].
```
If `## Extended Context` doesn't exist, create it at the bottom of CLAUDE.md:
```markdown
## Extended Context
> These files go beyond the standard protocol. Read when their trigger applies.

- docs/[filename] — [type]: [one-line description]. Read before [trigger condition].
```

If the file is architecture- or decisions-related (type C or any file that captures "why" decisions were made), also update **BRIEF.md**:
- Find or create a `## Reference files` section
- Append: `- docs/[filename] — [description]`

Confirm to the user: "Written ✅ — referenced in CLAUDE.md and docs/INDEX.md."

### Step 6 — Loop

Ask via AskUserQuestion:

```
Done. Do you need another extended context file?

Y — Yes, add another
N — No, all done
```

Repeat from Step 1 if Y.

---

## When done

Output a tidy summary:

```
Extended context files added:
  ✅ docs/[filename-1] — [type] — referenced in CLAUDE.md + INDEX.md
  ✅ docs/[filename-2] — [type] — referenced in CLAUDE.md + INDEX.md

CLAUDE.md §Extended Context now lists [N] files.
Next session, Claude Code will read these when their trigger condition applies.
```
