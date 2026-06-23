# Phase 6 — Extended context files (optional)

Offer to add deep-reference files beyond the standard protocol.

## Ask if needed

Use `AskUserQuestion`:

```
Does this project need any extended context files beyond the standard protocol?

Extended context files are deep-reference documents specific to this project:
  • Data contracts — API response shapes, DB table schemas, type definitions
  • Domain reference — business rules, terminology, product spec
  • Architecture supplements — detailed infra diagrams, service maps, sequence flows
  • External integrations — third-party API docs, webhook shapes, rate limits

Y — Yes, let's add some
N — No, standard files are enough
```

If N: skip to Phase 7.

If Y: run the extended context loop.

## Extended context loop

Repeat until user says no more.

### Step 1 — File type

```
What type of extended context file?

A — Data contracts (API shapes, DB schemas, response types)
B — Domain reference (business rules, terminology, product spec)
C — Architecture supplement (infra diagram, service map, sequence flow)
D — External integration (third-party API docs, webhook shapes, rate limits)

Or describe in plain English.
```

### Step 2 — Filename

```
What should this file be called?
(examples: data-contracts.md, domain.md, stripe-integration.md)

It will live in brain/docs/.
```

### Step 3 — Context collection

```
Paste the context for [filename] now. Multiple pages OK — paste everything at once.
Type DONE on a new line when finished.
```

Accumulate until "DONE".

### Step 4 — Summarize and write

Structure the paste based on file type:

**Data contracts** → sections: Request shapes | Response shapes | Error types | DB schema | Type definitions. Each entry: `name → fields (types) — one-line purpose`.

**Domain reference** → sections: Glossary | Business rules (numbered) | Key workflows | Edge cases.

**Architecture supplement** → sections: Overview | Components | Data flows (numbered steps) | Decisions | Open questions.

**External integration** → sections: What it does | Auth method | Key endpoints/webhooks | Rate limits | Error codes | Env vars required.

Show preview: "Here's what I'll write to `brain/docs/[filename]` — does this look right?"

Apply corrections, write the file.

### Step 5 — Cross-reference immediately

Update two places:

**`brain/docs/INDEX.md`** — add to Key Files table:
```
| brain/docs/[filename] | [type]: [what it contains] — read before [trigger condition] |
```

**Root `CLAUDE.md`** — append to `## Extended Context` section (create if doesn't exist):
```
- `brain/docs/[filename]` — [type]: [one-line description]. Read before [trigger condition].
```

If file is architecture- or decisions-related: also add to `brain/BRIEF.md` `## Reference files`:
```
- `brain/docs/[filename]` — [description]
```

### Step 6 — Loop

```
Written ✅ — referenced in CLAUDE.md and INDEX.md. Another file?

Y — Yes, add another
N — Done
```

## Output

End of Phase 6: every extended context file is written, referenced in INDEX.md and root CLAUDE.md, and (if architecture-related) referenced in brain/BRIEF.md.
