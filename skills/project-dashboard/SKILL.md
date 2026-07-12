---
name: project-dashboard
description: Generate or check one deterministic human-readable HTML dashboard from Project Protocol Markdown canon and local research assets. Use when the user wants the project report, brand overview, design preview, research/moodboard, or build progress in one page. The HTML is derived output, never a second source of truth.
---

# Project Dashboard

Render canon; never reinterpret or edit it.

## Generate

Resolve the installed plugin root from `CODEX_PLUGIN_ROOT` or `CLAUDE_PLUGIN_ROOT`, then run `python3 <plugin-root>/skills/project-dashboard/scripts/generate_dashboard.py <project-root>`. Default output is `brain/project-dashboard.html` with relative local assets. It contains Project, Brand, Design, Research/Moodboard, and Build Progress tabs.

The generator reads available canon conditionally. Missing optional files become explicit empty states. Markdown remains authoritative. Page-specific research choices remain in chapters; there is no global selected-decisions tab.

Use `--portable` only when the user explicitly requests one embedded private HTML file. It base64-embeds supported local images and may become large. Never embed remote images or assume redistribution rights.

## Check freshness

Run with `--check`. The generator compares current input hashes with hashes embedded in the existing dashboard and exits nonzero when stale. Regenerate explicitly; hooks and Save Session do not regenerate it automatically.

## Rules

- Do not write Markdown canon.
- Do not invent status, decisions, tokens, routes, or research conclusions.
- Screenshots are local/gitignored by default.
- Generated HTML may be ignored or committed according to project policy.
- Report output path, mode, inputs used, missing optional sources, and freshness.
