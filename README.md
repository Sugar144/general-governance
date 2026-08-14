# General Governance Framework

Authoritative repository for reusable GOV-GEN framework releases and immutable
release candidates.

The framework owns reusable L0 semantics, the L1 configuration contract, and
selected generic L6 helpers. A consumer owns its L3 projections, L5 evidence,
configuration values, state, and provider-specific bindings.

Current prospective correction candidate: `0.1.0-rc.2`. It requires an explicit
consumer-owned configuration instance and parameterizes material-prompt
identity without prescribing a project namespace.

See `docs/consumer-contract.md` for immutable pinning, conformance, and
controlled upgrades.
