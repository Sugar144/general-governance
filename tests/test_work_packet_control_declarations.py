from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "contracts/work-packet-manifest.schema.json").read_text(encoding="utf-8")
)


def valid_manifest() -> dict:
    return {
        "schema_version": "1.0.0",
        "packet_id": "PACKET-CONTROLS-001",
        "capability_contract_version": "1.0.0",
        "adoption_binding": {
            "binding_id": "BINDING-001",
            "sha256": "0" * 64,
        },
        "canonical_base": {
            "repository": "acme/example",
            "commit_sha": "1" * 40,
        },
        "authority_refs": [
            {
                "authority_ref_id": "AUTH-001",
                "identity": "authority:owner@sha256:" + "a" * 64,
            }
        ],
        "required_authority_refs": ["AUTH-001"],
        "outcomes": [
            {
                "outcome_id": "OUT-001",
                "completion_condition_refs": ["CC-001"],
            }
        ],
        "completion_conditions": [
            {"condition_id": "CC-001", "validation_refs": ["VAL-001"]}
        ],
        "prerequisites": [],
        "dependencies": [],
        "validations": [
            {"validation_id": "VAL-001", "method_identity": "test:VAL-001"}
        ],
        "evidence": [],
        "state_contexts": [],
        "external_dependencies": [],
        "execution_boundary": {
            "write_surface": ["src/target"],
            "effect_surface": ["product-behavior"],
            "excluded_nodes": [],
            "excluded_surfaces": [],
        },
        "stop_conditions": [
            {
                "stop_condition_id": "STOP-001",
                "condition_identity": "authority-or-scope-drift",
            }
        ],
        "terminal_boundary": {
            "completion_identity": "all-declared-outcomes-truthfully-complete"
        },
    }


def schema_errors(document: dict) -> list:
    return list(Draft202012Validator(SCHEMA).iter_errors(document))


class WorkPacketControlDeclarationTests(unittest.TestCase):
    def test_control_declarations_present_is_schema_valid(self):
        self.assertEqual(schema_errors(valid_manifest()), [])

    def test_governing_authority_declaration_is_required(self):
        document = valid_manifest()
        document["authority_refs"] = []
        self.assertTrue(schema_errors(document))

    def test_required_authority_set_is_required(self):
        document = valid_manifest()
        document["required_authority_refs"] = []
        self.assertTrue(schema_errors(document))

    def test_stop_condition_is_required(self):
        document = valid_manifest()
        document["stop_conditions"] = []
        self.assertTrue(schema_errors(document))

    def test_terminal_boundary_is_required(self):
        document = valid_manifest()
        del document["terminal_boundary"]
        self.assertTrue(schema_errors(document))


if __name__ == "__main__":
    unittest.main()
