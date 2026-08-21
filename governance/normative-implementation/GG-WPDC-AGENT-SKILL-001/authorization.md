---
record_id: GG-WPDC-AGENT-SKILL-001-AUTH-001
record_type: PROJECT_OWNER_BLOCK_AUTHORIZATION
status: ACTIVE_PROSPECTIVE
block_id: GG-WPDC-AGENT-SKILL-001
block_name: WPDC Agent Skill Design & Implementation
packet_id: GG-WPDC-AGENT-SKILL-001-P1
branch: method/wpdc-agent-skill-001-design
branch_start_sha: 09d678374c310d67a7ce56ef536dce6d94caef01
main_baseline_at_authorization: 09d678374c310d67a7ce56ef536dce6d94caef01
accepted_architecture_commit_sha: d43950df47d9d01b516a46f63e7ae9f7da1f24f7
accepted_architecture_blob_sha: 0ddf288274c9805a4a00b2d3929e9c7fe6aa12ec
owner_disposition_commit_sha: 88f1be46a3920154e66cad2d64344b9263737c78
authorization_date: 2026-08-21
---

# Project Owner Block Authorization — WPDC Agent Skill Design & Implementation

## Owner authority

The Project Owner's current instruction (packet `GG-WPDC-AGENT-SKILL-001-P1`) states:

> Block 4 — WPDC Agent Skill Design & Implementation — is Owner-authorized through bounded design, implementation, validation, review, correction, publication, and merge, subject to its declared gates.

This is an explicit, finite Project Owner authorization of a bounded work package under the `Bounded operational delegation` semantics of `framework/core/project-operating-contract.md`. It prospectively authorizes the routine mechanics of Block 4 — design, implementation, validation, review, correction, commit, push, pull request, review, exact-candidate integration, and technical closure through merge of the exact passing candidate — without a fresh Owner authorization at each step, strictly within Block 4's stated scope and subject to the stop/escalation conditions below.

It is bounded prospective authority, not unconditional acceptance. A failing or non-conforming candidate MUST NOT be accepted, published, or merged merely because Block 4 was authorized. Owner acceptance of any exact result remains reserved and is never satisfied by a delegated effect.

This authorization does not widen, relabel, or substitute for `OWNER_PUBLICATION_AUTHORIZATION`, which remains the narrow, distinct case defined by `framework/core/project-operating-contract.md`.

## Bound inputs

Block 4 is derived from, and MUST remain faithful to:

- the Owner-accepted WPDC architecture candidate `d43950df47d9d01b516a46f63e7ae9f7da1f24f7` (`docs/architecture/work-packet-design-dependency-closure.md`), in particular its `Candidate implementation topology` step 4, `Skill-specialist handoff`, and its `Agent / deterministic split` section;
- the durable architecture disposition `88f1be46a3920154e66cad2d64344b9263737c78` (`governance/architecture-decisions/GG-WPDC-ARCHITECTURE-001/owner-disposition.md`);
- the accepted WPDC normative capability contract `framework/capabilities/work-packet-design/contract.md`, version `1.0.0`;
- the accepted WPDC adoption contract `framework/capabilities/work-packet-design/adoption-contract.md`, version `1.0.0`;
- the accepted work-packet machine schemas (`contracts/work-packet-capability-binding.schema.json`, `contracts/work-packet-manifest.schema.json`) and deterministic validator `tools/validate_work_packet.py`;
- the required canonical base `09d678374c310d67a7ce56ef536dce6d94caef01` (`origin/main`, General Governance `0.1.0-rc.6`, `release-manifest.json` status `IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION`).

If completing Block 4 requires changing an accepted WPDC semantic invariant rather than merely deriving from it, execution MUST stop for material Owner disposition rather than proceed.

## Bound objective

Materialize the reusable, provider-neutral General Governance agent layer for WPDC — the `work-packet-designer` and `work-packet-reviewer` roles — as design, and later (in a separately gated packet) as implementation, without replacing or forking the WPDC normative contract, adoption contract, or deterministic validator.

## Packet scope: `GG-WPDC-AGENT-SKILL-001-P1`

