# Concurrent-work adoption scaffold

Status: **NON-NORMATIVE ADOPTER SCAFFOLD**

This directory is a reusable starting point for projects that choose to activate concurrent repository work. It does **not** make concurrency mandatory and it does not redefine or vendor Concurrent Repository Work Governance (CWG) or Agent Orchestrator (AO).

Normative/runtime sources remain external and must be pinned explicitly by each adopter:

- CWG: `Sugar144/concurrent-repository-work-governance`
- AO: `Sugar144/agent-orchestrator`

The first validated adopter/reference implementation is `Sugar144/check4fun`, whose project-specific concurrency layer lives under `.check4fun/concurrency/`.

## Activation rule

Do not copy this scaffold into every project pre-emptively. A project may remain linear indefinitely. Instantiate the scaffold only when the Owner decides that two or more work streams should execute concurrently.

A project that activates it should create one project-local concurrency directory (for example `.<project>/concurrency/`) containing:

- an adopter mapping derived from `adoption.template.json`;
- one packet per active/planned stream derived from `stream.template.json`;
- explicit generation contracts where producer/consumer compatibility needs a semantic currentness boundary;
- a project-local validator against `work-packet.schema.json` or a stricter adopter schema;
- project-owned integration automation that applies the pinned CWG/AO semantics.

## Minimal operating model

1. One stream owns one non-main branch.
2. Mutations are bounded to declared writable targets.
3. Unknown or unproven conflicts fail closed as `EXCLUSIVE_EFFECT`.
4. Integration to `main` is `ORDERED_EFFECT` and fenced by the exact expected target head.
5. Green CI is validation evidence, not merge authority.
6. Cross-stream semantic dependencies use explicit contract generations; disjoint paths alone are not sufficient proof of compatibility.
7. After integration changes the target generation, any shared control-plane fence that still references the previous generation must be revalidated/re-anchored before another governed integration.

## Context-economy rule

Concurrency must not become a new bootstrap-context tax. An executor should normally read only:

- the adopter mapping;
- its own stream packet;
- the contract generations referenced by that packet;
- the bounded project state required by the task.

Other stream packets, historical integration evidence, and unrelated contracts are on-demand context, not mandatory bootstrap input.

## Reference implementation

Use Check4Fun as an implementation example, not as a copy-paste source of project semantics. Names such as `fp-curriculum`, branches, target paths, stream letters, contract generations, and workflow identifiers are adopter-owned values.
