#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSPECTOR = ROOT / "skills/migrate-project/scripts/inspect_migration.py"
REQUIRED = (
    "CLAUDE.md", "brain/BRIEF.md", "brain/STATUS.md", "brain/STRUCTURE.md",
    "brain/WORKLOG.md", "brain/CHANGELOG.md", "brain/agenda.md", "brain/WONT-DO.md",
    "brain/chapters/README.md", "brain/chapters/_TEMPLATE.md",
)


def digest(root: Path) -> str:
    value = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        value.update(str(path.relative_to(root)).encode())
        value.update(path.read_bytes())
    return value.hexdigest()


def run(project: Path, validate: bool = False):
    command = ["python3", str(INSPECTOR), str(project), "--plugin-root", str(ROOT)]
    if validate:
        command.append("--validate-target")
    result = subprocess.run(command, text=True, capture_output=True)
    return result, json.loads(result.stdout)


class MigrationInspectorTests(unittest.TestCase):
    def test_legacy_plan_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "agents").mkdir(); (project / "agents/STATUS.md").write_text("legacy\n")
            before = digest(project)
            result, data = run(project)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(data["layout"], "legacy")
            self.assertEqual(data["current_version"], "pre-2.5.0")
            self.assertTrue(data["pending_manifests"])
            self.assertEqual(before, digest(project))
            self.assertFalse(data["mutated"])

    def test_partial_v4_target_fails_without_stamping(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); (project / "brain").mkdir()
            (project / "brain/.plugin-version").write_text("4.1.0\n")
            result, data = run(project, True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(data["validation"]["ok"])
            self.assertEqual((project / "brain/.plugin-version").read_text(), "4.1.0\n")

    def test_v3_brain_layout_reports_pending_chain_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); (project / "brain").mkdir()
            (project / "brain/.plugin-version").write_text("3.0.0\n")
            before = digest(project)
            result, data = run(project)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(data["layout"], "brain")
            self.assertEqual(data["current_version"], "3.0.0")
            self.assertTrue(any(item["version"] == "5.0.0" for item in data["pending_manifests"]))
            self.assertEqual(before, digest(project))

    def test_valid_v5_target_passes_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for relative in REQUIRED:
                path = project / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("# valid\n")
            (project / "brain/.plugin-version").write_text("5.0.0\n")
            before = digest(project)
            for _ in range(2):
                result, data = run(project, True)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertTrue(data["validation"]["ok"])
            self.assertEqual(before, digest(project))

    def test_v5_target_rejects_semantically_stale_claude(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for relative in REQUIRED:
                path = project / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("# valid\n")
            (project / "brain/.plugin-version").write_text("5.0.0\n")
            (project / "CLAUDE.md").write_text(
                "# Project\n\nOne tool active at a time.\n\n"
                "Log every change as it happens.\n\n## Hooks index\nOld hook manual.\n"
            )
            result, data = run(project, True)
            self.assertNotEqual(result.returncode, 0)
            codes = {item["path"] for item in data["validation"]["problems"]}
            self.assertIn("CLAUDE.md:one-tool-only", codes)
            self.assertIn("CLAUDE.md:per-action-worklog", codes)
            self.assertIn("CLAUDE.md:embedded-hooks-index", codes)


if __name__ == "__main__":
    unittest.main()
