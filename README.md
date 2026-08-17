# General Governance Framework

Authoritative repository for reusable GOV-GEN framework releases and immutable
release candidates.

The framework owns reusable L0 semantics, the L1 configuration contract, and
selected generic L6 helpers. A consumer owns its L3 projections, L5 evidence,
configuration values, state, and provider-specific bindings.

Current prospective correction candidate: `0.1.0-rc.4`. It preserves the rc.2
framework/configuration contracts and the rc.3 optional adopter-owned capability
composition contract, and adds a bounded operational delegation authority
model to the Project Operating Contract: distinct effect does not by itself
require a separate Project Owner decision, and a finite Owner grant may
prospectively cover several routine effects of one bounded work package,
fail-closed and subject to identity/currentness fences and mandatory
escalation triggers.

See `docs/consumer-contract.md` for immutable pinning, conformance, controlled
upgrades, and capability composition.
