#!/usr/bin/env python3
"""Structural release validator for the current plugin source."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED_HOOKS = {"SessionStart", "PreCompact", "PostCompact", "Stop", "PostToolUse"}
RETIRED_DIRS = {"session-recap", "audit-before-close", "audit", "discipline", "discussion-mode", "calibrate", "design-direction"}


def main() -> int:
    errors: list[str] = []
    manifests = [ROOT / ".claude-plugin/plugin.json", ROOT / ".codex-plugin/plugin.json", ROOT / ".claude-plugin/marketplace.json"]
    parsed = []
    for path in manifests:
        try:
            parsed.append(json.loads(path.read_text()))
        except Exception as exc:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    if len(parsed) == 3:
        versions = [parsed[0].get("version"), parsed[1].get("version"), parsed[2].get("plugins", [{}])[0].get("version")]
        if len(set(versions)) != 1:
            errors.append(f"manifest version drift: {versions}")
        elif not (ROOT / f"migrations/v{versions[0]}.md").is_file():
            errors.append(f"missing migrations/v{versions[0]}.md")

    skill_dirs = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
    for directory in skill_dirs:
        skill = directory / "SKILL.md"
        sidecar = directory / "agents/openai.yaml"
        if not skill.is_file():
            errors.append(f"missing {skill.relative_to(ROOT)}")
            continue
        text = skill.read_text()
        match = re.match(r"---\n(.*?)\n---", text, re.S)
        name = re.search(r"^name:\s*(.+)$", match.group(1), re.M).group(1).strip() if match and re.search(r"^name:\s*(.+)$", match.group(1), re.M) else None
        if name != directory.name:
            errors.append(f"skill name mismatch {directory.name}: {name}")
        if len(text.splitlines()) > 500:
            errors.append(f"skill exceeds 500 lines: {directory.name}")
        if re.search(r"\bTODO\b", text, re.I):
            errors.append(f"TODO in skill: {directory.name}")
        if not sidecar.is_file():
            errors.append(f"missing {sidecar.relative_to(ROOT)}")
        else:
            metadata = sidecar.read_text()
            for field in ("display_name:", "short_description:", "default_prompt:"):
                if field not in metadata:
                    errors.append(f"missing {field[:-1]} in {sidecar.relative_to(ROOT)}")
    for directory in RETIRED_DIRS:
        if (ROOT / "skills" / directory).exists():
            errors.append(f"retired skill directory remains: {directory}")

    hooks_path = ROOT / "hooks/hooks.json"
    try:
        hooks = json.loads(hooks_path.read_text())
        events = set(hooks.get("hooks", {}))
        if not events <= APPROVED_HOOKS:
            errors.append(f"unapproved hook events: {sorted(events - APPROVED_HOOKS)}")
        for match in re.findall(r"\$\{?PLUGIN_ROOT\}?/([^\s\"']+)", hooks_path.read_text()):
            target = match.rstrip("\\")
            if not (ROOT / target).exists():
                errors.append(f"hook target missing: {target}")
    except Exception as exc:
        errors.append(f"invalid hooks/hooks.json: {exc}")

    current_files = [ROOT / "README.md", ROOT / "hooks"] + skill_dirs
    retired_terms = ("brain/SITUATIONS.md",)
    for item in current_files:
        paths = [item] if item.is_file() else list(item.rglob("*.md")) + list(item.rglob("*.json"))
        for path in paths:
            text = path.read_text(errors="ignore")
            for term in retired_terms:
                if term in text and "migrate-to-brain" not in str(path):
                    errors.append(f"retired current-source reference {term}: {path.relative_to(ROOT)}")
    debris_roots = (ROOT / "skills", ROOT / "hooks", ROOT / "scripts", ROOT / "templates", ROOT / "aside-skill", ROOT / "tests")
    if (ROOT / ".DS_Store").exists():
        errors.append("packaging debris: .DS_Store")
    for base in debris_roots:
        if base.is_dir():
            for debris in list(base.rglob(".DS_Store")) + list(base.rglob("__pycache__")):
                errors.append(f"packaging debris: {debris.relative_to(ROOT)}")

    if errors:
        print("Structural audit failed:")
        for error in sorted(set(errors)):
            print(f"  - {error}")
        return 1
    print(f"Structural audit passed: {len(skill_dirs)} skills, manifests aligned, hooks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
