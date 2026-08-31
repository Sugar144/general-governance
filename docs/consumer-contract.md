# External Consumer Contract

`Sugar144/general-governance` is the authoritative identity for this framework.
A version label is descriptive only: a consumer is governed by the tuple
`(repository, version, commit_sha, release_manifest_sha256)`. The commit and
manifest digest are immutable; `main`, `latest`, `current`, branches, and tags
without an exact commit are invalid locks.

## Delivery, lock, and required configuration

A consumer may acquire bytes by an archive, clone, cache, package registry, or
other reproducible transport. Acquisition is not authority. It must write a
`framework-lock.json` conforming to `contracts/consumer-lock.schema.json`; the
lock identifies the immutable revision and the adopter-owned configuration path
that govern the consumer.

The configuration instance is mandatory. Its machine contract is
`contracts/consumer-configuration.schema.json`; its semantic contract is
`framework/contracts/configuration-schema.yaml`. The official validator fails
closed when the configuration is absent, structurally invalid, incompatible,
contains unresolved double-brace placeholders, omits a required key, or fails
to resolve a declared reusable-core placeholder.

Required core configuration values remain mandatory. Optional capability
discovery keys do not become required merely because a framework release makes
the capability available.

## Repository revision identity and release payload identity

The exact Git `commit_sha` binds the complete selected repository revision.
Operational/evolution evidence is therefore never unbound merely because it is
outside a prospective framework payload digest.

Historical releases through `0.1.0-rc.7` use the legacy complete-tracked-files
content identity: every tracked path except `release-manifest.json` contributes
to `content_sha256`.

A successor release may declare a scoped manifest with
`content_identity.method = SCOPED_TRACKED_FILES_V1`. Under that method,
`content_sha256` binds the classified **Framework Release Payload** while the
exact Git commit still binds the complete repository tree. Classification is
fail-closed: any tracked path not explicitly recognized as operational is
`RELEASE_INCLUDED`.

Manifest schema `1.4.0` remains supported for historical scoped releases.
`0.1.0-rc.10` uses manifest schema `1.5.0`, which adds the advertised HWG
capability identity without changing the `SCOPED_TRACKED_FILES_V1`
classification method.

`governance/**` is the reserved General Governance operational/evolution
namespace for formal run custody, decisions, discovery, design, implementation
process evidence, pilots, learning records, and release-process evidence. It
must not contain reusable consumer-visible framework behavior.

Method-v1 protected release surfaces include `framework/**`, `contracts/**`,
`tools/**`, `tests/**`, `docs/**`, `provenance/**`, `RELEASE_VERSION`,
`README.md`, and `.github/workflows/conformance-ci.yml`; manifest policy cannot
exclude them. Additional repository controls may be operational only through
the bounded exact-path policy declared by the release manifest.

For scoped releases, conformance has two distinct gates:

- **Gate A — full checkout identity:** exact commit, exact manifest hash,
  payload digest reproduction, compatibility and release-facing regressions.
- **Gate B — isolated payload self-sufficiency:** construct a fresh projection
  containing only `RELEASE_INCLUDED` files plus `release-manifest.json`, with
  operational files and `.git` physically absent, and run projection-safe
  release-facing validation there.

Gate B is not a substitute for the production exact-commit check. No
`skip_git_check`, `ignore_commit`, or equivalent production bypass is valid.

Later commits that change only `OPERATIONAL_EXCLUDED` bytes may be
payload-equivalent to a published scoped release, but they are still distinct
repository revisions because their exact commit SHAs differ. They do not become
publication anchors implicitly. A consumer remains bound to the exact commit
named in its lock.

## Material-prompt identity

Material-prompt identity semantics are reusable; the project namespace is not.
The reusable operating contract requires a stable identifier formed from the
adopter-owned `configuration.prompt_identity.namespace` and a zero-padded
positive decimal sequence whose width is
`configuration.prompt_identity.sequence_width`.

The framework does not infer a namespace from HugePlanning, Dopis, repository
history, or framework history. Each adopter supplies the value explicitly in
its configuration instance. Changing that value is consumer-owned semantic
change and is outside framework authority.

## Compatibility

Version `0.1.0-rc.10` uses framework contract `2.0.0`, consumer-lock schema
`2.0.0`, and consumer-configuration schema `1.0.0`, unchanged from
`0.1.0-rc.2`. It preserves the optional capability-composition contract/schema
`1.0.0`, the bounded operational delegation authority model, the bounded
replacement-execution lifecycle semantics, and the existing WPDC
contract/adoption/machine versions `1.0.0`.

The scoped release-payload identity mechanism does not itself add an
adopter-owned value. The current consumer-lock schema `2.0.0` remains sufficient
while the adopter identity tuple stays
`(repository, version, commit_sha, release_manifest_sha256)` and no new
consumer-owned identity obligation is introduced.

