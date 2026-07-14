#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import tempfile
import unittest
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "skills/project-dashboard/scripts/generate_dashboard.py"


class DashboardTests(unittest.TestCase):
    def test_generated_inline_javascript_is_syntactically_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); brain = project / "brain"; brain.mkdir()
            output = brain / "project-dashboard.html"
            generated = subprocess.run(["python3", str(GENERATOR), str(project)], text=True, capture_output=True)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', output.read_text(), re.S)
            self.assertTrue(scripts)
            checked = subprocess.run(["node", "--check", "-"], input=scripts[-1], text=True, capture_output=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)

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

    def test_page_recommendations_render_page_map_scopes_evidence_and_fallback_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp); research = project / "brain/research"; moodboard = project / "brain/moodboard"
            research.mkdir(parents=True); moodboard.mkdir(parents=True)
            (moodboard / "aman-hero.png").write_bytes(b"hero")
            (moodboard / "aman-mid.png").write_bytes(b"mid")
            packet = {
                "schema_version": "project-protocol.page-recommendations.v1",
                "mission_id": "mission-1",
                "project": "Example",
                "generated_at": "2026-07-13T00:00:00Z",
                "entry_mode": "provided-reference-discovery",
                "derived_path": "brain/research/page-recommendations.json",
                "checkout": {"checkout_root": str(project), "brain_root": str(project / "brain"), "branch": "test", "head": "abc"},
                "input": {
                    "site_goal": "Introduce one property clearly.",
                    "page_families": [{"family_id": "home", "label": "Home", "routes": ["/"], "kind": "unique"}],
                    "targets": [{"target_id": "home", "family_id": "home", "label": "Home", "content_goal": "Show stay, dine, and celebrate.", "content_jobs": ["Arrival", "Stay and dine", "Final invitation"]}],
                    "available_media": [],
                    "reference_scope": {"mode": "pinned", "urls": ["https://www.aman.com/"]},
                },
                "site_direction": {"recommendation_id": "site-quiet", "summary": "A quiet image-led arrival", "fit": "Matches the story", "alternatives": [], "evidence_refs": ["aman-home"], "confidence": {"level": "high", "reason": "Repeated evidence", "material_gaps": []}},
                "global_shell": {"target_id": "global-shell", "state": "recommended", "recommendations": [{"recommendation_id": "shell-overlay", "scope": "global-shell", "title": "Transparent arrival header", "dependencies": ["home--quiet-procession"], "evidence_refs": ["aman-home"]}]},
                "targets": [{
                    "target_id": "home",
                    "recommendations": [{
                        "recommendation_id": "home--quiet-procession",
                        "scope": "connected-sections",
                        "affected_blocks": ["arrival", "stay-and-dine"],
                        "title": "Quiet procession",
                        "description": "One connected visual journey.",
                        "fit": "Carries the supplied content without fragmenting it.",
                        "alternatives": [],
                        "compatibility_notes": {"dependencies": ["shell-overlay"], "notes": "Header is proposed, never auto-selected."},
                        "evidence": [{"evidence_id": "aman-home", "site": "Aman", "page": "Home", "live_url": "https://www.aman.com/", "screenshot_paths": ["brain/moodboard/aman-hero.png", "brain/moodboard/aman-mid.png"], "capture_status": "live-complete", "viewport": "1440x900", "video": {"role": "hero", "provider_or_page_url": "https://www.aman.com/", "delivery": "stream", "playback": "muted", "reduced_motion_fallback": "observed", "official_embed": "no"}, "motion": {"behavior": "calm crossfades", "implementation_evidence": "observed"}, "teardown_path": "brain/research/teardowns/aman.md", "evidence": "direct", "inference": "none"}],
                        "asset_requirements": [{"asset_id": "home-film", "kind": "video", "purpose": "Arrival", "quantity": "1", "orientation_or_dimensions": "landscape", "responsive_need": "desktop/mobile", "poster_or_fallback": "required", "safe_source_routes": ["client", "commissioned"], "replacement_or_rights_state": "missing"}],
                        "confidence": {"level": "high", "reason": "direct", "material_gaps": []},
                        "focused_followup": {"eligible": True, "question": "Inspect transition mechanics"},
                    }],
                }],
                "unresolved_gaps": [],
                "saturation": "stable",
                "evidence_readiness": "ready",
            }
            (research / "page-recommendations.json").write_text(json.dumps(packet))
            output = project / "brain/project-dashboard.html"
            result = subprocess.run(["python3", str(GENERATOR), str(project)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text()
            for text in ("Home", "Arrival", "Stay and dine", "Connected sections", "Quiet procession", "Open live site", "Video", "home-film", "Submit decisions"):
                self.assertIn(text, html)
            for control_id in ("update-decisions", "export-decisions", "copy-decisions"):
                self.assertIn(f'id="{control_id}"', html)
            for text in (
                "Choose this first · Site-wide direction",
                "Existing content, shown as a rough structure",
                "Optional: keep or change specific parts",
                "Research another pattern for this part",
                "Bring my own reference",
                "I’ll bring my own component later",
                "Recommended reference pattern",
            ):
                self.assertIn(text, html)
            self.assertIn('class="decision-workspace"', html)
            self.assertIn('class="decision-block', html)
            self.assertIn('class="brief"', html)
            self.assertIn('class="recommendation"', html)
            self.assertIn('<body class="review-mode">', html)
            self.assertIn('<header class="review-header">', html)
            self.assertNotIn('<nav class="dashboard-tabs">', html)
            self.assertNotIn('Concise visual projection of Markdown canon', html)
            for state_field in ("checkoutIdentity", "selected_parts", "missing_need", "liked_part", "deferred_component_intents"):
                self.assertIn(state_field, html)
            self.assertIn("choice?.status==='selected'", html)
            self.assertIn("Header remains pending", html)
            self.assertIn("brain/research/ui-decision-draft.json", html)

            direction_stage = html.split('id="direction-stage"', 1)[1].split('id="shell-stage"', 1)[0]
            shell_stage = html.split('id="shell-stage"', 1)[1].split('id="pages-stage"', 1)[0]
            pages_stage = html.split('id="pages-stage"', 1)[1]
            self.assertNotIn('data-request="component"', direction_stage)
            self.assertNotIn('data-request="component"', shell_stage)
            self.assertIn('data-request="component"', pages_stage)
            self.assertIn('data-affected-blocks="[&quot;arrival&quot;, &quot;stay-and-dine&quot;]"', pages_stage)
            self.assertIn("selectedBlocks.length?selectedBlocks:defaultBlocks", html)
            self.assertIn('class="evidence-carousel"', html)
            self.assertEqual(html.count('class="evidence-slide'), 6)
            self.assertEqual(html.count('class="evidence-slide active"'), 3)
            self.assertIn('class="previous-evidence"', html)
            self.assertIn('class="next-evidence"', html)
            self.assertIn('<span><b class="evidence-position">1</b> of 2</span>', html)
            self.assertNotIn('<div class="recommendation-nav">', html)
            self.assertIn('.decision-workspace{width:100%;max-width:none', html)
            self.assertIn('.brief{position:static;align-self:start', html)
            self.assertNotIn('.brief{position:static;align-self:stretch', html)
            self.assertIn('.dependency-note{background:#f4f4f5;color:#52525b', html)
            self.assertIn(':where(button,a,summary,input,textarea):focus-visible', html)


if __name__ == "__main__":
    unittest.main()
