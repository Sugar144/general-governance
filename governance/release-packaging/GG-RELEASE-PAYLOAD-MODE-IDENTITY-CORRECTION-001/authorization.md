# Owner authority — scoped Git-mode identity correction

Correction: `GG-RELEASE-PAYLOAD-MODE-IDENTITY-CORRECTION-001`

Finding: `P1-FIND-EXECUTABLE-MODE-NOT-AUTHENTICATED-001`

Authority source: explicit Project Owner authorization in chat on 2026-08-22 after bounded read-only scope derivation.

Exact predecessor PR head: `c787971f33c78d1d5b8cf57bdf1dc983acd22e53`.

Previously validated functional predecessor: `a586cc7f5eb44f15c64d10da9e76f2b1db2b1705`.

This authority permits exactly one bounded successor correction execution.

Authorized non-custody paths:

1. `tools/release_payload.py`
2. `tests/test_release_payload_identity.py`
3. `tests/test_release_payload_projection.py`
4. `docs/architecture/release-payload-identity.md`
5. `release-manifest.json`

Required behavior:

- legacy `1.3.0` / rc.7 record encoding remains unchanged;
- scoped `1.4.0` / `SCOPED_TRACKED_FILES_V1` authenticates tracked Git mode (`100644` / `100755`) together with path and exact file bytes;
- projection verification rejects coordinated projected-mode + index-mode tampering when bytes are unchanged;
- rc.8 manifest is rebound to the exact new scoped digest computed from the exact local checkout.

Custody is restricted to this governance directory.

No authority is granted for `RELEASE_VERSION`, schema/method changes, consumer/WPDC validators, CI, framework/provenance, review-thread resolution before validated PASS, merge/tag/release/deploy, PR #15/#16, or adopter/SVP mutation.

Execution allowance: `1`.

Retry/replacement authority: `NONE`.