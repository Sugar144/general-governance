---
record_id: GG-CROSS-PROJECT-EXECUTION-IDENTITY-001-OWNER-DISPOSITION-001
record_type: PROJECT_OWNER_ARCHITECTURE_DISPOSITION
status: ACCEPTED
architecture_id: GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001
architecture_path: docs/architecture/cross-project-execution-identity.md
accepted_candidate_commit_sha: 792b590303593ea2fc1005c50dff3f6489f0a534
accepted_candidate_blob_sha: 04eeaa649549872f0dcb60927b791f4bd24a4013
candidate_contract_version: 1.1.0
identity_schema: gg.execution-identity/v1
review_result: PASS_READY_FOR_OWNER_DISPOSITION
branch: architecture/cross-project-execution-identity
main_baseline_at_disposition: 486a6826685635eff0b4098fd33c4dfd826fb7ed
disposition_date: 2026-08-28
---

# Project Owner Architecture Disposition

## Owner disposition

The Project Owner explicitly accepted the exact Cross-Project Execution Identity Standard architecture candidate identified by commit `792b590303593ea2fc1005c50dff3f6489f0a534` after repository-bound review returned `PASS — READY_FOR_OWNER_DISPOSITION`.

The Owner instruction was `acepto`.

Under the Project Operating Contract, this explicit acceptance authorizes only the minimum bookkeeping required to make the decision durable. This record is that bookkeeping. It does not enlarge the accepted architecture boundary or authorize implementation, adoption, publication, integration, or downstream mutation.

## Bound accepted object

The acceptance is bound exactly to:

- repository: `Sugar144/general-governance`;
- architecture path: `docs/architecture/cross-project-execution-identity.md`;
- candidate commit: `792b590303593ea2fc1005c50dff3f6489f0a534`;
- candidate blob: `04eeaa649549872f0dcb60927b791f4bd24a4013`;
- candidate contract version: `1.1.0`;
- identity schema family: `gg.execution-identity/v1`;
- branch at disposition: `architecture/cross-project-execution-identity`;
- `main` baseline at disposition: `486a6826685635eff0b4098fd33c4dfd826fb7ed`;
- review result: `PASS_READY_FOR_OWNER_DISPOSITION`.

Any materially changed architecture content requires a new review and a new Project Owner disposition. This acceptance does not silently transfer to a later commit, changed blob, revised contract version, or modified schema semantics.

## Accepted architecture boundary

The accepted architecture establishes, at architecture level, the provider-neutral cross-project identity semantics for:

- `Identity Scope` as namespace/context rather than execution authority;
- `Semantic Intent` as upstream semantic intent, with `ST` as the canonical story subtype;
- strict separation between `Semantic Intent` and WPDC `declared outcome`;
- `PKT` reserved for Implementation Packet identity;
- explicit many-to-many `Semantic Intent ↔ PKT` relationships;
- `EXEC` as immutable executable specification over exactly one governed subject;
- optional generic PKT binding and mandatory exactly-one PKT binding for `execution_kind: IMPLEMENTATION_PACKET`;
- `RUN` as one historical invocation of one EXEC for prospective conforming execution;
- optional leaf identity `L` for leaf-based execution;
- explicit Attempt identity `A`, including `A001` for the first concrete invocation entering the attempt lifecycle;
- boundary crossing as evidence/state about an Attempt rather than the event that creates Attempt identity;
- `REC`, `REV`, and `DEC` as distinct typed lateral identities;
- `REV != RUN`, while allowing an explicit `produced_by_run` relation;
- preservation of existing GG `<BASE_RUN_ID>-R<N>` formal-run result correction identity as distinct from recovery, retry, and replacement;
- structured relationships as authoritative and durable identity strings as projections;
- non-destructive legacy bridging and historical identity immutability;
- no retroactive manufacture of missing `PKT`, `EXEC`, `L`, or `A` identities for historical evidence.

## Authority boundary

This Owner acceptance closes the architecture design/disposition boundary for `GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001` only.

It does not authorize:

- creation or modification of machine schemas or validators;
- modification of the Project Operating Contract;
- modification of WPDC contracts or schemas;
- modification of the GG learning lifecycle;
- AEC S6 implementation or mutation;
- AEC adoption of `gg.execution-identity/v1`;
- SVP migration, mutation, or historical renaming;
- OPD mutation;
- automatic cross-project migration;
- pull request creation;
- merge or integration to `main`;
- release, tag, publication, or deployment.

Any such material step requires its own applicable authority, currentness checks, and review/adoption lifecycle.
