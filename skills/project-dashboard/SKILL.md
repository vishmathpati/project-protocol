---
name: project-dashboard
description: Generate, serve, or check the human-readable Project Dashboard from Project Protocol canon, page-aware UI Research recommendations, and local evidence. Use for project/brand/design summaries, research and moodboard review, site-wide page/family decisions, provisional decision submission, or build progress. HTML and submitted JSON remain derived/provisional, never a second Markdown canon.
---

# Project Dashboard

Summarize and visualize canon for human decisions; never reinterpret or edit Markdown. The dashboard is not a Markdown reader or an automatic selector.

## Generate

Resolve the installed plugin root from `CODEX_PLUGIN_ROOT` or `CLAUDE_PLUGIN_ROOT`, then run `python3 <plugin-root>/skills/project-dashboard/scripts/generate_dashboard.py <project-root>`. Default output is `brain/project-dashboard.html` with relative local assets. It contains Project, Brand, Design, Research/Moodboard, and Build Progress tabs.

The generator reads available canon conditionally. Missing optional files become explicit empty states. Markdown remains authoritative. Project, Brand, Design, and Build views show bounded summaries and visual specimens, never full-file dumps.

When UI Research produced `brain/research/page-recommendations.json`, the Research / Moodboard checkpoint must also:

- use the exact active checkout/worktree packet; never borrow a main-checkout packet;
- show a compact site-wide direction and global-shell review before page/family tabs;
- merge repeated routes by the supplied page family while preserving unique/special/utility/legal targets;
- show a compact content-job page map and label each option as Whole page, Connected sections, One section, Repeated page family, or Global shell;
- use the decision workspace layout: the page goal and rough content structure stay visible on the left while one large evidence-backed recommendation appears on the right;
- order each page or family from its whole-page/page-family direction to connected sequences and only then optional section refinements; a refinement never substitutes for the base direction;
- show one recommendation at a time with large local evidence, exact live URLs, image/video/motion classification, fit, alternatives, dependencies, confidence, gaps, and asset requirements;
- treat a linked hero/header as a proposal only. The header remains pending until reviewed under Global Shell;
- let the human mark Recommended, Accept, Shortlist, or Not using; optionally keep/change exact affected parts; request focused research in plain language; bring an exact live reference plus the exact part liked; or record **I’ll bring my own component later** for that exact page/section. The last option records a deferred intent only: do not ask for it during dashboard review. Research compatibility is evidence; the browser never manufactures the agent's final compatibility verdict.

The broader concept/site evidence must still:

- show one concept at a time with its feeling, hero, navigation, rhythm, imagery/motion, strengths, risks, project fit, and representative sites when present;
- show one site at a time with large evidence grouped under that site, capture-quality labels, and a live-site link when canon contains its URL;
- distinguish live captures, media fallbacks, invalid captures, and video-led evidence;
- never treat a captured video frame as proof of an image-led concept;
- provide browser-local review notes only as a review aid, clearly stating that they are not canon.

Local video files may render with explicit controls, muted/playsinline, and metadata preload. Remote video must remain a poster/frame plus an official live/provider link unless the project records an owned/licensed embeddable source. Never autoplay research evidence.

## Submit provisional decisions

For real state sharing between the browser and Claude or Codex, start the loopback server:

```bash
python3 <plugin-root>/skills/project-dashboard/scripts/serve_dashboard.py <project-root> --port 3000
```

Open and report the printed tokenized `dashboard_url`, plus the exact resolved root, branch/HEAD, and packet path. The plain base URL is not an authenticated dashboard link. The server binds only to `127.0.0.1`, uses a per-run token and same-origin writes, serves only safe worktree-local evidence, and serializes Submit/Update for that checkout. If port 3000 is occupied, report the blocker and choose an explicit free port.

Candidate clicks remain browser-local. Only the universal **Submit decisions** or **Update decisions** action writes `brain/research/ui-decision-draft.json`. The server validates and atomically replaces it, increments its revision, forces `canonical: false`, resets agent review to pending, and keeps all builds locked.

Read `references/decision-packet.md` before ingesting or changing the submitted packet. Claude/Codex reads the packet, checks the complete site for compatibility, discusses adaptations/conflicts with the human, and only after final approval records the result in the existing Markdown owners. The browser never writes Markdown, declares compatibility, locks canon, or enables Build Page.

In static `file://` mode, browser choices cannot write a project file. Use **Export JSON** or **Copy relay** for the human-choice relay, then have Claude or Codex validate it against this active checkout's exact recommendation packet and normalize the server-authored identity/submission/review fields. Static output intentionally carries no path, Git, revision, approval, or build-gate authority; it is not byte-identical to a persisted server packet. Never claim static HTML is synchronized.

Use `--portable` only when the user explicitly requests one embedded private HTML file. It base64-embeds supported local images and may become large. Never embed remote images or assume redistribution rights.

## Check freshness

Run with `--check`. The generator compares current input hashes with hashes embedded in the existing dashboard and exits nonzero when stale. Regenerate explicitly; hooks and Save Session do not regenerate it automatically.

## Rules

- Do not write Markdown canon.
- Do not commit or treat `ui-decision-draft.json` as approved canon.
- Do not invent status, decisions, tokens, routes, or research conclusions.
- Do not mirror complete Markdown files or flatten all research media into one gallery.
- Screenshots are local/gitignored by default.
- Generated HTML may be ignored or committed according to project policy.
- Regeneration may replace HTML but must preserve `ui-decision-draft.json`.
- Report output path, mode, active checkout/worktree, packet state/revision, inputs used, missing optional sources, and freshness.
