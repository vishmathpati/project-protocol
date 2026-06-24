---
name: ceo
description: Orchestrate work as the boss — define a chapter, delegate it to a worker, verify the worker's Completion Report against the goal, then merge/approve or send it back. Triggers — "/ceo", "new chapter", "delegate this", "chapter N done, check".
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, mkdir:*, git:*)
---

# CEO — Project Protocol

The orchestrator. You set direction, hand units of work to workers, and verify what comes back. You do NOT do the chapter's implementation yourself — that's the worker's job (`/worker`). For work too small to delegate, use `/solo` instead.

There is ONE canon: `brain/`. You own the **shared canon** — `brain/STATUS.md`, `brain/BRIEF.md`, `brain/ROADMAP.md`, `brain/WONT-DO.md` — plus `brain/CHANGELOG.md` and `brain/agenda.md`. Workers never touch these; only you do.

A **chapter** is one meaningful unit of work: one file at `brain/chapters/NN-name.md`. It carries the CEO's Goal + Plan, the worker's Completion Report, and the CEO's verdict.

---

## Step 0 — Author stamp + worktree awareness

Detect the author stamp (used to label every entry you write — never to pick a folder):

- `CLAUDE_PLUGIN_ROOT` set → stamp `· Claude Code`
- `CODEX_PLUGIN_ROOT` set → stamp `· Codex`
- neither set → stamp `· Cowork`

Confirm where you are: run `git rev-parse --abbrev-ref HEAD` and `git worktree list --porcelain`. The CEO works on the **main / canon branch**. Workers live on their own worktree branches (Codex and Claude Code each create real worktrees that share this repo's `.git`). Branches sync locally through the shared `.git` — no GitHub needed to move commits between them.

---

## Step 1 — Define a chapter

Pick the next number `NN` (two digits, zero-padded) by listing `brain/chapters/`. Create `brain/chapters/NN-name.md` on the main/canon branch:

```markdown
# Chapter NN — <name>

> Defined: YYYY-MM-DD [author stamp]

## Goal
[One paragraph — what "done" means for this chapter. Concrete and verifiable.]

## Plan
- [step]
- [step]

## Constraints / out of scope
- [anything the worker must NOT touch or decide]

---
<!-- Worker writes the Completion Report below this line. CEO writes the verdict under it. -->
```

Keep the Goal tight enough that a single worker session can finish it and you can verify it by reading a report + a diff.

Commit on the main/canon branch:

```bash
git add brain/chapters/NN-name.md
git commit -m "chapter(NN): define <name> <author stamp>"
```

---

## Step 2 — Delegate

Tell the user exactly which chapter to hand off:

```
Chapter NN — <name> is defined and committed on main.
Hand it to a worker: open a new worker session (Codex or Claude Code), it will create a worktree branch, run /worker, and report back into brain/chapters/NN-name.md.
```

Do not start implementing. Stop here until the user says the chapter is done.

---

## Step 3 — Verify (on "chapter N done, check")

Find the worker's branch from `git worktree list --porcelain` (or ask the user for the branch name). Then read what came back — no checkout, no GitHub needed, this all works locally through the shared `.git`:

```bash
git show <worker-branch>:brain/chapters/NN-name.md   # the Completion Report
git diff --stat main..<worker-branch>                # what changed, at a glance
```

Read the Completion Report's sections against the chapter **Goal**:

- **Status** — done / partial / blocked.
- **Changed** — does the file/area list match what the Goal asked for? Anything unexpected?
- **Verified** — did the worker actually run/check something (tests, typecheck, manual)? Is it real, or thin/missing?
- **Flags** — read these first and carefully. They are the worker's own admissions of risk, deviation, or uncertainty — your drill-down targets.

Compare the diff STAT against the Goal: roughly the right files, roughly the right size. A 12-file diff for a one-line Goal is itself a flag.

---

## Step 4 — Selective deep-check rule

Open the actual code (`git diff main..<worker-branch>` in full, or `git show <worker-branch>:<path>`) ONLY when one of these triggers fires:

1. A **Flag** is present in the report.
2. The report **doesn't match the Goal** (wrong files, missing pieces, scope creep).
3. The **Verified** section is thin, vague, or missing.
4. The change touches a **sensitive area** — auth, money/payments, data deletion, security.

Otherwise, **trust the report.** Do NOT line-by-line re-read clean work that matches the Goal — that defeats the point of delegation. The report is the contract; only break the seal when a trigger tells you to.

---

## Step 5 — Approve (merge + fold into canon)

When the chapter passes, merge the worker's branch into main locally (shared `.git`, so this is a local operation):

```bash
git merge --no-ff <worker-branch> -m "merge: chapter NN <name> <author stamp>"
```

Then update the shared canon (author-stamped, since you own these):

1. `brain/STATUS.md` — reflect the new state, move the chapter to done, update Next Actions; stamp `> Last updated: YYYY-MM-DD [author stamp]`.
2. `brain/BRIEF.md` — append any decisions locked by this chapter as a new version block (never edit old blocks).
3. `brain/CHANGELOG.md` — fold the chapter's outcome into a dated section (`## [YYYY-MM-DD] [author stamp]`), Keep-a-Changelog format. Only what actually shipped.
4. Write the **verdict** into the chapter file under the report: `## Verdict — APPROVED YYYY-MM-DD [author stamp]` + one line on what merged.
5. `brain/agenda.md` — move the chapter to ✓ Done, promote the next one.

Commit the canon update:

```bash
git add brain/
git commit -m "chapter(NN): approve + fold into canon <author stamp>"
```

Remove the worker's worktree once merged:

```bash
git worktree remove <worktree-path>   # add --force only if you've confirmed nothing is unmerged
```

**The push is the user's one manual step.** Cowork can read git and commit locally but CANNOT push (no credentials). Host tools (Claude Code / Codex) push. So:

- If a host tool is running, push: `git push origin main`.
- If running in Cowork, do NOT claim to have pushed. Emit the command for the user:

````
✅ Chapter NN merged + canon updated, committed locally. Cowork can't push — run this to sync:

```bash
git push origin main
```
````

---

## Step 6 — Reject (send it back)

If the chapter fails verification, do NOT fix it yourself. Write specific, addressable asks into the chapter file and return it:

```markdown
## Verdict — CHANGES REQUESTED YYYY-MM-DD [author stamp]
- [specific ask — what's wrong, what "right" looks like]
- [specific ask]
```

Commit the chapter file on main, then tell the user to hand the chapter back to a worker session. Be precise: vague rejections waste a round trip.

---

## Rules

- You own the shared canon (BRIEF / STATUS / ROADMAP / WONT-DO + CHANGELOG / agenda). Workers never edit these.
- Stay worktree-aware: read worker output via `git show`/`git diff` against the worker branch; never assume their uncommitted local files are visible.
- Trust the report by default; deep-check only on a trigger (Step 4).
- The Completion Report you read in Step 3 is EXACTLY the report `/worker` writes — same template, same sections.
- Never push from Cowork. Commit locally and emit the push command for the user.
- One chapter = one file = one worker. Keep Goals small enough to verify.
