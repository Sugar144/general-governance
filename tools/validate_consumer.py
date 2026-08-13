#!/usr/bin/env python3
"""Deterministic local GOV-GEN consumer-lock and separation validator."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
REQUIRED = (
    "framework/core/project-operating-contract.md",
    "framework/contracts/configuration-schema.yaml",
    "framework/core/l6/authority.py",
    "framework/core/l6/identity.py",
    "contracts/consumer-lock.schema.json",
    "provenance/extraction-manifest.json",
    "release-manifest.json",
)
FORBIDDEN_CONSUMER_PREFIXES = ("framework/", "governance/core/", "governance/contracts/")


def fail(message: str) -> None:
    raise ValueError(message)


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON object required: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_content_digest(framework: Path) -> str:
    tracked = subprocess.check_output(["git", "-C", str(framework), "ls-files", "-z"], text=False).split(b"\0")
    records = []
    for raw_path in tracked:
        relative = raw_path.decode("utf-8")
        if relative and relative != "release-manifest.json":
            records.append((relative, digest(framework / relative)))
    encoded = "".join(f"{path}\0{hash_value}\n" for path, hash_value in sorted(records))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def validate_lock(lock: dict) -> None:
    if set(lock) != {"schema_version", "framework", "compatibility"} or lock["schema_version"] != "1.0.0":
        fail("consumer lock shape or schema_version is invalid")
    framework = lock["framework"]
    if not isinstance(framework, dict) or set(framework) != {"repository", "version", "commit_sha", "release_manifest_sha256"}:
        fail("framework identity shape is invalid")
    if framework["repository"] != "Sugar144/general-governance":
        fail("framework repository identity is invalid")
    if not COMMIT.fullmatch(framework["commit_sha"]):
        fail("floating or non-immutable framework commit is invalid")
    if not SHA256.fullmatch(framework["release_manifest_sha256"]):
        fail("release manifest hash is invalid")
    if lock["compatibility"] != {"framework_contract": "1.0.0", "consumer_lock_schema": "1.0.0"}:
        fail("unsupported compatibility declaration")


def validate_consumer_paths(consumer: Path) -> None:
    for path in consumer.rglob("*"):
        if path.is_file():
            relative = path.relative_to(consumer).as_posix()
            if relative.startswith(FORBIDDEN_CONSUMER_PREFIXES):
                fail(f"consumer duplicates or overrides framework-owned surface: {relative}")


def git_head(repository: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repository), "rev-parse", "HEAD"], text=True).strip()


def validate(lock_path: Path, framework: Path, consumer: Path, previous: Path | None = None) -> None:
    lock = load(lock_path)
    validate_lock(lock)
    validate_consumer_paths(consumer)
    identity = lock["framework"]
    if git_head(framework) != identity["commit_sha"]:
        fail("framework checkout does not equal immutable locked commit")
    manifest_path = framework / "release-manifest.json"
    if digest(manifest_path) != identity["release_manifest_sha256"]:
        fail("locked release manifest hash does not match framework content")
    manifest = load(manifest_path)
    if manifest.get("framework_version") != identity["version"]:
        fail("locked framework version does not match release manifest")
    if manifest.get("compatibility") != lock["compatibility"]:
        fail("locked compatibility is not supported by release")
    if manifest.get("content_sha256") != release_content_digest(framework):
        fail("release manifest content identity does not reproduce framework content")
    for relative in REQUIRED:
        if not (framework / relative).is_file():
            fail(f"required framework surface is missing: {relative}")
    if previous is not None:
        old = load(previous)
        validate_lock(old)
        if old["framework"] == identity:
            fail("controlled upgrade must change immutable framework identity")
    print("PASS: immutable lock, release identity, compatibility, required surfaces, and ownership boundary")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumer", type=Path, required=True)
    parser.add_argument("--framework", type=Path, required=True)
    parser.add_argument("--lock", type=Path, default=None)
    parser.add_argument("--previous-lock", type=Path, default=None)
    args = parser.parse_args()
    try:
        consumer = args.consumer.resolve()
        lock = args.lock or consumer / "framework-lock.json"
        validate(lock, args.framework.resolve(), consumer, args.previous_lock)
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
