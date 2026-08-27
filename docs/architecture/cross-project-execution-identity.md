# Cross-Project Execution Identity Standard

Status: CANDIDATE_FOR_OWNER_REVIEW

Artifact ID: `GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001`

Candidate contract version: 1.0.0

Identity schema name: `gg.execution-identity/v1`

## Purpose

This architecture defines a provider-neutral and project-neutral identity taxonomy for semantic outcomes, implementation packets, executable configurations, historical executions, execution leaves, concrete attempts, recoveries, reviews, and material decisions.

Its purpose is to prevent identities from different conceptual layers from being treated as interchangeable and to provide a stable identity substrate for cross-project governance, evidence lineage, execution architecture, recovery, review, and future autonomous orchestration.

The core separation is:

```text
Semantic Outcome != PKT != EXEC != RUN != L != A
```

and:

```text
REC != RUN
REV != reviewed object
DEC != governed action
```

The standard is owned by General Governance. Execution architectures may materialize these semantics, and adopters may project them into project-specific artifacts, but neither an execution runtime nor an adopter owns or may silently redefine the cross-project semantics established here.

## Ownership and layering

General Governance owns:

- provider-neutral identity semantics;
- canonical identity classes;
- cross-project invariants;
- relationship semantics;
- historical compatibility rules.

Execution architectures own, subject to these semantics:

- runtime representation;
- manifests;
- identifier generation;
- serialization;
- validation;
- evidence materialization;
- execution lifecycle implementation.

Adopters own:

- project-specific execution scopes;
- semantic outcomes;
- implementation decomposition;
- concrete mappings;
- adoption timing;
- legacy bridges.

This candidate does not make Claude Agent Execution Architecture, Stakeholder Validation Portal, Dopis, or any other adopter part of General Governance. It defines only a reusable identity contract that those systems may separately adopt.

## Canonical identity classes

### Execution Scope

An `Execution Scope` is the bounded project-defined context within which local identities are issued and interpreted.

Examples include a capability, vertical, release slice, or another explicitly bounded execution context.

A scope is not itself required to use a universal GG prefix. Its identifier and kind remain adopter-owned, but both MUST be explicit in structured identity data.

### Semantic Outcome

A `Semantic Outcome` describes product, business, behavioral, or system intent: what must become true.

A Semantic Outcome MUST NOT imply an implementation decomposition and MUST NOT be treated as directly executable merely because an implementation packet happens to map one-to-one to it.

`ST` is the canonical label for the `story` subtype of Semantic Outcome:

```text
ST-01
ST-02
ST-03
```

GG does not require every Semantic Outcome to be a story. Structured consumers SHOULD therefore represent both identity and kind, for example:

```yaml
outcome:
  id: ST-01
  kind: story
```

The GG abstraction is `Semantic Outcome`; `ST` is the standard story subtype, not a synonym for every possible outcome kind.

### Implementation Packet — PKT

`PKT` identifies one bounded `Implementation Packet`.

Example:

```text
PKT-01
```

The canonical `PKT-*` namespace MUST be reserved exclusively for Implementation Packets.

It MUST NOT be reused as a generic identity for:

- execution packages;
- runs;
- review bundles;
- recovery bundles;
- evidence bundles;
- semantic outcomes;
- stories.

The word `packet` MAY still occur informally in descriptive prose, but it does not acquire `PKT` semantics unless it identifies an Implementation Packet under this contract.

### Execution Specification — EXEC

`EXEC` identifies one immutable executable realization or configuration of exactly one Implementation Packet.

Conceptually, EXEC answers:

```text
what executable definition is bound for this packet?
```

Depending on the execution architecture, an EXEC MAY bind execution-relevant elements such as:

- execution graph;
- leaves;
- contracts;
- runtime-relevant inputs;
- execution strategy;
- provider/runtime configuration;
- validation boundaries;
- execution policies;
- other material execution configuration.

Once accepted or materialized for historical execution, an EXEC MUST NOT be silently mutated in place. A material change to its execution semantics MUST produce a new EXEC identity.

Example:

```text
PKT-01
├── EXEC-001
└── EXEC-002
```

An adopter or runtime MAY define stricter rules for what constitutes a material EXEC change, provided those rules do not weaken identity immutability.

### Execution Run — RUN

`RUN` identifies one historical invocation of exactly one EXEC.

Conceptually:

```text
EXEC = what was configured to execute
RUN  = one historical invocation of that configuration
```

Therefore:

```text
EXEC != RUN
```

Example:

```text
EXEC-001
├── RUN-001
├── RUN-002
└── RUN-003
```

A RUN identity MUST NOT be reused for another historical invocation.