This packet exercises only the **design** portion of the durable Block 4 delegation recorded above. It produces the canonical design contract for the agent layer. It does not implement, publish, or merge either skill's runnable content.

Implementation, validation, review, correction, publication, and merge of the actual skill content remain authorized under this same durable Block 4 delegation, but MUST occur in a separately bounded follow-on packet whose write surface is exactly the "Proposed implementation write surface" identified in `design.md`, and only after this design packet passes the declared next gate (`INDEPENDENT_REVIEW_OF_GG_WPDC_AGENT_SKILL_001_P1`).

## Allowed write surface for this packet

New or modified content for `GG-WPDC-AGENT-SKILL-001-P1` is limited exactly to:

- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md`;
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md`;
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/work-package.md`.

No other path may change. In particular, this packet MUST NOT create or modify any file under `framework/capabilities/work-packet-design/agent/**` — that surface is reserved for the follow-on implementation packet.

## Forbidden scope

Block 4, including this design packet, MUST NOT:

- modify L0 Project Operating Contract semantics;
- modify the WPDC normative capability contract, adoption contract, machine schemas, or `tools/validate_work_packet.py`;
- fork or duplicate WPDC normative semantics inside agent-layer content;
- modify `release-manifest.json`, `RELEASE_VERSION`, upgrade/evolution contracts, tags, or GitHub Releases;
- adopt WPDC in SVP or any other consumer, or touch any SVP repository, path, packet, or artifact;
- re-evaluate, rewrite, or authorize the existing SVP packet;
- create execution, publication, merge, release, acceptance, retry, or replacement authority through either agent role;
- bind canonical GG agent-layer content to Claude, Codex, Cursor, or another specific runtime/provider;
- implement either skill's runnable content within this design packet (`GG-WPDC-AGENT-SKILL-001-P1`).

## Stop and escalation conditions

Delegated execution under Block 4 MUST stop and escalate to the Project Owner, instead of proceeding under this grant, on encountering any of:

- a change of scope or requirements beyond this authorization;
- a material architectural decision not already settled by the accepted WPDC architecture or contracts;
- risk, security, or privacy acceptance;
- new authority or a material dependency not already bound above;
- write-surface drift beyond the allowed surface stated above;
- a failed or indeterminate gate;
- canonical-base or currentness drift (`origin/main` no longer equal to `09d678374c310d67a7ce56ef536dce6d94caef01` at a step that depends on it);
- any proposed change to an accepted WPDC normative invariant;
- any proposed effect on SVP or another consumer;
- ambiguity that cannot be resolved deterministically from the bound inputs.

Routine corrections that make this packet's content conform more precisely to the bound inputs do not require a new Owner authorization.

## Release consequence acknowledgment

Tracked General Governance content changes the release `content_sha256` identity computed by `tools/validate_work_packet.py` / `tools/validate_consumer.py`. This design packet's three governance-only files are outside `required_framework_surfaces` and outside the release content-identity input set as currently defined, so they do not by themselves change that digest.

The follow-on implementation packet, once it adds tracked content under `framework/capabilities/work-packet-design/agent/**`, WILL change the General Governance tracked-content digest. Consistent with the precedent established by Blocks 1–3 (`GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001`, `GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001`, `GG-RELEASE-PACKAGE-0.1.0-RC.6-001`), that later content therefore requires a new release identity rather than a modification of the immutable `0.1.0-rc.6` candidate. This authorization records that consequence prospectively; it does not select or modify the final release manifest, and no release action is authorized by this record.

## Merge authority boundary

This authorization covers Block 4 end-to-end (design through merge) as a durable prospective grant. It does not itself constitute Owner acceptance of any exact candidate. Each bounded sub-packet (beginning with this design packet, `GG-WPDC-AGENT-SKILL-001-P1`) must independently pass its own declared acceptance gates before any publication or merge action is taken under this grant. The exact next gate for this design packet is `INDEPENDENT_REVIEW_OF_GG_WPDC_AGENT_SKILL_001_P1`; no merge of this packet occurs before that review passes.
