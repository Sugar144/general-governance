---
name: work-packet-designer
description: Use this skill when constructing or evaluating a candidate work packet under Work Packet Design & Dependency Closure (WPDC) — General Governance's framework for turning an intended outcome into a dependency-closed, deterministically validated unit of work. Trigger it when the user is designing, drafting, or shaping a WPDC-governed work packet; discovering undeclared REACH/VALIDATE/COMPLETE prerequisites; determining the smallest coherent dependency-closed cut for a packet; deciding how a prerequisite should resolve (IN_PACKET, PREEXISTING_SATISFIED, BOUND_EXTERNAL_SATISFIED, or UNRESOLVED); or preparing a packet/manifest for tools/validate_work_packet.py. This is the constructive, packet-authoring role — it is not a generic project planner, task breakdown tool, or general work-estimation skill, and it does not apply outside an already-adopted WPDC context.
---

# Work Packet Designer

Operational entrypoint for the `work-packet-designer` semantic role. This file is intentionally thin: the actual role definition, workflow stages, and judgment principles live in canonical General Governance sources below. Read them before acting — do not attempt to construct a packet from this file alone.

## Before you start

1. Resolve the applicable WPDC context: the adopted WPDC capability-contract/adoption-contract versions in force, the adopter's declared source bindings, and the immutable canonical base the packet is evaluated against. If none of this has been supplied or can be resolved from bound sources, stop and say so rather than guessing.
2. Read, in order:
   - `framework/capabilities/work-packet-design/agent/contract.md` — the agent-layer boundary contract (what this role is and is not authorized to do).
   - `framework/capabilities/work-packet-design/agent/work-packet-designer/role.md` — the full Designer role definition: inputs, the ordered Stage 0–8 workflow, mandatory discovery cross-checks, cross-cutting judgment principles, stop/escalation conditions, and outputs. This is the authoritative source for how to do the work; this file only orients you toward it.
   - Where a cited WPDC provision is unfamiliar, the underlying normative sources it derives from: `framework/capabilities/work-packet-design/contract.md` (WPDC capability contract) and `framework/capabilities/work-packet-design/adoption-contract.md` (adoption contract). Consult these only to resolve a specific ambiguity `role.md` doesn't settle — they are not a substitute for reading `role.md` first.

## What this skill is for

Use it to construct, or evaluate the semantic soundness of, a candidate WPDC work packet: discovering undeclared REACH/VALIDATE/COMPLETE prerequisites, testing reachability/validation/truthful-completion coverage, shaping the smallest coherent dependency-closed cut, and preparing a packet for deterministic validation. It is not a generic task-decomposition or project-planning skill, and it has no authority outside an already-adopted WPDC context — if WPDC has not been adopted for the work at hand, this skill does not apply.

## Non-negotiable operating rules

These are load-bearing enough to restate here even though `role.md` is authoritative; if this summary and `role.md` ever disagree, `role.md` governs.

- **Follow the Stage 0–8 workflow in `role.md`** in order — resolve authority and sources, derive intended outcomes, discover prerequisites recursively across all three of REACH/VALIDATE/COMPLETE, select a resolution for each, shape the smallest dependency-closed cut, bind evidence, produce any machine projection, run the deterministic validator, then perform the final adversarial check.
- **Run all four mandatory discovery cross-checks.** Before freezing the dependency model, perform the role's **Local/external seam split**, **Surface-to-node closure**, **Integration-edge closure**, and **Validation-reachability closure** checks. Repeat them whenever graph/boundary claims change and again during Stage 8. A local adapter/interface/ledger/schema required to consume owner/external state must not disappear into an `UNRESOLVED` owner-state node; a declared execution/effect/persistence/validation surface must not be orphaned from a producing/enabling node; semantically required component dependencies must have explicit edges; and validation prerequisites must be able to reach every surface their bound methods require.
- **Run the deterministic validator** (`tools/validate_work_packet.py`) against the packet through its governed invocation, and treat its result as authoritative for whatever it is designed to check. Do not let confidence override a deterministic failure.
- **Preserve `UNRESOLVED` honestly.** When a real prerequisite cannot be truthfully resolved from bound sources, represent it as `UNRESOLVED` rather than fabricating a satisfied resolution to reach closure. `VALID_BUT_BLOCKED` is a legitimate terminal state, not a process failure.
- **Perform the Stage 8 final adversarial check** before declaring the packet complete. Re-run the four mandatory discovery cross-checks adversarially across the outcome and recursive prerequisite graph. If a material issue is found, return to semantic discovery/representation, correct prospectively, repeat deterministic Stage 7 on the corrected bytes, then repeat Stage 8.
- **Treat Stage 8 no-findings as bounded evidence only.** It may say the self-challenge completed with no findings; it must not say or imply that no material dependency is missing, that dependency discovery is complete, or that the graph is semantically exhaustive. Stage 8 never substitutes for an independently required Reviewer pass.
- **Never infer execution authority from dependency closure.** A `VALID_DEPENDENCY_CLOSED` (or any other) disposition is a semantic/conformance classification only. It never confers execution, publication, merge, release, acceptance, retry, or replacement authority, and it never substitutes for Project Owner, adopter, or independent-review authority.
- **Stop and escalate** rather than resolve unilaterally when a required authority/source ambiguity can't be resolved from bound sources, when closing the packet would require changing an accepted WPDC normative invariant, or when independent Reviewer execution appears required but the governing boundary for that can't itself be resolved.

## Output

A completed pass produces the candidate packet (outcomes, prerequisites, dependency edges, resolutions, exclusions, evidence bindings, execution boundary, stop conditions), its machine projection where applicable, the validator's exact invocation and disposition, and the Stage 8 self-adversarial note — exactly as `role.md` §6 defines. Label which evidence class each claim rests on (validator output vs. semantic judgment); the two are distinct and neither substitutes for the other (`contract.md` §7). A Stage 8 no-finding note is bounded self-challenge evidence, never a semantic-completeness warrant.
