---
name: grill
description: A relentless one-question-at-a-time interview that sharpens a chapter's Goal + Plan BEFORE any building starts — walk the decision tree branch by branch, resolve dependencies between decisions, recommend an answer for each, and explore the codebase instead of asking whenever the answer is discoverable. Reads brain/WONT-DO.md first so it never re-proposes something already rejected, then writes the sharpened goal + plan into the chapter file. The /ceo and /solo roles call this during chapter planning. Triggers — "grill me", "sharpen this goal", "pressure-test this plan", "interrogate the requirements", "what am I not thinking about", "before we build this", "scope this chapter".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*, cat:*, date:*, wc:*, git:*)
---

# Grill — Project Protocol

A relentless interview that sharpens a chapter's **Goal** before a single line gets built. Vague goals are the most expensive thing in the protocol — they get delegated, half-built, and bounced. Grill front-loads the thinking: walk every branch of the decision tree, resolve the dependencies between decisions, and land on a goal + plan tight enough that a worker can execute it and the CEO can verify it.

This runs during **CEO / solo chapter planning** — before `/ceo` writes the chapter and delegates, or before `/solo` starts a small job worth pinning down. The user can also invoke it directly by saying "grill me."

There is ONE canon: `brain/`. This skill reads canon and writes only the chapter file's Goal / Plan sections.

---

## Step 0 — Read WONT-DO first

Read `brain/WONT-DO.md` before asking anything. It is the list of paths already rejected — directions, features, and approaches the project has deliberately ruled out. **Never re-propose anything on it.** If the user steers toward a rejected path mid-interview, name the prior rejection and ask whether they're truly reopening it, rather than quietly walking back in.

Skim just enough of the rest of canon to ground the questions — `brain/BRIEF.md` (locked decisions), `brain/STATUS.md` (where things stand), `brain/ROADMAP.md` (what's planned). Don't read the whole project; read what makes your questions sharp.

---

## Step 1 — Map the decision tree

Lay out, for yourself, the branches that have to be resolved before this goal is buildable: the core decision, the sub-decisions it forks into, and the dependencies between them (decision B only matters if decision A went one way). You don't show the user the whole tree — you walk it.

---

## Step 2 — Explore before you ask

For every open question, ask: **can the codebase answer this?** If the answer is discoverable — an existing pattern, a current config, how a thing is already wired — go read it instead of asking. Use Read / Glob / Grep. Only questions that genuinely require the user's intent, taste, or priority should ever reach them. Spending the user's attention on something you could have looked up is a failure.

---

## Step 3 — Interview, ONE question at a time

Walk down each branch of the decision tree, in dependency order, asking exactly **one question at a time**. For each question:

- **Give your recommended answer** and a one-line why. Make it easy to just say "yes."
- Keep it concrete and decision-shaped — not "what do you want?" but "A or B; I'd pick A because …"
- Let the answer steer which branch you walk next; resolving one decision often prunes or reshapes the others.

Do **not** batch questions. One at a time keeps each answer crisp and lets each answer redirect the next question. There is **no fixed question cap** — keep going until the tree is resolved.

---

## Step 4 — Keep going until every branch is resolved

You're done when there are no unresolved branches left — every fork has an answer, every dependency is settled, and nothing material is still hand-wavy. If the user tries to stop early while a load-bearing decision is still open, say which decision is still unresolved and why it matters before you let it go.

---

## Step 5 — Pick the execution method

Now that the goal and scope are clear, choose how this chapter will be executed. Pick **one** of the three methods based on the chapter's size and nature:

- **solo** — small and self-contained; one tool/session does both planning and the work. Use when the chapter is bounded, low-risk, and doesn't need a separate worktree.
- **CEO + worker** — one specialist worker executes the chapter in a dedicated worktree. Use for most delegated chapters: clear goal, single discipline, reviewable in one pass.
- **CEO + specialists** — a large chapter that naturally spans multiple specialist passes (e.g. backend → UI → wire-up), each appending its own Completion Report. Use when the chapter has hard seams between disciplines or when parallel passes are the only sane way to scope it.

State your recommended method and give a one-line reason. Confirm with the user (a quick "yes" is fine). Record the chosen method in the chapter file's **Method** field (see Step 6).

---

## Step 6 — Write the sharpened goal + plan into the chapter

Write the result into the chapter file `brain/chapters/NN-name.md` — fill the **Goal**, **Method**, and **Plan** sections (creating them if the chapter is fresh):

- **Goal** — one tight paragraph of what "done" means: concrete, verifiable, reflecting every decision just made.
- **Method** — one of `solo` | `CEO+worker` | `CEO+specialists`, as chosen in Step 5.
- **Plan** — the ordered steps, now unambiguous because the branches are resolved. For `CEO+specialists`, note the specialist passes in order.

If decisions surfaced new things the project should explicitly NOT do, note them so the CEO can fold them into `brain/WONT-DO.md` (you sharpen the chapter; the CEO owns the shared canon). Hand back to whoever invoked you — `/ceo` to delegate, `/solo` to execute.

---

## Rules

- WONT-DO.md first, always — never re-propose a rejected path.
- One question at a time, each with a recommended answer. Never batch.
- If the codebase can answer it, explore — don't ask.
- No question cap; stop only when every branch of the tree is resolved.
- You write only the chapter's Goal / Method / Plan. Shared canon (BRIEF / STATUS / WONT-DO) stays the CEO's.
