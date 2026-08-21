---
record_id: GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001-REVIEW-001
record_type: SEMANTIC_REVIEW
status: PASS_MACHINE_CANDIDATE
block_id: GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001
reviewed_candidate_commit: d25cc9a30ab77f7025d8d6e4129daf530501e214
main_baseline: 640fb33bc96bff75d757b8325ae6290c1a4e0f2f
review_date: 2026-08-21
---

# Semantic Review — WPDC Machine Contract, Validator & Generic Regressions

## Verdict

`PASS — MACHINE CANDIDATE ACCEPTABLE, INTEGRATION DEFERRED TO RELEASE BLOCK`

The Block 2 candidate is consistent with the Owner-accepted architecture and the corrected Block 1 normative capability/adoption contracts. No unresolved machine-contract or semantic-boundary finding remains in the reviewed candidate.

## Reviewed machine surfaces

The candidate contains:

- `contracts/work-packet-capability-binding.schema.json`;
- `contracts/work-packet-manifest.schema.json`;
- `tools/validate_work_packet.py`;
- `tests/fixtures/work-packet/cases.json`;
- `tests/test_work_packet_contract.py`;
- `tests/test_work_packet_control_declarations.py`.

The machine contract represents only bounded deterministic claims. It does not infer undeclared semantic prerequisites, judge substantive product architecture, or grant execution authority.

## Deterministic semantics reviewed

The validator and schemas preserve the accepted distinctions:

- dependency relations `REACH`, `VALIDATE`, `COMPLETE`;
- resolutions `IN_PACKET`, `PREEXISTING_SATISFIED`, `BOUND_EXTERNAL_SATISFIED`, `UNRESOLVED`;
- transitive closure from every included outcome;
- cycles are invalid;
- `UNRESOLVED` yields `VALID_BUT_BLOCKED` when no stronger invalidity applies;
- unsatisfied required prerequisites cannot be excluded while their dependent included outcomes remain;
- adopter-owned satisfaction is distinct from separately identified external satisfaction;
- immutable canonical-base evidence is bound to exact commit bytes rather than current working-tree bytes;
- mutable state remains separately represented and currentness-bound;
- adoption binding bytes are digest-bound;
- required authority/control declarations are structural, not self-granting authority;
- `VALID_DEPENDENCY_CLOSED` explicitly does not imply execution authority.

## Findings discovered and corrected during Block 2

### F1 — Over-coupling exact adopter facts to generic source mappings

The first machine draft required all direct preexisting evidence/state identities to resolve through generic adopter source mappings. The adoption contract allows exact bounded references when generic mappings are absent.

Correction: exact adopter-owned canonical/state references may remain directly bound without inventing generic source mappings; declared mapped sources are still class-checked when present.

### F2 — Evidence custody incorrectly coupled to manifest directory

The first validator draft resolved evidence only beneath the manifest directory, which would require copying durable adopter evidence into packet custody.

Correction: evidence paths are repository-relative and must remain inside the supplied adopter repository root. Packet projection and evidence custody are independent.

### F3 — Canonical-base evidence could have been checked against drifted working-tree bytes

Correction: canonical evidence is verified through Git against the declared canonical commit (`git show <commit>:<path>`), and the declared canonical commit must resolve in the supplied adopter repository.

### F4 — Normative control-declaration omission

PR #13 review correctly identified that Block 1 had omitted explicit normative MUST language for authority, stop-condition, and terminal-boundary declarations even though the accepted architecture required deterministic handling of those controls.

Correction: `GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001-CORRECTION-001` materializes those existing architecture obligations in the normative contract. The machine schema is therefore no longer broader than its normative source.

### F5 — Provenance reachability warning

PR review also warned that exact architecture/provenance commits could become unreachable under an earlier branch topology.

Current ancestry checks demonstrate that `d43950df47d9d01b516a46f63e7ae9f7da1f24f7`, `88f1be46a3920154e66cad2d64344b9263737c78`, and `49bb7b37792290961d859b14a9854d80b3554729` are ancestors of the reviewed Block 2 candidate line. The warning is therefore not a live defect in the current topology, provided final integration preserves this ancestry.

## Regression result

The exact reconstructed Block 2 machine bytes plus the control-declaration regression file executed with:

`9/9 test methods PASS`

This includes the generic fixture catalog covering closed, blocked, invalid, transitive, cycle, evidence-digest, binding-digest, currentness, external-source classification, exclusion, and canonical-base cases.

The local execution runtime was CPython 3.13. Python 3.12 grammar compatibility was checked separately. GitHub Actions uses Python 3.12 and successfully meta-validates both new JSON schemas, but the current rc.5 CI workflow does not yet execute `test_work_packet_contract.py` or `test_work_packet_control_declarations.py`. Adding those release gates belongs to Block 3 and is required before final integration.

## Existing repository CI

On PR head `d25cc9a30ab77f7025d8d6e4129daf530501e214`, conformance-ci run `32424617909` successfully completed schema meta-validation, capability-stack syntax validation, and prospective evolution verification, then failed in the existing consumer-conformance tests because the expanded tracked content no longer reproduces immutable rc.5 release content identity.

This is the already-known release-integration dependency, not a Block 2 semantic/machine defect.

## Scope review

Block 2 has not changed:

- `release-manifest.json`;
- `RELEASE_VERSION`;
- current release compatibility declarations;
- L0 semantics;
- existing consumer validator behavior;
- CI workflow definitions;
- agent skill implementation;
- SVP or any consumer/adopter repository.

## Final review disposition

`PASS_MACHINE_CANDIDATE`

Block 2 is acceptable as the exact machine candidate dependency for Block 3. It MUST NOT merge independently while the release identity gate remains unsatisfied.
