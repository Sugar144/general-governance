# External Consumer Contract

`Sugar144/general-governance` is the authoritative repository identity for this framework.
A version label is descriptive only: a consumer is governed by the tuple
`(repository, version, commit_sha, release_manifest_sha256)`. The exact commit and
manifest digest are immutable; floating branches or tags are not valid locks.

## Delivery, lock, and required configuration

A consumer may acquire framework bytes by any reproducible transport, but acquisition is not authority.
It must write `framework-lock.json` conforming to `contracts/consumer-lock.schema.json`; the lock identifies
the immutable framework revision and adopter-owned configuration path.

The configuration instance is mandatory. Its machine contract is
`contracts/consumer-configuration.schema.json`; its semantic contract is
`framework/contracts/configuration-schema.yaml`.

Required core values remain mandatory. Optional capabilities are activated only by the discovery key owned by
that capability contract.

## Repository and release-payload identity

The exact Git commit binds the complete selected repository revision.

Historical releases through the legacy identity method bind every tracked path except
`release-manifest.json`. Scoped releases use
`content_identity.method = SCOPED_TRACKED_FILES_V1` so `content_sha256` binds the classified reusable
Framework Release Payload while the exact commit continues to bind the complete repository tree.

Manifest schema `1.4.0` remains supported for historical scoped releases. `0.1.0-rc.10` uses manifest schema
`1.5.0`, which adds the advertised HWG capability identity without changing the scoped file-classification method.

`governance/**` is reserved for operational/evolution evidence and is excluded from the reusable payload.
Protected reusable release surfaces include `framework/**`, `contracts/**`, `tools/**`, `tests/**`, `docs/**`,
`provenance/**`, `RELEASE_VERSION`, `README.md`, and `.github/workflows/conformance-ci.yml`.

For scoped releases, conformance has two gates:

- **Gate A — full checkout identity:** exact commit, exact manifest hash, payload digest reproduction,
  compatibility and release-facing regressions.
- **Gate B — isolated payload self-sufficiency:** project only reusable payload bytes plus
  `release-manifest.json`, physically omit operational files and `.git`, and rerun projection-safe validation.

## Compatibility

`0.1.0-rc.10` preserves:

- framework contract `2.0.0`;
- consumer-lock schema `2.0.0`;
- consumer-configuration schema `1.0.0`;
- capability-composition contract/schema `1.0.0`;
- Work Packet Design & Dependency Closure (WPDC) contract/adoption/machine versions `1.0.0`.

It adds optional Hierarchical Work Graph (HWG) contract/adoption/bundle/graph versions `1.0.0`.

No current core consumer-owned value is added. Consumers that do not adopt HWG require no configuration
migration beyond the new immutable framework lock identity.

## Work Packet Design & Dependency Closure

WPDC remains an optional L2 capability governing prerequisite closure inside one bounded packet.
Its discovery key is:

`configuration.capabilities.work_packet_design.binding_path`

Framework availability alone does not activate WPDC.

## Hierarchical Work Graph

HWG is an optional L2 capability governing reusable work hierarchy/topology and progressive parent/child graph expansion.
Its discovery key is:

`configuration.capabilities.hierarchical_work_graph.bundle_path`

When absent, HWG is not adopted and consumer conformance continues normally.

When present, the selected bundle must:

- conform to `contracts/hierarchical-work-graph-bundle.schema.json` version `1.0.0`;
- reference `WorkGraph` documents conforming to `contracts/work-graph.schema.json` version `1.0.0`;
- satisfy deterministic hierarchy invariants in `tools/validate_hierarchical_work_graph.py`;
- keep all selected bundle/graph paths inside the adopter repository;
- preserve exact graph SHA-256 identities;
- preserve exact supported source identities when file-backed source validation is requested.

A structurally valid HWG does not grant authority and does not prove concurrent safety.

For a software profile, a project may use:

```text
PRODUCT_OUTCOME
  -> WORK_PACKET
    -> EXECUTION_UNIT
```

The level labels are adopter-profile semantics rather than universal GG ontology.

## Controlled upgrade

An upgrade is an explicit `old lock -> configuration migration/evaluation -> new lock` transition recorded in
`framework-upgrade.json` with both immutable identities and a passing conformance result.

Moving from rc.9 to rc.10 requires a new immutable lock. If HWG remains absent, no HWG bundle is required.
If HWG is enabled, the adopter supplies its own exact bundle path and project-owned hierarchy artifacts.

Consumers never follow a moving branch automatically.

## Ownership boundary

Framework-owned surfaces are reusable L0 semantics, the L1 configuration contract, separately released L2
capabilities, reusable helpers, schemas and validators. Consumer-owned surfaces remain project-specific
projections, evidence/history, configuration values, state, authority, capability-stack bindings and runtime/provider
bindings.

General Governance conformance never transfers implementation, provider execution, mutation, merge, release,
deployment, acceptance or Owner authority.
