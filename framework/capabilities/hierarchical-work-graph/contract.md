---
document_id: GOV-L2-HIERARCHICAL-WORK-GRAPH-001
capability_id: hierarchical-work-graph
version: 1.0.0
status: NORMATIVE_CONTRACT_PENDING_RELEASE_INTEGRATION
layer: L2
architecture_source: governance/design/hierarchical-work-graph/GG_HWG_ARCHITECTURE_CANDIDATE_001.md
---

# Hierarchical Work Graph — Normative Capability Contract

## 1. Purpose and authority

Hierarchical Work Graph (HWG) is an optional reusable General Governance L2 capability for representing bounded work as a hierarchy of directed acyclic graphs without collapsing product outcomes, work packets and executable units into one flat task list.

HWG governs reusable **work structure, dependency topology, source lineage and hierarchical expansion**. It does not implement work, schedule workers, select execution providers, determine concurrent-effect compatibility, or grant project authority.

The terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` and `MAY` are normative only for a consumer that explicitly adopts HWG under the companion adoption contract.

## 2. Project-type neutrality

HWG does not define universal software-specific node names. An adopter defines an ordered finite **profile** of semantic levels.

A software adopter may use:

```text
PRODUCT_OUTCOME
  -> WORK_PACKET
    -> EXECUTION_UNIT
```

Another project type may use different level names while preserving the same HWG invariants.

## 3. Core model

### 3.1 HierarchicalWorkGraphBundle

A `HierarchicalWorkGraphBundle` is the exact current structural projection of one hierarchy. It declares:

- a stable bundle identity;
- one profile identity;
- an ordered contiguous list of semantic levels;
- one exact root graph reference;
- the complete exact set of graph files in the current bundle;
- fail-closed safety declarations that graph validity grants no authority and missing dependency edges prove no concurrent safety.

The bundle is logically a graph of graphs. Child graphs are separate exact artifacts referenced from parent nodes; HWG does not require one recursively nested mega-document.

### 3.2 WorkGraph

A `WorkGraph` is a directed acyclic graph of sibling `WorkNode` objects at exactly one profile level.

Every graph declares:

- stable `graph_id`;
- the bundle profile identity;
- exactly one `level_id`;
- either no parent binding for the root graph or exactly one parent `(graph_id, node_id)` binding;
- one or more exact source/provenance references;
- one or more sibling nodes.

### 3.3 WorkNode

A `WorkNode` is one bounded item at the graph's semantic level. It declares:

- stable `node_id`;
- one or more graph-local source-reference identities;
- dependencies on sibling nodes in the same graph;
- current expansion state.

A node is not necessarily executable.

### 3.4 Dependency

A dependency edge is directed from a dependent node to a prerequisite sibling node.

It means the dependent node cannot be considered dependency-ready until the adopter's governing completion semantics for the prerequisite are satisfied.

A dependency edge does **not** by itself prove:

- execution authority;
- mutation authority;
- completion or acceptance;
- concurrent incompatibility.

Absence of a dependency edge does **not** prove concurrent compatibility.

### 3.5 Expansion

A node has exactly one current expansion state in HWG v1:

- `NOT_MATERIALIZED` — no current child graph is bound;
- `MATERIALIZED` — exactly one current child graph is bound by identity.

Historical or superseded expansions remain adopter-owned history/evidence and are not represented as multiple competing current children inside one active HWG bundle.

A materialized expansion means:

```text
parent WorkNode
    -> exactly one child WorkGraph
