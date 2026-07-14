#!/usr/bin/env python3
"""Serve a worktree-local dashboard and persist provisional review decisions."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import secrets
import socket
import stat
import subprocess
import threading
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit


PACKET_NAME = "ui-decision-draft.json"
SCOPES = {"whole_page", "connected_sections", "section", "page_family", "global_shell"}
SOURCE_SCOPES = {
    "whole-page": "whole_page",
    "connected-sections": "connected_sections",
    "one-section": "section",
    "repeated-page-family": "page_family",
    "global-shell": "global_shell",
}
HUMAN_STATUSES = {"recommended", "shortlisted", "selected", "not_using", "needs_more_research"}
EVIDENCE_READINESS = {"ready", "ready_with_documented_gaps", "not_ready"}
SHELL_STATES = {"recommended", "not_needed"}
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".mp4", ".webm", ".mov"}


class PacketError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_value(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def load_recommendations(root: Path) -> dict[str, Any]:
    path = root / "brain/research/page-recommendations.json"
    try:
        packet = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise PacketError("missing brain/research/page-recommendations.json") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise PacketError("page recommendations are unreadable") from exc
    if packet.get("schema_version") not in {
        "project-protocol.page-recommendations.v1",
        "project-protocol.page-recommendations.v2",
    }:
        raise PacketError("page recommendations use an unsupported schema")
    checkout = packet.get("checkout")
    if not isinstance(checkout, dict):
        raise PacketError("page recommendations require checkout identity")
    expected_root = root.resolve()
    expected_brain = (root / "brain").resolve()
    try:
        packet_root = Path(str(checkout.get("checkout_root") or "")).resolve(strict=True)
        packet_brain = Path(str(checkout.get("brain_root") or "")).resolve(strict=True)
    except OSError as exc:
        raise PacketError("page recommendations identify an unavailable checkout") from exc
    if packet_root != expected_root or packet_brain != expected_brain:
        raise PacketError("page recommendations belong to another checkout")
    return packet


def validate_payload(root: Path, payload: Any) -> dict[str, Any]:
    source_packet = load_recommendations(root)
    if not isinstance(payload, dict):
        raise PacketError("packet must be a JSON object")
    if payload.get("schema_version") != 1:
        raise PacketError("schema_version must be 1")
    for key in ("project", "research", "site_direction", "global_shell"):
        if not isinstance(payload.get(key), dict):
            raise PacketError(f"{key} must be an object")
    for key in ("page_families", "pages", "asset_requirements", "focused_research_requests", "provided_references", "deferred_component_intents"):
        if not isinstance(payload.get(key), list):
            raise PacketError(f"{key} must be a list")
    if not payload["pages"]:
        raise PacketError("pages must include every unique page or family under review")
    if payload["research"].get("evidence_readiness") not in EVIDENCE_READINESS:
        raise PacketError("research.evidence_readiness is invalid")
    for payload_key, source_key in (
        ("mission_id", "mission_id"),
        ("mode", "entry_mode"),
        ("derived_path", "derived_path"),
    ):
        if payload["research"].get(payload_key) != source_packet.get(source_key):
            raise PacketError(f"research.{payload_key} does not match page recommendations")

    def validate_decision(decision: Any, location: str) -> None:
        if not isinstance(decision, dict):
            raise PacketError(f"{location} must be an object")
        decision_id = decision.get("id") or decision.get("recommendation_id")
        if not isinstance(decision_id, str) or not decision_id.strip():
            raise PacketError(f"{location} requires a stable recommendation id")
        if decision.get("status") not in HUMAN_STATUSES:
            raise PacketError(f"invalid human-choice status for {decision_id}")
        candidate_ids = decision.get("candidate_ids")
        if not isinstance(candidate_ids, list) or not candidate_ids or not all(isinstance(value, str) and value for value in candidate_ids):
            raise PacketError(f"candidate_ids must be a non-empty string list for {decision_id}")

    validate_decision(payload["site_direction"], "site_direction")
    source_direction = source_packet.get("site_direction")
    if not isinstance(source_direction, dict) or not source_direction.get("recommendation_id"):
        raise PacketError("page recommendations require a site direction")
    source_direction_id = str(source_direction["recommendation_id"])
    if (
        payload["site_direction"].get("recommendation_id") != source_direction_id
        or set(payload["site_direction"]["candidate_ids"]) != {source_direction_id}
    ):
        raise PacketError("site direction does not match page recommendations")
    shell = payload["global_shell"]
    if shell.get("target_id") != "global-shell" or shell.get("state") not in SHELL_STATES:
        raise PacketError("global_shell requires target_id global-shell and a valid state")
    recommendations = shell.get("recommendations")
    decisions = shell.get("decisions")
    if not isinstance(recommendations, list) or not isinstance(decisions, list):
        raise PacketError("global_shell recommendations and decisions must be lists")
    for index, decision in enumerate(decisions):
        validate_decision(decision, f"global_shell decision {index}")
    expected_shell = {str(item.get("recommendation_id")) for item in recommendations if isinstance(item, dict) and item.get("recommendation_id")}
    reviewed_shell = {str(item.get("recommendation_id") or item.get("id")) for item in decisions if isinstance(item, dict)}
    source_shell = source_packet.get("global_shell")
    if not isinstance(source_shell, dict):
        raise PacketError("page recommendations require global-shell state")
    source_shell_ids = {
        str(item.get("recommendation_id"))
        for item in source_shell.get("recommendations", [])
        if isinstance(item, dict) and item.get("recommendation_id")
    }
    if shell.get("state") != source_shell.get("state") or expected_shell != source_shell_ids:
        raise PacketError("global-shell choices do not match page recommendations")
    if any(not set(decision["candidate_ids"]).issubset(source_shell_ids) for decision in decisions):
        raise PacketError("global-shell candidate does not match page recommendations")
    if shell["state"] == "not_needed":
        if recommendations or decisions:
            raise PacketError("global_shell not_needed cannot contain recommendations or decisions")
    elif expected_shell != reviewed_shell:
        raise PacketError("every global-shell recommendation must be reviewed exactly once")

    family_ids: set[str] = set()
    for family in payload["page_families"]:
        if not isinstance(family, dict) or not isinstance(family.get("family_id"), str) or not family["family_id"].strip():
            raise PacketError("every page family requires a stable family_id")
        if family["family_id"] in family_ids:
            raise PacketError(f"duplicate page family id: {family['family_id']}")
        family_ids.add(family["family_id"])

    source_input = source_packet.get("input")
    if not isinstance(source_input, dict):
        raise PacketError("page recommendations require input coverage")
    source_family_ids = {
        str(item.get("family_id"))
        for item in source_input.get("page_families", [])
        if isinstance(item, dict) and item.get("family_id")
    }
    if family_ids != source_family_ids:
        raise PacketError("page families must exactly match page recommendations")
    source_input_targets = {
        str(item.get("target_id")): item
        for item in source_input.get("targets", [])
        if isinstance(item, dict) and item.get("target_id")
    }

    source_targets = {
        str(item.get("target_id")): item
        for item in source_packet.get("targets", [])
        if isinstance(item, dict) and item.get("target_id")
    }
    recommendation_contexts: dict[tuple[str, str], tuple[str, set[str], dict[str, Any]]] = {}
    for target_id, target in source_targets.items():
        for recommendation in target.get("recommendations", []):
            if not isinstance(recommendation, dict) or not recommendation.get("recommendation_id"):
                continue
            recommendation_id = str(recommendation["recommendation_id"])
            recommendation_contexts[(target_id, recommendation_id)] = (
                SOURCE_SCOPES.get(str(recommendation.get("scope")), ""),
                {
                    str(value)
                    for value in recommendation.get("affected_blocks", [])
                    if isinstance(value, str) and value.strip()
                },
                recommendation,
            )
    recommendation_contexts[("site-direction", source_direction_id)] = (
        "whole_page",
        {"site-wide feeling", "page-family rhythm", "motion language"},
        source_direction,
    )
    for recommendation in source_shell.get("recommendations", []):
        if isinstance(recommendation, dict) and recommendation.get("recommendation_id"):
            recommendation_contexts[("global-shell", str(recommendation["recommendation_id"]))] = (
                "global_shell",
                {"navigation", "footer", "header treatment"},
                recommendation,
            )
    page_ids: set[str] = set()
    for page in payload["pages"]:
        if not isinstance(page, dict) or not isinstance(page.get("id"), str) or not page["id"].strip():
            raise PacketError("every page requires a stable id")
        if page["id"] in page_ids:
            raise PacketError(f"duplicate page id: {page['id']}")
        page_ids.add(page["id"])
        source_target = source_targets.get(page["id"])
        if source_target is None:
            raise PacketError(f"page {page['id']} is not present in page recommendations")
        source_recommendations = {
            str(item.get("recommendation_id")): item
            for item in source_target.get("recommendations", [])
            if isinstance(item, dict) and item.get("recommendation_id")
        }
        if page.get("family_id") not in family_ids:
            raise PacketError(f"page {page['id']} references an unknown family_id")
        if page.get("family_id") != source_input_targets.get(page["id"], {}).get("family_id"):
            raise PacketError(f"page {page['id']} does not match its recommendation family")
        page_decisions = page.get("decisions")
        if not isinstance(page_decisions, list) or not page_decisions:
            raise PacketError(f"page {page['id']} has not been reviewed")
        decision_ids: set[str] = set()
        has_baseline = False
        for decision in page_decisions:
            validate_decision(decision, f"page {page['id']} decision")
            decision_id = str(decision.get("id") or decision.get("recommendation_id"))
            if decision_id in decision_ids:
                raise PacketError(f"duplicate decision id in {page['id']}: {decision_id}")
            decision_ids.add(decision_id)
            source_recommendation = source_recommendations.get(decision_id)
            if source_recommendation is None:
                raise PacketError(f"unknown recommendation id for {page['id']}: {decision_id}")
            if not set(decision["candidate_ids"]).issubset(source_recommendations):
                raise PacketError(f"unknown candidate id for {page['id']}: {decision_id}")
            if decision.get("scope") not in SCOPES:
                raise PacketError(f"invalid scope for {decision_id}")
            expected_scope = SOURCE_SCOPES.get(str(source_recommendation.get("scope")))
            if decision.get("scope") != expected_scope:
                raise PacketError(f"scope does not match page recommendations for {decision_id}")
            if expected_scope in {"whole_page", "page_family"}:
                has_baseline = True
        if not has_baseline:
            raise PacketError(f"page {page['id']} requires a whole-page or page-family baseline")
    if page_ids != set(source_targets):
        raise PacketError("pages must exactly cover every recommendation target")

    def validate_targeted_relay(item: Any, location: str) -> tuple[dict[str, Any], dict[str, Any]]:
        if not isinstance(item, dict):
            raise PacketError(f"{location} must be an object")
        target_id = item.get("target_id")
        recommendation_id = item.get("recommendation_id")
        context = recommendation_contexts.get((str(target_id), str(recommendation_id)))
        if context is None:
            raise PacketError(f"{location} does not match a recommendation target")
        expected_scope, allowed_blocks, source_recommendation = context
        if item.get("scope") != expected_scope:
            raise PacketError(f"{location}.scope does not match page recommendations")
        affected_blocks = item.get("affected_blocks")
        if (
            not isinstance(affected_blocks, list)
            or not affected_blocks
            or not all(isinstance(value, str) and value.strip() for value in affected_blocks)
        ):
            raise PacketError(f"{location}.affected_blocks must be a non-empty string list")
        if not set(affected_blocks).issubset(allowed_blocks):
            raise PacketError(f"{location} contains an affected block not present in page recommendations")
        if "created_at" in item and not isinstance(item["created_at"], str):
            raise PacketError(f"{location}.created_at must be a string")
        return item, source_recommendation

    for index, request in enumerate(payload["focused_research_requests"]):
        location = f"focused_research_requests[{index}]"
        request, _ = validate_targeted_relay(request, location)
        if request.get("kind") != "research":
            raise PacketError(f"{location}.kind must be research")
        if not isinstance(request.get("missing_need"), str) or not request["missing_need"].strip():
            raise PacketError(f"{location}.missing_need must be a non-empty string")

    initial_reference_urls = {
        str(value)
        for value in source_input.get("reference_scope", {}).get("urls", [])
        if isinstance(value, str) and value
    }
    for index, reference in enumerate(payload["provided_references"]):
        location = f"provided_references[{index}]"
        if isinstance(reference, dict) and reference.get("source") == "initial-research-scope":
            if set(reference) != {"live_url", "source"} or reference.get("live_url") not in initial_reference_urls:
                raise PacketError(f"{location} does not match the initial research scope")
            continue
        reference, _ = validate_targeted_relay(reference, location)
        if reference.get("kind") != "reference":
            raise PacketError(f"{location}.kind must be reference")
        parsed = urlsplit(str(reference.get("live_url") or ""))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise PacketError(f"{location}.live_url must be an http(s) URL")
        if not isinstance(reference.get("liked_part"), str) or not reference["liked_part"].strip():
            raise PacketError(f"{location}.liked_part must be a non-empty string")

    asset_keys: set[tuple[str, str, str]] = set()
    for index, asset in enumerate(payload["asset_requirements"]):
        location = f"asset_requirements[{index}]"
        if not isinstance(asset, dict):
            raise PacketError(f"{location} must be an object")
        target_id = str(asset.get("target_id") or "")
        recommendation_id = str(asset.get("recommendation_id") or "")
        context = recommendation_contexts.get((target_id, recommendation_id))
        if context is None or target_id not in source_targets:
            raise PacketError(f"{location} does not match a page recommendation")
        source_assets = {
            str(item.get("asset_id")): item
            for item in context[2].get("asset_requirements", [])
            if isinstance(item, dict) and item.get("asset_id")
        }
        asset_id = str(asset.get("asset_id") or "")
        source_asset = source_assets.get(asset_id)
        if source_asset is None:
            raise PacketError(f"{location} references an unknown asset requirement")
        expected_asset = {**source_asset, "target_id": target_id, "recommendation_id": recommendation_id}
        if asset != expected_asset:
            raise PacketError(f"{location} does not match page recommendations")
        key = (target_id, recommendation_id, asset_id)
        if key in asset_keys:
            raise PacketError(f"duplicate asset requirement for {target_id}/{recommendation_id}/{asset_id}")
        asset_keys.add(key)

    intent_keys: set[tuple[str, str, tuple[str, ...]]] = set()
    for index, intent in enumerate(payload["deferred_component_intents"]):
        location = f"deferred_component_intents[{index}]"
        if not isinstance(intent, dict):
            raise PacketError(f"{location} must be an object")
        if intent.get("kind") != "bring_own_component":
            raise PacketError(f"{location}.kind must be bring_own_component")
        if intent.get("status") != "awaiting_active_page":
            raise PacketError(f"{location}.status must be awaiting_active_page")
        target_id = intent.get("target_id")
        recommendation_id = intent.get("recommendation_id")
        source_target = source_targets.get(str(target_id))
        if source_target is None:
            raise PacketError(f"{location} references an unknown target")
        source_recommendations = {
            str(item.get("recommendation_id")): item
            for item in source_target.get("recommendations", [])
            if isinstance(item, dict) and item.get("recommendation_id")
        }
        source_recommendation = source_recommendations.get(str(recommendation_id))
        if source_recommendation is None:
            raise PacketError(f"{location} references an unknown recommendation")
        expected_scope = SOURCE_SCOPES.get(str(source_recommendation.get("scope")))
        if intent.get("scope") != expected_scope:
            raise PacketError(f"{location}.scope does not match page recommendations")
        affected_blocks = intent.get("affected_blocks")
        if (
            not isinstance(affected_blocks, list)
            or not affected_blocks
            or not all(isinstance(value, str) and value.strip() for value in affected_blocks)
        ):
            raise PacketError(f"{location}.affected_blocks must be a non-empty string list")
        allowed_blocks = {
            str(value)
            for value in source_recommendation.get("affected_blocks", [])
            if isinstance(value, str) and value.strip()
        }
        if not set(affected_blocks).issubset(allowed_blocks):
            raise PacketError(f"{location} contains an affected block not present in page recommendations")
        if not isinstance(intent.get("note", ""), str):
            raise PacketError(f"{location}.note must be a string")
        intent_key = (str(target_id), str(recommendation_id), tuple(sorted(affected_blocks)))
        if intent_key in intent_keys:
            raise PacketError(f"duplicate deferred component intent for {target_id}/{recommendation_id}")
        intent_keys.add(intent_key)
    return payload


def stamped_packet(root: Path, payload: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    packet = json.loads(json.dumps(validate_payload(root, payload)))
    timestamp = now_iso()
    prior_submission = previous.get("submission", {}) if previous else {}
    packet["canonical"] = False
    packet["project"].update({
        "root": str(root),
        "git_toplevel": git_value(root, "rev-parse", "--show-toplevel"),
        "branch": git_value(root, "branch", "--show-current"),
        "head": git_value(root, "rev-parse", "HEAD"),
    })
    packet["submission"] = {
        "id": prior_submission.get("id") or str(uuid.uuid4()),
        "revision": int(prior_submission.get("revision", 0)) + 1,
        "status": "submitted",
        "submitted_at": prior_submission.get("submitted_at") or timestamp,
        "updated_at": timestamp,
    }
    packet["agent_review"] = {
        "status": "pending",
        "allowed_compatibility_statuses": ["compatible", "compatible_with_adaptation", "conflicting"],
        "compatibility": [], "conflicts": [], "required_adaptations": [],
    }
    packet["build_gates"] = {"site_wide_locked": False, "enabled_pages": []}
    return packet


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, root: Path, port: int):
        self.root = root.resolve()
        self.brain = self.root / "brain"
        self.research = self.brain / "research"
        self.research.mkdir(parents=True, exist_ok=True)
        if self.brain.is_symlink() or self.research.is_symlink():
            raise PacketError("brain/research must not be a symlink")
        if not self.research.resolve().is_relative_to(self.root):
            raise PacketError("decision packet path escapes the active project root")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.research_fd = os.open(self.research, flags)
        opened = os.fstat(self.research_fd)
        self.research_identity = (opened.st_dev, opened.st_ino)
        self.dashboard_path = self.brain / "project-dashboard.html"
        self.token = secrets.token_urlsafe(24)
        self.state_lock = threading.Lock()
        super().__init__(("127.0.0.1", port), DashboardHandler)
        self.base_url = f"http://127.0.0.1:{self.server_port}"
        self.dashboard_url = f"{self.base_url}/?token={self.token}"

    def get_request(self) -> tuple[socket.socket, Any]:
        request, address = super().get_request()
        request.settimeout(15)
        return request, address

    def verify_research_directory(self) -> None:
        current = os.stat(self.research, follow_symlinks=False)
        opened = os.fstat(self.research_fd)
        if stat.S_ISLNK(current.st_mode) or (current.st_dev, current.st_ino) != self.research_identity:
            raise PacketError("brain/research changed after dashboard startup")
        if (opened.st_dev, opened.st_ino) != self.research_identity:
            raise PacketError("dashboard research directory is no longer trustworthy")

    def packet_exists(self) -> bool:
        self.verify_research_directory()
        try:
            info = os.stat(PACKET_NAME, dir_fd=self.research_fd, follow_symlinks=False)
        except FileNotFoundError:
            return False
        if not stat.S_ISREG(info.st_mode):
            raise PacketError("decision packet must be a regular file")
        return True

    def read_packet(self) -> dict[str, Any]:
        self.verify_research_directory()
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(PACKET_NAME, flags, dir_fd=self.research_fd)
        with os.fdopen(descriptor, "r") as handle:
            return json.load(handle)

    def write_packet(self, packet: dict[str, Any]) -> None:
        self.verify_research_directory()
        temporary = f".{PACKET_NAME}.{uuid.uuid4().hex}.tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary, flags, 0o600, dir_fd=self.research_fd)
        try:
            with os.fdopen(descriptor, "w") as handle:
                json.dump(packet, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            self.verify_research_directory()
            os.replace(temporary, PACKET_NAME, src_dir_fd=self.research_fd, dst_dir_fd=self.research_fd)
        finally:
            try:
                os.unlink(temporary, dir_fd=self.research_fd)
            except FileNotFoundError:
                pass

    def server_close(self) -> None:
        try:
            super().server_close()
        finally:
            os.close(self.research_fd)


class DashboardHandler(BaseHTTPRequestHandler):
    server: DashboardServer

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status: int, payload: Any) -> None:
        self.send_bytes(status, json.dumps(payload).encode(), "application/json; charset=utf-8")

    def header_authorized(self, write: bool = False) -> bool:
        token_ok = secrets.compare_digest(self.headers.get("X-Project-Dashboard-Token", ""), self.server.token)
        origin_ok = not write or self.headers.get("Origin") == self.server.base_url
        if token_ok and origin_ok:
            return True
        self.send_json(HTTPStatus.FORBIDDEN, {"error": "invalid dashboard token or origin"})
        return False

    def query_authorized(self, query: str) -> bool:
        supplied = parse_qs(query).get("token", [""])[0]
        referer = urlsplit(self.headers.get("Referer", ""))
        referer_token = parse_qs(referer.query).get("token", [""])[0]
        referer_ok = f"{referer.scheme}://{referer.netloc}" == self.server.base_url and secrets.compare_digest(referer_token, self.server.token)
        if secrets.compare_digest(supplied, self.server.token) or referer_ok:
            return True
        self.send_json(HTTPStatus.FORBIDDEN, {"error": "invalid dashboard token"})
        return False

    def do_GET(self) -> None:
        request = urlsplit(self.path)
        if request.path == "/":
            if not self.query_authorized(request.query):
                return
            if not self.server.dashboard_path.is_file() or self.server.dashboard_path.is_symlink():
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "generate the dashboard before serving it"})
                return
            source = self.server.dashboard_path.read_text(errors="replace")
            config = json.dumps({"url": self.server.base_url, "token": self.server.token})
            body = source.replace("</head>", f"<script>window.__PROJECT_DASHBOARD_SERVER__={config};</script></head>", 1).encode()
            self.send_bytes(HTTPStatus.OK, body, "text/html; charset=utf-8")
            return
        if request.path == "/api/state":
            if not self.header_authorized():
                return
            try:
                with self.server.state_lock:
                    if not self.server.packet_exists():
                        self.send_json(HTTPStatus.OK, {"status": "empty", "packet": None})
                        return
                    packet = self.server.read_packet()
                self.send_json(HTTPStatus.OK, {"status": "submitted", "packet": packet})
            except (OSError, PacketError, json.JSONDecodeError) as exc:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        if not self.query_authorized(request.query):
            return
        raw = unquote(request.path.lstrip("/"))
        relative = PurePosixPath(raw)
        if not raw or relative.is_absolute() or ".." in relative.parts:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "invalid evidence path"})
            return
        candidate = self.server.brain.joinpath(*relative.parts)
        try:
            resolved = candidate.resolve(strict=True)
            if candidate.is_symlink() or not resolved.is_relative_to(self.server.brain.resolve()) or not resolved.is_file():
                raise OSError("unsafe evidence path")
            if resolved.suffix.lower() not in ASSET_EXTENSIONS:
                raise OSError("unsupported evidence type")
            body = resolved.read_bytes()
        except OSError:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "evidence not found"})
            return
        content_type = mimetypes.guess_type(resolved.name)[0] or "application/octet-stream"
        self.send_bytes(HTTPStatus.OK, body, content_type)

    def do_POST(self) -> None:
        request = urlsplit(self.path)
        if request.path not in {"/api/submit", "/api/update"}:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if not self.header_authorized(write=True):
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2_000_000:
                raise PacketError("invalid packet size")
            payload = json.loads(self.rfile.read(length))
            with self.server.state_lock:
                exists = self.server.packet_exists()
                if request.path == "/api/submit" and exists:
                    self.send_json(HTTPStatus.CONFLICT, {"error": "a submitted packet exists; use Update"})
                    return
                if request.path == "/api/update" and not exists:
                    self.send_json(HTTPStatus.CONFLICT, {"error": "no submitted packet exists; use Submit"})
                    return
                previous = self.server.read_packet() if exists else None
                packet = stamped_packet(self.server.root, payload, previous)
                self.server.write_packet(packet)
            self.send_json(HTTPStatus.CREATED if not exists else HTTPStatus.OK, packet)
        except (PacketError, json.JSONDecodeError, OSError, ValueError, TimeoutError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--port", type=int, default=3000)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    brain = root / "brain"
    if not brain.is_dir():
        raise SystemExit(f"missing brain/: {root}")
    if brain.is_symlink() or not brain.resolve().is_relative_to(root):
        raise SystemExit(f"brain/ escapes the active project root: {brain}")
    generator = Path(__file__).with_name("generate_dashboard.py")
    generated = subprocess.run(["python3", str(generator), str(root)], text=True, capture_output=True)
    if generated.returncode != 0:
        raise SystemExit(generated.stderr or generated.stdout)
    try:
        server = DashboardServer(root, args.port)
    except (OSError, PacketError) as exc:
        raise SystemExit(f"cannot start dashboard for {root}: {exc}; choose another --port if needed") from exc
    print(json.dumps({
        "url": server.base_url,
        "dashboard_url": server.dashboard_url,
        "token": server.token,
        "root": str(root),
        "branch": git_value(root, "branch", "--show-current"),
        "head": git_value(root, "rev-parse", "HEAD"),
        "packet": str(server.research / PACKET_NAME),
    }), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
