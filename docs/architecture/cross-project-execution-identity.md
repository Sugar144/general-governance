# Cross-Project Execution Identity Standard

Status: CANDIDATE_FOR_OWNER_REVIEW

Artifact ID: `GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001`

Candidate contract version: 1.1.0

Identity schema name: `gg.execution-identity/v1`

Predecessor candidate commit: `e3d198fe6857babad573e3a0a2c610124d3dc6cf`

Predecessor review result: `CHANGES_REQUIRED`

Correction authority: `GG-MP-0014/1.0.0`

## Purpose

This architecture defines a provider-neutral and project-neutral identity taxonomy for semantic intent, implementation packets, executable specifications, historical executions, execution leaves, concrete attempts, recoveries, reviews, and material decisions.

Its purpose is to prevent objects from different conceptual layers from being treated as interchangeable and to provide a stable identity substrate for cross-project governance, evidence lineage, execution architecture, recovery, review, and future autonomous orchestration.

The core separation is:

```text
Semantic Intent != PKT != EXEC != RUN != L != A
```

and:

```text
REC != retry
REC != replacement RUN
REC != formal-run result correction
REV != RUN
REV != reviewed object
DEC != governed action
```

The identity model describes object identity and lineage. It does not create execution authority.

## Normative language

`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative for a consumer that explicitly adopts this standard or claims conformance with `gg.execution-identity/v1`.

This candidate is architecture only. Until separately accepted and materialized through the applicable GG adoption path, it grants no authority and changes no adopter semantics.

## Ownership and layering

General Governance owns:

- provider-neutral identity semantics;
- canonical identity classes;
- cross-project invariants;
- relationship semantics;
- historical compatibility rules.

Execution architectures own, subject to those semantics after adoption:

- runtime representation;
- manifests;
- identifier generation;
- serialization;
- deterministic validation;
- evidence materialization;
- runtime lifecycle implementation.

Adopters own:

- project-specific Identity Scopes;
- semantic intents;
- implementation decomposition;
- concrete typed relationships;
- execution kinds not reserved by this standard;
- adoption timing;
- legacy bridges.

This candidate does not make Claude Agent Execution Architecture, Stakeholder Validation Portal, Dopis, or any other adopter part of General Governance.

## Canonical identity classes

### Identity Scope

An `Identity Scope` is a bounded project-defined namespace/context within which local identities are issued and interpreted.

Examples include a capability, vertical, release slice, formal governance activity, or another explicitly bounded identity context.

A scope identifier and scope kind remain adopter-owned, but conforming structured identity data MUST expose them when local identifiers would otherwise be ambiguous.

Identity Scope is not an execution-authority concept.

The following inference is forbidden:

```text
membership in Identity Scope => execution authority
```

Authority remains governed by the applicable authority contract, decision, or run admission rules.

### Semantic Intent

A `Semantic Intent` identifies upstream product, business, behavioral, or system intent that implementation work may serve.

Semantic Intent describes what is desired at the semantic/product layer. It MUST NOT imply a particular implementation decomposition and MUST NOT be treated as directly executable merely because one implementation packet happens to map one-to-one to it.

`ST` is the canonical label for the `story` subtype of Semantic Intent:

```text
ST-01
ST-02
ST-03
```

GG does not require every Semantic Intent to be a story. Structured consumers SHOULD therefore represent both identity and kind:

```yaml
semantic_intent:
  id: ST-01
  kind: story
```

The GG abstraction is `Semantic Intent`; `ST` is the standard story subtype, not a synonym for every possible intent kind.

### Compatibility with WPDC declared outcomes

`Semantic Intent` is deliberately distinct from the existing Work Packet Design & Dependency Closure term `declared outcome`.

Under WPDC, a `declared outcome` is a bounded claim that a work packet intends to make true when that packet completes. It is part of the packet's internal completion/dependency model.

Under this standard, a `Semantic Intent` is an upstream semantic identity that may motivate or be implemented by one or more packets.

Therefore:

```text
Semantic Intent != WPDC declared outcome
```

A packet MAY reference upstream Semantic Intents through `intent_refs` while independently declaring its own WPDC outcomes.

Example:

```yaml
packet:
  id: PKT-01
  intent_refs:
    - id: ST-01
      kind: story

