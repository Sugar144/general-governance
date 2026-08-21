---
record_id: GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001-AUTH-001
record_type: PROJECT_OWNER_BLOCK_AUTHORIZATION
status: ACTIVE_PROSPECTIVE
block_id: GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001
block_name: WPDC Machine Contract, Deterministic Validator & Generic Regressions
branch: method/wpdc-normative-capability-adoption-001
starting_head: 094b5ca4e0dcf3e4a81e8cf213407b56e3dfab18
main_baseline: 640fb33bc96bff75d757b8325ae6290c1a4e0f2f
normative_candidate: 49bb7b37792290961d859b14a9854d80b3554729
pull_request: 13
---

# Project Owner Block Authorization — WPDC Machine Contract & Validator

## Owner authority

The Project Owner instruction `adelante`, given after Block 1 was accepted at normative-candidate level and its integration was deferred by the release-identity gate, authorizes Block 2 as one bounded implementation block.

Under the Owner-approved block-authorization operating mode, this authorization covers ordinary implementation, deterministic validation, semantic review, bounded corrections, commits, pushes, PR maintenance, and conditional acceptance for this block without requiring separate authorization for each minor action.

Because General Governance release identity prevents Blocks 1 and 2 from being merged independently without Block 3, this authorization does not manufacture a merge that bypasses the repository-required release-identity gate. Block 2 may become an accepted exact candidate on the existing bounded integration line while final merge remains dependent on separately authorized Framework Release Integration.

## Bound inputs

Block 2 is derived from:

- Owner-accepted WPDC architecture candidate `d43950df47d9d01b516a46f63e7ae9f7da1f24f7`;
- durable architecture disposition `88f1be46a3920154e66cad2d64344b9263737c78`;
- reviewed Block 1 normative candidate `49bb7b37792290961d859b14a9854d80b3554729`;
- Block 1 result at integration-line HEAD `094b5ca4e0dcf3e4a81e8cf213407b56e3dfab18`;
- unchanged protected `main` baseline `640fb33bc96bff75d757b8325ae6290c1a4e0f2f`.

If implementing Block 2 requires changing an accepted WPDC semantic invariant rather than merely encoding it, execution must stop for material disposition.

## Objective

Implement the smallest deterministic machine surface that faithfully encodes the accepted WPDC v1 contracts:

1. one adopter-binding schema;
2. one minimal work-packet manifest schema;
3. one dedicated deterministic validator;
4. one generic regression suite/fixture family covering the accepted invariants.

The machine implementation must complement semantic packet design/review; it must not claim semantic completeness or execution authority.

## Allowed write surface

Only:

- `contracts/work-packet-capability-binding.schema.json`;
- `contracts/work-packet-manifest.schema.json`;
- `tools/validate_work_packet.py`;
- `tests/test_work_packet_contract.py`;
- `tests/fixtures/work-packet/**`;
- `governance/normative-implementation/GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001/**`;
- PR #13 metadata/comments required to preserve the block result.

No existing Block 1 normative contract may be changed unless a machine-implementation attempt exposes a genuine material contradiction that cannot be resolved without semantic contract change; such a condition is a stop boundary, not implicit authority to rewrite Block 1.

## Required machine behavior

The resulting deterministic validator must, from declared machine claims only:

- validate both machine schemas;
- bind a packet evaluation to the exact adopter-binding identity/content digest supplied for evaluation;
- verify stable identifier/reference integrity;
- validate canonical-base identity shape and adopter-repository binding when declared;
- traverse prerequisite dependencies transitively from all included outcomes;
- reject dependency cycles;
- require exactly one supported resolution for every represented prerequisite;
- validate evidence file existence, bounded relative paths, and SHA-256 digests when evidence is used;
- preserve the mutually exclusive `PREEXISTING_SATISFIED` versus `BOUND_EXTERNAL_SATISFIED` source boundary where the declared identities make that distinction deterministic;
- validate represented state-currentness rule references without inventing semantic freshness;
- reject included/excluded contradictions and excluded unsatisfied required prerequisites;
- validate completion-condition to validation-reference coverage structurally;
- require represented authority/boundary/stop/terminal claims without interpreting them as granted authority;
- derive only `PACKET_INVALID`, `VALID_BUT_BLOCKED`, or `VALID_DEPENDENCY_CLOSED`;
- never interpret `VALID_DEPENDENCY_CLOSED` as execution authorization.

## Required generic regressions

At minimum, regression coverage must prove:

- `IN_PACKET` with complete closure -> `VALID_DEPENDENCY_CLOSED`;
- correctly evidenced direct adopter-owned satisfaction -> `VALID_DEPENDENCY_CLOSED`;
- correctly evidenced separately bound external satisfaction -> `VALID_DEPENDENCY_CLOSED`;
- honestly declared `UNRESOLVED` -> `VALID_BUT_BLOCKED`;
- reachable `UNRESOLVED` plus exclusion -> `PACKET_INVALID`;
- reachable `IN_PACKET` plus exclusion -> `PACKET_INVALID`;
- transitive unresolved prerequisite -> `VALID_BUT_BLOCKED`;
- unresolved references -> `PACKET_INVALID`;
- dependency cycle -> `PACKET_INVALID`;
- missing structural validation coverage -> `PACKET_INVALID`;
- declared external satisfaction misrepresented as adopter-owned where machine-bound source identities prove otherwise -> `PACKET_INVALID`;
- invalid evidence/currentness/binding identity -> `PACKET_INVALID`.

Additional bounded regressions may be added when they directly protect an accepted invariant or a defect discovered during this block.

## Acceptance gates

Block 2 may be accepted at exact-candidate level only when:

1. both JSON Schemas pass Draft 2020-12 meta-validation;
2. the validator compiles under the repository's Python 3.12 target;
3. the dedicated regression suite passes in an isolated checkout of the exact candidate;
4. semantic review finds no WPDC contract drift, authority leakage, consumer/SVP coupling, hidden inference, or false closure behavior;
5. the diff remains inside the allowed write surface;
6. exact candidate identity and review evidence are recorded durably;
7. any repository-required check failure attributable solely to the known unreleased content identity is preserved as the Block 3 dependency rather than bypassed.

## Forbidden actions

Block 2 MUST NOT:

- change `release-manifest.json` or `RELEASE_VERSION`;
- modify `.github/workflows/**` or CI requirements;
- modify L0 Project Operating Contract semantics;
- modify capability-stack semantics;
- modify the base consumer configuration/lock schemas merely to activate WPDC;
- implement the Packet Designer/Reviewer skill;
- adopt WPDC in SVP or any consumer;
- rewrite/reclassify the existing SVP packet;
- merge while the required release-identity gate fails;
- tag, release, deploy, or publish a General Governance release.

## Stop boundary

Stop for material Owner disposition only if the machine implementation requires changing accepted WPDC semantics, expanding into another independently governed capability, weakening a current authority/currentness invariant, or otherwise exceeding this block. Ordinary implementation defects and test/review findings inside the accepted machine boundary are authorized for correction within the block.