A consumed or completed RUN MUST remain historically immutable.

A replacement execution MUST receive a new RUN identity. Replacement, retry, recovery, and ordinary execution MUST NOT be treated as interchangeable concepts merely because they may be causally related.

### Execution Leaf — L

`L` identifies one bounded executable node within an EXEC execution graph.

Example:

```text
EXEC-001
├── L001
├── L002
└── L003
```

A leaf logically belongs to the EXEC definition. A RUN invokes the applicable leaves defined by its bound EXEC.

Therefore:

```text
RUN != L
```

### Attempt — A

`A` identifies one concrete invocation of one leaf within one run.

Every actual leaf invocation MUST have an explicit Attempt identity, including the first invocation.

Therefore, when `L003` is actually invoked:

```text
L003
└── A001
```

If another invocation occurs:

```text
L003
├── A001
└── A002
```

The first execution MUST NOT remain anonymous merely because no retry has yet occurred. This prevents the semantic identity of the first invocation from changing retrospectively when a later attempt appears.

An Attempt MUST reference exactly one RUN and exactly one L.

A leaf that never crosses its execution boundary MAY have zero attempts.

### Recovery — REC

`REC` identifies an explicit recovery intervention or recovery record.

Recovery is a lateral typed identity. It MUST NOT be treated as another name for a retry, attempt, replacement run, resumed run, or ordinary execution.

Example:

```yaml
recovery:
  id: REC-001
  target_refs:
    - RUN-003
    - L003
    - A001
```

A recovery MAY cause or authorize later execution activity, but that activity retains its own canonical identity.

Therefore:

```text
REC-001 != RUN-004
```

unless an explicit typed relation connects those separate objects.

### Review — REV

`REV` identifies one review instance over one or more governed objects or evidence surfaces.

A review MUST identify its targets through explicit references.

Example:

```yaml
review:
  id: REV-003
  target_refs:
    - EXEC-002
  result: PASS
```

Review result is an attribute, not an identity class. Prefer `REV-003` with `result: PASS`, not identifiers such as `REV-PASS-003`.

### Material Decision — DEC

`DEC` identifies one material governance or authority decision.

Examples MAY include decisions concerning:

- execution authorization;
- replacement authorization;
- recovery strategy;
- exception handling;
- adoption;
- publication;
- integration;
- policy disposition.

A DEC MAY affect multiple governed objects and MUST remain distinguishable from the execution or action it authorizes.

Example:

```yaml
decision:
  id: DEC-017
  affects:
    - RUN-004
    - REC-001
```

## Outcome-to-packet relationship

Semantic Outcomes and Implementation Packets are separate identity classes.

GG MUST NOT define the following as a mandatory parent-child identity hierarchy:

```text
ST → PKT
```

The valid relationship cardinality MAY be:

```text
1 Outcome → 1 PKT
1 Outcome → N PKTs
N Outcomes → 1 PKT
N Outcomes → N PKTs
```

when justified by the implementation decomposition.

Examples:

```text
ST-02
├── PKT-01
└── PKT-02
```

and:

```text
PKT-04
├── implements ST-05
└── implements ST-06
```

The canonical semantic relationship is therefore:

```text
Semantic Outcome ↔ PKT
```

with explicit typed references.

A system MUST NOT infer packet ownership solely from a concatenated identifier containing a story or other outcome identifier.

## Canonical relationship model

The logical model is:

```text
                    Execution Scope
                          │
             ┌────────────┴────────────┐
             │                         │
      Semantic Outcomes               PKT
             ▲                         │
             │                         │
             └── implements/covers ────┤
                                       │
                                      EXEC
                                 ┌─────┴─────┐
                                 │           │
                                L           RUN
                                 \           /
                                  \         /
                                   Attempt

REC ──targets──▶ governed execution/history objects
REV ──targets──▶ reviewable objects/evidence
DEC ──affects──▶ governed objects
```

Normative cardinalities are:

```text
Scope → 0..N Semantic Outcomes
Scope → 0..N PKTs

Semantic Outcome ↔ PKT
many-to-many permitted

PKT → 1..N EXEC over its lifecycle

EXEC → 0..N RUN
EXEC → 1..N L when leaf-based execution is used

RUN + L → 0..N A
```

`REC`, `REV`, and `DEC` use explicit typed lateral references rather than mandatory hierarchical containment.

## Local identifier grammar

Recommended canonical local identifiers are:

```text
ST-01
PKT-01
EXEC-001
RUN-001
L001
A001
REC-001
REV-001
DEC-001
```

Recommended patterns are:

