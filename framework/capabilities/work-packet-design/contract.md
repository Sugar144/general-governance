---
document_id: GOV-L2-WORK-PACKET-DESIGN-DEPENDENCY-CLOSURE-001
capability_id: work-packet-design-dependency-closure
version: 1.0.0
status: NORMATIVE_CONTRACT_PENDING_RELEASE_INTEGRATION
layer: L2
accepted_architecture_commit: d43950df47d9d01b516a46f63e7ae9f7da1f24f7
accepted_architecture_blob: 0ddf288274c9805a4a00b2d3929e9c7fe6aa12ec
owner_disposition_commit: 88f1be46a3920154e66cad2d64344b9263737c78
---

# Work Packet Design & Dependency Closure — Normative Capability Contract

## 1. Purpose and authority

Work Packet Design & Dependency Closure (WPDC) is an optional reusable General Governance L2 capability. It governs how a work packet represents and closes the prerequisites required to reach, validate, and truthfully complete its included declared outcomes.

This contract materializes the Owner-accepted architecture identified in the front matter. The architecture explains design rationale and boundaries; this document is the reusable normative L2 contract for the capability.

The capability does not replace the Project Operating Contract, product requirements, product architecture, project state, or adopter authority. It adds no execution authority by itself.

The terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative only for a consumer that has explicitly adopted WPDC under the companion adoption contract.

## 2. Layering and scope

General Governance owns this reusable L2 contract. The adopter remains responsible for project-specific projection, project state, evidence/history, configuration values, and provider/runtime bindings.

WPDC is not a capability-stack component. Capability-stack composition governs independently governed repositories/systems. WPDC is an optional module inside General Governance and follows the General Governance framework identity selected by the adopter.

Framework availability of WPDC does not activate it for a consumer. Adoption is explicit and is governed by `adoption-contract.md`.

WPDC governs only packet-design/dependency-closure semantics. It does not own or redefine:

- product requirements or architecture;
- story decomposition as a whole;
- Project Owner authority;
- execution admission or mutation authority;
- generic code review;
- provider/runtime selection;
- CWG or AET semantics;
- release approval or product acceptance;
- semantic truth that is not represented by the adopter's authoritative sources;
- deterministic inference of missing product dependencies.

## 3. Normative vocabulary

### 3.1 Declared outcome

A **declared outcome** is a bounded claim that the packet intends to make true when the packet completes.

An outcome is **included** when the packet claims responsibility for producing or establishing that outcome. An outcome that is not included creates no closure obligation for that packet unless another included node depends on it as a prerequisite.

### 3.2 Completion condition

A **completion condition** is an observable or demonstrable condition whose satisfaction is necessary before an included outcome may be claimed complete.

Completion conditions define what must be true; they do not, by themselves, prove that it is true.

### 3.3 Prerequisite

A **prerequisite** is a condition required to reach, validate, or truthfully complete an included outcome or another prerequisite in that outcome's dependency closure.

A prerequisite may be produced inside the current packet, already satisfied directly in adopter-owned context, supplied through a separately identified external dependency, or unresolved.

### 3.4 Dependency relation

Each dependency edge is directed from a dependent node to a prerequisite node and declares exactly one of these relations:

- `REACH`: the prerequisite is necessary for the dependent result to be reachable or producible;
- `VALIDATE`: the prerequisite is necessary to demonstrate the dependent result correctly;
- `COMPLETE`: the prerequisite is necessary for the completion claim to be truthful rather than partial or misleading.

The relation identifies why the prerequisite is required. It does not itself state how the prerequisite is satisfied.

### 3.5 Canonical base

The **canonical base** is the exact immutable design/evaluation input against which the packet's outcomes, governing authority references, dependency model, and repository-bound claims were derived.

A moving alias such as `main`, `latest`, `current`, or a branch name is not an immutable canonical-base identity.

The canonical base does not prove mutable runtime or external state. Database rows, queues, service state, external-provider state, mutable files outside the immutable base, and similar conditions require their own state/evidence context when used to satisfy prerequisites.

### 3.6 State evaluation context

A **state evaluation context** is the bounded identity and currentness context used to support a prerequisite-satisfaction claim that depends on mutable or external state rather than solely on immutable canonical-base content.

As applicable, it identifies the observed target/state, durable evidence or observation artifact, observation sequence or time, and a freshness/revalidation boundary.

WPDC does not prescribe one universal time-based freshness interval. Applicable adopter semantics and authority determine what makes an observation current enough for the claim.

### 3.7 Exclusion

An **exclusion** declares a node, work surface, or effect surface that the packet will not produce, modify, or execute.