rc.6 added Work Packet Design & Dependency Closure (WPDC) as an optional reusable
L2 capability. WPDC contract version `1.0.0` and adoption contract version
`1.0.0` define explicit outcomes, completion conditions, prerequisite relations
(`REACH`, `VALIDATE`, `COMPLETE`), transitive closure, and the resolution set
`IN_PACKET`, `PREEXISTING_SATISFIED`, `BOUND_EXTERNAL_SATISFIED`, and
`UNRESOLVED`. `UNRESOLVED` may produce `VALID_BUT_BLOCKED`; hidden or
contradictorily excluded required prerequisites remain invalid. Direct
adopter-owned satisfaction is distinct from separately bound external
satisfaction, and immutable repository identity never proves mutable state by
itself.

The WPDC machine projection uses
`contracts/work-packet-capability-binding.schema.json` and
`contracts/work-packet-manifest.schema.json`, both schema version `1.0.0`, with
dedicated deterministic validator `tools/validate_work_packet.py`. The validator
checks represented graph/reference integrity, resolution/evidence and currentness
bindings, cycles, exclusion contradictions, validation coverage, required
authority/control declarations, and derives WPDC packet dispositions. It does
not infer undeclared semantic dependencies and does not grant execution,
mutation, merge, release, publication, or acceptance authority.

WPDC is absent unless explicitly adopted by the consumer. Its reserved optional
discovery key is
`configuration.capabilities.work_packet_design.binding_path`. A consumer that
does not adopt WPDC requires no WPDC configuration migration. A consumer that
does adopt WPDC must provide a supported exact adoption binding and conforming
work-packet projection; framework availability alone does not activate the
capability or retroactively re-evaluate historical packets.

### Hierarchical Work Graph in rc.10

rc.10 adds Hierarchical Work Graph (HWG) as an optional reusable L2 capability.
HWG contract version `1.0.0`, adoption contract version `1.0.0`, bundle schema
version `1.0.0`, and graph schema version `1.0.0` define:

- finite ordered work-hierarchy profiles;
- sibling-only DAG dependencies;
- exact reciprocal parent/child graph expansion;
- progressive/JIT expansion;
- exact graph and source lineage;
- structural completion eligibility distinct from acceptance;
- explicit separation of graph validity from authority and concurrent safety.

HWG is absent unless explicitly adopted through:

`configuration.capabilities.hierarchical_work_graph.bundle_path`

A consumer that leaves this key absent requires no HWG bundle and remains a
conforming consumer. If the key is present, the selected adopter-owned bundle
must resolve inside the consumer repository and pass
`tools/validate_hierarchical_work_graph.py` against the normative schemas.

The HWG validator proves represented structural integrity only. It does not
infer undeclared dependencies, prove semantic boundary sufficiency, grant
execution authority, or infer that missing dependency edges make work safe to
run concurrently.

For a software adopter the profile may be:

```text
PRODUCT_OUTCOME
  -> WORK_PACKET
    -> EXECUTION_UNIT
```

These level labels are adopter-profile semantics, not universal GG ontology.
The capability does not assume one product outcome equals one work packet. When
an executable child graph depends materially on current repository/runtime
context, the execution expansion is produced or revalidated under the
designated execution-decomposition contract; in the current AI Software Factory
software profile, AEA D1/D2 is that producer for `WORK_PACKET -> EXECUTION_UNIT`.

The current `framework-lock.json` remains a General Governance lock only. A
consumer that composes additional independently governed systems uses the
separate adopter-owned capability-stack contract. That stack pins exact
component commits and preserves each component's own authority/conformance
boundary; General Governance conformance does not imply CWG, AET, AO, AEA, or
other capability conformance.

Schema `contracts/consumer-lock-v1.schema.json` is retained only so a controlled
upgrade can validate a prior `0.1.0-rc.1` lock. It is not accepted as a current
lock by the current validator.

Optional capabilities are absent unless explicitly bound by the adopter. A
project remains responsible for its own project-specific semantics; framework
conformance is not a project semantic review.

## Controlled upgrade

An upgrade is an explicit `old lock -> configuration migration -> evaluation ->
new lock` transition. The consumer records it in `framework-upgrade.json`,
including both immutable identities and a passing conformance result. The
validator accepts schema-1.0 previous locks for this transition but requires a
schema-2.0 current lock. It rejects a no-op, floating, unsupported,
unverifiable, or configuration-incomplete transition. Consumers never follow a
moving branch automatically.

See `docs/upgrades/0.1.0-rc.1-to-0.1.0-rc.2.md` for adopter #1 and adopter #2
migration requirements. Every later release transition requires a new immutable
GG lock identity even when compatibility schemas remain unchanged.

The rc.9 -> rc.10 transition requires no HWG configuration migration when HWG
remains unadopted. An adopter enabling HWG supplies its optional bundle path and
project-owned hierarchy artifacts as an explicit adopter change.

## Ownership boundary

Framework-owned surfaces are L0, the L1 configuration contract, selected L2
modules if separately released, reusable L6 helpers, and generic contracts.
Consumer-owned surfaces are project-specific projections, evidence/history,
configuration values, project state, capability-stack bindings, and
provider-specific runtime bindings. Consumers reference framework normative
semantics through their lock; they must not copy or override them under
framework-owned paths.

General Governance project-operational evidence may be referenced by an adopter
using an exact GG commit/artifact identity independently of the adopter's
framework lock. Such a reference is evidence only: it does not upgrade the
framework lock and transfers no execution, mutation, acceptance, merge, release,
deployment, or normative authority.
