# Work Packet Design & Dependency Closure Architecture

Status: CANDIDATE_FOR_OWNER_REVIEW

Candidate contract version: 1.0.0

## Purpose

`Work Packet Design & Dependency Closure` is an optional reusable General Governance L2 capability. It defines how a bounded work packet derives, represents, and validates the prerequisite closure required to reach, validate, and truthfully complete its declared outcomes.

The capability distinguishes semantic packet validity, unresolved dependency blocking, dependency closure, and execution authority. It does not infer product requirements, grant execution authority, replace project architecture, or redefine adopter-owned state.

This architecture is generic and technology-neutral. Its first empirical trigger was a packet-boundary failure observed in `Sugar144/stakeholder-validation-portal`, but the reusable semantics defined here are not SVP-specific and must not encode SVP routes, events, schemas, paths, or story identifiers.

## Ownership and layering

The capability is owned by General Governance as a reusable optional L2 surface.

- L0 remains the Project Operating Contract and existing reusable constitutional semantics.
- L1 remains the adopter-owned General Governance configuration contract.
- L2 owns reusable Work Packet Design & Dependency Closure semantics and its machine contracts when separately released.
- L3 remains adopter/project projection and project-specific interpretation.
- L5 remains adopter evidence/history/state.
- L6 may host generic deterministic helpers that implement accepted L2 rules without becoming a second normative source.

The capability is not a `capability-stack` component. The capability-stack contract composes independently governed repositories/systems. Work Packet Design & Dependency Closure is an internal optional General Governance capability and acquires no independent repository or authority chain.

Capability availability in a GG release does not imply adopter activation. Capability activation does not imply packet validity. Packet validity does not imply dependency closure. Dependency closure does not imply execution, publication, acceptance, or release authority.

## Non-goals

This capability does not own or redefine:

- product requirements;
- product architecture;
- story decomposition as a whole;
- Project Owner authority;
- execution admission or mutation authority;
- generic code review;
- provider/runtime selection;
- CWG semantics;
- AET semantics;
- release acceptance;
- project/product acceptance;
- deterministic inference of undeclared semantic dependencies.

## Normative vocabulary

### Declared outcome

A `declared outcome` is a bounded claim that the packet intends to make true when the packet completes.

### Completion condition

A `completion condition` is an observable or demonstrable condition whose satisfaction is necessary to assert honestly that a declared outcome is complete.

### Prerequisite

A `prerequisite` is a condition required to reach, validate, or truthfully complete a declared outcome or another prerequisite in that outcome's dependency closure.

### Dependency relation

A dependency edge is directed from a dependent node to a prerequisite node and declares exactly one relation:

- `REACH`: the prerequisite is necessary for the dependent result to be reachable or producible;
- `VALIDATE`: the prerequisite is necessary to demonstrate the dependent result correctly;
- `COMPLETE`: the prerequisite is necessary for the completion claim to be truthful rather than partial or misleading.

No additional relation kind is implied by this candidate contract.

### Canonical base

The `canonical base` is the exact immutable design/evaluation input against which the packet's intended outcomes, governing authority references, dependency model, and repository-bound claims were derived. A moving branch, `main`, `latest`, `current`, or another floating alias does not substitute for the immutable base identity.

The canonical base does not, by itself, establish mutable runtime or external state. Database rows, queues, service state, external-provider state, mutable files outside the immutable base, and similar conditions require their own evidence/currentness context when they are used to satisfy prerequisites.

### State evaluation context

A `state evaluation context` is the bounded identity and currentness context required to support a prerequisite-satisfaction claim that depends on mutable or external state rather than solely on immutable canonical-base content.

A state evaluation context may need to identify, as applicable, an observation or evidence artifact, the state or target observed, the time or sequence of observation, and a freshness/revalidation boundary. The capability does not prescribe one universal clock-based freshness interval; the applicable authority and semantics determine what makes an observation current enough for the claimed prerequisite.

### Dependency closure

The dependency closure of a declared outcome is the transitive set of prerequisites reachable through dependency edges from that outcome.

Dependency closure is transitive. Marking a prerequisite `IN_PACKET` does not terminate dependency analysis; the prerequisites of that included prerequisite remain part of the closure.

### Exclusion

An `exclusion` describes a work/effect surface or node that the packet will not produce, modify, or execute. Exclusion is a scope statement only. Exclusion never proves that a prerequisite is satisfied.

### Dependency-closed

A packet is `dependency-closed` only when every prerequisite reachable from every included declared outcome has a valid non-pending resolution under this contract.

### Execution authority

