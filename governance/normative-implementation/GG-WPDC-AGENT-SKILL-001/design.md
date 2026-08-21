---
document_id: GOV-WPDC-AGENT-SKILL-DESIGN-001
packet_id: GG-WPDC-AGENT-SKILL-001-P1
block_id: GG-WPDC-AGENT-SKILL-001
status: DESIGN_CANDIDATE_PENDING_INDEPENDENT_REVIEW
authorization_record: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md
canonical_base: 09d678374c310d67a7ce56ef536dce6d94caef01
wpdc_capability_contract_version: 1.0.0
wpdc_adoption_contract_version: 1.0.0
wpdc_manifest_schema_version: 1.0.0
wpdc_binding_schema_version: 1.0.0
---

# WPDC Agent Layer — Design Contract

## 1. Purpose and derivation

This document is the canonical design contract for the reusable, provider-neutral General Governance agent layer that operationalizes Work Packet Design & Dependency Closure (WPDC) through two distinct semantic roles: `work-packet-designer` and `work-packet-reviewer`.

Every normative statement below is derived from, and subordinate to:

- `framework/capabilities/work-packet-design/contract.md` (WPDC normative capability contract `1.0.0`), especially §7 "Semantic and deterministic responsibility split" and §11 "Human and machine artifact relationship";
- `framework/capabilities/work-packet-design/adoption-contract.md` (WPDC adoption contract `1.0.0`);
- `docs/architecture/work-packet-design-dependency-closure.md`, especially its "Agent / deterministic split" section and its "Candidate implementation topology" step 4, "Skill-specialist handoff";
- `contracts/work-packet-capability-binding.schema.json` and `contracts/work-packet-manifest.schema.json`;
- `tools/validate_work_packet.py`.

This design contract restates no WPDC normative vocabulary, invariant, or disposition rule. Where a rule is needed, it is cited by section reference rather than duplicated. If a citation and this document ever appear to diverge, the cited WPDC contract governs and this document is in error and must be corrected.

This design contract does not authorize implementation. It settles the design decisions required before a separately gated implementation packet may materialize `framework/capabilities/work-packet-design/agent/**`.

## 2. Roles are semantic actors, not new authority

`work-packet-designer` and `work-packet-reviewer` are semantic-process roles, analogous to the "Packet Designer" and "Packet Reviewer" already named (but not designed) in the accepted architecture's "Agent / deterministic split" section. Neither role:

- replaces, forks, narrows, or widens the WPDC normative capability contract or adoption contract;
- replaces or reimplements `tools/validate_work_packet.py` or either machine schema;
- creates execution, mutation, publication, merge, release, acceptance, retry, or replacement authority (WPDC-009; `framework/capabilities/work-packet-design/contract.md` §12 "Authority boundary");
- substitutes for Project Owner authority, adopter authority, or an applicable independent review process (`framework/core/project-operating-contract.md`, "Authority boundaries and preview-first workflow").

A packet disposition (`PACKET_INVALID`, `VALID_BUT_BLOCKED`, `VALID_DEPENDENCY_CLOSED`) produced with either role's help remains exactly what WPDC §6 defines it as: a semantic/conformance classification, never `AUTHORIZED_TO_EXECUTE`.

## 3. Canonical provider-neutral source layout

The reusable GG-owned source for the agent layer lives under:

```
framework/capabilities/work-packet-design/agent/
├── contract.md
├── work-packet-designer/
│   └── role.md
└── work-packet-reviewer/
    └── role.md
```

- `contract.md` is the GG-owned agent-layer boundary contract: it states the responsibility boundary (§4), the reference-binding requirement (§5), the independence rule (§7), and the provider-neutrality clause (§8) as normative prose, versioned independently (starting `1.0.0`) from the WPDC capability contract it derives from.
- `work-packet-designer/role.md` and `work-packet-reviewer/role.md` are the provider-neutral normative role definitions for each skill: responsibilities, workflow boundaries, inputs, outputs, and stop conditions, written as prose a competent human or any capable model-driven agent can execute without a specific runtime's tool-call syntax or frontmatter schema.

Semantic test/fixture material is deliberately **not** placed under `agent/`. It lives beside the existing WPDC deterministic fixtures as a sibling family (§9), preserving the existing repository pattern of separating normative source from fixture/regression material.

