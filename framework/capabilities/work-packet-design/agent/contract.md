---
document_id: GOV-L2-WORK-PACKET-DESIGN-AGENT-LAYER-001
capability_id: work-packet-design-dependency-closure
agent_layer_version: 1.0.0
status: NORMATIVE_CONTRACT_PENDING_RELEASE_INTEGRATION
derived_from_design_record: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md
wpdc_capability_contract: framework/capabilities/work-packet-design/contract.md
wpdc_capability_contract_version: 1.0.0
wpdc_adoption_contract: framework/capabilities/work-packet-design/adoption-contract.md
wpdc_adoption_contract_version: 1.0.0
---

# Work Packet Design Agent Layer — Boundary Contract

## 1. Purpose and derivation

This document is the General-Governance-owned, provider-neutral boundary contract for the WPDC agent layer: the two semantic roles `work-packet-designer` and `work-packet-reviewer` defined beside this file at `work-packet-designer/role.md` and `work-packet-reviewer/role.md`.

It materializes exactly the decisions settled by the accepted design record named in the front matter. It restates no WPDC normative vocabulary, invariant, resolution enum, disposition rule, or schema field list. Every normative statement below is subordinate to, and must be read together with:

- `framework/capabilities/work-packet-design/contract.md` (WPDC normative capability contract, version declared above);
- `framework/capabilities/work-packet-design/adoption-contract.md` (WPDC adoption contract, version declared above);
- `contracts/work-packet-capability-binding.schema.json`, `contracts/work-packet-manifest.schema.json`;
- `tools/validate_work_packet.py`.

If any statement in this document or in either role file appears to diverge from a cited WPDC contract, the cited WPDC contract governs and the diverging text is in error and must be corrected; it is not a competing interpretation.

## 2. Roles are semantic actors, not new authority

`work-packet-designer` and `work-packet-reviewer` are semantic-process roles. Neither role:

- replaces, forks, narrows, or widens the WPDC normative capability contract or adoption contract;
- replaces or reimplements `tools/validate_work_packet.py` or either machine schema;
- creates execution, mutation, publication, merge, release, acceptance, retry, or replacement authority (WPDC-009; `contract.md` §12 "Authority boundary");
- substitutes for Project Owner authority, adopter authority, or an applicable independent review process (`framework/core/project-operating-contract.md`, "Authority boundaries and preview-first workflow").

A packet disposition (`PACKET_INVALID`, `VALID_BUT_BLOCKED`, `VALID_DEPENDENCY_CLOSED`) produced with either role's help remains exactly what WPDC §6 defines it as: a semantic/conformance classification, never `AUTHORIZED_TO_EXECUTE`.

## 3. Responsibility boundary

The Designer role operationalizes semantic discovery and packet construction; it is the actor that produces a candidate work packet and, where applicable, its machine-projection claims. Its workflow boundaries are fixed exactly by `work-packet-designer/role.md`.

The Reviewer role independently challenges an existing candidate packet for semantic dependency completeness and packet-boundary correctness. It does not design a packet from a blank state. Its responsibilities are fixed exactly by `work-packet-reviewer/role.md`.

Both roles are bound by the same WPDC vocabulary and the same deterministic validator; they differ in stance (constructive versus adversarial) and in which artifact each is trusted to originate.

## 4. Reference-binding requirement

Both roles MUST treat the following as authoritative and MUST reference them by exact path and exact version rather than restate their content:

- WPDC normative contract: `framework/capabilities/work-packet-design/contract.md`, declaring the exact `capability_contract_version` used;
- WPDC adoption contract: `framework/capabilities/work-packet-design/adoption-contract.md`, declaring the exact `adoption_contract_version` used;
- work-packet machine schema(s): `contracts/work-packet-capability-binding.schema.json`, `contracts/work-packet-manifest.schema.json`, declaring exact `binding_schema_version` / `manifest_schema_version`;
- deterministic validator: `tools/validate_work_packet.py`, invoked as an external check, never reimplemented inline.

Neither role definition may embed a copy of WPDC invariant text, the resolution enum, the disposition precedence rule, or the schema field list. Where a role needs to state "run the deterministic validator," it names the tool path and expected exit/disposition contract; it does not restate what the validator checks.

