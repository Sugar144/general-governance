from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.release_payload import LEGACY_METHOD, OPERATIONAL_EXCLUDED, RELEASE_INCLUDED, ReleasePayloadError, build_projection, classify_path, content_digest, file_digest, identity_method, load_release_manifest, release_content_digest, validate_release_manifest
from tools.validate_work_packet import verify_locked_framework_identity

ROOT = Path(__file__).resolve().parents[1]
RC7_COMMIT = "22a1d5e2f759fda53574884e1056a3a56baa211a"
RC7_CONTENT_SHA256 = "14fceee7fb261fee6c2b515cbd81e39c91daaaaa3aa8dc431d3c1beac754d15e"
RC7_MANIFEST_SHA256 = "a3df71d9f46c5477389458225f08ee3ce51d552a67aeffcfa0ca25fce71d9bdd"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def scoped_manifest(content_sha256: str = "0" * 64) -> dict:
    return {
        "manifest_schema_version": "1.4.0",
        "repository": "Sugar144/general-governance",
        "framework_version": "0.1.0-rc.test",
        "release_status": "IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION",
        "compatibility": {"framework_contract": "2.0.0", "consumer_lock_schema": "2.0.0", "consumer_configuration_schema": "1.0.0"},
        "capability_composition": {"contract_version": "1.0.0", "stack_schema": "1.0.0", "optional": True},
        "work_packet_design": {"contract_version": "1.0.0", "adoption_contract_version": "1.0.0", "binding_schema_version": "1.0.0", "manifest_schema_version": "1.0.0", "optional": True},
        "content_sha256": content_sha256,
        "content_identity": {"method": "SCOPED_TRACKED_FILES_V1", "default_classification": "RELEASE_INCLUDED", "manifest_self_excluded": True, "reserved_operational_prefixes": ["governance/"], "operational_exact_paths": [".gitignore", "PROJECT_STATE.yaml", ".github/workflows/project-state-integrity.yml"]},
        "extraction_provenance": "provenance/extraction-manifest.json",
        "evolution_provenance": "provenance/evolution-manifest.json",
        "required_framework_surfaces": ["tools/release_payload.py", "contracts/release-manifest.schema.json"],
    }


