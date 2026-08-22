---
prompt_id: GG-MP-0012
version: 1.0.0
mode: BOUNDED_FINDING_CORRECTION
status: APPROVED_FOR_SINGLE_EXECUTION
---

# Material prompt — executable-mode successor correction

Correct only `FIND-EXEC-BIT-001` from Claude Independent Review `GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-CORRECTION-001-IR-001`.

Preserve Git executable-mode fidelity in the isolated release-payload projection. `TrackedEntry.mode` is authoritative for included paths. Projection included records must bind `{path, sha256, mode}`. Materialize Git mode `100644` as filesystem mode `0644` and Git mode `100755` as `0755`, and make `verify_projection` fail closed on mode drift independently of byte equality.

Add regressions proving both downgrade (`0755 -> 0644`) and upgrade (`0644 -> 0755`) tampering fail, and that a projected `100755` script remains executable where the POSIX fixture supports it.

Preserve all predecessor behavior: direct/ancestor symlink hardening, gitlink rejection, operational-plane decoupling, exact rc.7 reproduction, consumer-lock 2.0.0 compatibility, WPDC source compatibility, and explicit `EXPECTED_BOOTSTRAP_FAIL_PENDING_P1` state.

Do not harden `FIND-TOCTOU-001` in this run. Do not modify any non-custody path beyond:

- `tools/release_payload.py`
- `tests/test_release_payload_identity.py`
- `tests/test_release_payload_projection.py`

Stop at an exact corrected candidate pending a fresh Claude Independent Review. No P1, PR, merge, release, publication, or adopter mutation.
