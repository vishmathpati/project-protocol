---
name: handoff
description: Mid-task continuity for a long-running session — captures a context carry-over note so the next session can pick up where this one left off. Distinct from the worker→CEO Completion Report and from Codex's built-in "Handoff". Any role uses it when a session runs long or context fills up. Triggers — "context is filling up", "running low on context", "carry over", "hand off to the next session", "write a continuation note", "pick this up later", "I'm about to run out of room", "save state to continue".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*)
---

# Handoff — Project Protocol

> **Not** Codex's built-in **"Handoff"** (which moves a thread between **Local** and **Worktree**). This skill is a **context carry-over note**: one session handing off to its OWN continuation when the context window is filling up.
>
> Also **not** the worker→CEO **Completion Report** — that's a finished chapter handed to a different role for verification. This is mid-task, same work, next session.

When a session is running long and context is filling, write a small note so the next session can resume without re-deriving where things stood. Any role (`/ceo`, `/worker`, `/solo`) can invoke it.

There is ONE canon: `brain/`. The carry-over lives on the active chapter file (or a scratch note if there's no chapter).

---

## Step 0 — Author stamp

- `CLAUDE_PLUGIN_ROOT` set → stamp `· Claude Code`
- `CODEX_PLUGIN_ROOT` set → stamp `· Codex`
- neither set → stamp `· Cowork`

---

## Step 1 — Write the Carry-over note

Short and operational — enough for the next session to resume cold, no more. Cover:

- **Where we are** — the current state in one or two lines.
- **What's done** — what's actually finished and verified this session.
- **What's next** — the immediate next action(s), in order.
- **Open threads / decisions pending** — anything unresolved, any decision still owed, any half-explored idea worth not losing.

**Redact secrets.** No API keys, passwords, tokens, or PII in the note — replace with a placeholder (`<API_KEY redacted>`) and say where the real value lives if needed.

**Don't duplicate the canon.** If something is already captured in canon, a report, or the chapter's Goal/Plan, **reference it by path** rather than re-writing it. The carry-over is the delta — what's in your head that isn't yet on disk.

---

## Step 2 — Append it to the ACTIVE chapter

Append the note as a **`## Carry-over`** section to the active chapter file `brain/chapters/NN-name.md`, so the next session reads the chapter + carry-over together as one continuous record:

```markdown
## Carry-over — YYYY-MM-DD [author stamp]

**Where we are** — …

**What's done** — …

**What's next** —
- …

**Open threads / decisions pending** —
- …
```

If there have been earlier carry-overs on this chapter, add a new dated section rather than overwriting — the trail of carry-overs is itself useful.

**No chapter for this work?** Write the same note to a scratch note instead — e.g. `brain/carry-over-YYYY-MM-DD.md` — and **tell the user the exact path** so the next session knows where to look.

---

## Step 3 — Tell the user how to resume

Point the next session at the note in one line, e.g.:

```
Carry-over written to brain/chapters/NN-name.md (## Carry-over). Next session: read that chapter + carry-over to resume.
```

If this session can commit, fold the carry-over into the normal commit; if running in Cowork (no push), commit locally and emit the push command per the git skill. The carry-over is a note, not a Completion Report — it does not close the chapter.

---

## Rules

- This is a context carry-over note — distinct from Codex's built-in Local↔Worktree "Handoff" and from the worker→CEO Completion Report.
- Keep it short and operational: where / done / next / open threads.
- Redact secrets — never write keys, passwords, or PII into the note.
- Reference canon by path instead of duplicating it; the note is only the delta.
- Append as `## Carry-over` to the active chapter (or a scratch note + tell the user the path when there's no chapter).
