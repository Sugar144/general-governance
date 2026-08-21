---
document_id: GOV-L2-WORK-PACKET-DESIGN-ADOPTION-001
capability_id: work-packet-design-dependency-closure
version: 1.0.0
status: NORMATIVE_ADOPTION_CONTRACT_PENDING_RELEASE_INTEGRATION
normative_capability_contract: framework/capabilities/work-packet-design/contract.md
capability_contract_version: 1.0.0
accepted_architecture_commit: d43950df47d9d01b516a46f63e7ae9f7da1f24f7
owner_disposition_commit: 88f1be46a3920154e66cad2d64344b9263737c78
---

# Work Packet Design & Dependency Closure — Adoption Contract

## 1. Purpose

This contract defines how a General Governance consumer explicitly adopts the optional Work Packet Design & Dependency Closure (WPDC) L2 capability without moving adopter-owned project truth into the framework.

It defines semantic activation, binding ownership, source-class boundaries, projection ownership, currentness, and failure behavior. The machine schema for the binding document is a later implementation surface and MUST implement this contract rather than redefine it.

## 2. Explicit activation only

WPDC is absent for a consumer unless the adopter explicitly activates it.

The reserved optional discovery key is:

`configuration.capabilities.work_packet_design.binding_path`

The key belongs to the WPDC optional capability contract. It is not a new required core configuration key for consumers that do not adopt WPDC.

A consumer activates WPDC only when all of the following are true:

1. its adopter-owned General Governance configuration contains the discovery key;
2. the value resolves to exactly one adopter-owned WPDC binding document;
3. that binding document conforms to a WPDC adoption contract version supported by the selected General Governance framework identity;
4. the binding selects a WPDC normative capability contract version supported by that framework identity;
5. the binding itself satisfies the mandatory identity/version and internal-coherence semantics of this contract.

Packet-specific source sufficiency is evaluated separately. A globally valid adoption does not guarantee that every future packet has enough bounded project context to be designed truthfully.

A framework release merely containing WPDC does not activate it. A binding file that exists but is not selected by the adopter configuration does not activate it. A prose statement that "WPDC applies" does not substitute for the explicit binding.

If the discovery key is present but the referenced binding is absent, ambiguous, unsupported, unresolved, or materially invalid, WPDC adoption is invalid and a packet MUST NOT be treated as WPDC-conformant until the adoption defect is corrected.

## 3. Ownership boundary

The adopter owns:

- the consumer configuration value that selects the binding;
- the binding document itself;
- source mappings and source identities declared by the binding;
- project-specific authority, requirements, architecture, decisions, planning, state, and evidence;
- any packet projection target/root selected by binding or exact packet context;
- mutable-state observation/currentness semantics not defined by reusable GG contracts;
- project-specific interpretation of what the mapped sources mean.

General Governance owns:

- the reusable WPDC capability semantics;
- this reusable adoption contract;
- future reusable WPDC machine schemas/validators/helpers when separately implemented and released.

The binding identifies adopter truth; it does not transfer ownership of that truth to General Governance.

## 4. Binding identity and versioning

Each adopter binding MUST have a stable binding identity and MUST declare the WPDC adoption-contract version and WPDC capability-contract version it intends to use.

A packet evaluation governed by WPDC MUST be traceable to the exact binding content/currentness context used for that evaluation. A later machine contract may represent this with a digest, immutable repository identity, or equivalent exact binding mechanism; the exact field shape is intentionally deferred.

Changing the binding may change packet-design semantics even when the General Governance framework lock does not change. Therefore a changed binding MUST NOT silently transfer prior packet-evaluation claims when the changed mapping can affect authority, source resolution, state interpretation, projection, or dependency evidence.

A binding change is adopter-owned semantic change. The applicable project/governance process determines whether existing packets require re-evaluation.

## 5. Required semantic binding content

A valid WPDC binding MUST identify, at semantic level:

- one stable binding identity;
- the adopted WPDC adoption-contract version;
- the adopted WPDC capability-contract version;
- the adopting project/repository identity or equivalent stable adopter identity;
- every source binding that the adopter elects to make generically available to WPDC;
- any adopter-specific state-source/currentness rules required to interpret declared mutable state sources;
- any explicit bounded source-resolution rules needed to prevent the capability from searching arbitrary undeclared project surfaces.

The binding SHOULD identify the adopter-owned packet projection target/root when the adopter wants one stable generic WPDC projection location.