class TempScopedRepo:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "tests@example.invalid")
        git(self.root, "config", "user.name", "GG Tests")
        self.write("README.md", "test\n")
        self.write("RELEASE_VERSION", "0.1.0-rc.test\n")
        self.write("tools/example.py", "VALUE = 1\n")
        self.write("contracts/example.schema.json", "{}\n")
        self.write("contracts/release-manifest.schema.json", (ROOT / "contracts/release-manifest.schema.json").read_text(encoding="utf-8"))
        self.write("governance/discovery/evidence.md", "operational\n")
        self.write("PROJECT_STATE.yaml", "status: TEST\n")
        self.write(".github/workflows/conformance-ci.yml", "name: test\non: [push]\njobs: {}\n")
        self.write("release-manifest.json", json.dumps(scoped_manifest(), indent=2) + "\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "initial")
        manifest = scoped_manifest()
        manifest["content_sha256"] = content_digest(self.root, manifest)
        self.write("release-manifest.json", json.dumps(manifest, indent=2) + "\n")
        git(self.root, "add", "release-manifest.json")
        git(self.root, "commit", "-qm", "bind scoped manifest")

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def close(self) -> None:
        self.temp.cleanup()


class ReleasePayloadIdentityTests(unittest.TestCase):
    def test_release_payload_error_preserves_consumer_and_wpdc_error_contracts(self) -> None:
        self.assertTrue(issubclass(ReleasePayloadError, ValueError))
        self.assertTrue(issubclass(ReleasePayloadError, OSError))
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(OSError):
                file_digest(Path(temp) / "missing")

    def test_current_manifest_matches_release_manifest_schema(self) -> None:
        schema = json.loads((ROOT / "contracts/release-manifest.schema.json").read_text())
        manifest = json.loads((ROOT / "release-manifest.json").read_text())
        errors = list(Draft202012Validator(schema).iter_errors(manifest))
        self.assertEqual(errors, [], [error.message for error in errors])

    def test_exact_historical_rc7_identity_is_reproduced(self) -> None:
        if not (ROOT / ".git").exists():
            self.skipTest("historical Git regression requires a Git checkout")
        subprocess.check_call(["git", "-C", str(ROOT), "cat-file", "-e", f"{RC7_COMMIT}^{{commit}}"])
        with tempfile.TemporaryDirectory() as temp:
            worktree = Path(temp) / "rc7"
            subprocess.check_call(["git", "-C", str(ROOT), "worktree", "add", "--quiet", "--detach", str(worktree), RC7_COMMIT])
            try:
                manifest = json.loads((worktree / "release-manifest.json").read_text())
                self.assertEqual(identity_method(manifest), LEGACY_METHOD)
                self.assertEqual(file_digest(worktree / "release-manifest.json"), RC7_MANIFEST_SHA256)
                self.assertEqual(release_content_digest(worktree), RC7_CONTENT_SHA256)
            finally:
                subprocess.check_call(["git", "-C", str(ROOT), "worktree", "remove", "--force", str(worktree)])

    def test_legacy_extra_tracked_file_changes_digest(self) -> None:
        repo = TempScopedRepo()
        try:
            legacy = json.loads((ROOT / "release-manifest.json").read_text())
            repo.write("release-manifest.json", json.dumps(legacy, indent=2) + "\n")
            git(repo.root, "add", "release-manifest.json")
            before = content_digest(repo.root, legacy)
            repo.write("extra-operational-looking.md", "new\n")
            git(repo.root, "add", "extra-operational-looking.md")
            after = content_digest(repo.root, legacy)
            self.assertNotEqual(before, after)
        finally:
            repo.close()

    def test_governance_file_is_operational_and_does_not_change_scoped_digest(self) -> None:
        repo = TempScopedRepo()
        try:
            manifest = load_release_manifest(repo.root)
            before = release_content_digest(repo.root)
            self.assertEqual(classify_path("governance/discovery/evidence.md", manifest), OPERATIONAL_EXCLUDED)
            repo.write("governance/learning/new.md", "new evidence\n")
            git(repo.root, "add", "governance/learning/new.md")
            self.assertEqual(release_content_digest(repo.root), before)
        finally:
            repo.close()

    def test_operational_symlink_is_excluded_without_blocking_scoped_digest(self) -> None:
        repo = TempScopedRepo()
        try:
            before = release_content_digest(repo.root)
            link = repo.root / "governance/discovery/evidence-link.md"
            link.symlink_to("evidence.md")
            git(repo.root, "add", "governance/discovery/evidence-link.md")
            self.assertTrue(git(repo.root, "ls-files", "-s", "governance/discovery/evidence-link.md").startswith("120000 "))
            self.assertEqual(release_content_digest(repo.root), before)
        finally:
            repo.close()

    def test_unknown_root_file_is_included_and_changes_scoped_digest(self) -> None:
        repo = TempScopedRepo()
        try:
            manifest = load_release_manifest(repo.root)
            before = release_content_digest(repo.root)
            self.assertEqual(classify_path("surprise.txt", manifest), RELEASE_INCLUDED)
            repo.write("surprise.txt", "surprise\n")
            git(repo.root, "add", "surprise.txt")
            self.assertNotEqual(release_content_digest(repo.root), before)
        finally:
            repo.close()

    def test_tracked_symlink_into_governance_fails_closed(self) -> None:
        repo = TempScopedRepo()
        try:
            link = repo.root / "tools/evil.py"
            link.symlink_to("../governance/discovery/evidence.md")
            git(repo.root, "add", "tools/evil.py")
            self.assertTrue(git(repo.root, "ls-files", "-s", "tools/evil.py").startswith("120000 "))
            with self.assertRaisesRegex(ReleasePayloadError, r"unsupported tracked Git mode 120000.*tools/evil.py"):
                release_content_digest(repo.root)
        finally:
            repo.close()

    def test_tracked_broken_symlink_fails_by_git_mode_before_target_lookup(self) -> None:
        repo = TempScopedRepo()
        try:
            link = repo.root / "tools/broken.py"
            link.symlink_to("../governance/does-not-exist.txt")
            git(repo.root, "add", "tools/broken.py")
            with self.assertRaisesRegex(ReleasePayloadError, r"unsupported tracked Git mode 120000.*tools/broken.py"):
                release_content_digest(repo.root)
        finally:
            repo.close()

    def test_symlinked_parent_directory_cannot_smuggle_operational_bytes(self) -> None:
        repo = TempScopedRepo()
        try:
            repo.write("governance/example.py", "SMUGGLED = True\n")
            git(repo.root, "add", "governance/example.py")
            self.assertTrue(git(repo.root, "ls-files", "-s", "tools/example.py").startswith("100644 "))
            (repo.root / "tools/example.py").unlink()
            (repo.root / "tools").rmdir()
            (repo.root / "tools").symlink_to("governance", target_is_directory=True)
            with self.assertRaisesRegex(ReleasePayloadError, r"path component must not be a symlink: .*tools"):
                release_content_digest(repo.root)
        finally:
            repo.close()

    def test_embedded_gitlink_mode_fails_closed(self) -> None:
        repo = TempScopedRepo()
        try:
            nested = repo.root / "vendor/component"
            nested.mkdir(parents=True)
            git(nested, "init", "-q")
            git(nested, "config", "user.email", "tests@example.invalid")
            git(nested, "config", "user.name", "GG Tests")
            (nested / "README.md").write_text("component\n", encoding="utf-8")
            git(nested, "add", "README.md")
            git(nested, "commit", "-qm", "nested")
            git(repo.root, "add", "vendor/component")
            self.assertTrue(git(repo.root, "ls-files", "-s", "vendor/component").startswith("160000 "))
            with self.assertRaisesRegex(ReleasePayloadError, r"unsupported tracked Git mode 160000.*vendor/component"):
                release_content_digest(repo.root)
        finally:
            repo.close()

    def test_regular_and_executable_git_modes_remain_supported(self) -> None:
        repo = TempScopedRepo()
        try:
            self.assertTrue(git(repo.root, "ls-files", "-s", "README.md").startswith("100644 "))
            repo.write("tools/executable.py", "print('ok')\n")
            git(repo.root, "add", "tools/executable.py")
            git(repo.root, "update-index", "--chmod=+x", "tools/executable.py")
            self.assertTrue(git(repo.root, "ls-files", "-s", "tools/executable.py").startswith("100755 "))
            digest = release_content_digest(repo.root)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
        finally:
            repo.close()

    def test_scoped_digest_changes_when_included_git_mode_changes(self) -> None:
        repo = TempScopedRepo()
        try:
            path = repo.root / "tools/example.py"
            before_bytes = path.read_bytes()
            self.assertTrue(git(repo.root, "ls-files", "-s", "tools/example.py").startswith("100644 "))
            before = release_content_digest(repo.root)
            git(repo.root, "update-index", "--chmod=+x", "tools/example.py")
            self.assertTrue(git(repo.root, "ls-files", "-s", "tools/example.py").startswith("100755 "))
            self.assertEqual(path.read_bytes(), before_bytes)
            after = release_content_digest(repo.root)
            self.assertNotEqual(before, after)
        finally:
            repo.close()

    def test_protected_surface_cannot_be_excluded(self) -> None:
        manifest = scoped_manifest()
        manifest["content_identity"]["operational_exact_paths"].append("tools/release_payload.py")
        with self.assertRaisesRegex(ValueError, "unsupported operational exact-path exclusion"):
            validate_release_manifest(manifest)

    def test_arbitrary_operational_prefix_is_rejected(self) -> None:
        manifest = scoped_manifest()
        manifest["content_identity"]["reserved_operational_prefixes"] = ["tools/"]
        with self.assertRaisesRegex(ValueError, "reserved_operational_prefixes"):
            validate_release_manifest(manifest)

    def test_arbitrary_glob_exclusion_is_rejected(self) -> None:
        manifest = scoped_manifest()
        manifest["content_identity"]["operational_exact_paths"].append("*.md")
        with self.assertRaisesRegex(ValueError, "unsupported operational exact-path exclusion"):
            validate_release_manifest(manifest)

    def test_unknown_manifest_method_fails_closed(self) -> None:
        manifest = scoped_manifest()
        manifest["content_identity"]["method"] = "FUTURE_UNKNOWN"
        with self.assertRaisesRegex(ValueError, "unsupported scoped release identity method"):
            validate_release_manifest(manifest)

    def test_scoped_manifest_rejects_unrecognized_top_level_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "contracts").mkdir(parents=True)
            (root / "contracts/release-manifest.schema.json").write_text((ROOT / "contracts/release-manifest.schema.json").read_text(encoding="utf-8"), encoding="utf-8")
            manifest = scoped_manifest()
            manifest["unexpected"] = "unsafe"
            (root / "release-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "schema validation failed"):
                load_release_manifest(root)

    def test_policy_change_changes_manifest_hash(self) -> None:
        first = scoped_manifest()
        second = scoped_manifest()
        second["content_identity"]["operational_exact_paths"].append("ROADMAP.md")
        first_bytes = (json.dumps(first, sort_keys=True) + "\n").encode()
        second_bytes = (json.dumps(second, sort_keys=True) + "\n").encode()
        self.assertNotEqual(hashlib.sha256(first_bytes).hexdigest(), hashlib.sha256(second_bytes).hexdigest())

    def test_consumer_lock_2_schema_shape_requires_no_new_identity_field(self) -> None:
        schema = json.loads((ROOT / "contracts/consumer-lock.schema.json").read_text())
        self.assertEqual(schema["properties"]["framework"]["required"], ["repository", "version", "commit_sha", "release_manifest_sha256"])

    def test_wpdc_uses_compatibility_wrapper_without_source_change(self) -> None:
        repo = TempScopedRepo()
        try:
            manifest_path = repo.root / "release-manifest.json"
            manifest = load_release_manifest(repo.root)
            lock = {"schema_version": "2.0.0", "framework": {"repository": "Sugar144/general-governance", "version": manifest["framework_version"], "commit_sha": git(repo.root, "rev-parse", "HEAD"), "release_manifest_sha256": file_digest(manifest_path)}, "consumer": {"configuration_path": "governance/adopter/configuration.yaml"}, "compatibility": manifest["compatibility"]}
            verify_locked_framework_identity(lock, repo.root)
        finally:
            repo.close()

    def test_build_projection_uses_scoped_method(self) -> None:
        repo = TempScopedRepo()
        try:
            with tempfile.TemporaryDirectory() as temp:
                destination = Path(temp) / "projection"
                index = build_projection(repo.root, destination)
                self.assertEqual(index["content_sha256"], load_release_manifest(repo.root)["content_sha256"])
        finally:
            repo.close()


if __name__ == "__main__":
    unittest.main()
