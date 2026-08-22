# Authorization — P1 test fixture + manifest rebind correction

Identity: `GG-RELEASE-PACKAGING-SCOPED-PAYLOAD-P1-TEST-FIXTURE-REBIND-CORRECTION-001`

Project Owner authorization observed in chat on 2026-08-22.

## Exact predecessor

`9c4cc94bdc9f271e5389931c2feb73488584580e`

## Functional write surface

Exactly:

- `tests/test_work_packet_contract.py`
- `release-manifest.json`

## Required semantics

- refresh only `test_locked_release_must_advertise_wpdc` to a supported legacy `1.3.0` fake manifest;
- add non-empty legacy `content_identity_method`;
- keep `work_packet_design` absent;
- recompute the scoped rc.8 `content_sha256` after the test change;
- change only `release-manifest.json.content_sha256` as the rebind;
- keep `RELEASE_VERSION` exactly `0.1.0-rc.8`.

## Custody surface

Only under this governance directory.

## Explicitly forbidden

No `tools/**`, schemas/contracts, framework/docs/provenance, `RELEASE_VERSION`, PR, merge, tag, release/publication, or adopter mutation.

## Execution allowance

One bounded successor execution. No retry/replacement authority. Any failure or third functional path requirement is STOP.