Execution authority is outside this capability. No packet classification emitted by this capability creates Owner authority, execution authority, publication authority, acceptance, or release readiness.

## Prerequisite resolution model

Every prerequisite reachable from an included outcome MUST declare exactly one resolution when the packet is evaluated under an explicitly adopted Work Packet Design & Dependency Closure capability.

### IN_PACKET

`IN_PACKET` means the prerequisite is not relied upon as pre-existing satisfaction; the current packet will produce or establish it as part of the coherent result boundary.

An `IN_PACKET` prerequisite remains subject to transitive dependency closure.

### PREEXISTING_SATISFIED

`PREEXISTING_SATISFIED` means the prerequisite is already satisfied directly by the adopter's own canonical-base facts and/or adopter-owned state evaluation context, without relying on a separately identified external dependency as the source of satisfaction.

This resolution requires durable evidence bound strongly enough to the identities and state evaluation context applicable to the satisfaction claim. Immutable repository facts may be bound to the canonical base. Mutable adopter-owned state claims require evidence/currentness constraints appropriate to that state. A belief, branch name, unbound historical note, assumed prior implementation, or stale observation is not sufficient evidence.

If satisfying the prerequisite depends on a result, artifact, or condition supplied through a separately identified external dependency boundary, `PREEXISTING_SATISFIED` MUST NOT be used; the prerequisite must use `BOUND_EXTERNAL_SATISFIED`.

### BOUND_EXTERNAL_SATISFIED

`BOUND_EXTERNAL_SATISFIED` means the prerequisite is satisfied through a separately identified external dependency that provides an exact result, artifact, or condition whose source identity, evidence, applicable currentness constraints, and authority are explicitly bound.

The external dependency may already have produced its result before the current packet is designed; temporal pre-existence alone does not convert externally supplied satisfaction into `PREEXISTING_SATISFIED`.

A prior work-packet result is one valid class of external source, but it is not the only valid class. The capability must not assume that every external prerequisite originates in another work packet.

### UNRESOLVED

`UNRESOLVED` means a real prerequisite has been discovered and represented honestly but is not yet satisfied and is not included for production by the current packet.

An unresolved prerequisite does not by itself make the packet structurally invalid. It blocks dependency closure and therefore prevents the capability from classifying the packet as dependency-closed.

## Candidate normative invariants

Unless a rule explicitly states otherwise, the normative `MUST`, `MUST NOT`, `SHOULD`, and `MAY` statements in this capability apply only to work packets evaluated under an explicitly adopted Work Packet Design & Dependency Closure capability. Publishing this capability in GG does not impose these packet semantics on consumers that have not adopted it.

### WPDC-001 — Declared outcome

Every work packet evaluated under this capability MUST declare at least one bounded outcome whose completion can be evaluated.

### WPDC-002 — Completion conditions

Every declared outcome MUST reference one or more completion conditions sufficient to define what must be true before that outcome may be claimed complete.

### WPDC-003 — Dependency discovery

Every prerequisite known to be required for `REACH`, `VALIDATE`, or `COMPLETE` MUST be represented explicitly in the packet's semantic dependency model.

The deterministic validator may verify the declared model but MUST NOT claim to infer undeclared semantic dependencies from product requirements, architecture, code, or project state.

### WPDC-004 — Transitive closure

Dependency closure MUST be evaluated transitively from every included declared outcome. An `IN_PACKET` prerequisite does not terminate dependency traversal.

### WPDC-005 — Explicit resolution

Every prerequisite reachable from an included outcome MUST declare exactly one supported resolution.

### WPDC-006 — Evidence-bound satisfaction

`PREEXISTING_SATISFIED` and `BOUND_EXTERNAL_SATISFIED` MUST be supported by durable evidence bound to the immutable identities, mutable/external state context, currentness constraints, and applicable authority sufficient to establish the claimed prerequisite satisfaction.

`PREEXISTING_SATISFIED` MUST be used only for satisfaction demonstrated directly from adopter-owned canonical-base facts or adopter-owned state context. `BOUND_EXTERNAL_SATISFIED` MUST be used when the satisfaction claim depends on a separately identified external dependency source. The two resolutions are mutually exclusive for a given prerequisite claim.

The evidence model MUST NOT treat an immutable repository SHA as proof of mutable runtime or external state merely because the packet was designed against that SHA.

### WPDC-007 — Honest blocking

A prerequisite declared `UNRESOLVED` MAY exist in a semantically coherent packet. Its presence prevents dependency closure. The packet MUST NOT represent the prerequisite as satisfied and MUST NOT derive execution readiness from this capability while the prerequisite remains unresolved.

