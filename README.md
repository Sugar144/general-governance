# General Governance Framework

Authoritative repository for reusable GOV-GEN framework releases and immutable
release candidates.

The framework owns reusable L0 semantics, the L1 configuration contract,
selected optional L2 capability contracts when separately released, and
selected generic L6 helpers. A consumer owns its L3 projections, L5 evidence,
configuration values, state, and provider-specific bindings.

Current prospective correction candidate: `0.1.0-rc.6`. It preserves the rc.2
framework/configuration contracts, the rc.3 optional adopter-owned capability
composition contract, the rc.4 bounded operational delegation authority model,
and the rc.5 bounded replacement-execution lifecycle semantics. It adds the
optional Work Packet Design & Dependency Closure (WPDC) L2 capability: explicit
transitive prerequisite closure, honest blocked states, exact evidence/currentness
bindings, dedicated machine contracts and deterministic validation, while
preserving the separation between dependency closure and execution authority.

See `docs/consumer-contract.md` for immutable pinning, conformance, controlled
upgrades, capability composition, and optional WPDC adoption.
