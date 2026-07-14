#!/usr/bin/env python3
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UIResearchContractTests(unittest.TestCase):
    def test_page_recommendation_packet_is_versioned_complete_and_exactly_shared(self):
        paths = [
            ROOT / "docs/interface-spec-research-engine.md",
            ROOT / "skills/ui-research/references/round-formats.md",
            ROOT / "skills/ui-research/references/mission-prompt-template.md",
            ROOT / "aside-skill/ui-research/SKILL.md",
        ]
        start = "<!-- PAGE_RECOMMENDATIONS_V1_START -->"
        end = "<!-- PAGE_RECOMMENDATIONS_V1_END -->"

        def contract(path):
            text = path.read_text()
            self.assertEqual(text.count(start), 1, path)
            self.assertEqual(text.count(end), 1, path)
            return text.split(start, 1)[1].split(end, 1)[0].strip()

        contracts = [contract(path) for path in paths]
        self.assertTrue(all(value == contracts[0] for value in contracts[1:]))
        for required in (
            '"schema_version": "project-protocol.page-recommendations.v2"',
            '"checkout_root"',
            '"page_families"',
            '"target_id"',
            '"scope": "whole-page | connected-sections | one-section | repeated-page-family | global-shell"',
            '"job_id": "<target-id>--job-<slug>"',
            '"copy_excerpt"',
            '"copy_ref"',
            '"description": "<what the asset shows, one line>"',
            '"affected_blocks": ["<supplied job_id>"]',
            '"serves_jobs": ["<job_id>"]',
            '"first_impression": true|false',
            '"live_url"',
            '"screenshot_paths"',
            '"video"',
            '"motion"',
            '"confidence"',
            '"material_gaps"',
            '"asset_requirements"',
            '"focused_followup"',
        ):
            self.assertIn(required, contracts[0])
        self.assertNotIn("human_selection", contracts[0])
        self.assertNotIn('"content_jobs": ["<job>"]', contracts[0])
        self.assertNotIn("page-recommendations.v1", contracts[0])

    def test_research_readiness_shell_and_approval_ownership_are_unambiguous(self):
        paths = [
            ROOT / "docs/interface-spec-research-engine.md",
            ROOT / "skills/ui-research/references/round-formats.md",
            ROOT / "skills/ui-research/references/mission-prompt-template.md",
            ROOT / "aside-skill/ui-research/SKILL.md",
        ]
        start = "<!-- PAGE_RECOMMENDATIONS_V1_START -->"
        end = "<!-- PAGE_RECOMMENDATIONS_V1_END -->"
        contracts = [path.read_text().split(start, 1)[1].split(end, 1)[0] for path in paths]
        for contract in contracts:
            self.assertIn('"evidence_readiness"', contract)
            self.assertNotIn('"ready_verdict"', contract)
            self.assertIn('"target_id": "global-shell"', contract)
            self.assertIn('"state": "recommended | not_needed"', contract)
            self.assertIn('"compatibility_notes"', contract)
            self.assertNotIn('"compatibility": {"status"', contract)

        for path in paths:
            text = path.read_text()
            self.assertIn("research-evidence readiness", text)
            self.assertIn("compatible_with_adaptation", text)
            self.assertIn("source/skills/build-page/references/site-direction-lock.md", text)
            self.assertIn("## Approved Site Direction", text)
            self.assertRegex(text.lower(), r"canonical research evidence is not an approved design\s+selection")
            for status in ("compatible", "compatible_with_adaptation", "conflicting"):
                self.assertIn(status, text)

    def test_site_wide_research_and_focused_followup_are_state_aware(self):
        skill = (ROOT / "skills/ui-research/SKILL.md").read_text()
        mission = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        aside = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()

        self.assertRegex(skill, r"stable family and target IDs")
        self.assertRegex(skill, r"every unique\s+page or repeated page family")
        for required in (
            "whole-page",
            "connected-sections",
            "one-section",
            "repeated-page-family",
            "global-shell",
            "brain/research/page-recommendations.json",
        ):
            self.assertIn(required, skill)
        for required in (
            "SITE AND PAGE MAP",
            "ACTIVE CHECKOUT IDENTITY",
            "ASSET AVAILABILITY",
            "FOCUSED PATTERN FOLLOW-UP",
            "append the PAGE_RECOMMENDATIONS packet",
        ):
            self.assertIn(required, mission)
        self.assertRegex(mission, r"Do not reopen the\s+site-wide direction")
        self.assertIn("Target and job IDs are immutable", aside)
        self.assertIn("never create a human selection", aside)
        self.assertIn("never create a build lock", aside)
        self.assertIn("focused follow-up", aside)
        self.assertIn("exact URL", aside)
        self.assertIn("Inspect Component", aside)
        for text in (skill, mission, aside):
            self.assertIn("whole-page", text)
            self.assertIn("repeated-page-family", text)
            self.assertRegex(text, r"optional refinements|optional refinement")
            self.assertRegex(text, r"never\s+(?:replace|substitute)")

    def test_aside_output_includes_video_and_provided_reference_relay(self):
        aside = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        self.assertIn("## Video evidence", aside)
        self.assertIn("## PROVIDED-REFERENCE SUMMARY BLOCK", aside)
        self.assertIn("READY VERDICT:", aside)
        self.assertIn("provider or page URL", aside)

    def test_aside_never_writes_selection_and_round_two_uses_approved_target_ids(self):
        skill = (ROOT / "skills/ui-research/SKILL.md").read_text()
        mission = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        formats = (ROOT / "skills/ui-research/references/round-formats.md").read_text()
        aside = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        for text in (mission, aside):
            self.assertNotIn("End concepts.md with `## Human selection`", text)
            self.assertNotIn("write `Status: pending`", text)
            self.assertNotIn("Preserve human selection", text)
        self.assertNotIn("## Human selection", aside)
        for text in (skill, mission, formats, aside):
            self.assertIn("approved target", text)
            self.assertIn("recommendation ID", text)
            self.assertIn("ui-decision-draft.json", text)
        for status in ("compatible", "compatible_with_adaptation", "conflicting"):
            self.assertIn(status, skill)

    def test_plugin_skill_has_four_entry_modes_and_scope_precedence(self):
        text = (ROOT / "skills/ui-research/SKILL.md").read_text()
        self.assertIn("Open discovery", text)
        self.assertIn("Provided-reference concept discovery", text)
        self.assertIn("Selected-focus teardown", text)
        self.assertIn("Focused pattern follow-up", text)
        self.assertIn("A supplied URL list", text)
        self.assertIn("constraint—not concept selection", text)
        self.assertIn("explicit target and reference\nconstraint outrank STATUS/ROADMAP", text)
        self.assertRegex(text, r"Manual Aside paste-prompt is the default\s+transport")

    def test_provided_reference_concept_mission_is_closed_and_stops(self):
        text = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        self.assertIn("PINNED REFERENCE SET — CLOSED CONCEPT DISCOVERY", text)
        self.assertIn("Group only these sites into as many genuinely distinct", text)
        self.assertIn("NEXT: SITE-WIDE REVIEW REQUIRED", text)
        self.assertIn("Do not select, blend, tear down", text)

    def test_selected_provided_reference_teardown_is_closed(self):
        text = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        self.assertIn("Variant D — SELECTED PROVIDED REFERENCES", text)
        self.assertIn("PINNED REFERENCE SET — CLOSED", text)
        self.assertIn("Inspect every pinned URL and no other website", text)
        self.assertIn("do not inspect unrelated inner pages", text)
        self.assertIn("brain/research/ui-decision-draft.json alone is invalid", text)

    def test_aside_skill_obeys_closed_reference_scope(self):
        text = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        self.assertIn("Provided-reference concept discovery", text)
        self.assertIn("Selected provided-reference teardown", text)
        self.assertIn("discover no additional sites", text)
        self.assertIn("substituting another site", text)
        self.assertIn("never approval", text)

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

    def test_dashboard_submit_and_human_approval_gate_are_required(self):
        skill = (ROOT / "skills/ui-research/SKILL.md").read_text()
        formats = (ROOT / "skills/ui-research/references/round-formats.md").read_text()
        self.assertIn("explicitly invoke Project Dashboard", skill)
        self.assertIn("one universal submit action", skill)
        self.assertIn("brain/research/ui-decision-draft.json", skill)
        for status in ("compatible", "compatible_with_adaptation", "conflicting"):
            self.assertIn(status, skill)
        self.assertIn("approved target", formats)
        self.assertIn("A draft does not authorize Round 2 or a build", formats)
        self.assertIn("chapter", formats)

    def test_build_page_rejects_inferred_research_selection(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()
        self.assertIn("UI Research remains optional", text)
        self.assertIn("brain/research/page-recommendations.json", text)
        self.assertIn("ui-decision-draft.json", text)
        self.assertIn("submitted is not locked", text)
        self.assertIn("cannot substitute for the approved chapter record", text)
        self.assertIn("route to the site-wide review", text)

    def test_visual_readiness_and_video_evidence_are_first_class(self):
        mission = (ROOT / "skills/ui-research/references/mission-prompt-template.md").read_text()
        formats = (ROOT / "skills/ui-research/references/round-formats.md").read_text()
        aside = (ROOT / "aside-skill/ui-research/SKILL.md").read_text()
        for text in (mission, formats, aside):
            self.assertIn("document.fonts.ready", text)
            self.assertIn("decode()", text)
            self.assertIn("readyState >= 2", text)
            self.assertIn("Network idle alone is insufficient", text)
            self.assertIn("bounded", text)
            self.assertIn("PARTIAL/loading-state", text)
            self.assertIn("reduced-motion", text)
        self.assertIn("never classify one captured video frame as an image-led concept", aside)

    def test_dashboard_checkpoint_is_visual_and_one_at_a_time(self):
        text = (ROOT / "skills/ui-research/SKILL.md").read_text()
        self.assertIn("one recommendation at a time", text)
        self.assertIn("visual decision interface, not a raw Markdown mirror", text)
        self.assertIn("at a useful viewing scale", text)

    def test_build_page_is_content_first_and_media_explicit(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()
        lifecycle = (ROOT / "skills/build-page/references/media-lifecycle.md").read_text()
        self.assertLess(text.index("Content inventory"), text.index("Pattern choice"))
        self.assertLess(text.index("Section jobs and narrative order"), text.index("Media plan"))
        self.assertIn("let the human choose", text)
        self.assertIn("reference-only", lifecycle)
        self.assertIn("before visual approval", lifecycle)
        self.assertIn("Routine UI icons", lifecycle)


if __name__ == "__main__":
    unittest.main()
