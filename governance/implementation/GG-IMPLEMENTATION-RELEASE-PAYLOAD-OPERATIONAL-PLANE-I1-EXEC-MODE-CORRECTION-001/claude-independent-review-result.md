# Claude Independent Review Result

Review ID: `GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-EXEC-MODE-CORRECTION-001-IR-001`

Candidate reviewed: `8da3499f08119a886df63f2267af8c2cb906146d`

Verdict: `CHANGES_REQUIRED`

## Findings

### FIND-EXEC-MODE-TEST-001 — MATERIAL

The production correction closes executable-mode fidelity, but two shipped tests intended to prove `100755` behavior are invalid fixtures:

- `tests/test_release_payload_projection.py::test_projection_preserves_and_binds_executable_mode`
- `tests/test_release_payload_projection.py::test_projection_detects_executable_mode_downgrade`

Both add `tools/run.sh` as a new `RELEASE_INCLUDED` tracked path after the fixture manifest has already bound its `content_sha256`, then invoke `build_projection()` without rebinding the manifest. `build_projection()` correctly fails closed because the manifest content identity is stale, before either mode assertion is reached.

Reviewer reproduction:

`python3 -m unittest -v tests/test_release_payload_projection.py` -> both tests ERROR with `ReleasePayloadError: projection content digest does not reproduce manifest content identity`.

Bounded recommendation: after adding `tools/run.sh`, recompute the scoped content digest, rewrite `release-manifest.json`, stage and commit it in the temporary fixture before building the projection.

This is a defect in shipped validation evidence, not in production executable-mode logic.

### FIND-MANIFEST-MODE-001 — MINOR

`build_projection()` materializes the release manifest using its Git mode, but `verify_projection()` re-verifies only the manifest byte hash, not its mode. This is an asymmetry, but the reviewer classified it MINOR because `release-manifest.json` is schema-validated JSON, `MANIFEST_SELF_EXCLUDED`, not executable, and its bytes remain independently bound.

Bounded recommendation: either verify manifest mode too or explicitly document why manifest mode is intentionally outside post-build mode fidelity.

## Production-code closure

`FIND-EXEC-BIT-001` is CLOSED at the production-code level.

Independent adversarial fixture with a correctly rebound manifest demonstrated:

- `100755` projects as executable and can be directly invoked on POSIX;
- `100644` projects as non-executable;
- `0755 -> 0644` tampering is rejected;
- `0644 -> 0755` tampering is rejected;
- invalid included modes are rejected;
- missing `mode` index key is rejected;
- projection-index schema `1.1.0` is enforced and stale `1.0.0` rejected.

Prior symlink-smuggling hardening remains intact.

## Validation evidence summary

- exact candidate SHA confirmed before and after review;
- `py_compile`: PASS;
- targeted identity + projection suite: 37 tests, 35 PASS, 2 ERROR from `FIND-EXEC-MODE-TEST-001`;
- full suite: 77 tests, 10 failures + 3 errors; 11 remain the known `EXPECTED_BOOTSTRAP_FAIL_PENDING_P1` set, 2 are the new fixture errors;
- independent adversarial executable-mode fixture: 12/12 PASS;
- projection-index stale-version search: no stale live `1.0.0` references;
- exact-commit, legacy rc.7, consumer-lock 2.0.0, WPDC compatibility, symlink/gitlink/ancestor defenses, operational-plane decoupling and correction write-surface: PASS.

## Required invariants

PASS:
- 100644 projection fidelity;
- 100755 production projection fidelity;
- projection index mode binding;
- executable-mode downgrade detection;
- executable-mode upgrade detection;
- projection-index schema coherence;
- projection-index trust-chain consistency under the accepted colocated Gate B model;
- included symlink fail-closed;
- gitlink fail-closed;
- ancestor symlink fail-closed;
- operational-plane decoupling;
- exact-commit preservation;
- legacy rc.7 reproduction;
- consumer-lock 2.0.0 sufficiency;
- WPDC source-unchanged compatibility;
- correction write-surface compliance;
- bootstrap non-integrability disclosure.

CHANGES_REQUIRED because the shipped tests that are supposed to constitute closure evidence for the central executable-mode behavior are invalid and error before reaching their assertions.

## Authority

This review grants no correction, retry, P1 packaging, PR, merge, release, publication, deployment, or adopter authority.