Exclusion is a scope statement. Exclusion never proves prerequisite satisfaction.

### 3.8 Dependency closure

The **dependency closure** of an included outcome is the transitive set of prerequisites reachable through dependency edges from that outcome.

The packet closure is the union of the dependency closures of all included outcomes.

### 3.9 Dependency-closed

A packet is **dependency-closed** only when every prerequisite reachable from every included outcome has a valid non-pending resolution and all mandatory applicable WPDC invariants pass.

Dependency-closed is a dependency-design classification, not an execution or acceptance authority state.

## 4. Prerequisite resolution model

Every prerequisite reachable from an included outcome MUST declare exactly one of the four resolutions below.

### 4.1 `IN_PACKET`

`IN_PACKET` means the current packet is responsible for producing or establishing the prerequisite as part of its coherent result boundary.

An `IN_PACKET` prerequisite remains part of the graph and MUST itself satisfy transitive dependency closure. `IN_PACKET` never means "assume satisfied when execution begins."

An `IN_PACKET` prerequisite MUST NOT simultaneously be excluded from the packet's required work/effect boundary.

### 4.2 `PREEXISTING_SATISFIED`

`PREEXISTING_SATISFIED` means the prerequisite is already satisfied directly by the adopter's own canonical-base facts and/or adopter-owned state evaluation context, without relying on a separately identified external dependency as the source of satisfaction.

This resolution MUST be supported by durable evidence bound strongly enough to the identities and state context applicable to the claim.

Immutable repository facts may be bound to the canonical base. Mutable adopter-owned state claims require applicable evidence/currentness constraints. A belief, floating branch, unbound historical note, assumed prior implementation, or stale observation is not sufficient evidence.

If satisfaction depends on a result, artifact, or condition supplied through a separately identified external dependency boundary, `PREEXISTING_SATISFIED` MUST NOT be used.

### 4.3 `BOUND_EXTERNAL_SATISFIED`

`BOUND_EXTERNAL_SATISFIED` means the prerequisite is satisfied through a separately identified external dependency that provides an exact result, artifact, or condition whose source identity, evidence, applicable currentness constraints, and authority are explicitly bound.

A prior work-packet result is one possible external source, but it is not the only possible external source.

Temporal pre-existence does not change source ownership: an external dependency that completed before the current packet was designed remains external and MUST NOT be relabeled `PREEXISTING_SATISFIED` merely because its result already exists.

### 4.4 `UNRESOLVED`

`UNRESOLVED` means a real prerequisite has been discovered and represented honestly but is not yet satisfied and is not included for production by the current packet.

`UNRESOLVED` does not by itself make a coherent packet invalid. It prevents dependency closure and therefore yields a blocked packet when no stronger invalidity applies.

An unresolved prerequisite MUST NOT be represented as satisfied, MUST NOT be used to support completion, and MUST NOT produce execution readiness from WPDC.

## 5. Normative invariants

### WPDC-001 — Declared outcome

Every work packet evaluated under WPDC MUST declare at least one bounded included outcome whose completion can be evaluated.

### WPDC-002 — Completion conditions

Every included outcome MUST reference one or more completion conditions sufficient to define what must be true before the outcome may be claimed complete.

### WPDC-003 — Dependency discovery

Every prerequisite known by the applicable semantic design/review process to be required for `REACH`, `VALIDATE`, or `COMPLETE` MUST be represented explicitly in the packet dependency model.

Deterministic tooling may validate the declared graph but MUST NOT claim that absence of an undeclared edge proves no semantic dependency exists.

### WPDC-004 — Transitive closure

Dependency closure MUST be evaluated transitively from every included outcome. An `IN_PACKET` prerequisite does not terminate traversal.

### WPDC-005 — Explicit resolution

Every prerequisite reachable from an included outcome MUST declare exactly one supported resolution.

### WPDC-006 — Evidence-bound satisfaction

`PREEXISTING_SATISFIED` and `BOUND_EXTERNAL_SATISFIED` MUST be supported by durable evidence bound to the immutable identities, state context, currentness constraints, and applicable authority sufficient for the satisfaction claim.

`PREEXISTING_SATISFIED` is limited to direct adopter-owned satisfaction. `BOUND_EXTERNAL_SATISFIED` is required when the satisfaction claim depends on a separately identified external dependency source. The two resolutions are mutually exclusive for one prerequisite claim.

An immutable repository SHA MUST NOT be treated as proof of mutable runtime or external state merely because the packet was designed against that SHA.

### WPDC-007 — Honest blocking