```

The child graph refines the parent boundary; it does not replace the parent identity or silently broaden its governed outcome/work boundary.

### 3.6 Source reference

Every graph and node MUST be traceable to adopter-owned source/provenance identity.

HWG v1 supports exact source identities of these kinds:

- `SHA256`;
- `GIT_BLOB_SHA1`;
- `OPAQUE_EXACT`.

A machine validator may verify file-backed SHA-256 and Git-blob identities when an adopter source root is supplied. `OPAQUE_EXACT` preserves an exact external or non-file identity but does not cause the validator to invent a resolver.

## 4. Normative invariants

### HWG-001 — Acyclic sibling graph

Every `WorkGraph` MUST be acyclic.

### HWG-002 — Same-level dependency

Every dependency edge MUST reference a sibling node in the same graph. Arbitrary direct cross-level or cross-graph dependency edges are invalid.

Interaction between hierarchy levels occurs through explicit parent/child expansion boundaries.

### HWG-003 — Exact root

The bundle MUST identify exactly one root graph. The root graph MUST use the first profile level and MUST have `parent_binding = null`.

### HWG-004 — Exact reciprocal parent/child binding

Every non-root graph MUST be referenced by exactly one `MATERIALIZED` parent node. Its `parent_binding` MUST exactly match that parent graph/node pair.

### HWG-005 — Single current parent

One child graph MUST NOT be claimed by more than one current parent node.

### HWG-006 — Adjacent-level expansion

A materialized expansion MUST advance exactly one level in the ordered profile. A parent MUST NOT skip directly over an intermediate declared profile level.

### HWG-007 — Reachable hierarchy

Every graph in the active bundle MUST be reachable from the root by following materialized expansions. Orphan graphs are invalid.

### HWG-008 — Exact graph-file identity

Every graph file referenced by the bundle MUST be bound by SHA-256. The bytes loaded by a validator MUST match that digest.

### HWG-009 — Source traceability

Every node MUST reference at least one graph-local source identity and MUST NOT reference an undeclared source identity.

### HWG-010 — Progressive expansion

A hierarchy MAY be partially expanded. `NOT_MATERIALIZED` is a valid planning state when no governing rule requires the child graph yet.

### HWG-011 — No forced one-to-one decomposition

HWG MUST NOT assume one parent node maps to one child node. A parent node may remain unexpanded or may expand to a child graph containing one or many nodes.

In a software profile, a vertical slice MUST NOT be assumed to equal one work packet.

### HWG-012 — Current-context executable expansion

When an expansion produces executable units whose correctness depends materially on mutable repository/runtime context, the expansion MUST be produced or revalidated against the current context required by the designated execution-decomposition contract rather than reused silently from an obsolete baseline.

For the current AI Software Factory software profile, AEA D1/D2 is the designated producer of `WORK_PACKET -> EXECUTION_UNIT` expansion.

### HWG-013 — Completion eligibility is not acceptance

Completion of required child work may make a parent completion-eligible under adopter semantics. HWG structure MUST NOT convert that condition into project/product acceptance, release, deployment or operational readiness.

### HWG-014 — No synthetic authority

Graph validity, dependency topology, expansion materialization and completion eligibility grant zero implementation, provider execution, mutation, merge, release, deployment, acceptance or Owner authority.

### HWG-015 — No synthetic concurrency

Absence of a dependency edge MUST NOT be interpreted as proof that nodes or descendants may safely execute concurrent effects. Concurrent-effect compatibility remains governed by the applicable concurrency mechanism, such as CWG when adopted.

### HWG-016 — Boundary preservation

An expansion MUST refine the parent work/outcome boundary and MUST NOT silently broaden or redefine it. Deterministic tooling validates represented structure; semantic boundary preservation remains a review/governance responsibility unless an adopter-specific machine contract can prove it.

## 5. Relationship to WPDC

HWG and Work Packet Design & Dependency Closure (WPDC) are sibling L2 capabilities with different responsibilities.

```text
HWG
- hierarchy/topology
- sibling dependencies
- parent/child expansion
- exact structural lineage

WPDC
- prerequisites inside one bounded packet
- REACH / VALIDATE / COMPLETE closure
- prerequisite resolution and evidence
- dependency-closed packet disposition
```

A software adopter MAY require a `WORK_PACKET` node to reference a valid WPDC-governed packet before it becomes eligible for execution expansion. That policy belongs to the adopter/profile and does not make HWG a substitute for WPDC.

## 6. Relationship to execution and concurrency systems

HWG owns reusable structural semantics only.

- AEA may produce an exact execution-unit child graph projection from an admitted decomposition.
- Agent Orchestrator may consume HWG plus separately governed lifecycle/authority state to derive a candidate scheduling frontier.
- CWG may determine whether simultaneously eligible effectful work is `EXCLUSIVE_EFFECT`, `ORDERED_EFFECT`, or `SHARED_COMPATIBLE_EFFECT` under its own contract.
- AET may provide execution evidence but does not create HWG validity or authority.

## 7. Machine-validation boundary

A conforming deterministic HWG validator MUST be able to validate, from represented data:

- bundle and graph schemas;
- unique profile levels and contiguous ordering;
- exact graph-file digests;
- unique graph/node/source identities;
- sibling-only dependency references;
- dependency acyclicity;
- root identity and level;
- reciprocal parent/child bindings;
- one-current-parent rule;
- adjacent-level expansion;
- hierarchy reachability;
- declared source-reference integrity;
- supported file-backed source identities when a source root is supplied.

It MUST NOT claim to prove semantic boundary sufficiency, product acceptance, execution authority, concurrent safety, or undeclared missing dependencies.

## 8. Disposition

A machine-valid active HWG bundle has structural disposition:

`VALID_HIERARCHICAL_WORK_GRAPH`

Any mandatory schema, identity, graph, dependency, hierarchy or source-binding defect yields a fail-closed invalid result.

This disposition is structural only and grants no authority.