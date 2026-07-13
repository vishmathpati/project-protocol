#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "skills/project-dashboard/scripts/serve_dashboard.py"


def request_json(url: str, token: str, payload: dict | None = None, origin: str | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Origin": origin or url.split("/api/", 1)[0],
            "X-Project-Dashboard-Token": token,
        },
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return response.status, json.loads(response.read())


def valid_payload() -> dict:
    return {
        "schema_version": 1,
        "project": {"name": "Example"},
        "research": {
            "mission_id": "mission-1",
            "mode": "provided-reference-discovery",
            "evidence_readiness": "ready",
            "derived_path": "brain/research/page-recommendations.json",
        },
        "site_direction": {"recommendation_id": "site-quiet", "status": "selected", "candidate_ids": ["site-quiet"]},
        "global_shell": {
            "target_id": "global-shell",
            "state": "recommended",
            "recommendations": [{"recommendation_id": "shell-overlay"}],
            "decisions": [{"recommendation_id": "shell-overlay", "status": "selected", "candidate_ids": ["shell-overlay"]}],
        },
        "page_families": [
            {"family_id": "home", "label": "Home", "routes": ["/"], "kind": "unique"},
            {"family_id": "family-stay", "label": "Stay", "routes": ["/rooms", "/suites"], "kind": "repeated-family"},
        ],
        "pages": [
            {
                "id": "home",
                "family_id": "home",
                "decisions": [
                    {"id": "home-direction", "scope": "whole_page", "status": "selected", "candidate_ids": ["home-direction"]}
                ],
            },
            {
                "id": "family-stay",
                "family_id": "family-stay",
                "decisions": [
                    {"id": "stay-template", "scope": "page_family", "status": "selected", "candidate_ids": ["stay-template"]}
                ],
            },
        ],
        "asset_requirements": [],
        "focused_research_requests": [],
        "provided_references": [],
    }


def write_recommendations(project: Path, checkout_root: Path | None = None) -> None:
    root = (checkout_root or project).resolve()
    packet = {
        "schema_version": "project-protocol.page-recommendations.v1",
        "mission_id": "mission-1",
        "entry_mode": "provided-reference-discovery",
        "derived_path": "brain/research/page-recommendations.json",
        "checkout": {
            "checkout_root": str(root),
            "brain_root": str(root / "brain"),
            "branch": "test",
            "head": "abc",
        },
        "input": {
            "page_families": valid_payload()["page_families"],
            "targets": [
                {"target_id": "home", "family_id": "home", "label": "Home"},
                {"target_id": "family-stay", "family_id": "family-stay", "label": "Stay"},
            ],
        },
        "site_direction": {"recommendation_id": "site-quiet"},
        "global_shell": {
            "target_id": "global-shell",
            "state": "recommended",
            "recommendations": [{"recommendation_id": "shell-overlay"}],
        },
        "targets": [
            {
                "target_id": "home",
                "recommendations": [
                    {"recommendation_id": "home-direction", "scope": "whole-page"},
                    {"recommendation_id": "home-detail", "scope": "one-section"},
                ],
            },
            {
                "target_id": "family-stay",
                "recommendations": [
                    {"recommendation_id": "stay-template", "scope": "repeated-page-family"}
                ],
            },
        ],
    }
    (project / "brain/research/page-recommendations.json").write_text(json.dumps(packet))


