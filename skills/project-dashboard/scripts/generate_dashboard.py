#!/usr/bin/env python3
"""Deterministic Project Protocol dashboard generator (stdlib only)."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

GROUPS = {
    "Project": ["BRIEF.md", "STATUS.md", "STRUCTURE.md", "ROADMAP.md", "WONT-DO.md"],
    "Brand": ["BRAND.md", "marketing/CONTENT.md", "marketing/SITEMAP.md", "marketing/MEDIA.md"],
    "Design": ["DESIGN.md", "FUNDAMENTALS.md", "TASTE.md", "DISCOVERIES.md"],
}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
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
    paths.extend(p for p in (brain / "moodboard").rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS) if (brain / "moodboard").exists() else None
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


def markdown_card(root: Path, path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    body = html.escape(path.read_text(errors="replace"))
    return f'<article class="card"><h3>{html.escape(rel)}</h3><pre>{body}</pre></article>'


def image_src(output: Path, path: Path, portable: bool) -> str:
    if portable:
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"
    return Path(os.path.relpath(path, output.parent)).as_posix()


def research_html(root: Path, output: Path, paths: list[Path], portable: bool) -> str:
    docs = [p for p in paths if "/research/" in f"/{p.relative_to(root).as_posix()}" or p.name == "manifest.md"]
    images = [p for p in paths if p.suffix.lower() in IMAGE_EXTS]
    cards = "".join(markdown_card(root, p) for p in docs) or '<div class="empty">No UI research or moodboard manifest yet.</div>'
    gallery = []
    for p in images:
        src = image_src(output, p, portable)
        gallery.append(f'<figure><img loading="lazy" src="{html.escape(str(src))}" alt="Research capture {html.escape(p.stem)}"><figcaption>{html.escape(p.relative_to(root).as_posix())}</figcaption></figure>')
    return cards + (f'<div class="gallery">{"".join(gallery)}</div>' if gallery else "")


def build_progress(root: Path, paths: list[Path]) -> str:
    selected = []
    for path in paths:
        rel = f"/{path.relative_to(root).as_posix()}"
        is_real_chapter = "/chapters/" in rel and path.stem.lower() not in {"readme", "template", "_template"}
        if path.name in {"STATUS.md", "SITEMAP.md"} or is_real_chapter:
            selected.append(path)
    return "".join(markdown_card(root, p) for p in selected) or '<div class="empty">No chapters or sitemap yet.</div>'


def design_preview(root: Path) -> str:
    design = root / "brain" / "DESIGN.md"
    if not design.is_file():
        return ""
    text = design.read_text(errors="replace")
    values = []
    for value in re.findall(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", text):
        if value.lower() not in {v.lower() for v in values}:
            values.append(value)
    families = re.findall(r'^\s*family:\s*["\']?([^"\'\n#]+)', text, re.M)
    display = families[0].strip() if families else "Georgia"
    body = families[1].strip() if len(families) > 1 else "system-ui"
    swatch_html = '<div class="swatches">' + "".join(f'<span style="--swatch:{v}"><i></i><b>{v}</b></span>' for v in values[:32]) + '</div>' if values else '<p class="empty">No concrete color values yet.</p>'
    return f'''<article class="design-preview"><p class="eyebrow">Rendered design overview</p><h3 style="font-family:{html.escape(display)}">A brand should be felt before it is explained.</h3><p style="font-family:{html.escape(body)}">Body typography sample for navigation, content, forms, and supporting copy. If these fonts are installed or loaded by the project, this view renders them directly.</p>{swatch_html}</article>'''


def render(root: Path, output: Path, paths: list[Path], portable: bool) -> str:
    current = hashes(root, paths)
    marker = base64.urlsafe_b64encode(json.dumps(current, sort_keys=True, separators=(",", ":")).encode()).decode().rstrip("=")
    brain = root / "brain"
    tabs: dict[str, str] = {}
    for name, rels in GROUPS.items():
        present = [brain / rel for rel in rels if (brain / rel).is_file()]
        content = "".join(markdown_card(root, p) for p in present) or f'<div class="empty">No {name.lower()} canon yet.</div>'
        tabs[name] = (design_preview(root) + content) if name == "Design" else content
    tabs["Research / Moodboard"] = research_html(root, output, paths, portable)
    tabs["Build Progress"] = build_progress(root, paths)
    nav = "".join(f'<button data-tab="t{i}" class="{"active" if i == 0 else ""}">{html.escape(name)}</button>' for i, name in enumerate(tabs))
    panels = "".join(f'<section id="t{i}" class="panel {"active" if i == 0 else ""}"><h2>{html.escape(name)}</h2>{content}</section>' for i, (name, content) in enumerate(tabs.items()))
    mode = "portable" if portable else "local"
    title = html.escape(root.name)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Project Dashboard</title><style>
:root{{--bg:#f4f1ea;--panel:#fffdf8;--ink:#1d1b18;--muted:#706b63;--line:#d9d2c7;--accent:#8a3d24}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,sans-serif}}header{{padding:32px clamp(20px,5vw,72px);border-bottom:1px solid var(--line)}}h1{{margin:0;font:700 clamp(30px,5vw,58px)/1.05 ui-serif,Georgia,serif}}header p{{color:var(--muted)}}nav{{display:flex;gap:8px;overflow:auto;padding:16px clamp(20px,5vw,72px);position:sticky;top:0;background:rgba(244,241,234,.94);backdrop-filter:blur(12px);z-index:2}}button{{border:1px solid var(--line);background:var(--panel);padding:10px 14px;border-radius:999px;white-space:nowrap;cursor:pointer}}button.active{{background:var(--ink);color:white}}main{{padding:12px clamp(20px,5vw,72px) 80px}}.panel{{display:none}}.panel.active{{display:block}}.card,.design-preview{{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:20px;margin:16px 0;box-shadow:0 8px 30px rgba(50,40,25,.05)}}.design-preview h3{{font-size:clamp(32px,5vw,68px);line-height:1.02;max-width:900px;margin:10px 0 20px}}.design-preview p{{font-size:17px;max-width:720px}}.eyebrow{{text-transform:uppercase;letter-spacing:.14em;color:var(--muted);font-size:11px!important}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.55 ui-monospace,SFMono-Regular,monospace}}.empty{{padding:40px;border:1px dashed var(--line);border-radius:18px;color:var(--muted)}}.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}figure{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden}}img{{display:block;width:100%;height:220px;object-fit:cover}}figcaption{{padding:10px;color:var(--muted);font-size:12px}}.swatches{{display:flex;flex-wrap:wrap;gap:10px}}.swatches span{{display:grid;gap:5px;font-size:11px}}.swatches i{{width:70px;height:52px;border-radius:10px;background:var(--swatch);border:1px solid var(--line)}}
</style></head><body>{HASH_PREFIX}{marker} --><header><h1>{title}</h1><p>Generated from Markdown canon · {mode} assets · {len(paths)} hashed inputs</p></header><nav>{nav}</nav><main>{panels}</main><script>document.querySelectorAll('button[data-tab]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('button,.panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.tab).classList.add('active')}}));</script></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--output")
    parser.add_argument("--portable", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    output = Path(args.output).resolve() if args.output else root / "brain" / "project-dashboard.html"
    paths = collect(root)
    if args.check:
        old = read_embedded_hashes(output)
        current = hashes(root, paths)
        if old == current:
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
