---
name: save-session
description: >
  Save and close a Claude Code or Codex project session. Use whenever the session is ending —
  triggered by "save", "save session", "close session", "end session", "done for today",
  or "lock session". Reads WORKLOG.md, appends to CHANGELOG.md, updates STATUS.md,
  signs BRIEF.md if decisions were made, and clears WORKLOG.md.
  Works for any project following the standard project protocol.
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*,date:*,wc:*)
---

# Save Session — Project Protocol

Closes out the current coding session cleanly. Works for any project that follows
the standard protocol (CLAUDE.md, STATUS.md, WORKLOG.md, CHANGELOG.md, BRIEF.md).

---

## Step 1 — Read WORKLOG.md

Read `WORKLOG.md` from the project root. This is your real-time log of what happened.
If WORKLOG.md is empty or missing, reconstruct from memory of this session.

---

## Step 2 — Update CHANGELOG.md

Read WORKLOG.md entries and categorize them into Keep a Changelog format.
If `CHANGELOG.md` does not exist, create it with the header below first.

**Mapping WORKLOG entries to changelog categories:**
- `fixed:` entries → `### Fixed`
- `decided:` entries about new capabilities → `### Added`
- `decided:` entries about changes to existing features → `### Changed`
- `tried_failed:` entries → **excluded** (internal working notes, not shipped)
- `found_bug:` entries → **excluded** unless fixed this session (then → `### Fixed`)

**Only include entries for things that actually shipped.**

Append a new dated section to `CHANGELOG.md` at the top (below the header):

```markdown
## [YYYY-MM-DD] · Claude Code

### Added
- [new feature or capability shipped this session]

### Changed
- [modification to existing feature]

### Fixed
- [bug that was resolved]

### Removed
- [anything deliberately deleted]
```

Include agent label (`· Claude Code` or `· Codex`) in the section header.
Omit any section that has no entries. If nothing shipped this session, write:
```markdown
## [YYYY-MM-DD] · Claude Code
- No changes shipped this session.
```

**CHANGELOG.md header (create once, never overwrite):**
```markdown
# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---
```

**CHANGELOG.md is never cleared.** It accumulates for the entire life of the project.

---

## Step 3 — Check docs/INDEX.md was updated

If any feature was added, any page changed, or any shared function was modified this session:
- Verify docs/INDEX.md was updated inline during the session
- If it was NOT updated: add a reminder in STATUS.md Next Actions:
  `[ ] Update docs/INDEX.md — [what changed that needs reflecting]`

Do not update INDEX.md yourself during save-session — that should have happened inline.

---

## Step 4 — Update STATUS.md

Read `STATUS.md`. Apply:
1. Update "Last updated" line to: `> Last updated: YYYY-MM-DD · Claude Code` (or `· Codex`)
2. Add this session's one-line summary to Recent Sessions (rolling — keep last 5, drop oldest)
3. Update Health: add new bugs as 🔴, remove resolved bugs from 🔴
4. Update "Needs CEO Input" section: add any open decisions that need Cowork; clear resolved items
5. Update Next Actions to reflect what's actually next

Rule: STATUS.md must never exceed 60 lines.

---

## Step 5 — Sign BRIEF.md if decisions were made

If any architecture, tech stack, or significant scope decisions were made this session:

Append a new version block to `BRIEF.md`:

```markdown
---

## v1.X — YYYY-MM-DD HH:MM · Claude Code

[describe only the delta — what changed or was decided this session]
[rejected options if any]
```

**Rules:**
- Increment the version number from the last block in BRIEF.md
- Include the exact time (not just date) — run `date +%Y-%m-%d\ %H:%M` if needed
- Only append; never edit existing blocks
- If nothing significant was decided, skip this step entirely
- **500-line limit check:** If BRIEF.md is approaching 500 lines, create `BRIEF-2.md` first, add a pointer at the top of BRIEF.md (`> Continued in BRIEF-2.md`), and append the new block to BRIEF-2.md instead

---

## Step 6 — Update DISCOVERIES.md if needed

If any UI patterns, component integrations, or design decisions proved out this session, append:

```
[YYYY-MM-DD] · Claude Code · [component or pattern name] — what worked and why
```

Examples of what belongs here:
- A shadcn component that integrated cleanly with the existing token system
- A layout pattern that solved a specific spacing problem
- An animation timing that felt right for this product's personality
- A CSS variable combination that produced a specific visual effect

Examples of what does NOT belong here:
- Bug fixes (those go in CHANGELOG.md)
- Architecture decisions (those go in BRIEF.md)
- Session events (those go in WORKLOG.md before it's cleared)

Never clear or reorganize DISCOVERIES.md. Append only.

---

## Step 7 — Clear WORKLOG.md

Replace contents with:

```
# Worklog — cleared after each session.
```

---

## Step 8 — Confirm

```
✅ CHANGELOG.md updated — [N Added, N Changed, N Fixed]
✅ STATUS.md updated · [agent label]
✅ BRIEF.md signed (v1.X) — [Y/N, or "no decisions this session"]
✅ WORKLOG.md cleared.
[X completed, Y bugs, Z decisions]
```

---

## Rules

- Never make up content that wasn't in the session. Only log what actually happened.
- If this session had no changes, still run through the steps — update STATUS.md at minimum.
- CHANGELOG.md is never cleared — only appended to.
- DISCOVERIES.md is never cleared — only appended to.
- BRIEF.md is never overwritten — only appended to.
- Goal: a new session reading STATUS.md + BRIEF.md has 100% context to continue without asking Vish anything.
