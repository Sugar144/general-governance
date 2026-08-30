# Hierarchical Work Graph Architecture

Status: `NON_NORMATIVE_CANDIDATE_FOR_EMPIRICAL_ADOPTION`

Candidate id: `GG-HWG-ARCH-001`

This artifact is General Governance design-process custody under `governance/**`. It is **not** current reusable framework behavior and is intentionally outside the current release payload. If empirical adoption supports it, a later separately governed release block may promote accepted semantics into release-included framework/docs/contracts/tools surfaces with a new immutable release identity.

## Purpose

Hierarchical Work Graph (HWG) is a prospective optional General Governance L2 capability for representing bounded work as a hierarchy of directed acyclic graphs without collapsing product outcomes, implementation packets, and executable units into one flat task list.

HWG is project-type-neutral. A software adopter may profile levels as vertical slices/outcomes, work packets, and execution leaves; another adopter may use different domain names.

HWG governs **structure and lineage**. It does not implement work, schedule workers, select providers, decide concurrent-effect compatibility, or grant authority.

## Motivation

A project may know useful high-level dependency structure before lower-level executable work can be safely decomposed. Materializing every executable unit up front can make downstream decomposition stale because repository or operational context changes as predecessor work completes.

HWG therefore supports progressive expansion:

```text
higher-level work graph
        ↓
selected node
        ↓ expansion
child work graph
        ↓
selected child node
        ↓ later/JIT expansion
lower-level graph
```

The hierarchy preserves the semantic level at which each dependency belongs while allowing a scheduler or other consumer to derive a current execution frontier from materialized descendants.

## Ownership and layering

HWG is intended to be owned by General Governance as reusable L2 work-governance semantics if later accepted and released.

- General Governance would own the generic meaning of graph, node, dependency, parent/child expansion, completion eligibility, and structural validity.
- An adopter owns its concrete graph instances, project-specific node kinds/profile, source artifacts, acceptance semantics, state, authority and evidence.
- WPDC remains the reusable capability for semantic prerequisite closure inside a work packet or equivalent bounded work unit.
- Agent Execution Architecture (AEA) may act as a specialized expansion producer for software execution graphs. AEA does not become the normative owner of the generic hierarchy.
- Agent Orchestrator (AO) may consume admitted graph projections for scheduling. AO does not become the normative owner of HWG semantics.
- Concurrent Repository Work Governance (CWG) remains authoritative for specialized concurrent-effect compatibility/admission where adopted. Lack of a HWG dependency edge never proves that two mutations are concurrently safe.
- AI Execution Telemetry (AET) may provide execution evidence but creates no HWG authority or completion claim by itself.

## Non-goals

HWG does not own or redefine:

- business discovery;
- requirements derivation or acceptance;
- use-case modelling;
- story/backlog semantics;
- product architecture;
- technical architecture;
- WPDC prerequisite semantics;
- provider/runtime selection;
- execution scheduling algorithms;
- concurrency compatibility;
- repository locks/leases/fencing;
- Owner authority;
- merge, release, deployment or product acceptance.

Governance of the upstream `Discovery → Requirements → Use Cases → Stories → Product Outcomes` refinement chain is a separate future General Governance concern and is deliberately outside this bounded candidate.

## Core model

### Work graph

A `WorkGraph` is a directed acyclic graph of sibling work nodes that share one semantic level/profile.

Every graph declares:

- stable graph identity;
- adopter-defined level/profile identity;
- optional parent binding;
- immutable or otherwise explicitly current source context sufficient for the graph claim;
- one or more work nodes.

### Work node

A `WorkNode` is one bounded item at the graph's semantic level. It declares:

- stable node identity;
- source/provenance reference owned by the adopter;
- dependencies on sibling nodes in the same graph;
- expansion state;
- optional child-graph binding when expansion is materialized.

A node is not necessarily executable. Higher-level nodes normally represent outcomes or bounded work whose implementation may later be expanded.

### Dependency

A HWG dependency is an ordering/availability relationship between sibling nodes in the same graph:

```text
dependent node → prerequisite sibling node
```

It means the dependent node's declared work boundary cannot be considered dependency-ready until its prerequisite sibling has reached the adopter-defined required completion state.

A dependency edge is **not**:

- proof of authority;
- proof of execution readiness;
- proof of concurrent incompatibility;
- proof that an absent edge means concurrency is safe;
- a substitute for WPDC semantic prerequisite closure.

### Parent binding

A child graph binds to exactly one parent node in exactly one parent graph.

Conceptually:

```text
ParentGraph / ParentNode
        ↓ expands to
ChildGraph
```

The child graph may refine how the parent outcome/work boundary will be produced, but it must not silently broaden or replace that parent boundary.

### Expansion state

Minimum states:

- `NOT_MATERIALIZED` — no child graph currently exists;
- `MATERIALIZED` — a child graph is bound by exact identity;
- `SUPERSEDED` — a previously materialized expansion is retained as history but is not current.

A future runtime may need richer transient states such as `EXPANDING`, but transient scheduler/runtime state is outside the normative minimum.

### Completion eligibility

Child completion may make a parent **completion-eligible**. It does not automatically make the parent accepted, integrated, released, deployed or operationally ready.

HWG therefore distinguishes:

