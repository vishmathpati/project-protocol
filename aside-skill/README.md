# aside-skill/ — standalone skills for the Aside browser

These are **not** Claude Code / Codex skills. They are standalone skills you upload **into the
Aside browser** (aside.com). The project-protocol plugin **ships, versions, and updates** them —
but they run inside Aside, driven by a per-project prompt the plugin generates.

Why they live here (and not under `skills/`): the plugin loads `skills/` as its own agent skills.
An Aside skill must NOT be loaded as a plugin skill — it belongs to a different runtime. Keeping it
in `aside-skill/` means the plugin can manage and version it without Claude Code ever trying to run
it.

## Skills

| Skill | Upload into Aside | Driven by | Purpose |
|-------|-------------------|-----------|---------|
| `design-research/SKILL.md` | once (re-upload on version bump) | `calibrate` (plugin) generates the mission prompt per project | Two-round design research: SWEEP a niche into named concepts → human picks/blends → DEEP TEARDOWN of the chosen concept's best real sites. |

## How it's used (the loop)

1. **One-time:** upload `design-research/SKILL.md` into your Aside skills.
2. **Per project:** the plugin's `calibrate` skill fills the mission prompt from the project's canon
   (niche, register, refusals, depth) and hands it to you.
3. You paste the prompt into your Aside `design-research` chat; Aside researches and prints a
   summary block.
4. You paste the summary back into the plugin session; you pick/blend a concept; the plugin
   generates the Round-2 directive; you paste that into the **same** Aside chat.
5. Aside tears down the chosen concept; you paste the final summary back; the plugin folds it into
   canon.

The plugin side of this loop is `skills/calibrate/` (`SKILL.md` + `references/mission-prompt-template.md`
+ `references/round-formats.md`). This folder is only the Aside half.

## Versioning

This skill's version tracks the plugin version. When `CHANGELOG.md` records a change to the Aside
`design-research` skill, re-upload the updated `SKILL.md` into Aside so the two stay in sync.
