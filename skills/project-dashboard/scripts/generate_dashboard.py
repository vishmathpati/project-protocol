#!/usr/bin/env python3
"""Deterministic decision-grade Project Protocol dashboard (stdlib only)."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import os
import re
from pathlib import Path

GROUPS = {
    "Project": ["BRIEF.md", "STATUS.md", "STRUCTURE.md", "ROADMAP.md", "WONT-DO.md"],
    "Brand": ["BRAND.md", "marketing/CONTENT.md", "marketing/SITEMAP.md", "marketing/MEDIA.md"],
    "Design": ["DESIGN.md", "FUNDAMENTALS.md", "TASTE.md", "DISCOVERIES.md"],
}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
VIDEO_EXTS = {".mp4", ".webm", ".mov"}
MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS
HASH_PREFIX = "<!-- project-dashboard-hashes:"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(root: Path) -> list[Path]:
    brain = root / "brain"
    paths: list[Path] = []
    for rels in GROUPS.values():
        paths.extend(brain / rel for rel in rels if (brain / rel).is_file())
    for pattern in ("chapters/*.md", "marketing/briefs/*.md", "marketing/copy/**/*.md", "research/**/*.md", "moodboard/**/*.md"):
        paths.extend(p for p in brain.glob(pattern) if p.is_file())
    if (brain / "moodboard").exists():
        paths.extend(p for p in (brain / "moodboard").rglob("*") if p.is_file() and p.suffix.lower() in MEDIA_EXTS)
    recommendations = brain / "research/page-recommendations.json"
    if recommendations.is_file():
        paths.append(recommendations)
    return sorted(set(paths), key=lambda p: p.relative_to(root).as_posix())


def hashes(root: Path, paths: list[Path]) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): digest(p) for p in paths}


def read_embedded_hashes(output: Path) -> dict[str, str] | None:
    if not output.is_file():
        return None
    match = re.search(r"<!-- project-dashboard-hashes:([A-Za-z0-9_-]+) -->", output.read_text(errors="ignore"))
    if not match:
        return None
    try:
        return json.loads(base64.urlsafe_b64decode(match.group(1) + "===").decode())
    except (ValueError, json.JSONDecodeError):
        return None


def clean_inline(value: str) -> str:
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    return re.sub(r"[*_]+", "", value).strip()


def source_summary(root: Path, path: Path) -> str:
    """Render a bounded digest, never a raw Markdown mirror."""
    text = path.read_text(errors="replace")
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    title = clean_inline(title_match.group(1)) if title_match else path.stem.replace("-", " ").title()
    facts: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", ">", "```", "|---")) or re.match(r"^\|.*\|$", line):
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^\d+[.)]\s+", "", line)
        line = clean_inline(line)
        if len(line) < 3 or line in facts:
            continue
        facts.append(line[:240] + ("…" if len(line) > 240 else ""))
        if len(facts) == 6:
            break
    rel = path.relative_to(root).as_posix()
    items = "".join(f"<li>{html.escape(f)}</li>" for f in facts) or "<li>No concise facts found.</li>"
    return f'<article class="summary-card"><p class="source">{html.escape(rel)}</p><h3>{html.escape(title)}</h3><ul>{items}</ul></article>'


def parse_concepts(path: Path) -> tuple[list[dict[str, str]], dict[str, str]]:
    if not path.is_file():
        return [], {"status": "missing"}
    text = path.read_text(errors="replace")
    selection: dict[str, str] = {"status": "pending"}
    selection_match = re.search(r"^##\s+Human selection\s*$([\s\S]*?)(?=^##\s|\Z)", text, re.M | re.I)
    if selection_match:
        visible_selection = selection_match.group(1).split("<!--", 1)[0]
        for key, value in re.findall(r"^-\s*([^:]+):\s*(.+)$", visible_selection, re.M):
            selection[key.strip().lower()] = clean_inline(value)

    heading = re.compile(r"^#{2,3}\s+Concept\s+([A-Z0-9]+)\s*[:—-]\s*([^\n]+)$", re.M | re.I)
    matches = [m for m in heading.finditer(text) if "human selection" not in m.group(0).lower()]
    concepts: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end():end]
        label = match.group(1) or str(index + 1)
        name = clean_inline(match.group(2))
        fields: dict[str, str] = {"label": label, "name": name}
        aliases = {
            "Feeling": "feeling", "Hero": "hero", "Opening move": "hero", "Navigation": "navigation",
            "Rhythm": "rhythm", "Imagery": "imagery", "Motion": "motion", "Sites": "sites",
            "Evidence": "sites", "Moves": "moves", "Signature": "moves", "Strengths": "strengths",
            "Risks": "risks", "Project fit": "project_fit", "Fit for Singh": "project_fit",
        }
        for key, target in aliases.items():
            found = re.search(rf"^\s*(?:[-*+]\s*)?\**{re.escape(key)}\**\s*:\s*(.+?)\**\s*$", block, re.M | re.I)
            if found:
                fields[target] = clean_inline(found.group(1))
        urls = re.findall(r"https?://[^\s)>]+", block)
        if urls:
            fields["urls"] = " ".join(urls)
        if len(fields) == 2:
            useful = [clean_inline(x) for x in block.splitlines() if x.strip() and not x.lstrip().startswith("#")]
            fields["summary"] = " ".join(useful[:3])[:700]
        concepts.append(fields)
    return concepts, selection


def evidence_key(stem: str) -> str:
    return re.sub(r"-(hero|mid|end|mobile)(?:-media-fallback|-invalid-desktop-capture|-mobile-invalid-desktop-capture)?$", "", stem, flags=re.I)


def teardown_sites(root: Path, paths: list[Path]) -> dict[str, dict[str, object]]:
    sites: dict[str, dict[str, object]] = {}
    for path in paths:
        rel = path.relative_to(root).as_posix()
        if "/research/teardowns/" not in f"/{rel}" or path.suffix.lower() != ".md":
            continue
        text = path.read_text(errors="replace")
        title = re.search(r"^#\s*(?:Teardown\s*[—-]\s*)?(.+)$", text, re.M)
        url = re.search(r"\bURL:\s*(https?://\S+)", text)
        video = re.search(r"(?:##\s+Video evidence|video hero|<video|\.m3u8|\.mp4|Vimeo|Mux)", text, re.I)
        sites[path.stem.lower()] = {
            "name": clean_inline(title.group(1)) if title else path.stem.replace("-", " ").title(),
            "url": url.group(1).rstrip("|,.;") if url else "",
            "video": bool(video),
            "media": [],
        }
    for path in paths:
        if path.suffix.lower() not in MEDIA_EXTS:
            continue
        key = evidence_key(path.stem).lower()
        if key not in sites:
            sites[key] = {"name": key.replace("-", " ").title(), "url": "", "video": path.suffix.lower() in VIDEO_EXTS, "media": []}
        sites[key]["media"].append(path)
    return sites


def media_src(output: Path, path: Path, portable: bool) -> str:
    if portable:
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"
    return Path(os.path.relpath(path, output.parent)).as_posix()


def evidence_status(path: Path) -> tuple[str, str]:
    name = path.name.lower()
    if "invalid" in name:
        return "Invalid capture", "bad"
    if "media-fallback" in name:
        return "Media fallback only", "warn"
    if "mobile" in name:
        return "Mobile evidence", "ok"
    return "Live capture", "ok"


def concepts_html(concepts: list[dict[str, str]], selection: dict[str, str]) -> str:
    status = selection.get("status", "pending")
    selected = status.lower() == "selected"
    selection_text = "Human selection recorded" if selected else "Human selection required before teardown or research-grounded Build Page"
    if not concepts:
        return f'<div class="empty">No synthesized concepts yet. {html.escape(selection_text)}.</div>'
    nav = "".join(f'<button class="concept-jump {"active" if i == 0 else ""}" data-concept="concept-{i}">{html.escape(c.get("label", str(i+1)))} · {html.escape(c["name"])}</button>' for i, c in enumerate(concepts))
    panels = []
    labels = [("feeling", "Feeling"), ("hero", "Hero"), ("navigation", "Navigation"), ("rhythm", "Rhythm"), ("imagery", "Imagery"), ("motion", "Motion"), ("moves", "Signature moves"), ("strengths", "Strengths"), ("risks", "Risks"), ("project_fit", "Project fit"), ("sites", "Representative sites"), ("summary", "Summary")]
    for i, concept in enumerate(concepts):
        facts = "".join(f'<div><dt>{title}</dt><dd>{html.escape(concept[key])}</dd></div>' for key, title in labels if concept.get(key))
        links = "".join(f'<a href="{html.escape(url)}" target="_blank" rel="noreferrer">Open reference ↗</a>' for url in concept.get("urls", "").split())
        panels.append(f'''<article id="concept-{i}" class="concept-panel {"active" if i == 0 else ""}"><p class="eyebrow">Concept {html.escape(concept.get("label", str(i+1)))}</p><h3>{html.escape(concept["name"])}</h3><dl>{facts}</dl><div class="live-links">{links}</div><div class="review" data-review-key="{html.escape(concept.get("label", str(i+1)))}"><span>Private review aid</span>{''.join(f'<button data-verdict="{v}">{v}</button>' for v in ("Keep", "Maybe", "Blend", "Reject"))}<textarea placeholder="What do you like or refuse? Saved only in this browser, never canon."></textarea></div></article>''')
    return f'<div class="selection-status {"selected" if selected else "pending"}"><b>{html.escape(selection_text)}</b><span>Dashboard review notes never write Markdown canon.</span></div><div class="concept-layout"><aside>{nav}</aside><div>{"".join(panels)}</div></div>'


def sites_html(root: Path, output: Path, sites: dict[str, dict[str, object]], portable: bool) -> str:
    useful = [(key, value) for key, value in sites.items() if value.get("media")]
    if not useful:
        return '<div class="empty">No grouped site evidence yet.</div>'
    nav = "".join(f'<button class="site-jump {"active" if i == 0 else ""}" data-site="site-{i}">{html.escape(str(site["name"]))}</button>' for i, (_, site) in enumerate(useful))
    panels = []
    for i, (_, site) in enumerate(useful):
        media = []
        for path in sorted(site["media"], key=lambda p: p.name):
            src = media_src(output, path, portable)
            label, tone = evidence_status(path)
            rel = path.relative_to(root).as_posix()
            if path.suffix.lower() in VIDEO_EXTS:
                item = f'<figure><video controls muted playsinline preload="metadata" src="{html.escape(src)}"></video><figcaption><span class="badge {tone}">{label}</span>{html.escape(rel)}</figcaption></figure>'
            else:
                item = f'<figure><img loading="lazy" src="{html.escape(src)}" alt="Research evidence for {html.escape(str(site["name"]))}"><figcaption><span class="badge {tone}">{label}</span>{html.escape(rel)}</figcaption></figure>'
            media.append(item)
        url = str(site.get("url", ""))
        live = f'<a class="live" href="{html.escape(url)}" target="_blank" rel="noreferrer">Open live site ↗</a>' if url else ""
        video_note = '<span class="badge warn">Video-led evidence — verify motion on live site</span>' if site.get("video") else ""
        panels.append(f'<article id="site-{i}" class="site-panel {"active" if i == 0 else ""}"><header><div><p class="eyebrow">Site evidence</p><h3>{html.escape(str(site["name"]))}</h3></div>{live}</header>{video_note}<div class="evidence-stack">{"".join(media)}</div></article>')
    return f'<div class="site-layout"><aside>{nav}</aside><div>{"".join(panels)}</div></div>'


def load_page_recommendations(root: Path) -> dict[str, object] | None:
    path = root / "brain/research/page-recommendations.json"
    if not path.is_file():
        return None
    try:
        packet = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if packet.get("schema_version") != "project-protocol.page-recommendations.v1":
        return None
    return packet


def scope_label(scope: str) -> str:
    return {
        "whole-page": "Whole page",
        "connected-sections": "Connected sections",
        "one-section": "One section",
        "repeated-page-family": "Repeated page family",
        "global-shell": "Global shell",
    }.get(scope, scope.replace("-", " ").title())


def recommendation_evidence_html(root: Path, output: Path, evidence: list[dict[str, object]], portable: bool) -> str:
    rendered: list[str] = []
    for item in evidence:
        name = html.escape(str(item.get("site") or "Reference"))
        url = str(item.get("live_url") or "")
        live = f'<a class="live" href="{html.escape(url)}" target="_blank" rel="noreferrer">Open live site ↗</a>' if url else ""
        video = item.get("video") if isinstance(item.get("video"), dict) else {}
        video_role = str(video.get("role") or "none")
        video_badge = '<span class="badge warn">Video — verify motion live</span>' if video_role.lower() != "none" else ""
        capture = html.escape(str(item.get("capture_status") or "unknown"))
        media: list[str] = []
        for raw_path in item.get("screenshot_paths", []):
            candidate = Path(str(raw_path))
            path = candidate if candidate.is_absolute() else root / candidate
            try:
                resolved = path.resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                    continue
            except OSError:
                continue
            src = media_src(output, resolved, portable)
            media.append(f'<img loading="lazy" src="{html.escape(src)}" alt="{name} evidence">')
        gallery = "".join(media) or '<div class="evidence-missing">No local visual. Use the live link and evidence notes.</div>'
        motion = item.get("motion") if isinstance(item.get("motion"), dict) else {}
        details = " · ".join(filter(None, [str(item.get("page") or ""), str(item.get("viewport") or ""), capture]))
        rendered.append(f'''<article class="decision-evidence"><header><div><b>{name}</b><p>{html.escape(details)}</p></div>{live}</header>{video_badge}<div class="decision-media">{gallery}</div><p><b>Observed:</b> {html.escape(str(item.get("evidence") or "Not recorded"))}</p><p><b>Motion:</b> {html.escape(str(motion.get("behavior") or "Not observed"))}</p></article>''')
    return "".join(rendered) or '<div class="empty">No visual evidence attached to this recommendation.</div>'


def assets_html(requirements: list[dict[str, object]]) -> str:
    if not requirements:
        return '<p class="muted">No special media or bespoke marks required.</p>'
    rows = []
    for asset in requirements:
        routes = ", ".join(str(value) for value in asset.get("safe_source_routes", []))
        rows.append(f'''<li><b>{html.escape(str(asset.get("kind") or "asset")).title()} · {html.escape(str(asset.get("asset_id") or "unnamed"))}</b><span>{html.escape(str(asset.get("purpose") or ""))} · {html.escape(str(asset.get("quantity") or ""))} · {html.escape(str(asset.get("orientation_or_dimensions") or ""))}</span><small>Responsive: {html.escape(str(asset.get("responsive_need") or "unknown"))} · Poster/fallback: {html.escape(str(asset.get("poster_or_fallback") or "none"))} · Safe sources: {html.escape(routes or "not recorded")}</small></li>''')
    return f'<ul class="asset-list">{"".join(rows)}</ul>'


def decision_actions(recommendation_id: str, scope: str, target_id: str, parts: list[str] | None = None) -> str:
    actions = (
        ("recommended", "Recommended"),
        ("selected", "Accept"),
        ("shortlisted", "Shortlist"),
        ("not_using", "Not using"),
    )
    buttons = "".join(f'<button class="decision-action" data-status="{status}">{label}</button>' for status, label in actions)
    part_buttons = "".join(f'<button class="part-choice" type="button" data-part="{html.escape(part)}" aria-pressed="false">{html.escape(part)}</button>' for part in (parts or []))
    optional_parts = f'<details class="optional-parts"><summary>Optional: keep or change specific parts</summary><div class="part-list">{part_buttons}</div></details>' if part_buttons else ""
    return f'''{optional_parts}<div class="decision-actions" data-recommendation-id="{html.escape(recommendation_id)}" data-scope="{html.escape(scope)}" data-target-id="{html.escape(target_id)}">{buttons}<button class="request-action" type="button" data-request="research">Research another pattern for this part</button><button class="request-action" type="button" data-request="reference">Bring my own reference</button><textarea placeholder="Optional note for Claude or Codex"></textarea><p class="choice-state">No choice recorded.</p></div>'''


def recommendation_card(root: Path, output: Path, recommendation: dict[str, object], target: dict[str, object], portable: bool, active: bool) -> str:
    rid = str(recommendation.get("recommendation_id") or "")
    target_id = str(target.get("target_id") or "")
    scope = str(recommendation.get("scope") or "one-section")
    compatibility = recommendation.get("compatibility_notes") if isinstance(recommendation.get("compatibility_notes"), dict) else {}
    dependencies = [str(value) for value in compatibility.get("dependencies", [])]
    dependency_note = '<p class="dependency-note">Header remains pending. This option may propose a linked header treatment, but never selects it automatically.</p>' if dependencies else ""
    affected_blocks = [str(value) for value in recommendation.get("affected_blocks", [])]
    affected = ", ".join(affected_blocks) or "whole target"
    alternatives = ", ".join(str(value) for value in recommendation.get("alternatives", [])) or "none recorded"
    evidence = recommendation.get("evidence") if isinstance(recommendation.get("evidence"), list) else []
    requirements = recommendation.get("asset_requirements") if isinstance(recommendation.get("asset_requirements"), list) else []
    jobs = [str(value) for value in target.get("content_jobs", [])]
    wireframe = "".join(f'<div class="wire-row"><strong>{html.escape(job)}</strong><small>{"Lead" if index == 0 else "Required"}</small></div>' for index, job in enumerate(jobs)) or '<div class="wire-row"><strong>No content job recorded</strong><small>Open</small></div>'
    if scope in {"whole-page", "repeated-page-family"}:
        level = "Choose this first · Whole-page direction" if scope == "whole-page" else "Choose this first · Repeated page family"
    elif scope == "connected-sections":
        level = "Connected sequence"
    else:
        level = "Optional section refinement"
    connection = f'<div class="connection-note"><strong>Keep this together:</strong> This recommendation affects {html.escape(affected)} as one connected composition.</div>' if scope == "connected-sections" else ""
    confidence = str((recommendation.get("confidence") or {}).get("level", "unknown") if isinstance(recommendation.get("confidence"), dict) else "unknown")
    return f'''<article class="decision-block recommendation-card {"connected " if scope == "connected-sections" else ""}{"page-wide " if scope in {"whole-page", "repeated-page-family"} else ""}{"active" if active else ""}" data-recommendation-panel="{html.escape(rid)}"><div class="brief"><div class="block-number">{html.escape(level)} · {html.escape(str(recommendation.get("title") or rid))}</div><h3>{html.escape(str(target.get("content_goal") or recommendation.get("description") or ""))}</h3><p class="goal">This is what the page needs to communicate. The visual pattern on the right is judged against this—not chosen only because it looks attractive.</p><div class="content-label">Existing content, shown as a rough structure</div><div class="wireframe">{wireframe}</div>{connection}</div><div class="recommendation"><div class="recommendation-visual"><span class="scope-badge">{html.escape(scope_label(scope))}</span>{recommendation_evidence_html(root, output, evidence, portable)}</div><div class="recommendation-body"><div class="recommendation-heading"><div><p class="eyebrow">Recommended reference pattern</p><h4>{html.escape(str(recommendation.get("title") or rid))}</h4><p>{html.escape(str(recommendation.get("description") or ""))}</p></div><span class="confidence">{html.escape(confidence)} confidence</span></div><div class="fit-grid"><div><b>Why it may fit</b><p>{html.escape(str(recommendation.get("fit") or ""))}</p></div><div><b>What Claude or Codex receives</b><p>{html.escape(str(compatibility.get("notes") or "The complete combination still needs an agent compatibility check."))}</p><small>Alternatives: {html.escape(alternatives)}</small></div></div>{dependency_note}<section><h5>What this option needs</h5>{assets_html(requirements)}</section>{decision_actions(rid, scope, target_id, affected_blocks)}</div></div></article>'''


def page_decisions_html(root: Path, output: Path, packet: dict[str, object] | None, portable: bool) -> str:
    if not packet:
        return '<div class="empty">No page-aware recommendations yet. UI Research must produce <code>brain/research/page-recommendations.json</code>.</div>'
    input_data = packet.get("input") if isinstance(packet.get("input"), dict) else {}
    input_targets = {str(item.get("target_id")): item for item in input_data.get("targets", []) if isinstance(item, dict)}
    result_targets = {str(item.get("target_id")): item for item in packet.get("targets", []) if isinstance(item, dict)}
    families = {str(item.get("family_id")): item for item in input_data.get("page_families", []) if isinstance(item, dict)}
    evidence_index: dict[str, dict[str, object]] = {}
    for result in result_targets.values():
        for recommendation in result.get("recommendations", []):
            if not isinstance(recommendation, dict):
                continue
            for evidence in recommendation.get("evidence", []):
                if isinstance(evidence, dict) and evidence.get("evidence_id"):
                    evidence_index[str(evidence["evidence_id"])] = evidence
    nav: list[str] = []
    panels: list[str] = []
    for index, (target_id, target) in enumerate(input_targets.items()):
        label = str(target.get("label") or target_id)
        family = families.get(str(target.get("family_id") or ""), {})
        kind = str(family.get("kind") or "unique")
        routes = ", ".join(str(value) for value in family.get("routes", []))
        nav.append(f'<button class="page-review-tab {"active" if index == 0 else ""}" data-review-page="review-page-{index}">{html.escape(label)}</button>')
        jobs = [str(value) for value in target.get("content_jobs", [])]
        page_map = "".join(f'<li><span>{number + 1}</span><b>{html.escape(job)}</b></li>' for number, job in enumerate(jobs)) or '<li><b>No content jobs recorded.</b></li>'
        recommendations = [item for item in result_targets.get(target_id, {}).get("recommendations", []) if isinstance(item, dict)]
        priority = {"whole-page": 0, "repeated-page-family": 0, "connected-sections": 1, "one-section": 2}
        recommendations.sort(key=lambda item: priority.get(str(item.get("scope") or "one-section"), 3))
        cards = "".join(recommendation_card(root, output, item, target, portable, card_index == 0) for card_index, item in enumerate(recommendations))
        controls = '<div class="recommendation-nav"><button class="previous-recommendation">← Previous</button><span>Review one recommendation at a time</span><button class="next-recommendation">Next →</button></div>' if len(recommendations) > 1 else ""
        panels.append(f'''<section id="review-page-{index}" class="page-review-panel {"active" if index == 0 else ""}"><header class="page-review-header"><div><p class="eyebrow">{html.escape(kind)} · {html.escape(routes)}</p><h4>{html.escape(label)}</h4><p>{html.escape(str(target.get("content_goal") or ""))}</p></div><div class="page-map"><b>What this page must cover</b><ol>{page_map}</ol></div></header><div class="recommendation-stack">{cards or '<div class="empty">No recommendation for this target.</div>'}</div>{controls}</section>''')

    direction = packet.get("site_direction") if isinstance(packet.get("site_direction"), dict) else {}
    direction_id = str(direction.get("recommendation_id") or "site-direction")
    direction_evidence = [evidence_index[value] for value in map(str, direction.get("evidence_refs", [])) if value in evidence_index]
    direction_pseudo = {
        "recommendation_id": direction_id,
        "scope": "whole-page",
        "affected_blocks": ["site-wide feeling", "page-family rhythm", "motion language"],
        "title": str(direction.get("summary") or "Site-wide direction"),
        "description": str(direction.get("summary") or "Review the family resemblance for the whole website."),
        "fit": str(direction.get("fit") or ""),
        "alternatives": direction.get("alternatives", []),
        "compatibility_notes": {"dependencies": [], "notes": "Claude or Codex checks the complete site combination after submission."},
        "evidence": direction_evidence,
        "asset_requirements": [],
        "confidence": direction.get("confidence", {}),
    }
    direction_target = {"target_id": "site-direction", "content_goal": str(input_data.get("site_goal") or "Choose the website's shared visual and behavioral direction."), "content_jobs": ["Site-wide feeling", "Page-family relationship", "Shared motion and media language"]}
    direction_card = recommendation_card(root, output, direction_pseudo, direction_target, portable, True).replace("Choose this first · Whole-page direction", "Choose this first · Site-wide direction", 1)
    shell = packet.get("global_shell") if isinstance(packet.get("global_shell"), dict) else {"target_id": "global-shell", "state": "not_needed", "recommendations": []}
    shell_recommendations = shell.get("recommendations") if isinstance(shell.get("recommendations"), list) else []
    shell_target = {"target_id": "global-shell", "content_goal": "Choose navigation, footer, and any page-dependent header treatment without separating them from the selected page direction.", "content_jobs": ["Navigation", "Footer", "Dependent header treatment"]}
    shell_items: list[str] = []
    for item in shell_recommendations:
        if not isinstance(item, dict):
            continue
        refs = [str(value) for value in item.get("evidence_refs", [])]
        pseudo = {
            **item,
            "description": str(item.get("title") or "Global shell option"),
            "fit": "Use this only when its linked page or hero direction is also selected.",
            "affected_blocks": ["navigation", "footer", "header treatment"],
            "compatibility_notes": {"dependencies": item.get("dependencies", []), "notes": "Header remains pending until reviewed here. A hero never selects it automatically."},
            "evidence": [evidence_index[value] for value in refs if value in evidence_index],
            "asset_requirements": [],
            "confidence": {"level": "evidence-backed"},
        }
        shell_items.append(recommendation_card(root, output, pseudo, shell_target, portable, len(shell_items) == 0))
    serialized = json.dumps(packet, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return f'''<div class="decision-workspace"><div class="decision-intro"><div><p class="eyebrow">Site-wide review before building</p><h3>Choose the family resemblance first, then review every page or family.</h3><p>Choices stay in this browser until the universal Submit or Update button writes <code>brain/research/ui-decision-draft.json</code>. Claude or Codex still checks compatibility; the browser never locks canon or unlocks a build.</p></div><div class="readiness"><b>{html.escape(str(packet.get("evidence_readiness") or "unknown"))}</b><span>Research evidence readiness</span></div></div><section class="site-direction-option">{direction_card}</section><section class="shell-review"><header><p class="eyebrow">Global shell</p><h4>Navigation, footer, and dependent header treatments</h4></header>{''.join(shell_items) or '<div class="empty">Research determined that no separate global-shell choice is needed.</div>'}</section><div class="page-review-tabs">{"".join(nav)}</div><div class="page-review-panels">{"".join(panels)}</div><div class="decision-submit-bar"><div><b id="decision-count">0 choices saved in this browser</b><span id="decision-message">Review the site direction, shell, and every page before submitting.</span></div><div><button id="review-decisions">Review choices</button><button id="export-decisions">Export JSON</button><button id="copy-decisions">Copy relay</button><button id="update-decisions" disabled>Update decisions</button><button id="submit-decisions">Submit decisions</button></div></div><dialog id="decision-request-dialog"><form method="dialog" id="decision-request-form"><h3 id="decision-request-title">Focused request</h3><p id="decision-request-copy"></p><div id="decision-request-fields"></div><div class="dialog-actions"><button value="cancel">Cancel</button><button value="save" id="decision-request-save">Save request</button></div></form></dialog><script type="application/json" id="page-recommendation-data">{serialized}</script></div>'''


def design_preview(root: Path) -> str:
    design = root / "brain" / "DESIGN.md"
    if not design.is_file():
        return ""
    text = design.read_text(errors="replace")
    values = list(dict.fromkeys(re.findall(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", text)))
    families = re.findall(r'^\s*family:\s*["\']?([^"\'\n#]+)', text, re.M)
    display = families[0].strip() if families else "Georgia"
    body = families[1].strip() if len(families) > 1 else "system-ui"
    swatches = "".join(f'<span><i style="--swatch:{v}"></i><b>{v}</b></span>' for v in values[:24]) or '<span class="empty">No concrete colors.</span>'
    return f'<article class="design-preview"><p class="eyebrow">Visual specimen</p><h3 style="font-family:{html.escape(display)}">A brand should be felt before it is explained.</h3><p style="font-family:{html.escape(body)}">Representative body typography, surfaces, and token colors.</p><div class="swatches">{swatches}</div></article>'


def progress_html(root: Path, paths: list[Path]) -> str:
    selected = []
    for path in paths:
        rel = f"/{path.relative_to(root).as_posix()}"
        real_chapter = "/chapters/" in rel and path.stem.lower() not in {"readme", "template", "_template"}
        if path.name in {"STATUS.md", "SITEMAP.md"} or real_chapter:
            selected.append(path)
    return '<div class="summary-grid">' + "".join(source_summary(root, p) for p in selected) + "</div>" if selected else '<div class="empty">No chapters or sitemap yet.</div>'


def render(root: Path, output: Path, paths: list[Path], portable: bool) -> str:
    current = hashes(root, paths)
    marker = base64.urlsafe_b64encode(json.dumps(current, sort_keys=True, separators=(",", ":")).encode()).decode().rstrip("=")
    brain = root / "brain"
    tabs: dict[str, str] = {}
    for name, rels in GROUPS.items():
        present = [brain / rel for rel in rels if (brain / rel).is_file()]
        summaries = '<div class="summary-grid">' + "".join(source_summary(root, p) for p in present) + "</div>" if present else f'<div class="empty">No {name.lower()} canon yet.</div>'
        tabs[name] = (design_preview(root) + summaries) if name == "Design" else summaries
    concepts, selection = parse_concepts(brain / "research/concepts.md")
    sites = teardown_sites(root, paths)
    page_recommendations = load_page_recommendations(root)
    review_content = f'<section class="research-section page-decision-section">{page_decisions_html(root, output, page_recommendations, portable)}</section>'
    if page_recommendations:
        # A page-aware packet opens as a dedicated decision workspace. The old
        # project-summary tabs would compete with the human review and recreate
        # the confusing dashboard shell this workflow replaces.
        nav = ""
        panels = f'<section class="panel active">{review_content}</section>'
        body_class = "review-mode"
        header = f'<header class="review-header"><h1>{html.escape(root.name)}</h1><span>UI review</span></header>'
    else:
        tabs["Research / Moodboard"] = f'{review_content}<section class="research-section"><h3>Review the broader concept evidence</h3>{concepts_html(concepts, selection)}</section><section class="research-section"><h3>Inspect evidence one site at a time</h3>{sites_html(root, output, sites, portable)}</section>'
        tabs["Build Progress"] = progress_html(root, paths)
        nav = "".join(f'<button data-tab="t{i}" class="{"active" if i == 0 else ""}">{html.escape(name)}</button>' for i, name in enumerate(tabs))
        panels = "".join(f'<section id="t{i}" class="panel {"active" if i == 0 else ""}"><h2>{html.escape(name)}</h2>{content}</section>' for i, (name, content) in enumerate(tabs.items()))
        body_class = "dashboard-mode"
        header = f'<header><h1>{html.escape(root.name)}</h1><p>Concise visual projection of Markdown canon · {"portable" if portable else "local"} assets · {len(paths)} hashed inputs</p></header>'
    mode = "portable" if portable else "local"
    title = html.escape(root.name)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Project Dashboard</title><style>
:root{{--bg:#f4f1ea;--panel:#fffdf8;--ink:#1d1b18;--muted:#706b63;--line:#d9d2c7;--accent:#174c3c;--warn:#9a5b10}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,sans-serif}}body>header{{padding:14px clamp(20px,4vw,56px);border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:16px}}body>header p{{margin:0}}h1{{margin:0;font:700 clamp(24px,3vw,34px)/1.05 ui-serif,Georgia,serif}}h2{{font-size:clamp(26px,3vw,40px)}}h3{{line-height:1.15}}p,.muted,small{{color:var(--muted)}}nav{{display:flex;gap:8px;overflow:auto;padding:10px clamp(20px,4vw,56px);position:sticky;top:0;background:rgba(244,241,234,.96);backdrop-filter:blur(12px);z-index:6}}button{{border:1px solid var(--line);background:var(--panel);padding:9px 13px;border-radius:999px;cursor:pointer;font:inherit}}button:disabled{{opacity:.45;cursor:not-allowed}}nav button{{white-space:nowrap}}button.active,button[aria-pressed="true"]{{background:var(--ink);color:white}}main{{padding:8px clamp(20px,4vw,56px) 90px}}.panel,.concept-panel,.site-panel,.page-review-panel,.recommendation-card{{display:none}}.panel.active,.concept-panel.active,.site-panel.active,.page-review-panel.active,.recommendation-card.active{{display:block}}.summary-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}.summary-card,.design-preview,.concept-panel,.site-panel,.selection-status,.site-direction-option,.shell-review,.page-review-panel{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 8px 30px rgba(50,40,25,.05)}}.summary-card ul{{padding-left:20px}}.source,.eyebrow{{text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-size:11px}}.design-preview h3,.concept-panel h3,.site-panel h3{{font-size:clamp(32px,5vw,70px);margin:10px 0 22px}}.swatches{{display:flex;flex-wrap:wrap;gap:10px}}.swatches span{{display:grid;gap:5px;font-size:11px}}.swatches i{{width:78px;height:58px;border-radius:10px;background:var(--swatch);border:1px solid var(--line)}}.empty{{padding:32px;border:1px dashed var(--line);border-radius:14px;color:var(--muted)}}.research-section{{margin:24px 0 64px}}.page-decision-section{{margin-top:8px}}.research-section>h3{{font-size:clamp(24px,3vw,40px)}}.selection-status{{display:flex;justify-content:space-between;gap:16px;margin-bottom:16px}}.selection-status.pending{{border-color:#d5a562;background:#fff8e8}}.selection-status span{{color:var(--muted)}}.concept-layout,.site-layout{{display:grid;grid-template-columns:minmax(190px,260px) minmax(0,1fr);gap:18px}}aside{{display:flex;flex-direction:column;gap:8px;align-self:start;position:sticky;top:68px}}aside button{{text-align:left;border-radius:12px}}dl>div{{display:grid;grid-template-columns:150px 1fr;gap:18px;border-top:1px solid var(--line);padding:13px 0}}dt{{font-weight:700}}dd{{margin:0}}.live-links,.site-panel header,.decision-evidence header{{display:flex;gap:12px;justify-content:space-between;align-items:center;flex-wrap:wrap}}a.live,.live-links a{{display:inline-flex;padding:9px 13px;background:var(--ink);color:white;border-radius:999px;text-decoration:none}}.review{{margin-top:28px;padding-top:20px;border-top:1px solid var(--line);display:flex;gap:8px;align-items:center;flex-wrap:wrap}}.review span{{font-weight:700}}textarea{{width:100%;min-height:72px;margin-top:8px;border:1px solid var(--line);border-radius:10px;padding:11px;font:inherit}}.evidence-stack{{display:grid;gap:24px;margin-top:18px}}figure{{margin:0;background:#111;border-radius:15px;overflow:hidden}}figure img,figure video{{display:block;width:100%;height:auto;max-height:78vh;object-fit:contain;background:#111}}figcaption{{padding:10px;background:var(--panel);color:var(--muted);font-size:12px}}.badge,.scope-badge,.confidence{{display:inline-block;padding:5px 9px;border-radius:999px;margin-right:8px;font-size:11px;font-weight:700}}.badge.ok{{background:#e7f3e8;color:#255c2a}}.badge.warn,.dependency-note{{background:#fff0d4;color:#80500b}}.badge.bad{{background:#f9dddd;color:#8b2525}}.scope-badge{{background:#e4eee9;color:var(--accent)}}.confidence{{background:#ece8df;color:#4f4a43}}.decision-intro{{display:flex;justify-content:space-between;gap:24px;align-items:end;padding:10px 0 18px}}.decision-intro h3{{font-size:clamp(26px,4vw,48px);max-width:900px;margin:4px 0}}.readiness{{display:grid;text-align:right;white-space:nowrap}}.readiness b{{font-size:20px}}.site-direction-option,.shell-review{{margin-bottom:14px}}.site-direction-option h4,.shell-review h4,.page-review-header h4{{font:700 clamp(24px,3vw,38px)/1.1 ui-serif,Georgia,serif;margin:8px 0}}.shell-option{{border-top:1px solid var(--line);padding:18px 0}}.dependency-note{{padding:10px 12px;border-radius:10px}}.page-review-tabs{{display:flex;gap:8px;overflow:auto;padding:12px 0;position:sticky;top:53px;background:var(--bg);z-index:5}}.page-review-tabs button{{white-space:nowrap}}.page-review-header{{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,.75fr);gap:28px;border-bottom:1px solid var(--line);padding-bottom:18px}}.page-map ol{{display:flex;flex-wrap:wrap;gap:7px;padding:0;list-style:none}}.page-map li{{display:flex;gap:7px;align-items:center;border:1px solid var(--line);padding:7px 10px;border-radius:999px}}.page-map li span{{display:grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--ink);color:#fff;font-size:11px}}.recommendation-card{{padding-top:22px}}.recommendation-heading,.fit-grid{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,.6fr);gap:24px}}.recommendation-heading h4{{font:700 clamp(30px,5vw,64px)/1.02 ui-serif,Georgia,serif;margin:8px 0}}.recommendation-description{{font-size:18px;max-width:900px}}.fit-grid>div{{border-top:1px solid var(--line);padding-top:12px}}.recommendation-card h5{{font-size:18px;margin:24px 0 10px}}.decision-evidence{{margin:14px 0;border:1px solid var(--line);border-radius:14px;overflow:hidden}}.decision-evidence header,.decision-evidence>p,.decision-evidence>.badge{{margin:12px 16px}}.decision-media{{background:#111;display:grid;place-items:center}}.decision-media img{{display:block;width:100%;max-height:78vh;object-fit:contain}}.evidence-missing{{padding:60px 24px;color:#fff}}.asset-list{{display:grid;gap:8px;padding:0;list-style:none}}.asset-list li{{display:grid;gap:3px;border-top:1px solid var(--line);padding:10px 0}}.decision-actions{{display:flex;gap:8px;flex-wrap:wrap;border-top:1px solid var(--line);margin-top:20px;padding-top:18px}}.decision-actions textarea,.decision-actions .choice-state{{flex-basis:100%}}.choice-state{{margin:0;color:var(--accent)}}.recommendation-nav{{display:flex;justify-content:space-between;align-items:center;margin-top:18px}}.decision-submit-bar{{position:sticky;bottom:10px;background:#1d1b18;color:#fff;padding:12px 14px;border-radius:14px;display:flex;justify-content:space-between;align-items:center;gap:16px;box-shadow:0 12px 40px rgba(0,0,0,.22);z-index:8}}.decision-submit-bar>div{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}.decision-submit-bar span{{color:#d4cec5;font-size:12px}}.decision-submit-bar button{{background:#fff}}.decision-submit-bar #submit-decisions,.decision-submit-bar #update-decisions{{background:#2a6a55;color:#fff;border-color:#2a6a55}}@media(max-width:760px){{body>header{{display:block}}.concept-layout,.site-layout,.page-review-header,.recommendation-heading,.fit-grid{{grid-template-columns:1fr}}aside{{position:static;display:flex;flex-direction:row;overflow:auto}}aside button{{white-space:nowrap}}dl>div{{grid-template-columns:1fr;gap:3px}}.selection-status,.decision-intro,.decision-submit-bar{{display:grid}}.readiness{{text-align:left}}.decision-submit-bar{{bottom:4px}}}}
.decision-workspace{{max-width:1800px;margin:0 auto}}.decision-workspace .decision-intro{{padding:4px 0 10px}}.decision-workspace .decision-intro h3{{font-size:clamp(22px,3vw,38px)}}.decision-workspace .site-direction-option,.decision-workspace .shell-review,.decision-workspace .page-review-panel{{padding:0;background:transparent;border:0;box-shadow:none}}.decision-block{{grid-template-columns:minmax(280px,.72fr) minmax(0,1.28fr);gap:clamp(22px,4vw,64px);padding:clamp(28px,5vw,72px) 0;border-top:1px solid var(--line)}}.decision-block.active{{display:grid}}.decision-block.connected{{margin:18px 0;padding:clamp(24px,4vw,54px);border:1px solid #c9d9d2;border-radius:18px;background:#edf4f0}}.decision-block.page-wide{{border-top:3px solid var(--ink)}}.brief{{position:sticky;top:68px;align-self:start}}.block-number,.content-label{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}}.brief h3{{font:500 clamp(25px,3vw,42px)/1.14 ui-serif,Georgia,serif;margin:12px 0}}.brief .goal{{font-size:16px}}.wireframe{{display:grid;gap:8px;margin-top:16px;padding:14px;border:1px dashed #bbb3a8;border-radius:14px;background:rgba(255,255,255,.55)}}.wire-row{{min-height:44px;padding:10px 12px;border-radius:9px;background:#fff;display:flex;justify-content:space-between;gap:12px;align-items:center}}.wire-row small{{font-size:10px;text-transform:uppercase;letter-spacing:.08em}}.connection-note{{margin-top:14px;padding:13px;border-left:3px solid var(--accent);background:var(--accent-soft)}}.recommendation{{background:var(--panel);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 18px 55px rgba(47,39,28,.09)}}.recommendation-visual{{position:relative;padding:12px;background:#222}}.recommendation-visual>.scope-badge{{position:absolute;z-index:2;top:22px;left:22px}}.recommendation-visual .decision-evidence{{margin:0;border:0}}.recommendation-visual .decision-media img{{max-height:64vh}}.recommendation-body{{padding:clamp(20px,3vw,34px)}}.recommendation-heading{{align-items:start}}.recommendation-heading h4{{font:500 clamp(25px,3vw,42px)/1.12 ui-serif,Georgia,serif;margin:6px 0}}.optional-parts{{margin:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}.optional-parts summary{{padding:13px 0;cursor:pointer;color:var(--muted)}}.part-list{{display:flex;flex-wrap:wrap;gap:8px;padding-bottom:14px}}.part-choice[aria-pressed="true"]{{background:var(--accent);color:#fff;border-color:var(--accent)}}.request-action{{border-radius:10px}}.decision-actions .decision-action{{border-radius:10px}}dialog{{width:min(680px,calc(100% - 28px));border:0;border-radius:20px;padding:0;box-shadow:0 32px 100px rgba(0,0,0,.28)}}dialog::backdrop{{background:rgba(14,14,12,.62);backdrop-filter:blur(4px)}}#decision-request-form{{padding:28px}}#decision-request-form h3{{font:500 30px/1.15 ui-serif,Georgia,serif}}#decision-request-fields label{{display:grid;gap:7px;margin:16px 0}}#decision-request-fields input,#decision-request-fields textarea{{width:100%;padding:12px;border:1px solid var(--line);border-radius:10px;font:inherit}}.dialog-actions{{display:flex;justify-content:flex-end;gap:10px}}body>header{{padding:8px clamp(16px,2vw,32px)}}body>header h1{{font-size:20px}}body>header p{{font-size:11px}}body>nav{{padding:7px clamp(16px,2vw,32px)}}main{{padding-inline:clamp(16px,2vw,32px)}}.review-header{{position:sticky;top:0;z-index:7;justify-content:space-between;background:rgba(244,241,234,.96);backdrop-filter:blur(12px)}}.review-header span{{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}}.review-mode main{{padding-top:0}}.review-mode .page-review-tabs{{top:40px}}@media(max-width:900px){{.decision-block.active{{display:grid;grid-template-columns:1fr}}.brief{{position:static}}}}
</style></head><body class="{body_class}">{HASH_PREFIX}{marker} -->{header}{f'<nav class="dashboard-tabs">{nav}</nav>' if nav else ''}<main>{panels}</main><script>
function swap(selector,panel,id){{document.querySelectorAll(selector).forEach(x=>x.classList.remove('active'));document.querySelectorAll(panel).forEach(x=>x.classList.remove('active'));const b=document.querySelector(`[data-${{selector.includes('concept')?'concept':'site'}}="${{id}}"]`);if(b)b.classList.add('active');const p=document.getElementById(id);if(p)p.classList.add('active')}}
document.querySelectorAll('nav button[data-tab]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('nav button,.panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.tab).classList.add('active')}}));
document.querySelectorAll('.concept-jump').forEach(b=>b.addEventListener('click',()=>swap('.concept-jump','.concept-panel',b.dataset.concept)));
document.querySelectorAll('.site-jump').forEach(b=>b.addEventListener('click',()=>swap('.site-jump','.site-panel',b.dataset.site)));
document.querySelectorAll('.review').forEach(r=>{{const key='project-dashboard-review:'+r.dataset.reviewKey;let saved={{}};try{{saved=JSON.parse(localStorage.getItem(key)||'{{}}')}}catch(e){{}}const t=r.querySelector('textarea');t.value=saved.note||'';r.querySelectorAll('button').forEach(b=>{{if(saved.verdict===b.dataset.verdict)b.setAttribute('aria-pressed','true');b.addEventListener('click',()=>{{saved.verdict=b.dataset.verdict;localStorage.setItem(key,JSON.stringify(saved));r.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}})}});t.addEventListener('input',()=>{{saved.note=t.value;localStorage.setItem(key,JSON.stringify(saved))}})}});
document.querySelectorAll('.page-review-tab').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.page-review-tab,.page-review-panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.reviewPage).classList.add('active')}}));
document.querySelectorAll('.page-review-panel').forEach(panel=>{{const cards=[...panel.querySelectorAll('.recommendation-card')];let index=0;const show=next=>{{if(!cards.length)return;index=(next+cards.length)%cards.length;cards.forEach((card,i)=>card.classList.toggle('active',i===index))}};panel.querySelector('.previous-recommendation')?.addEventListener('click',()=>show(index-1));panel.querySelector('.next-recommendation')?.addEventListener('click',()=>show(index+1))}});
const recommendationNode=document.getElementById('page-recommendation-data');
if(recommendationNode){{
 const source=JSON.parse(recommendationNode.textContent);const checkoutIdentity=source.checkout?.checkout_root||'unknown-checkout',reviewKey='project-dashboard-page-decisions:'+checkoutIdentity+':'+source.mission_id,requestKey=reviewKey+':requests';let review={{}},requests=[];try{{review=JSON.parse(localStorage.getItem(reviewKey)||'{{}}')}}catch(e){{review={{}}}}try{{requests=JSON.parse(localStorage.getItem(requestKey)||'[]')}}catch(e){{requests=[]}}
 const message=document.getElementById('decision-message'),count=document.getElementById('decision-count'),submitButton=document.getElementById('submit-decisions'),updateButton=document.getElementById('update-decisions');let submitted=false;
 const saveLocal=()=>{{localStorage.setItem(reviewKey,JSON.stringify(review));localStorage.setItem(requestKey,JSON.stringify(requests))}};
 const refresh=()=>{{document.querySelectorAll('.decision-actions').forEach(group=>{{const saved=review[group.dataset.recommendationId]||{{}};group.querySelectorAll('.decision-action').forEach(button=>button.setAttribute('aria-pressed',String(saved.status===button.dataset.status)));group.closest('.recommendation-body')?.querySelectorAll('.part-choice').forEach(button=>button.setAttribute('aria-pressed',String((saved.selected_parts||[]).includes(button.dataset.part))));group.querySelector('textarea').value=saved.note||'';group.querySelector('.choice-state').textContent=saved.status?`Choice: ${{saved.status.replaceAll('_',' ')}}`:'No choice recorded.'}});count.textContent=`${{Object.keys(review).length}} choices · ${{requests.length}} requests saved in this browser`}};
 document.querySelectorAll('.decision-actions').forEach(group=>{{group.querySelectorAll('.decision-action').forEach(button=>button.addEventListener('click',()=>{{const previous=review[group.dataset.recommendationId]||{{}};review[group.dataset.recommendationId]={{...previous,status:button.dataset.status,candidate_ids:[group.dataset.recommendationId],scope:group.dataset.scope,target_id:group.dataset.targetId,note:group.querySelector('textarea').value||''}};saveLocal();refresh()}}));group.querySelector('textarea').addEventListener('input',event=>{{if(!review[group.dataset.recommendationId])return;review[group.dataset.recommendationId].note=event.target.value;saveLocal()}});group.closest('.recommendation-body')?.querySelectorAll('.part-choice').forEach(button=>button.addEventListener('click',()=>{{const saved=review[group.dataset.recommendationId]||{{status:'shortlisted',candidate_ids:[group.dataset.recommendationId],scope:group.dataset.scope,target_id:group.dataset.targetId,note:''}},parts=new Set(saved.selected_parts||[]);parts.has(button.dataset.part)?parts.delete(button.dataset.part):parts.add(button.dataset.part);saved.selected_parts=[...parts];review[group.dataset.recommendationId]=saved;saveLocal();refresh()}}))}});
 const normalizeScope=value=>({{'whole-page':'whole_page','connected-sections':'connected_sections','one-section':'section','repeated-page-family':'page_family','global-shell':'global_shell'}}[value]||value);
 const buildPacket=()=>{{const targetResults=new Map((source.targets||[]).map(target=>[target.target_id,target]));const pages=(source.input.targets||[]).map(target=>{{const recs=(targetResults.get(target.target_id)||{{recommendations:[]}}).recommendations||[];return{{id:target.target_id,family_id:target.family_id,label:target.label,decisions:recs.filter(rec=>review[rec.recommendation_id]).map(rec=>({{...review[rec.recommendation_id],id:rec.recommendation_id,scope:normalizeScope(rec.scope),affected_blocks:(review[rec.recommendation_id].selected_parts?.length?review[rec.recommendation_id].selected_parts:rec.affected_blocks)||[]}}))}}}});const directionId=source.site_direction?.recommendation_id;const shellSource=source.global_shell||{{target_id:'global-shell',state:'not_needed',recommendations:[]}},shellRecommendations=shellSource.recommendations||[],shell=shellRecommendations.filter(item=>review[item.recommendation_id]).map(item=>({{...review[item.recommendation_id],recommendation_id:item.recommendation_id,scope:'global_shell'}}));const assets=[],assetKeys=new Set();(source.targets||[]).forEach(target=>(target.recommendations||[]).forEach(rec=>{{const choice=review[rec.recommendation_id];if(choice?.status==='selected')(rec.asset_requirements||[]).forEach(asset=>{{const key=`${{target.target_id}}:${{rec.recommendation_id}}:${{asset.asset_id}}`;if(!assetKeys.has(key)){{assetKeys.add(key);assets.push({{...asset,target_id:target.target_id,recommendation_id:rec.recommendation_id}})}}}})}}));const focused=requests.filter(item=>item.kind==='research'),provided=[...(source.input.reference_scope?.urls||[]).map(url=>({{live_url:url,source:'initial-research-scope'}})),...requests.filter(item=>item.kind==='reference')];return{{schema_version:1,project:{{name:source.project}},research:{{mission_id:source.mission_id,mode:source.entry_mode,evidence_readiness:source.evidence_readiness,derived_path:source.derived_path,documented_gaps:source.unresolved_gaps||[]}},site_direction:{{recommendation_id:directionId,...(review[directionId]||{{}})}},global_shell:{{target_id:'global-shell',state:shellSource.state||'not_needed',recommendations:shellRecommendations,decisions:shell}},page_families:source.input.page_families||[],pages,asset_requirements:assets,focused_research_requests:focused,provided_references:provided}}}};
 const requestDialog=document.getElementById('decision-request-dialog'),requestForm=document.getElementById('decision-request-form'),requestFields=document.getElementById('decision-request-fields');let pendingRequest=null;
 document.querySelectorAll('.request-action').forEach(button=>button.addEventListener('click',()=>{{const group=button.closest('.decision-actions'),kind=button.dataset.request;pendingRequest={{kind,target_id:group.dataset.targetId,recommendation_id:group.dataset.recommendationId,scope:normalizeScope(group.dataset.scope),affected_blocks:[...group.closest('.recommendation-body').querySelectorAll('.part-choice[aria-pressed="true"]')].map(item=>item.dataset.part)}};document.getElementById('decision-request-title').textContent=kind==='research'?'Research another pattern':'Bring your own reference';document.getElementById('decision-request-copy').textContent=kind==='research'?'Describe what the current recommendations fail to solve. This creates one focused Aside request, not a new broad research round.':'Paste the exact page URL and explain the exact part you liked. Claude or Codex will not assume you want the whole website.';requestFields.innerHTML=kind==='research'?'<label><span>What is missing?</span><textarea name="missing_need" required></textarea></label>':'<label><span>Exact website or page URL</span><input name="live_url" type="url" required></label><label><span>What exactly did you like?</span><textarea name="liked_part" required></textarea></label>';requestDialog.showModal()}}));
 requestForm.addEventListener('submit',event=>{{if(event.submitter?.value!=='save'||!pendingRequest)return;event.preventDefault();const data=Object.fromEntries(new FormData(requestForm));requests.push({{...pendingRequest,...data,created_at:new Date().toISOString()}});if(pendingRequest.kind==='research'){{const saved=review[pendingRequest.recommendation_id]||{{candidate_ids:[pendingRequest.recommendation_id],scope:pendingRequest.scope,target_id:pendingRequest.target_id,note:''}};saved.status='needs_more_research';review[pendingRequest.recommendation_id]=saved}}saveLocal();requestDialog.close();requestForm.reset();pendingRequest=null;refresh();message.textContent='Focused request saved locally. Submit or Update to relay it to Claude or Codex.'}});
 const incomplete=packet=>{{if(!packet.site_direction.status)return 'Review the site-wide direction.';if(packet.global_shell.state!=='not_needed'&&(packet.global_shell.recommendations||[]).some(item=>!review[item.recommendation_id]))return 'Review every global-shell option.';const missing=packet.pages.find(page=>!page.decisions.length);return missing?`Review ${{missing.label||missing.id}}.`:''}};
 const exportPacket=()=>{{const packet=buildPacket(),blob=new Blob([JSON.stringify(packet,null,2)+'\\n'],{{type:'application/json'}}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='ui-decision-draft.json';link.click();URL.revokeObjectURL(link.href);message.textContent='Exported the provisional relay. It is not canon.'}};
 const copyPacket=async()=>{{try{{await navigator.clipboard.writeText(JSON.stringify(buildPacket(),null,2));message.textContent='Copied the provisional relay for Claude or Codex.'}}catch(error){{message.textContent='Clipboard access is unavailable here. Use Export JSON instead.'}}}};
 const persist=async action=>{{const packet=buildPacket(),problem=incomplete(packet);if(problem){{message.textContent=problem;return}}const config=window.__PROJECT_DASHBOARD_SERVER__;if(!config){{message.textContent='Static HTML cannot write project files. Use Export JSON or Copy relay.';return}}try{{const response=await fetch(`${{config.url}}/api/${{action}}`,{{method:'POST',headers:{{'Content-Type':'application/json','X-Project-Dashboard-Token':config.token}},body:JSON.stringify(packet)}}),result=await response.json();if(!response.ok)throw new Error(result.error||'Request failed');submitted=true;submitButton.disabled=true;updateButton.disabled=false;message.textContent=`Revision ${{result.submission.revision}} submitted for agent review. Build remains locked.`}}catch(error){{message.textContent=error.message}}}};
 document.getElementById('review-decisions').addEventListener('click',()=>{{const packet=buildPacket(),problem=incomplete(packet),selected=packet.pages.flatMap(page=>page.decisions.map(decision=>`${{page.label||page.id}} · ${{decision.status}} · ${{decision.id}}`));message.textContent=problem||`Ready to submit: ${{selected.length}} page choices, ${{packet.focused_research_requests.length}} focused requests, ${{packet.provided_references.length}} references.`}});document.getElementById('export-decisions').addEventListener('click',exportPacket);document.getElementById('copy-decisions').addEventListener('click',copyPacket);submitButton.addEventListener('click',()=>persist('submit'));updateButton.addEventListener('click',()=>persist('update'));
 const config=window.__PROJECT_DASHBOARD_SERVER__;if(config)fetch(`${{config.url}}/api/state`,{{headers:{{'X-Project-Dashboard-Token':config.token}}}}).then(response=>response.json()).then(state=>{{if(!state.packet)return;submitted=true;submitButton.disabled=true;updateButton.disabled=false;const packet=state.packet;const decisions=[packet.site_direction,...(packet.global_shell?.decisions||[]),...(packet.pages||[]).flatMap(page=>page.decisions||[])];decisions.filter(Boolean).forEach(item=>{{const id=item.id||item.recommendation_id||(item.candidate_ids||[])[0];if(id)review[id]={{status:item.status,candidate_ids:item.candidate_ids||[id],scope:item.scope,target_id:item.target_id,note:item.note||''}}}});localStorage.setItem(reviewKey,JSON.stringify(review));refresh();message.textContent=`Loaded submitted revision ${{packet.submission.revision}}. Build remains locked pending agent review.`}}).catch(()=>{{message.textContent='Could not load server state. Browser choices remain local.'}});
 refresh();
}}
</script></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--output")
    parser.add_argument("--portable", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    output = Path(args.output).resolve() if args.output else root / "brain/project-dashboard.html"
    paths = collect(root)
    if args.check:
        if read_embedded_hashes(output) == hashes(root, paths):
            print(f"fresh: {output}")
            return 0
        print(f"stale: {output}")
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(root, output, paths, args.portable))
    print(json.dumps({"output": str(output), "mode": "portable" if args.portable else "local", "inputs": len(paths)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
