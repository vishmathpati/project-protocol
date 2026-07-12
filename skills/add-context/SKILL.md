---
name: add-context
description: Add an extended-context doc (data contract, domain reference, integration notes) to a project's `brain/docs/`. Use when supporting reference material needs a permanent home in the project's knowledge base. Triggers — "add context", "add context file", "create an integration doc".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*,ls:*,cat:*)
---

# Add Context

Add one or more extended context files to an already-initialized project. Each file is written into `brain/docs/` and immediately cross-referenced in root `CLAUDE.md` and `brain/docs/INDEX.md` so no file is orphaned.

---

## Pre-flight — Read existing protocol

Before adding anything, silently read:
1. **Root `CLAUDE.md`** — check if `## Extended Context` section exists; note current contents.
2. **`brain/docs/INDEX.md`** — locate the Key Files table; note current entries.

If either file is missing, stop and tell the user:

> "This project doesn't appear to have the brain protocol initialized yet — run init-project first."

If the project has the legacy flat layout (no `brain/` folder), also stop and tell the user:

> "This project uses a legacy layout. Run migrate-to-brain, then migrate-project, before adding context."

---

## The loop

Repeat until the user says done.

### Step 1 — File type

Use `AskUserQuestion`:

```
What type of extended context file do you need?

A — Data contracts (API response shapes, DB table schemas, type definitions)
B — Domain reference (business rules, terminology, product spec, "how this works")
C — Architecture supplement (infra diagram, service map, sequence flow)
D — External integration (third-party API docs, webhook shapes, rate limits)

Or describe in plain English — I'll categorize it.
```

### Step 2 — Filename

```
What should this file be called?
(examples: data-contracts.md, domain.md, stripe-integration.md)

It will live in `brain/docs/`.
```

Check whether `brain/docs/[filename]` already exists. If yes, ask:

```
brain/docs/[filename] already exists. What would you like to do?

A — Append new content to the existing file
B — Replace it entirely
C — Cancel — pick a different name
```

### Step 3 — Context collection

```
Paste the context for [filename] now.
This can be multiple pages — paste everything at once.
Type DONE on a new line when finished.
```

In Claude Code / Codex (multi-line input), you can send multiple messages and type DONE in the final one.

Accumulate all lines until "DONE" appears on its own line. Strip the "DONE" line.

### Step 4 — Summarize and write

Structure the raw paste based on file type:

**Data contracts** → organize into sections:
- Request shapes: `name → fields (types) — purpose`
- Response shapes: `name → fields (types) — purpose`
- Error types: `code — meaning — when it occurs`
- DB schema: `table_name: field (type) — purpose`
- Type definitions: shared TypeScript/Python types

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

Show preview: "Here's what I'll write to `brain/docs/[filename]` — does this look right?"

Apply corrections, then write the file.

Create `brain/docs/` if it doesn't exist: `mkdir -p brain/docs`

### Step 5 — Cross-reference immediately

Without asking, update two places:

**`brain/docs/INDEX.md`** — find the Key Files table and add:
```
| brain/docs/[filename] | [type]: [what it contains] — read before [trigger condition] |
```
If no Key Files table exists, create a `## Key Files` section.

**Root `CLAUDE.md`** — keep this as a concise index, not a second copy of the context. Find `## Extended Context` and append:
```
- `brain/docs/[filename]` — [type]: [one-line description]. Read before [trigger condition].
```
The `## Extended Context` stub is created by `init-project` Phase 3 — do not re-create it; it already exists. If it is genuinely missing (legacy project), create it at the bottom:
```markdown
## Extended Context
> These files go beyond the standard protocol. Read when their trigger applies.

- `brain/docs/[filename]` — [type]: [one-line description]. Read before [trigger condition].
```

If the file is architecture- or decisions-related (type C, or any file capturing "why" decisions were made), also update **`brain/BRIEF.md`**:
- Find or create a `## Reference files` section
- Append: `- brain/docs/[filename] — [description]`

Confirm: "Written ✅ — referenced in root CLAUDE.md and brain/docs/INDEX.md."

### Step 6 — Loop

```
Done. Another extended context file?

Y — Yes, add another
N — No, all done
```

Repeat from Step 1 if Y.

---

## When done

Output a tidy summary:

```
Extended context files added:
  ✅ brain/docs/[filename-1] — [type] — referenced in root CLAUDE.md + brain/docs/INDEX.md
  ✅ brain/docs/[filename-2] — [type] — referenced in root CLAUDE.md + brain/docs/INDEX.md

Root CLAUDE.md §Extended Context now lists [N] files.
Next session, the relevant agent will read these when their trigger condition applies.
```