wpdc:
  outcomes:
    - outcome_id: OUTCOME-01
```

No equality between `ST-01` and `OUTCOME-01` is implied.

### Implementation Packet — PKT

`PKT` identifies one bounded `Implementation Packet`.

Example:

```text
PKT-01
```

The canonical `PKT-*` namespace MUST be reserved exclusively for Implementation Packets.

It MUST NOT be reused as a generic identity for:

- execution specifications or packages;
- runs;
- review bundles;
- recovery bundles;
- evidence bundles;
- semantic intents;
- stories.

The word `packet` MAY still occur informally in descriptive prose, but it does not acquire `PKT` semantics unless it identifies an Implementation Packet under this contract.

#### Relationship to WPDC work packets

This standard does not retroactively redefine every historical or future WPDC `work packet` as a `PKT`.

A WPDC work packet MAY use a `PKT-*` identity when the adopter explicitly declares that the WPDC packet is an Implementation Packet governed by this identity standard.

Absent that explicit binding, similarity of terminology is not canonical equivalence.

### Execution Specification — EXEC

`EXEC` identifies one immutable executable specification/configuration over one governed subject.

Conceptually, EXEC answers:

```text
what exact executable definition is bound for this governed subject?
```

An EXEC MUST expose a typed `subject_ref` identifying the object or bounded work subject it executes.

An EXEC MAY be related to zero or one Implementation Packet.

If `execution_kind` is `IMPLEMENTATION_PACKET`:

- exactly one PKT relation MUST exist;
- the primary `subject_ref` MUST identify that PKT;
- the execution MUST NOT silently absorb a second PKT as though both were one packet identity.

For other execution kinds, a PKT relation is not required.

Non-packet execution subjects may include, when separately governed:

- a review;
- a correction activity;
- an analysis;
- release or publication work;
- another bounded formal activity.

This standard reserves only the `IMPLEMENTATION_PACKET` execution-kind meaning. Other execution-kind values remain adopter/runtime-owned unless separately standardized.

Depending on the execution architecture, an EXEC MAY bind execution-relevant elements such as:

- execution graph;
- leaves;
- contracts;
- runtime-relevant inputs;
- execution strategy;
- provider/runtime configuration;
- validation boundaries;
- execution policies;
- effect model;
- other material execution configuration.

Once accepted or materialized for historical execution, an EXEC MUST NOT be silently mutated in place. A material change to its execution semantics MUST produce a new EXEC identity.

Packet example:

```text
PKT-01
├── EXEC-001
└── EXEC-002
```

Generic non-packet example:

```text
REV-003
└── EXEC-017
```

An adopter or runtime MAY define stricter rules for what constitutes a material EXEC change, provided those rules do not weaken identity immutability.

### Execution Run — RUN

`RUN` identifies one historical invocation of exactly one EXEC for a conforming prospective execution.

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

A replacement execution MUST receive a distinct RUN identity and MUST retain explicit causal lineage to the failed execution when replacement semantics apply.

Replacement, retry, recovery, resume, and ordinary execution MUST NOT be treated as interchangeable merely because they may be causally related.

Historical GG formal-run identities created before adoption of this standard remain valid historical identities and are not retroactively required to manufacture an EXEC parent. Any prospective bridge must be explicit and non-destructive.

### Execution Leaf — L

`L` identifies one bounded executable node within an EXEC execution graph when the execution architecture uses leaf-based decomposition.

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

Not every execution architecture is required to invent synthetic leaves. When leaf-based execution is not used, L and A may be inapplicable.

### Attempt — A

`A` identifies one concrete invocation of one leaf within one RUN.

An Attempt identity MUST be created when the concrete leaf invocation enters the runtime's admitted/started attempt lifecycle. It MUST NOT depend on whether an external provider, mutation, or other execution boundary is later crossed.

Therefore the first admitted invocation is explicitly:

```text
L003
└── A001
```

A subsequent concrete invocation is separately:

```text
L003
├── A001
└── A002
```

An Attempt MUST reference exactly one RUN and exactly one L.

Boundary crossing is evidence/state about the Attempt, not the event that creates its identity.

Example:

```yaml
attempt:
  id: A001
  run_ref: RUN-001
  leaf_ref: L003
  admitted: true
  execution_boundary_crossed: false
  result: PRE_EXECUTION_FAILURE