class DashboardStateTests(unittest.TestCase):
    def test_dashboard_handoff_names_the_active_chapter_as_the_only_approval_owner(self):
        contract = (ROOT / "skills/project-dashboard/references/decision-packet.md").read_text()
        self.assertIn("brain/chapters/<active-chapter>.md", contract)
        self.assertIn("## Approved Site Direction", contract)
        self.assertNotIn("site-wide research selection in the existing research Markdown owner", contract)

    def test_submit_rejects_recommendations_from_another_checkout(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other_tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project, Path(other_tmp))
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], valid_payload())
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_submit_rejects_forged_recommendation_and_candidate_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                payload = valid_payload()
                payload["pages"][0]["decisions"][0].update({
                    "id": "forged-direction",
                    "candidate_ids": ["forged-candidate"],
                })
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_submit_requires_exact_recommendation_target_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                payload = valid_payload()
                payload["pages"] = payload["pages"][:1]
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_submit_rejects_forged_site_direction_and_shell_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                for field in ("site_direction", "global_shell"):
                    payload = valid_payload()
                    if field == "site_direction":
                        payload[field].update({
                            "recommendation_id": "forged-site",
                            "candidate_ids": ["forged-site"],
                        })
                    else:
                        payload[field]["recommendations"] = [{"recommendation_id": "forged-shell"}]
                        payload[field]["decisions"] = [{
                            "recommendation_id": "forged-shell",
                            "status": "selected",
                            "candidate_ids": ["forged-shell"],
                        }]
                    with self.subTest(field=field):
                        with self.assertRaises(urllib.error.HTTPError) as caught:
                            request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                        self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_submit_rejects_family_coverage_that_differs_from_recommendations(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                payload = valid_payload()
                payload["page_families"][0]["family_id"] = "forged-home"
                payload["pages"][0]["family_id"] = "forged-home"
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_optional_section_choice_cannot_replace_page_or_family_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                payload = valid_payload()
                payload["pages"][0]["decisions"] = [{
                    "id": "home-detail",
                    "scope": "section",
                    "status": "selected",
                    "candidate_ids": ["home-detail"],
                }]
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_submit_rejects_a_draft_for_another_research_mission(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                payload = valid_payload()
                payload["research"]["mission_id"] = "another-mission"
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_submit_then_update_persists_server_owned_provisional_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                base = startup["url"]
                token = startup["token"]

                status, submitted = request_json(f"{base}/api/submit", token, valid_payload())
                self.assertEqual(status, 201)
                self.assertEqual(submitted["submission"]["revision"], 1)
                self.assertFalse(submitted["canonical"])
                self.assertEqual(submitted["agent_review"]["status"], "pending")
                self.assertFalse(submitted["build_gates"]["site_wide_locked"])

                packet_path = project / "brain/research/ui-decision-draft.json"
                self.assertEqual(json.loads(packet_path.read_text()), submitted)

                update = valid_payload()
                update["site_direction"]["note"] = "Keep the quieter arrival."
                status, updated = request_json(f"{base}/api/update", token, update)
                self.assertEqual(status, 200)
                self.assertEqual(updated["submission"]["revision"], 2)
                self.assertEqual(updated["site_direction"]["note"], "Keep the quieter arrival.")
                self.assertFalse(updated["canonical"])
                self.assertEqual(updated["agent_review"]["status"], "pending")
                self.assertFalse(updated["build_gates"]["site_wide_locked"])
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_server_is_loopback_token_origin_protected_and_loading_never_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                self.assertTrue(startup["url"].startswith("http://127.0.0.1:"))
                self.assertIn("?token=", startup["dashboard_url"])
                self.assertEqual(startup["root"], str(project.resolve()))
                packet_path = project / "brain/research/ui-decision-draft.json"
                self.assertFalse(packet_path.exists())

                with self.assertRaises(urllib.error.HTTPError) as plain_dashboard:
                    urllib.request.urlopen(startup["url"], timeout=5)
                self.assertEqual(plain_dashboard.exception.code, 403)
                with urllib.request.urlopen(startup["dashboard_url"], timeout=5) as response:
                    self.assertEqual(response.status, 200)

                request_json(f"{startup['url']}/api/state", startup["token"])
                self.assertFalse(packet_path.exists())
                with self.assertRaises(urllib.error.HTTPError) as bad_token:
                    request_json(f"{startup['url']}/api/submit", "wrong", valid_payload())
                self.assertEqual(bad_token.exception.code, 403)
                with self.assertRaises(urllib.error.HTTPError) as bad_origin:
                    request_json(f"{startup['url']}/api/submit", startup["token"], valid_payload(), origin="https://example.com")
                self.assertEqual(bad_origin.exception.code, 403)
                self.assertFalse(packet_path.exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_regeneration_preserves_packet_and_symlink_escape_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                request_json(f"{startup['url']}/api/submit", startup["token"], valid_payload())
                packet_path = project / "brain/research/ui-decision-draft.json"
                original = packet_path.read_text()
                generator = ROOT / "skills/project-dashboard/scripts/generate_dashboard.py"
                regenerated = subprocess.run(["python3", str(generator), str(project)], text=True, capture_output=True)
                self.assertEqual(regenerated.returncode, 0, regenerated.stderr)
                self.assertEqual(packet_path.read_text(), original)
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

            escaped = Path(tmp) / "escaped"
            (escaped / "brain").mkdir(parents=True)
            (escaped / "brain/research").symlink_to(Path(outside_tmp), target_is_directory=True)
            refused = subprocess.run(["python3", str(SERVER), str(escaped), "--port", "0"], text=True, capture_output=True, timeout=5)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("must not be a symlink", refused.stderr)
            self.assertFalse((Path(outside_tmp) / "ui-decision-draft.json").exists())

    def test_post_start_research_symlink_swap_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            project = Path(tmp)
            research = project / "brain/research"
            research.mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                (research / "page-recommendations.json").unlink()
                research.rmdir()
                research.symlink_to(Path(outside_tmp), target_is_directory=True)
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], valid_payload())
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((Path(outside_tmp) / "ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_concurrent_submit_is_serialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                results: list[int] = []
                lock = threading.Lock()

                def submit() -> None:
                    try:
                        code, _ = request_json(f"{startup['url']}/api/submit", startup["token"], valid_payload())
                    except urllib.error.HTTPError as exc:
                        code = exc.code
                    with lock:
                        results.append(code)

                threads = [threading.Thread(target=submit) for _ in range(8)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(timeout=5)
                self.assertEqual(results.count(201), 1)
                self.assertEqual(results.count(409), 7)
                packet = json.loads((project / "brain/research/ui-decision-draft.json").read_text())
                self.assertEqual(packet["submission"]["revision"], 1)
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_local_evidence_is_served_but_traversal_and_symlink_are_blocked(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            project = Path(tmp)
            research = project / "brain/research"
            research.mkdir(parents=True)
            (project / "brain/evidence.png").write_bytes(b"PNG-EVIDENCE")
            (Path(outside_tmp) / "secret.png").write_bytes(b"SECRET")
            (project / "brain/leak.png").symlink_to(Path(outside_tmp) / "secret.png")
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                with urllib.request.urlopen(f"{startup['url']}/evidence.png?token={startup['token']}", timeout=5) as response:
                    self.assertEqual(response.read(), b"PNG-EVIDENCE")
                for path in ("/%2e%2e/secret.png", "/leak.png"):
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        urllib.request.urlopen(f"{startup['url']}{path}?token={startup['token']}", timeout=5)
                    self.assertIn(caught.exception.code, {403, 404})
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_invalid_update_is_rejected_without_replacing_previous_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                base = startup["url"]
                token = startup["token"]
                request_json(f"{base}/api/submit", token, valid_payload())
                packet_path = project / "brain/research/ui-decision-draft.json"
                original = packet_path.read_text()

                invalid = valid_payload()
                invalid["pages"][0]["decisions"][0]["scope"] = "mystery_scope"
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{base}/api/update", token, invalid)
                self.assertEqual(caught.exception.code, 400)
                self.assertEqual(packet_path.read_text(), original)
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()

    def test_site_direction_and_every_global_shell_recommendation_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "brain/research").mkdir(parents=True)
            write_recommendations(project)
            process = subprocess.Popen(
                ["python3", str(SERVER), str(project), "--port", "0"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                assert process.stdout is not None
                startup = json.loads(process.stdout.readline())
                payload = valid_payload()
                payload["site_direction"].pop("status")
                payload["global_shell"]["decisions"] = []
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request_json(f"{startup['url']}/api/submit", startup["token"], payload)
                self.assertEqual(caught.exception.code, 400)
                self.assertFalse((project / "brain/research/ui-decision-draft.json").exists())
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()


if __name__ == "__main__":
    unittest.main()
