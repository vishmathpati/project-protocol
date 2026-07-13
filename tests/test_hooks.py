#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "hooks/scripts"


def run(script: str, cwd: Path, extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CODEX_PLUGIN_ROOT"] = str(ROOT)
    env.update(extra_env or {})
    return subprocess.run(["python3", str(HOOKS / script)], cwd=cwd, env=env, text=True, capture_output=True)


class HookSmokeTests(unittest.TestCase):
    def test_session_start_reports_drift_but_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); (project / "brain").mkdir()
            (project / "brain/.plugin-version").write_text("4.1.0\n")
            before = sorted(str(path.relative_to(project)) for path in project.rglob("*"))
            result = run("session_start.py", project)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Plugin drift: project 4.1.0", result.stdout)
            self.assertEqual(before, sorted(str(path.relative_to(project)) for path in project.rglob("*")))

    def test_session_start_is_quiet_about_drift_when_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); (project / "brain").mkdir()
            (project / "brain/.plugin-version").write_text("5.0.1\n")
            result = run("session_start.py", project)
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("Plugin drift", result.stdout)

    def test_post_write_routes_design_and_ui(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); (project / "brain").mkdir()
            design = project / "brain/DESIGN.md"; design.write_text("# Design\n")
            result = run("post_write.py", project, {"TOOL_INPUT_FILE_PATH": str(design)})
            self.assertIn("Style Lock synchronization", result.stdout)
            ui = project / "components/Hero.tsx"; ui.parent.mkdir(); ui.write_text('export const Hero = () => <div style={{color: "#ffffff"}} />\n')
            result = run("post_write.py", project, {"TOOL_INPUT_FILE_PATH": str(ui)})
            self.assertIn("Run Design Check postflight", result.stdout)
            self.assertIn("raw hex", result.stdout)


if __name__ == "__main__":
    unittest.main()