No source class is made globally mandatory merely by this adoption contract. A particular packet may still require authority, requirements, architecture, state, decision, or planning material to be supplied through a declared binding or another exact authority-bound packet input before that packet can be designed or evaluated truthfully.

The future machine schema may split, normalize, or name these fields differently only if it preserves these semantics.

## 6. Source classes

WPDC v1 recognizes these adopter source classes:

- **authority sources** — durable sources used to determine applicable Owner/governance authority, constraints, permissions, and stop boundaries;
- **state sources** — sources or observation mechanisms used to determine adopter-owned mutable/project state relevant to prerequisite satisfaction or currentness;
- **requirements sources** — durable sources for product/project requirements and acceptance semantics;
- **architecture sources** — durable sources for architectural constraints, dependencies, interfaces, and reachability semantics;
- **decision sources** — durable decisions/ADRs/dispositions that constrain packet design;
- **planning sources** — durable plans, stories, work packages, milestones, or sequencing material that provide bounded planning context.

These are semantic classes, not mandatory directory names and not a universal repository layout.

An adopter MAY map one durable source to more than one class when that source legitimately serves multiple roles. Such overlap does not merge the meanings of the classes.

The binding MUST NOT invent authority merely by labeling a path or source as an authority source. Source-class mapping says where the capability may resolve relevant adopter material; substantive authority still comes from the mapped content and applicable governance hierarchy.

## 7. Bounded source resolution

A WPDC process MUST resolve project context through the adopter's declared source bindings and applicable exact references. It MUST NOT roam arbitrary repository or external surfaces merely because potentially relevant information exists there.

If a required semantic input cannot be resolved from the declared source bindings or another exact authority-bound reference already supplied to the packet process, the process MUST stop, block, or escalate according to applicable governance rather than silently broadening its search surface.

The adoption binding MAY identify repository-local paths, externally resolved sources, state-observation mechanisms, or other bounded locators where the later machine contract supports them. This contract does not require all source classes to be repository-local files.

Omission of any source class does not make adoption globally invalid. It means that class is unavailable through the generic binding unless another applicable exact reference is supplied to the packet process.

If a particular packet cannot be designed truthfully without material from an omitted class, that packet process cannot claim semantic completeness and MUST block/escalate unless the missing material is supplied through an exact bounded input.

In particular, WPDC packet design MUST have a bounded way to resolve applicable authority, whether through an authority-source binding or an exact authority-bound packet input. Absence of a generic authority-source binding is not by itself an adoption failure; inability to resolve applicable authority for the packet is a packet-evaluation stop condition.

## 8. State sources and currentness

State-source bindings require special treatment because mutable state is not proven by the immutable repository canonical base.

When a packet uses mutable adopter-owned state to support `PREEXISTING_SATISFIED`, the evaluation MUST obtain durable evidence and a state evaluation context sufficient under the normative capability contract.

A state-source binding SHOULD identify how the relevant state target is located and what adopter/governing semantics define a valid observation/currentness boundary. The binding MUST NOT fabricate one universal freshness interval when the project has no such semantics.

When state evidence comes from a separately identified external dependency rather than direct adopter-owned state context, the packet MUST use `BOUND_EXTERNAL_SATISFIED` rather than relabeling it as direct pre-existing satisfaction.

## 9. External dependency satisfaction

The adoption binding does not need to enumerate every external dependency that any future packet might consume.

A packet using `BOUND_EXTERNAL_SATISFIED` MUST bind the applicable external dependency source/evidence exactly at packet-evaluation level under the normative capability contract and future machine contract.

The adoption binding MAY provide bounded source locations or authority sources from which such external dependencies can be resolved, but it MUST NOT convert externally supplied results into adopter-owned pre-existing facts simply by mapping them into a source class.

## 10. Packet projection target

The binding SHOULD declare exactly one adopter-owned packet projection target/root when the adopter wants a stable generic location for WPDC-governed packet artifacts.

The projection target is an output/custody location, not a source class. Content written there does not become an authoritative requirements, architecture, state, or authority source merely because WPDC produced it.

If the generic binding omits a projection target, a packet-producing process MUST NOT invent a universal path. It must use an exact adopter-owned projection target supplied by applicable packet/project authority before persisting WPDC packet artifacts.

If an adopter intentionally wants historical packet artifacts to serve as a planning/decision/authority source for later work, it MUST map that source role explicitly under the applicable source class and preserve the governing provenance/authority semantics.