```

A leaf MAY have zero attempts only when no concrete invocation entered the attempt lifecycle.

This preserves stable semantics for pre-boundary failures, provider failures, retries, and later invocations.

### Recovery — REC

`REC` identifies an explicit recovery intervention or recovery record.

Recovery is a lateral typed identity. It MUST NOT be treated as another name for:

- retry;
- Attempt;
- replacement RUN;
- resumed RUN;
- ordinary execution;
- formal-run result correction.

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

A formal review MAY itself be executed by an EXEC/RUN chain. That execution and the Review identity remain distinct.

Example:

```yaml
review:
  id: REV-003
  produced_by_run_ref: RUN-017
```

Therefore:

```text
REV != RUN
```

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

A DEC identity records a decision; it does not itself prove that the authorized action occurred.

## Existing GG formal-run correction identity

The Project Operating Contract already defines formal-run result correction identity as:

```text
<BASE_RUN_ID>-R<N>
```

where the correction preserves the immutable completed base run and versions a correction of that run's result.

This candidate preserves that existing GG semantic and does not rename it to REC or create a competing correction prefix.

The required distinction is:

```text
formal-run result correction != REC
formal-run result correction != replacement RUN
formal-run result correction != retry
```

A future cross-project canonical correction class such as `COR` would require a separate GG design/adoption decision. It is not introduced by this candidate.

## Semantic Intent-to-Packet relationship

Semantic Intents and Implementation Packets are separate identity classes.

GG MUST NOT define the following as a mandatory parent-child identity hierarchy:

```text
ST → PKT
```

The relationship MAY be:

```text
1 Semantic Intent → 1 PKT
1 Semantic Intent → N PKTs
N Semantic Intents → 1 PKT
N Semantic Intents → N PKTs
```

when justified by implementation decomposition.

Examples:

```text
ST-02
├── implemented_by PKT-01
└── implemented_by PKT-02
```

and:

```text
PKT-04
├── intent_ref ST-05
└── intent_ref ST-06
```

The canonical relationship is therefore:

```text
Semantic Intent ↔ PKT
```

with explicit typed references.

A system MUST NOT infer packet ownership solely from a concatenated identifier containing a story or other Semantic Intent identifier.

## Canonical relationship model

The generic logical model is:

```text
Identity Scope
│
├── Semantic Intent
│      └── ST = story subtype
│
├── PKT
│     └── intent_refs ↔ Semantic Intent
│
├── EXEC
│     ├── subject_ref ──▶ governed subject
│     ├── optional PKT relation
│     ├── L
│     └── RUN
│           └── A when invoking L
│
├── REC ──targets──▶ governed execution/history objects
├── REV ──targets──▶ reviewable objects/evidence
│       └─ may be produced_by_run ──▶ RUN
└── DEC ──affects──▶ governed objects
```

Normative cardinalities are:

```text
Identity Scope → 0..N Semantic Intents
Identity Scope → 0..N PKTs
Identity Scope → 0..N EXECs

Semantic Intent ↔ PKT
many-to-many permitted

PKT → 0..N EXEC over its lifecycle

