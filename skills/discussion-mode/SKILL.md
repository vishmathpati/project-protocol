---
name: discussion-mode
description: >
  No-edit conversation mode. Activate when the user signals they want to think,
  discuss, or explore rather than execute — phrases like "discuss", "let's
  talk", "I want to chat", "what do you think", "your opinion", "brainstorm",
  "explore". Prevents file edits, premature artifact production, and unsolicited
  recommendations during what should be a thinking session.
allowed-tools: Read, Glob, Grep
---

# Discussion Mode

Pure conversation. No file edits. No premature production.

---

## When this fires

User signals via phrases like:
- "discuss this", "let's talk about", "I want to chat"
- "what do you think", "your opinion", "your take"
- "brainstorm", "explore", "think through"
- "before we do anything..."
- Slash command: `/discuss`

---

## The protocol

**1. Acknowledge mode.** Tell the user explicitly: "Discussion mode. No file edits until you say 'do it' or equivalent."

**2. Read-only operation.** Only Read, Glob, Grep tools allowed during this skill's lifetime. No Write, no Edit, no spawning of execution sub-agents.

**3. Provide analysis, not artifacts.** If the user asks for thinking — give thinking. Don't draft files, don't generate code, don't write documentation. Just talk.

**4. Surface trade-offs, not decisions.** Lay out options and their consequences. Let the user pick. Don't pick for them.

**5. Exit mode** only when the user explicitly signals execution: "do it", "go ahead", "implement", "let's build it", "make the change". Then the `discipline` skill takes over for the actual action.

---

## What this prevents

- Drafting a 500-line file when the user asked "what do you think about X".
- Running `init-project` when the user said "let's discuss the layout".
- Committing recommendations as edits when the user wanted to weigh options.

---

## Why it exists

Agents default to production mode — they want to be helpful, which often means doing work. But thinking together is its own work. This skill protects thinking time from production-mode reflexes.
