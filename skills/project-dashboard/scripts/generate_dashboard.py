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


def normalize_content_jobs(raw: object) -> list[dict[str, str]]:
    """Normalize content_jobs to one shape for v1 (strings) and v2 (objects).

    Each entry becomes {"job_id": str|"", "label": str, "copy_excerpt": str|"", "copy_ref": str|""}.
    v1 strings and pseudo-target string jobs carry an empty job_id, copy_excerpt, and copy_ref.
    """
    jobs: list[dict[str, str]] = []
    for entry in raw if isinstance(raw, list) else []:
        if isinstance(entry, dict):
            jobs.append({
                "job_id": str(entry.get("job_id") or ""),
                "label": str(entry.get("label") or ""),
                "copy_excerpt": str(entry.get("copy_excerpt") or ""),
                "copy_ref": str(entry.get("copy_ref") or ""),
            })
        else:
            jobs.append({"job_id": "", "label": str(entry), "copy_excerpt": "", "copy_ref": ""})
    return jobs


def copy_excerpt_state(root: Path, copy_ref: str, excerpt: str) -> str:
    """Report whether a wireframe excerpt still matches its approved copy section.

    copy_ref is "brain/marketing/copy/<file>.md#<job-id>". Empty copy_ref or excerpt
    yields "unknown" (render nothing). A missing file or missing section yields "stale".
    Otherwise "fresh" when the normalized excerpt is a substring of the normalized
    section text, else "stale".
    """
    if not copy_ref or not excerpt:
        return "unknown"
    rel, _, job_id = copy_ref.partition("#")
    rel, job_id = rel.strip(), job_id.strip()
    if not rel or not job_id:
        return "stale"
    candidate = root / rel
    try:
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
            return "stale"
    except OSError:
        return "stale"
    text = resolved.read_text(errors="replace")
    section = re.search(rf"^##[ \t]+{re.escape(job_id)}(?![\w-])[\s\S]*?(?=^##[ \t]|\Z)", text, re.M)
    if not section:
        return "stale"

    def normalize(value: str) -> str:
        joined = " ".join(clean_inline(line) for line in value.splitlines())
        return re.sub(r"\s+", " ", joined).strip().casefold()

    section_norm = normalize(section.group(0))
    excerpt_norm = normalize(excerpt)
    return "fresh" if excerpt_norm and excerpt_norm in section_norm else "stale"


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
    if packet.get("schema_version") not in {
        "project-protocol.page-recommendations.v1",
        "project-protocol.page-recommendations.v2",
    }:
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
    evidence = sorted(evidence, key=lambda item: not (isinstance(item, dict) and item.get("first_impression")))
    slides: list[str] = []
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
        if not media:
            media.append('<div class="evidence-missing">No local visual. Use the live link and evidence notes.</div>')
        motion = item.get("motion") if isinstance(item.get("motion"), dict) else {}
        details = " · ".join(filter(None, [str(item.get("page") or ""), str(item.get("viewport") or ""), capture]))
        for medium in media:
            active = " active" if not slides else ""
            slides.append(f'''<article class="evidence-slide{active}"><header><div><b>{name}</b><p>{html.escape(details)}</p></div>{live}</header>{video_badge}<div class="decision-media">{medium}</div><div class="evidence-notes"><p><b>Observed:</b> {html.escape(str(item.get("evidence") or "Not recorded"))}</p><p><b>Motion:</b> {html.escape(str(motion.get("behavior") or "Not observed"))}</p></div></article>''')
    if not slides:
        return '<div class="empty">No visual evidence attached to this recommendation.</div>'
    controls = ""
    if len(slides) > 1:
        controls = f'''<div class="evidence-controls"><button class="previous-evidence" type="button" aria-label="Previous evidence">←</button><span><b class="evidence-position">1</b> of {len(slides)}</span><button class="next-evidence" type="button" aria-label="Next evidence">→</button></div>'''
    return f'''<div class="evidence-carousel" data-evidence-carousel>{"".join(slides)}{controls}</div>'''


def assets_html(requirements: list[dict[str, object]]) -> str:
    if not requirements:
        return '<p class="muted">No special media or bespoke marks required.</p>'
    rows = []
    for asset in requirements:
        routes = ", ".join(str(value) for value in asset.get("safe_source_routes", []))
        rows.append(f'''<li><b>{html.escape(str(asset.get("kind") or "asset")).title()} · {html.escape(str(asset.get("asset_id") or "unnamed"))}</b><span>{html.escape(str(asset.get("purpose") or ""))} · {html.escape(str(asset.get("quantity") or ""))} · {html.escape(str(asset.get("orientation_or_dimensions") or ""))}</span><small>Responsive: {html.escape(str(asset.get("responsive_need") or "unknown"))} · Poster/fallback: {html.escape(str(asset.get("poster_or_fallback") or "none"))} · Safe sources: {html.escape(routes or "not recorded")}</small></li>''')
    return f'<ul class="asset-list">{"".join(rows)}</ul>'


def decision_actions(
    recommendation_id: str,
    scope: str,
    target_id: str,
    parts: list[str] | None = None,
    allow_deferred_component: bool = True,
) -> str:
    actions = (
        ("recommended", "Recommended", "Go with what the research recommends"),
        ("selected", "Accept", "Yes — use this for the site"),
        ("shortlisted", "Shortlist", "Keep as a maybe"),
        ("not_using", "Not using", "Rule this out"),
    )
    buttons = "".join(f'<button class="decision-action" data-status="{status}" title="{tip}">{label}</button>' for status, label, tip in actions)
    part_buttons = "".join(f'<button class="part-choice" type="button" data-part="{html.escape(part)}" aria-pressed="false">{html.escape(part)}</button>' for part in (parts or []))
    optional_parts = f'<details class="optional-parts"><summary>Optional: keep or change specific parts</summary><div class="part-list">{part_buttons}</div></details>' if part_buttons else ""
    component_action = '<button class="request-action" type="button" data-request="component">I’ll bring my own component later</button>' if allow_deferred_component else ""
    default_blocks = html.escape(json.dumps(parts or []), quote=True)
    return f'''{optional_parts}<div class="decision-actions" data-recommendation-id="{html.escape(recommendation_id)}" data-scope="{html.escape(scope)}" data-target-id="{html.escape(target_id)}" data-affected-blocks="{default_blocks}">{buttons}<button class="request-action" type="button" data-request="research">Research another pattern for this part</button><button class="request-action" type="button" data-request="reference">Bring my own reference</button>{component_action}<textarea placeholder="Optional note for Claude or Codex"></textarea><p class="choice-state">No choice recorded.</p></div>'''