EXEC → exactly 1 governed subject_ref
EXEC → 0..1 PKT
EXEC → 0..N RUN
EXEC → 0..N L

if execution_kind == IMPLEMENTATION_PACKET:
    EXEC → exactly 1 PKT

if leaf-based execution is used:
    EXEC → 1..N L
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

The existing `<BASE_RUN_ID>-R<N>` correction grammar remains governed by the Project Operating Contract and is not replaced by the patterns above.

## Durable identity projection

Systems MAY expose human-readable durable identifiers by combining Identity Scope and local identities.

For example, with scope:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001
```

a story Semantic Intent MAY project as:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001-ST-01
```

an Implementation Packet MAY project as:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01
```

and a packet execution chain MAY project as:

```text
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001-RUN-001
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001-L003
SVP-STAGE2A-GUIDED-ANSWERING-001-PKT-01-EXEC-001-RUN-001-L003-A001
```

For a non-packet execution, a projection MAY omit PKT entirely:

```text
GG-REVIEW-SCOPE-001-EXEC-017
GG-REVIEW-SCOPE-001-EXEC-017-RUN-001
```

The governed subject remains explicit structured data.

A Semantic Intent identity MUST NOT be inserted into the PKT durable identity as though the intent were necessarily its parent.

Therefore prefer:

```text
...-PKT-01
```

with:

```yaml
intent_refs:
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

A conforming identity record MUST expose enough information to identify:

1. the identity schema family;
2. the project or governing namespace;
3. the Identity Scope;
4. the entity type;
5. the local identity;
6. applicable typed relationships.

Minimal generic representation:

```yaml
identity_schema: gg.execution-identity/v1

project_id: SVP

identity_scope:
  id: SVP-STAGE2A-GUIDED-ANSWERING-001
  kind: vertical

entity:
  type: execution_run
  local_id: RUN-001

relations:
  execution_ref: EXEC-001
```

An EXEC representation MUST expose its governed subject:

```yaml
execution:
  id: EXEC-001
  execution_kind: IMPLEMENTATION_PACKET
  subject_ref:
    type: implementation_packet
    id: PKT-01
```

A non-packet execution MAY instead be:

```yaml
execution:
  id: EXEC-017
  execution_kind: REVIEW
  subject_ref:
    type: review
    id: REV-003
```

`REVIEW` above is illustrative adopter/runtime vocabulary, not a closed GG execution-kind enumeration.

## Implementation-packet execution profile

Execution runtimes executing Implementation Packets SHOULD expose, at minimum when applicable:

```yaml
identity_schema: gg.execution-identity/v1

project_id: SVP

identity_scope:
  id: SVP-STAGE2A-GUIDED-ANSWERING-001
  kind: vertical

semantic_intent_refs:
  - id: ST-01
    kind: story

packet:
  id: PKT-01

execution:
  id: EXEC-001
  execution_kind: IMPLEMENTATION_PACKET
  subject_ref:
    type: implementation_packet
    id: PKT-01

run:
  id: RUN-001
```

A leaf invocation additionally exposes:

```yaml
leaf:
  id: L003

attempt:
  id: A001
  run_ref: RUN-001
  leaf_ref: L003
```

This candidate defines semantic requirements only. It does not create a JSON Schema, RunManifest implementation, validator, identifier generator, or migration tool.

## Required invariants

Conforming implementations MUST preserve the following invariants for every identity class they use.

### Identity separation

```text
Semantic Intent != PKT
PKT != EXEC
EXEC != RUN
RUN != L
L != A
A != REC
REC != replacement RUN
REC != formal-run result correction
REV != RUN
REV != reviewed object
DEC != governed action
```

### No scope-derived authority

Identity Scope membership MUST NOT be interpreted as execution, mutation, publication, acceptance, release, merge, or deployment authority.

### Semantic-intent relationship explicitness

