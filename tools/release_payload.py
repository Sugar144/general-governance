#!/usr/bin/env python3
"""Deterministic General Governance release-payload identity helpers.

This module owns release content classification, digest dispatch, and isolated
payload projection. It contains no authority or release-status inference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

MANIFEST_PATH = "release-manifest.json"
PROJECTION_INDEX = "projection-index.json"

LEGACY_SCHEMA_VERSION = "1.3.0"
LEGACY_METHOD = "LEGACY_COMPLETE_TRACKED_FILES_V1"
SCOPED_SCHEMA_VERSION = "1.4.0"
SCOPED_METHOD = "SCOPED_TRACKED_FILES_V1"

RELEASE_INCLUDED = "RELEASE_INCLUDED"
OPERATIONAL_EXCLUDED = "OPERATIONAL_EXCLUDED"
MANIFEST_SELF_EXCLUDED = "MANIFEST_SELF_EXCLUDED"

PROTECTED_RELEASE_PREFIXES = (
    "framework/",
    "contracts/",
    "tools/",
    "tests/",
    "docs/",
    "provenance/",
)
PROTECTED_RELEASE_EXACT_PATHS = frozenset(
    {
        "RELEASE_VERSION",
        "README.md",
        ".github/workflows/conformance-ci.yml",
    }
)
SCOPED_V1_RESERVED_OPERATIONAL_PREFIXES = ("governance/",)
SCOPED_V1_OPERATIONAL_EXACT_ALLOWLIST = frozenset(
    {
        ".gitignore",
        "AGENTS.md",
        "PROJECT_STATE.yaml",
        "ROADMAP.md",
        "project-state-integrity.json",
        "scripts/project_state_integrity.py",
        ".github/pull_request_template.md",
        ".github/workflows/project-state-integrity.yml",
    }
)


@dataclass(frozen=True)
class Classification:
    included: tuple[str, ...]
    operational_excluded: tuple[str, ...]
    manifest_self_excluded: tuple[str, ...] = (MANIFEST_PATH,)


def fail(message: str) -> None:
    raise ValueError(message)


def file_digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        fail(f"cannot read release content path {path}: {exc}")


def load_release_manifest(root: Path) -> dict:
    path = root / MANIFEST_PATH
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid release manifest {path}: {exc}")
    if not isinstance(value, dict):
        fail("release manifest must be a JSON object")
    validate_release_manifest(value)
    return value


def _validate_sha256(value: object, label: str) -> None:
    import re
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        fail(f"{label} must be a lowercase 64-hex SHA-256")


def _normalized_repo_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty repository-relative path")
    if "\\" in value or "\x00" in value or "\n" in value or "\r" in value:
        fail(f"{label} is not a normalized POSIX repository path")
    path = PurePosixPath(value)
    if path.is_absolute() or "." in path.parts or ".." in path.parts:
        fail(f"{label} is not a safe repository-relative path")
    normalized = path.as_posix()
    if normalized != value or normalized == ".":
        fail(f"{label} is not normalized")
    return value


def _is_protected_release_path(path: str) -> bool:
    return path in PROTECTED_RELEASE_EXACT_PATHS or path.startswith(PROTECTED_RELEASE_PREFIXES)


def validate_release_manifest(manifest: Mapping[str, object]) -> None:
    schema_version = manifest.get("manifest_schema_version")
    if manifest.get("repository") != "Sugar144/general-governance":
        fail("release manifest repository identity is invalid")
    if not isinstance(manifest.get("framework_version"), str) or not manifest["framework_version"]:
        fail("release manifest framework_version is invalid")
    _validate_sha256(manifest.get("content_sha256"), "release manifest content_sha256")

    if schema_version == LEGACY_SCHEMA_VERSION:
        method_text = manifest.get("content_identity_method")
        if not isinstance(method_text, str) or not method_text.strip():
            fail("legacy release manifest requires content_identity_method")
        if "content_identity" in manifest:
            fail("legacy release manifest cannot declare scoped content_identity")
        return

    if schema_version != SCOPED_SCHEMA_VERSION:
        fail(f"unsupported release manifest schema version: {schema_version!r}")

    if "content_identity_method" in manifest:
        fail("scoped release manifest must use content_identity, not content_identity_method")

    identity = manifest.get("content_identity")
    expected_keys = {
        "method",
        "default_classification",
        "manifest_self_excluded",
        "reserved_operational_prefixes",
        "operational_exact_paths",
    }
    if not isinstance(identity, dict) or set(identity) != expected_keys:
        fail("scoped release manifest content_identity shape is invalid")
    if identity["method"] != SCOPED_METHOD:
        fail("unsupported scoped release identity method")
    if identity["default_classification"] != RELEASE_INCLUDED:
        fail("scoped release identity must default to RELEASE_INCLUDED")
    if identity["manifest_self_excluded"] is not True:
        fail("release-manifest.json must be self-excluded only from content_sha256")
    prefixes = identity["reserved_operational_prefixes"]
    if prefixes != list(SCOPED_V1_RESERVED_OPERATIONAL_PREFIXES):
        fail("scoped v1 reserved_operational_prefixes must equal ['governance/']")

    exact_paths = identity["operational_exact_paths"]
    if not isinstance(exact_paths, list):
        fail("operational_exact_paths must be a list")
    if len(exact_paths) != len(set(exact_paths)):
        fail("operational_exact_paths contains duplicates")
    for index, raw in enumerate(exact_paths):
        path = _normalized_repo_path(raw, f"operational_exact_paths[{index}]")
        if path not in SCOPED_V1_OPERATIONAL_EXACT_ALLOWLIST:
            fail(f"unsupported operational exact-path exclusion: {path}")
        if _is_protected_release_path(path) or path == MANIFEST_PATH:
            fail(f"protected release path cannot be operationally excluded: {path}")


def identity_method(manifest: Mapping[str, object]) -> str:
    validate_release_manifest(manifest)
    if manifest["manifest_schema_version"] == LEGACY_SCHEMA_VERSION:
        return LEGACY_METHOD
    return SCOPED_METHOD


def tracked_paths(root: Path) -> tuple[str, ...]:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-z"], text=False
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot enumerate tracked paths: {exc}")
    values: list[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            path = item.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(f"tracked path is not UTF-8: {exc}")
        values.append(path)
    if len(values) != len(set(values)):
        fail("tracked path enumeration contains duplicates")
    return tuple(values)


def classify_path(path: str, manifest: Mapping[str, object]) -> str:
    _normalized_repo_path(path, "tracked path")
    method = identity_method(manifest)
    if path == MANIFEST_PATH:
        return MANIFEST_SELF_EXCLUDED
    if method == LEGACY_METHOD:
        return RELEASE_INCLUDED
    if _is_protected_release_path(path):
        return RELEASE_INCLUDED
    identity = manifest["content_identity"]
    assert isinstance(identity, dict)
    exact_paths = identity["operational_exact_paths"]
    assert isinstance(exact_paths, list)
    if path in exact_paths:
        return OPERATIONAL_EXCLUDED
    if path.startswith(SCOPED_V1_RESERVED_OPERATIONAL_PREFIXES):
        return OPERATIONAL_EXCLUDED
    return RELEASE_INCLUDED


def classify_tracked_paths(paths: Sequence[str], manifest: Mapping[str, object]) -> Classification:
    validate_release_manifest(manifest)
    if len(paths) != len(set(paths)):
        fail("tracked path input contains duplicates")
    included: list[str] = []
    excluded: list[str] = []
    manifest_seen = False
    for raw in paths:
        path = _normalized_repo_path(raw, "tracked path")
        classification = classify_path(path, manifest)
        if classification == MANIFEST_SELF_EXCLUDED:
            manifest_seen = True
        elif classification == OPERATIONAL_EXCLUDED:
            excluded.append(path)
        else:
            included.append(path)
    if not manifest_seen:
        fail("tracked release checkout must include release-manifest.json")
    return Classification(
        included=tuple(sorted(included)),
        operational_excluded=tuple(sorted(excluded)),
    )


def _digest_paths(root: Path, paths: Iterable[str]) -> str:
    records: list[tuple[str, str]] = []
    for path in paths:
        _normalized_repo_path(path, "release content path")
        target = root / path
        if not target.exists() or target.is_dir():
            fail(f"release content path is missing or not a file: {path}")
        records.append((path, file_digest(target)))
    encoded = "".join(
        f"{path}\0{hash_value}\n" for path, hash_value in sorted(records)
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def content_digest(root: Path, manifest: Mapping[str, object]) -> str:
    method = identity_method(manifest)
    paths = tracked_paths(root)
    if method == LEGACY_METHOD:
        return _digest_paths(root, (path for path in paths if path != MANIFEST_PATH))
    classification = classify_tracked_paths(paths, manifest)
    return _digest_paths(root, classification.included)


def release_content_digest(root: Path) -> str:
    manifest = load_release_manifest(root)
    return content_digest(root, manifest)


def _git_head_or_none(root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_projection(source: Path, destination: Path) -> dict:
    source = source.resolve()
    destination = destination.resolve()
    manifest = load_release_manifest(source)
    if identity_method(manifest) != SCOPED_METHOD:
        fail("isolated release-payload projection requires SCOPED_TRACKED_FILES_V1")
    if destination.exists():
        fail("projection destination must not already exist")
    classification = classify_tracked_paths(tracked_paths(source), manifest)
    destination.mkdir(parents=True)
    for relative in classification.included + (MANIFEST_PATH,):
        source_path = source / relative
        if not source_path.exists() or source_path.is_dir():
            fail(f"projection source path is missing or not a file: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source_path.read_bytes())
    included_records = [
        {"path": path, "sha256": file_digest(source / path)}
        for path in classification.included
    ]
    index = {
        "schema": "gg.release-payload-projection-index/1.0.0",
        "source_commit": _git_head_or_none(source),
        "release_manifest_sha256": file_digest(source / MANIFEST_PATH),
        "content_sha256": manifest["content_sha256"],
        "included": included_records,
        "operational_excluded": list(classification.operational_excluded),
    }
    (destination / PROJECTION_INDEX).write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    verify_projection(destination, index)
    return index


def _load_projection_index(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid projection index {path}: {exc}")
    if not isinstance(value, dict):
        fail("projection index must be a JSON object")
    return value


def verify_projection(projection: Path, index: Mapping[str, object] | None = None) -> None:
    projection = projection.resolve()
    if index is None:
        index = _load_projection_index(projection / PROJECTION_INDEX)
    expected_keys = {
        "schema",
        "source_commit",
        "release_manifest_sha256",
        "content_sha256",
        "included",
        "operational_excluded",
    }
    if set(index) != expected_keys:
        fail("projection index shape is invalid")
    if index["schema"] != "gg.release-payload-projection-index/1.0.0":
        fail("projection index schema is unsupported")
    _validate_sha256(index["release_manifest_sha256"], "projection manifest hash")
    _validate_sha256(index["content_sha256"], "projection content hash")
    manifest_path = projection / MANIFEST_PATH
    if file_digest(manifest_path) != index["release_manifest_sha256"]:
        fail("projection release manifest hash mismatch")
    manifest = load_release_manifest(projection)
    if identity_method(manifest) != SCOPED_METHOD:
        fail("projection manifest is not scoped")
    if manifest["content_sha256"] != index["content_sha256"]:
        fail("projection index content identity does not match manifest")
    included_raw = index["included"]
    excluded_raw = index["operational_excluded"]
    if not isinstance(included_raw, list) or not isinstance(excluded_raw, list):
        fail("projection index path sets are invalid")
    included_paths: list[str] = []
    for item in included_raw:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            fail("projection included record shape is invalid")
        path = _normalized_repo_path(item["path"], "projection included path")
        _validate_sha256(item["sha256"], f"projection included hash for {path}")
        if file_digest(projection / path) != item["sha256"]:
            fail(f"projection included file hash mismatch: {path}")
        included_paths.append(path)
    if len(included_paths) != len(set(included_paths)):
        fail("projection included paths contain duplicates")
    excluded_paths: list[str] = []
    for raw in excluded_raw:
        path = _normalized_repo_path(raw, "projection excluded path")
        if (projection / path).exists():
            fail(f"projection contains operationally excluded path: {path}")
        excluded_paths.append(path)
    if len(excluded_paths) != len(set(excluded_paths)):
        fail("projection excluded paths contain duplicates")
    expected_files = set(included_paths) | {MANIFEST_PATH, PROJECTION_INDEX}
    actual_files = {
        path.relative_to(projection).as_posix()
        for path in projection.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        fail(f"projection file-set mismatch: missing={missing} extra={extra}")
    if (projection / ".git").exists():
        fail("projection must not contain .git")
    reproduced = _digest_paths(projection, included_paths)
    if reproduced != index["content_sha256"]:
        fail("projection content digest does not reproduce manifest content identity")


def _cli() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    digest_parser = sub.add_parser("digest")
    digest_parser.add_argument("root", type=Path)
    project_parser = sub.add_parser("project")
    project_parser.add_argument("source", type=Path)
    project_parser.add_argument("destination", type=Path)
    verify_parser = sub.add_parser("verify-projection")
    verify_parser.add_argument("projection", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "digest":
            print(release_content_digest(args.root.resolve()))
        elif args.command == "project":
            index = build_projection(args.source.resolve(), args.destination)
            print(json.dumps(index, sort_keys=True))
        else:
            verify_projection(args.projection.resolve())
            print("PASS: isolated release-payload projection integrity")
    except ValueError as exc:
        import sys
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
