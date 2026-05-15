# Phase 0a — Empty-project bootstrap

Runs only when Phase 0 classifies the project as **empty** (Mode C) and the user opted to answer questions rather than accept placeholder templates. The goal is to gather just enough information that the three-folder templates can be populated with real content from the start.

This phase is read + collect + plan. It does NOT create files. Phase 3 onwards uses the answers gathered here to write populated templates instead of `[Project Name]` placeholders.

---

## What you collect

Use `AskUserQuestion`. Ask in a single batch if the tool supports multiple-choice + free-text in one call; otherwise ask one question at a time but keep momentum — no preamble, no commentary between questions.

1. **Project name** — what should this project be called?
2. **One sentence** — what does it do, in one sentence?
3. **Target user** — who is it for?
   - A — Just me (personal tool)
   - B — My team / company (internal tool)
   - C — External customers (product)
   - D — Open source / community
   - Or free text
4. **Tech stack** — what stack are you planning?
   - Free text. Examples: "Next.js + Supabase", "Python CLI", "Go service", "haven't decided yet".
5. **Current stage** —
   - A — Idea (nothing built yet)
   - B — Prototype (some code exists but not stable)
   - C — Actively building (real codebase, in development)
   - D — Already shipping (live with users)
6. **Locked decisions** — anything already decided you want captured in `agents/BRIEF.md` v1.0? Free text, can be empty.
   - Examples: "No auth in v1", "MIT licensed", "Postgres, not MongoDB", "Single binary deploy".
7. **First chapter direction** — what's the first thing you'd like on `agents/ROADMAP.md`? One sentence.
   - Example: "Get a working end-to-end skeleton — auth + one happy path."

Mark any answer the user explicitly punts on (e.g., "haven't decided", "skip") with `[VERIFY]` so Phase 7 surfaces it.

---

## What you do NOT ask

Don't duplicate downstream phases. The following are handled later — skip them here:

- Brand voice / personality / not-this — Phase 4 (BRAND.md A/B/C flow) handles this.
- Design tokens / colors / typography — Phase 4 (DESIGN.md A/B/C flow) handles this.
- Feature dependency map / shared functions / API surface — Phase 5 handles this (and writes a minimal stub for empty projects since there are no features yet).
- Extended-context files — Phase 6 offers this as an opt-in loop.

---

## Output of Phase 0a

A structured answer object passed forward to Phase 3:

```
{
  project_name: "<name>",
  one_sentence: "<sentence>",
  user: "just-me | team | external | open-source | <free text>",
  stack: "<stack or 'undecided'>",
  stage: "idea | prototype | building | shipping",
  locked_decisions: ["<decision>", "..."],
  direction: "<first chapter direction>"
}
```

---

## How later phases use these answers

**Phase 3 — root `CLAUDE.md`**
- `# CLAUDE.md — <project_name>` heading.
- Add a `## What this is` section with the `one_sentence` answer.

**Phase 3 — root `README.md`**
- Opening paragraph uses `one_sentence` + `user`.

**Phase 3 — `cowork/STATUS.md`**
- `## Current focus` line uses `direction` answer (or "Setting up the project" if empty).

**Phase 3 — `cowork/BRIEF.md` v1.0**
- `### What this is` derived from `one_sentence`.
- Leave `Locked decisions` empty — orchestration locks are user-driven.

**Phase 3 — `agents/STATUS.md`**
- `## Current sprint` line uses `direction`.
- `## Next actions` lists one placeholder: "Open `agents/BRIEF.md` and confirm tech stack + scope."

**Phase 3 — `agents/BRIEF.md` v1.0**
- `### What we're building` uses `one_sentence`.
- `### Tech stack — chosen` pre-fills a single row from `stack` (or marks `[VERIFY]` if "undecided").
- `### Architecture decisions` lists every entry from `locked_decisions`.
- `### Scope — in / out` left empty with `[VERIFY]` markers.

**Phase 3 — `agents/ROADMAP.md`**
- `## Direction` uses the answer to question 7.
- `## Phases / Acts` seeded with one stub: `### Act 1 — <direction summary>` with `[VERIFY]` on done criteria.

**Phase 4 — `agents/BRAND.md`**
- Name + one-sentence + target user are already known; the BRAND flow only needs the personality / tone / not-this answer (one short question instead of three).

**Phase 4 — `agents/DESIGN.md`**
- No existing tokens to detect. Use the "no existing tokens" branch (A — generate fresh from product description / B — describe the vibe).

**Phase 5 — `agents/docs/INDEX.md`**
- Minimal stub:
  - Section 1 Human Map: project sentence + "Pages: (none yet)" + "Features: (none yet)".
  - Section 2 Agent Dependency Index: all sections present, all marked `[VERIFY]` or "(none yet — add as features ship)".

**Phase 6 — extended context**
- Offered as usual. Most empty projects will say N here.

**Phase 7 — final summary**
- Lists every `[VERIFY]` marker for the user to fill in.

---

## Escape hatch

If the user types "skip questions" / "just placeholders" / "I'll fill it in later" at any point inside Phase 0a:
- Discard whatever was collected.
- Set the answer object to defaults (`project_name` = repo folder name, everything else `[VERIFY]`).
- Continue to Phase 3 — the templates fall back to the placeholder behavior used in Mode D (fresh).

---

## End of Phase 0a

Hand off directly to Phase 3 (skip Phase 1 and Phase 2 — there is nothing to discover and no non-protocol files to merge). Phase 4 runs after Phase 3. Phase 5 runs but writes the minimal-stub INDEX.md described above. Phase 6 is offered. Phase 7 surfaces `[VERIFY]` items.