If the referenced contract, adoption contract, schema, or validator version changes, both role definitions require a currentness re-check before continued use (mirrors WPDC §14 "Version and change boundary" and the adoption contract's §12 "Adoption currentness and re-evaluation").

## 5. Independence rule

- The Designer's output MAY be reviewed by the Reviewer.
- The Reviewer MUST NOT silently become a correction executor: on finding a defect, the Reviewer records the finding and a disposition recommendation; it does not itself rewrite the packet to make its own finding disappear. Correction remains the Designer's (or an accountable human's) action, subject to its own re-validation (`framework/core/project-operating-contract.md`, "Authority boundaries and preview-first workflow"; "Versioned formal-run correction identity").
- Independent Reviewer execution is mandatory whenever an existing applicable adopter/project governance, risk, assurance, authority, or review boundary requires independent review for the packet at hand. Where such existing governance instead permits proportional judgment (WPDC `contract.md` §9), the agent layer uses that existing boundary rather than creating a WPDC-specific review policy of its own; a packet within that proportional-judgment space MAY be Designer-self-checked without a separate Reviewer pass.
- This contract fixes no numeric or universal materiality threshold of its own, consistent with WPDC's refusal to prescribe universal freshness/materiality intervals (WPDC §3.6). If a packet is materially dependent on independent review and no applicable governing boundary can determine whether independent review is required, the agent layer MUST stop and escalate rather than invent a threshold to resolve the ambiguity.
- Designer self-review never substitutes for an independently required Reviewer pass under the rule above; it is a compensating control available only within the proportional-judgment space, not an alternative to a governance-mandated independent review.

## 6. Provider-neutrality

Canonical content under `framework/capabilities/work-packet-design/agent/**` MUST be:

- plain, provider-neutral prose (no vendor-specific frontmatter schema, tool-call syntax, or skill-invocation convention);
- expressed in terms of "the acting agent" or "the Designer/Reviewer process," never a specific product name;
- free of any assumption about a specific runtime's file discovery convention, slash-command surface, or tool permission model.

Provider-specific installation or projection — for example, generating a Claude Code `SKILL.md` with its frontmatter, a Cursor rule file, or any other runtime-specific artifact from the canonical `role.md` content — is explicitly outside canonical WPDC semantics. It is adopter/integration tooling that projects the canonical source, exactly as the adoption contract separates adopter-owned projection from GG-owned reusable semantics (`adoption-contract.md` §3 "Ownership boundary", §10 "Packet projection target"). This contract does not create, name, or authorize any such projection mechanism.

## 7. Evidence boundary

Semantic-agent evidence (a Designer's discovery rationale, a Reviewer's finding record, either role's self-adversarial-check note) and deterministic-validator evidence (`tools/validate_work_packet.py` output: schema pass/fail, graph traversal result, evidence-digest checks, disposition) are and remain distinct evidence classes. Neither substitutes for the other:

- a deterministic `PASS` does not establish that Designer discovery was semantically complete, and does not prevent a Reviewer from returning a semantic finding that yields `PACKET_INVALID` (WPDC §7, penultimate paragraph);
- semantic confidence from either role MUST NOT override a deterministic contract failure without correcting the represented packet (WPDC §7, final paragraph);
- a role's own narrative confidence is not, by itself, evidence sufficient under WPDC-006; only the evidence artifacts and bindings the packet actually cites satisfy that requirement.

Both roles MUST label which evidence class a given claim rests on when the two could otherwise be conflated (e.g., "the validator confirmed no cycle exists" versus "the Reviewer judges this dependency set complete").

## 8. Version and change boundary

This is agent-layer boundary contract version `1.0.0`. It derives from WPDC capability contract `1.0.0` and adoption contract `1.0.0` as declared in the front matter.

Any change that modifies the responsibility boundary, the reference-binding requirement, the independence rule, the provider-neutrality clause, or the evidence boundary is a semantic change to this contract and requires explicit version/change disposition. A change to the WPDC normative contract, adoption contract, or machine schema versions this contract references requires a currentness re-check of this contract and both role files before continued use.
