#!/usr/bin/env python3
"""Resolve and attach opt-in private Project Protocol canon.

Mappings live outside project repositories. A mapping is keyed by the Git
remote so every worktree of the same repository resolves the same private
canon. Attachment uses symlinks and never replaces an existing path.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONFIG = Path.home() / ".config/project-protocol/private-canons.json"
PRIVATE_PATHS = ("CLAUDE.md", "brain")


@dataclass(frozen=True)
class Attachment:
    canon_root: Path | None
    attached: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


def _git(repo: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def repository_root(path: Path) -> Path | None:
    value = _git(path, "rev-parse", "--show-toplevel")
    return Path(value).resolve() if value else None


def repository_identity(path: Path) -> str | None:
    root = repository_root(path)
    if root is None:
        return None
    remote = _git(root, "config", "--get", "remote.origin.url")
    if remote:
        normalized = remote.strip().removesuffix(".git").rstrip("/")
        return f"remote:{normalized}"
    common = _git(root, "rev-parse", "--git-common-dir")
    if not common:
        return None
    common_path = Path(common)
    if not common_path.is_absolute():
        common_path = root / common_path
    return f"git:{common_path.resolve()}"


def config_path() -> Path:
    override = os.environ.get("PROJECT_PROTOCOL_PRIVATE_CANON_CONFIG")
    return Path(override).expanduser() if override else DEFAULT_CONFIG


def _load(path: Path) -> dict:
    if not path.is_file():
        return {"version": 1, "repositories": {}}
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "repositories": {}}
    if not isinstance(data.get("repositories"), dict):
        data["repositories"] = {}
    data["version"] = 1
    return data


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def _exclude_private_paths(repo: Path) -> None:
    common = _git(repo, "rev-parse", "--git-common-dir")
    if not common:
        return
    common_path = Path(common)
    if not common_path.is_absolute():
        common_path = repo / common_path
    exclude = common_path.resolve() / "info/exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude.read_text().splitlines() if exclude.is_file() else []
    required = ["/CLAUDE.md", "/brain"]
    if all(rule in existing for rule in required):
        return
    lines = [*existing]
    if lines and lines[-1] != "":
        lines.append("")
    lines.append("# Project Protocol private canon (local only)")
    lines.extend(rule for rule in required if rule not in existing)
    exclude.write_text("\n".join(lines) + "\n")


def _install_post_checkout(repo: Path) -> None:
    """Install a local-only worktree attachment hook without replacing user hooks."""
    common = _git(repo, "rev-parse", "--git-common-dir")
    if not common:
        return
    common_path = Path(common)
    if not common_path.is_absolute():
        common_path = repo / common_path
    hook = common_path.resolve() / "hooks/post-checkout"
    marker = "# project-protocol-private-canon"
    if hook.is_file():
        if marker in hook.read_text(errors="ignore"):
            return
        raise ValueError(f"existing post-checkout hook requires manual integration: {hook}")
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(
        "#!/bin/sh\n"
        f"{marker}\n"
        "repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0\n"
        "resolver=\"$repo_root/hooks/scripts/private_canon.py\"\n"
        "if [ -f \"$resolver\" ]; then\n"
        "  PYTHONDONTWRITEBYTECODE=1 python3 \"$resolver\" attach --repo \"$repo_root\" >/dev/null 2>&1 || true\n"
        "fi\n"
        "exit 0\n"
    )
    hook.chmod(0o755)


def resolve(path: Path) -> Path | None:
    identity = repository_identity(path)
    if identity is None:
        return None
    entry = _load(config_path())["repositories"].get(identity)
    if not isinstance(entry, dict) or not entry.get("canon_root"):
        return None
    return Path(entry["canon_root"]).expanduser().resolve()


def register(repo_path: Path, canon_root: Path) -> Path:
    repo = repository_root(repo_path)
    identity = repository_identity(repo_path)
    if repo is None or identity is None:
        raise ValueError(f"not a Git repository: {repo_path}")
    canon = canon_root.expanduser().resolve()
    if not (canon / "brain").is_dir() or not (canon / "CLAUDE.md").is_file():
        raise ValueError("private canon must contain CLAUDE.md and brain/")
    try:
        canon.relative_to(repo)
    except ValueError:
        pass
    else:
        raise ValueError("private canon must live outside the public source repository")
    path = config_path()
    data = _load(path)
    data["repositories"][identity] = {"canon_root": str(canon)}
    _write(path, data)
    _exclude_private_paths(repo)
    _install_post_checkout(repo)
    return canon


def attach(path: Path) -> Attachment:
    repo = repository_root(path)
    canon = resolve(path)
    if repo is None or canon is None:
        return Attachment(canon_root=None)
    attached: list[str] = []
    conflicts: list[str] = []
    for relative in PRIVATE_PATHS:
        source = canon / relative
        destination = repo / relative
        if not source.exists():
            conflicts.append(f"missing private source: {source}")
            continue
        if destination.is_symlink():
            if destination.resolve() == source.resolve():
                attached.append(relative)
            else:
                conflicts.append(f"existing symlink: {destination}")
            continue
        if destination.exists():
            conflicts.append(f"existing path: {destination}")
            continue
        destination.symlink_to(source, target_is_directory=source.is_dir())
        attached.append(relative)
    return Attachment(canon_root=canon, attached=tuple(attached), conflicts=tuple(conflicts))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("register", "resolve", "attach", "status"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--canon", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "register":
            if args.canon is None:
                parser.error("register requires --canon")
            canon = register(args.repo, args.canon)
            result = attach(args.repo)
            print(json.dumps({"canon_root": str(canon), "attached": result.attached, "conflicts": result.conflicts}))
            return 1 if result.conflicts else 0
        if args.command == "resolve":
            canon = resolve(args.repo)
            if canon is None:
                return 1
            print(canon)
            return 0
        result = attach(args.repo)
        payload = {
            "canon_root": str(result.canon_root) if result.canon_root else None,
            "attached": result.attached,
            "conflicts": result.conflicts,
        }
        print(json.dumps(payload))
        return 1 if result.conflicts else 0
    except ValueError as exc:
        print(f"private canon error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
