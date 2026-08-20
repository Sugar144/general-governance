# General Governance Framework

Authoritative repository for reusable GOV-GEN framework releases and immutable
release candidates.

The framework owns reusable L0 semantics, the L1 configuration contract,
selected optional L2 capability contracts when separately released, and
selected generic L6 helpers. A consumer owns its L3 projections, L5 evidence,
configuration values, state, and provider-specific bindings.

Current prospective correction candidate: `0.1.0-rc.5`. It preserves the rc.2
framework/configuration contracts, the rc.3 optional adopter-owned capability
composition contract, and the rc.4 bounded operational delegation authority
model. It adds bounded replacement-execution lifecycle semantics to the Project
Operating Contract: terminal failure creates no authority; replacement is a
distinct, finite, explicitly authorized execution with immutable lineage,
effect-state/currentness gates, and no recursive authority creation.

See `docs/consumer-contract.md` for immutable pinning, conformance, controlled
upgrades, and capability composition.
