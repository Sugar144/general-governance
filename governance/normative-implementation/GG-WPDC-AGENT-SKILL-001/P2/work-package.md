---
work_package_id: GG-WPDC-AGENT-SKILL-001-P2
block_id: GG-WPDC-AGENT-SKILL-001
authorization_record: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P2/authorization.md
durable_block_authorization: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md
status: VALIDATED_PENDING_FRESH_SESSION_SEMANTIC_VALIDATION
general_governance_baseline: 09d678374c310d67a7ce56ef536dce6d94caef01
predecessor_commit: 2ecb0335003f33cdab3f0fa7ff3b5536041c9077
predecessor_branch: method/wpdc-agent-skill-001-design
branch: method/wpdc-agent-skill-001-implementation
implementation_commit: 126d521f8ab8c9f23faea59d3b03ced17d771ea0
---

# Work Package and Output Contract — WPDC Agent Skill Implementation (P2)

## Objective

Implement the canonical, provider-neutral WPDC agent layer (`work-packet-designer`, `work-packet-reviewer`) and its semantic fixture catalog exactly per the accepted P1 design (`governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md`), without redesigning it, without forking WPDC normative semantics, and without any provider/adopter-specific projection.

## Preflight performed

1. Verified predecessor commit `2ecb0335003f33cdab3f0fa7ff3b5536041c9077` exists, is the exact head of `method/wpdc-agent-skill-001-design`, and matches the exact 40-character SHA supplied by the packet.
2. Verified `2ecb0335003f33cdab3f0fa7ff3b5536041c9077` descends from canonical GG base `09d678374c310d67a7ce56ef536dce6d94caef01` (two commits ahead: `396505f…` then `2ecb033…`).
3. Fetched `origin/main` and confirmed `git rev-parse origin/main` equals `09d678374c310d67a7ce56ef536dce6d94caef01` exactly — no conflicting WPDC agent-layer work exists on `origin/main`; `git merge-base 2ecb033… origin/main` also equals the canonical base, confirming `origin/main` has not moved since.
4. Confirmed the source worktree (`method/wpdc-agent-skill-001-design`) was clean (`git status` — nothing to commit).
5. Searched for an applicable `CLAUDE.md`/`AGENTS.md`: none found at the repository root. No repository-local operating instruction was found to conflict with this packet.
6. Created an isolated worktree at `../general-governance-wt-wpdc-agent-skill-001-implementation` on new branch `method/wpdc-agent-skill-001-implementation`, created directly from `2ecb0335003f33cdab3f0fa7ff3b5536041c9077`.
7. No stop condition was triggered: predecessor matched exactly, canonical-base ancestry held, `origin/main` was current, the write surface was clear, no requested step required changing an accepted WPDC normative invariant.

## Grounding read

- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md` (accepted P1 design, in full) — authoritative for agent-layer architecture;
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md` (durable Block 4 authorization, in full);
- `framework/capabilities/work-packet-design/contract.md` (WPDC normative capability contract `1.0.0`, in full);
- `framework/capabilities/work-packet-design/adoption-contract.md` (WPDC adoption contract `1.0.0`, in full);
- `contracts/work-packet-manifest.schema.json` (manifest schema, in full);
- `tools/validate_work_packet.py`, inspected only for its CLI invocation interface (`--manifest`, `--binding`, `--configuration`, `--repository-root`) and disposition/exit-code contract, not for reimplementation of its logic;
- `framework/core/project-operating-contract.md`, sections "Bounded operational delegation," "Versioned formal-run correction identity," and "Failure, learning, and immutability";
- prior Block 2/Block 3 governance precedent (`GG-WPDC-MACHINE-CONTRACT-VALIDATOR-001/block-result.md`) for governance-record structure;
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/work-package.md` (P1's work package), for preflight/validation-record structure precedent.

## Required outputs (this packet)

1. `framework/capabilities/work-packet-design/agent/contract.md` — GG-owned agent-layer boundary contract.
2. `framework/capabilities/work-packet-design/agent/work-packet-designer/role.md` — Designer role definition.
3. `framework/capabilities/work-packet-design/agent/work-packet-reviewer/role.md` — Reviewer role definition.
4. `tests/fixtures/work-packet-agent/cases.md` — adopter-neutral semantic fixture catalog.
5. This work package and its accompanying `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P2/**` governance records.

## Declared result

Terminal status for this packet: `VALIDATED_PENDING_FRESH_SESSION_SEMANTIC_VALIDATION`.

Primary disposition: `WPDC_AGENT_SKILL_IMPLEMENTATION_CANDIDATE`.

Next gate: `GG_WPDC_AGENT_SKILL_001_P3_FRESH_SESSION_SEMANTIC_VALIDATION`.

## Required validation

Before this packet is treated as complete:

1. `origin/main` equals `09d678374c310d67a7ce56ef536dce6d94caef01` at candidate preparation time — verified.
2. Exactly the four canonical implementation paths (§ "Required outputs" items 1–4) differ from the predecessor commit, plus this packet's own `P2/**` governance records — verified by `git diff --stat`/`--name-only` against `2ecb0335003f33cdab3f0fa7ff3b5536041c9077` (see `result.md`).
3. `git diff --check` reports no whitespace/conflict-marker errors on the implementation commit — verified.
4. No file under any forbidden path (`release-manifest.json`, `RELEASE_VERSION`, WPDC normative/adoption contracts, machine schemas, `tools/validate_work_packet.py`, CI workflows, any SVP path) changed — verified.
5. Every requirement enumerated by the P2 governance packet (canonical agent contract, Designer workflow items, Reviewer responsibilities, review-requirement resolution, historical truth handling, fixture catalog minimum coverage) is traceable to an implemented section of the four canonical artifacts — self-checked requirement-by-requirement against `design.md`.
6. Neither role file grants execution, publication, merge, release, acceptance, retry, or replacement authority anywhere in its text — self-checked.
7. `EXCLUDED` is never modeled as prerequisite satisfaction, and `UNRESOLVED` is preserved as a legitimate outcome, in every place the Designer/Reviewer role files discuss these terms — self-checked against WPDC §4.4, WPDC-008.
8. Neither role file, nor the agent-layer contract, embeds a copy of WPDC invariant text, the resolution enum, the disposition precedence rule, or the schema field list — self-checked; every rule is cited by section/invariant identifier.
9. No provider-, runtime-, or adopter-specific projection (Claude Code `SKILL.md` frontmatter, Cursor rule file, or similar) exists anywhere under the implemented paths — self-checked.
10. The semantic fixture catalog covers, at minimum, all eight required scenario families and uses no SVP or other adopter-specific vocabulary — self-checked against `design.md` §10.
11. The existing WPDC deterministic regression suite and consumer-conformance tests show no new failure relative to the predecessor-commit baseline — verified (see `result.md`).
12. The resulting tracked-content digest is computed and recorded as a known release-integration condition, without modifying `release-manifest.json` to make it match — verified (see `result.md`).

Detailed validation results, exact commands, and outcomes are recorded in `result.md`.

## Out of scope

- any file under `framework/capabilities/work-packet-design/contract.md`, `adoption-contract.md`, either machine schema, or `tools/validate_work_packet.py`;
- any change to `release-manifest.json`, `RELEASE_VERSION`, CI workflows, or `L0` semantics;
- any SVP repository, path, packet, or artifact;
- any Claude-, Codex-, Cursor-, or other provider/adopter-specific projection of the canonical role content;
- fresh-session semantic empirical validation of the Designer/Reviewer roles against the fixture catalog (reserved for `GG_WPDC_AGENT_SKILL_001_P3_FRESH_SESSION_SEMANTIC_VALIDATION`);
- independent Reviewer evaluation of this implementation candidate itself;
- pull request creation, merge, tag, release, deployment, or publication of this candidate commit.
