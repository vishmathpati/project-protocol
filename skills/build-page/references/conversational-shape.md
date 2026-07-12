# Conversational shape — how build-page stays productive across a long session

A page build is a long conversation. This file documents the prose-level discipline that keeps the conversation productive without inventing new machinery beyond what every other skill in the plugin already uses.

## The model

There are no formal phases. There is a starting state and there is an ending state, and in between the user iterates freely. The skill's job is to keep the canon, the WORKLOG, and the user's intent aligned across however many turns it takes.

Starting state: the user invokes the skill, names a page, the agent reads canon, surfaces an analysis, proposes a starting plan, and announces the conversation is open.

Ending state: every section has a real component path, the page file is written, INDEX.md is updated, `design-check` has run, and the agent prints the end-of-skill summary. The user can also end early by saying "save" or "close" — `save-session` runs, and the build is suspended (resumable next time via the breadcrumbs in WORKLOG + STATUS Next Actions).

Everything between those two states is conversation.

## Cadence rules

**Surface analysis before proposing.** When entering a new context (new page, new section, new external reference), read the relevant material first, then describe what you read in one paragraph, then propose. Do not propose before describing what you read. Users push back more usefully when they see what the agent is working from.

**One proposal at a time.** Don't propose three section orderings at once. Don't propose a plan AND component strategies in the same turn. Each proposal is a single thing the user can react to.

**Iterate in place.** When the user pushes back, revise the proposal and re-show it. Don't write iteration history files. Don't number proposals "v1, v2, v3" — that adds friction. The conversation transcript is the history.

**No 5-iteration cap.** `design-direction`'s Phase 6.5 caps token iterations because tokens have a small valid surface and looping there usually means the direction is wrong. Page architecture has a huge valid surface — iterating ten times on the section list is fine. The user knows when they've landed.

**Append to WORKLOG only on decisions, not on iterations.** A user saying "drop §6" is iteration, not a decision — don't log it. The user saying "yes, plan locked, 9 sections, hero-loud, trust-calm, …" is a decision — log it as `[HH:MM] decided: build-page plan locked for /home — 9 sections`.

## What goes in WORKLOG

One line per decision, canonical prefix vocabulary, timestamp at the start.

`decided:` entries — append on:
- Skill start: `[HH:MM] decided: build-page started for /<slug> (<tier>)`. This is mandatory — it disarms the cleared-state PreToolUse warning that would otherwise fire on the first Edit/Write later in the session.
- Plan lock: `[HH:MM] decided: build-page plan locked for /<slug> — N sections`.
- Per-section strategy lock: `[HH:MM] decided: §<n> strategy — <reuse|adapt|build-new> via <component path>`.
- Per-section built: `[HH:MM] decided: §<n> built — <component path>`.
- External reference adopted: `[HH:MM] decided: §<n> adopting external <source> via build-component adopt-external`.
- Page wired: `[HH:MM] decided: build-page wired /<slug> → <file path>`.
- Skill complete: `[HH:MM] decided: build-page complete for /<slug> — N components used (R reused, A adapted, N built)`.

`tried_failed:` entries — append on:
- Plan iteration that the user rejected: `[HH:MM] tried_failed: build-page plan v1 for /<slug> — user wanted 4-col workflow not 3-col`.
- Component strategy that didn't fit: `[HH:MM] tried_failed: §<n> v1 — proposed adapt of <component>, user wanted build-new`.
- External reference rejected: `[HH:MM] tried_failed: §<n> external <source> — <reason for reject>`.

`found_bug:` entries — append on:
- A real bug discovered during the build (missing token in DESIGN.md, broken existing component, canon contradiction). Use P1/P2/P3 severity tag.

`fixed:` entries — append on:
- A bug fixed in passing during the build (rare — usually fixes are explicit work, not page-build side-effects).

Hook-injected lines (`[HH:MM] subagent_start` / `[HH:MM] subagent_stop`) will also appear automatically — they're added by the SubagentStart / SubagentStop hooks when Task tool sub-agents run. Ignore them; `save-session`'s grep skips them.

