---
record_id: GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001-CORRECTION-001
record_type: NORMATIVE_CORRECTION
status: PASS
block_id: GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001
authorized_by: PROJECT_OWNER
source_review_pr: 13
source_review_comment: 3825699572
pre_correction_contract_blob: 8c4239a2da29ba19da8d585933540acc0e71b773
corrected_contract_commit: 917b16a5bd3a79fce0cde3178794bf191f8bb0e2
corrected_contract_blob: 6fdbebe5e5d8beec5dddce7b571e6df9337d0fc0
control_regression_commit: d25cc9a30ab77f7025d8d6e4129daf530501e214
control_regression_blob: 607750cac8510d0c9b542bdf7e11677e730ca4d1
correction_date: 2026-08-21
---

# Normative Correction 001 — Required WPDC Packet Control Declarations

## Finding

PR #13 review identified that the accepted WPDC architecture required deterministic handling of missing required boundary/authority declarations, including required authority declarations and terminal/stop-boundary shape, while the first normative capability-contract candidate did not state those packet declarations as explicit normative obligations.

That omission created an invalid derivation direction: the Block 2 machine manifest required `authority_refs`, `required_authority_refs`, `stop_conditions`, and `terminal_boundary`, but the Block 1 normative contract did not yet require all of those controls explicitly.

## Authority

The Project Owner explicitly authorized the bounded normative correction after the finding was reported as material.

The correction is limited to materializing semantics already present in the Owner-accepted architecture at `d43950df47d9d01b516a46f63e7ae9f7da1f24f7`. It does not introduce a new WPDC product decision or broaden the capability.

## Correction

`framework/capabilities/work-packet-design/contract.md` now requires every packet evaluated under adopted WPDC to declare:

- governing authority references and the authority references required for represented evaluation;
- one or more explicit stop conditions for governed-boundary drift;
- a terminal boundary for WPDC packet completion.

The contract also states explicitly that these are structural governance inputs and never self-grant execution, mutation, publication, merge, release, or acceptance authority.

`PACKET_INVALID` examples and the deterministic-responsibility boundary were aligned with the same accepted architecture.

## Regression protection

`tests/test_work_packet_control_declarations.py` proves schema-level rejection when:

- governing authority declarations are absent;
- the required-authority set is empty;
- stop conditions are absent;
- the terminal boundary is absent.

The valid control-declaration shape remains accepted.

The combined WPDC machine/control suite executed after the correction with 9/9 test methods passing, including the existing generic regression catalog.

## Provenance reachability review

A separate PR review finding had warned that architecture/provenance commits might become unreachable in a future clone. That finding described an earlier branch topology. Against the corrected integration line, all three referenced identities are ancestors of the Block 2 candidate line:

- accepted architecture candidate `d43950df47d9d01b516a46f63e7ae9f7da1f24f7`;
- durable Owner disposition `88f1be46a3920154e66cad2d64344b9263737c78`;
- original reviewed normative candidate `49bb7b37792290961d859b14a9854d80b3554729`.

Therefore no additional provenance rewrite is required on the current topology. The ancestry must remain preserved through final merge integration.

## Disposition

`PASS`

The Block 1 normative contract and the Block 2 machine contract are now directionally consistent. Release identity and final integration remain deferred to the separately authorized Framework Release Integration block.
