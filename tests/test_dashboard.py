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
            self.assertNotIn("<pre>", html)
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

    def test_research_is_guided_grouped_and_never_raw_dumped(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); brain = project / "brain"
            teardown = brain / "research/teardowns"; moodboard = brain / "moodboard"
            teardown.mkdir(parents=True); moodboard.mkdir(parents=True)
            (brain / "research/concepts.md").write_text("""# Concepts
## Homepage concept families
### Concept A — Quiet Procession
*Feeling: Calm arrival*
- **Opening move:** Full-viewport film
- **Rhythm:** Arrive, stay, dine, celebrate
- **Risks:** Needs excellent real media
- **Project fit:** Strong
### Concept B — Editorial House
*Feeling: Intimate*
- **Opening move:** Still architectural frame
## Human selection
- Status: pending
<!-- On selection, replace above with:
- Status: selected
- Focus: Example only
-->
""")
            (teardown / "aman.md").write_text("# Teardown — Aman\nURL: https://www.aman.com/ | Captured: today\n## Video evidence\nHero video observed.\n")
            (moodboard / "aman-hero.png").write_bytes(b"hero")
            (moodboard / "aman-mid-media-fallback.png").write_bytes(b"fallback")
            output = brain / "project-dashboard.html"
            result = subprocess.run(["python3", str(GENERATOR), str(project)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text()
            self.assertIn("Quiet Procession", html)
            self.assertIn("Editorial House", html)
            self.assertIn('class="concept-jump', html)
            self.assertIn('class="site-jump', html)
            self.assertIn("Open live site", html)
            self.assertIn("Media fallback only", html)
            self.assertIn("Video-led evidence", html)
            self.assertIn("never canon", html)
            self.assertIn("Human selection required", html)
            self.assertNotIn("Human selection recorded", html)
            self.assertNotIn("<pre>", html)

    def test_local_video_has_safe_explicit_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); moodboard = project / "brain/moodboard"; moodboard.mkdir(parents=True)
            (moodboard / "hotel-hero.mp4").write_bytes(b"video")
            output = project / "brain/project-dashboard.html"
            result = subprocess.run(["python3", str(GENERATOR), str(project)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text()
            self.assertIn("<video controls muted playsinline", html)
            self.assertIn('preload="metadata"', html)
            self.assertNotIn("autoplay", html)


if __name__ == "__main__":
    unittest.main()
