from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_consumer.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(VALIDATOR), *args], text=True, capture_output=True
    )


def valid_lock(configuration_path: str = "governance/adopter/configuration.yaml") -> dict:
    return {
        "schema_version": "2.0.0",
        "framework": {
            "repository": "Sugar144/general-governance",
            "version": (ROOT / "RELEASE_VERSION").read_text().strip(),
            "commit_sha": subprocess.check_output(
                ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
            ).strip(),
            "release_manifest_sha256": hashlib.sha256(
                (ROOT / "release-manifest.json").read_bytes()
            ).hexdigest(),
        },
        "consumer": {"configuration_path": configuration_path},
        "compatibility": {
            "framework_contract": "2.0.0",
            "consumer_lock_schema": "2.0.0",
            "consumer_configuration_schema": "1.0.0",
        },
    }


def legacy_v1_lock() -> dict:
    return {
        "schema_version": "1.0.0",
        "framework": {
            "repository": "Sugar144/general-governance",
            "version": "0.1.0-rc.1",
            "commit_sha": "d2f84cdb933f0738003d6de9696f44226c734065",
            "release_manifest_sha256": "4ff7871bae53502134d2b2f20be8c1a954a75874bf0103ff66634a010e556f9f",
        },
        "compatibility": {
            "framework_contract": "1.0.0",
            "consumer_lock_schema": "1.0.0",
        },
    }


def config_text(
    *,
    prompt_namespace: str = "ACME-PROMPT",
    prompt_width: str = "3",
    omit: str | None = None,
    unresolved: bool = False,
) -> str:
    values = {
        "base_run_id": "RUN-006",
        "first_correction_id": "RUN-006-R1",
        "formal_run_prompt_snapshots": "governance/runs/<run>/prompt/",
        "learning_readme": "governance/learning/README.md",
        "allocator_namespace": "acme.learning",
        "state_path": "governance/identity/state.json",
        "ledger_path": "governance/identity/ledger.jsonl",
        "prompt_namespace": prompt_namespace,
        "prompt_width": prompt_width,
    }
    if unresolved:
        values["learning_readme"] = "{{configuration.paths.learning_readme}}"

    lines = [
        "document_id: ACME-GOV-CONFIG-001",
        "version: 1.0.0",
        "status: ACTIVE_PROJECT_OWNED_CONFIGURATION",
        "configuration:",
        "  correction_example:",
    ]
    if omit != "base_run_id":
        lines.append(f"    base_run_id: {values['base_run_id']}")
    if omit != "first_correction_id":
        lines.append(f"    first_correction_id: {values['first_correction_id']}")
    lines += ["  paths:"]
    if omit != "formal_run_prompt_snapshots":
        lines.append(
            f"    formal_run_prompt_snapshots: {values['formal_run_prompt_snapshots']}"
        )
    if omit != "learning_readme":
        lines.append(f"    learning_readme: {values['learning_readme']}")
    lines += ["  identity_allocator:"]
    if omit != "allocator_namespace":
        lines.append(f"    namespace: {values['allocator_namespace']}")
    if omit != "state_path":
        lines.append(f"    state_path: {values['state_path']}")
    if omit != "ledger_path":
        lines.append(f"    ledger_path: {values['ledger_path']}")
    lines += ["  prompt_identity:"]
    if omit != "prompt_namespace":
        lines.append(f"    namespace: {values['prompt_namespace']}")
    if omit != "prompt_width":
        lines.append(f"    sequence_width: {values['prompt_width']}")
    return "\n".join(lines) + "\n"


class ConsumerContractTests(unittest.TestCase):
    def write_consumer(
        self,
        lock: dict,
        *,
        config: str | None = None,
        duplicate: bool = False,
    ) -> tempfile.TemporaryDirectory[str]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "framework-lock.json").write_text(json.dumps(lock), encoding="utf-8")
        (root / "governance/project").mkdir(parents=True)
        (root / "governance/project/specialization.yaml").write_text(
            "owner: consumer\n", encoding="utf-8"
        )
        if config is not None:
            config_path = root / lock["consumer"]["configuration_path"]
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(config, encoding="utf-8")
        if duplicate:
            (root / "framework/core").mkdir(parents=True)
            (root / "framework/core/copied.md").write_text(
                "forbidden", encoding="utf-8"
            )
        return temp

    def test_valid_independent_consumer_configuration_passes(self):
        lock = valid_lock()
        temp = self.write_consumer(lock, config=config_text())
        result = run("--consumer", temp.name, "--framework", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_project_specific_prompt_namespace_passes_without_core_change(self):
        lock = valid_lock()
        temp = self.write_consumer(
            lock, config=config_text(prompt_namespace="DOPIS-PROMPT", prompt_width="4")
        )
        result = run("--consumer", temp.name, "--framework", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        core = (ROOT / "framework/core/project-operating-contract.md").read_text()
        self.assertNotIn("HP-PROMPT-###", core)
        self.assertIn("configuration.prompt_identity.namespace", core)

    def test_missing_required_configuration_file_fails(self):
        temp = self.write_consumer(valid_lock(), config=None)
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_missing_required_configuration_key_fails(self):
        lock = valid_lock()
        temp = self.write_consumer(lock, config=config_text(omit="prompt_namespace"))
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_unresolved_placeholder_configuration_fails(self):
        lock = valid_lock()
        temp = self.write_consumer(lock, config=config_text(unresolved=True))
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_incompatible_configuration_contract_fails(self):
        lock = valid_lock()
        lock["compatibility"]["consumer_configuration_schema"] = "9.0.0"
        temp = self.write_consumer(lock, config=config_text())
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_invalid_prompt_identity_configuration_fails(self):
        lock = valid_lock()
        temp = self.write_consumer(
            lock, config=config_text(prompt_namespace="bad namespace")
        )
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_machine_configuration_schema_rejects_wrong_type(self):
        lock = valid_lock()
        temp = self.write_consumer(
            lock, config=config_text(prompt_width='"3"')
        )
        result = run("--consumer", temp.name, "--framework", str(ROOT))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema validation failed", result.stderr)

    def test_floating_ref_rejected(self):
        lock = valid_lock()
        lock["framework"]["commit_sha"] = "main"
        temp = self.write_consumer(lock, config=config_text())
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_manifest_hash_mismatch_rejected(self):
        lock = valid_lock()
        lock["framework"]["release_manifest_sha256"] = "0" * 64
        temp = self.write_consumer(lock, config=config_text())
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_framework_normative_duplication_rejected(self):
        lock = valid_lock()
        temp = self.write_consumer(lock, config=config_text(), duplicate=True)
        self.assertNotEqual(
            run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0
        )

    def test_controlled_upgrade_accepts_legacy_v1_previous_lock(self):
        lock = valid_lock()
        temp = self.write_consumer(lock, config=config_text())
        previous_path = Path(temp.name) / "old-lock.json"
        previous_path.write_text(json.dumps(legacy_v1_lock()), encoding="utf-8")
        result = run(
            "--consumer",
            temp.name,
            "--framework",
            str(ROOT),
            "--previous-lock",
            str(previous_path),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_noop_v2_upgrade_rejected(self):
        lock = valid_lock()
        temp = self.write_consumer(lock, config=config_text())
        previous_path = Path(temp.name) / "old-lock.json"
        previous_path.write_text(json.dumps(lock), encoding="utf-8")
        self.assertNotEqual(
            run(
                "--consumer",
                temp.name,
                "--framework",
                str(ROOT),
                "--previous-lock",
                str(previous_path),
            ).returncode,
            0,
        )


if __name__ == "__main__":
    unittest.main()
