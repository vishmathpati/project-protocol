#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "skills/project-dashboard/scripts/generate_dashboard.py"


class DashboardTests(unittest.TestCase):
    def test_generate_check_and_staleness(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); brain = project / "brain"; brain.mkdir()
            (brain / "BRIEF.md").write_text("# Brief\nA durable contract.\n")
            (brain / "DESIGN.md").write_text("# Design\nfamily: Inter\nfamily: Georgia\ncolor: #123456\n")
            output = brain / "project-dashboard.html"
            generated = subprocess.run(["python3", str(GENERATOR), str(project)], text=True, capture_output=True)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            html = output.read_text()
            for tab in ("Project", "Brand", "Design", "Research / Moodboard", "Build Progress"):
                self.assertIn(tab, html)
            self.assertIn("#123456", html)
            fresh = subprocess.run(["python3", str(GENERATOR), str(project), "--check"], text=True, capture_output=True)
            self.assertEqual(fresh.returncode, 0)
            (brain / "BRIEF.md").write_text("# Brief\nChanged.\n")
            stale = subprocess.run(["python3", str(GENERATOR), str(project), "--check"], text=True, capture_output=True)
            self.assertEqual(stale.returncode, 1)

    def test_portable_mode_embeds_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); moodboard = project / "brain/moodboard"; moodboard.mkdir(parents=True)
            (moodboard / "manifest.md").write_text("# Moodboard\n")
            (moodboard / "capture.png").write_bytes(b"not-a-real-png-but-valid-for-embedding")
            output = project / "portable.html"
            result = subprocess.run(["python3", str(GENERATOR), str(project), "--portable", "--output", str(output)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("data:image/png;base64,", output.read_text())


if __name__ == "__main__":
    unittest.main()
