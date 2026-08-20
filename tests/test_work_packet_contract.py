from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "validate_work_packet.py"
CASES = json.loads((ROOT / "tests/fixtures/work-packet/cases.json").read_text())

spec = importlib.util.spec_from_file_location("validate_work_packet", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True
    ).strip()


def base_binding() -> dict:
    return {
        "schema_version": "1.0.0",
        "binding_id": "ACME-WPDC-BINDING-001",
        "capability_id": "work-packet-design-dependency-closure",
        "adoption_contract_version": "1.0.0",
        "capability_contract_version": "1.0.0",
        "adopter": {"adopter_id": "ACME", "repository": "acme/example"},
        "source_bindings": [
            {
                "source_id": "AUTH-001",
                "classes": ["AUTHORITY"],
                "locator": {
                    "kind": "REPOSITORY_PATH",
                    "value": "governance/authority.md",
                },
            },
            {
                "source_id": "ARCH-001",
                "classes": ["ARCHITECTURE"],
                "locator": {
                    "kind": "REPOSITORY_PATH",
                    "value": "docs/architecture.md",
                },
            },
            {
                "source_id": "STATE-001",
                "classes": ["STATE"],
                "locator": {
                    "kind": "STATE_OBSERVER",
                    "value": "acme-state-observer",
                },
                "currentness_rule_ref": "STATE-CURRENT",
            },
        ],
        "packet_projection": {"root": "governance/work-packets"},
        "currentness_rules": [
            {
                "rule_id": "STATE-CURRENT",
                "mode": "REFERENCE_BOUND",
                "reference": "ACME-STATE-CURRENTNESS-POLICY-001",
            }
        ],
    }