```text
ST-[0-9]{2,}
PKT-[0-9]{2,}
EXEC-[0-9]{3,}
RUN-[0-9]{3,}
L[0-9]{3,}
A[0-9]{3,}
REC-[0-9]{3,}
REV-[0-9]{3,}
DEC-[0-9]{3,}
```

Projects MAY use larger numeric widths.

Once issued within an identity namespace, an identifier MUST NOT be reassigned to a different object.

## Durable identity projection

Systems MAY expose human-readable durable identifiers by combining scope and local identity.

For example, for scope:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001
```

an outcome MAY project as:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001-ST-01
```

and an implementation/execution chain MAY project as:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001-RUN-001
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001-L003
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001-RUN-001-L003-A001
```

A Semantic Outcome identity MUST NOT be inserted into the PKT durable identity as though the Outcome were necessarily its parent.

Therefore prefer:

```text
...-PKT-01
```

with structured references such as:

```yaml
outcome_refs:
  - id: ST-01
    kind: story
```

rather than:

```text
...-ST-01-PKT-01
```

## Structured identity is authoritative

Concatenated identifiers are useful projections for humans, logs, filenames, evidence artifacts, debugging, and interoperability.

They are not the authoritative relationship model.

Canonical relationships MUST be represented structurally.

The governing principle is:

> The identity string is not the data model.

A consumer MUST NOT depend solely on parsing a durable identifier to reconstruct semantic relationships that can be represented explicitly.

## Minimum structured identity envelope

Cross-project adopters claiming conformance MUST expose enough information to identify:

1. the identity schema;
2. the project;
3. the execution scope;
4. the entity type;
5. the local identity;
6. relevant relationships.

A minimal generic representation is:

```yaml
identity_schema: gg.execution-identity/v1

project_id: SVP

scope:
  id: SVP-STAGE2A-GUIDED-ANSWERING-001
  kind: vertical

entity:
  type: execution_run
  local_id: RUN-001

relations:
  packet_ref: PKT-01
  execution_ref: EXEC-001
```

Implementations MAY additionally expose a generated durable identifier.

Execution runtimes SHOULD expose the following relationship data when applicable:

```yaml
identity_schema: gg.execution-identity/v1

project_id: SVP

scope:
  id: SVP-STAGE2A-GUIDED-ANSWERING-001
  kind: vertical

packet:
  id: PKT-01
  outcome_refs:
    - id: ST-01
      kind: story

execution:
  id: EXEC-001

run:
  id: RUN-001
```

A concrete leaf invocation SHOULD additionally expose:

```yaml
leaf:
  id: L003

attempt:
  id: A001
```

This candidate defines the semantic minimum only. It does not itself create a JSON Schema, RunManifest implementation, validator, or identifier generator.

## Required invariants

Conforming implementations MUST preserve the following invariants.

### Identity separation

```text
Semantic Outcome != PKT
PKT != EXEC
EXEC != RUN
RUN != L
L != A
A != REC
REC != replacement RUN
REV != reviewed object
DEC != governed action
```

### Relationship explicitness

A many-to-many Outcome/PKT relationship MUST NOT be encoded only through identifier concatenation.

### Attempt completeness

Every actual leaf invocation MUST have an Attempt identity, including the first invocation.

### Historical immutability

Historical accepted identities MUST NOT be reassigned, renamed, or rewritten merely to comply with a newer naming standard.

### Execution immutability

A material change to an accepted or historically materialized EXEC MUST result in a new EXEC identity.

### No implicit retry/recovery equivalence

Systems MUST NOT infer:

```text
retry == recovery
replacement == recovery
replacement == retry
```

unless a separate governing policy explicitly establishes a typed relationship for the specific event.

### Typed lateral references

REC, REV, and DEC MUST identify their target or affected objects explicitly.

## Historical compatibility

Historical accepted identities are immutable historical names.

Adoption of this standard MUST NOT:

- rename historical accepted artifacts;
- rewrite accepted evidence;
- reinterpret old identifiers solely because their terminology resembles this standard;
- manufacture canonical equivalence where none has been established.

In particular, historical identities such as:

```text
Packet 01
Packet 02
Packet 03
```

remain their original accepted identities.

They MUST NOT automatically be reinterpreted as:

```text
PKT-01
PKT-02
PKT-03
```

under this standard.

## Legacy bridge

When an adopter needs to relate a historical identity to canonical identities, it MUST use an explicit non-destructive bridge.

Example:

```yaml
legacy_identity:
  namespace: SVP-STAGE2A-V1
  id: Packet 01

canonical_mapping:
  status: exact
  refs:
    - PKT-01
