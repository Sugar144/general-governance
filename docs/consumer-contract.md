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

## Repository revision identity and release payload identity

The exact Git `commit_sha` binds the complete selected repository revision.
Operational/evolution evidence is therefore never unbound merely because it is
outside a prospective framework payload digest.

Historical releases through `0.1.0-rc.7` use the legacy complete-tracked-files
content identity: every tracked path except `release-manifest.json` contributes
to `content_sha256`.

A successor release may declare manifest schema `1.4.0` with
`content_identity.method = SCOPED_TRACKED_FILES_V1`. Under that method,
`content_sha256` binds the classified **Framework Release Payload** while the
exact Git commit still binds the complete repository tree. Classification is
fail-closed: any tracked path not explicitly recognized as operational is
`RELEASE_INCLUDED`.

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

Version `0.1.0-rc.7` uses framework contract `2.0.0`, consumer-lock schema
`2.0.0`, and consumer-configuration schema `1.0.0`, unchanged from
`0.1.0-rc.2`. It preserves the `0.1.0-rc.3` optional capability-composition
contract/schema `1.0.0`, the `0.1.0-rc.4` bounded operational delegation
authority model, and the `0.1.0-rc.5` bounded replacement-execution lifecycle
semantics unchanged.

The scoped release-payload identity mechanism does not itself add an
adopter-owned value. The current consumer-lock schema `2.0.0` remains sufficient
only while the adopter identity tuple stays
`(repository, version, commit_sha, release_manifest_sha256)` and no new
consumer-owned obligation is introduced. If implementation or packaging proves
otherwise, compatibility review is required before changing schemas or
compatibility declarations.

rc.6 adds Work Packet Design & Dependency Closure (WPDC) as an optional reusable
L2 capability. WPDC contract version `1.0.0` and adoption contract version
`1.0.0` define explicit outcomes, completion conditions, prerequisite relations
(`REACH`, `VALIDATE`, `COMPLETE`), transitive closure, and the resolution set
`IN_PACKET`, `PREEXISTING_SATISFIED`, `BOUND_EXTERNAL_SATISFIED`, and
`UNRESOLVED`. `UNRESOLVED` may produce `VALID_BUT_BLOCKED`; hidden or
contradictorily excluded required prerequisites remain invalid. Direct
adopter-owned satisfaction is distinct from separately bound external
satisfaction, and immutable repository identity never proves mutable state by
itself.

The rc.6 machine projection uses `contracts/work-packet-capability-binding.schema.json`
and `contracts/work-packet-manifest.schema.json`, both schema version `1.0.0`,
with dedicated deterministic validator `tools/validate_work_packet.py`. The
validator checks represented graph/reference integrity, resolution/evidence and
currentness bindings, cycles, exclusion contradictions, validation coverage,
required authority/control declarations, and derives WPDC packet dispositions.
It does not infer undeclared semantic dependencies and does not grant execution,
mutation, merge, release, publication, or acceptance authority.

WPDC is absent unless explicitly adopted by the consumer. The reserved optional
discovery key is `configuration.capabilities.work_packet_design.binding_path`.
A consumer that does not adopt WPDC requires no configuration migration from
rc.5. A consumer that does adopt WPDC must provide a supported exact adoption
binding and conforming work-packet projection; framework availability alone does
not activate the capability or retroactively re-evaluate historical packets.

The current `framework-lock.json` remains a General Governance lock only. A
consumer that composes additional independently governed systems uses the
separate adopter-owned capability-stack contract. That stack pins exact
component commits and preserves each component's own authority/conformance
boundary; General Governance conformance does not imply CWG, AET, or other
capability conformance.

Schema `contracts/consumer-lock-v1.schema.json` is retained only so a controlled
upgrade can validate a prior `0.1.0-rc.1` lock. It is not accepted as a current
lock by the current validator.

Optional capabilities are absent unless explicitly bound by the adopter. A
project remains responsible for its own L3/L5 semantics; framework conformance
is not a project semantic review.

## Controlled upgrade

An upgrade is an explicit `old lock -> configuration migration -> evaluation ->
new lock` transition. The consumer records it in `framework-upgrade.json`,
including both immutable identities and a passing conformance result. The
validator accepts schema-1.0 previous locks for this transition but requires a
schema-2.0 current lock. It rejects a no-op, floating, unsupported,
unverifiable, or configuration-incomplete transition. Consumers never follow a
moving branch automatically.

See `docs/upgrades/0.1.0-rc.1-to-0.1.0-rc.2.md` for adopter #1 and adopter #2
migration requirements. Moving from rc.2 to rc.3, rc.3 to rc.4, rc.4 to rc.5,
or rc.5 to rc.6 requires a new immutable GG lock identity. The rc.5 -> rc.6
transition requires no configuration migration when WPDC remains unadopted; an
adopter enabling WPDC supplies its optional binding as a separate adopter-owned
change.

## Ownership boundary

Framework-owned surfaces are L0, the L1 configuration contract, selected L2
modules if separately released, reusable L6 helpers, and generic contracts.
Consumer-owned surfaces are L3 projections, L5 evidence/history, configuration
values, project state, capability-stack bindings, and provider-specific runtime
bindings. Consumers reference framework normative semantics through their lock;
they must not copy or override them under framework-owned paths.

General Governance project-operational evidence may be referenced by an adopter
using an exact GG commit/artifact identity independently of the adopter's
framework lock. Such a reference is evidence only: it does not upgrade the
framework lock and transfers no execution, mutation, acceptance, merge, release,
deployment, or normative authority.
