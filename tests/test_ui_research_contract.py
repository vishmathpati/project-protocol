#!/usr/bin/env python3
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UIResearchContractTests(unittest.TestCase):
    def test_plugin_skill_has_three_entry_modes_and_scope_precedence(self):
        text = (ROOT / "skills/ui-research/SKILL.md").read_text()
        self.assertIn("Open discovery", text)
        self.assertIn("Provided-reference concept discovery", text)
        self.assertIn("Selected-focus teardown", text)
        self.assertIn("A supplied URL list", text)
        self.assertIn("constraint—not concept selection", text)
        self.assertIn("explicit target and reference constraint outrank STATUS/ROADMAP", text)
        self.assertIn("Manual Aside paste-prompt is the default transport", text)

    def test_provided_reference_concept_mission_is_closed_and_stops(self):
        text = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        self.assertIn("PINNED REFERENCE SET — CLOSED CONCEPT DISCOVERY", text)
        self.assertIn("Group only these sites into as many genuinely distinct", text)
        self.assertIn("NEXT: HUMAN SELECTION REQUIRED", text)
        self.assertIn("Do not select, blend, tear down", text)

    def test_selected_provided_reference_teardown_is_closed(self):
        text = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        self.assertIn("Variant D — SELECTED PROVIDED REFERENCES", text)
        self.assertIn("PINNED REFERENCE SET — CLOSED", text)
        self.assertIn("Inspect every pinned URL and no other website", text)
        self.assertIn("do not inspect unrelated inner pages", text)
        self.assertIn("BRAND/DESIGN alone is invalid", text)

    def test_aside_skill_obeys_closed_reference_scope(self):
        text = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        self.assertIn("Provided-reference concept discovery", text)
        self.assertIn("Selected provided-reference teardown", text)
        self.assertIn("discover no additional sites", text)
        self.assertIn("substituting another site", text)
        self.assertIn("Never infer selection", text)

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

    def test_human_selection_record_and_dashboard_gate_are_required(self):
        skill = (ROOT / "skills/ui-research/SKILL.md").read_text()
        formats = (ROOT / "skills/ui-research/references/round-formats.md").read_text()
        self.assertIn("explicitly invoke Project Dashboard", skill)
        self.assertIn("Status: pending", skill)
        for field in ["Status: selected", "Focus:", "Selected by:", "Selected at:", "Included moves:"]:
            self.assertIn(field, formats)
        self.assertIn("blocks Round 2", skill)

    def test_build_page_rejects_inferred_research_selection(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()
        self.assertIn("UI Research remains optional", text)
        self.assertIn("Status: pending", text)
        self.assertIn("route back to UI Research", text)
        self.assertIn("cannot substitute for explicit human selection", text)


if __name__ == "__main__":
    unittest.main()
