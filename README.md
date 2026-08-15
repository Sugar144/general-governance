# General Governance Framework

Authoritative repository for reusable GOV-GEN framework releases and immutable
release candidates.

The framework owns reusable L0 semantics, the L1 configuration contract, and
selected generic L6 helpers. A consumer owns its L3 projections, L5 evidence,
configuration values, state, and provider-specific bindings.

Current prospective correction candidate: `0.1.0-rc.3`. It preserves the rc.2
framework/configuration contracts and adds an optional adopter-owned capability
composition contract for independently governed systems such as CWG and AET.

See `docs/consumer-contract.md` for immutable pinning, conformance, controlled
upgrades, and capability composition.