### WPDC-008 — Exclusion safety

A required prerequisite that is not satisfied MUST NOT be excluded while an outcome that depends on it remains included.

In particular:

- `IN_PACKET` plus exclusion of the same required prerequisite is contradictory;
- `UNRESOLVED` plus exclusion of the same required prerequisite while retaining the dependent outcome is invalid;
- a prerequisite MAY be outside the execution surface when its valid resolution is `PREEXISTING_SATISFIED` or `BOUND_EXTERNAL_SATISFIED` and the supporting evidence/currentness binding remains valid.

### WPDC-009 — No synthetic authority

`PACKET_INVALID`, `VALID_BUT_BLOCKED`, and `VALID_DEPENDENCY_CLOSED` are semantic/conformance classifications only. None creates execution, publication, acceptance, release, or Owner authority.

### WPDC-010 — Validation coverage

Every completion condition MUST have at least one declared validation strategy/reference intended to cover it.

Deterministic structural coverage does not prove semantic sufficiency. Determining whether a validation method genuinely proves a completion condition remains a semantic review responsibility.

### WPDC-011 — Canonical and state currentness

Canonical-base-bound claims MUST NOT silently transfer to a different immutable repository state. A changed canonical base requires currentness evaluation or re-evaluation appropriate to the changed claims before prior repository-bound evidence may be reused.

Mutable or external state satisfaction claims MUST also remain inside their declared currentness/revalidation boundary. A canonical-base identity that remains unchanged does not preserve a mutable-state satisfaction claim after that claim's evidence/currentness boundary is no longer valid.

### WPDC-012 — Coherent boundary

A work packet SHOULD represent the smallest coherent result-producing boundary capable of making the full set of included declared outcomes dependency-closed and truthfully completable, without absorbing materially independent outcomes that are not required by the dependency closure or another explicit governing constraint.

This invariant prevents both under-fragmentation that excludes unsatisfied prerequisites and over-packaging that combines unrelated outcomes merely because they are adjacent in implementation or documentation. One dependency-closed included outcome does not excuse another included outcome whose dependency model is blocked, contradictory, or incomplete.

## Packet classification

The capability derives one of three semantic classifications. These classifications are not a replacement lifecycle and do not supersede existing GG execution/authority states.

### PACKET_INVALID

The packet is invalid when its declared machine/semantic model contains a contradiction or fails a mandatory invariant that can be established at the applicable validation layer.

Candidate deterministic reasons include:

- malformed or incompatible machine contract;
- invalid or floating canonical base where an immutable base is required;
- duplicate or unresolved identifiers;
- dependency cycle;
- missing prerequisite resolution;
- missing or mismatched evidence/currentness binding required by a satisfaction resolution;
- included/excluded contradiction;
- unsatisfied required prerequisite excluded while a dependent outcome remains included;
- missing completion condition;
- missing structural validation coverage;
- missing required boundary/authority declarations.

### VALID_BUT_BLOCKED

The packet is internally coherent under the declared model but at least one prerequisite reachable from an included outcome has resolution `UNRESOLVED`.

`VALID_BUT_BLOCKED` means the packet may be correctly designed for a future dependency state, but dependency closure has not been achieved. This classification creates zero execution authority and zero execution readiness from this capability.

### VALID_DEPENDENCY_CLOSED

All prerequisites reachable from every included outcome have a valid non-pending resolution of `IN_PACKET`, `PREEXISTING_SATISFIED`, or `BOUND_EXTERNAL_SATISFIED`, and all deterministic structural invariants pass.

`VALID_DEPENDENCY_CLOSED` MUST NOT be interpreted as `AUTHORIZED_TO_EXECUTE`.

Execution admission remains subject to the Project Operating Contract, Owner authority, currentness, effect-state, isolation, publication, and any other applicable governance gates.

## Cycles

A dependency cycle is invalid. If nodes A and B must be established jointly, their relationship SHOULD be represented beneath a coherent higher-level outcome rather than asserting that each is a prerequisite that must already be established by the other.

The machine validator may reject declared cycles deterministically. It must not infer semantic cyclicity from undeclared project behavior.

## Validation boundary

A future deterministic validator may validate only declared machine-checkable claims. Its responsibility is expected to include:

- schema and capability-version compatibility;
- canonical identity syntax/binding;
- state/evidence identity and declared currentness-binding shape;
- adoption-binding validity;
- identifier uniqueness and reference integrity;
- dependency relation/resolution enums;
- transitive graph traversal;
- cycle detection;
- mandatory resolution for reachable prerequisites;
- evidence-reference presence and binding constraints;
- deterministic separation of adopter-owned direct satisfaction from separately bound external-dependency satisfaction where the manifest declares the applicable source class;
- direct inclusion/exclusion contradictions;
- unresolved/excluded required prerequisite contradictions;
- structural completion-condition validation coverage;
- required work/effect boundary declarations;
- required authority declarations;
- terminal/stop-boundary shape;
- derivation of `PACKET_INVALID`, `VALID_BUT_BLOCKED`, or `VALID_DEPENDENCY_CLOSED` from the declared model.

The deterministic validator MUST NOT claim to determine:

- whether an undeclared semantic prerequisite exists;
- whether a declared validation method genuinely proves its completion condition;
- whether product architecture is sufficient;
- whether two outcomes are materially independent;
- whether a requirement, architecture decision, or project state is substantively correct;
- whether mutable/external evidence is semantically fresh enough when that judgment is not deterministically encoded by the applicable contract;
- whether an asserted adopter-owned versus external source classification is semantically truthful when that distinction cannot be established from declared machine-bound identities;
- whether execution is authorized.

Those require semantic analysis, independent review when proportionate, Owner disposition where applicable, or another authoritative mechanism.

## Human and machine artifact model

The human-readable work packet remains the semantic execution/output contract. This capability does not replace `work-package.md`-style artifacts with a machine-only format.

A future machine manifest SHOULD contain only the minimum claims necessary for deterministic conformance, including conceptually:

- packet identity;
- capability contract version;
- canonical base;
- adoption binding identity;
- governing authority references;
- declared outcomes;
- completion-condition references;
- prerequisites;
- dependency edges;
- prerequisite resolutions;
- evidence references and applicable state/currentness bindings;
- write surface;
- effect surface;
- exclusions;
- required validation references;
- required authority references;
- stop conditions;
- terminal boundary.

The machine manifest MUST NOT become a second canonical requirements or architecture store. Full requirements text, architecture prose, generic implementation instructions, agent chain-of-thought, product state, or synthetic authorization booleans do not belong in the machine contract merely for convenience.

## Adoption boundary

The capability is absent unless explicitly adopted by the consumer.

The existing L1 consumer configuration MAY carry an optional pointer to a capability-specific adopter binding. The exact configuration key and machine schema are implementation details to be fixed only after this architecture is accepted.

The capability-specific binding SHOULD identify adopter-owned source classes without prescribing universal repository paths. Candidate source classes are:

- authority sources;
- state sources;
- requirements sources;
- architecture sources;
- decision sources;
- planning sources.

The binding SHOULD separately identify the adopter-owned packet projection target/root. The projection target is not a source class.

These source classes are semantic categories, not mandatory directory names. An adopter may project them differently. General Governance MUST NOT assume that every consumer uses `docs/architecture/**`, `docs/requirements/**`, or any other fixed project structure.

Capability release by GG does not activate a consumer. Consumer adoption does not retroactively re-evaluate existing packets. Adoption by SVP, re-evaluation of its existing packet, and any resulting implementation authorization are separate later decisions.

## Agent / deterministic split

A future Packet Designer agent may perform semantic tasks such as:

1. resolve durable governing authority and exact source identities;
2. derive intended outcomes;
3. derive completion conditions;
4. discover semantic prerequisite relationships;
5. construct the prerequisite graph;
6. determine prerequisite resolution candidates;
7. compute the required unresolved closure semantically;
8. derive the smallest coherent work/effect boundary;
9. derive validation and exclusion surfaces;
10. perform a semantic closure cross-check;
11. produce the human packet and minimal machine claims.

A future independent Packet Reviewer, when proportional assurance requires one, may review dependency completeness, reachability, scope, authority leakage, excluded prerequisites, validation sufficiency, and accidental multi-outcome packaging.

Detailed agent/skill design is intentionally outside this architecture candidate. The skill is not the canonical contract. A future specialist handoff should be derived only after the normative capability and machine contract are stable enough to constrain it.

## Regression model

Framework regression fixtures MUST be generic and tied to accepted invariants rather than copying adopter-specific domain vocabulary.

The first generic regression family should include at least:

- `IN_PACKET` prerequisite with complete transitive closure -> `VALID_DEPENDENCY_CLOSED`;
- `PREEXISTING_SATISFIED` prerequisite with correctly bound adopter-owned immutable or state/currentness evidence -> `VALID_DEPENDENCY_CLOSED`;
- `BOUND_EXTERNAL_SATISFIED` prerequisite with correctly bound external-dependency identity, evidence/currentness, and authority -> `VALID_DEPENDENCY_CLOSED`;
- externally supplied prerequisite misclassified as `PREEXISTING_SATISFIED` where the declared source identity proves a separate external dependency -> `PACKET_INVALID`;
- honestly declared `UNRESOLVED` prerequisite -> `VALID_BUT_BLOCKED`;
- reachable `UNRESOLVED` prerequisite also excluded -> `PACKET_INVALID` / `EXCLUDED_REQUIRED_PREREQUISITE`;
- reachable `IN_PACKET` prerequisite also excluded -> `PACKET_INVALID`;
- transitive unresolved prerequisite -> `VALID_BUT_BLOCKED`;
- unresolved reference -> `PACKET_INVALID`;
- dependency cycle -> `PACKET_INVALID`;
- completion condition without validation coverage -> `PACKET_INVALID`;
- satisfaction evidence violating its applicable immutable identity or state/currentness binding -> `PACKET_INVALID`.

No fixture should be added merely because a failure is imaginable. A reusable fixture should correspond to an accepted normative invariant.

## Expected machine-contract boundary

After Owner acceptance of this architecture, the smallest coherent implementation is expected to define, without duplicating product truth:

1. one capability-specific adoption binding contract/schema;
2. one minimal work-packet manifest contract/schema;
3. one dedicated deterministic validator;
4. one generic regression suite;
5. bounded CI/release integration;
6. release documentation identifying the capability as optional.

The exact filenames, schema field names, configuration key, diagnostic vocabulary, and release version are deliberately not frozen by this architecture document.

## Release and compatibility boundary

Adding this optional capability SHOULD NOT silently modify the meaning of an already locked consumer that does not adopt it.

The current framework contract, consumer-lock schema, consumer-configuration schema, and capability-composition contract MUST NOT be declared compatible or unchanged merely by assumption. Release packaging must validate whether the final accepted implementation preserves their compatibility before publication.

A future release manifest may publish Work Packet Design & Dependency Closure as an optional capability with its own contract/schema versions. The final release identifier and compatibility disposition belong to the release flow, not this architecture candidate.

## First empirical trigger and preservation rule

The first empirical trigger was a Stakeholder Validation Portal work packet that retained a first target operation while excluding an unsatisfied prerequisite journey-state chain required to reach that operation. Empirical execution reached the backend guard and failed; read-only persistence inspection showed that the prerequisite state was not pre-satisfied.

The reusable GG regression MUST abstract this to the invariant:

> A required prerequisite that is unsatisfied may not be excluded while retaining an included dependent outcome.

The SVP-specific failure remains adopter provenance and a future adopter regression. This GG architecture does not resolve, rewrite, authorize, or mutate the SVP packet.

### Non-normative origin provenance

The empirical origin is preserved for traceability only and does not define reusable GG semantics:

- repository: `Sugar144/stakeholder-validation-portal`;
- capability/slice: `SVP-STAGE2A-GUIDED-ANSWERING-001`;
- work packet: `SVP-STAGE2A-GUIDED-ANSWERING-PACKET-01`;
- observed implementation HEAD: `fc2bac8f6f0098f559188d73882b65c8aaa74c87`.

At that observed state, the first valid-card save attempt returned `HTTP 422` with `section-not-entered`, and read-only persistence inspection found no pre-existing journey-progress state sufficient to satisfy the excluded prerequisite chain. These observations are historical provenance, not a machine inference rule for other adopters.

## Candidate implementation topology

If this architecture is accepted, implementation should remain sequential and dependency-ordered:

1. **Normative capability and adoption contract** — materialize accepted L2 semantics and adopter binding semantics without implementing the future agent skill.
2. **Machine contract, validator, and generic regressions** — implement only deterministic rules justified by accepted invariants.
3. **Framework release integration** — integrate CI, release manifest/surfaces, compatibility evidence, and release packaging.
4. **Skill-specialist handoff** — derive a bounded handoff for the Packet Designer/Reviewer skill from accepted repository-bound contracts.
5. **Consumer adoption** — evaluate SVP or another adopter separately; capability acceptance does not authorize adoption or packet re-evaluation.

## Authority and stop boundary

This document is a candidate architecture only. It does not authorize:

- implementation of schemas or validators;
- modification of L0 semantics;
- final adoption-key/schema naming;
- implementation of the Packet Designer or Reviewer skill;
- release publication;
- SVP adoption or mutation;
- reclassification/rewrite of the existing SVP packet;
- product implementation dependent on this capability.

The next material step after this candidate is repository-bound review and Owner disposition on the architecture/contract boundary. If changes are required, they should amend this candidate before implementation is authorized.