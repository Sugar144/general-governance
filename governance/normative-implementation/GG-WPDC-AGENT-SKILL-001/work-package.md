---
work_package_id: GG-WPDC-AGENT-SKILL-001-P1
block_id: GG-WPDC-AGENT-SKILL-001
authorization_record: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md
status: VALIDATED_PENDING_INDEPENDENT_REVIEW
general_governance_baseline: 09d678374c310d67a7ce56ef536dce6d94caef01
branch: method/wpdc-agent-skill-001-design
---

# Work Package and Output Contract — WPDC Agent Skill Design (P1)

## Objective

Define the canonical design contract for the reusable WPDC agent layer (`work-packet-designer`, `work-packet-reviewer`) as an explicit, provider-neutral General Governance L2-adjacent design surface, derived exclusively from the existing accepted WPDC architecture, normative capability contract, adoption contract, machine schemas, and deterministic validator. Do not implement, publish, or merge either skill's runnable content in this packet, and do not touch SVP.

## Preflight performed

1. Resolved repository root: `/home/sugar/Proyectos/general-governance`.
2. Searched for an applicable `AGENTS.md` (repository root and full tree): none exists at any path. No repository-local operating instructions were found to reconcile against this packet.
3. Fetched `origin/main` and verified its head is exactly `09d678374c310d67a7ce56ef536dce6d94caef01`, matching the required canonical base.
4. Verified the pre-existing checkout (`architecture/bounded-operational-delegation-rc4`, local head `2e20eb0fa90bed83260d2008773c27e7d04fb050`) without modifying it; confirmed it is an ancestor of `origin/main` (`git merge-base` equals the local head) and is unrelated to this packet's write surface.
5. Created an isolated worktree at `../general-governance-wt-wpdc-agent-skill-001-design` on branch `method/wpdc-agent-skill-001-design`, created directly from `09d678374c310d67a7ce56ef536dce6d94caef01`.
6. Confirmed no open remote branch or in-flight work touches `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/**` or `framework/capabilities/work-packet-design/agent/**` (`git ls-remote --heads origin` and `git ls-tree -r origin/main` checked).
7. No stop condition was triggered: `origin/main` matched exactly; no applicable repository instruction was found to contradict the packet; the write surface was clear; no requested step required changing accepted WPDC normative semantics.

## Grounding read

- `docs/architecture/work-packet-design-dependency-closure.md` (accepted architecture, commit `d43950df47d9d01b516a46f63e7ae9f7da1f24f7`), in full, including its "Agent / deterministic split" and "Candidate implementation topology" sections;
- `framework/capabilities/work-packet-design/contract.md` (normative capability contract `1.0.0`), in full;
- `framework/capabilities/work-packet-design/adoption-contract.md` (adoption contract `1.0.0`), in full;
- `governance/architecture-decisions/GG-WPDC-ARCHITECTURE-001/owner-disposition.md`, in full;
- `release-manifest.json` at the canonical base;
- `framework/core/project-operating-contract.md` at the canonical base (`0.5.0`), in particular "Bounded operational delegation";
- `tools/validate_work_packet.py` (structure and referenced schemas/modules) and `tests/fixtures/work-packet/cases.json` (existing deterministic fixture shape, for the semantic-fixture strategy comparison);
- prior Block 1/Block 2 governance precedent (`GG-WPDC-NORMATIVE-CAPABILITY-ADOPTION-001/authorization.md`, `.../block-result.md`; `GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001/authorization.md`), for authorization/write-surface/stop-condition structure and the release-identity precedent cited in `design.md` §12;
- `governance/normative-implementation/GG-METHOD-NORMATIVE-IMPLEMENTATION-BOUNDED-REPLACEMENT-EXECUTION-001/work-package.md` and `.../authorization.md`, for work-package/authorization document structure.

## Required outputs (this packet)

1. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md` — durable Owner authorization of Block 4 as a bounded operational delegation, with its material stop/escalation conditions preserved.
2. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md` — the canonical design contract settling the eleven required decisions.
3. This work package.

## Declared result

Terminal status for this packet: `VALIDATED_PENDING_INDEPENDENT_REVIEW`.

Primary disposition: `WPDC_AGENT_SKILL_DESIGN_CANDIDATE`.

Next gate: `INDEPENDENT_REVIEW_OF_GG_WPDC_AGENT_SKILL_001_P1`.

## Required validation

Before this packet is treated as complete:

1. `origin/main` equals `09d678374c310d67a7ce56ef536dce6d94caef01` at candidate preparation time — verified.
2. Exactly the three authorized paths differ from the canonical base — verified by `git diff --stat` against `09d678374c310d67a7ce56ef536dce6d94caef01` (see Validation results below).
3. `git diff --check` reports no whitespace/conflict-marker errors — verified (see Validation results below).
4. `design.md` derives every normative statement from an existing WPDC/architecture/operating-contract citation rather than duplicating or contradicting WPDC normative semantics — self-checked section by section against the grounding read above.
5. Neither role is granted execution, publication, merge, release, acceptance, retry, or replacement authority anywhere in `design.md` or `authorization.md` — self-checked.
6. `UNRESOLVED` is preserved as a legitimate fail-safe outcome, and `EXCLUDED` is never modeled as prerequisite satisfaction, in every place `design.md` discusses these terms — self-checked against WPDC §4.4 and WPDC-008.
7. No file outside the three authorized paths changed — verified.
8. No SVP path, repository, or artifact is referenced as a target of any authorized action (only as read-only historical provenance already present in the cited architecture document) — self-checked.

## Validation results

Executed inside the isolated worktree (`../general-governance-wt-wpdc-agent-skill-001-design`, branch `method/wpdc-agent-skill-001-design`, base `09d678374c310d67a7ce56ef536dce6d94caef01`):

- `git status --short` — showed exactly three untracked files, all under `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/`, before staging.
- `git diff --stat 09d678374c310d67a7ce56ef536dce6d94caef01` (after staging/commit) — reported exactly:
  - `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md`
  - `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md`
  - `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/work-package.md`
- `git diff --check 09d678374c310d67a7ce56ef536dce6d94caef01` — reported no output (pass).
- No SVP repository, path, or artifact was created, read for mutation purposes, or modified.

## Out of scope

- any file under `framework/capabilities/work-packet-design/agent/**` (reserved for the follow-on implementation packet, see `design.md` §13);
- any change to `framework/capabilities/work-packet-design/contract.md`, `adoption-contract.md`, either machine schema, or `tools/validate_work_packet.py`;
- any change to `release-manifest.json`, `RELEASE_VERSION`, CI workflows, or `L0` semantics;
- any SVP repository, path, packet, or artifact;
- pull request creation, merge, tag, release, deployment, or publication of this candidate commit.
