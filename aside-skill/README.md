# Aside skills

Standalone browser skills uploaded into Aside, not loaded as Claude Code/Codex plugin skills.

| Aside skill | Project Protocol driver | Purpose |
|---|---|---|
| `ui-research/SKILL.md` | `ui-research` | Map site-wide and page-family recommendations, then deeply inspect only approved targets or run a focused pattern follow-up. |
| `inspect-component/SKILL.md` | `inspect-component` | Investigate one exact external UI region and return implementation evidence. |

Upload each skill once and re-upload when its interface changes. Project Protocol supplies project-specific
missions and ingests Markdown evidence plus the versioned `page-recommendations.json` relay in the active
checkout. Aside preserves stable page, recommendation, and evidence IDs and always prints the same packet
for paste fallback. Aside does not write dashboard selections, human approvals, build locks, or implementation
code. A known URL whose exact region needs implementation forensics belongs to `inspect-component`.
