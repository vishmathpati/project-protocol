#!/usr/bin/env python3
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GuidedVisualBuildFlowTests(unittest.TestCase):
    def test_research_led_marketing_build_requires_locked_site_review(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()

        self.assertIn("Site-wide decision gate", text)
        self.assertIn("submitted is not locked", text)
        self.assertIn("every unique page and page family", text)
        self.assertIn("stop before implementation", text)

    def test_sitemap_declares_page_families_and_exceptions(self):
        text = (ROOT / "templates/SITEMAP.md").read_text()

        for field in ("Page/family ID", "Scope", "Representative page", "Shared pattern", "Exceptions"):
            self.assertIn(field, text)
        self.assertIn("unique-page", text)
        self.assertIn("page-family", text)

    def test_page_blueprint_preserves_connected_composition_and_header_coupling(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()
        lower = text.lower()

        self.assertLess(lower.index("whole-page direction"), lower.index("optional section overrides"))
        self.assertIn("connected-section sequence", lower)
        self.assertIn("hero/header", lower)
        self.assertIn("never silently select", lower)

    def test_page_activation_checks_shell_home_and_prior_pages(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()

        for context in ("locked global shell", "approved homepage", "previously approved or built pages", "page-family siblings"):
            self.assertIn(context, text)
        for verdict in ("compatible", "compatible_with_adaptation", "conflicting"):
            self.assertIn(verdict, text)
        self.assertIn("shell slice first", text)

    def test_marketing_component_actions_require_an_active_page(self):
        build = (ROOT / "skills/build-component/SKILL.md").read_text()
        inspect = (ROOT / "skills/inspect-component/SKILL.md").read_text()

        for text in (build, inspect):
            self.assertIn("active Build Page", text)
            self.assertIn("queued", text)
            self.assertIn("ordinary product/dashboard", text)
        self.assertIn("approved page decision", build)
        self.assertIn("exact approved page region", inspect)

    def test_page_asset_request_is_complete_and_does_not_ask_for_routine_icons(self):
        build = (ROOT / "skills/build-page/SKILL.md").read_text()
        lifecycle = (ROOT / "skills/build-page/references/media-lifecycle.md").read_text()
        template = (ROOT / "templates/MEDIA.md").read_text()

        self.assertIn("Page Asset Request", build)
        for asset_type in ("images", "videos", "posters", "illustrations", "logos", "bespoke marks", "other load-bearing assets"):
            self.assertIn(asset_type, build)
        self.assertIn("Routine icons are automatic", build)
        self.assertIn("Availability / next action", template)
        self.assertIn("one consolidated request", lifecycle)

    def test_dashboard_uses_the_approved_human_review_workspace(self):
        text = (ROOT / "skills/project-dashboard/SKILL.md").read_text()

        for requirement in (
            "rough content structure stay visible on the left",
            "recommendation appears on the right",
            "whole-page/page-family direction",
            "optional section refinements",
            "keep/change exact affected parts",
            "bring an exact live reference",
        ):
            self.assertIn(requirement, text)

    def test_marketing_classifies_unique_pages_and_real_page_families(self):
        skill = (ROOT / "skills/marketing-brief/SKILL.md").read_text()
        page_brief = (ROOT / "templates/PAGE-BRIEF.md").read_text()

        self.assertIn("unique page or page family", skill)
        self.assertIn("representative page", skill)
        self.assertIn("genuine exceptions", skill)
        for field in ("Page/family ID", "Scope", "Family members", "Representative page", "Exceptions"):
            self.assertIn(field, page_brief)

    def test_design_check_enforces_but_does_not_choose_site_compatibility(self):
        text = (ROOT / "skills/design-check/SKILL.md").read_text()

        self.assertIn("site-wide direction is locked", text)
        self.assertIn("active page compatibility verdict", text)
        self.assertIn("submitted or conflicting", text)
        self.assertIn("global shell, approved homepage, prior pages, and family siblings", text)
        self.assertIn("does not choose or repair the direction", text)

    def test_chapter_separates_submission_review_and_lock(self):
        text = (ROOT / "templates/CHAPTER.md").read_text()

        for field in ("Approved Site Direction", "Submission ID", "Submission revision", "Approved by", "Approved at", "Approved page and family matrix", "Global shell"):
            self.assertIn(field, text)
        self.assertIn("Submitted is not locked", text)

    def test_retained_component_references_cannot_bypass_current_contract(self):
        inspiration = (ROOT / "skills/build-component/references/recreate-from-inspiration.md").read_text()
        intake = (ROOT / "skills/build-component/references/phase-2-intake-and-tier.md").read_text()
        write = (ROOT / "skills/build-component/references/phase-5-preview-and-write.md").read_text()

        self.assertIn("never creates STRUCTURE", inspiration)
        self.assertIn("approved page content", intake)
        self.assertIn("smallest approved file set", write)
        self.assertIn("routing reminder", write)
        self.assertNotIn("hook's 8 steps", write)

    def test_build_page_consumes_state_from_the_active_checkout_only(self):
        text = (ROOT / "skills/build-page/SKILL.md").read_text()

        self.assertIn("git rev-parse --show-toplevel", text)
        self.assertIn("same active checkout", text)
        self.assertIn("sibling or main checkout", text)

    def test_approved_site_direction_has_one_exact_machine_readable_contract(self):
        build = (ROOT / "skills/build-page/SKILL.md").read_text()
        contract = (ROOT / "skills/build-page/references/site-direction-lock.md").read_text()
        chapter = (ROOT / "templates/CHAPTER.md").read_text()

        self.assertIn("references/site-direction-lock.md", build)
        self.assertIn("## Approved Site Direction", contract)
        for field in (
            "Status: locked",
            "Submission ID:",
            "Submission revision:",
            "Project root:",
            "Branch:",
            "HEAD:",
            "Approved by:",
            "Approved at:",
            "Site direction recommendation ID:",
            "Global shell:",
            "Unresolved conflicts: none",
        ):
            self.assertIn(field, contract)
        for status in ("compatible", "compatible_with_adaptation", "conflicting"):
            self.assertIn(status, contract)
        self.assertIn("Every unique page and page family", contract)
        self.assertIn("## Approved Site Direction", chapter)
        self.assertNotIn("COMPATIBLE | ADAPTATION REQUIRED | CONFLICT", chapter)


if __name__ == "__main__":
    unittest.main()
