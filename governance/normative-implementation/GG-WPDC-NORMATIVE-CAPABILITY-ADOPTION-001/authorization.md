---
record_id: GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001-AUTH-001
record_type: PROJECT_OWNER_BLOCK_AUTHORIZATION
status: ACTIVE_PROSPECTIVE
block_id: GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001
block_name: Work Packet Design & Dependency Closure — Normative Capability & Adoption Contract
branch: method/wpdc-normative-capability-adoption-001
branch_start_sha: 88f1be46a3920154e66cad2d64344b9263737c78
accepted_architecture_commit_sha: d43950df47d9d01b516a46f63e7ae9f7da1f24f7
accepted_architecture_blob_sha: 0ddf288274c9805a4a00b2d3929e9c7fe6aa12ec
main_baseline_at_authorization: 640fb33bc96bff75d757b8325ae6290c1a4e0f2f
authorization_date: 2026-08-20
---

# Block Authorization — WPDC Normative Capability & Adoption Contract

## Owner authority

The Project Owner instruction `acepto el primer bloque adelante` authorizes this complete bounded block through merge, subject to the acceptance gates and stop conditions below.

Within this block, separate Owner authorization is not required for routine preparation, repository mutation inside the allowed write surface, commits, pushes, repository-bound review, corrections that remain within the accepted architecture and write surface, pull-request creation, CI/review handling, conditional acceptance, or merge of the exact passing candidate.

This is bounded prospective authority, not unconditional acceptance. A failing candidate MUST NOT be accepted or merged merely because the block was authorized.

## Bound objective

Materialize the Owner-accepted Work Packet Design & Dependency Closure architecture as the first reusable optional General Governance L2 normative capability and define its adopter-facing semantic adoption contract.

The block must establish durable normative semantics and adoption semantics only. Machine schemas, deterministic implementation, regression fixtures, CI integration, release packaging, skills, and consumer adoption are later blocks.

## Required outputs

The block must produce:

1. a normative Work Packet Design & Dependency Closure capability contract version `1.0.0`;
2. an adopter-facing semantic adoption contract version `1.0.0`;
3. any minimal descriptive repository update required so top-level ownership statements do not contradict the newly materialized optional L2 capability;
4. this durable block authorization and bounded review/acceptance evidence needed to support merge.

## Allowed write surface

New or modified content is limited to:

- `framework/capabilities/work-packet-design/**`;
- `README.md`, only if needed to correct the framework ownership summary for selected optional L2 modules;
- `governance/normative-implementation/GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001/**`.

The already accepted architecture and Owner disposition inherited from branch start are inputs and MUST NOT be rewritten by this block:

- `docs/architecture/work-packet-design-dependency-closure.md`;
- `governance/architecture-decisions/GG-WPDC-ARCHITECTURE-001/owner-disposition.md`.

## Forbidden scope

This block MUST NOT:

- modify L0 Project Operating Contract semantics;
- create or modify JSON/YAML machine schemas;
- implement `validate_work_packet.py` or other deterministic validators;
- add regression fixtures or test code;
- modify CI workflows;
- modify `release-manifest.json`, `RELEASE_VERSION`, upgrade/evolution contracts, tags, or GitHub Releases;
- implement Packet Designer or Reviewer skills;
- adopt the capability in SVP or any other consumer;
- re-evaluate, rewrite, or authorize the existing SVP packet;
- create execution authority from dependency closure.

## Acceptance contract

The block may be conditionally accepted and merged only when all of the following are true:

1. the normative capability is faithful to the exact Owner-accepted architecture and does not introduce a materially new invariant;
2. the capability remains optional L2 and applies only after explicit adopter activation;
3. dependency closure remains transitive over all included outcomes and preserves `REACH`, `VALIDATE`, and `COMPLETE`;
4. the four prerequisite resolutions remain `IN_PACKET`, `PREEXISTING_SATISFIED`, `BOUND_EXTERNAL_SATISFIED`, and `UNRESOLVED`, with direct adopter-owned satisfaction distinct from separately bound external satisfaction;
5. mutable/external state evidence remains distinct from immutable canonical-base identity and is subject to applicable currentness/revalidation semantics;
6. `UNRESOLVED` yields a valid-but-blocked packet when no contradictory exclusion or other invalidity exists;
7. dependency closure never manufactures execution, publication, acceptance, release, or Owner authority;
8. the adoption contract requires explicit adopter-owned binding, does not prescribe universal repository paths, and does not retroactively activate or re-evaluate packets;
9. the human semantic packet remains authoritative over machine projection, while later deterministic tooling is explicitly bounded to declared machine-checkable claims;
10. no forbidden scope or unexpected file is present in the block diff;
11. repository-bound semantic review returns PASS with no unresolved material finding;
12. `main` currentness and PR mergeability are rechecked before merge;
13. the repository-required `consumer-contract` check passes on the exact PR head, or an equivalent repository-protected required check proves merge readiness;
14. the exact merged head is the reviewed and passing candidate; no unreviewed semantic change is introduced after acceptance.

## Stop and escalation conditions

The block MUST stop for a new Owner decision if completing it requires any of the following:

- changing an accepted architecture invariant or responsibility boundary;
- widening the allowed write/effect surface materially;
- modifying L0, machine schemas, validators, CI, release semantics, skills, or a consumer;
- resolving a newly discovered product/governance dependency that changes the capability design materially;
- accepting a semantic review finding by changing the architecture rather than correcting implementation drift;
- bypassing a required branch-protection or currentness gate.

Routine corrections that simply make the block conform to the accepted architecture do not require a new Owner authorization.

## Merge authority boundary

This authorization includes creation of one PR for this block and merge of the exact passing candidate into `main` after all acceptance gates pass.

Merge closes this block. It does not authorize tag, GitHub Release, release packaging, deployment, the next WPDC implementation block, skill work, or consumer/SVP adoption.