def recommendation_card(
    root: Path,
    output: Path,
    recommendation: dict[str, object],
    target: dict[str, object],
    portable: bool,
    active: bool,
    allow_deferred_component: bool = True,
    copy_outline: str = "",
) -> str:
    rid = str(recommendation.get("recommendation_id") or "")
    target_id = str(target.get("target_id") or "")
    scope = str(recommendation.get("scope") or "one-section")
    compatibility = recommendation.get("compatibility_notes") if isinstance(recommendation.get("compatibility_notes"), dict) else {}
    dependencies = [str(value) for value in compatibility.get("dependencies", [])]
    dependency_note = '<p class="dependency-note">Header remains pending. This option may propose a linked header treatment, but never selects it automatically.</p>' if dependencies else ""
    affected_blocks = [str(value) for value in recommendation.get("affected_blocks", [])]
    affected = ", ".join(affected_blocks) or "whole target"
    affected_pretty = ", ".join(block.replace("-", " ").replace("_", " ") for block in affected_blocks) or "whole target"
    alternatives = ", ".join(str(value) for value in recommendation.get("alternatives", [])) or "none recorded"
    evidence = recommendation.get("evidence") if isinstance(recommendation.get("evidence"), list) else []
    requirements = recommendation.get("asset_requirements") if isinstance(recommendation.get("asset_requirements"), list) else []
    normalized_jobs = normalize_content_jobs(target.get("content_jobs"))
    wire_rows: list[str] = []
    for index, job in enumerate(normalized_jobs):
        label = html.escape(job["label"] or "Untitled content job")
        excerpt = f'<em>{html.escape(job["copy_excerpt"])}</em>' if job["copy_excerpt"] else ""
        stale = '<span class="stale-copy">copy changed since research</span>' if copy_excerpt_state(root, job["copy_ref"], job["copy_excerpt"]) == "stale" else ""
        tag = "Lead" if index == 0 else "Required"
        wire_rows.append(f'<div class="wire-row"><strong>{label}</strong>{excerpt}{stale}<small>{tag}</small></div>')
    wireframe = "".join(wire_rows) or '<div class="wire-row"><strong>No content job recorded</strong><small>Open</small></div>'
    serves_jobs = [str(value) for value in recommendation.get("serves_jobs", []) if str(value)]
    if serves_jobs:
        label_by_id = {job["job_id"]: job["label"] for job in normalized_jobs if job["job_id"]}
        covers_pretty = ", ".join(
            label_by_id.get(job_id) or job_id.replace("-", " ").replace("_", " ") for job_id in serves_jobs
        ) or "whole target"
    else:
        covers_pretty = affected_pretty
    if scope in {"whole-page", "repeated-page-family"}:
        level = "Choose this first · Whole-page direction" if scope == "whole-page" else "Choose this first · Repeated page family"
    elif scope == "connected-sections":
        level = "Connected sequence"
    elif scope == "global-shell":
        level = "Shared across the site"
    else:
        level = "Optional section refinement"
    connection = f'<div class="connection-note"><strong>Keep this together:</strong> This recommendation affects {html.escape(affected)} as one connected composition.</div>' if scope == "connected-sections" else ""
    confidence = str((recommendation.get("confidence") or {}).get("level", "unknown") if isinstance(recommendation.get("confidence"), dict) else "unknown")
    title_text = str(recommendation.get("title") or rid)
    description_html = f'<p>{html.escape(str(recommendation.get("description")))}</p>' if recommendation.get("description") and str(recommendation.get("description")) != title_text else ""
    scope_plain = {
        "whole-page": "changes this entire page",
        "connected-sections": "a linked group of sections",
        "one-section": "just one section — optional",
        "repeated-page-family": "a layout reused by similar pages",
        "global-shell": "shared navigation & footer",
    }.get(scope, "")
    scope_plain_html = f'<i> · {html.escape(scope_plain)}</i>' if scope_plain else ""
    return f'''<article class="decision-block recommendation-card {"connected " if scope == "connected-sections" else ""}{"page-wide " if scope in {"whole-page", "repeated-page-family"} else ""}{"active" if active else ""}" data-recommendation-panel="{html.escape(rid)}"><div class="brief"><div class="block-number">{html.escape(level)} · {html.escape(title_text)}</div><p class="side-label">Your content</p><h3>{html.escape(str(target.get("content_goal") or recommendation.get("description") or ""))}</h3><p class="goal">This is what the page needs to communicate. The visual pattern on the right is judged against this—not chosen only because it looks attractive.</p><div class="content-label">Existing content, shown as a rough structure</div><div class="wireframe">{wireframe}</div>{connection}{copy_outline}</div><div class="recommendation"><div class="recommendation-heading"><div><p class="eyebrow">Recommended reference pattern</p><h4>{html.escape(title_text)}</h4>{description_html}</div><span class="confidence">{html.escape(confidence)} confidence</span></div><div class="mapping-line"><span class="scope-badge">{html.escape(scope_label(scope))}{scope_plain_html}</span><span class="mapping-covers">Covers: {html.escape(covers_pretty)}</span></div><div class="recommendation-visual">{recommendation_evidence_html(root, output, evidence, portable)}</div><div class="recommendation-body"><div class="fit-grid"><div><b>Why it may fit</b><p>{html.escape(str(recommendation.get("fit") or ""))}</p></div><div><b>What Claude or Codex receives</b><p>{html.escape(str(compatibility.get("notes") or "The complete combination still needs an agent compatibility check."))}</p><small>Alternatives: {html.escape(alternatives)}</small></div></div>{dependency_note}<section><h5>What this option needs</h5>{assets_html(requirements)}</section>{decision_actions(rid, scope, target_id, affected_blocks, allow_deferred_component)}</div></div></article>'''


