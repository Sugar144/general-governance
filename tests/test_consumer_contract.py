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
    return subprocess.run(["python3", str(VALIDATOR), *args], text=True, capture_output=True)


def valid_lock() -> dict:
    return {
        "schema_version": "1.0.0",
        "framework": {
            "repository": "Sugar144/general-governance",
            "version": (ROOT / "RELEASE_VERSION").read_text().strip(),
            "commit_sha": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
            "release_manifest_sha256": hashlib.sha256((ROOT / "release-manifest.json").read_bytes()).hexdigest(),
        },
        "compatibility": {"framework_contract": "1.0.0", "consumer_lock_schema": "1.0.0"},
    }


class ConsumerContractTests(unittest.TestCase):
    def write_consumer(self, lock: dict, duplicate: bool = False) -> tempfile.TemporaryDirectory[str]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "framework-lock.json").write_text(json.dumps(lock), encoding="utf-8")
        (root / "governance/project").mkdir(parents=True)
        (root / "governance/project/specialization.yaml").write_text("owner: consumer\n", encoding="utf-8")
        if duplicate:
            (root / "framework/core").mkdir(parents=True)
            (root / "framework/core/copied.md").write_text("forbidden", encoding="utf-8")
        return temp

    def test_valid_lock_and_consumer_specialization_pass(self):
        temp = self.write_consumer(valid_lock())
        self.assertEqual(run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0)

    def test_floating_ref_rejected(self):
        lock = valid_lock(); lock["framework"]["commit_sha"] = "main"
        temp = self.write_consumer(lock)
        self.assertNotEqual(run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0)

    def test_manifest_hash_mismatch_rejected(self):
        lock = valid_lock(); lock["framework"]["release_manifest_sha256"] = "0" * 64
        temp = self.write_consumer(lock)
        self.assertNotEqual(run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0)

    def test_unsupported_compatibility_rejected(self):
        lock = valid_lock(); lock["compatibility"]["framework_contract"] = "2.0.0"
        temp = self.write_consumer(lock)
        self.assertNotEqual(run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0)

    def test_framework_normative_duplication_rejected(self):
        temp = self.write_consumer(valid_lock(), duplicate=True)
        self.assertNotEqual(run("--consumer", temp.name, "--framework", str(ROOT)).returncode, 0)

    def test_explicit_upgrade_requires_distinct_immutable_identity(self):
        lock = valid_lock(); previous = json.loads(json.dumps(lock)); previous["framework"]["commit_sha"] = "a" * 40
        temp = self.write_consumer(lock)
        previous_path = Path(temp.name) / "old-lock.json"; previous_path.write_text(json.dumps(previous), encoding="utf-8")
        self.assertEqual(run("--consumer", temp.name, "--framework", str(ROOT), "--previous-lock", str(previous_path)).returncode, 0)
