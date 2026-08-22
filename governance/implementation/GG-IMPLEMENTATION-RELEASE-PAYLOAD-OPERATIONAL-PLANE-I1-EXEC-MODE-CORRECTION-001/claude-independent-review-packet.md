---
review_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-EXEC-MODE-CORRECTION-001-IR-001
correction_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-EXEC-MODE-CORRECTION-001
reviewer: CLAUDE
mode: INDEPENDENT_READ_ONLY_SEMANTIC_SECURITY_REVIEW
candidate: 8da3499f08119a886df63f2267af8c2cb906146d
predecessor_candidate: 2567fbd67e7fff50383d347913cf6442fbdebc61
historical_baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
status: PREPARED_FOR_EXTERNAL_INDEPENDENT_REVIEW
---

# Claude independent review — executable-mode successor correction

## Independence boundary

Review the exact functional candidate `8da3499f08119a886df63f2267af8c2cb906146d` in a fresh Claude Code session. Do not review later governance-only custody commits as implementation content.

Read-only review only. Do not modify tracked files, commit, push, open/modify a PR, merge, tag, release, deploy, publish, or repair findings. Temporary external fixtures are allowed.

## Trigger

The predecessor candidate `2567fbd67e7fff50383d347913cf6442fbdebc61` closed the prior symlink-smuggling finding, but Claude IR found:

`FIND-EXEC-BIT-001 — MATERIAL`

A Git `100755` included file projected as filesystem `0644`; `build_projection` and `verify_projection` still passed.

Previous Claude review also recorded `FIND-TOCTOU-001 — MINOR`. That threat-model hardening is explicitly out of scope for this correction unless you determine the new correction materially worsens it.

## Intended correction

The candidate should:

1. keep `content_sha256` byte/path encoding unchanged;
2. keep exact Git commit as the authority that binds Git entry mode;
3. advance the temporary projection-index schema from `1.0.0` to `1.1.0` because included record shape changes;
4. bind every release-included record as `{path, sha256, mode}`;
5. support only Git modes `100644` and `100755` for included payload entries;
6. materialize `100644 -> 0644` and `100755 -> 0755` in the isolated projection;
7. make `verify_projection` reject mode drift even when bytes/hash are unchanged;
8. preserve direct and ancestor symlink hardening, gitlink rejection and operational-plane decoupling from the predecessor;
9. leave `release-manifest.json`, `RELEASE_VERSION`, WPDC, consumer-lock and P1 packaging untouched.

## Exact authorized functional surface

At most:

- `tools/release_payload.py`
- `tests/test_release_payload_identity.py`
- `tests/test_release_payload_projection.py`

The candidate actually changes only the helper and projection test, plus preparation custody under the correction `governance/**` root.

## Mandatory independent checks

First confirm:

```bash
git rev-parse HEAD
```

must equal exactly:

`8da3499f08119a886df63f2267af8c2cb906146d`

Inspect:

```bash
git diff 2567fbd67e7fff50383d347913cf6442fbdebc61..8da3499f08119a886df63f2267af8c2cb906146d -- tools/release_payload.py tests/test_release_payload_identity.py tests/test_release_payload_projection.py
```

Run at minimum:

```bash
python3 -m py_compile \
  tools/release_payload.py \
  tests/test_release_payload_identity.py \
  tests/test_release_payload_projection.py

python3 -m unittest -v \
  tests/test_release_payload_identity.py \
  tests/test_release_payload_projection.py
```

Also run the full existing test suite and distinguish the already-known `EXPECTED_BOOTSTRAP_FAIL_PENDING_P1` set from any new failure.

Independently construct adversarial fixtures rather than trusting only shipped tests.

### Executable-mode fidelity

Prove independently:

- tracked `100755` file projects with executable semantics and, on POSIX, can be invoked directly;
- tracked `100644` file projects non-executable;
- projection index records the correct Git mode for each included file;
- `0755 -> 0644` after projection fails `verify_projection` with unchanged bytes;
- `0644 -> 0755` after projection fails likewise;
- unsupported index `mode` values fail closed;
- included-record shape without `mode` fails closed;
- the index schema transition to `gg.release-payload-projection-index/1.1.0` is coherent and has no stale hard-coded `1.0.0` dependency in the candidate release payload.

### Trust-chain / architecture consistency

Assess explicitly whether recording mode in the temporary projection index is sufficient under the accepted architecture where:

- exact Git `commit_sha` binds repository modes;
- scoped `content_sha256` intentionally remains byte/path-based;
- Gate A validates the exact source checkout;
- Gate B validates the isolated projection derived from that exact checkout.

If simultaneous tampering with both the projection file mode and the temporary index can pass when the index itself is treated as untrusted, classify whether that is outside the accepted projection-index trust model or a material gap requiring a stronger trust anchor. Do not infer either answer without explaining the architecture consequence.

### Manifest and non-included projection metadata

Assess whether mode fidelity must also be bound/verified for `release-manifest.json`, which is projected but is `MANIFEST_SELF_EXCLUDED` rather than a release-included content record. If current behavior is safe under the accepted architecture, explain why. If not, raise a bounded finding; do not repair it.

### Regression preservation

Re-run/adversarially verify:

- direct included symlink fail-closed;
- broken symlink fail-closed by Git mode;
- gitlink `160000` fail-closed;
- included path through symlinked ancestor fail-closed;
- projection included file replaced by symlink fail-closed;
- projection included parent replaced by symlink fail-closed;
- operational-only symlink under `governance/**` remains excluded without re-coupling payload identity;
- exact historical rc.7 content digest reproduction;
- exact-commit preservation;
- consumer-lock `2.0.0` sufficiency;
- WPDC source remains unchanged and compatible;
- correction write-surface compliance;
- bootstrap non-integrability remains disclosed and P1 remains unauthorized.

## Required verdict

Your response MUST begin with exactly one:

`PASS`
`CHANGES_REQUIRED`
`INDETERMINATE`

Then provide:

### Candidate reviewed
Exact SHA.

### Findings
For every finding: stable ID, severity (`BLOCKING`, `MATERIAL`, `MINOR`), exact surface/reproduction, invariant violated, bounded recommendation. Do not implement it.

### Validation evidence
Commands, tests and independent fixtures actually executed with observed results.

### FIND-EXEC-BIT-001 closure assessment
Explicitly state whether the original `100755 -> 0644` defect is closed and whether both upgrade/downgrade tampering are detected.

### Prior FIND-001 preservation
State whether direct and ancestor symlink-smuggling closure remains intact.

### Required invariants assessment
PASS / FAIL / INDETERMINATE individually for:

- 100644 projection fidelity
- 100755 projection fidelity
- projection index mode binding
- executable-mode downgrade detection
- executable-mode upgrade detection
- projection-index schema coherence
- projection-index trust-chain consistency
- included symlink fail-closed
- gitlink fail-closed
- ancestor symlink fail-closed
- operational-plane decoupling
- exact-commit preservation
- legacy rc.7 reproduction
- consumer-lock 2.0.0 sufficiency
- WPDC source-unchanged compatibility
- correction write-surface compliance
- bootstrap non-integrability disclosure

### Authority statement
Explicitly state that this review grants no correction, retry, P1 packaging, PR, merge, release, publication, deployment or adopter authority.

A PASS is valid only if no BLOCKING or MATERIAL finding remains and `FIND-EXEC-BIT-001` is independently demonstrated closed.