A prerequisite declared `UNRESOLVED` MAY exist in a semantically coherent packet. Its presence prevents dependency closure.

The packet MUST NOT claim that unresolved prerequisite as satisfied and MUST NOT derive execution readiness from WPDC while it remains unresolved.

### WPDC-008 — Exclusion safety

A required prerequisite that is not satisfied MUST NOT be excluded while an included outcome depends on it.

In particular:

- `IN_PACKET` plus exclusion of the same required prerequisite is contradictory;
- `UNRESOLVED` plus exclusion of the same required prerequisite while retaining the dependent included outcome is invalid;
- a prerequisite MAY be outside the execution surface when its valid resolution is `PREEXISTING_SATISFIED` or `BOUND_EXTERNAL_SATISFIED` and its evidence/currentness binding remains valid.

### WPDC-009 — No synthetic authority

WPDC packet dispositions are semantic/conformance classifications only. They MUST NOT create execution, publication, acceptance, release, merge, or Project Owner authority.

### WPDC-010 — Validation coverage

Every completion condition MUST have at least one declared validation strategy/reference intended to cover it.

Structural coverage does not prove semantic sufficiency. A semantic reviewer or applicable authority remains responsible for judging whether the selected validation can actually demonstrate the condition when that judgment is not deterministically encoded.

### WPDC-011 — Canonical and state currentness

Canonical-base-bound claims MUST NOT silently transfer to a different immutable repository state. A changed canonical base requires currentness evaluation or re-evaluation appropriate to the affected claims before repository-bound evidence may be reused.

Mutable or external state satisfaction claims MUST remain within their declared currentness/revalidation boundary. An unchanged canonical-base identity does not preserve a mutable-state claim after that claim's state/evidence boundary is no longer valid.

### WPDC-012 — Coherent boundary

A work packet SHOULD represent the smallest coherent result-producing boundary capable of making the full set of included outcomes dependency-closed and truthfully completable, without absorbing materially independent outcomes that are not required by dependency closure or another explicit governing constraint.

One closed included outcome does not excuse another included outcome whose dependency model is blocked, contradictory, or incomplete.

## 6. Packet disposition model

WPDC defines exactly these packet dispositions:

- `PACKET_INVALID`;
- `VALID_BUT_BLOCKED`;
- `VALID_DEPENDENCY_CLOSED`.

They are not an execution lifecycle.

### 6.1 Precedence

For one evaluation context, disposition precedence is:

1. `PACKET_INVALID` if any mandatory applicable invariant is violated or the represented packet model is contradictory/structurally unusable;
2. otherwise `VALID_BUT_BLOCKED` if at least one prerequisite reachable from an included outcome is `UNRESOLVED`;
3. otherwise `VALID_DEPENDENCY_CLOSED` when every reachable prerequisite has a valid non-pending resolution and all mandatory applicable invariants pass.

A lower-precedence successful condition MUST NOT mask a higher-precedence invalidity. For example, an unrelated unresolved prerequisite does not downgrade an exclusion contradiction from invalid to merely blocked.

### 6.2 `PACKET_INVALID`

A packet is invalid when an applicable validation layer establishes a mandatory contract violation or contradiction.

Examples include invalid/floating canonical identity where an immutable base is required, unresolved references, dependency cycles, missing prerequisite resolution, invalid evidence/currentness binding, included/excluded contradiction, required unsatisfied prerequisite excluded while the dependent outcome remains included, missing completion conditions, or missing structural validation coverage.

A semantic review may also establish invalidity by finding a required undeclared dependency or semantically insufficient completion/validation model. Deterministic tooling is not required to infer those facts.

### 6.3 `VALID_BUT_BLOCKED`

A packet is valid-but-blocked when the represented packet is coherent under applicable WPDC rules but at least one prerequisite in the transitive closure of an included outcome is `UNRESOLVED`.

This disposition means the packet may be correctly designed for a future dependency state. It creates zero execution readiness or authority from WPDC.

### 6.4 `VALID_DEPENDENCY_CLOSED`

A packet is valid-dependency-closed when all prerequisites reachable from every included outcome resolve through `IN_PACKET`, `PREEXISTING_SATISFIED`, or `BOUND_EXTERNAL_SATISFIED`, and all mandatory applicable WPDC invariants pass.

`VALID_DEPENDENCY_CLOSED` MUST NOT be interpreted as `AUTHORIZED_TO_EXECUTE`.

## 7. Semantic and deterministic responsibility split

WPDC intentionally separates semantic discovery/judgment from deterministic verification.

A semantic packet-design/review process is responsible, as applicable, for:

- resolving governing project authority and authoritative sources;
- deriving bounded outcomes and completion conditions;
- discovering semantic prerequisites;
- choosing dependency relations;
- determining whether satisfaction is adopter-owned, externally supplied, or unresolved;
- judging the smallest coherent result boundary;
- judging semantic validation sufficiency;
- detecting materially independent outcomes or hidden scope expansion.

Future deterministic tooling may verify only claims that are represented in its machine contract, including graph/reference integrity, declared resolution shape, transitive traversal, cycles, evidence/currentness bindings that are machine-represented, direct inclusion/exclusion contradictions, and structural validation coverage.

Deterministic tooling MUST NOT claim to determine an undeclared semantic prerequisite, semantic freshness that is not encoded by an applicable contract, substantive architectural correctness, or execution authority.

A deterministic PASS over the declared model does not prevent an applicable semantic review from identifying a missing dependency and returning `PACKET_INVALID`. Conversely, semantic confidence MUST NOT override a deterministic contract failure without correcting the represented packet.

## 8. Cycles and co-produced conditions

A prerequisite dependency cycle is invalid under WPDC v1.

If two conditions must be established jointly, the packet SHOULD model them beneath a coherent higher-level result or as co-produced parts of an included result boundary rather than representing each as a prerequisite that must be established by the other.

WPDC v1 does not define strongly connected component semantics or cyclic prerequisite execution.

## 9. Validation closure

For each included outcome, the semantic chain is:

`outcome -> completion conditions -> required validation`.

The packet MUST declare enough validation references to cover every completion condition structurally.

Structural reference coverage is necessary but not sufficient. Where validation sufficiency requires domain judgment, that judgment remains semantic and may require independent review proportionate to the risk/materiality of the packet.

## 10. Work/effect boundary and exclusions

A governed packet MUST delimit the work/effect surface required to produce its included outcomes and `IN_PACKET` prerequisites.

An exclusion MUST NOT contradict the transitive prerequisite closure. The packet may explicitly exclude work already satisfied by valid `PREEXISTING_SATISFIED` or `BOUND_EXTERNAL_SATISFIED` evidence, because those resolutions demonstrate that the packet is not responsible for producing that prerequisite.

An exclusion does not transform an unsatisfied prerequisite into a satisfied one and does not remove a prerequisite edge from the semantic graph.

## 11. Human and machine artifact relationship

The human-readable work packet remains the semantic execution/output contract for the adopter.

A future machine manifest is a bounded projection of claims needed for deterministic conformance. It MUST NOT become a second canonical requirements, architecture, project-state, or authorization store.

When the human semantic packet and machine projection conflict on a material WPDC claim, the conflict MUST fail closed until reconciled. The machine manifest MUST NOT silently override the human semantic contract, and prose MUST NOT be used to bypass a required machine constraint after the machine contract exists.

Full requirements prose, architecture prose, generic implementation instructions, model chain-of-thought, product state, or synthetic authorization booleans MUST NOT be copied into the machine projection merely for convenience.

## 12. Authority boundary

WPDC evaluates dependency design and closure only.

No WPDC disposition creates or substitutes for:

- Owner authorization;
- execution admission;
- mutation permission;
- publication authority;
- merge authority;
- release authority;
- consumer acceptance;
- provider/runtime authority.

A project may require a dependency-closed packet before execution, but the authority that admits execution must come from the applicable General Governance/project mechanism outside WPDC.

## 13. Adoption dependency

A consumer is governed by this contract only after explicit WPDC adoption under `framework/capabilities/work-packet-design/adoption-contract.md`.

A General Governance release may contain this contract without activating it for any consumer.

The adoption states are distinct:

- if the optional WPDC discovery key is absent, WPDC is absent for that consumer;
- if the discovery key is present and resolves to a valid supported binding, WPDC is adopted;
- if the discovery key is present but the binding is missing, invalid, ambiguous, or unsupported, WPDC adoption is invalid for governed evaluation and MUST NOT be treated as either successful adoption or simple absence.

Adoption does not retroactively re-evaluate historical packets unless a separately authorized process performs that evaluation.

## 14. Version and change boundary

This is WPDC normative contract version `1.0.0`.

Any future change that modifies the meaning of outcomes, dependency relations, prerequisite resolutions, closure, dispositions, evidence/currentness semantics, optional-adoption boundary, or authority separation is a contract-semantic change and requires explicit version/change disposition under the applicable General Governance release process.

Machine schema versions, validator diagnostics, CI integration, and release-manifest advertisement are intentionally outside this contract's current implementation block and MUST be derived from this contract rather than redefine it.