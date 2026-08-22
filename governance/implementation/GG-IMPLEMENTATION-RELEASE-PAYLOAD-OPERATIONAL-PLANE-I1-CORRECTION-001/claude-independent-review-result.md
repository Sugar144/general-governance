# Claude Independent Review Result

Review ID: `GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-CORRECTION-001-IR-001`

Candidate reviewed: `2567fbd67e7fff50383d347913cf6442fbdebc61`

Verdict: `CHANGES_REQUIRED`

## Findings

### FIND-EXEC-BIT-001 — MATERIAL

`tools/release_payload.py` admits Git mode `100755` as supported, but `build_projection` copies bytes with `write_bytes()` without preserving executable mode and `verify_projection` does not verify mode fidelity. An independent fixture demonstrated a tracked `100755` file projects as filesystem mode `0o644` while build + verify still succeed.

This is a correctness failure for Gate B: a future release-included executable can silently become non-executable in the isolated release payload while all current integrity checks pass.

Bounded recommendation from reviewer: either preserve/verify mode for `100755`, or explicitly remove executable-mode fidelity from the supported contract. No correction was implemented by the reviewer.

### FIND-TOCTOU-001 — MINOR

Symlink hardening uses separate lstat/is_symlink checks followed by file read, so a concurrent local writer could theoretically race validation. Reviewer classified this MINOR because the stated threat model is malicious repository/working-tree state, not a concurrent local attacker with write access during validation.

## FIND-001 closure

The original blocking finding is independently CLOSED:

1. direct tracked symlink into `governance/**` — PASS fail-closed;
2. ancestor-directory symlink variant — PASS fail-closed.

Additional adversarial checks passed for broken symlinks, gitlink `160000`, nested ancestor symlinks, projection direct-symlink tamper, projection ancestor-directory symlink tamper, operational-plane decoupling, non-zero index stage rejection, exact-commit preservation, legacy rc.7 reproduction, consumer-lock 2.0.0, WPDC source-unchanged compatibility, and correction write-surface compliance.

## Validation evidence summary

- exact candidate SHA confirmed;
- targeted compile/tests: PASS;
- identity + projection suite: `34/34 OK`;
- full suite candidate vs predecessor: identical `10 failures + 1 error`, all classified as the already documented `EXPECTED_BOOTSTRAP_FAIL_PENDING_P1` set;
- historical rc.7 content digest reproduced exactly as `14fceee7fb261fee6c2b515cbd81e39c91daaaaa3aa8dc431d3c1beac754d15e`;
- independent adversarial fixture demonstrated the new executable-bit projection fidelity defect.

## Required invariants

PASS:
- included tracked symlink fail-closed;
- included gitlink/unsupported mode fail-closed;
- ancestor-directory symlink fail-closed;
- projection direct-symlink tamper detection;
- projection ancestor-symlink tamper detection;
- operational-plane decoupling;
- scoped manifest/schema enforcement;
- exact-commit preservation;
- legacy rc.7 reproduction;
- consumer-lock 2.0.0 sufficiency;
- WPDC source-unchanged compatibility;
- correction write-surface compliance;
- bootstrap non-integrability disclosure.

FAIL:
- `100755` executable-mode projection fidelity.

## Authority

This review grants no correction, retry, P1 packaging, PR, merge, release, publication, deployment, or adopter authority.
