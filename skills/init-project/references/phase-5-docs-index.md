# Phase 5 — Generate `brain/docs/INDEX.md`

Analyze the codebase and generate a real, populated INDEX.md — not a blank template.

```bash
mkdir -p brain/docs/detail
```

## 5a. Detect project shape (Haiku)

```
Task(
  prompt="Scan project root. Detect: (1) monorepo (apps/ or packages/) or single; (2) frontend/backend split (separate backend/, server/, api/ dirs); (3) framework from package.json; (4) env var prefixes from .env.example. Report concisely.",
  subagent_type="general-purpose",
  model="haiku"
)
```

## 5b. Extract structure (Haiku, one sub-agent per concern)

**Routes:**
```
Scan app/, pages/, src/app/, src/pages/, routes/. List every route path with one-line description.
```

**API routes:**
```
Scan app/api/, pages/api/, routes/, src/routes/. List: HTTP method + path + one-line purpose. Flag webhook handlers explicitly.
```

**Services:**
```
Read .env.example or .env.local. Group by prefix (SUPABASE_, STRIPE_, CLERK_, etc.) — each prefix = one external service. Also scan for MCP config files and devDependencies CLI tools.
Output: service name + env prefix + how to access (MCP, CLI command, API).
```

**Dependencies:**
```
Read package.json. Extract framework + version, key libraries (auth, db, ui, payments, email, storage). Skip dev tooling.
```

## 5c. Identify shared functions and components (Sonnet)

```
Analyze the codebase. Find functions/components that are:
1. Imported in 3+ different files
2. Used across multiple features or pages
3. Central to data flow (auth, db writes, storage uploads)

For each: name, file, rough list of where it's imported/used.
Identify: which functions would cause widespread breakage if changed?

Output as structured list. Use Grep and Read to find imports.
```

## 5d. Infer features (Sonnet)

```
Based on routes, components, and API handlers, infer user-facing features. A feature is something a user can DO — not a technical implementation detail.

For each feature:
- Which page/route it lives on
- Status: live / in-progress / planned
- Which shared functions/components it depends on (use shared functions list)
- What external service it touches

Output as structured list suitable for a dependency map.
```

Provide this sub-agent the routes list, shared functions list, and services list.

## 5e. Write `brain/docs/INDEX.md` (Sonnet)

```
Write brain/docs/INDEX.md with exactly two sections.

SECTION 1 — HUMAN MAP (no code, no file paths, no function names):
- Project: one sentence + stack line
- Pages: one line per page/route — what it shows, what features it hosts
- Features: one line per feature — name, page, status (live/in-progress/planned)

SECTION 2 — AGENT DEPENDENCY INDEX:
- Data Model: entity/table names + one-line purpose + how to get schema (MCP command or file path)
- External Services: name + what it does + exact access method
- Key Files: non-obvious entry points only — auth config, middleware, shared utils, main DB client
- Critical Functions/Components: name + what features depend on them. Format: name → used by: feature-a, feature-b
- Feature Dependency Map: per feature:
    feature-name:
      flow: <Component> → POST /api/route → function() → ExternalService [config note]
      data: table.field (type)
      guards: auth requirements, limits, constraints
      shared with: other-feature (if any)
- Guardrails: 3-5 specific rules about what must not be changed or assumed

Flag uncertain items with [VERIFY].
Every entry one line maximum. No prose paragraphs.
```

## 5f. Create `brain/docs/detail/README.md`

```markdown
# brain/docs/detail/

Deep-dive documentation for features too complex for a single dependency map entry.

## Creation rule

Only create a file here when a feature's flow cannot be captured in the INDEX.md entry.
- DO create: OAuth flow, Stripe webhook pipeline, multi-step file processing.
- DO NOT create: basic CRUD, simple UI components, standard API routes.

When created, the INDEX.md entry links here: `→ brain/docs/detail/feature-name.md`

## Files
(none yet — created as needed)
```
