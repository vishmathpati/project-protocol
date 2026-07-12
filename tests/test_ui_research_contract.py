#!/usr/bin/env python3
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UIResearchContractTests(unittest.TestCase):
    def test_plugin_skill_has_two_entry_modes_and_scope_precedence(self):
        text = (ROOT / "skills/ui-research/SKILL.md").read_text()
        self.assertIn("Discovery mode", text)
        self.assertIn("Provided-reference mode", text)
        self.assertIn("explicit target and reference constraint outrank STATUS/ROADMAP", text)
        self.assertIn("Manual Aside paste-prompt is the default transport", text)

    def test_provided_reference_mission_is_closed(self):
        text = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        self.assertIn("PINNED REFERENCE SET — CLOSED", text)
        self.assertIn("Inspect every pinned URL and no other website", text)
        self.assertIn("do not inspect unrelated inner pages", text)

    def test_aside_skill_obeys_closed_reference_scope(self):
        text = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        self.assertIn("direct constrained teardown mode", text)
        self.assertIn("discover no additional sites", text)
        self.assertIn("of substituting another site", text)

    def test_provided_reference_mission_enforces_evidence_integrity(self):
        text = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        self.assertIn("EVIDENCE INTEGRITY", text)
        self.assertIn("MEDIA FALLBACK ONLY", text)
        self.assertIn("mobile-invalid-desktop-capture", text)
        self.assertIn("FRAMEWORK/PLUGIN", text)
        self.assertIn("READY VERDICT", text)

    def test_aside_skill_classifies_capture_and_saturation_honestly(self):
        text = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        self.assertIn("Root variables are candidates, not proof", text)
        self.assertIn("media-fallback", text)
        self.assertIn("Classify evidence honestly", text)
        self.assertIn("WITH DOCUMENTED GAPS", text)

    def test_current_worktree_owns_research_writes(self):
        text = (ROOT / "skills/ui-research/SKILL.md").read_text()
        self.assertIn("git rev-parse --show-toplevel", text)
        self.assertIn("always point Aside at that worktree", text)


if __name__ == "__main__":
    unittest.main()
