# Capability Composition Architecture

Status: CANDIDATE_FOR_OWNER_REVIEW

## Decision

General Governance (GG), Concurrent Repository Work Governance (CWG), and AI Execution Telemetry (AET) remain independently owned and independently versioned systems. None acquires normative authority over another.

A project/adopter is the composition boundary. A project may bind GG together with zero or more specialized governance or evidence/observability capabilities. The binding is project-owned and does not merge the component authority chains.

Dopis and stakeholder-validation-portal are intended implementation consumers of the combined stack GG + CWG + AET. This establishes a concrete need for a reusable composition contract now rather than a hypothetical future extension.

## Component roles

- `GOVERNANCE_FRAMEWORK`: reusable general-governance semantics. For this contract the framework is `Sugar144/general-governance`.
- `GOVERNANCE_CAPABILITY`: specialized governance with authority only inside its own declared domain. CWG is the first intended instance.
- `EVIDENCE_OBSERVABILITY_CAPABILITY`: observations/evidence that may be consumed by governance or project logic but create no governance authority or acceptance. AET is the first intended instance.

Provider/runtime adapters are project-owned projections and are not composition components. They must not create or redefine normative semantics.

## Binding rules

1. Every component is pinned to an exact repository and 40-character Git commit SHA. Floating branches, tags, `main`, `latest`, or similar aliases are invalid bindings.
2. Component versions and contract identifiers may be recorded when the component publishes them, but a version label never substitutes for the exact commit.
3. Exactly one `GOVERNANCE_FRAMEWORK` is present and it is General Governance.
4. Governance components declare `OWN_DOMAIN_ONLY`; evidence/observability components declare `NONE` for governance authority.
5. Composition does not imply compatibility, conformance, authority transfer, acceptance, or release readiness.
6. An `ACTIVE` stack requires adopter-owned compatibility evidence for the exact bound component set. A `PREPARED` stack may exist before that evidence is complete but grants no implementation authority by itself.
7. A component's own conformance rules and validator remain authoritative for that component. The composition validator checks only stack identity, role separation, and activation evidence; it does not reinterpret component semantics.
8. Upgrading one component does not silently upgrade another. Any changed component SHA creates a new stack identity/evaluation context.

## Protected implementation boundary

This composition decision does not change CWG. Accepted CWG already permits ordinary implementation activity inside a proven isolation boundary that cannot affect the governed repository/candidate; governance then applies at the isolated-to-shared transition. A project may therefore use an isolated implementation workspace and govern promotion/publication/integration without treating every internal file edit as a distinct protected effect.

This does not permit a free-running agent to mutate a governed shared target under a broad admission. Any mutation that can reach a governed target remains subject to CWG's accepted exact-boundary and channel-classification requirements.

## AET boundary

AET observations are evidence inputs only. AET does not authorize work, decide CWG policy, establish Owner acceptance, or make provider observations authoritative beyond their demonstrated predicates. Raw project/governance content must continue to respect AET's own privacy contract.

## Proportionality

No named risk-tier taxonomy is introduced by this decision. Scope/materiality and CWG governed-subject semantics remain unchanged. Whether the framework later needs a small reusable assurance/protection profile controlling review/validation depth remains an open design question and is not required to activate the composition contract.

## Non-goals

This decision does not:

- merge GG, CWG, or AET repositories;
- make CWG or AET submodules owned by GG;
- modify CWG G0-G6 or the AET telemetry contract;
- create a plugin runtime or dynamic module loader;
- require CWG to register every adopter;
- introduce risk scoring or R1/R2/R3 tiers;
- select Claude, Codex, or another provider as normative architecture;
- authorize Dopis or SVP implementation by itself.

## Minimal adopter flow

1. Pin the exact GG/CWG/AET revisions required by the project.
2. Record them in one adopter-owned capability-stack document.
3. Establish one bounded compatibility/conformance result for that exact set.
4. Mark the stack `ACTIVE` only after that evidence exists.
5. Execute project work using each component only within its own authority domain.

No additional composition lifecycle is required.