No file under this layout may declare a runtime, provider, or tool-invocation convention specific to Claude, Codex, Cursor, or any other agent runtime. See §8.

## 4. Responsibility boundary between Designer and Reviewer

### 4.1 `work-packet-designer`

The Designer role **operationalizes** semantic discovery and packet construction: it is the actor that produces a candidate work packet and, where applicable, its machine-projection claims. Its workflow boundaries are fixed exactly to the ordered list in §6.

### 4.2 `work-packet-reviewer`

The Reviewer role **independently challenges** a Designer-produced (or otherwise existing) packet for semantic dependency completeness and packet-boundary correctness. It does not design a packet from a blank state; its input is always an existing candidate packet (and, where available, its machine projection and validator output). Its responsibilities are fixed exactly to the ordered list in §7.

### 4.3 What separates them

The Designer's default posture is constructive: derive the smallest coherent, dependency-closed cut and represent it honestly, including honest `UNRESOLVED` where closure is not achievable. The Reviewer's default posture is adversarial: assume the candidate packet may be wrong and look specifically for the failure classes in §7, including failure classes that a purely constructive process is structurally prone to miss (e.g., a Designer under pressure to reach closure is the actor most likely to under-scope a prerequisite or misclassify external evidence as pre-existing; the Reviewer exists precisely to check that pressure).

Both roles are bound by the same WPDC vocabulary and the same deterministic validator; they differ in stance and in which artifact they are trusted to originate.

## 5. How both roles reference canonical GG sources

Both roles MUST treat the following as authoritative and MUST reference them by exact path and exact version rather than restate their content:

- WPDC normative contract: `framework/capabilities/work-packet-design/contract.md` (declare the exact `capability_contract_version` used, e.g. `1.0.0`);
- WPDC adoption contract: `framework/capabilities/work-packet-design/adoption-contract.md` (declare the exact `adoption_contract_version` used);
- work-packet machine schema(s): `contracts/work-packet-capability-binding.schema.json`, `contracts/work-packet-manifest.schema.json` (declare exact `binding_schema_version` / `manifest_schema_version`);
- deterministic validator: `tools/validate_work_packet.py`, invoked as an external check, never reimplemented inline.

A role definition MUST NOT embed a copy of WPDC invariant text, the resolution enum, the disposition precedence rule, or the schema field list. Where a role needs to state "run the deterministic validator," it names the tool path and expected exit/disposition contract; it does not restate what the validator checks.