## What goes in BRIEF.md

Per `save-session` Step 6 contract: append a version block on major locks. For build-page:

**Plan lock** writes a block:
```markdown
---

## v1.X — YYYY-MM-DD HH:MM · Claude Code

build-page locked architecture for /<slug>:
N sections — <one-line rhythm summary>
Strategy will be drawn from these existing components: <list>
Net-new components anticipated: <count, names>
External references adopted: <list, if any, with sources>
```

**Page wired** writes a follow-up block:
```markdown
---

## v1.X+1 — YYYY-MM-DD HH:MM · Claude Code

build-page shipped /<slug>:
File written: <path>
Components used: <N reused, N adapted, N built new>
INDEX.md updated.
design-check: <findings or clean>.
```

Per-section component decisions don't merit their own BRIEF blocks — they fold into the page-wired block.

## What goes in INDEX.md

Read `brain/docs/INDEX.md`. Find the section that lists pages (usually `## Pages` or `## Routes` or a similar heading). Append a row for the new page:

```markdown
- `/<slug>` — <one-line intent from brief> · `src/app/(<tier>)/<slug>/page.tsx`
```

If the file doesn't have a Pages / Routes section, add one (with a `## Pages` heading) and put the row there. Keep entries alphabetical within the section.

This satisfies `save-session` Step 4. Without this inline update, save-session plants a reminder in STATUS Next Actions to update INDEX.md — clutter that's avoidable.

## What does NOT happen

- **No `brain/build-page-scratch/` folder.** Ever.
- **No state file.** The conversation transcript + canon + WORKLOG are the state.
- **No iteration history files** (e.g. `plan-v1.md`, `plan-v2.md`). Iterate in place in chat.
- **No tool palette restriction.** Standard `allowed-tools` per the SKILL.md frontmatter. The discipline is prose, not enforcement.
- **No multi-page tracking.** One slug per session. Second invocation of `/build-page` halts politely if the prior session didn't close: *"There's an open build-page session for /<previous-slug> (last WORKLOG entry: <line>). Close that first with `save-session`, or type 'switch' to suspend it and start a new one."*
- **No defer-list elaborate compatibility machinery.** Other skills' triggers work normally. If the user invokes `/project-audit` mid-build, audit runs and returns; build-page picks back up in the next message. The agent is responsible for staying oriented across that — same as it would for any other skill.

## Save-session interaction

When the user types "save" or "save session" mid-build:

1. **Append the current-state line to WORKLOG**: `[HH:MM] decided: build-page suspended for /<slug> at <state> — N of M sections complete`. Where `<state>` is one of `plan-pending`, `plan-locked`, `section-<n>-deciding`, `section-<n>-building`, `wiring`, or `done`.
2. **Let `save-session` run normally.** It will categorize WORKLOG, append to CHANGELOG, update STATUS, append to BRIEF, clear WORKLOG, commit+push.
3. **`save-session` will see the suspension line and write a STATUS Next Actions entry**:
   ```
   [ ] Resume /build-page <slug> — suspended at <state> (<date>)
   ```
4. **Next session**: the user invokes `/build-page <slug>` again. This skill reads canon + STATUS + the previous BRIEF block(s) + the new WORKLOG (now cleared). The agent surfaces *"Resuming build-page for /<slug>. Per BRIEF v1.X you locked plan with N sections. The last suspension was at <state>. Want to pick up there?"* and continues.

This is the same pattern every other long-running skill uses. There is no special "resume protocol" — it's just reading the canon and behaving sensibly.

## When other skills get invoked mid-conversation

If the user types something that fires another skill (`/discuss`, `/project-audit`, `/save`, `/recap`):

- That skill runs.
- It returns control.
- The next user message is interpreted as continuing build-page (because the WORKLOG shows it's open and no completion entry exists).
- If the user wants to abandon build-page, they say so explicitly — *"abandon build-page"* or *"never mind the page build"*. The agent appends `[HH:MM] decided: build-page abandoned for /<slug>` and exits.

Do not declare a "lock" on other skills. They work normally. The agent's responsibility is to stay oriented.
