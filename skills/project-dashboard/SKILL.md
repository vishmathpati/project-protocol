---
name: project-dashboard
description: Generate or check one deterministic human-readable HTML dashboard from Project Protocol Markdown canon and local research assets. Use when the user wants the project report, brand overview, design preview, research/moodboard, or build progress in one page. The HTML is derived output, never a second source of truth.
---

# Project Dashboard

Summarize and visualize canon for human decisions; never reinterpret or edit it. The dashboard is not a Markdown reader.

## Generate

Resolve the installed plugin root from `CODEX_PLUGIN_ROOT` or `CLAUDE_PLUGIN_ROOT`, then run `python3 <plugin-root>/skills/project-dashboard/scripts/generate_dashboard.py <project-root>`. Default output is `brain/project-dashboard.html` with relative local assets. It contains Project, Brand, Design, Research/Moodboard, and Build Progress tabs.

The generator reads available canon conditionally. Missing optional files become explicit empty states. Markdown remains authoritative. Project, Brand, Design, and Build views show bounded summaries and visual specimens, never full-file dumps.

The Research / Moodboard checkpoint must:

- show one concept at a time with its feeling, hero, navigation, rhythm, imagery/motion, strengths, risks, project fit, and representative sites when present;
- show one site at a time with large evidence grouped under that site, capture-quality labels, and a live-site link when canon contains its URL;
- distinguish live captures, media fallbacks, invalid captures, and video-led evidence;
- never treat a captured video frame as proof of an image-led concept;
- provide browser-local Keep/Maybe/Blend/Reject notes only as a review aid, clearly stating that they are not canon.

Local video files may render with explicit controls, muted/playsinline, and metadata preload. Remote video must remain a poster/frame plus an official live/provider link unless the project records an owned/licensed embeddable source. Never autoplay research evidence.

Page-specific research choices remain in chapters; there is no global selected-decisions tab. Final selection is relayed to UI Research, which writes the canonical `## Human selection` block. The dashboard never edits Markdown.

Use `--portable` only when the user explicitly requests one embedded private HTML file. It base64-embeds supported local images and may become large. Never embed remote images or assume redistribution rights.

## Check freshness

Run with `--check`. The generator compares current input hashes with hashes embedded in the existing dashboard and exits nonzero when stale. Regenerate explicitly; hooks and Save Session do not regenerate it automatically.

## Rules

- Do not write Markdown canon.
- Do not invent status, decisions, tokens, routes, or research conclusions.
- Do not mirror complete Markdown files or flatten all research media into one gallery.
- Screenshots are local/gitignored by default.
- Generated HTML may be ignored or committed according to project policy.
- Report output path, mode, inputs used, missing optional sources, and freshness.
