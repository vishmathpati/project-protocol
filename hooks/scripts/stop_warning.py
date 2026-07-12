#!/usr/bin/env python3
"""Warn only when the checkout likely contains unpersisted session state."""

from __future__ import annotations

import subprocess
from pathlib import Path


status = subprocess.run(["git", "status", "--porcelain"], text=True, capture_output=True, check=False).stdout.splitlines()
worklog = Path("brain/WORKLOG.md")
meaningful = False
if worklog.is_file():
    meaningful = any(line.strip() and not line.lstrip().startswith("#") and "Temporary recovery buffer" not in line for line in worklog.read_text(errors="replace").splitlines())
if status or meaningful:
    parts = []
    if status:
        parts.append(f"{len(status)} dirty/untracked path(s)")
    if meaningful:
        parts.append("WORKLOG recovery entries")
    print("[project-protocol] Possible unpersisted state: " + " and ".join(parts) + ". Run /save-session if this work should be closed.")
