from __future__ import annotations

import unittest

from tests import test_work_packet_contract as contract_cases


class WorkPacketEvidenceContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = contract_cases.WorkPacketContractTests(
            methodName="test_schemas_are_draft_2020_12_valid"
        )
        self.helper.setUp()

    def tearDown(self) -> None:
        self.helper.tearDown()

    def evaluate_case(self, manifest, manifest_path, binding, binding_path):
        return contract_cases.validator.evaluate(
            manifest,
            manifest_path,
            binding,
            binding_path,
            self.helper.root,
        )

    def test_unused_evidence_rejects_dangling_state_context(self):
        manifest, manifest_path, binding, binding_path = self.helper.write_case(
            "in_packet_closed"
        )
        evidence_path = self.helper.root / "evidence/adopter.json"
        manifest["evidence"] = [
            {
                "evidence_id": "EVID-UNUSED-STATE",
                "path": "evidence/adopter.json",
                "sha256": contract_cases.digest(evidence_path),
                "source_scope": "ADOPTER_OWNED",
                "source_ref": "DIRECT-STATE-001",
                "context": {
                    "kind": "STATE_EVALUATION",
                    "state_context_ref": "STATE-CTX-MISSING",
                },
            }
        ]
        with self.assertRaises(contract_cases.validator.ValidationFailure) as caught:
            self.evaluate_case(manifest, manifest_path, binding, binding_path)
        self.assertEqual(caught.exception.code, "UNRESOLVED_REFERENCE")
        self.assertIn("unknown state context", caught.exception.message)

    def test_unused_evidence_rejects_dangling_external_dependency(self):
        manifest, manifest_path, binding, binding_path = self.helper.write_case(
            "in_packet_closed"
        )
        evidence_path = self.helper.root / "evidence/external.json"
        manifest["evidence"] = [
            {
                "evidence_id": "EVID-UNUSED-EXTERNAL",
                "path": "evidence/external.json",
                "sha256": contract_cases.digest(evidence_path),
                "source_scope": "EXTERNAL_DEPENDENCY",
                "source_ref": "EXT-MISSING",
                "context": {
                    "kind": "EXTERNAL_DEPENDENCY",
                    "external_dependency_ref": "EXT-MISSING",
                },
            }
        ]
        with self.assertRaises(contract_cases.validator.ValidationFailure) as caught:
            self.evaluate_case(manifest, manifest_path, binding, binding_path)
        self.assertEqual(caught.exception.code, "UNRESOLVED_REFERENCE")
        self.assertIn("unknown external dependency", caught.exception.message)

    def test_unused_state_evidence_rejects_source_context_mismatch(self):
        manifest, manifest_path, binding, binding_path = self.helper.write_case(
            "in_packet_closed"
        )
        evidence_path = self.helper.root / "evidence/adopter.json"
        manifest["state_contexts"] = [
            {
                "state_context_id": "STATE-CTX-UNUSED",
                "source_id": "DIRECT-STATE-A",
                "target_identity": "database:unused-state",
                "currentness": {
                    "mode": "EXACT_REFERENCE",
                    "reference": "observation:unused-state@sequence:7",
                },
            }
        ]
        manifest["evidence"] = [
            {
                "evidence_id": "EVID-UNUSED-STATE-MISMATCH",
                "path": "evidence/adopter.json",
                "sha256": contract_cases.digest(evidence_path),
                "source_scope": "ADOPTER_OWNED",
                "source_ref": "DIRECT-STATE-B",
                "context": {
                    "kind": "STATE_EVALUATION",
                    "state_context_ref": "STATE-CTX-UNUSED",
                },
            }
        ]
        with self.assertRaises(contract_cases.validator.ValidationFailure) as caught:
            self.evaluate_case(manifest, manifest_path, binding, binding_path)
        self.assertEqual(caught.exception.code, "INVALID_RESOLUTION_EVIDENCE")
        self.assertIn("source differs from its state context source", caught.exception.message)

    def test_unused_evidence_rejects_external_source_as_adopter_owned(self):
        manifest, manifest_path, binding, binding_path = self.helper.write_case(
            "in_packet_closed"
        )
        evidence_path = self.helper.root / "evidence/adopter.json"
        manifest["external_dependencies"] = [
            {
                "external_dependency_id": "EXT-UNUSED",
                "source_identity": "external-result:EXT-UNUSED@sha256:" + "b" * 64,
                "authority_refs": ["AUTH-REF-001"],
                "currentness": {"mode": "IMMUTABLE"},
            }
        ]
        manifest["evidence"] = [
            {
                "evidence_id": "EVID-UNUSED-MISCLASSIFIED",
                "path": "evidence/adopter.json",
                "sha256": contract_cases.digest(evidence_path),
                "source_scope": "ADOPTER_OWNED",
                "source_ref": "EXT-UNUSED",
                "context": {
                    "kind": "CANONICAL_BASE",
                    "repository": "acme/example",
                    "commit_sha": self.helper.canonical_sha,
                },
            }
        ]
        with self.assertRaises(contract_cases.validator.ValidationFailure) as caught:
            self.evaluate_case(manifest, manifest_path, binding, binding_path)
        self.assertEqual(caught.exception.code, "INVALID_RESOLUTION_EVIDENCE")
        self.assertIn("separately declared external dependency", caught.exception.message)


if __name__ == "__main__":
    unittest.main()
