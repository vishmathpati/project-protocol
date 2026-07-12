---
name: discuss
description: No-edit conversation mode for evaluating options, trade-offs, architecture, or direction before implementation. Use when the user says discuss, brainstorm, explore, or asks what you think.
allowed-tools: Read, Glob, Grep
---

# Discuss

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

**4. Bring expertise.** Compare options with live project sources, identify gaps, and recommend the strongest option. The user makes the final decision.

**5. Exit mode** only when the user explicitly signals execution: "do it", "go ahead", "implement", "let's build it", "make the change". Then the `change-check` skill takes over for the actual action.

---

## What this prevents

- Drafting a 500-line file when the user asked "what do you think about X".
- Running `init-project` when the user said "let's discuss the layout".
- Committing recommendations as edits when the user wanted to weigh options.

---

## Why it exists

Agents default to production mode — they want to be helpful, which often means doing work. But thinking together is its own work. This skill protects thinking time from production-mode reflexes.
