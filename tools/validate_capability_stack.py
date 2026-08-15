#!/usr/bin/env python3
"""Validate adopter-owned composition without interpreting component semantics."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "capability-stack.schema.json"
GG_REPOSITORY = "Sugar144/general-governance"


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail("capability stack must be a JSON object")
    return value


def validate_stack(document: dict) -> None:
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

    if document["status"] == "ACTIVE" and not document["compatibility_evidence"]:
        fail("ACTIVE capability stack requires compatibility evidence")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stack", type=Path)
    args = parser.parse_args()
    try:
        validate_stack(load_json(args.stack))
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: capability stack identity, role separation, and activation evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
