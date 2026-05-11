---
name: verify-by-reading
description: >
  Read-before-answer enforcement. Use before answering any question about file
  content, project state, decisions, or recommendations that reference specific
  files. Forces opening the actual file rather than relying on conversational
  memory or recall. Catches "memory drift" — when an agent answers from prior
  context instead of current file state.
allowed-tools: Read, Glob, Grep
---

# Verify by Reading

When answering anything specific, open the file. Don't trust memory.

---

## When this fires

- About to make a claim that references a specific file, decision, or fact.
- About to recommend an action based on what a file "says".
- About to answer "what does X file contain" or "what did we decide about Y".
- Slash command: `/verify` or `/read-first`

---

## The protocol

**1. Identify the file(s)** the answer references.

**2. Open the file** with the Read tool. Do not skip — even if you "remember" it.

**3. Quote specifics.** In the answer, quote the actual lines or section names from the file. Not paraphrased from memory — quoted from the file.

**4. Flag staleness.** If your memory and the file disagree, trust the file. Say so openly: "Memory said X, file says Y — going with the file."

**5. Delegate deep reads.** For large reference files (anything in `docs/detail/` or `docs/reference/`, or any file over ~500 lines), spawn a sub-agent to read it and return findings rather than loading the whole file into your main context.

---

## Anti-patterns

- "From what I remember, the file says..." — wrong move. Open it.
- "Earlier we discussed X in this file" — confirm by opening.
- "The function name is `doFoo`" — grep before stating.

Every specific claim is a hypothesis until the file confirms it.

---

## Why it exists

LLM agents default to recall when answering. Recall drifts — even within a single session, the model's representation of a file's content can diverge from what the file actually says. Opening the file is cheap. Drift is expensive.
