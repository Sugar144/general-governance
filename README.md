# General Governance Framework

Authoritative repository for reusable GOV-GEN framework releases and immutable
release candidates.

The framework owns reusable L0 semantics, the L1 configuration contract,
selected optional L2 capability contracts when separately released, and
selected generic L6 helpers. A consumer owns its project-specific projections,
evidence, configuration values, state, authority and provider/runtime bindings.

Current prospective release candidate: `0.1.0-rc.10`.

The release preserves the existing core governance, capability-composition and
Work Packet Design & Dependency Closure (WPDC) semantics while adding the
optional **Hierarchical Work Graph (HWG)** L2 capability.

HWG provides reusable project-type-neutral semantics for:

- finite ordered work-hierarchy profiles;
- same-level DAG dependencies;
- exact parent/child graph expansion;
- progressive/JIT expansion;
- exact graph/source lineage;
- fail-closed structural validation;
- explicit separation of graph validity from authority and concurrent safety.

For the AI Software Factory software profile this can represent:

```text
PRODUCT_OUTCOME
  -> WORK_PACKET
    -> EXECUTION_UNIT
```

without assuming one product outcome equals one packet and without forcing all
execution leaves to be generated before their current baseline exists.

HWG is optional and is activated only through the adopter-owned configuration
key `configuration.capabilities.hierarchical_work_graph.bundle_path`.

See:

- `docs/consumer-contract.md` for immutable pinning and controlled upgrades;
- `docs/architecture/work-packet-design-dependency-closure.md` for WPDC;
- `docs/architecture/hierarchical-work-graph.md` for HWG;
- `framework/capabilities/hierarchical-work-graph/contract.md` for normative HWG semantics.
