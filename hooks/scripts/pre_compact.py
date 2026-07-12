#!/usr/bin/env python3
"""Emit compact recovery context without creating backup files."""

from __future__ import annotations

import subprocess
from pathlib import Path


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


print(f"[project-protocol] PreCompact · branch: {git('rev-parse', '--abbrev-ref', 'HEAD')} · root: {git('rev-parse', '--show-toplevel')}")
worklog = Path("brain/WORKLOG.md")
if worklog.is_file():
    lines = [line for line in worklog.read_text(errors="replace").splitlines() if line.strip()]
    if lines:
        print("[project-protocol] Useful WORKLOG tail:")
        print("\n".join(lines[-40:]))
print("[project-protocol] After compaction, continue the human-invoked role and run /recap before acting.")