If the referenced contract, adoption-contract, schema, or validator version changes, both role definitions require a currentness re-check before continued use (mirrors WPDC §14 "Version and change boundary" and the adoption contract's §12 "Adoption currentness and re-evaluation").

## 6. Designer workflow boundaries

The Designer's workflow is fixed to exactly these ordered stages, each bounded by the cited WPDC semantics:

1. **Intended outcomes** — derive bounded included outcomes from the adopter's bound authority/requirements/architecture sources (WPDC §3.1, §5 WPDC-001). The Designer does not invent outcomes unsupported by an authoritative adopter source.
2. **Semantic `REACH`, `VALIDATE`, and `COMPLETE` prerequisite discovery** — for each included outcome, discover every prerequisite known to the Designer's available sources to be required to reach, validate, or truthfully complete it, and classify each discovered edge as `REACH`, `VALIDATE`, or `COMPLETE` (WPDC §3.4, WPDC-003). The Designer MUST NOT claim that an undiscovered edge does not exist merely because none was found.
3. **Prerequisite-resolution selection** — for each discovered prerequisite, select exactly one of `IN_PACKET`, `PREEXISTING_SATISFIED`, `BOUND_EXTERNAL_SATISFIED`, or `UNRESOLVED` (WPDC §4), honoring the mutual exclusivity of `PREEXISTING_SATISFIED` and `BOUND_EXTERNAL_SATISFIED` (WPDC-006) and never selecting a satisfied resolution merely to avoid `UNRESOLVED`.
4. **Smallest coherent dependency-closed cut** — shape the packet's included-outcome set to the smallest coherent result-producing boundary that can be made dependency-closed and truthfully completable, without absorbing materially independent outcomes (WPDC-012).
5. **Evidence/context binding** — for every `PREEXISTING_SATISFIED` or `BOUND_EXTERNAL_SATISFIED` resolution, bind durable evidence to the immutable canonical-base identity and/or the applicable state evaluation context and currentness boundary (WPDC §3.5, §3.6, WPDC-006, WPDC-011). The Designer MUST NOT treat an immutable repository SHA as proof of mutable or external state.
6. **Machine representation** — where a machine projection is produced, project only the bounded claim set defined by the manifest schema; the Designer MUST NOT copy full requirements/architecture prose, chain-of-thought, or synthetic authorization booleans into it (WPDC §11).
7. **Deterministic validation** — run `tools/validate_work_packet.py` against the produced packet/manifest and treat its result as authoritative for every claim it is designed to check; a deterministic failure is not overridden by Designer confidence (WPDC §7, final paragraph).
8. **Final adversarial missing-dependency check** — before declaring the packet complete, the Designer performs one explicit self-adversarial pass asking "what prerequisite would make this outcome unreachable, unvalidatable, or dishonestly complete that I have not represented?" This stage exists because WPDC-003 explicitly forbids deterministic tooling from proving the absence of an undeclared edge; it is a designed compensating control, not a formal guarantee, and does not substitute for independent Reviewer challenge under §7 when proportionate.

The Designer MUST stop and represent `UNRESOLVED` (never fabricate a resolution) when a required prerequisite cannot be truthfully resolved from bound sources, and MUST stop and escalate rather than resolve a required authority/source ambiguity the same way the adoption contract requires (adoption contract §7 "Bounded source resolution").

## 7. Reviewer responsibilities

The Reviewer's review is fixed to detecting, at minimum, each of the following failure classes, each bound to the WPDC rule it protects:

1. **Missing prerequisite nodes/edges** — a `REACH`, `VALIDATE`, or `COMPLETE` dependency that should exist but is absent from the graph (WPDC-003, WPDC-004).
2. **Incorrect prerequisite resolution** — a resolution that does not match its actual evidence class, e.g. an `IN_PACKET` claim for something never produced by the packet, or an `UNRESOLVED` claim for something actually evidenced (WPDC §4, WPDC-005).
3. **Misuse of `EXCLUDED`** — any exclusion that contradicts a live dependency edge: excluding a required, unsatisfied prerequisite while its dependent included outcome remains included (WPDC-008).
4. **Mutable/external truth misclassification** — `PREEXISTING_SATISFIED` claimed for something that actually depends on a separately identified external dependency, or a mutable-state claim asserted without a valid state evaluation context/currentness boundary (WPDC-006, WPDC §3.6, WPDC-011).
5. **Over-aggregation** — an included-outcome set that absorbs materially independent outcomes not required by dependency closure or another explicit governing constraint (WPDC-012).
6. **Authority fabrication** — any packet content, prose, or machine claim that implies WPDC disposition confers execution, publication, merge, release, acceptance, retry, or replacement authority (WPDC-009; `contract.md` §12).
7. **Historical-truth rewriting** — any attempt to edit, reclassify, or silently supersede an immutable completed packet, run, or evidence record rather than create a new versioned/superseding record (`framework/core/project-operating-contract.md`, "Failure, learning, and immutability" and "Versioned formal-run correction identity").
8. **Unjustified semantic completeness claims** — any assertion that dependency discovery is complete, or that no undeclared dependency exists, that is not itself something the applicable contract allows to be established deterministically (WPDC-003's explicit prohibition on tooling claiming discovery-completeness).

The Reviewer records each finding against the packet, cites the WPDC section/invariant it violates, and returns a disposition recommendation. It does not invent a ninth failure class outside this list without a design amendment, though it MAY report an observation outside this list as non-blocking commentary distinct from a finding.

## 8. Independence rule

- The Designer's output MAY be reviewed by the Reviewer.
- The Reviewer MUST NOT silently become a correction executor: on finding a defect, the Reviewer records the finding and a disposition recommendation; it does not itself rewrite the packet to make its own finding disappear. Correction remains the Designer's (or an accountable human's) action, subject to its own re-validation, mirroring the existing General Governance pattern that no actor inherits another actor's authority (`framework/core/project-operating-contract.md`, "Authority boundaries and preview-first workflow") and the WPDC precedent that a correction of an immutable result requires its own explicit authorization and independent evaluation ("Versioned formal-run correction identity").
- Review independence is required only when materiality/risk justifies it. WPDC itself anchors this proportionality: "validation sufficiency requires domain judgment, that judgment remains semantic and may require independent review proportionate to the risk/materiality of the packet" (`contract.md` §9). A low-materiality packet MAY be Designer-self-checked (§6 stage 8) without a separate Reviewer pass; a packet whose closure claim affects execution admission, an irreversible effect, or a materially ambiguous authority/evidence question SHOULD receive an independent Reviewer pass before that claim is relied upon. This design does not fix one universal materiality threshold; the applicable adopter/project authority determines it, consistent with WPDC's refusal to prescribe universal freshness/materiality intervals (WPDC §3.6).

## 9. Provider-neutrality

Canonical content under `framework/capabilities/work-packet-design/agent/**` MUST be:

- plain, provider-neutral prose (no vendor-specific frontmatter schema, tool-call syntax, or skill-invocation convention);
- expressed in terms of "the acting agent" or "the Designer/Reviewer process," never a specific product name;
- free of any assumption about a specific runtime's file discovery convention, slash-command surface, or tool permission model.

Provider-specific installation or projection — for example, generating a Claude Code `SKILL.md` with its frontmatter, a Cursor rule file, or any other runtime-specific artifact from the canonical `role.md` content — is explicitly **outside** canonical WPDC semantics. It is adopter/integration tooling that projects the canonical source, exactly as the adoption contract already separates adopter-owned projection from GG-owned reusable semantics (`adoption-contract.md` §3 "Ownership boundary", §10 "Packet projection target"). This design packet does not create, name, or authorize any such projection mechanism; that remains a later, separately authorized, adopter-facing concern if and when it is needed.

## 10. Semantic test/fixture strategy

Semantic-agent fixtures test model judgment, not deterministic code; they are therefore a distinct family from `tests/fixtures/work-packet/cases.json` (which `tools/validate_work_packet.py`'s pytest suite executes deterministically). The proposed location is:

```
tests/fixtures/work-packet-agent/cases.md
```

a human-readable, adopter-neutral scenario catalog (scenario id, bounded scenario description, the correct Designer and/or Reviewer judgment, and the WPDC rule it exercises) — not an automated pytest suite, since grading model judgment deterministically is out of scope for this design and would risk manufacturing false determinism over a semantic question (WPDC §7's own warning against deterministic tooling overclaiming semantic judgment applies equally to grading the agents that produce semantic judgment).

At minimum, the catalog MUST cover these scenario families, each adopter-neutral (no SVP or other adopter-specific vocabulary, per the architecture's "Regression model" precedent):

1. **Missing `REACH`** — a prerequisite genuinely necessary to reach an outcome is absent from a candidate graph; correct behavior is to discover and add it (§6 stage 2; WPDC-003).
2. **Honest `UNRESOLVED`** — a real prerequisite exists with no available satisfying evidence; correct behavior is `UNRESOLVED`, not a fabricated resolution (WPDC §4.4, WPDC-007).
3. **Immutable `PREEXISTING_SATISFIED`** — a prerequisite is satisfied purely by immutable canonical-base content; correct behavior is `PREEXISTING_SATISFIED` bound to that canonical identity (WPDC §4.2).
4. **Mutable state requiring state/currentness evidence** — a prerequisite depends on adopter-owned mutable state; correct behavior requires a state evaluation context and currentness boundary, not a bare canonical-base citation (WPDC §3.6, WPDC-011).
5. **External dependency requiring `BOUND_EXTERNAL_SATISFIED`** — a prerequisite's satisfaction is supplied by a separately identified external dependency; correct behavior is `BOUND_EXTERNAL_SATISFIED` with bound source identity/evidence/authority, never `PREEXISTING_SATISFIED` (WPDC §4.3, WPDC-006).
6. **Over-aggregation** — a candidate packet bundles a materially independent outcome not required by dependency closure; correct behavior is to flag/reject the bundling (WPDC-012).
7. **Dependency-closed packet without execution authority** — a packet is correctly `VALID_DEPENDENCY_CLOSED`; correct behavior is to state this creates zero execution/publication/merge/release/acceptance authority (WPDC-009, `contract.md` §6.4, §12).
8. **Historical packet defect preservation** — a defect is found in an already-immutable historical packet; correct behavior is a new superseding/correction record, never an edit of the historical artifact (`project-operating-contract.md`, "Failure, learning, and immutability").

This §10 fixes the strategy and minimum coverage only. The catalog file itself is implementation-block work and is not created by this design packet.

## 11. Evidence boundary

Semantic-agent evidence (a Designer's discovery rationale, a Reviewer's finding record, either role's self-adversarial-check note) and deterministic-validator evidence (`tools/validate_work_packet.py` output: schema pass/fail, graph traversal result, evidence-digest checks, disposition) are and remain **distinct evidence classes**. Neither substitutes for the other:

- a deterministic `PASS` does not establish that Designer discovery was semantically complete, and does not prevent a Reviewer from returning a semantic finding that yields `PACKET_INVALID` (WPDC §7, penultimate paragraph);
- semantic confidence — from either role — MUST NOT override a deterministic contract failure without correcting the represented packet (WPDC §7, final paragraph);
- a role's own narrative confidence is not, by itself, "durable evidence bound to the immutable identities, state context, currentness constraints, and applicable authority" required by WPDC-006; only the evidence artifacts and bindings the packet actually cites satisfy that requirement.

Both roles MUST label which evidence class a given claim rests on when the two could otherwise be conflated (e.g., "the validator confirmed no cycle exists" versus "the Reviewer judges this dependency set complete").

## 12. Release consequence

Tracked General Governance content changes the release `content_sha256` identity (`release-manifest.json`, `content_identity_method`). This design packet's three governance-only files fall outside `required_framework_surfaces` and do not, by themselves, change that digest.

The follow-on implementation packet will add tracked content under `framework/capabilities/work-packet-design/agent/**` (and, if the fixture catalog in §10 is adopted as tracked content, under `tests/fixtures/work-packet-agent/**`). Consistent with the precedent set by Blocks 1–3 (`GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001` block-result: "adding tracked framework content changes the release content digest while `release-manifest.json` still identifies immutable release candidate `0.1.0-rc.5`"), that later content changes the tracked-content digest and therefore requires a new release identity rather than a modification of the current immutable `0.1.0-rc.6` candidate (`release-manifest.json`, `release_status: IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION`). This design packet does not select or modify the final release manifest.

## 13. Proposed minimal write surface for the next implementation packet

Exactly, and no more:

- `framework/capabilities/work-packet-design/agent/contract.md`;
- `framework/capabilities/work-packet-design/agent/work-packet-designer/role.md`;
- `framework/capabilities/work-packet-design/agent/work-packet-reviewer/role.md`;
- `tests/fixtures/work-packet-agent/cases.md`;
- its own governance record under `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/` (e.g. a `-P2` packet authorization/result, following this packet's naming pattern).

The implementation packet MUST NOT touch `release-manifest.json`, `RELEASE_VERSION`, the WPDC normative/adoption contracts, the machine schemas, `tools/validate_work_packet.py`, CI workflows, or any SVP path — mirroring exactly the forbidden-scope pattern already proven for Blocks 1 and 2.

## 14. Unresolved material questions carried forward

This design packet settles the decisions listed in its authorizing packet. It explicitly does not settle, and defers to the implementation packet or a later Owner disposition:

- the exact minimum-materiality threshold (§8) that triggers mandatory independent Reviewer review versus Designer self-check alone, beyond the qualitative proportionality rule already stated;
- whether the fixture catalog (§10) should eventually be supplemented by an automatable structural check (e.g., "every scenario id has both a Designer-expected and Reviewer-expected judgment recorded") without attempting to automate the semantic judgment itself;
- whether a future provider-specific projection mechanism (§9) should itself become a separately governed GG-owned optional surface, or remain purely adopter-owned tooling outside General Governance custody.

None of these blocks acceptance of this design packet; they are scoped follow-on questions for the implementation packet's own authorization.
