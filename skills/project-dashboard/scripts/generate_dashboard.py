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
    tabs["Research / Moodboard"] = f'<section class="research-section"><h3>Choose or blend a concept</h3>{concepts_html(concepts, selection)}</section><section class="research-section"><h3>Inspect evidence one site at a time</h3>{sites_html(root, output, sites, portable)}</section>'
    tabs["Build Progress"] = progress_html(root, paths)
    nav = "".join(f'<button data-tab="t{i}" class="{"active" if i == 0 else ""}">{html.escape(name)}</button>' for i, name in enumerate(tabs))
    panels = "".join(f'<section id="t{i}" class="panel {"active" if i == 0 else ""}"><h2>{html.escape(name)}</h2>{content}</section>' for i, (name, content) in enumerate(tabs.items()))
    mode = "portable" if portable else "local"
    title = html.escape(root.name)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Project Dashboard</title><style>
:root{{--bg:#f4f1ea;--panel:#fffdf8;--ink:#1d1b18;--muted:#706b63;--line:#d9d2c7;--accent:#8a3d24;--warn:#9a5b10}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,sans-serif}}body>header{{padding:32px clamp(20px,5vw,72px);border-bottom:1px solid var(--line)}}h1{{margin:0;font:700 clamp(30px,5vw,58px)/1.05 ui-serif,Georgia,serif}}h2{{font-size:clamp(28px,4vw,48px)}}h3{{line-height:1.15}}p{{color:var(--muted)}}nav{{display:flex;gap:8px;overflow:auto;padding:16px clamp(20px,5vw,72px);position:sticky;top:0;background:rgba(244,241,234,.94);backdrop-filter:blur(12px);z-index:3}}button{{border:1px solid var(--line);background:var(--panel);padding:10px 14px;border-radius:999px;cursor:pointer}}nav button{{white-space:nowrap}}button.active,button[aria-pressed="true"]{{background:var(--ink);color:white}}main{{padding:12px clamp(20px,5vw,72px) 80px}}.panel,.concept-panel,.site-panel{{display:none}}.panel.active,.concept-panel.active,.site-panel.active{{display:block}}.summary-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}.summary-card,.design-preview,.concept-panel,.site-panel,.selection-status{{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:0 8px 30px rgba(50,40,25,.05)}}.summary-card ul{{padding-left:20px}}.source,.eyebrow{{text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-size:11px}}.design-preview h3,.concept-panel h3,.site-panel h3{{font-size:clamp(32px,5vw,70px);margin:10px 0 22px}}.swatches{{display:flex;flex-wrap:wrap;gap:10px}}.swatches span{{display:grid;gap:5px;font-size:11px}}.swatches i{{width:78px;height:58px;border-radius:10px;background:var(--swatch);border:1px solid var(--line)}}.empty{{padding:36px;border:1px dashed var(--line);border-radius:18px;color:var(--muted)}}.research-section{{margin:36px 0 70px}}.research-section>h3{{font-size:clamp(24px,3vw,40px)}}.selection-status{{display:flex;justify-content:space-between;gap:16px;margin-bottom:16px}}.selection-status.pending{{border-color:#d5a562;background:#fff8e8}}.selection-status span{{color:var(--muted)}}.concept-layout,.site-layout{{display:grid;grid-template-columns:minmax(190px,260px) minmax(0,1fr);gap:18px}}aside{{display:flex;flex-direction:column;gap:8px;align-self:start;position:sticky;top:88px}}aside button{{text-align:left;border-radius:12px}}dl>div{{display:grid;grid-template-columns:150px 1fr;gap:18px;border-top:1px solid var(--line);padding:13px 0}}dt{{font-weight:700}}dd{{margin:0}}.live-links,.site-panel header{{display:flex;gap:12px;justify-content:space-between;align-items:center;flex-wrap:wrap}}a.live,.live-links a{{display:inline-flex;padding:10px 14px;background:var(--ink);color:white;border-radius:999px;text-decoration:none}}.review{{margin-top:28px;padding-top:20px;border-top:1px solid var(--line);display:flex;gap:8px;align-items:center;flex-wrap:wrap}}.review span{{font-weight:700}}textarea{{width:100%;min-height:90px;margin-top:8px;border:1px solid var(--line);border-radius:12px;padding:12px;font:inherit}}.evidence-stack{{display:grid;gap:24px;margin-top:18px}}figure{{margin:0;background:#111;border-radius:15px;overflow:hidden}}figure img,figure video{{display:block;width:100%;height:auto;max-height:78vh;object-fit:contain;background:#111}}figcaption{{padding:10px;background:var(--panel);color:var(--muted);font-size:12px}}.badge{{display:inline-block;padding:4px 8px;border-radius:999px;margin-right:8px;font-size:11px;font-weight:700}}.badge.ok{{background:#e7f3e8;color:#255c2a}}.badge.warn{{background:#fff0d4;color:#80500b}}.badge.bad{{background:#f9dddd;color:#8b2525}}@media(max-width:760px){{.concept-layout,.site-layout{{grid-template-columns:1fr}}aside{{position:static;display:flex;flex-direction:row;overflow:auto}}aside button{{white-space:nowrap}}dl>div{{grid-template-columns:1fr;gap:3px}}.selection-status{{display:grid}}}}
</style></head><body>{HASH_PREFIX}{marker} --><header><h1>{title}</h1><p>Concise visual projection of Markdown canon · {mode} assets · {len(paths)} hashed inputs</p></header><nav>{nav}</nav><main>{panels}</main><script>
function swap(selector,panel,id){{document.querySelectorAll(selector).forEach(x=>x.classList.remove('active'));document.querySelectorAll(panel).forEach(x=>x.classList.remove('active'));const b=document.querySelector(`[data-${{selector.includes('concept')?'concept':'site'}}="${{id}}"]`);if(b)b.classList.add('active');const p=document.getElementById(id);if(p)p.classList.add('active')}}
document.querySelectorAll('nav button[data-tab]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('nav button,.panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.tab).classList.add('active')}}));
document.querySelectorAll('.concept-jump').forEach(b=>b.addEventListener('click',()=>swap('.concept-jump','.concept-panel',b.dataset.concept)));
document.querySelectorAll('.site-jump').forEach(b=>b.addEventListener('click',()=>swap('.site-jump','.site-panel',b.dataset.site)));
document.querySelectorAll('.review').forEach(r=>{{const key='project-dashboard-review:'+r.dataset.reviewKey;let saved={{}};try{{saved=JSON.parse(localStorage.getItem(key)||'{{}}')}}catch(e){{}}const t=r.querySelector('textarea');t.value=saved.note||'';r.querySelectorAll('button').forEach(b=>{{if(saved.verdict===b.dataset.verdict)b.setAttribute('aria-pressed','true');b.addEventListener('click',()=>{{saved.verdict=b.dataset.verdict;localStorage.setItem(key,JSON.stringify(saved));r.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}})}});t.addEventListener('input',()=>{{saved.note=t.value;localStorage.setItem(key,JSON.stringify(saved))}})}});
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
