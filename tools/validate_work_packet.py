#!/usr/bin/env python3
"""Deterministically validate declared WPDC machine claims.

This validator checks only represented machine-contract facts. It does not infer
undeclared semantic prerequisites and never grants execution authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.core.l6.strict_yaml import StrictYAMLError, load as load_yaml
from tools.validate_consumer import (
    digest as framework_file_digest,
    git_head as framework_git_head,
    release_content_digest,
)

BINDING_SCHEMA = ROOT / "contracts" / "work-packet-capability-binding.schema.json"
MANIFEST_SCHEMA = ROOT / "contracts" / "work-packet-manifest.schema.json"
CONSUMER_CONFIGURATION_SCHEMA = ROOT / "contracts" / "consumer-configuration.schema.json"
CONSUMER_LOCK_SCHEMA = ROOT / "contracts" / "consumer-lock.schema.json"
EXPECTED_WPDC_RELEASE = {
    "contract_version": "1.0.0",
    "adoption_contract_version": "1.0.0",
    "binding_schema_version": "1.0.0",
    "manifest_schema_version": "1.0.0",
    "optional": True,
}


@dataclass(frozen=True)
class PacketEvaluation:
    disposition: str
    unresolved_prerequisites: tuple[str, ...] = ()


class ValidationFailure(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class CapabilityAbsent(RuntimeError):
    """The adopter configuration does not activate optional WPDC."""


def fail(code: str, message: str) -> None:
    raise ValidationFailure(code, message)


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail("SCHEMA_INVALID", f"invalid {label} JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail("SCHEMA_INVALID", f"{label} must be a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def validate_schema(document: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: [str(part) for part in error.path],
    )
    if errors:
        first = errors[0]
        where = "$" + "".join(f"[{part!r}]" for part in first.path)
        fail(
            "SCHEMA_INVALID",
            f"{label} schema validation failed at {where}: {first.message}",
        )


def load_adopter_configuration(path: Path) -> dict[str, Any]:
    try:
        value = load_yaml(path)
    except (OSError, StrictYAMLError) as exc:
        fail("INVALID_ADOPTION_BINDING", f"invalid adopter configuration {path}: {exc}")
    if not isinstance(value, dict):
        fail("INVALID_ADOPTION_BINDING", "adopter configuration must be a mapping")
    schema = json.loads(CONSUMER_CONFIGURATION_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: [str(part) for part in error.path],
    )
    if errors:
        first = errors[0]
        where = "$" + "".join(f"[{part!r}]" for part in first.path)
        fail(
            "INVALID_ADOPTION_BINDING",
            f"adopter configuration schema validation failed at {where}: {first.message}",
        )
    return value


def verify_locked_framework_identity(
    lock: dict[str, Any], framework_root: Path = ROOT
) -> None:
    """Bind WPDC use to the exact locked GG release that advertises WPDC."""
    framework = framework_root.resolve()
    identity = lock["framework"]
    try:
        actual_head = framework_git_head(framework)
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(
            "INVALID_ADOPTION_BINDING",
            f"cannot resolve running General Governance checkout identity: {exc}",
        )
    if actual_head != identity["commit_sha"]:
        fail(
            "INVALID_ADOPTION_BINDING",
            "running General Governance checkout does not equal the immutable commit selected by framework-lock.json",
        )

    release_manifest_path = framework / "release-manifest.json"
    if not release_manifest_path.is_file():
        fail(
            "INVALID_ADOPTION_BINDING",
            "locked General Governance checkout lacks release-manifest.json",
        )
    if framework_file_digest(release_manifest_path) != identity["release_manifest_sha256"]:
        fail(
            "INVALID_ADOPTION_BINDING",
            "framework-lock.json release manifest hash does not match the running General Governance checkout",
        )
    release_manifest = load_json(release_manifest_path, "General Governance release manifest")
    if release_manifest.get("framework_version") != identity["version"]:
        fail(
            "INVALID_ADOPTION_BINDING",
            "framework-lock.json version does not match the running General Governance release manifest",
        )
    if release_manifest.get("compatibility") != lock["compatibility"]:
        fail(
            "INVALID_ADOPTION_BINDING",
            "framework-lock.json compatibility is not supported by the running General Governance release",
        )
    try:
        reproduced = release_content_digest(framework)
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(
            "INVALID_ADOPTION_BINDING",
            f"cannot reproduce General Governance release content identity: {exc}",
        )
    if release_manifest.get("content_sha256") != reproduced:
        fail(
            "INVALID_ADOPTION_BINDING",
            "running General Governance release content identity does not reproduce release-manifest.json",
        )
    if release_manifest.get("work_packet_design") != EXPECTED_WPDC_RELEASE:
        fail(
            "INVALID_ADOPTION_BINDING",
            "locked General Governance release does not advertise the supported WPDC contract and machine versions",
        )


def verify_configuration_selected_by_consumer_lock(
    configuration_path: Path, repository_root: Path
) -> None:
    root = repository_root.resolve()
    lock_path = root / "framework-lock.json"
    if not lock_path.is_file():
        fail(
            "INVALID_ADOPTION_BINDING",
            "consumer framework-lock.json is required to resolve the governing adopter configuration",
        )
    lock = load_json(lock_path, "consumer framework lock")
    schema = json.loads(CONSUMER_LOCK_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(lock),
        key=lambda error: [str(part) for part in error.path],
    )
    if errors:
        first = errors[0]
        where = "$" + "".join(f"[{part!r}]" for part in first.path)
        fail(
            "INVALID_ADOPTION_BINDING",
            f"consumer framework lock schema validation failed at {where}: {first.message}",
        )

    verify_locked_framework_identity(lock)

    selected = lock["consumer"]["configuration_path"]
    selected_path = (root / selected).resolve()
    try:
        selected_path.relative_to(root)
    except ValueError:
        fail(
            "INVALID_ADOPTION_BINDING",
            "consumer framework lock configuration_path escapes the adopter repository",
        )
    if not selected_path.is_file():
        fail(
            "INVALID_ADOPTION_BINDING",
            f"framework-lock.json selected adopter configuration does not exist: {selected}",
        )
    if selected_path != configuration_path.resolve():
        fail(
            "INVALID_ADOPTION_BINDING",
            "supplied adopter configuration is not the configuration selected by framework-lock.json",
        )


def verify_adoption_selection(
    configuration_path: Path, binding_path: Path, repository_root: Path
) -> None:
    root = repository_root.resolve()
    config_path = configuration_path.resolve()
    try:
        config_path.relative_to(root)
    except ValueError:
        fail(
            "INVALID_ADOPTION_BINDING",
            "adopter configuration must be inside the supplied adopter repository",
        )
    if not config_path.is_file():
        fail(
            "INVALID_ADOPTION_BINDING",
            f"adopter configuration does not exist: {configuration_path}",
        )

    document = load_adopter_configuration(config_path)
    configuration = document.get("configuration")
    if not isinstance(configuration, dict):
        fail(
            "INVALID_ADOPTION_BINDING",
            "adopter configuration lacks the top-level configuration mapping",
        )
    capabilities = configuration.get("capabilities")
    if capabilities is None:
        raise CapabilityAbsent(
            "configuration.capabilities.work_packet_design.binding_path is absent"
        )
    if not isinstance(capabilities, dict):
        fail(
            "INVALID_ADOPTION_BINDING",
            "configuration.capabilities must be a mapping when present",
        )
    if "work_packet_design" not in capabilities:
        raise CapabilityAbsent(
            "configuration.capabilities.work_packet_design.binding_path is absent"
        )
    wpdc = capabilities["work_packet_design"]
    if not isinstance(wpdc, dict):
        fail(
            "INVALID_ADOPTION_BINDING",
            "configuration.capabilities.work_packet_design must be a mapping",
        )
    selected = wpdc.get("binding_path")
    if not isinstance(selected, str) or not selected.strip():
        fail(
            "INVALID_ADOPTION_BINDING",
            "configuration.capabilities.work_packet_design.binding_path must be a non-empty path",
        )

    selected_path = Path(selected)
    if not selected_path.is_absolute():
        selected_path = root / selected_path
    selected_path = selected_path.resolve()
    if not selected_path.is_file():
        fail(
            "INVALID_ADOPTION_BINDING",
            f"configured WPDC binding does not exist: {selected}",
        )
    if selected_path != binding_path.resolve():
        fail(
            "INVALID_ADOPTION_BINDING",
            "supplied WPDC binding is not the binding selected by adopter configuration",
        )


def unique_index(
    items: Iterable[dict[str, Any]], key: str, label: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        identity = item[key]
        if identity in result:
            fail("DUPLICATE_ID", f"duplicate {label} identity: {identity}")
        result[identity] = item
    return result


def validate_binding(binding: dict[str, Any]) -> dict[str, Any]:
    validate_schema(binding, BINDING_SCHEMA, "WPDC binding")
    sources = unique_index(binding["source_bindings"], "source_id", "source")
    rules = unique_index(
        binding.get("currentness_rules", []), "rule_id", "currentness rule"
    )
    for source in sources.values():
        ref = source.get("currentness_rule_ref")
        if ref is not None and ref not in rules:
            fail(
                "INVALID_ADOPTION_BINDING",
                f"source {source['source_id']} references unknown currentness rule {ref}",
            )
    return {"sources": sources, "rules": rules}


def verify_binding_identity(
    manifest: dict[str, Any], binding: dict[str, Any], binding_path: Path
) -> None:
    declared = manifest["adoption_binding"]
    if declared["binding_id"] != binding["binding_id"]:
        fail(
            "INVALID_ADOPTION_BINDING",
            "manifest adoption binding_id does not match supplied binding",
        )
    if declared["sha256"] != sha256(binding_path):
        fail(
            "ADOPTION_BINDING_DIGEST_MISMATCH",
            "manifest adoption binding digest does not match supplied binding bytes",
        )
    if manifest["capability_contract_version"] != binding["capability_contract_version"]:
        fail(
            "INVALID_ADOPTION_BINDING",
            "manifest capability contract version does not match supplied binding",
        )


def verify_canonical_base(
    manifest: dict[str, Any], binding: dict[str, Any], repository_root: Path
) -> None:
    adopter_repo = binding["adopter"].get("repository")
    if (
        adopter_repo is not None
        and manifest["canonical_base"]["repository"] != adopter_repo
    ):
        fail(
            "INVALID_CANONICAL_BASE",
            "manifest canonical repository does not match adopter repository bound by WPDC adoption",
        )

    root = repository_root.resolve()
    if not root.is_dir():
        fail(
            "INVALID_CANONICAL_BASE",
            f"adopter repository root is not a directory: {repository_root}",
        )
    commit_sha = manifest["canonical_base"]["commit_sha"]
    try:
        subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{commit_sha}^{{commit}}"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        fail(
            "INVALID_CANONICAL_BASE",
            f"canonical commit is not resolvable in supplied adopter repository: {commit_sha}",
        )


def authority_index(
    manifest: dict[str, Any], sources: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    authorities = unique_index(
        manifest["authority_refs"], "authority_ref_id", "authority reference"
    )
    for authority in authorities.values():
        source_id = authority.get("source_id")
        if source_id is None:
            continue
        source = sources.get(source_id)
        if source is None:
            fail(
                "UNRESOLVED_REFERENCE",
                f"authority reference {authority['authority_ref_id']} uses unknown source {source_id}",
            )
        if "AUTHORITY" not in source["classes"]:
            fail(
                "INVALID_SOURCE_CLASS",
                f"authority reference {authority['authority_ref_id']} uses non-authority source {source_id}",
            )
    for ref in manifest["required_authority_refs"]:
        if ref not in authorities:
            fail(
                "MISSING_AUTHORITY_DECLARATION",
                f"required authority reference does not resolve: {ref}",
            )
    return authorities


def verify_state_contexts(
    manifest: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    rules: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    contexts = unique_index(
        manifest["state_contexts"], "state_context_id", "state context"
    )
    for context in contexts.values():
        source_id = context["source_id"]
        source = sources.get(source_id)
        if source is not None and "STATE" not in source["classes"]:
            fail(
                "INVALID_SOURCE_CLASS",
                f"state context {context['state_context_id']} uses non-state mapped source {source_id}",
            )
        currentness = context["currentness"]
        if currentness["mode"] == "BINDING_RULE":
            rule_ref = currentness["rule_ref"]
            if rule_ref not in rules:
                fail(
                    "INVALID_ADOPTION_BINDING",
                    f"state context {context['state_context_id']} references unknown binding currentness rule {rule_ref}",
                )
            if source is None:
                fail(
                    "INVALID_ADOPTION_BINDING",
                    f"unmapped state context {context['state_context_id']} cannot use BINDING_RULE; use an exact currentness reference",
                )
            source_rule = source.get("currentness_rule_ref")
            if source_rule != rule_ref:
                fail(
                    "INVALID_ADOPTION_BINDING",
                    f"state context {context['state_context_id']} currentness rule {rule_ref} does not match source {source_id} rule {source_rule}",
                )
    return contexts


def verify_external_dependencies(
    manifest: dict[str, Any],
    authorities: dict[str, dict[str, Any]],
    rules: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    dependencies = unique_index(
        manifest["external_dependencies"],
        "external_dependency_id",
        "external dependency",
    )
    for dependency in dependencies.values():
        for ref in dependency["authority_refs"]:
            if ref not in authorities:
                fail(
                    "UNRESOLVED_REFERENCE",
                    f"external dependency {dependency['external_dependency_id']} references unknown authority {ref}",
                )
        currentness = dependency["currentness"]
        if (
            currentness["mode"] == "BINDING_RULE"
            and currentness["rule_ref"] not in rules
        ):
            fail(
                "INVALID_ADOPTION_BINDING",
                f"external dependency {dependency['external_dependency_id']} references unknown binding currentness rule {currentness['rule_ref']}",
            )
    return dependencies


def repository_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        fail(
            "INVALID_RESOLUTION_EVIDENCE",
            f"evidence path escapes adopter repository root: {relative}",
        )
    return path


def git_file_bytes(repository_root: Path, commit_sha: str, relative: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repository_root), "show", f"{commit_sha}:{relative}"],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        fail(
            "INVALID_RESOLUTION_EVIDENCE",
            f"canonical evidence path is not available at {commit_sha}: {relative}",
        )


def verify_evidence_files(
    manifest: dict[str, Any], repository_root: Path
) -> dict[str, dict[str, Any]]:
    """Verify exact evidence bytes in their declared evaluation context."""
    evidence = unique_index(manifest["evidence"], "evidence_id", "evidence")
    root = repository_root.resolve()
    if not root.is_dir():
        fail(
            "INVALID_EVIDENCE_ROOT",
            f"adopter repository root is not a directory: {repository_root}",
        )
    canonical = manifest["canonical_base"]

    for item in evidence.values():
        relative = item["path"]
        repository_path(root, relative)
        context = item["context"]

        if context["kind"] == "CANONICAL_BASE":
            if (
                context["repository"] != canonical["repository"]
                or context["commit_sha"] != canonical["commit_sha"]
            ):
                fail(
                    "EVIDENCE_IDENTITY_MISMATCH",
                    f"canonical evidence {item['evidence_id']} is not bound to the packet canonical base",
                )
            actual_digest = bytes_sha256(
                git_file_bytes(root, canonical["commit_sha"], relative)
            )
        else:
            path = repository_path(root, relative)
            if not path.is_file():
                fail(
                    "INVALID_RESOLUTION_EVIDENCE",
                    f"evidence file does not exist: {relative}",
                )
            actual_digest = sha256(path)

        if actual_digest != item["sha256"]:
            fail(
                "EVIDENCE_IDENTITY_MISMATCH",
                f"evidence digest mismatch: {relative}",
            )
    return evidence


def verify_declared_evidence_contexts(
    evidence: dict[str, dict[str, Any]],
    state_contexts: dict[str, dict[str, Any]],
    external_dependencies: dict[str, dict[str, Any]],
) -> None:
    """Validate context references and source/scope coherence for every evidence item."""
    for item in evidence.values():
        evidence_id = item["evidence_id"]
        scope = item["source_scope"]
        source_ref = item["source_ref"]
        context = item["context"]
        kind = context["kind"]

        if scope == "ADOPTER_OWNED" and source_ref in external_dependencies:
            fail(
                "INVALID_RESOLUTION_EVIDENCE",
                f"adopter-owned evidence {evidence_id} source_ref identifies a separately declared external dependency",
            )

        if kind == "CANONICAL_BASE":
            if scope != "ADOPTER_OWNED":
                fail(
                    "INVALID_RESOLUTION_EVIDENCE",
                    f"canonical-base evidence {evidence_id} must be adopter-owned",
                )
            continue

        if kind == "STATE_EVALUATION":
            if scope != "ADOPTER_OWNED":
                fail(
                    "INVALID_RESOLUTION_EVIDENCE",
                    f"state-evaluation evidence {evidence_id} must be adopter-owned",
                )
            state_ref = context["state_context_ref"]
            state = state_contexts.get(state_ref)
            if state is None:
                fail(
                    "UNRESOLVED_REFERENCE",
                    f"evidence {evidence_id} references unknown state context {state_ref}",
                )
            if state["source_id"] != source_ref:
                fail(
                    "INVALID_RESOLUTION_EVIDENCE",
                    f"evidence {evidence_id} source differs from its state context source",
                )
            continue

        if scope != "EXTERNAL_DEPENDENCY":
            fail(
                "INVALID_RESOLUTION_EVIDENCE",
                f"external-dependency evidence {evidence_id} must use external dependency scope",
            )
        external_ref = context["external_dependency_ref"]
        if external_ref not in external_dependencies:
            fail(
                "UNRESOLVED_REFERENCE",
                f"evidence {evidence_id} references unknown external dependency {external_ref}",
            )
        if source_ref != external_ref:
            fail(
                "INVALID_RESOLUTION_EVIDENCE",
                f"evidence {evidence_id} source differs from its external dependency context",
            )


def verify_evidence_semantics(
    manifest: dict[str, Any],
    evidence: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    state_contexts: dict[str, dict[str, Any]],
    external_dependencies: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    prereqs = unique_index(
        manifest["prerequisites"], "prerequisite_id", "prerequisite"
    )
    for prereq in prereqs.values():
        resolution = prereq["resolution"]
        kind = resolution["kind"]
        if kind in {"IN_PACKET", "UNRESOLVED"}:
            continue

        refs: list[dict[str, Any]] = []
        for evidence_ref in resolution["evidence_refs"]:
            item = evidence.get(evidence_ref)
            if item is None:
                fail(
                    "UNRESOLVED_REFERENCE",
                    f"prerequisite {prereq['prerequisite_id']} references unknown evidence {evidence_ref}",
                )
            refs.append(item)

        if kind == "PREEXISTING_SATISFIED":
            for item in refs:
                if item["source_scope"] != "ADOPTER_OWNED":
                    fail(
                        "INVALID_RESOLUTION_EVIDENCE",
                        f"prerequisite {prereq['prerequisite_id']} misclassifies externally supplied evidence as PREEXISTING_SATISFIED",
                    )
                if item["source_ref"] in external_dependencies:
                    fail(
                        "INVALID_RESOLUTION_EVIDENCE",
                        f"preexisting evidence {item['evidence_id']} source_ref identifies a separately declared external dependency",
                    )
                context = item["context"]
                if context["kind"] == "EXTERNAL_DEPENDENCY":
                    fail(
                        "INVALID_RESOLUTION_EVIDENCE",
                        f"preexisting evidence {item['evidence_id']} declares external dependency context",
                    )
                if context["kind"] == "CANONICAL_BASE":
                    canonical = manifest["canonical_base"]
                    if (
                        context["repository"] != canonical["repository"]
                        or context["commit_sha"] != canonical["commit_sha"]
                    ):
                        fail(
                            "EVIDENCE_IDENTITY_MISMATCH",
                            f"preexisting evidence {item['evidence_id']} is not bound to the packet canonical base",
                        )
                elif context["kind"] == "STATE_EVALUATION":
                    state_ref = context["state_context_ref"]
                    state = state_contexts.get(state_ref)
                    if state is None:
                        fail(
                            "UNRESOLVED_REFERENCE",
                            f"preexisting evidence {item['evidence_id']} references unknown state context {state_ref}",
                        )
                    if state["source_id"] != item["source_ref"]:
                        fail(
                            "INVALID_RESOLUTION_EVIDENCE",
                            f"preexisting evidence {item['evidence_id']} source differs from its state context source",
                        )

        elif kind == "BOUND_EXTERNAL_SATISFIED":
            external_ref = resolution["external_dependency_ref"]
            if external_ref not in external_dependencies:
                fail(
                    "UNRESOLVED_REFERENCE",
                    f"prerequisite {prereq['prerequisite_id']} references unknown external dependency {external_ref}",
                )
            for item in refs:
                if item["source_scope"] != "EXTERNAL_DEPENDENCY":
                    fail(
                        "INVALID_RESOLUTION_EVIDENCE",
                        f"prerequisite {prereq['prerequisite_id']} requires external evidence but {item['evidence_id']} is adopter-owned",
                    )
                if item["source_ref"] != external_ref:
                    fail(
                        "INVALID_RESOLUTION_EVIDENCE",
                        f"external evidence {item['evidence_id']} is bound to a different external dependency",
                    )
                context = item["context"]
                if (
                    context["kind"] != "EXTERNAL_DEPENDENCY"
                    or context["external_dependency_ref"] != external_ref
                ):
                    fail(
                        "INVALID_RESOLUTION_EVIDENCE",
                        f"external evidence {item['evidence_id']} lacks matching external dependency context",
                    )
    return prereqs


def verify_completion_and_validation_refs(
    manifest: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    outcomes = unique_index(manifest["outcomes"], "outcome_id", "outcome")
    conditions = unique_index(
        manifest["completion_conditions"], "condition_id", "completion condition"
    )
    validations = unique_index(
        manifest["validations"], "validation_id", "validation"
    )
    for outcome in outcomes.values():
        if not outcome["completion_condition_refs"]:
            fail(
                "MISSING_COMPLETION_CONDITION",
                f"outcome {outcome['outcome_id']} has no completion conditions",
            )
        for ref in outcome["completion_condition_refs"]:
            if ref not in conditions:
                fail(
                    "UNRESOLVED_REFERENCE",
                    f"outcome {outcome['outcome_id']} references unknown completion condition {ref}",
                )
    for condition in conditions.values():
        if not condition["validation_refs"]:
            fail(
                "MISSING_VALIDATION_COVERAGE",
                f"completion condition {condition['condition_id']} has no validation coverage",
            )
        for ref in condition["validation_refs"]:
            if ref not in validations:
                fail(
                    "UNRESOLVED_REFERENCE",
                    f"completion condition {condition['condition_id']} references unknown validation {ref}",
                )
    return outcomes, conditions, validations


def dependency_graph(
    manifest: dict[str, Any],
    outcomes: dict[str, dict[str, Any]],
    prereqs: dict[str, dict[str, Any]],
) -> dict[str, set[str]]:
    overlap = set(outcomes) & set(prereqs)
    if overlap:
        fail(
            "DUPLICATE_ID",
            f"outcome/prerequisite node identity collision: {sorted(overlap)[0]}",
        )
    nodes = set(outcomes) | set(prereqs)
    graph: dict[str, set[str]] = {node: set() for node in nodes}
    seen: set[tuple[str, str, str]] = set()
    for edge in manifest["dependencies"]:
        dependent = edge["dependent_ref"]
        prerequisite = edge["prerequisite_ref"]
        relation = edge["relation"]
        if dependent not in nodes:
            fail(
                "UNRESOLVED_REFERENCE",
                f"dependency uses unknown dependent node {dependent}",
            )
        if prerequisite not in prereqs:
            fail(
                "UNRESOLVED_REFERENCE",
                f"dependency prerequisite_ref must resolve to a prerequisite: {prerequisite}",
            )
        identity = (dependent, prerequisite, relation)
        if identity in seen:
            fail(
                "DUPLICATE_DEPENDENCY",
                f"duplicate dependency edge: {dependent} -{relation}-> {prerequisite}",
            )
        seen.add(identity)
        graph[dependent].add(prerequisite)
    return graph


def reject_cycles(graph: dict[str, set[str]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: list[str]) -> None:
        if node in visiting:
            start = path.index(node) if node in path else 0
            fail(
                "DEPENDENCY_CYCLE",
                "dependency cycle detected: " + " -> ".join(path[start:] + [node]),
            )
        if node in visited:
            return
        visiting.add(node)
        path.append(node)
        for child in sorted(graph[node]):
            visit(child, path)
        path.pop()
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node, [])


def reachable_prerequisites(
    outcomes: dict[str, dict[str, Any]], graph: dict[str, set[str]]
) -> set[str]:
    reachable: set[str] = set()
    stack = list(outcomes)
    visited: set[str] = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for child in graph[node]:
            reachable.add(child)
            stack.append(child)
    return reachable


def verify_exclusions(
    manifest: dict[str, Any],
    outcomes: dict[str, dict[str, Any]],
    prereqs: dict[str, dict[str, Any]],
    reachable: set[str],
) -> None:
    known = set(outcomes) | set(prereqs)
    for node in manifest["execution_boundary"]["excluded_nodes"]:
        if node not in known:
            fail("UNRESOLVED_REFERENCE", f"excluded node does not resolve: {node}")
        if node in outcomes:
            fail(
                "INCLUDED_EXCLUDED_CONTRADICTION",
                f"included outcome is also excluded: {node}",
            )
        if node in reachable:
            kind = prereqs[node]["resolution"]["kind"]
            if kind in {"IN_PACKET", "UNRESOLVED"}:
                fail(
                    "EXCLUDED_REQUIRED_PREREQUISITE",
                    f"required prerequisite {node} is {kind} but excluded while its dependent outcome remains included",
                )


def evaluate(
    manifest: dict[str, Any],
    manifest_path: Path,
    binding: dict[str, Any],
    binding_path: Path,
    repository_root: Path,
) -> PacketEvaluation:
    validate_schema(manifest, MANIFEST_SCHEMA, "WPDC manifest")
    binding_state = validate_binding(binding)
    verify_binding_identity(manifest, binding, binding_path)
    verify_canonical_base(manifest, binding, repository_root)
    authorities = authority_index(manifest, binding_state["sources"])
    state_contexts = verify_state_contexts(
        manifest, binding_state["sources"], binding_state["rules"]
    )
    external_dependencies = verify_external_dependencies(
        manifest, authorities, binding_state["rules"]
    )
    evidence = verify_evidence_files(manifest, repository_root)
    verify_declared_evidence_contexts(
        evidence, state_contexts, external_dependencies
    )
    prereqs = verify_evidence_semantics(
        manifest,
        evidence,
        binding_state["sources"],
        state_contexts,
        external_dependencies,
    )
    outcomes, _, _ = verify_completion_and_validation_refs(manifest)
    graph = dependency_graph(manifest, outcomes, prereqs)
    reject_cycles(graph)
    reachable = reachable_prerequisites(outcomes, graph)
    verify_exclusions(manifest, outcomes, prereqs, reachable)
    unresolved = tuple(
        sorted(
            prereq_id
            for prereq_id in reachable
            if prereqs[prereq_id]["resolution"]["kind"] == "UNRESOLVED"
        )
    )
    if unresolved:
        return PacketEvaluation("VALID_BUT_BLOCKED", unresolved)
    return PacketEvaluation("VALID_DEPENDENCY_CLOSED")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a WPDC work-packet manifest against the exact binding selected by the exact locked General Governance release and adopter configuration"
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--binding", required=True, type=Path)
    parser.add_argument("--configuration", required=True, type=Path)
    parser.add_argument(
        "--repository-root",
        required=True,
        type=Path,
        help="adopter repository root containing framework-lock.json and the exact canonical/current evidence",
    )
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    binding_path = args.binding.resolve()
    configuration_path = args.configuration.resolve()
    repository_root = args.repository_root.resolve()
    try:
        verify_configuration_selected_by_consumer_lock(configuration_path, repository_root)
        verify_adoption_selection(configuration_path, binding_path, repository_root)
        manifest = load_json(manifest_path, "WPDC manifest")
        binding = load_json(binding_path, "WPDC binding")
        result = evaluate(
            manifest,
            manifest_path,
            binding,
            binding_path,
            repository_root,
        )
    except CapabilityAbsent as exc:
        print(f"WPDC_ABSENT: {exc}; no WPDC packet disposition is produced")
        return 2
    except ValidationFailure as exc:
        print(f"PACKET_INVALID: {exc.code}: {exc.message}")
        return 1
    if result.disposition == "VALID_BUT_BLOCKED":
        unresolved = ",".join(result.unresolved_prerequisites)
        print(
            "VALID_BUT_BLOCKED: declared WPDC model is coherent but has unresolved "
            f"required prerequisites: {unresolved}; no execution authority is implied"
        )
    else:
        print(
            "VALID_DEPENDENCY_CLOSED: declared WPDC dependency closure passes; "
            "no execution authority is implied"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
