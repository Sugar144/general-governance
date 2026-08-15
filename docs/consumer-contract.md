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

The release manifest is deterministic and carries the hash of the complete
release content set (excluding the manifest itself). It names the framework
contract and schema compatibility supported by that release.

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

Version `0.1.0-rc.3` uses framework contract `2.0.0`, consumer-lock schema
`2.0.0`, and consumer-configuration schema `1.0.0`, unchanged from
`0.1.0-rc.2`. It additionally publishes optional capability-composition
contract/schema `1.0.0`.

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
migration requirements. Moving from rc.2 to rc.3 requires a new immutable GG
lock identity but no configuration migration when the existing rc.2
configuration remains valid.

## Ownership boundary

Framework-owned surfaces are L0, the L1 configuration contract, selected L2
modules if separately released, reusable L6 helpers, and generic contracts.
Consumer-owned surfaces are L3 projections, L5 evidence/history, configuration
values, project state, capability-stack bindings, and provider-specific runtime
bindings. Consumers reference framework normative semantics through their lock;
they must not copy or override them under framework-owned paths.
