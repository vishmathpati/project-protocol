#!/usr/bin/env python3
"""Deterministic post-write UI findings and routing reminders."""

from __future__ import annotations

import os
import re
from pathlib import Path


raw = os.environ.get("TOOL_INPUT_FILE_PATH") or os.environ.get("TOOL_INPUT_PATH") or ""
if not raw:
    raise SystemExit(0)
path = Path(raw)
normalized = path.as_posix()
if any(part in normalized for part in ("/node_modules/", "/.git/", "/dist/", "/build/", "/.next/")):
    raise SystemExit(0)

if normalized.endswith("/brain/DESIGN.md") or normalized == "brain/DESIGN.md":
    print("[project-protocol] DESIGN changed: run Style Lock synchronization (lint → safe export into the actual theme target → render verification).")
    raise SystemExit(0)

ui_suffixes = {".tsx", ".jsx", ".vue", ".svelte", ".swift", ".css", ".scss"}
ui_file = path.suffix.lower() in ui_suffixes or any(part in normalized for part in ("/components/", "/styles/", "tailwind.config"))
if not ui_file:
    raise SystemExit(0)

print(f"[project-protocol] UI changed: {raw}. Run Design Check postflight on the changed hunks and rendered surface.")
if not path.is_file():
    raise SystemExit(0)

try:
    text = path.read_text(errors="replace")
except OSError:
    raise SystemExit(0)

shadcn = Path("components.json").is_file() or any(p.is_file() for p in Path.cwd().glob("*/components.json"))
for number, line in enumerate(text.splitlines(), 1):
    findings = []
    if re.search(r"#[0-9a-fA-F]{3,8}", line) and "var(--" not in line:
        findings.append("raw hex")
    if path.suffix.lower() in {".tsx", ".jsx", ".vue", ".svelte", ".swift"} and re.search(r"(?<![\w-])\d+px", line):
        findings.append("raw px")
    if "font-family:" in line:
        findings.append("raw font-family")
    if re.search(r"<(div|span)\s+[^>]*onClick", line):
        findings.append("clickable div/span")
    if "outline: none" in line:
        findings.append("outline removed")
    if shadcn and re.search(r"<(select|dialog)\b", line, re.I):
        findings.append("native primitive while shadcn is configured")
    if findings:
        print(f"[project-protocol design-scan] {raw}:{number} — {', '.join(findings)}")
