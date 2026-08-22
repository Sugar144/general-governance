from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.release_payload import PROJECTION_INDEX, ReleasePayloadError, build_projection, content_digest, load_release_manifest, verify_projection
from tools.validate_capability_stack import component_set_sha256, validate_stack

ROOT = Path(__file__).resolve().parents[1]


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def manifest_template(content_sha256: str = "0" * 64) -> dict:
    return {
        "manifest_schema_version": "1.4.0",
        "repository": "Sugar144/general-governance",
        "framework_version": "0.1.0-rc.test",
        "release_status": "IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION",
        "compatibility": {"framework_contract": "2.0.0", "consumer_lock_schema": "2.0.0", "consumer_configuration_schema": "1.0.0"},
        "capability_composition": {"contract_version": "1.0.0", "stack_schema": "1.0.0", "optional": True},
        "work_packet_design": {"contract_version": "1.0.0", "adoption_contract_version": "1.0.0", "binding_schema_version": "1.0.0", "manifest_schema_version": "1.0.0", "optional": True},
        "content_sha256": content_sha256,
        "content_identity": {"method": "SCOPED_TRACKED_FILES_V1", "default_classification": "RELEASE_INCLUDED", "manifest_self_excluded": True, "reserved_operational_prefixes": ["governance/"], "operational_exact_paths": ["PROJECT_STATE.yaml"]},
        "extraction_provenance": "provenance/extraction-manifest.json",
        "evolution_provenance": "provenance/evolution-manifest.json",
        "required_framework_surfaces": ["tools/release_payload.py"],
    }


class ProjectionRepo:
    def __init__(self, hidden_dependency: bool = False) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "tests@example.invalid")
        git(self.root, "config", "user.name", "GG Tests")
        self.write("README.md", "projection test\n")
        self.write("RELEASE_VERSION", "0.1.0-rc.test\n")
        self.write("contracts/release-manifest.schema.json", (ROOT / "contracts/release-manifest.schema.json").read_text(encoding="utf-8"))
        if hidden_dependency:
            self.write("tools/check.py", "from pathlib import Path\nprint(Path('governance/secret.txt').read_text())\n")
            self.write("governance/secret.txt", "secret\n")
        else:
            self.write("tools/check.py", "print('ok')\n")
            self.write("governance/evidence.md", "evidence\n")
        self.write("PROJECT_STATE.yaml", "status: TEST\n")
        self.write(".github/workflows/conformance-ci.yml", "name: test\non: [push]\njobs: {}\n")
        self.write("release-manifest.json", json.dumps(manifest_template(), indent=2) + "\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "initial")
        manifest = manifest_template()
        manifest["content_sha256"] = content_digest(self.root, manifest)
        self.write("release-manifest.json", json.dumps(manifest, indent=2) + "\n")
        git(self.root, "add", "release-manifest.json")
        git(self.root, "commit", "-qm", "bind manifest")

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def close(self) -> None:
        self.temp.cleanup()


class ReleasePayloadProjectionTests(unittest.TestCase):
    def test_projection_excludes_operational_files_and_git(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                index = build_projection(repo.root, projection)
                self.assertFalse((projection / ".git").exists())
                self.assertFalse((projection / "governance/evidence.md").exists())
                self.assertFalse((projection / "PROJECT_STATE.yaml").exists())
                self.assertTrue((projection / "tools/check.py").is_file())
                self.assertTrue((projection / "release-manifest.json").is_file())
                self.assertTrue((projection / PROJECTION_INDEX).is_file())
                verify_projection(projection, index)
        finally:
            repo.close()

    def test_projection_rejects_tracked_symlink_before_target_bytes_are_copied(self) -> None:
        repo = ProjectionRepo()
        try:
            link = repo.root / "tools/evil.py"
            link.symlink_to("../governance/evidence.md")
            git(repo.root, "add", "tools/evil.py")
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                with self.assertRaisesRegex(ReleasePayloadError, r"unsupported tracked Git mode 120000.*tools/evil.py"):
                    build_projection(repo.root, projection)
                self.assertFalse(projection.exists())
        finally:
            repo.close()

    def test_projection_missing_included_file_fails(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                index = build_projection(repo.root, projection)
                (projection / "tools/check.py").unlink()
                with self.assertRaises(ValueError):
                    verify_projection(projection, index)
        finally:
            repo.close()

    def test_projection_included_file_replaced_by_symlink_fails(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                projection = root / "projection"
                index = build_projection(repo.root, projection)
                included = projection / "tools/check.py"
                same_bytes_outside_projection = root / "outside-check.py"
                same_bytes_outside_projection.write_bytes(included.read_bytes())
                included.unlink()
                included.symlink_to(same_bytes_outside_projection)
                with self.assertRaisesRegex(ValueError, "must not be a symlink"):
                    verify_projection(projection, index)
        finally:
            repo.close()

    def test_projection_injected_excluded_file_fails(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                index = build_projection(repo.root, projection)
                injected = projection / "governance/evidence.md"
                injected.parent.mkdir(parents=True)
                injected.write_text("injected\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "operationally excluded"):
                    verify_projection(projection, index)
        finally:
            repo.close()

    def test_projection_injected_broken_symlink_at_excluded_path_fails(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                index = build_projection(repo.root, projection)
                injected = projection / "governance/evidence.md"
                injected.parent.mkdir(parents=True)
                injected.symlink_to("missing-target")
                with self.assertRaisesRegex(ValueError, "operationally excluded"):
                    verify_projection(projection, index)
        finally:
            repo.close()

    def test_projection_undeclared_extra_file_fails(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                index = build_projection(repo.root, projection)
                (projection / "extra.txt").write_text("extra\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "file-set mismatch"):
                    verify_projection(projection, index)
        finally:
            repo.close()

    def test_projection_detects_hidden_dependency_by_execution(self) -> None:
        repo = ProjectionRepo(hidden_dependency=True)
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                build_projection(repo.root, projection)
                result = subprocess.run(["python3", "tools/check.py"], cwd=projection, text=True, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("governance/secret.txt", result.stderr)
        finally:
            repo.close()

    def test_projection_index_matches_manifest_content_identity(self) -> None:
        repo = ProjectionRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                projection = Path(temp) / "projection"
                index = build_projection(repo.root, projection)
                manifest = load_release_manifest(projection)
                self.assertEqual(index["content_sha256"], manifest["content_sha256"])
        finally:
            repo.close()

    def test_capability_stack_validation_is_projection_safe(self) -> None:
        components = [
            {
                "component_id": "GG",
                "role": "GOVERNANCE_FRAMEWORK",
                "repository": "Sugar144/general-governance",
                "commit_sha": "1" * 40,
                "governance_authority": "OWN_DOMAIN_ONLY",
            }
        ]
        document = {
            "schema_version": "1.0.0",
            "stack_id": "PROJECTION-SAFE",
            "component_set_sha256": component_set_sha256(components),
            "status": "PREPARED",
            "components": components,
            "compatibility_evidence": [],
        }
        with tempfile.TemporaryDirectory() as temp:
            stack_path = Path(temp) / "capability-stack.json"
            stack_path.write_text(json.dumps(document), encoding="utf-8")
            validate_stack(document, stack_path)


if __name__ == "__main__":
    unittest.main()
