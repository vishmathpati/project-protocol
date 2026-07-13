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
    env.setdefault("PROJECT_PROTOCOL_PRIVATE_CANON_CONFIG", str(cwd / ".test-private-canons.json"))
    env.update(extra_env or {})
    return subprocess.run(["python3", str(HOOKS / script)], cwd=cwd, env=env, text=True, capture_output=True)


class HookSmokeTests(unittest.TestCase):
    def test_session_start_attaches_private_canon_in_a_new_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            project = base / "project"
            canon = base / "private-canon"
            worktree = base / "worktree"
            config = base / "private-canons.json"
            project.mkdir()
            (canon / "brain").mkdir(parents=True)
            (canon / "CLAUDE.md").write_text("# Private project index\n")
            (canon / "brain/.plugin-version").write_text("5.0.1\n")
            subprocess.run(["git", "init", "-b", "main"], cwd=project, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=project, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=project, check=True)
            subprocess.run(["git", "remote", "add", "origin", "git@example.com:test/project.git"], cwd=project, check=True)
            (project / "README.md").write_text("# Test\n")
            subprocess.run(["git", "add", "README.md"], cwd=project, check=True)
            subprocess.run(["git", "commit", "-m", "init"], cwd=project, check=True, capture_output=True)
            env = os.environ.copy()
            env["PROJECT_PROTOCOL_PRIVATE_CANON_CONFIG"] = str(config)
            registered = subprocess.run(
                ["python3", str(HOOKS / "private_canon.py"), "register", "--repo", str(project), "--canon", str(canon)],
                env=env,
                text=True,
                capture_output=True,
            )
            self.assertEqual(registered.returncode, 0, registered.stdout + registered.stderr)
            subprocess.run(["git", "worktree", "add", "-b", "feature", str(worktree)], cwd=project, check=True, capture_output=True)
            result = run("session_start.py", worktree, {"PROJECT_PROTOCOL_PRIVATE_CANON_CONFIG": str(config)})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Private canon attached", result.stdout)
            self.assertFalse((HOOKS / "__pycache__").exists())
            self.assertEqual((worktree / "brain").resolve(), (canon / "brain").resolve())
            self.assertEqual((worktree / "CLAUDE.md").resolve(), (canon / "CLAUDE.md").resolve())
            status = subprocess.run(["git", "status", "--porcelain"], cwd=worktree, text=True, capture_output=True, check=True)
            self.assertEqual(status.stdout, "")

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