def page_copy_outline(root: Path, routes: list[str], label: str) -> str:
    """Show only approved marketing copy that already exists on disk; never invent content."""
    copy_dir = root / "brain/marketing/copy"
    if not copy_dir.is_dir() or not routes:
        return ""
    groups: list[tuple[str, str, list[tuple[str, list[str], str]]]] = []
    for path in sorted(copy_dir.glob("*.md")):
        text = path.read_text(errors="replace")
        first_line = text.splitlines()[0] if text else ""
        match = re.match(r"^#\s+(.+?)\s*\(`([^`]+)`\)", first_line)
        if not match:
            continue
        file_label, file_route = clean_inline(match.group(1)), match.group(2).strip()
        if file_route not in routes:
            continue
        sections: list[tuple[str, list[str], str]] = []
        for section in re.finditer(r"^##\s+(?:\d+[.)]?\s*)?(.+)$([\s\S]*?)(?=^##\s|\Z)", text, re.M):
            name = clean_inline(section.group(1))
            if name.lower().startswith("copy notes"):
                continue
            headlines: list[str] = []
            blurb = ""
            for element, value in re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", section.group(2), re.M):
                key = element.strip().lower()
                cleaned = clean_inline(value)
                if key == "element" or not cleaned or set(cleaned) <= {"-"}:
                    continue
                if len(headlines) < 3 and any(k in key for k in ("wordmark", "h1", "headline", "title", "proper name", "name")):
                    headlines.append(cleaned)
                elif not blurb and any(k in key for k in ("tagline", "subtitle", "blurb", "body", "description", "intro")):
                    blurb = cleaned
            sections.append((name, headlines, blurb))
            if len(sections) == 8:
                break
        if sections:
            groups.append((file_label, file_route, sections))
        if len(groups) == 3:
            break
    if not groups:
        return ""
    parts = ['<div class="copy-outline"><div class="content-label">Approved copy on file</div>']
    show_file_names = len(groups) > 1
    for file_label, file_route, sections in groups:
        if show_file_names:
            parts.append(f'<p class="copy-file">{html.escape(file_label)} · {html.escape(file_route)}</p>')
        for number, (name, headlines, blurb) in enumerate(sections, 1):
            headline_html = f'<b>{html.escape(" · ".join(headlines))}</b>' if headlines else '<b class="copy-missing">No headline copy yet</b>'
            blurb_html = f"<small>{html.escape(blurb)}</small>" if blurb else ""
            parts.append(f'<div class="copy-slot"><span>{number}</span><div><i>{html.escape(name)}</i>{headline_html}{blurb_html}</div></div>')
    parts.append("</div>")
    return "".join(parts)


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
        outline = page_copy_outline(root, [str(value) for value in family.get("routes", [])], label)
        nav.append(f'<button class="page-review-tab {"active" if index == 0 else ""}" data-review-page="review-page-{index}">{html.escape(label)}</button>')
        jobs = normalize_content_jobs(target.get("content_jobs"))
        page_map = "".join(f'<li><span>{number + 1}</span><b>{html.escape(job["label"] or "Untitled content job")}</b></li>' for number, job in enumerate(jobs)) or '<li><b>No content jobs recorded.</b></li>'
        recommendations = [item for item in result_targets.get(target_id, {}).get("recommendations", []) if isinstance(item, dict)]
        priority = {"whole-page": 0, "repeated-page-family": 0, "connected-sections": 1, "one-section": 2}
        recommendations.sort(key=lambda item: priority.get(str(item.get("scope") or "one-section"), 3))
        cards = "".join(recommendation_card(root, output, item, target, portable, card_index == 0, copy_outline=outline) for card_index, item in enumerate(recommendations))
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
    direction_card = recommendation_card(root, output, direction_pseudo, direction_target, portable, True, False).replace("Choose this first · Whole-page direction", "Choose this first · Site-wide direction", 1)
    shell = packet.get("global_shell") if isinstance(packet.get("global_shell"), dict) else {"target_id": "global-shell", "state": "not_needed", "recommendations": []}
    shell_recommendations = shell.get("recommendations") if isinstance(shell.get("recommendations"), list) else []
    shell_target = {"target_id": "global-shell", "content_goal": "Pick the shared pieces every page uses: the top navigation, the footer, and any header style that depends on the page design you chose.", "content_jobs": ["Navigation", "Footer", "Dependent header treatment"]}
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
        shell_items.append(recommendation_card(root, output, pseudo, shell_target, portable, len(shell_items) == 0, False))
    serialized = json.dumps(packet, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    shell_controls = '<div class="recommendation-nav shell-recommendation-nav"><button class="previous-shell-recommendation">← Previous</button><span>Review one shell option at a time</span><button class="next-shell-recommendation">Next →</button></div>' if len(shell_items) > 1 else ""
    readiness = html.escape(str(packet.get("evidence_readiness") or "unknown").replace("_", " "))
    return f'''<div class="decision-workspace"><div class="decision-toolbar"><div class="review-stage-tabs" role="tablist" aria-label="Review stages"><button class="review-stage-tab active" data-review-stage="direction-stage">Direction</button><button class="review-stage-tab" data-review-stage="shell-stage">Global shell</button><button class="review-stage-tab" data-review-stage="pages-stage">Pages &amp; families</button></div><div class="publish-actions"><button id="review-decisions">Review</button><button id="export-decisions">Export</button><button id="copy-decisions">Copy</button><button id="update-decisions" disabled>Update</button><button id="submit-decisions">Submit decisions</button></div></div><div class="review-status"><div><b id="decision-count">0 choices saved</b><span id="decision-message">Start with Direction, then review Global shell and every page or family.</span></div><span class="readiness">Evidence: {readiness}</span></div><section id="direction-stage" class="review-stage active"><div class="stage-heading"><div><p class="eyebrow">First decision</p><h3>Website direction</h3></div><p>Choose the shared visual and behavioral family. This does not approve individual pages.</p></div><section class="site-direction-option">{direction_card}</section></section><section id="shell-stage" class="review-stage"><div class="stage-heading"><div><p class="eyebrow">Shared across the site</p><h3>Global shell</h3></div><p>Review navigation, footer, and any header treatment tied to a page or hero.</p></div><section class="shell-review">{''.join(shell_items) or '<div class="empty">Research determined that no separate global-shell choice is needed.</div>'}{shell_controls}</section></section><section id="pages-stage" class="review-stage"><div class="stage-heading"><div><p class="eyebrow">Page-aware review</p><h3>Pages &amp; families</h3></div><p>Select a page or repeated family, then review its full direction before optional refinements.</p></div><div class="page-review-tabs">{"".join(nav)}</div><div class="page-review-panels">{"".join(panels)}</div></section><dialog id="decision-request-dialog"><form method="dialog" id="decision-request-form"><h3 id="decision-request-title">Focused request</h3><p id="decision-request-copy"></p><div id="decision-request-fields"></div><div class="dialog-actions"><button value="cancel">Cancel</button><button value="save" id="decision-request-save">Save request</button></div></form></dialog><script type="application/json" id="page-recommendation-data">{serialized}</script></div>'''


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
.decision-workspace{{max-width:1800px;margin:0 auto}}.decision-workspace .decision-intro{{padding:4px 0 10px}}.decision-workspace .decision-intro h3{{font-size:clamp(22px,3vw,38px)}}.decision-workspace .site-direction-option,.decision-workspace .shell-review,.decision-workspace .page-review-panel{{padding:0;background:transparent;border:0;box-shadow:none}}.decision-block{{grid-template-columns:minmax(280px,.72fr) minmax(0,1.28fr);gap:clamp(22px,4vw,64px);padding:clamp(28px,5vw,72px) 0;border-top:1px solid var(--line)}}.decision-block.active{{display:grid}}.decision-block.connected{{margin:18px 0;padding:clamp(24px,4vw,54px);border:1px solid #c9d9d2;border-radius:18px;background:#edf4f0}}.decision-block.page-wide{{border-top:3px solid var(--ink)}}.brief{{position:sticky;top:68px;align-self:start}}.block-number,.content-label{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}}.brief h3{{font:500 clamp(25px,3vw,42px)/1.14 ui-serif,Georgia,serif;margin:12px 0}}.brief .goal{{font-size:16px}}.wireframe{{display:grid;gap:8px;margin-top:16px;padding:14px;border:1px dashed #bbb3a8;border-radius:14px;background:rgba(255,255,255,.55)}}.wire-row{{min-height:44px;padding:10px 12px;border-radius:9px;background:#fff;display:flex;justify-content:space-between;gap:12px;align-items:center}}.wire-row small{{font-size:10px;text-transform:uppercase;letter-spacing:.08em}}.connection-note{{margin-top:14px;padding:13px;border-left:3px solid var(--accent);background:var(--accent-soft)}}.recommendation{{background:var(--panel);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 18px 55px rgba(47,39,28,.09)}}.recommendation-visual{{position:relative;padding:12px;background:#222}}.recommendation-visual>.scope-badge{{position:absolute;z-index:2;top:22px;left:22px}}.recommendation-visual .decision-evidence{{margin:0;border:0}}.recommendation-visual .decision-media img{{max-height:64vh}}.recommendation-body{{padding:clamp(20px,3vw,34px)}}.recommendation-heading{{align-items:start}}.recommendation-heading h4{{font:500 clamp(25px,3vw,42px)/1.12 ui-serif,Georgia,serif;margin:6px 0}}.optional-parts{{margin:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}.optional-parts summary{{padding:13px 0;cursor:pointer;color:var(--muted)}}.part-list{{display:flex;flex-wrap:wrap;gap:8px;padding-bottom:14px}}.part-choice[aria-pressed="true"]{{background:var(--accent);color:#fff;border-color:var(--accent)}}.request-action{{border-radius:10px}}.decision-actions .decision-action{{border-radius:10px}}dialog{{width:min(680px,calc(100% - 28px));border:0;border-radius:20px;padding:0;box-shadow:0 32px 100px rgba(0,0,0,.28)}}dialog::backdrop{{background:rgba(14,14,12,.62);backdrop-filter:blur(4px)}}#decision-request-form{{padding:28px}}#decision-request-form h3{{font:500 30px/1.15 ui-serif,Georgia,serif}}#decision-request-fields label{{display:grid;gap:7px;margin:16px 0}}#decision-request-fields input,#decision-request-fields textarea{{width:100%;padding:12px;border:1px solid var(--line);border-radius:10px;font:inherit}}.dialog-actions{{display:flex;justify-content:flex-end;gap:10px}}body>header{{padding:8px clamp(16px,2vw,32px)}}body>header h1{{font-size:20px}}body>header p{{font-size:11px}}body>nav{{padding:7px clamp(16px,2vw,32px)}}main{{padding-inline:clamp(16px,2vw,32px)}}.review-header{{position:sticky;top:0;z-index:7;justify-content:space-between;background:rgba(244,241,234,.96);backdrop-filter:blur(12px)}}.review-header span{{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}}.review-mode main{{padding-top:0}}@media(max-width:900px){{.decision-block.active{{display:grid;grid-template-columns:1fr}}.brief{{position:static}}}}
/* The review app is one reusable product surface. Project data changes; this interface does not. */
.review-mode{{--bg:#faf8f3;--panel:#fffefb;--ink:#22211d;--body-c:#55534b;--muted:#8b8779;--line:#e8e4d8;--accent:#1e5c45;--accent-soft:#e9f1ec;--clay:#a2593a;--clay-soft:#f7ede6;--amber:#8a5a12;--amber-soft:#f7edd8;--warn:#8a5a12;--ok:#1e5c45;--side:236px;--side-bg:#f4f1e9;--font-display:"New York","Iowan Old Style",Palatino,ui-serif,Georgia,serif;--font-body:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Inter,sans-serif;background:var(--bg);color:var(--ink);font:14px/1.55 var(--font-body);-webkit-font-smoothing:antialiased}}
.review-mode .review-header{{position:fixed;top:0;left:0;width:var(--side);height:56px;z-index:32;margin:0;padding:0 18px;background:var(--side-bg);border:0;border-right:1px solid var(--line);border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:flex-start;backdrop-filter:none}}
.review-mode .review-header h1{{font-family:var(--font-display);font-size:16px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.review-mode .review-header span{{display:none}}
.review-mode main{{padding:0 0 0 var(--side)}}
.review-mode main::before{{content:"";position:fixed;left:0;top:0;bottom:0;width:var(--side);background:var(--side-bg);border-right:1px solid var(--line);z-index:20}}
.review-mode .page-decision-section{{margin:0}}
.decision-workspace{{width:100%;max-width:none;margin:0 auto}}
.decision-toolbar{{position:fixed;left:0;top:56px;width:var(--side);z-index:33;display:block;padding:10px;border:0;background:transparent;min-height:0}}
.review-stage-tabs{{display:flex;flex-direction:column;align-items:stretch;gap:2px;padding:0;background:transparent;border-radius:0;overflow:visible}}
.review-stage-tabs button{{position:relative;text-align:left;border:0;background:transparent;border-radius:9px;padding:8px 10px 8px 30px;color:#6b675a;font-size:13px;font-weight:600;white-space:normal}}
.review-stage-tabs button::before{{content:"";position:absolute;left:11px;top:14px;width:8px;height:8px;border-radius:50%;background:#cfc9ba}}
.review-stage-tabs button.decided::before{{background:var(--ok)}}
.review-stage-tabs button.active{{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(60,50,30,.1)}}
.review-stage-tabs button::after{{display:block;font-size:10.5px;font-weight:500;color:#9a9484;margin-top:1px}}
.review-stage-tabs button:nth-of-type(1)::after{{content:"The whole site's shared look"}}
.review-stage-tabs button:nth-of-type(2)::after{{content:"Navigation & footer"}}
.review-stage-tabs button:nth-of-type(3)::after{{content:"Each page, one at a time"}}
.page-review-tabs{{position:fixed;left:0;top:226px;bottom:300px;width:var(--side);z-index:33;display:flex;flex-direction:column;align-items:stretch;gap:1px;overflow-y:auto;margin:0;padding:8px 10px;background:transparent;border-radius:0;border-top:1px solid var(--line)}}
.page-review-tabs button{{position:relative;text-align:left;border:0;background:transparent;border-radius:8px;padding:7px 8px 7px 30px;color:#6b675a;font-size:12.5px;font-weight:550;white-space:normal}}
.page-review-tabs button::before{{content:"";position:absolute;left:11px;top:12px;width:7px;height:7px;border-radius:50%;background:#cfc9ba}}
.page-review-tabs button.decided::before{{background:var(--ok)}}
.page-review-tabs button.active{{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(60,50,30,.1)}}
.page-review-tabs::-webkit-scrollbar{{width:6px}}
.page-review-tabs::-webkit-scrollbar-thumb{{background:#ddd6c6;border-radius:6px}}
.publish-actions{{position:fixed;left:0;bottom:0;width:var(--side);z-index:34;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:12px 12px 14px;background:var(--side-bg);border-top:1px solid var(--line);border-right:1px solid var(--line)}}
.publish-actions::before{{content:"Decide every item — then submit everything at once from here.";grid-column:1/-1;font-size:10.5px;color:var(--muted);line-height:1.5;padding:0 2px}}
.publish-actions button{{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:9px;padding:8px 10px;font-size:12.5px;font-weight:600;white-space:nowrap}}
.publish-actions #review-decisions,.publish-actions #export-decisions,.publish-actions #copy-decisions{{grid-column:auto;background:transparent;border:0;color:var(--muted);font-size:11.5px;font-weight:550;padding:5px 4px}}
.publish-actions #review-decisions:hover,.publish-actions #export-decisions:hover,.publish-actions #copy-decisions:hover{{color:var(--ink);text-decoration:underline}}
.publish-actions #update-decisions{{grid-column:1/-1}}
.publish-actions #submit-decisions{{grid-column:1/-1;padding:11px;font-size:13px}}
.publish-actions #submit-decisions,.publish-actions #update-decisions{{background:var(--accent);border-color:var(--accent);color:#fff}}
.publish-actions #submit-decisions:disabled,.publish-actions #update-decisions:disabled{{display:none}}
.review-status{{position:fixed;left:0;bottom:150px;width:var(--side);z-index:33;display:flex;flex-direction:column;align-items:flex-start;gap:8px;padding:10px 16px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);background:var(--side-bg)}}
.review-status>div{{display:flex;flex-direction:column;gap:2px;align-items:flex-start;min-width:0}}
.review-status b{{color:var(--ink);font-weight:650;white-space:normal}}
.review-status #decision-message{{position:static;max-width:none;background:transparent;color:var(--muted);padding:0;box-shadow:none;white-space:normal;overflow:visible;font-size:11.5px;line-height:1.5}}
.review-status .readiness{{display:block;padding:4px 10px;background:#fff;color:var(--muted);border:1px solid var(--line);border-radius:12px;font-size:11px;font-weight:600;text-transform:capitalize;white-space:normal;text-align:left;line-height:1.4;max-width:100%}}
.review-stage{{display:none}}
.review-stage.active{{display:block}}
.stage-heading{{display:none}}
.decision-workspace .site-direction-option,.decision-workspace .shell-review,.decision-workspace .page-review-panel{{padding:0;background:transparent;border:0;box-shadow:none}}
#direction-stage,#shell-stage,#pages-stage{{padding:16px 22px 28px}}
.page-review-header{{display:block;padding:4px 2px 14px;background:transparent;border:0;border-radius:0;margin-bottom:4px;box-shadow:none}}
.page-review-header .eyebrow{{font-size:10px;letter-spacing:.1em;color:var(--muted)}}
.page-review-header h4{{font-family:var(--font-display);font-size:27px;font-weight:600;letter-spacing:0;margin:4px 0 2px}}
.page-review-header p{{margin:2px 0 0;color:var(--body-c);font-size:13px;max-width:760px}}
.page-map{{display:none}}
.decision-block{{grid-template-columns:minmax(300px,410px) minmax(0,1fr);gap:18px;padding:0;border:0}}
.decision-block.connected{{margin:0;padding:0;border:0;background:transparent}}
.decision-block.page-wide{{border:0}}
.brief{{position:static;align-self:start;padding:18px;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-left:3px solid var(--clay);border-radius:14px;min-height:0;box-shadow:0 1px 2px rgba(60,50,30,.05)}}
.brief .block-number{{color:var(--muted);font-size:9px;letter-spacing:.08em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.brief .side-label{{margin:10px 0 0;color:var(--clay);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
.brief h3{{font-family:var(--font-display);font-size:20px;line-height:1.35;font-weight:600;letter-spacing:0;margin:6px 0 4px;color:var(--ink)}}
.brief .goal{{color:var(--muted);font-size:12px;margin:4px 0 0}}
.brief .content-label{{margin-top:14px;color:var(--clay);font-size:9.5px;font-weight:700;letter-spacing:.08em}}
.wireframe{{border:0;border-radius:0;background:transparent;padding:0;margin-top:8px;display:grid;gap:7px}}
.wire-row{{min-height:0;background:#fff;color:var(--ink);border:1.5px dashed #d8c7b8;border-radius:9px;padding:9px 11px;font-size:12.5px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;align-items:center}}
.wire-row:first-child{{border-style:solid;border-color:var(--clay);background:var(--clay-soft)}}
.wire-row small{{color:#b39b83;font-size:8.5px;font-weight:700;letter-spacing:.1em}}
.wire-row em{{font-style:normal;display:block;width:100%;font-size:11px;color:var(--body-c);margin-top:3px;line-height:1.45}}
.stale-copy{{display:block;width:max-content;margin-top:4px;padding:2px 8px;border-radius:999px;background:var(--amber-soft);color:var(--amber);font-size:9.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}}
.connection-note{{margin-top:12px;padding:9px 12px;background:var(--accent-soft);color:#1c4a39;border-left:3px solid var(--accent);border-radius:8px;font-size:12px}}
.copy-outline{{margin-top:16px;border-top:1px solid var(--line);padding-top:12px}}
.copy-file{{margin:8px 0 2px;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.copy-slot{{display:flex;gap:9px;padding:8px 10px;background:#faf7f0;border-radius:8px;margin-top:6px;align-items:flex-start}}
.copy-slot>span{{flex:none;width:18px;height:18px;border-radius:50%;background:#e9dfd0;color:#7a5c42;font-size:10px;font-weight:700;display:grid;place-items:center;margin-top:1px}}
.copy-slot i{{display:block;font-style:normal;font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.copy-slot b{{display:block;font-size:12.5px;font-weight:600;color:var(--ink);margin-top:2px;line-height:1.35}}
.copy-slot b.copy-missing{{color:#b08968;font-weight:550}}
.copy-slot small{{margin-top:2px;font-size:11.5px;color:var(--body-c);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.recommendation{{border:1px solid var(--line);border-top:3px solid var(--accent);border-radius:14px;background:var(--panel);box-shadow:0 1px 2px rgba(60,50,30,.05),0 12px 30px rgba(60,50,30,.06);overflow:hidden}}
.recommendation-heading{{padding:16px 18px 8px;display:flex;justify-content:space-between;gap:16px;align-items:start}}
.recommendation-heading .eyebrow{{color:var(--accent);font-size:10px;font-weight:700;letter-spacing:.1em}}
.recommendation-heading h4{{font-family:var(--font-display);font-size:24px;font-weight:600;letter-spacing:0;margin:4px 0 0;line-height:1.22}}
.recommendation-heading p{{margin:5px 0 0;color:var(--body-c);font-size:13px}}
.confidence{{flex:none;background:var(--accent-soft);color:var(--accent);padding:5px 10px;border-radius:999px;font-size:11px;font-weight:650;margin:0}}
.mapping-line{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:0 18px 12px}}
.mapping-line .scope-badge{{position:static;background:var(--accent-soft);color:var(--accent);margin:0}}
.scope-badge i{{font-style:normal;font-weight:500;color:#4f7a68}}
.mapping-covers{{font-size:11.5px;color:var(--muted)}}
.recommendation-visual{{position:relative;padding:0 18px;background:transparent}}
.recommendation-visual>.scope-badge{{display:none}}
.evidence-slide{{display:none;position:relative;border-radius:0;overflow:visible}}
.evidence-slide.active{{display:flex;flex-direction:column}}
.evidence-slide header{{order:2;min-height:40px;margin:0;padding:8px 2px 0;background:transparent;color:var(--ink);display:flex;gap:12px;justify-content:space-between;align-items:center;flex-wrap:wrap}}
.evidence-slide header b{{font-size:12.5px;font-weight:650;color:var(--ink)}}
.evidence-slide header p{{margin:1px 0 0;color:var(--muted);font-size:10.5px}}
.evidence-slide>.badge{{position:absolute;top:12px;left:14px;z-index:3;display:block;width:max-content;margin:0;background:var(--amber-soft);color:var(--amber);border:1px solid #e7d3ac}}
.recommendation-visual .decision-media{{order:1;height:320px;max-height:none;min-height:0;overflow:hidden;display:block;background:#efece3;border:1px solid var(--line);border-radius:10px}}
.recommendation-visual .decision-media img,.recommendation-visual .decision-media video{{width:100%;height:100%;max-height:none;object-fit:cover;object-position:top;display:block}}
.recommendation-visual .evidence-missing{{height:320px;display:grid;place-items:center;color:var(--muted);background:#efece3;border:1px solid var(--line);border-radius:10px}}
.evidence-notes{{order:3;display:flex;gap:16px;padding:2px 2px 6px;background:transparent;border:0}}
.evidence-notes p{{margin:0;color:var(--muted);font-size:11px;line-height:1.5}}
.evidence-notes b{{color:var(--body-c);font-weight:650}}
.evidence-controls{{position:static;height:0;padding:0;background:transparent;display:block}}
.evidence-controls span{{position:absolute;top:14px;right:30px;z-index:4;background:rgba(34,33,29,.75);color:#fff;padding:4px 10px;border-radius:999px;font-size:11px}}
.evidence-controls .previous-evidence,.evidence-controls .next-evidence{{position:absolute;top:150px;width:38px;height:38px;padding:0;border-radius:50%;background:rgba(255,255,255,.95);color:var(--ink);border:1px solid var(--line);font-size:15px;z-index:4;box-shadow:0 2px 10px rgba(40,30,10,.18);cursor:pointer}}
.evidence-controls .previous-evidence{{left:28px}}
.evidence-controls .next-evidence{{right:28px}}
.evidence-controls .previous-evidence:hover,.evidence-controls .next-evidence:hover{{background:#fff;border-color:#c8c2b2}}
a.live{{padding:6px 11px;background:var(--ink);color:#fff;border-radius:8px;font-size:11.5px;font-weight:650;text-decoration:none}}
.recommendation-body{{padding:6px 18px 16px}}
.fit-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}}
.fit-grid>div{{padding:12px;background:#f6f3ea;border:0;border-radius:10px}}
.fit-grid b{{font-size:12px}}
.fit-grid p{{margin:5px 0 0;font-size:12.5px;color:var(--body-c)}}
.fit-grid small{{display:block;margin-top:6px;color:var(--muted)}}
.recommendation-card h5{{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:14px 0 6px}}
.asset-list{{grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:6px}}
.asset-list li{{padding:9px 11px;border:1px solid var(--line);border-radius:9px;background:#fff}}
.asset-list b{{font-size:12px}}
.asset-list span{{font-size:11.5px;color:var(--body-c)}}
.asset-list small{{color:var(--muted);font-size:10.5px}}
.optional-parts{{margin:12px 0 0;border-top:1px solid var(--line);border-bottom:0}}
.optional-parts summary{{padding:10px 0 6px;font-size:12px;font-weight:550;color:var(--muted);cursor:pointer}}
.part-list{{padding-bottom:8px}}
.part-choice{{border-radius:7px;font-size:11.5px;padding:6px 10px;background:#fff;border:1px solid var(--line)}}
.part-choice[aria-pressed="true"]{{background:var(--ink);color:#fff;border-color:var(--ink)}}
.decision-actions{{position:sticky;bottom:10px;z-index:8;gap:6px;margin-top:12px;padding:10px;background:rgba(255,254,251,.97);border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 28px rgba(60,50,30,.16);backdrop-filter:blur(8px);align-items:center}}
.decision-actions .decision-action{{border-radius:8px;padding:8px 13px;font-size:12.5px;font-weight:600;background:#fff;border:1px solid var(--line)}}
.decision-actions .decision-action:hover{{border-color:#c8c2b2}}
.decision-actions .decision-action[aria-pressed="true"]{{background:var(--ink);border-color:var(--ink);color:#fff}}
.decision-actions .decision-action[data-status="selected"][aria-pressed="true"]{{background:var(--ok);border-color:var(--ok)}}
.decision-actions .decision-action[data-status="shortlisted"][aria-pressed="true"]{{background:#996c15;border-color:#996c15}}
.decision-actions .decision-action[data-status="not_using"][aria-pressed="true"]{{background:#757164;border-color:#757164}}
.request-action{{border-radius:8px;padding:7px 11px;font-size:11.5px;font-weight:550;background:#f3efe4;border:1px solid transparent;color:var(--body-c)}}
.request-action:hover{{background:#ece7d8}}
.request-action[data-request="component"]{{border:1px dashed #c8c2b2;background:#fff}}
.decision-actions textarea{{min-height:40px;margin-top:2px;background:#fff;border:1px solid var(--line);border-radius:9px;font-size:12.5px}}
.choice-state{{font-size:12px;font-weight:600;color:var(--muted);display:flex;align-items:center;gap:7px}}
.choice-state::before{{content:"";width:8px;height:8px;border-radius:50%;background:#cfc9ba;flex:none}}
.decision-actions:has(.decision-action[aria-pressed="true"]) .choice-state{{color:var(--ok)}}
.decision-actions:has(.decision-action[aria-pressed="true"]) .choice-state::before{{background:var(--ok)}}
.recommendation-nav{{margin:12px 0 0;padding:8px 12px;background:#efebe0;border-radius:10px;font-size:12px;color:var(--muted)}}
.recommendation-nav button{{border-radius:8px;background:#fff;border:1px solid var(--line);padding:7px 12px;font-size:12px;font-weight:600}}
dialog{{border-radius:16px}}
#decision-request-form{{padding:24px}}
#decision-request-form h3{{font-family:var(--font-display);font-size:20px;font-weight:600;margin:0 0 6px}}
#decision-request-form p{{color:var(--muted);font-size:13px}}
#decision-request-fields label span{{font-size:12px;font-weight:600}}
#decision-request-fields input,#decision-request-fields textarea{{border-radius:10px}}
.dialog-actions button{{border-radius:9px;padding:8px 14px;font-weight:600}}
.dialog-actions #decision-request-save{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.dependency-note{{background:#f4f4f5;color:#52525b;border:1px solid var(--line);border-radius:10px;font-size:12px;margin-top:10px}}
.review-mode :where(button,a,summary,input,textarea):focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
@media(max-width:1020px){{.review-mode main{{padding-left:0}}.review-mode main::before{{display:none}}.review-mode .review-header{{position:sticky;width:auto;right:0;border-right:0}}.decision-toolbar{{position:static;width:auto;display:flex;flex-direction:column;gap:8px;padding:10px 14px;border-bottom:1px solid var(--line)}}.review-stage-tabs{{flex-direction:row;overflow:auto}}.review-stage-tabs button{{white-space:nowrap}}.review-stage-tabs button::after{{display:none}}.review-stage-tabs button::before{{display:none}}.page-review-tabs{{position:static;width:auto;flex-direction:row;overflow-x:auto;border-top:0}}.page-review-tabs button{{white-space:nowrap}}.page-review-tabs button::before{{display:none}}.publish-actions{{position:static;width:auto;display:flex;flex-wrap:wrap;border-right:0}}.review-status{{position:static;width:auto;flex-direction:row;align-items:center;border-top:0}}.decision-block.active{{grid-template-columns:1fr}}.recommendation-visual .decision-media{{height:240px}}.fit-grid{{grid-template-columns:1fr}}}}
</style></head><body class="{body_class}">{HASH_PREFIX}{marker} -->{header}{f'<nav class="dashboard-tabs">{nav}</nav>' if nav else ''}<main>{panels}</main><script>
function swap(selector,panel,id){{document.querySelectorAll(selector).forEach(x=>x.classList.remove('active'));document.querySelectorAll(panel).forEach(x=>x.classList.remove('active'));const b=document.querySelector(`[data-${{selector.includes('concept')?'concept':'site'}}="${{id}}"]`);if(b)b.classList.add('active');const p=document.getElementById(id);if(p)p.classList.add('active')}}
document.querySelectorAll('nav button[data-tab]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('nav button,.panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.tab).classList.add('active')}}));
document.querySelectorAll('.concept-jump').forEach(b=>b.addEventListener('click',()=>swap('.concept-jump','.concept-panel',b.dataset.concept)));
document.querySelectorAll('.site-jump').forEach(b=>b.addEventListener('click',()=>swap('.site-jump','.site-panel',b.dataset.site)));
document.querySelectorAll('.review').forEach(r=>{{const key='project-dashboard-review:'+r.dataset.reviewKey;let saved={{}};try{{saved=JSON.parse(localStorage.getItem(key)||'{{}}')}}catch(e){{}}const t=r.querySelector('textarea');t.value=saved.note||'';r.querySelectorAll('button').forEach(b=>{{if(saved.verdict===b.dataset.verdict)b.setAttribute('aria-pressed','true');b.addEventListener('click',()=>{{saved.verdict=b.dataset.verdict;localStorage.setItem(key,JSON.stringify(saved));r.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}})}});t.addEventListener('input',()=>{{saved.note=t.value;localStorage.setItem(key,JSON.stringify(saved))}})}});
document.querySelectorAll('.review-stage-tab').forEach(button=>button.addEventListener('click',()=>{{document.querySelectorAll('.review-stage-tab,.review-stage').forEach(item=>item.classList.remove('active'));button.classList.add('active');document.getElementById(button.dataset.reviewStage)?.classList.add('active')}}));
document.querySelectorAll('.page-review-tab').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.page-review-tab,.page-review-panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.reviewPage).classList.add('active')}}));
document.querySelectorAll('.page-review-panel').forEach(panel=>{{const cards=[...panel.querySelectorAll('.recommendation-card')];let index=0;const show=next=>{{if(!cards.length)return;index=(next+cards.length)%cards.length;cards.forEach((card,i)=>card.classList.toggle('active',i===index))}};panel.querySelector('.previous-recommendation')?.addEventListener('click',()=>show(index-1));panel.querySelector('.next-recommendation')?.addEventListener('click',()=>show(index+1))}});
{{const shell=document.querySelector('.shell-review'),cards=[...(shell?.querySelectorAll('.recommendation-card')||[])];let index=0;const show=next=>{{if(!cards.length)return;index=(next+cards.length)%cards.length;cards.forEach((card,i)=>card.classList.toggle('active',i===index))}};shell?.querySelector('.previous-shell-recommendation')?.addEventListener('click',()=>show(index-1));shell?.querySelector('.next-shell-recommendation')?.addEventListener('click',()=>show(index+1))}}
document.querySelectorAll('[data-evidence-carousel]').forEach(carousel=>{{const slides=[...carousel.querySelectorAll('.evidence-slide')],position=carousel.querySelector('.evidence-position');let index=0;const show=next=>{{if(!slides.length)return;index=(next+slides.length)%slides.length;slides.forEach((slide,i)=>slide.classList.toggle('active',i===index));if(position)position.textContent=String(index+1)}};carousel.querySelector('.previous-evidence')?.addEventListener('click',()=>show(index-1));carousel.querySelector('.next-evidence')?.addEventListener('click',()=>show(index+1))}});
const recommendationNode=document.getElementById('page-recommendation-data');
if(recommendationNode){{
 const packetPath='brain/research/ui-decision-draft.json';const source=JSON.parse(recommendationNode.textContent);const checkoutIdentity=source.checkout?.checkout_root||'unknown-checkout',reviewKey='project-dashboard-page-decisions:'+checkoutIdentity+':'+source.mission_id,requestKey=reviewKey+':requests';let review={{}},requests=[];try{{review=JSON.parse(localStorage.getItem(reviewKey)||'{{}}')}}catch(e){{review={{}}}}try{{requests=JSON.parse(localStorage.getItem(requestKey)||'[]')}}catch(e){{requests=[]}}
 const message=document.getElementById('decision-message'),count=document.getElementById('decision-count'),submitButton=document.getElementById('submit-decisions'),updateButton=document.getElementById('update-decisions');let submitted=false;
 const saveLocal=()=>{{localStorage.setItem(reviewKey,JSON.stringify(review));localStorage.setItem(requestKey,JSON.stringify(requests))}};
 const updateNav=()=>{{const navDirectionId=source.site_direction?.recommendation_id;const shellIds=(source.global_shell?.recommendations||[]).map(item=>item.recommendation_id);document.querySelectorAll('.page-review-tab').forEach(tab=>{{const panel=document.getElementById(tab.dataset.reviewPage);if(!panel)return;const ids=[...panel.querySelectorAll('.decision-actions')].map(group=>group.dataset.recommendationId);tab.classList.toggle('decided',ids.some(id=>review[id]?.status))}});const pagesDone=[...document.querySelectorAll('.page-review-panel')].every(panel=>[...panel.querySelectorAll('.decision-actions')].some(group=>review[group.dataset.recommendationId]?.status));document.querySelectorAll('.review-stage-tab').forEach(tab=>{{const stage=tab.dataset.reviewStage;const done=stage==='direction-stage'?Boolean(review[navDirectionId]?.status):stage==='shell-stage'?(shellIds.length===0||shellIds.every(id=>review[id]?.status)):pagesDone;tab.classList.toggle('decided',done)}})}};
 const refresh=()=>{{document.querySelectorAll('.decision-actions').forEach(group=>{{const saved=review[group.dataset.recommendationId]||{{}};group.querySelectorAll('.decision-action').forEach(button=>button.setAttribute('aria-pressed',String(saved.status===button.dataset.status)));group.closest('.recommendation-body')?.querySelectorAll('.part-choice').forEach(button=>button.setAttribute('aria-pressed',String((saved.selected_parts||[]).includes(button.dataset.part))));group.querySelector('textarea').value=saved.note||'';group.querySelector('.choice-state').textContent=saved.status?`Choice: ${{saved.status.replaceAll('_',' ')}}`:'No choice recorded.'}});count.textContent=`${{Object.keys(review).length}} choices · ${{requests.length}} requests saved in this browser`;updateNav()}};
 document.querySelectorAll('.decision-actions').forEach(group=>{{group.querySelectorAll('.decision-action').forEach(button=>button.addEventListener('click',()=>{{const previous=review[group.dataset.recommendationId]||{{}};review[group.dataset.recommendationId]={{...previous,status:button.dataset.status,candidate_ids:[group.dataset.recommendationId],scope:group.dataset.scope,target_id:group.dataset.targetId,note:group.querySelector('textarea').value||''}};saveLocal();refresh()}}));group.querySelector('textarea').addEventListener('input',event=>{{if(!review[group.dataset.recommendationId])return;review[group.dataset.recommendationId].note=event.target.value;saveLocal()}});group.closest('.recommendation-body')?.querySelectorAll('.part-choice').forEach(button=>button.addEventListener('click',()=>{{const saved=review[group.dataset.recommendationId]||{{status:'shortlisted',candidate_ids:[group.dataset.recommendationId],scope:group.dataset.scope,target_id:group.dataset.targetId,note:''}},parts=new Set(saved.selected_parts||[]);parts.has(button.dataset.part)?parts.delete(button.dataset.part):parts.add(button.dataset.part);saved.selected_parts=[...parts];review[group.dataset.recommendationId]=saved;saveLocal();refresh()}}))}});
 const normalizeScope=value=>({{'whole-page':'whole_page','connected-sections':'connected_sections','one-section':'section','repeated-page-family':'page_family','global-shell':'global_shell'}}[value]||value);
 const buildPacket=()=>{{const targetResults=new Map((source.targets||[]).map(target=>[target.target_id,target]));const pages=(source.input.targets||[]).map(target=>{{const recs=(targetResults.get(target.target_id)||{{recommendations:[]}}).recommendations||[];return{{id:target.target_id,family_id:target.family_id,label:target.label,decisions:recs.filter(rec=>review[rec.recommendation_id]).map(rec=>({{...review[rec.recommendation_id],id:rec.recommendation_id,scope:normalizeScope(rec.scope),affected_blocks:(review[rec.recommendation_id].selected_parts?.length?review[rec.recommendation_id].selected_parts:rec.affected_blocks)||[]}}))}}}});const directionId=source.site_direction?.recommendation_id;const shellSource=source.global_shell||{{target_id:'global-shell',state:'not_needed',recommendations:[]}},shellRecommendations=shellSource.recommendations||[],shell=shellRecommendations.filter(item=>review[item.recommendation_id]).map(item=>({{...review[item.recommendation_id],recommendation_id:item.recommendation_id,scope:'global_shell'}}));const assets=[],assetKeys=new Set();(source.targets||[]).forEach(target=>(target.recommendations||[]).forEach(rec=>{{const choice=review[rec.recommendation_id];if(choice?.status==='selected')(rec.asset_requirements||[]).forEach(asset=>{{const key=`${{target.target_id}}:${{rec.recommendation_id}}:${{asset.asset_id}}`;if(!assetKeys.has(key)){{assetKeys.add(key);assets.push({{...asset,target_id:target.target_id,recommendation_id:rec.recommendation_id}})}}}})}}));const focused=requests.filter(item=>item.kind==='research'),provided=[...(source.input.reference_scope?.urls||[]).map(url=>({{live_url:url,source:'initial-research-scope'}})),...requests.filter(item=>item.kind==='reference')],deferred=requests.filter(item=>item.kind==='component').map(item=>({{...item,kind:'bring_own_component',status:'awaiting_active_page'}}));return{{schema_version:1,project:{{name:source.project}},research:{{mission_id:source.mission_id,mode:source.entry_mode,evidence_readiness:source.evidence_readiness,derived_path:source.derived_path,documented_gaps:source.unresolved_gaps||[]}},site_direction:{{recommendation_id:directionId,...(review[directionId]||{{}})}},global_shell:{{target_id:'global-shell',state:shellSource.state||'not_needed',recommendations:shellRecommendations,decisions:shell}},page_families:source.input.page_families||[],pages,asset_requirements:assets,focused_research_requests:focused,provided_references:provided,deferred_component_intents:deferred}}}};
 const requestDialog=document.getElementById('decision-request-dialog'),requestForm=document.getElementById('decision-request-form'),requestFields=document.getElementById('decision-request-fields');let pendingRequest=null;
 document.querySelectorAll('.request-action').forEach(button=>button.addEventListener('click',()=>{{const group=button.closest('.decision-actions'),kind=button.dataset.request,selectedBlocks=[...group.closest('.recommendation-body').querySelectorAll('.part-choice[aria-pressed="true"]')].map(item=>item.dataset.part);let defaultBlocks=[];try{{defaultBlocks=JSON.parse(group.dataset.affectedBlocks||'[]')}}catch(error){{defaultBlocks=[]}}pendingRequest={{kind,target_id:group.dataset.targetId,recommendation_id:group.dataset.recommendationId,scope:normalizeScope(group.dataset.scope),affected_blocks:selectedBlocks.length?selectedBlocks:defaultBlocks}};const titles={{research:'Research another pattern',reference:'Bring your own reference',component:'Bring your own component later'}},copies={{research:'Describe what the current recommendations fail to solve. This creates one focused Aside request, not a new broad research round.',reference:'Paste the exact page URL and explain the exact part you liked. Claude or Codex will not assume you want the whole website.',component:'This records a reminder for this exact page or section. You will provide the component only when Build Page reaches it—nothing is uploaded or requested now.'}};document.getElementById('decision-request-title').textContent=titles[kind];document.getElementById('decision-request-copy').textContent=copies[kind];requestFields.innerHTML=kind==='research'?'<label><span>What is missing?</span><textarea name="missing_need" required></textarea></label>':kind==='reference'?'<label><span>Exact website or page URL</span><input name="live_url" type="url" required></label><label><span>What exactly did you like?</span><textarea name="liked_part" required></textarea></label>':'<label><span>Optional reminder for later</span><textarea name="note" placeholder="For example: I have a booking strip component to show you."></textarea></label>';requestDialog.showModal()}}));
 requestForm.addEventListener('submit',event=>{{if(event.submitter?.value!=='save'||!pendingRequest)return;event.preventDefault();const data=Object.fromEntries(new FormData(requestForm));requests.push({{...pendingRequest,...data,created_at:new Date().toISOString()}});if(pendingRequest.kind==='research'){{const saved=review[pendingRequest.recommendation_id]||{{candidate_ids:[pendingRequest.recommendation_id],scope:pendingRequest.scope,target_id:pendingRequest.target_id,note:''}};saved.status='needs_more_research';review[pendingRequest.recommendation_id]=saved}}saveLocal();requestDialog.close();requestForm.reset();pendingRequest=null;refresh();message.textContent='Focused request saved locally. Submit or Update to relay it to Claude or Codex.'}});
 const incomplete=packet=>{{if(!packet.site_direction.status)return 'Review the site-wide direction.';if(packet.global_shell.state!=='not_needed'&&(packet.global_shell.recommendations||[]).some(item=>!review[item.recommendation_id]))return 'Review every global-shell option.';const missing=packet.pages.find(page=>!page.decisions.length);return missing?`Review ${{missing.label||missing.id}}.`:''}};
 const exportPacket=()=>{{const packet=buildPacket(),blob=new Blob([JSON.stringify(packet,null,2)+'\\n'],{{type:'application/json'}}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='ui-decision-draft.json';link.click();URL.revokeObjectURL(link.href);message.textContent='Exported the provisional relay. It is not canon.'}};
 const copyPacket=async()=>{{try{{await navigator.clipboard.writeText(JSON.stringify(buildPacket(),null,2));message.textContent='Copied the provisional relay for Claude or Codex.'}}catch(error){{message.textContent='Clipboard access is unavailable here. Use Export JSON instead.'}}}};
 const persist=async action=>{{const packet=buildPacket(),problem=incomplete(packet);if(problem){{message.textContent=problem;return}}const config=window.__PROJECT_DASHBOARD_SERVER__;if(!config){{message.textContent='Static HTML cannot write project files. Use Export JSON or Copy relay.';return}}try{{const response=await fetch(`${{config.url}}/api/${{action}}`,{{method:'POST',headers:{{'Content-Type':'application/json','X-Project-Dashboard-Token':config.token}},body:JSON.stringify(packet)}}),result=await response.json();if(!response.ok)throw new Error(result.error||'Request failed');submitted=true;submitButton.disabled=true;updateButton.disabled=false;message.textContent=`Revision ${{result.submission.revision}} submitted for agent review. Build remains locked.`}}catch(error){{message.textContent=error.message}}}};
 document.getElementById('review-decisions').addEventListener('click',()=>{{const packet=buildPacket(),problem=incomplete(packet),selected=packet.pages.flatMap(page=>page.decisions.map(decision=>`${{page.label||page.id}} · ${{decision.status}} · ${{decision.id}}`));message.textContent=problem||`Ready to submit: ${{selected.length}} page choices, ${{packet.focused_research_requests.length}} focused requests, ${{packet.provided_references.length}} references, ${{packet.deferred_component_intents.length}} components to provide later.`}});document.getElementById('export-decisions').addEventListener('click',exportPacket);document.getElementById('copy-decisions').addEventListener('click',copyPacket);submitButton.addEventListener('click',()=>persist('submit'));updateButton.addEventListener('click',()=>persist('update'));
 const config=window.__PROJECT_DASHBOARD_SERVER__;if(config)fetch(`${{config.url}}/api/state`,{{headers:{{'X-Project-Dashboard-Token':config.token}}}}).then(response=>response.json()).then(state=>{{if(!state.packet)return;submitted=true;submitButton.disabled=true;updateButton.disabled=false;const packet=state.packet;const decisions=[packet.site_direction,...(packet.global_shell?.decisions||[]),...(packet.pages||[]).flatMap(page=>page.decisions||[])];decisions.filter(Boolean).forEach(item=>{{const id=item.id||item.recommendation_id||(item.candidate_ids||[])[0];if(id)review[id]={{status:item.status,candidate_ids:item.candidate_ids||[id],scope:item.scope,target_id:item.target_id,note:item.note||''}}}});requests=[...(packet.focused_research_requests||[]).map(item=>({{...item,kind:'research'}})),...(packet.provided_references||[]).filter(item=>item.source!=='initial-research-scope').map(item=>({{...item,kind:'reference'}})),...(packet.deferred_component_intents||[]).map(item=>({{...item,kind:'component'}}))];localStorage.setItem(reviewKey,JSON.stringify(review));localStorage.setItem(requestKey,JSON.stringify(requests));refresh();message.textContent=`Loaded submitted revision ${{packet.submission.revision}}. Build remains locked pending agent review.`}}).catch(()=>{{message.textContent='Could not load server state. Browser choices remain local.'}});
 document.addEventListener('keydown',event=>{{if(event.target.closest('textarea,input,dialog'))return;if(event.key!=='ArrowLeft'&&event.key!=='ArrowRight')return;const stage=document.querySelector('.review-stage.active');if(!stage)return;const scopeNode=stage.querySelector('.page-review-panel.active')||stage;const card=scopeNode.querySelector('.recommendation-card.active')||scopeNode;const carousel=card.querySelector('[data-evidence-carousel]');carousel?.querySelector(event.key==='ArrowLeft'?'.previous-evidence':'.next-evidence')?.click()}});
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
