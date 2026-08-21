---
record_id: GG-WPDC-AGENT-SKILL-001-AUTH-002
record_type: BOUNDED_IMPLEMENTATION_AUTHORITY
status: ACTIVE_PROSPECTIVE
block_id: GG-WPDC-AGENT-SKILL-001
packet_id: GG-WPDC-AGENT-SKILL-001-P2
durable_block_authorization: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md
predecessor_commit: 2ecb0335003f33cdab3f0fa7ff3b5536041c9077
predecessor_branch: method/wpdc-agent-skill-001-design
implementation_branch: method/wpdc-agent-skill-001-implementation
canonical_base: 09d678374c310d67a7ce56ef536dce6d94caef01
authorization_date: 2026-08-21
---

# Bounded Implementation Authority — WPDC Agent Skill Implementation (P2)

## Source of authority

This packet does not introduce a new Project Owner authorization. It exercises the implementation portion of the durable Block 4 delegation already recorded at `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md`:

> Block 4 — WPDC Agent Skill Design & Implementation — is Owner-authorized through bounded design, implementation, validation, review, correction, publication, and merge, subject to its declared gates.

That record's "Packet scope" section explicitly reserves implementation for "a separately bounded follow-on packet whose write surface is exactly the 'Proposed implementation write surface' identified in `design.md`, and only after this design packet passes the declared next gate (`INDEPENDENT_REVIEW_OF_GG_WPDC_AGENT_SKILL_001_P1`)." This packet is that follow-on packet, `GG-WPDC-AGENT-SKILL-001-P2`.

This record does not widen, relabel, or substitute for the durable Block 4 authorization; it documents this specific bounded sub-packet's write surface, grounding, and stop conditions, consistent with that authorization's "Merge authority boundary" section, which requires each bounded sub-packet to independently pass its own declared acceptance gates.

## Bound inputs

Unchanged from the durable Block 4 authorization; in particular:

- the accepted P1 design record, `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md`, at predecessor commit `2ecb0335003f33cdab3f0fa7ff3b5536041c9077` — authoritative for agent-layer architecture; not redesigned by this packet;
- the WPDC normative capability contract `framework/capabilities/work-packet-design/contract.md`, version `1.0.0`;
- the WPDC adoption contract `framework/capabilities/work-packet-design/adoption-contract.md`, version `1.0.0`;
- the work-packet machine schemas and `tools/validate_work_packet.py`;
- the required canonical base `09d678374c310d67a7ce56ef536dce6d94caef01`.

## Allowed write surface for this packet

Exactly the paths named by `design.md` §13 ("Proposed minimal write surface for the next implementation packet"), plus this packet's own governance record path:

- `framework/capabilities/work-packet-design/agent/contract.md`;
- `framework/capabilities/work-packet-design/agent/work-packet-designer/role.md`;
- `framework/capabilities/work-packet-design/agent/work-packet-reviewer/role.md`;
- `tests/fixtures/work-packet-agent/cases.md`;
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P2/**`.

No other path may change.

## Forbidden scope

Unchanged from `design.md` §13 and the durable Block 4 authorization's forbidden-scope pattern: this packet MUST NOT touch `release-manifest.json`, `RELEASE_VERSION`, the WPDC normative/adoption contracts, the machine schemas, `tools/validate_work_packet.py`, CI workflows, or any SVP path; MUST NOT create a Claude-, Codex-, Cursor-, SVP-, or other provider/adopter-specific projection; and MUST NOT begin semantic empirical validation or independent review of its own output in this same session.

## Stop and escalation conditions

Inherited from the durable Block 4 authorization, unchanged. In particular: write-surface drift beyond the allowed surface above, canonical-base or currentness drift, any proposed change to an accepted WPDC normative invariant, or any proposed effect on SVP or another consumer.

## Next gate

`GG_WPDC_AGENT_SKILL_001_P3_FRESH_SESSION_SEMANTIC_VALIDATION`, per this packet's own bounded scope. This record does not authorize P3.