Semantic Intent/PKT relationships MUST be represented explicitly and MUST NOT depend only on concatenated identity strings.

### WPDC vocabulary separation

Semantic Intent MUST NOT be silently substituted for WPDC `declared outcome`, and a WPDC `outcome_id` MUST NOT automatically be interpreted as a Semantic Intent identity.

### Optional generic packet binding

A generic EXEC MUST NOT require a PKT merely to make the execution identifiable.

An EXEC with `execution_kind: IMPLEMENTATION_PACKET` MUST bind exactly one PKT as its primary governed subject.

### Packet pre-execution existence

A PKT MAY exist with zero EXEC identities. Packet design, review, blocking, or readiness states MUST NOT require manufacturing an EXEC before one has actually been defined.

### Attempt completeness

Every concrete leaf invocation that enters its attempt lifecycle MUST receive an Attempt identity, including the first invocation.

Attempt identity creation MUST NOT depend on later external/provider/effect boundary crossing.

### Historical immutability

Historical accepted identities MUST NOT be reassigned, renamed, or rewritten merely to comply with this or a newer naming standard.

### Execution immutability

A material change to an accepted or historically materialized EXEC MUST result in a new EXEC identity.

### No implicit execution/recovery equivalence

Systems MUST NOT infer:

```text
retry == recovery
replacement == recovery
replacement == retry
correction == recovery
correction == replacement
correction == retry
```

unless a separate governing policy establishes an explicit typed relation for the specific event without collapsing the distinct identities.

### Typed lateral references

REC, REV, and DEC MUST identify their target, producer, or affected objects explicitly as applicable.

## Historical compatibility

Historical accepted identities are immutable historical names.

Adoption of this standard MUST NOT:

- rename historical accepted artifacts;
- rewrite accepted evidence;
- reinterpret old identifiers solely because their terminology resembles this standard;
- manufacture canonical equivalence where none has been established;
- manufacture missing historical EXEC, PKT, L, or A identities solely to make old evidence look conformant.

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

Historical GG formal-run identities likewise remain valid without retroactive insertion into a new EXEC chain.

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
    - type: implementation_packet
      id: PKT-01
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

## Conformance model

A consumer claiming `gg.execution-identity/v1` conformance MUST use the canonical meanings and invariants for every standardized identity class it materializes.

The standard does not require every consumer to materialize every class.

In particular:

- a project that does not use Implementation Packets need not create PKT identities;
- an execution architecture that is not leaf-based need not invent L or A identities;
- a consumer that does not perform a recovery need not create REC;
- a consumer MUST NOT reuse an unrelated canonical prefix merely because another class is absent.

For prospective execution, a conforming RUN MUST bind exactly one EXEC.

For prospective leaf-based execution, every concrete leaf invocation MUST bind an A identity as defined above.

A consumer MAY adopt incrementally, but MUST NOT claim that historical objects have been migrated unless the required explicit bridges exist.

## AEC S6 adoption guidance

If Claude Agent Execution Architecture adopts this candidate after GG acceptance, its Implementation-Packet execution profile SHOULD distinguish at least:

```text
identity_scope
semantic_intent_refs
packet_id
execution_id
run_id
leaf_id
attempt_id
recovery_id
review_id
decision_id
```

The intended AEC mapping is:

```text
semantic_intent_refs → upstream product/story intent references
packet_id            → Implementation Packet
execution_id         → immutable executable specification
run_id               → historical invocation
leaf_id              → bounded DAG/execution unit
attempt_id           → concrete admitted leaf invocation
recovery_id          → recovery record
review_id            → review instance
decision_id          → material authority/governance decision
```

AEC SHOULD NOT make `story_id` a structural parent of `packet_id`.

AEC SHOULD NOT require all generic formal executions to manufacture a packet identity; the packet requirement applies to its Implementation-Packet execution profile.

A RunManifest or equivalent runtime surface SHOULD consume structured identity rather than derive semantic truth from filenames or bespoke script naming.

