#!/usr/bin/env python3
"""Read-only Project Protocol migration planner and v5 target validator."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED = (
    "CLAUDE.md", "brain/BRIEF.md", "brain/STATUS.md", "brain/STRUCTURE.md",
    "brain/WORKLOG.md", "brain/CHANGELOG.md", "brain/agenda.md",
    "brain/WONT-DO.md", "brain/chapters/README.md", "brain/chapters/_TEMPLATE.md",
)
LEGACY_DIRS = ("cowork", "agents", "human")
RETIRED_FILES = ("brain/SITUATIONS.md", "brain/CLAUDE.md")
RETIRED_SKILLS = ("session-recap", "audit-before-close", "discussion-mode", "discipline")


def version_key(value: str) -> tuple[int, int, int]:
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", value or "")
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


def inspect(project: Path, plugin: Path, validate: bool) -> tuple[dict, int]:
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    target = manifest["version"]
    version_file = project / "brain/.plugin-version"
    current = version_file.read_text().strip() if version_file.exists() else "pre-2.5.0"
    legacy = [name for name in LEGACY_DIRS if (project / name).exists()]
    manifests = []
    for path in sorted((plugin / "migrations").glob("v*.md"), key=lambda p: version_key(p.name)):
        version = re.search(r"v(\d+\.\d+\.\d+)", path.name).group(1)
        if version_key(current) < version_key(version) <= version_key(target):
            manifests.append({"version": version, "path": str(path)})

    problems: list[dict[str, str]] = []
    if validate:
        for relative in REQUIRED:
            if not (project / relative).is_file():
                problems.append({"code": "missing-required", "path": relative})
        for relative in RETIRED_FILES:
            if (project / relative).exists():
                problems.append({"code": "retired-file", "path": relative})
        if legacy:
            problems.append({"code": "legacy-layout", "path": ",".join(legacy)})
        claude = (project / "CLAUDE.md").read_text(errors="ignore") if (project / "CLAUDE.md").exists() else ""
        for skill in RETIRED_SKILLS:
            if re.search(rf"(?<![\w-]){re.escape(skill)}(?![\w-])", claude):
                problems.append({"code": "retired-route", "path": f"CLAUDE.md:{skill}"})

    result = {
        "project_root": str(project), "plugin_root": str(plugin),
        "current_version": current, "target_version": target,
        "layout": "legacy" if legacy else "brain" if (project / "brain").is_dir() else "uninitialized",
        "legacy_directories": legacy, "pending_manifests": manifests,
        "validation": {"requested": validate, "ok": validate and not problems, "problems": problems},
        "mutated": False,
    }
    return result, 1 if validate and problems else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--plugin-root", required=True, type=Path)
    parser.add_argument("--validate-target", action="store_true")
    args = parser.parse_args()
    result, code = inspect(args.project_root.resolve(), args.plugin_root.resolve(), args.validate_target)
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