```

Supported mapping states SHOULD include:

```text
exact
partial
none
unknown
```

When semantics do not align exactly, a partial mapping MUST remain partial and MUST NOT be promoted to exact for tooling convenience.

Historical artifacts remain source truth for their original historical context.

## Conformance requirements

A system claiming conformance with `gg.execution-identity/v1` MUST:

1. distinguish PKT, EXEC, RUN, L, and A;
2. preserve Semantic Outcome and PKT as independent entities;
3. represent Outcome/PKT relationships explicitly;
4. issue an Attempt identity for every concrete leaf invocation;
5. treat REC, REV, and DEC as typed identities rather than aliases for execution objects;
6. preserve historical identities;
7. expose structured identity data;
8. avoid relying on concatenated strings as the sole relationship model.

A system MAY adopt the model incrementally, but MUST NOT claim full `gg.execution-identity/v1` conformance before satisfying all MUST requirements.

## AEC S6 adoption guidance

If Claude Agent Execution Architecture adopts this candidate after GG acceptance, its S6 identity model SHOULD distinguish at least:

```text
outcome_refs
packet_id
execution_id
run_id
leaf_id
attempt_id
recovery_id
review_id
decision_id
```

The intended mapping is:

```text
outcome_refs  → semantic intent references
packet_id     → Implementation Packet
execution_id  → executable packet configuration
run_id        → historical execution
leaf_id       → bounded DAG/execution unit
attempt_id    → concrete invocation
recovery_id   → recovery record
review_id     → review instance
decision_id   → material authority/governance decision
```

A RunManifest or equivalent runtime surface SHOULD consume structured identity rather than derive semantic truth from filenames or bespoke script naming.

This section is adopter guidance only. It does not authorize AEC implementation or mutation.

## Relationship to GG learning lifecycle

The identity model may be used by the cross-project learning lifecycle to reference semantic outcomes, packets, executions, runs, leaves, attempts, recoveries, reviews, and decisions without overloading packet/run terminology.

This candidate does not change the semantics, authority, evidence admission rules, or lifecycle of `GG-METHOD-PILOT-CROSS-PROJECT-LEARNING-LIFECYCLE-001`.

Any learning-lifecycle adoption requires its own explicit integration decision.

## Non-goals

This standard does not define:

- how Semantic Outcomes are discovered;
- how stories are written;
- how Implementation Packets are decomposed;
- how execution DAGs are generated;
- provider selection;
- retry policy;
- recovery authority;
- review policy;
- merge, release, or deployment authority;
- repository layout;
- a concrete machine schema implementation;
- AEC runtime implementation;
- adopter-specific migration.

Those concerns remain governed by separate architecture, capability, adopter, or authority surfaces.

## Adoption boundary

Owner acceptance of this architecture candidate would accept the provider-neutral identity semantics only.

It would not, by itself, authorize:

- retroactive renaming of accepted historical artifacts;
- automatic migration across repositories;
- SVP product mutation;
- AEC S6 runtime implementation;
- OPD mutation;
- modification of the GG learning lifecycle;
- creation or modification of machine schemas or validators;
- PR creation, merge, release, tag, or deployment;
- alteration of accepted historical source truth.

Each material adoption or implementation step remains subject to its own applicable authority and currentness checks.

## Canonical summary

```text
Execution Scope

Semantic Outcome
    ST = canonical story subtype

Semantic Outcome ↔ PKT
    explicit relationship
    many-to-many permitted

PKT
    Implementation Packet only

PKT → EXEC
    immutable executable realization/configuration

EXEC → RUN
    historical invocation

EXEC → L
    DAG/execution leaf

RUN + L → A
    concrete attempt
    A001 exists for the first actual invocation

REC
    lateral recovery identity

REV
    lateral review identity

DEC
    lateral material-decision identity
```

Core invariants:

```text
Outcome != PKT
PKT != EXEC
EXEC != RUN
RUN != L
L != A
A != REC

Structured relationships are authoritative.
Durable identity strings are projections.

Historical accepted identities remain immutable.
Legacy equivalence must be explicit and non-destructive.
```

## Candidate disposition

```text
STANDARD_STATUS=CANDIDATE_FOR_OWNER_REVIEW
ARTIFACT_ID=GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001
CONTRACT_VERSION=1.0.0
IDENTITY_SCHEMA=gg.execution-identity/v1
OWNER=GENERAL_GOVERNANCE

RETROACTIVE_RENAME_AUTHORIZED=false
AUTOMATIC_MIGRATION_AUTHORIZED=false
AEC_IMPLEMENTATION_AUTHORIZED=false
SVP_MUTATION_AUTHORIZED=false
GG_LEARNING_LIFECYCLE_MUTATION_AUTHORIZED=false
PR_CREATION_AUTHORIZED=false
MERGE_AUTHORIZED=false
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
```
