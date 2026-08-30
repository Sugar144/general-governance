# Hierarchical Work Graph Architecture

Hierarchical Work Graph (HWG) is an optional General Governance L2 capability for representing a hierarchy of DAGs without flattening unlike semantic work levels.

## Shape

```text
WorkGraph(level 1)
  └─ WorkNode
       └─ child WorkGraph(level 2)
            └─ WorkNode
                 └─ child WorkGraph(level 3)
```

The graph-of-graphs relationship is logical. Each WorkGraph is a separate exact JSON artifact and the bundle binds every graph file by SHA-256.

A software adopter may profile the levels as:

```text
PRODUCT_OUTCOME
  ↓
WORK_PACKET
  ↓
EXECUTION_UNIT
```

The generic HWG ontology does not depend on those software labels.

## Why hierarchical instead of one global flat DAG

Dependencies have different meanings at different levels. Product-outcome dependency is not the same thing as a work-packet dependency or an execution-leaf dependency. HWG preserves those boundaries and allows lower levels to be materialized progressively against current context.

This permits global planning before executable decomposition while avoiding stale up-front leaf generation.

## Progressive/JIT expansion

A node may remain `NOT_MATERIALIZED` until its child graph is needed. When executable decomposition depends on mutable repository/runtime context, the child execution graph is produced or revalidated against the applicable current baseline.

For the AI Software Factory software profile, AEA D1/D2 is the designated producer for `WORK_PACKET → EXECUTION_UNIT` expansion.

## Dependency boundary

Dependency edges are only between sibling nodes in one WorkGraph. Cross-level interaction is represented through parent/child graph expansion, not arbitrary edges spanning the hierarchy.

This prevents hard-to-reason chains such as an execution leaf directly depending on an unrelated product-level node.

## Current projection versus history

HWG v1 models one current active expansion per node:

- `NOT_MATERIALIZED`;
- `MATERIALIZED`.

Superseded graphs remain adopter-owned history/evidence rather than competing current children inside one active bundle.

## Completion, scheduling and authority

HWG is structural governance.

```text
HWG structure/dependencies
        ↓
candidate structural frontier
        ↓
project authority + lifecycle + WPDC/execution admission
        ↓
AO scheduling
        ↓
CWG concurrent-effect admission when needed
```

HWG deliberately does not own runtime `READY/RUNNING/FAILED` state, provider selection or concurrent compatibility.

Missing a dependency edge never proves parallel safety.

## Relationship to WPDC

HWG owns hierarchy/topology; WPDC owns prerequisite closure inside a bounded work packet.

A software adopter can therefore represent:

```text
Vertical Slice / Product Outcome
      ↓ HWG expansion
one or more Work Packets
      ↓ WPDC evaluates each packet's prerequisite closure
execution-eligible packet
      ↓ AEA D1/D2
Execution Unit DAG
```

HWG does not assume one vertical slice equals one work packet.

## First empirical adopter

Dopis is the first intended adopter. Its accepted `DOPIS_VERTICAL_SLICES.json` remains the authoritative product-outcome topology. HWG projects that topology mechanically rather than creating a second product backlog, then progressively binds real packet and admitted AEA decomposition graphs as they become available.

## Normative surfaces

- `framework/capabilities/hierarchical-work-graph/contract.md`
- `framework/capabilities/hierarchical-work-graph/adoption-contract.md`
- `contracts/hierarchical-work-graph-bundle.schema.json`
- `contracts/work-graph.schema.json`
- `tools/validate_hierarchical_work_graph.py`
