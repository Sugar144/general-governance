---
review_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-TEST-FIXTURE-CORRECTION-001-IR-001
correction_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-TEST-FIXTURE-CORRECTION-001
reviewer: CLAUDE
mode: INDEPENDENT_READ_ONLY_SEMANTIC_SECURITY_REVIEW
candidate: 201a4566bfff7c35c56ad112f203c46f19d70385
predecessor_candidate: 8da3499f08119a886df63f2267af8c2cb906146d
historical_baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
status: PREPARED_FOR_EXTERNAL_INDEPENDENT_REVIEW
---

# Claude independent review — executable-mode test fixture correction

## Independence and authority boundary

Run in a fresh Claude/Claude Code session. Review is read-only. Do not modify repository files, repair findings, commit, push, open/modify a PR, merge, package P1, tag, release, deploy, publish, or mutate adopters.

Review the exact functional candidate:

`201a4566bfff7c35c56ad112f203c46f19d70385`

Do not review later governance-only custody commits as functional content.

## Context from the predecessor review

Candidate `8da3499f08119a886df63f2267af8c2cb906146d` received `CHANGES_REQUIRED`.

The prior review independently established:

- production `FIND-EXEC-BIT-001` is CLOSED at the production-code level;
- `100644`/`100755` projection fidelity and mode-tamper detection work in an independently rebound fixture;
- prior symlink/gitlink/ancestor hardening remains intact;
- the new MATERIAL defect was `FIND-EXEC-MODE-TEST-001`: two shipped tests added `tools/run.sh` after fixture manifest binding and therefore failed on the intentionally fail-closed stale content identity before reaching their own mode assertions;
- `FIND-MANIFEST-MODE-001` and `FIND-TOCTOU-001` were MINOR and are intentionally not corrected by this successor.

Do not reinterpret those claims as evidence for this successor; verify independently.

## Authorized correction

The successor is allowed to modify only:

`tests/test_release_payload_projection.py`

The intended correction is to rebind the fixture manifest after a tracked RELEASE_INCLUDED mutation, not to weaken identity validation.

Expected diff shape:

- add a fixture-only helper that loads the fixture release manifest, recomputes `content_sha256` using `content_digest`, rewrites/stages/commits the fixture `release-manifest.json`;
- call that helper after adding/chmodding `tools/run.sh` in the two affected tests;
- no production-code changes.

## Mandatory review questions

Independently establish:

1. Does `git rev-parse HEAD` equal the exact candidate?
2. Is the predecessor-to-candidate functional diff limited to `tests/test_release_payload_projection.py` plus custody under the correction root?
3. Does the fixture helper recompute from the current Git index rather than copying/forcing a known digest?
4. Does it preserve the stale-manifest fail-closed invariant rather than bypassing `build_projection` verification?
5. Do both previously broken tests now reach their executable-mode assertions?
6. Does `test_projection_preserves_and_binds_executable_mode` prove `100755 -> 0755`, mode binding, verification, and direct POSIX execution where applicable?
7. Does `test_projection_detects_executable_mode_downgrade` prove byte-identical `0755 -> 0644` tampering is rejected by mode verification?
8. Does `test_projection_detects_non_executable_mode_upgrade` remain PASS?
9. Do prior symlink/gitlink/ancestor regressions remain PASS?
10. Does exact historical rc.7 reproduction remain PASS?
11. Does WPDC source-unchanged compatibility remain PASS?
12. Is consumer-lock 2.0.0 still sufficient?
13. Are any failures beyond the already disclosed P1 bootstrap set introduced?
14. Is `FIND-EXEC-MODE-TEST-001` genuinely closed?
15. Do the two MINOR findings remain non-blocking under the accepted threat/architecture model, without being silently treated as corrected?

## Mandatory commands

Run at minimum:

```bash
git rev-parse HEAD

git diff --stat 8da3499f08119a886df63f2267af8c2cb906146d..201a4566bfff7c35c56ad112f203c46f19d70385

git diff 8da3499f08119a886df63f2267af8c2cb906146d..201a4566bfff7c35c56ad112f203c46f19d70385 -- tests/test_release_payload_projection.py

python3 -m py_compile \
  tools/release_payload.py \
  tests/test_release_payload_identity.py \
  tests/test_release_payload_projection.py

python3 -m unittest -v \
  tests/test_release_payload_identity.py \
  tests/test_release_payload_projection.py

python3 -m unittest discover -s tests -v
```

The targeted identity/projection suite was 37 tests on the predecessor and had exactly 2 new fixture errors. A valid correction is expected to remove those two errors; do not infer PASS if the actual run differs.

For the full suite, distinguish the already documented `EXPECTED_BOOTSTRAP_FAIL_PENDING_P1` failures from any new failure introduced by this successor. Do not count expected bootstrap failures as PASS.

## Required verdict format

Your response MUST begin with exactly one of:

`PASS`
`CHANGES_REQUIRED`
`INDETERMINATE`

Then provide:

### Candidate reviewed
Exact SHA.

### Findings
For each finding: stable ID, severity (`BLOCKING`, `MATERIAL`, `MINOR`), reproducible surface, violated invariant, bounded recommendation. Do not implement it.

### Validation evidence
Commands/tests/fixtures actually run and observed results.

### FIND-EXEC-MODE-TEST-001 closure assessment
State explicitly whether both previously broken tests now reach and validate the intended mode behavior.

### Production finding preservation
State whether `FIND-EXEC-BIT-001` remains closed and prior `FIND-001` symlink hardening remains intact.

### Required invariants assessment
PASS / FAIL / INDETERMINATE individually for:

- fixture manifest rebind correctness;
- stale-manifest fail-closed preservation;
- targeted identity/projection suite;
- 100644 projection fidelity;
- 100755 projection fidelity;
- executable-mode downgrade detection;
- executable-mode upgrade detection;
- projection-index schema coherence;
- symlink/gitlink/ancestor fail-closed behavior;
- operational-plane decoupling;
- exact-commit preservation;
- legacy rc.7 reproduction;
- consumer-lock 2.0.0 sufficiency;
- WPDC source-unchanged compatibility;
- correction write-surface compliance;
- bootstrap non-integrability disclosure.

### Minor findings disposition
State whether `FIND-MANIFEST-MODE-001` and `FIND-TOCTOU-001` remain MINOR/non-blocking or whether new evidence changes their severity.

### Authority statement
Explicitly state that the review grants no correction, retry, P1 packaging, PR, merge, release, publication, deployment, or adopter authority.

A `PASS` is valid only if no BLOCKING or MATERIAL finding remains and `FIND-EXEC-MODE-TEST-001` is independently demonstrated closed.
