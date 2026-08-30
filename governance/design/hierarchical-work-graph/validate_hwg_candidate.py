#!/usr/bin/env python3
"""Deterministically validate the non-normative HWG 0.1.0 candidate.

This tool validates represented structure only. It does not infer semantic
boundary preservation, authority, completion, execution readiness, or concurrent
compatibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
BUNDLE_SCHEMA = HERE / "contracts" / "hwg-bundle.schema.json"
GRAPH_SCHEMA = HERE / "contracts" / "work-graph.schema.json"


class ValidationFailure(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


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


def validate_schema(document: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: [str(part) for part in error.path],
    )
    if errors:
        first = errors[0]
        where = "$" + "".join(f"[{part!r}]" for part in first.path)
        fail("SCHEMA_INVALID", f"{label} schema validation failed at {where}: {first.message}")


def bounded_path(base: Path, relative: str, label: str) -> Path:
    raw = Path(relative)
    if raw.is_absolute():
        fail("PATH_OUTSIDE_BOUNDARY", f"{label} must be relative: {relative}")
    resolved = (base / raw).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        fail("PATH_OUTSIDE_BOUNDARY", f"{label} escapes its boundary: {relative}")
    return resolved


def unique_by(items: list[dict[str, Any]], field: str, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        identity = item[field]
        if identity in result:
            fail("DUPLICATE_ID", f"duplicate {label} identity: {identity}")
        result[identity] = item
    return result


def assert_dag(graph_id: str, nodes: dict[str, dict[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visited:
            return
        if node_id in visiting:
            fail("DEPENDENCY_CYCLE", f"dependency cycle in graph {graph_id} at node {node_id}")
        visiting.add(node_id)
        for dependency in nodes[node_id]["dependencies"]:
            visit(dependency)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in nodes:
        visit(node_id)


def verify_source_identity(source: dict[str, Any], source_root: Path | None) -> None:
    identity = source["identity"]
    kind = identity["kind"]
    value = identity["value"]
    if kind == "SHA256":
        if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
            fail("INVALID_SOURCE_IDENTITY", f"source {source['source_id']} has invalid SHA256 identity")
    elif kind == "GIT_BLOB_SHA1":
        if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
            fail("INVALID_SOURCE_IDENTITY", f"source {source['source_id']} has invalid Git blob identity")
    elif kind == "OPAQUE_EXACT":
        return

    if source_root is None:
        return

    path = bounded_path(source_root, source["locator"], f"source {source['source_id']} locator")
    if not path.is_file():
        fail("SOURCE_NOT_FOUND", f"source {source['source_id']} does not exist: {source['locator']}")
    if kind == "SHA256":
        actual = sha256(path)
    else:
        try:
            completed = subprocess.run(
                ["git", "-C", str(source_root), "hash-object", str(path)],
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            fail("SOURCE_IDENTITY_UNVERIFIABLE", f"cannot calculate Git blob identity for {source['locator']}: {exc}")
        actual = completed.stdout.strip()
    if actual != value:
        fail(
            "SOURCE_IDENTITY_MISMATCH",
            f"source {source['source_id']} identity mismatch: expected {value}, got {actual}",
        )


def validate_bundle(bundle_path: Path, *, source_root: Path | None = None) -> dict[str, Any]:
    bundle_path = bundle_path.resolve()
    bundle = load_json(bundle_path, "HWG bundle")
    validate_schema(bundle, BUNDLE_SCHEMA, "HWG bundle")

    levels = bundle["profile"]["levels"]
    level_ids = [level["level_id"] for level in levels]
    orders = [level["order"] for level in levels]
    if len(set(level_ids)) != len(level_ids):
        fail("DUPLICATE_ID", "profile level_id values must be unique")
    if len(set(orders)) != len(orders):
        fail("DUPLICATE_ORDER", "profile level order values must be unique")
    if sorted(orders) != list(range(1, len(levels) + 1)):
        fail("INVALID_LEVEL_ORDER", "profile level orders must be contiguous starting at 1")
    level_order = {level["level_id"]: level["order"] for level in levels}

    bundle_dir = bundle_path.parent
    graph_ref_paths: dict[Path, dict[str, Any]] = {}
    for ref in bundle["graph_refs"]:
        path = bounded_path(bundle_dir, ref["path"], "graph_ref.path")
        if path in graph_ref_paths:
            fail("DUPLICATE_REFERENCE", f"graph file referenced more than once: {ref['path']}")
        if not path.is_file():
            fail("GRAPH_NOT_FOUND", f"referenced graph does not exist: {ref['path']}")
        actual = sha256(path)
        if actual != ref["sha256"]:
            fail("GRAPH_DIGEST_MISMATCH", f"graph digest mismatch for {ref['path']}: expected {ref['sha256']}, got {actual}")
        graph_ref_paths[path] = ref

    root_path = bounded_path(bundle_dir, bundle["root_graph_ref"]["path"], "root_graph_ref.path")
    if root_path not in graph_ref_paths:
        fail("ROOT_NOT_LISTED", "root_graph_ref must also appear exactly once in graph_refs")
    if sha256(root_path) != bundle["root_graph_ref"]["sha256"]:
        fail("GRAPH_DIGEST_MISMATCH", "root_graph_ref digest does not match root graph bytes")

    graphs: dict[str, dict[str, Any]] = {}
    graph_paths: dict[str, Path] = {}
    node_indexes: dict[str, dict[str, dict[str, Any]]] = {}

    for path in graph_ref_paths:
        graph = load_json(path, "WorkGraph")
        validate_schema(graph, GRAPH_SCHEMA, "WorkGraph")
        graph_id = graph["graph_id"]
        if graph_id in graphs:
            fail("DUPLICATE_ID", f"duplicate graph_id: {graph_id}")
        if graph["profile_id"] != bundle["profile"]["profile_id"]:
            fail("PROFILE_MISMATCH", f"graph {graph_id} profile_id does not match bundle profile")
        if graph["level_id"] not in level_order:
            fail("UNKNOWN_LEVEL", f"graph {graph_id} uses unknown level_id {graph['level_id']}")

        sources = unique_by(graph["source_refs"], "source_id", f"source in graph {graph_id}")
        for source in sources.values():
            verify_source_identity(source, source_root)

        nodes = unique_by(graph["nodes"], "node_id", f"node in graph {graph_id}")
        for node in nodes.values():
            if node["node_id"] in node["dependencies"]:
                fail("SELF_DEPENDENCY", f"node {graph_id}/{node['node_id']} depends on itself")
            missing_deps = sorted(set(node["dependencies"]) - set(nodes))
            if missing_deps:
                fail("CROSS_GRAPH_OR_UNKNOWN_DEPENDENCY", f"node {graph_id}/{node['node_id']} references non-sibling dependencies: {missing_deps}")
            missing_sources = sorted(set(node["source_ref_ids"]) - set(sources))
            if missing_sources:
                fail("UNKNOWN_SOURCE_REFERENCE", f"node {graph_id}/{node['node_id']} references unknown source ids: {missing_sources}")
        assert_dag(graph_id, nodes)

        graphs[graph_id] = graph
        graph_paths[graph_id] = path
        node_indexes[graph_id] = nodes

    root_graph = load_json(root_path, "root WorkGraph")
    root_id = root_graph["graph_id"]
    if root_id not in graphs:
        fail("ROOT_NOT_LISTED", "root graph identity is not present in loaded graph set")
    if graphs[root_id]["parent_binding"] is not None:
        fail("INVALID_ROOT_PARENT", "root graph must have parent_binding = null")
    if level_order[graphs[root_id]["level_id"]] != 1:
        fail("INVALID_ROOT_LEVEL", "root graph must use the first profile level")

    child_claims: dict[str, tuple[str, str]] = {}
    for graph_id, graph in graphs.items():
        for node in node_indexes[graph_id].values():
            expansion = node["expansion"]
            if expansion["state"] != "MATERIALIZED":
                continue
            child_id = expansion["child_graph_id"]
            if child_id not in graphs:
                fail("UNKNOWN_CHILD_GRAPH", f"node {graph_id}/{node['node_id']} references unknown child graph {child_id}")
            if child_id in child_claims:
                first = child_claims[child_id]
                fail("MULTIPLE_PARENTS", f"child graph {child_id} is claimed by both {first[0]}/{first[1]} and {graph_id}/{node['node_id']}")
            child_claims[child_id] = (graph_id, node["node_id"])
            child = graphs[child_id]
            expected_parent = {"parent_graph_id": graph_id, "parent_node_id": node["node_id"]}
            if child["parent_binding"] != expected_parent:
                fail("PARENT_CHILD_MISMATCH", f"child graph {child_id} does not bind back to {graph_id}/{node['node_id']}")
            if level_order[child["level_id"]] != level_order[graph["level_id"]] + 1:
                fail("LEVEL_SKIP", f"expansion {graph_id}/{node['node_id']} -> {child_id} must advance exactly one profile level")

    for graph_id, graph in graphs.items():
        if graph_id == root_id:
            continue
        parent = graph["parent_binding"]
        if parent is None:
            fail("ORPHAN_GRAPH", f"non-root graph {graph_id} lacks parent_binding")
        if graph_id not in child_claims:
            fail("ORPHAN_GRAPH", f"non-root graph {graph_id} is not referenced by a MATERIALIZED parent expansion")

    visiting_graphs: set[str] = set()
    visited_graphs: set[str] = set()

    def walk(graph_id: str) -> None:
        if graph_id in visited_graphs:
            return
        if graph_id in visiting_graphs:
            fail("EXPANSION_CYCLE", f"hierarchy expansion cycle detected at graph {graph_id}")
        visiting_graphs.add(graph_id)
        for node in node_indexes[graph_id].values():
            expansion = node["expansion"]
            if expansion["state"] == "MATERIALIZED":
                walk(expansion["child_graph_id"])
        visiting_graphs.remove(graph_id)
        visited_graphs.add(graph_id)

    walk(root_id)
    unreachable = sorted(set(graphs) - visited_graphs)
    if unreachable:
        fail("ORPHAN_GRAPH", f"bundle contains graphs unreachable from root: {unreachable}")

    materialized_expansions = sum(
        1
        for graph_id in graphs
        for node in node_indexes[graph_id].values()
        if node["expansion"]["state"] == "MATERIALIZED"
    )
    return {
        "status": "VALID",
        "bundle_id": bundle["bundle_id"],
        "profile_id": bundle["profile"]["profile_id"],
        "graph_count": len(graphs),
        "node_count": sum(len(nodes) for nodes in node_indexes.values()),
        "materialized_expansions": materialized_expansions,
        "root_graph_id": root_id,
        "authority_granted": False,
        "parallel_safety_proven": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--source-root", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        result = validate_bundle(args.bundle, source_root=args.source_root)
    except ValidationFailure as exc:
        print(json.dumps({"status": "INVALID", "code": exc.code, "message": exc.message}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
