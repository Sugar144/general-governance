#!/usr/bin/env python3
"""Validate adopter-owned composition without interpreting component semantics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "capability-stack.schema.json"
GG_REPOSITORY = "Sugar144/general-governance"


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid {label} JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def component_set_sha256(components: list[dict]) -> str:
    material = "".join(
        f"{component['repository']}@{component['commit_sha']}\n"
        for component in sorted(components, key=lambda item: item["repository"])
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def verify_compatibility_evidence(
    stack_path: Path, references: list[dict], expected_component_set: str
) -> None:
    stack_dir = stack_path.resolve().parent
    for reference in references:
        evidence_path = (stack_dir / reference["path"]).resolve()
        try:
            evidence_path.relative_to(stack_dir)
        except ValueError:
            fail("compatibility evidence path escapes the stack document directory")
        if not evidence_path.is_file():
            fail(f"compatibility evidence file does not exist: {reference['path']}")

        actual_digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        if actual_digest != reference["sha256"]:
            fail(f"compatibility evidence digest mismatch: {reference['path']}")

        evidence = load_json(evidence_path, "compatibility evidence")
        if evidence.get("schema_version") != "1.0.0":
            fail("unsupported compatibility evidence schema_version")
        if evidence.get("component_set_sha256") != expected_component_set:
            fail("compatibility evidence is not bound to the current component set")
        if evidence.get("result") != "PASS":
            fail("compatibility evidence result must be PASS")


def validate_stack(document: dict, stack_path: Path) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    diagnostics = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.path),
    )
    if diagnostics:
        first = diagnostics[0]
        where = "$" + "".join(f"[{part!r}]" for part in first.path)
        fail(f"schema validation failed at {where}: {first.message}")

    components = document["components"]
    ids = [component["component_id"] for component in components]
    repositories = [component["repository"] for component in components]
    if len(ids) != len(set(ids)):
        fail("component_id values must be unique")
    if len(repositories) != len(set(repositories)):
        fail("a repository may appear only once in a stack")

    frameworks = [
        component
        for component in components
        if component["role"] == "GOVERNANCE_FRAMEWORK"
    ]
    if len(frameworks) != 1 or frameworks[0]["repository"] != GG_REPOSITORY:
        fail("exactly one General Governance GOVERNANCE_FRAMEWORK is required")

    for component in components:
        if component["role"] == "EVIDENCE_OBSERVABILITY_CAPABILITY":
            if component["governance_authority"] != "NONE":
                fail(
                    "evidence/observability capabilities must declare "
                    "governance_authority NONE"
                )
        elif component["governance_authority"] != "OWN_DOMAIN_ONLY":
            fail(
                "governance components must declare "
                "governance_authority OWN_DOMAIN_ONLY"
            )

    expected_component_set = component_set_sha256(components)
    if document["component_set_sha256"] != expected_component_set:
        fail("component_set_sha256 does not match the exact bound component set")

    references = document["compatibility_evidence"]
    if document["status"] == "ACTIVE" and not references:
        fail("ACTIVE capability stack requires compatibility evidence")
    if references:
        verify_compatibility_evidence(stack_path, references, expected_component_set)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stack", type=Path)
    args = parser.parse_args()
    try:
        stack_path = args.stack.resolve()
        validate_stack(load_json(stack_path, "capability stack"), stack_path)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: exact capability set, role separation, and activation evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
