---
document_id: GOV-L2-HIERARCHICAL-WORK-GRAPH-ADOPTION-001
capability_id: hierarchical-work-graph
version: 1.0.0
status: NORMATIVE_ADOPTION_CONTRACT_PENDING_RELEASE_INTEGRATION
normative_capability_contract: framework/capabilities/hierarchical-work-graph/contract.md
capability_contract_version: 1.0.0
---

# Hierarchical Work Graph — Adoption Contract

## 1. Purpose

This contract defines how a General Governance consumer explicitly adopts the optional Hierarchical Work Graph (HWG) capability while keeping project-specific hierarchy instances and source truth in the adopter repository.

## 2. Explicit activation

HWG is absent for a consumer unless the adopter configuration declares:

`configuration.capabilities.hierarchical_work_graph.bundle_path`

The value MUST be one non-empty adopter-repository-relative path to exactly one current `HierarchicalWorkGraphBundle` document.

No discovery key means HWG is simply not adopted. A framework release containing HWG does not activate it automatically.

If the discovery key exists but the selected bundle is missing, escapes the adopter repository, is structurally invalid, or uses unsupported HWG versions, adoption fails closed.

## 3. Ownership

General Governance owns:

- the reusable HWG normative contract;
- this adoption contract;
- reusable HWG machine schemas;
- the deterministic structural validator.

The adopter owns:

- the configuration value selecting its bundle;
- the bundle and all WorkGraph instances;
- project-specific level/profile names;
- the source artifacts and identities referenced by its graphs;
- product/work semantics, completion semantics, acceptance and authority;
- historical/superseded graph custody;
- any project-specific producer that materializes graph projections.

General Governance MUST NOT copy adopter product truth into framework-owned files merely to adopt HWG.

## 4. Bundle selection and currentness

The selected bundle is the adopter's current HWG structural projection for the applicable repository state.

Changing `bundle_path`, bundle bytes, graph refs, graph bytes, source identities, level profile, dependencies or expansion bindings is an adopter-owned structural change. Prior HWG validity MUST NOT silently transfer when changed bytes are material to the claim.

Each graph file is bound by exact SHA-256 in the bundle. File-backed source references MAY additionally bind exact SHA-256 or Git blob identity.

## 5. Bounded source resolution

HWG source locators are resolved only from exact graph `source_refs`.

When a validator receives an adopter `source_root`:

- a `SHA256` source MUST resolve to a file inside that root and match its declared SHA-256;
- a `GIT_BLOB_SHA1` source MUST resolve to a file inside that root and match `git hash-object` identity;
- an `OPAQUE_EXACT` source remains an exact identity label and MUST NOT cause the validator to search arbitrary external systems.

The validator MUST NOT roam undeclared repository paths to infer missing source context.

## 6. Relationship to project lifecycle state

HWG v1 represents current hierarchy structure, not a universal runtime lifecycle database.

Transient or authority-bearing states such as `READY`, `RUNNING`, `FAILED`, `AUTHORIZED`, `ACCEPTED`, `DEPLOYED` or `OUTCOME_UNCERTAIN` remain owned by the applicable adopter/runtime/governance surfaces.

A scheduler may combine HWG with those separate states, but MUST NOT rewrite HWG semantics merely to obtain a convenient queue.

## 7. Software profile

A software adopter MAY define the ordered profile:

```text
PRODUCT_OUTCOME
WORK_PACKET
EXECUTION_UNIT
```

For such a profile:

- product/outcome topology remains derived from adopter product truth;
- work-packet expansion remains adopter-owned and may reference WPDC-governed packet identities;
- executable-unit expansion SHOULD be materialized from the exact admitted AEA decomposition current for that packet/baseline;
- the HWG projection MUST NOT require re-running an otherwise valid admitted decomposition solely to change packaging format.

## 8. Validation and failure behavior

A conforming adoption path MUST fail closed when a selected HWG bundle cannot satisfy the normative structural contract.

A failed HWG adoption MUST NOT silently fall back to a best-effort hierarchy while still claiming HWG conformance.

A consumer that does not declare the discovery key is not in failure; HWG is absent.

## 9. Authority boundary

HWG adoption or validation grants no implementation, provider execution, mutation, merge, release, deployment, product acceptance, pilot or Owner authority.