WPDC MUST NOT assume a universal projection path such as `docs/work-packets`, `governance/work-packages`, or any other fixed directory.

## 11. Binding versus canonical product truth

The binding is a routing/ownership contract, not a copy of product truth.

It SHOULD identify bounded sources by locator/identity semantics rather than duplicate full requirements, architecture prose, decisions, project state, or evidence content.

The binding MUST NOT contain synthetic booleans such as `authorized: true` or `requirements_satisfied: true` as substitutes for resolving the actual authoritative source/evidence.

When mapped sources conflict materially, WPDC MUST apply the existing applicable authority/durable-truth hierarchy or stop for disposition. It MUST NOT choose the source that makes a packet easiest to close.

## 12. Adoption currentness and re-evaluation

WPDC adoption is evaluated in the context of:

- the adopter's exact General Governance framework identity;
- the adopter-owned configuration selecting the binding;
- the binding identity/content used by the packet evaluation;
- the packet canonical base;
- any mutable/external state evaluation contexts used for prerequisite satisfaction.

A change in one identity does not automatically invalidate every other layer, but no claim may silently transfer when the changed layer is material to that claim.

In particular:

- moving the project repository to a new commit requires packet canonical-base currentness evaluation;
- changing the WPDC binding requires evaluation of affected source/projection semantics;
- changing mutable/external state requires state evidence/currentness evaluation;
- changing the selected GG/WPDC contract identity requires compatibility evaluation under the framework release/upgrade process.

The capability and its validator MUST NOT guess that drift is semantically irrelevant when the applicable contract requires currentness evidence.

## 13. Historical packets and activation/deactivation

Adopting WPDC affects only evaluations performed under the adoption after activation. It does not retroactively make historical packets WPDC-conformant, invalid, blocked, or dependency-closed.

Historical packet re-evaluation requires an explicit project/governance action with an exact evaluation context.

Removing the discovery key or otherwise deactivating WPDC affects future use of the optional capability; it does not erase historical WPDC evidence or rewrite prior dispositions.

Activation and deactivation do not themselves create execution, publication, acceptance, merge, or release authority.

## 14. Machine-validation boundary

A future WPDC machine validator may verify adoption facts that are explicitly represented, such as:

- presence/shape of the discovery key when WPDC use is requested;
- binding existence and supported version identity;
- required binding identity/version declarations;
- declared source-class and projection-target reference integrity;
- binding identity/currentness references represented by a packet manifest;
- contradictions provable from declared source ownership/identity;
- packet-specific absence of a required bounded authority/source/projection input when the future machine contract makes that requirement representable.

It MUST NOT infer whether mapped requirements or architecture are substantively correct, whether a source truly has authority when that cannot be determined from declared machine-bound evidence, or whether mutable state is semantically fresh enough when the adopter has not encoded a deterministic currentness rule.

Those remain semantic/governance responsibilities.

## 15. Failure behavior

WPDC adoption MUST fail closed for the packet being evaluated when a mandatory adoption fact is missing, unresolved, contradictory, or unsupported.

A failed WPDC adoption MUST NOT silently fall back to "best effort WPDC" while still claiming WPDC conformance.

A consumer that has not adopted WPDC is not in an adoption-failure state; WPDC is simply absent for that consumer.

This distinction is normative:

- no discovery key -> WPDC absent;
- discovery key plus valid supported binding -> WPDC adopted;
- discovery key plus missing/invalid/unsupported binding -> WPDC adoption invalid for governed evaluation.

A valid adoption plus insufficient bounded context for one particular packet is a packet-evaluation problem, not automatic global adoption invalidity.

## 16. Compatibility and release boundary

This contract reserves the optional discovery key and binding semantics, but it does not itself declare a particular General Governance release compatible with WPDC.

Release integration must separately advertise/support the WPDC contract and future machine schemas, and must prove the compatibility impact on the framework contract, consumer lock, consumer configuration, capability composition, and required surfaces.

Consumers that do not add the optional discovery key MUST NOT acquire WPDC packet obligations merely because a later General Governance release contains WPDC.

## 17. Version and change boundary

This is WPDC adoption contract version `1.0.0`.

Changes to activation semantics, discovery-key meaning, adopter/framework ownership, source-class availability semantics, packet projection ownership, binding currentness, historical re-evaluation, or fail-closed adoption behavior are semantic contract changes and require explicit version/change disposition.

The future binding JSON/YAML schema and validator implementation must be derived from this contract and may not narrow or broaden these semantics without a separately governed contract change.