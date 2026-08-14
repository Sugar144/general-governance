#!/usr/bin/env python3
"""Deterministic GOV-GEN external-consumer conformance validator."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.core.l6.schemas import load_schema, validate as validate_schema
from framework.core.l6.strict_yaml import StrictYAMLError, load as load_yaml

SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
PLACEHOLDER = re.compile(r"\{\{(configuration(?:\.[A-Za-z0-9_]+)+)\}\}")
UNRESOLVED = re.compile(r"\{\{[^{}]+\}\}")
PROMPT_NAMESPACE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,63}$")

CURRENT_COMPATIBILITY = {
    "framework_contract": "2.0.0",
    "consumer_lock_schema": "2.0.0",
    "consumer_configuration_schema": "1.0.0",
}
LEGACY_V1_COMPATIBILITY = {
    "framework_contract": "1.0.0",
    "consumer_lock_schema": "1.0.0",
}

REQUIRED = (
    "framework/core/project-operating-contract.md",
    "framework/contracts/configuration-schema.yaml",
    "framework/core/l6/authority.py",
    "framework/core/l6/identity.py",
    "contracts/consumer-lock.schema.json",
    "contracts/consumer-lock-v1.schema.json",
    "contracts/consumer-configuration.schema.json",
    "contracts/framework-upgrade.schema.json",
    "provenance/extraction-manifest.json",
    "release-manifest.json",
)
FORBIDDEN_CONSUMER_PREFIXES = ("framework/", "governance/core/", "governance/contracts/")


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
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
    tracked = subprocess.check_output(
        ["git", "-C", str(framework), "ls-files", "-z"], text=False
    ).split(b"\0")
    records = []
    for raw_path in tracked:
        relative = raw_path.decode("utf-8")
        if relative and relative != "release-manifest.json":
            records.append((relative, digest(framework / relative)))
    encoded = "".join(
        f"{path}\0{hash_value}\n" for path, hash_value in sorted(records)
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _validate_framework_identity(framework: object) -> dict:
    if not isinstance(framework, dict) or set(framework) != {
        "repository", "version", "commit_sha", "release_manifest_sha256"
    }:
        fail("framework identity shape is invalid")
    if framework["repository"] != "Sugar144/general-governance":
        fail("framework repository identity is invalid")
    if not isinstance(framework["version"], str) or not re.fullmatch(
        r"0\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?", framework["version"]
    ):
        fail("framework version is invalid")
    if not COMMIT.fullmatch(framework["commit_sha"]):
        fail("floating or non-immutable framework commit is invalid")
    if not SHA256.fullmatch(framework["release_manifest_sha256"]):
        fail("release manifest hash is invalid")
    return framework


def _safe_relative_consumer_path(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        fail("consumer configuration_path must be a non-empty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) == ".":
        fail("consumer configuration_path escapes consumer repository")
    return value


def validate_lock(lock: dict) -> dict:
    if set(lock) != {"schema_version", "framework", "consumer", "compatibility"}:
        fail("consumer lock shape is invalid")
    if lock["schema_version"] != "2.0.0":
        fail("unsupported current consumer lock schema_version")
    identity = _validate_framework_identity(lock["framework"])
    consumer = lock["consumer"]
    if not isinstance(consumer, dict) or set(consumer) != {"configuration_path"}:
        fail("consumer binding shape is invalid")
    _safe_relative_consumer_path(consumer["configuration_path"])
    if lock["compatibility"] != CURRENT_COMPATIBILITY:
        fail("unsupported compatibility declaration")
    return identity


def validate_previous_lock(lock: dict) -> dict:
    schema_version = lock.get("schema_version")
    if schema_version == "1.0.0":
        if set(lock) != {"schema_version", "framework", "compatibility"}:
            fail("legacy previous lock shape is invalid")
        identity = _validate_framework_identity(lock["framework"])
        if lock["compatibility"] != LEGACY_V1_COMPATIBILITY:
            fail("legacy previous lock compatibility is invalid")
        return identity
    if schema_version == "2.0.0":
        return validate_lock(lock)
    fail("unsupported previous lock schema_version")


def validate_consumer_paths(consumer: Path) -> None:
    for path in consumer.rglob("*"):
        if path.is_file():
            relative = path.relative_to(consumer).as_posix()
            if relative.startswith(FORBIDDEN_CONSUMER_PREFIXES):
                fail(f"consumer duplicates or overrides framework-owned surface: {relative}")


def git_head(repository: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True
    ).strip()


def _get_nested(value: dict, dotted: str) -> Any:
    current: Any = value
    for key in dotted.split("."):
        if not isinstance(current, dict) or key not in current:
            fail(f"required consumer configuration value is missing: {dotted}")
        current = current[key]
    return current


def _walk_values(value: Any, path: str = "configuration") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _walk_values(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _walk_values(item, f"{path}[{index}]")
    elif isinstance(value, str) and UNRESOLVED.search(value):
        fail(f"unresolved configuration placeholder at {path}")


def _core_placeholders(framework: Path) -> set[str]:
    result: set[str] = set()
    core = framework / "framework/core"
    for path in core.rglob("*"):
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            result.update(PLACEHOLDER.findall(text))
    return result


def _declared_configuration_keys(framework: Path) -> set[str]:
    path = framework / "framework/contracts/configuration-schema.yaml"
    try:
        contract = load_yaml(path)
    except StrictYAMLError as exc:
        fail(f"invalid framework configuration contract: {exc}")
    if not isinstance(contract, dict):
        fail("framework configuration contract must be a mapping")
    keys = contract.get("required_configuration_keys")
    if not isinstance(keys, list) or not keys or any(
        not isinstance(key, str) or not key.startswith("configuration.") for key in keys
    ):
        fail("framework required_configuration_keys is invalid")
    if len(keys) != len(set(keys)):
        fail("framework required_configuration_keys contains duplicates")
    return set(keys)


def _require_nonempty_string(config: dict, dotted: str) -> str:
    value = _get_nested(config, dotted)
    if not isinstance(value, str) or not value.strip():
        fail(f"consumer configuration value must be a non-empty string: {dotted}")
    return value


def validate_configuration(
    framework: Path, consumer: Path, lock: dict
) -> Path:
    relative = _safe_relative_consumer_path(lock["consumer"]["configuration_path"])
    path = (consumer / relative).resolve()
    try:
        path.relative_to(consumer.resolve())
    except ValueError:
        fail("consumer configuration_path escapes consumer repository")
    if not path.is_file():
        fail(f"required consumer configuration is missing: {relative}")
    try:
        document = load_yaml(path)
    except StrictYAMLError as exc:
        fail(f"invalid consumer configuration: {exc}")
    if not isinstance(document, dict) or not isinstance(document.get("configuration"), dict):
        fail("consumer configuration must be a mapping with top-level configuration")
    schema = load_schema(framework / "contracts/consumer-configuration.schema.json")
    diagnostics = validate_schema(document, schema, prefix="$consumer_configuration")
    if diagnostics:
        first = diagnostics[0]
        fail(f"consumer configuration schema validation failed at {first.path}: {first.message}")
    config = document
    declared = _declared_configuration_keys(framework)
    placeholders = _core_placeholders(framework)
    undeclared = placeholders - declared
    if undeclared:
        fail(f"core contains undeclared configuration placeholders: {sorted(undeclared)}")
    for dotted in sorted(declared):
        _get_nested(config, dotted)
    for dotted in sorted(placeholders):
        _get_nested(config, dotted)
    _walk_values(document, path.relative_to(consumer).as_posix())

    for dotted in (
        "configuration.correction_example.base_run_id",
        "configuration.correction_example.first_correction_id",
        "configuration.paths.formal_run_prompt_snapshots",
        "configuration.paths.learning_readme",
        "configuration.identity_allocator.namespace",
        "configuration.identity_allocator.state_path",
        "configuration.identity_allocator.ledger_path",
    ):
        _require_nonempty_string(config, dotted)

    namespace = _require_nonempty_string(config, "configuration.prompt_identity.namespace")
    if not PROMPT_NAMESPACE.fullmatch(namespace):
        fail("configuration.prompt_identity.namespace is invalid")
    width = _get_nested(config, "configuration.prompt_identity.sequence_width")
    if isinstance(width, bool) or not isinstance(width, int) or not 1 <= width <= 12:
        fail("configuration.prompt_identity.sequence_width must be an integer from 1 to 12")
    return path


def validate(
    lock_path: Path,
    framework: Path,
    consumer: Path,
    previous: Path | None = None,
) -> None:
    lock = load_json(lock_path)
    identity = validate_lock(lock)
    validate_consumer_paths(consumer)

    if git_head(framework) != identity["commit_sha"]:
        fail("framework checkout does not equal immutable locked commit")
    manifest_path = framework / "release-manifest.json"
    if digest(manifest_path) != identity["release_manifest_sha256"]:
        fail("locked release manifest hash does not match framework content")
    manifest = load_json(manifest_path)
    if manifest.get("framework_version") != identity["version"]:
        fail("locked framework version does not match release manifest")
    if manifest.get("compatibility") != lock["compatibility"]:
        fail("locked compatibility is not supported by release")
    if manifest.get("content_sha256") != release_content_digest(framework):
        fail("release manifest content identity does not reproduce framework content")

    for relative in REQUIRED:
        if not (framework / relative).is_file():
            fail(f"required framework surface is missing: {relative}")

    validate_configuration(framework, consumer, lock)

    if previous is not None:
        old_identity = validate_previous_lock(load_json(previous))
        if old_identity == identity:
            fail("controlled upgrade must change immutable framework identity")

    print(
        "PASS: immutable lock, release identity, compatibility, required consumer "
        "configuration, core placeholder resolution, and ownership boundary"
    )


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
