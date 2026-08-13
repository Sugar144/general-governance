# External Consumer Contract

`Sugar144/general-governance` is the authoritative identity for this framework.
A version label is descriptive only: a consumer is governed by the tuple
`(repository, version, commit_sha, release_manifest_sha256)`.  The commit and
manifest digest are immutable; `main`, `latest`, `current`, branches, and tags
without an exact commit are invalid locks.

## Delivery and lock

A consumer may acquire bytes by an archive, clone, cache, package registry, or
other reproducible transport.  Acquisition is not authority.  It must write a
`framework-lock.json` conforming to `contracts/consumer-lock.schema.json`; the
lock identifies the immutable revision that governs the consumer.

The release manifest is deterministic and carries the hash of the complete
release content set (excluding the manifest itself).  It names the framework
contract compatibility supported by that release.

## Compatibility

Compatibility is declared only for framework contracts and schemas.  Version
`0.1.0-rc.1` supports consumer-lock schema `1.0.0` and framework contract
`1.0.0`.  Optional modules/adapters must declare their own compatibility and
are absent unless explicitly locked.  A project remains responsible for its
own L3/L5 semantics; framework conformance is not a project semantic review.

## Controlled upgrade

An upgrade is an explicit `old lock -> evaluation -> new lock` transition.
The consumer records it in `framework-upgrade.json`, including both immutable
identities and a passing conformance result.  The validator rejects a no-op,
floating, unsupported, or unverifiable transition.  Consumers never follow a
moving branch automatically.

## Ownership boundary

Framework-owned surfaces are L0, the L1 configuration contract, selected L2
modules if separately released, reusable L6 helpers, and generic contracts.
Consumer-owned surfaces are L3 projections, L5 evidence/history, configuration
values, project state, and provider-specific runtime bindings.  Consumers
reference framework normative semantics through their lock; they must not copy
or override them under framework-owned paths.