This section is adopter guidance only. It does not authorize AEC S6 implementation or mutation.

## Relationship to GG learning lifecycle

The identity model may be used by the cross-project learning lifecycle to reference Semantic Intents, Implementation Packets, executable specifications, runs, leaves, attempts, recoveries, reviews, and decisions without overloading packet/run terminology.

This candidate does not change the semantics, authority, evidence admission rules, or lifecycle of `GG-METHOD-PILOT-CROSS-PROJECT-LEARNING-LIFECYCLE-001`.

Any learning-lifecycle adoption requires its own explicit integration decision.

## Non-goals

This standard does not define:

- how Semantic Intents are discovered;
- how stories are written;
- how Implementation Packets are decomposed;
- how WPDC declared outcomes are designed;
- how execution DAGs are generated;
- provider selection;
- retry policy;
- recovery authority;
- review policy;
- formal-run result correction policy beyond preserving existing GG semantics;
- merge, release, publication, or deployment authority;
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
- WPDC contract/schema mutation;
- Project Operating Contract mutation;
- modification of the GG learning lifecycle;
- creation or modification of machine schemas or validators;
- PR creation, merge, release, tag, publication, or deployment;
- alteration of accepted historical source truth.

Each material adoption or implementation step remains subject to its own applicable authority and currentness checks.

## Canonical summary

```text
Identity Scope
    namespace/context only
    grants no execution authority

Semantic Intent
    ST = canonical story subtype
    != WPDC declared outcome

Semantic Intent ↔ PKT
    explicit relationship
    many-to-many permitted

PKT
    Implementation Packet only
    may exist with zero EXECs

EXEC
    immutable executable specification
    exactly one governed subject
    generic PKT relation: 0..1
    IMPLEMENTATION_PACKET execution: exactly one PKT

EXEC → RUN
    historical invocation

EXEC → L
    optional DAG/execution leaf

RUN + L → A
    concrete admitted attempt
    A001 exists from first actual attempt lifecycle entry
    boundary crossing is evidence, not identity creation

REC
    lateral recovery identity

REV
    lateral review identity
    REV != RUN
    may reference produced_by_run

DEC
    lateral material-decision identity

existing GG <BASE_RUN_ID>-R<N>
    formal-run result correction
    != REC
    != replacement
    != retry
```

Core invariants:

```text
Semantic Intent != PKT
PKT != EXEC
EXEC != RUN
RUN != L
L != A
A != REC
REV != RUN

Structured relationships are authoritative.
Durable identity strings are projections.
Identity scope grants no authority.
Historical accepted identities remain immutable.
Legacy equivalence must be explicit and non-destructive.
```

## Candidate disposition

```text
STANDARD_STATUS=CANDIDATE_FOR_OWNER_REVIEW
ARTIFACT_ID=GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001
CONTRACT_VERSION=1.1.0
IDENTITY_SCHEMA=gg.execution-identity/v1
OWNER=GENERAL_GOVERNANCE
PREDECESSOR_CANDIDATE=e3d198fe6857babad573e3a0a2c610124d3dc6cf
PREDECESSOR_REVIEW=CHANGES_REQUIRED
CORRECTION_AUTHORITY=GG-MP-0014/1.0.0

RETROACTIVE_RENAME_AUTHORIZED=false
AUTOMATIC_MIGRATION_AUTHORIZED=false
AEC_IMPLEMENTATION_AUTHORIZED=false
SVP_MUTATION_AUTHORIZED=false
WPDC_MUTATION_AUTHORIZED=false
PROJECT_OPERATING_CONTRACT_MUTATION_AUTHORIZED=false
GG_LEARNING_LIFECYCLE_MUTATION_AUTHORIZED=false
PR_CREATION_AUTHORIZED=false
MERGE_AUTHORIZED=false
RELEASE_AUTHORIZED=false
PUBLICATION_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
```
