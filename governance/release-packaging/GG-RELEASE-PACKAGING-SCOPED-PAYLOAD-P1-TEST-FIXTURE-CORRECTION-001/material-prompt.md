---
prompt_id: GG-MP-0011
version: 1.0.0
status: APPROVED_NOT_EXECUTED
correction_id: GG-RELEASE-PACKAGING-SCOPED-PAYLOAD-P1-TEST-FIXTURE-CORRECTION-001
---

# Material prompt

Perform exactly one bounded test-fixture correction on predecessor `9c4cc94bdc9f271e5389931c2feb73488584580e`.

Modify only `tests/test_work_packet_contract.py`, and only the fake release manifest built by `test_locked_release_must_advertise_wpdc`.

Replace unsupported `manifest_schema_version: 1.2.0` with supported legacy `1.3.0` and add the non-empty legacy `content_identity_method` required by the current release payload validator. Keep `work_packet_design` absent so the test still proves that a locked release lacking the WPDC declaration fails with `INVALID_ADOPTION_BINDING` and a `does not advertise` message.

Do not modify production code, release payload implementation, validators, schemas, `RELEASE_VERSION`, `release-manifest.json`, framework/docs/provenance, P1 release semantics, PRs, merge state, tags, releases, deployment/publication, or adopters.

Required post-change evidence: exact write-surface, targeted test, full work-packet test module, identity/projection 37/37, full suite 77/77, Gate A and Gate B, then fresh independent review. Any failure stops execution; no retry/replacement authority exists.