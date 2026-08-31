from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import validate_hierarchical_work_graph as hwg


def write_json(path: Path, value: dict) -> str:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(source_id: str) -> dict:
    return {
        "source_id": source_id,
        "locator": f"source/{source_id}.json",
        "identity": {"kind": "OPAQUE_EXACT", "value": f"exact:{source_id}:001"},
    }


def graph(graph_id: str, level_id: str, parent, nodes: list[dict]) -> dict:
    source_ids = sorted({ref for node in nodes for ref in node["source_ref_ids"]})
    return {
        "schema_version": "1.0.0",
        "kind": "WorkGraph",
        "graph_id": graph_id,
        "profile_id": "software-demo",
        "level_id": level_id,
        "parent_binding": parent,
        "source_refs": [source(item) for item in source_ids],
        "nodes": nodes,
    }


def node(node_id: str, *, deps=(), child=None, source_id=None) -> dict:
    return {
        "node_id": node_id,
        "source_ref_ids": [source_id or f"src-{node_id}"],
        "dependencies": list(deps),
        "expansion": (
            {"state": "MATERIALIZED", "child_graph_id": child}
            if child
            else {"state": "NOT_MATERIALIZED"}
        ),
    }


class HWGValidatorTests(unittest.TestCase):
    def build_bundle(self, root: Path, graphs: list[dict], root_graph_id="g-vs") -> Path:
        refs = []
        root_ref = None
        for item in graphs:
            path = root / f"{item['graph_id']}.json"
            digest = write_json(path, item)
            ref = {"path": path.name, "sha256": digest}
            refs.append(ref)
            if item["graph_id"] == root_graph_id:
                root_ref = ref
        self.assertIsNotNone(root_ref)
        bundle = {
            "schema_version": "1.0.0",
            "kind": "HierarchicalWorkGraphBundle",
            "bundle_id": "bundle-001",
            "profile": {
                "profile_id": "software-demo",
                "levels": [
                    {"level_id": "OUTCOME", "order": 1},
                    {"level_id": "WORK_PACKET", "order": 2},
                    {"level_id": "EXECUTION_UNIT", "order": 3},
                ],
            },
            "root_graph_ref": root_ref,
            "graph_refs": refs,
            "safety": {
                "graph_validity_grants_authority": False,
                "missing_dependency_proves_parallel_safety": False,
                "cross_level_dependency_edges_allowed": False,
            },
        }
        bundle_path = root / "bundle.json"
        write_json(bundle_path, bundle)
        return bundle_path

    def valid_graphs(self) -> list[dict]:
        return [
            graph(
                "g-vs",
                "OUTCOME",
                None,
                [
                    node("vs-a", child="g-wp-a"),
                    node("vs-b", deps=("vs-a",)),
                ],
            ),
            graph(
                "g-wp-a",
                "WORK_PACKET",
                {"parent_graph_id": "g-vs", "parent_node_id": "vs-a"},
                [
                    node("wp-a1", child="g-leaf-a1"),
                    node("wp-a2", deps=("wp-a1",)),
                ],
            ),
            graph(
                "g-leaf-a1",
                "EXECUTION_UNIT",
                {"parent_graph_id": "g-wp-a", "parent_node_id": "wp-a1"},
                [node("leaf-1"), node("leaf-2", deps=("leaf-1",))],
            ),
        ]

    def assert_invalid(self, graphs: list[dict], code: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.build_bundle(Path(tmp), graphs)
            with self.assertRaises(hwg.ValidationFailure) as captured:
                hwg.validate_bundle(bundle)
            self.assertEqual(captured.exception.code, code)

    def test_valid_three_level_progressive_hierarchy(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.build_bundle(Path(tmp), self.valid_graphs())
            result = hwg.validate_bundle(bundle)
            self.assertEqual(result["status"], "VALID_HIERARCHICAL_WORK_GRAPH")
            self.assertEqual(result["graph_count"], 3)
            self.assertEqual(result["node_count"], 6)
            self.assertEqual(result["materialized_expansions"], 2)
            self.assertFalse(result["authority_granted"])
            self.assertFalse(result["parallel_safety_proven"])

    def test_dependency_cycle_is_rejected(self):
        graphs = self.valid_graphs()
        graphs[0]["nodes"][0]["dependencies"] = ["vs-b"]
        self.assert_invalid(graphs, "DEPENDENCY_CYCLE")

    def test_cross_graph_or_unknown_dependency_is_rejected(self):
        graphs = self.valid_graphs()
        graphs[0]["nodes"][1]["dependencies"] = ["wp-a1"]
        self.assert_invalid(graphs, "CROSS_GRAPH_OR_UNKNOWN_DEPENDENCY")

    def test_child_without_matching_back_reference_is_rejected(self):
        graphs = self.valid_graphs()
        graphs[1]["parent_binding"]["parent_node_id"] = "vs-b"
        self.assert_invalid(graphs, "PARENT_CHILD_MISMATCH")

    def test_level_skip_is_rejected(self):
        graphs = self.valid_graphs()
        graphs[0]["nodes"][0]["expansion"]["child_graph_id"] = "g-leaf-a1"
        graphs[2]["parent_binding"] = {"parent_graph_id": "g-vs", "parent_node_id": "vs-a"}
        graphs[1]["nodes"][0]["expansion"] = {"state": "NOT_MATERIALIZED"}
        self.assert_invalid(graphs, "LEVEL_SKIP")

    def test_same_child_claimed_by_two_parents_is_rejected(self):
        graphs = self.valid_graphs()
        graphs[0]["nodes"][1]["expansion"] = {"state": "MATERIALIZED", "child_graph_id": "g-wp-a"}
        self.assert_invalid(graphs, "MULTIPLE_PARENTS")

    def test_unreachable_graph_is_rejected(self):
        graphs = self.valid_graphs()
        orphan = graph(
            "g-orphan",
            "WORK_PACKET",
            {"parent_graph_id": "g-vs", "parent_node_id": "vs-b"},
            [node("wp-orphan")],
        )
        graphs.append(orphan)
        self.assert_invalid(graphs, "ORPHAN_GRAPH")

    def test_graph_digest_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle_path = self.build_bundle(root, self.valid_graphs())
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            bundle["graph_refs"][0]["sha256"] = "0" * 64
            write_json(bundle_path, bundle)
            with self.assertRaises(hwg.ValidationFailure) as captured:
                hwg.validate_bundle(bundle_path)
            self.assertEqual(captured.exception.code, "GRAPH_DIGEST_MISMATCH")

    def test_graph_bytes_are_read_once_for_digest_and_parse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle_path = self.build_bundle(root, self.valid_graphs())
            original_read_bytes = Path.read_bytes
            reads: dict[Path, int] = {}

            def counted_read_bytes(path: Path) -> bytes:
                resolved = path.resolve()
                if resolved.parent == root.resolve() and resolved.name.startswith("g-"):
                    reads[resolved] = reads.get(resolved, 0) + 1
                return original_read_bytes(path)

            with mock.patch.object(Path, "read_bytes", counted_read_bytes):
                result = hwg.validate_bundle(bundle_path)

            self.assertEqual(result["status"], "VALID_HIERARCHICAL_WORK_GRAPH")
            self.assertEqual(len(reads), 3)
            self.assertTrue(all(count == 1 for count in reads.values()), reads)

    def test_long_dependency_chain_does_not_depend_on_python_recursion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chain = []
            for index in range(1500):
                node_id = f"n-{index:04d}"
                deps = (f"n-{index - 1:04d}",) if index else ()
                chain.append(node(node_id, deps=deps))
            bundle = self.build_bundle(root, [graph("g-vs", "OUTCOME", None, chain)])
            result = hwg.validate_bundle(bundle)
            self.assertEqual(result["status"], "VALID_HIERARCHICAL_WORK_GRAPH")
            self.assertEqual(result["node_count"], 1500)

    def test_absent_discovery_key_means_capability_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "configuration.yaml"
            config.write_text("configuration:\n  capabilities: {}\n", encoding="utf-8")
            self.assertIsNone(hwg.validate_selected_consumer_bundle(config, root))

    def test_selected_bundle_is_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hwg_dir = root / "hwg"
            hwg_dir.mkdir()
            self.build_bundle(hwg_dir, self.valid_graphs())
            config = root / "configuration.yaml"
            config.write_text(
                "configuration:\n"
                "  capabilities:\n"
                "    hierarchical_work_graph:\n"
                "      bundle_path: hwg/bundle.json\n",
                encoding="utf-8",
            )
            result = hwg.validate_selected_consumer_bundle(config, root)
            self.assertIsNotNone(result)
            self.assertEqual(result["status"], "VALID_HIERARCHICAL_WORK_GRAPH")


if __name__ == "__main__":
    unittest.main()