def base_manifest(canonical_sha: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "packet_id": "PACKET-001",
        "capability_contract_version": "1.0.0",
        "adoption_binding": {
            "binding_id": "ACME-WPDC-BINDING-001",
            "sha256": "0" * 64,
        },
        "canonical_base": {
            "repository": "acme/example",
            "commit_sha": canonical_sha,
        },
        "authority_refs": [
            {
                "authority_ref_id": "AUTH-REF-001",
                "identity": "governance/authority.md@sha256:" + "a" * 64,
                "source_id": "AUTH-001",
            }
        ],
        "required_authority_refs": ["AUTH-REF-001"],
        "outcomes": [
            {
                "outcome_id": "OUT-001",
                "completion_condition_refs": ["CC-001"],
            }
        ],
        "completion_conditions": [
            {"condition_id": "CC-001", "validation_refs": ["VAL-001"]}
        ],
        "prerequisites": [
            {
                "prerequisite_id": "PRE-001",
                "resolution": {"kind": "IN_PACKET"},
            }
        ],
        "dependencies": [
            {
                "dependent_ref": "OUT-001",
                "prerequisite_ref": "PRE-001",
                "relation": "REACH",
            }
        ],
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


class WorkPacketContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "evidence").mkdir()
        (self.root / "packets").mkdir()
        (self.root / "evidence/adopter.json").write_text(
            json.dumps(
                {"result": "PASS", "kind": "adopter-owned"}, sort_keys=True
            ),
            encoding="utf-8",
        )
        (self.root / "evidence/external.json").write_text(
            json.dumps({"result": "PASS", "kind": "external"}, sort_keys=True),
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.name", "WPDC Test"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "config",
                "user.email",
                "wpdc-test@example.invalid",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "add", "evidence"], check=True
        )
        subprocess.run(
            ["git", "-C", str(self.root), "commit", "-qm", "canonical base"],
            check=True,
        )
        self.canonical_sha = run_git(self.root, "rev-parse", "HEAD")
        self.configuration_path = self.root / "consumer-configuration.yaml"
        self.write_configuration()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_configuration(
        self, binding_path: str = "binding.json", *, activate_wpdc: bool = True
    ) -> None:
        configuration = {
            "correction_example": {
                "base_run_id": "RUN-001",
                "first_correction_id": "CORR-001",
            },
            "paths": {
                "formal_run_prompt_snapshots": "prompts",
                "learning_readme": "README.md",
            },
            "identity_allocator": {
                "namespace": "ACME",
                "state_path": "state.json",
                "ledger_path": "ledger.json",
            },
            "prompt_identity": {"namespace": "ACME", "sequence_width": 4},
        }
        if activate_wpdc:
            configuration["capabilities"] = {
                "work_packet_design": {"binding_path": binding_path}
            }
        self.configuration_path.write_text(
            json.dumps({"configuration": configuration}, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )

    def restore_evidence_worktree(self) -> None:
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "checkout",
                "--",
                "evidence/adopter.json",
                "evidence/external.json",
            ],
            check=True,
        )

    def write_case(self, case_id: str) -> tuple[dict, Path, dict, Path]:
        self.restore_evidence_worktree()
        self.write_configuration()
        binding = base_binding()
        manifest = base_manifest(self.canonical_sha)
        adopter_evidence = self.root / "evidence/adopter.json"
        external_evidence = self.root / "evidence/external.json"

        def adopter_evidence_record(
            source_ref: str = "ARCH-001", *, state: bool = False
        ) -> dict:
            context = (
                {
                    "kind": "STATE_EVALUATION",
                    "state_context_ref": "STATE-CTX-001",
                }
                if state
                else {
                    "kind": "CANONICAL_BASE",
                    "repository": "acme/example",
                    "commit_sha": self.canonical_sha,
                }
            )
            return {
                "evidence_id": "EVID-001",
                "path": "evidence/adopter.json",
                "sha256": digest(adopter_evidence),
                "source_scope": "ADOPTER_OWNED",
                "source_ref": source_ref,
                "context": context,
            }

        def external_dependency() -> dict:
            return {
                "external_dependency_id": "EXT-001",
                "source_identity": "external-result:EXT-001@sha256:" + "b" * 64,
                "authority_refs": ["AUTH-REF-001"],
                "currentness": {"mode": "IMMUTABLE"},
            }

        def external_evidence_record() -> dict:
            return {
                "evidence_id": "EVID-EXT-001",
                "path": "evidence/external.json",
                "sha256": digest(external_evidence),
                "source_scope": "EXTERNAL_DEPENDENCY",
                "source_ref": "EXT-001",
                "context": {
                    "kind": "EXTERNAL_DEPENDENCY",
                    "external_dependency_ref": "EXT-001",
                },
            }

        if case_id == "exact_authority_without_binding_source_closed":
            binding["source_bindings"] = [
                source
                for source in binding["source_bindings"]
                if source["source_id"] != "AUTH-001"
            ]
            binding.pop("packet_projection", None)
            manifest["authority_refs"][0].pop("source_id", None)
        elif case_id == "preexisting_immutable_closed":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            manifest["evidence"] = [adopter_evidence_record()]
        elif case_id == "preexisting_immutable_without_binding_source_closed":
            binding["source_bindings"] = [
                source
                for source in binding["source_bindings"]
                if source["source_id"] != "ARCH-001"
            ]
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            manifest["evidence"] = [
                adopter_evidence_record("DIRECT-ADOPTER-FACT-001")
            ]
        elif case_id == "canonical_worktree_drift_closed":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            manifest["evidence"] = [adopter_evidence_record()]
            adopter_evidence.write_text(
                json.dumps({"result": "CHANGED-WORKTREE"}), encoding="utf-8"
            )
        elif case_id == "preexisting_state_closed":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            manifest["state_contexts"] = [
                {
                    "state_context_id": "STATE-CTX-001",
                    "source_id": "STATE-001",
                    "target_identity": "database:journey-progress",
                    "currentness": {
                        "mode": "BINDING_RULE",
                        "rule_ref": "STATE-CURRENT",
                    },
                }
            ]
            manifest["evidence"] = [
                adopter_evidence_record("STATE-001", state=True)
            ]
        elif case_id == "preexisting_state_without_binding_source_closed":
            binding["source_bindings"] = [
                source
                for source in binding["source_bindings"]
                if source["source_id"] != "STATE-001"
            ]
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            manifest["state_contexts"] = [
                {
                    "state_context_id": "STATE-CTX-001",
                    "source_id": "DIRECT-STATE-001",
                    "target_identity": "database:journey-progress",
                    "currentness": {
                        "mode": "EXACT_REFERENCE",
                        "reference": "observation:STATE-001@sequence:42",
                    },
                }
            ]
            manifest["evidence"] = [
                adopter_evidence_record("DIRECT-STATE-001", state=True)
            ]
        elif case_id == "external_satisfied_closed":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "BOUND_EXTERNAL_SATISFIED",
                "external_dependency_ref": "EXT-001",
                "evidence_refs": ["EVID-EXT-001"],
            }
            manifest["external_dependencies"] = [external_dependency()]
            manifest["evidence"] = [external_evidence_record()]
        elif case_id == "unresolved_blocked":
            manifest["prerequisites"][0]["resolution"] = {"kind": "UNRESOLVED"}
        elif case_id == "unresolved_excluded_invalid":
            manifest["prerequisites"][0]["resolution"] = {"kind": "UNRESOLVED"}
            manifest["execution_boundary"]["excluded_nodes"] = ["PRE-001"]
        elif case_id == "in_packet_excluded_invalid":
            manifest["execution_boundary"]["excluded_nodes"] = ["PRE-001"]
        elif case_id == "transitive_unresolved_blocked":
            manifest["prerequisites"].append(
                {
                    "prerequisite_id": "PRE-002",
                    "resolution": {"kind": "UNRESOLVED"},
                }
            )
            manifest["dependencies"].append(
                {
                    "dependent_ref": "PRE-001",
                    "prerequisite_ref": "PRE-002",
                    "relation": "COMPLETE",
                }
            )
        elif case_id == "unresolved_reference_invalid":
            manifest["dependencies"][0]["prerequisite_ref"] = "PRE-MISSING"
        elif case_id == "dependency_cycle_invalid":
            manifest["prerequisites"].append(
                {
                    "prerequisite_id": "PRE-002",
                    "resolution": {"kind": "IN_PACKET"},
                }
            )
            manifest["dependencies"].extend(
                [
                    {
                        "dependent_ref": "PRE-001",
                        "prerequisite_ref": "PRE-002",
                        "relation": "COMPLETE",
                    },
                    {
                        "dependent_ref": "PRE-002",
                        "prerequisite_ref": "PRE-001",
                        "relation": "COMPLETE",
                    },
                ]
            )
        elif case_id == "missing_validation_coverage_invalid":
            manifest["completion_conditions"][0]["validation_refs"] = []
        elif case_id == "external_misclassified_preexisting_invalid":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-EXT-001"],
            }
            manifest["external_dependencies"] = [external_dependency()]
            manifest["evidence"] = [external_evidence_record()]
        elif case_id == "external_identity_misclassified_preexisting_invalid":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            manifest["external_dependencies"] = [external_dependency()]
            manifest["evidence"] = [adopter_evidence_record("EXT-001")]
        elif case_id == "evidence_digest_mismatch_invalid":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            record = adopter_evidence_record()
            record["sha256"] = "0" * 64
            manifest["evidence"] = [record]
        elif case_id == "binding_digest_mismatch_invalid":
            pass
        elif case_id == "canonical_repository_mismatch_invalid":
            manifest["canonical_base"]["repository"] = "other/example"
        elif case_id == "canonical_commit_missing_invalid":
            manifest["canonical_base"]["commit_sha"] = "f" * 40
        elif case_id == "missing_binding_currentness_rule_invalid":
            binding["source_bindings"][2]["currentness_rule_ref"] = "MISSING-RULE"
        elif case_id == "canonical_evidence_mismatch_invalid":
            manifest["prerequisites"][0]["resolution"] = {
                "kind": "PREEXISTING_SATISFIED",
                "evidence_refs": ["EVID-001"],
            }
            record = adopter_evidence_record()
            record["context"]["commit_sha"] = "2" * 40
            manifest["evidence"] = [record]
        elif case_id == "authority_source_class_mismatch_invalid":
            manifest["authority_refs"][0]["source_id"] = "ARCH-001"
        elif case_id != "in_packet_closed":
            raise AssertionError(f"unknown fixture case {case_id}")

        binding_path = self.root / "binding.json"
        binding_path.write_text(
            json.dumps(binding, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if case_id != "binding_digest_mismatch_invalid":
            manifest["adoption_binding"]["sha256"] = digest(binding_path)
        # Manifest custody is deliberately separate from evidence custody.
        manifest_path = self.root / "packets/manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return manifest, manifest_path, binding, binding_path

    def run_cli(self, manifest_path: Path, binding_path: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                "python3",
                str(VALIDATOR_PATH),
                "--manifest",
                str(manifest_path),
                "--binding",
                str(binding_path),
                "--configuration",
                str(self.configuration_path),
                "--repository-root",
                str(self.root),
            ],
            text=True,
            capture_output=True,
        )

    def rewrite_case_documents(
        self,
        manifest: dict,
        manifest_path: Path,
        binding: dict,
        binding_path: Path,
    ) -> None:
        binding_path.write_text(
            json.dumps(binding, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        manifest["adoption_binding"]["sha256"] = digest(binding_path)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def test_schemas_are_draft_2020_12_valid(self):
        for path in (
            ROOT / "contracts/work-packet-capability-binding.schema.json",
            ROOT / "contracts/work-packet-manifest.schema.json",
        ):
            Draft202012Validator.check_schema(json.loads(path.read_text()))

    def test_generic_regression_catalog(self):
        for case in CASES:
            with self.subTest(case=case["case_id"]):
                manifest, manifest_path, binding, binding_path = self.write_case(
                    case["case_id"]
                )
                if case["expected"] == "PACKET_INVALID":
                    with self.assertRaises(validator.ValidationFailure) as caught:
                        validator.evaluate(
                            manifest,
                            manifest_path,
                            binding,
                            binding_path,
                            self.root,
                        )
                    self.assertEqual(caught.exception.code, case["code"])
                else:
                    result = validator.evaluate(
                        manifest,
                        manifest_path,
                        binding,
                        binding_path,
                        self.root,
                    )
                    self.assertEqual(result.disposition, case["expected"])

    def test_cli_blocked_is_valid_but_not_closed(self):
        _, manifest_path, _, binding_path = self.write_case("unresolved_blocked")
        result = self.run_cli(manifest_path, binding_path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALID_BUT_BLOCKED", result.stdout)
        self.assertIn("no execution authority is implied", result.stdout)

    def test_cli_invalid_fails_closed(self):
        _, manifest_path, _, binding_path = self.write_case(
            "in_packet_excluded_invalid"
        )
        result = self.run_cli(manifest_path, binding_path)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "PACKET_INVALID: EXCLUDED_REQUIRED_PREREQUISITE", result.stdout
        )

    def test_cli_without_discovery_key_reports_wpdc_absent(self):
        _, manifest_path, _, binding_path = self.write_case("in_packet_closed")
        self.write_configuration(activate_wpdc=False)
        result = self.run_cli(manifest_path, binding_path)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("WPDC_ABSENT", result.stdout)
        self.assertNotIn("VALID_DEPENDENCY_CLOSED", result.stdout)
        self.assertNotIn("VALID_BUT_BLOCKED", result.stdout)

    def test_cli_rejects_binding_not_selected_by_configuration(self):
        _, manifest_path, _, binding_path = self.write_case("in_packet_closed")
        other_binding = self.root / "other-binding.json"
        other_binding.write_bytes(binding_path.read_bytes())
        result = self.run_cli(manifest_path, other_binding)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("PACKET_INVALID: INVALID_ADOPTION_BINDING", result.stdout)
        self.assertIn("not the binding selected", result.stdout)

    def test_cli_rejects_missing_configured_binding(self):
        _, manifest_path, _, binding_path = self.write_case("in_packet_closed")
        self.write_configuration(binding_path="missing-binding.json")
        result = self.run_cli(manifest_path, binding_path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("PACKET_INVALID: INVALID_ADOPTION_BINDING", result.stdout)
        self.assertIn("configured WPDC binding does not exist", result.stdout)

    def test_state_binding_rule_must_match_mapped_source_rule(self):
        manifest, manifest_path, binding, binding_path = self.write_case(
            "preexisting_state_closed"
        )
        binding["currentness_rules"].append(
            {
                "rule_id": "OTHER-CURRENTNESS",
                "mode": "REFERENCE_BOUND",
                "reference": "ACME-OTHER-CURRENTNESS-POLICY-001",
            }
        )
        manifest["state_contexts"][0]["currentness"] = {
            "mode": "BINDING_RULE",
            "rule_ref": "OTHER-CURRENTNESS",
        }
        self.rewrite_case_documents(
            manifest, manifest_path, binding, binding_path
        )
        with self.assertRaises(validator.ValidationFailure) as caught:
            validator.evaluate(
                manifest, manifest_path, binding, binding_path, self.root
            )
        self.assertEqual(caught.exception.code, "INVALID_ADOPTION_BINDING")
        self.assertIn("does not match source", caught.exception.message)

    def test_unmapped_state_source_cannot_use_binding_rule(self):
        manifest, manifest_path, binding, binding_path = self.write_case(
            "preexisting_state_without_binding_source_closed"
        )
        manifest["state_contexts"][0]["currentness"] = {
            "mode": "BINDING_RULE",
            "rule_ref": "STATE-CURRENT",
        }
        self.rewrite_case_documents(
            manifest, manifest_path, binding, binding_path
        )
        with self.assertRaises(validator.ValidationFailure) as caught:
            validator.evaluate(
                manifest, manifest_path, binding, binding_path, self.root
            )
        self.assertEqual(caught.exception.code, "INVALID_ADOPTION_BINDING")
        self.assertIn("cannot use BINDING_RULE", caught.exception.message)


if __name__ == "__main__":
    unittest.main()