```text
child graph structurally/completion closed
        ↓
parent completion eligible
        ≠
parent accepted
```

The adopter's own completion/acceptance authority remains controlling.

## Candidate invariants

These are design candidates only until a later GG release promotes them into normative release-included semantics.

### HWG-001 — Acyclic sibling graph

Every `WorkGraph` should be acyclic. A dependency cycle is invalid.

### HWG-002 — Same-level dependency

A HWG dependency edge should reference a sibling node in the same graph. Arbitrary dependency edges directly between different hierarchy levels should be invalid.

### HWG-003 — Exact parent

Every materialized child graph should bind to exactly one parent `(graph_id, node_id)` pair, and that parent node should bind back to the child graph identity.

### HWG-004 — Single current expansion

A parent node should not have more than one current `MATERIALIZED` child graph for the same expansion slot/profile. Alternative/historical expansions require explicit supersession/history rather than ambiguous current children.

### HWG-005 — Boundary preservation

Expanding a node should refine the parent work/outcome boundary and should not silently redefine or broaden it. Semantic verification remains a review responsibility unless a future adopter-specific contract can prove it deterministically.

### HWG-006 — No synthetic authority

Graph validity, dependency readiness, expansion materialization and parent completion eligibility grant zero execution, mutation, merge, release, deployment, acceptance or Owner authority.

### HWG-007 — No synthetic concurrency

Absence of a dependency edge must not be interpreted as proof that two nodes or descendants may safely execute concurrent effects. Concurrent-effect compatibility belongs to the applicable concurrency-governance mechanism such as CWG.

### HWG-008 — Progressive expansion

A graph may be partially expanded. A node with `NOT_MATERIALIZED` expansion remains a valid higher-level planning node when no governing rule requires the child graph yet.

### HWG-009 — Current-context execution expansion

When an expansion produces executable units whose correctness depends materially on mutable repository/runtime context, the expansion should be produced or revalidated against the current context required by the applicable execution contract rather than frozen prematurely from an obsolete baseline.

For the current software Factory profile, AEA D1/D2 is the intended JIT producer of `work packet → executable leaf DAG` expansion.

### HWG-010 — Completion does not equal acceptance

A parent may become completion-eligible only after the required child graph completion conditions hold. Completion eligibility must not be represented as project/product acceptance unless the adopter's separate acceptance authority has resolved it.

### HWG-011 — Source traceability

Every graph and node should carry sufficient adopter-owned source/provenance identity to explain where the represented work boundary came from. HWG does not infer source semantics from labels alone.

### HWG-012 — No forced one-to-one decomposition

HWG must not assume one parent node maps to exactly one child node. A parent may expand to zero current children (`NOT_MATERIALIZED`), one child, or multiple child nodes. In particular, a software vertical slice must not be assumed to equal one work packet.

## Relationship to WPDC

HWG and WPDC answer different questions:

```text
HWG
What work hierarchy/topology exists?
Which sibling work depends on which?
Which nodes have been expanded?

WPDC
For this bounded work packet, are all required prerequisites
represented and dependency-closed strongly enough to claim completion?
```

A future software profile may require every execution-eligible work-packet node in HWG to reference a valid WPDC packet disposition. That binding is an adopter/profile concern, not an implication of HWG itself.

## Software Factory profile

The first intended empirical profile is:

```text
Level 1: PRODUCT_OUTCOME
    Dopis projection: vertical slice

Level 2: WORK_PACKET
    Dopis projection: WPDC-governed packet(s)

Level 3: EXECUTION_UNIT
    producer: AEA D1/D2 leaf DAG
```

This is a profile, not the generic ontology of HWG.

For Dopis specifically:

- `docs/planning/DOPIS_VERTICAL_SLICES.json` already owns the accepted Level-1 outcome identities and hard dependencies;
- HWG should reference that truth rather than become a competing product backlog;
- `VS-ORDERING-001` may bind a child work-packet graph containing the current `DOPIS-WP-VS-ORDERING-001-005` packet;
- other vertical slices may remain `NOT_MATERIALIZED` at the WP level until packetization is actually performed;
- the successful AEA D1/D2 result for the current ordering packet may later be bound as the Level-3 execution expansion without re-running D1/D2 solely to satisfy HWG packaging.

## Runtime projection boundary

A scheduler may derive a flat frontier from the currently materialized hierarchy, but that projection is runtime state, not a replacement for the hierarchy.

Conceptually:

```text
HWG hierarchy
    ↓ structural/dependency eligibility
candidate frontier
    ↓ authority / WPDC / execution admission
admitted frontier
    ↓ CWG compatibility where concurrent effects are possible
concurrently dispatchable set
```

The scheduler should not feed transient `READY/RUNNING/FAILED` state back into the future normative HWG contract unless a later accepted lifecycle extension explicitly requires it.

## Candidate adoption path

1. review these generic HWG semantics;
2. create one bounded, explicitly non-normative Dopis projection using existing vertical-slice truth and current ordering WP evidence;
3. verify that the model does not force duplicate truth or stale leaf decomposition;
4. only then decide the minimum machine schema/validator and new GG release/adoption surface required for normative activation;
5. leave scheduler/CWG runtime wiring for a separately justified phase.

This candidate grants no Dopis implementation authority and does not alter the already granted `VS-ORDERING-001` authority or successful D1/D2 result.
