#!/usr/bin/env python3
"""Minimal session reminder plus deterministic plugin-version drift check."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from private_canon import attach


def version(value: str) -> tuple[int, int, int]:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", value.strip())
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


root_value = os.environ.get("CODEX_PLUGIN_ROOT") or os.environ.get("CLAUDE_PLUGIN_ROOT")
plugin_root = Path(root_value) if root_value else Path(__file__).resolve().parents[2]
project_root = Path.cwd()

print("[project-protocol] Invoke /ceo, /worker, or /solo; that role runs /recap from live Git and canon.")

private = attach(project_root)
if private.canon_root:
    if private.conflicts:
        print("[project-protocol] Private canon needs attention: " + "; ".join(private.conflicts))
    else:
        print(f"[project-protocol] Private canon attached: {private.canon_root}")

try:
    plugin_version = json.loads((plugin_root / ".claude-plugin" / "plugin.json").read_text())["version"]
except (OSError, KeyError, json.JSONDecodeError):
    raise SystemExit(0)

version_file = project_root / "brain" / ".plugin-version"
project_version = version_file.read_text().strip() if version_file.is_file() else "pre-2.5.0"
skip_file = project_root / "brain" / ".plugin-version-skip"
if skip_file.is_file() and skip_file.read_text().strip() == plugin_version:
    raise SystemExit(0)
if version(project_version) < version(plugin_version):
    print(f"[project-protocol] Plugin drift: project {project_version} → plugin {plugin_version}. Run /migrate-project before protocol edits.")
