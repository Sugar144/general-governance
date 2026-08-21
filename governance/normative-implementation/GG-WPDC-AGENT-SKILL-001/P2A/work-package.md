---
work_package_id: GG-WPDC-AGENT-SKILL-001-P2A
block_id: GG-WPDC-AGENT-SKILL-001
authorization_record: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P2A/authorization.md
status: PACKAGING_CANDIDATE_PASS_PENDING_FRESH_SESSION_EMPIRICAL_VALIDATION
general_governance_baseline: 09d678374c310d67a7ce56ef536dce6d94caef01
predecessor_commit: 9744449c9144d99f0d0372bbdd4514662dd23e0e
branch: method/wpdc-agent-skill-001-packaging
---

# Work Package and Output Contract — WPDC Agent Skill Packaging (P2A)

## Objective

Convert the already-implemented, already-accepted provider-neutral WPDC agent roles (`work-packet-designer`, `work-packet-reviewer`) into real canonical Agent Skill packages — a thin `SKILL.md` operational entrypoint per role that orients the executor toward the existing canonical `contract.md`/`role.md` material rather than duplicating it — using current Agent Skill packaging conventions obtained from the installed `skill-creator:skill-creator` skill. Do not redesign WPDC semantics, do not modify either existing `role.md` or `contract.md`, and do not perform empirical/semantic activation validation (reserved for P3).

## Preflight performed

1. Verified the current worktree's `HEAD` was exactly the required predecessor `9744449c9144d99f0d0372bbdd4514662dd23e0e` (`method/wpdc-agent-skill-001-implementation`, "governance(wpdc-agent-skill-001): P2 implementation authority, work package, and result evidence").
2. Verified `9744449…` descends from the P1 accepted design commit `2ecb0335003f33cdab3f0fa7ff3b5536041c9077` (`git merge-base --is-ancestor`).
3. Verified the pre-existing worktree was clean (`git status --porcelain` empty) before branching.
4. Fetched `origin/main` and confirmed its head, `09d678374c310d67a7ce56ef536dce6d94caef01`, is an ancestor of the predecessor commit — i.e. no conflicting WPDC agent-layer work exists on `origin/main` beyond what this line of work already builds on.
5. Created an isolated worktree at `../general-governance-wt-wpdc-agent-skill-001-packaging` on branch `method/wpdc-agent-skill-001-packaging`, created directly from `9744449c9144d99f0d0372bbdd4514662dd23e0e`.
6. No stop condition was triggered: the predecessor matched exactly, ancestry held, the working tree was clean, and `origin/main` carried no conflicting agent-layer work.

## Grounding read

- `framework/capabilities/work-packet-design/agent/contract.md` (agent-layer boundary contract `1.0.0`), in full;
- `framework/capabilities/work-packet-design/agent/work-packet-designer/role.md`, in full;
- `framework/capabilities/work-packet-design/agent/work-packet-reviewer/role.md`, in full;
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md`, in full, including §3 (canonical source layout), §9 (provider-neutrality), and §13 (proposed minimal write surface);
- `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/authorization.md` (durable Block 4 authorization) and `.../P2/authorization.md`, `.../P2/result.md` (P2 packet precedent), for authorization/work-package/result document structure and prior validation-command precedent.

## Required skill-creator use

`skill-creator:skill-creator` was explicitly invoked (via the `Skill` tool) before authoring either `SKILL.md`, with an explicit instruction set constraining it to a guidance-only consultation: report current Agent Skill packaging conventions (frontmatter fields, naming, description/trigger-quality guidance, progressive disclosure, SKILL.md body conciseness, referencing deeper material) and a structural checklist, without redesigning WPDC semantics, without writing any file, and without running its description-optimization loop, benchmark/viewer loop, or `scripts/run_eval.py`. The invocation returned the skill's own instructions (`SKILL.md` body), from which the following conventions were extracted and applied:

- frontmatter requires `name` (skill identifier, matching the directory) and `description` (the primary triggering mechanism — must state both what the skill does and when to use it, specific enough to avoid over-triggering on adjacent generic tasks);
- progressive disclosure: metadata (name+description) always in context; SKILL.md body kept concise (guideline: under ~500 lines) and in context only when triggered; deeper material referenced by path with guidance on when to read it, not duplicated;
- writing style: imperative instructions, explain the "why," avoid restating content that lives authoritatively elsewhere.

No description-optimization loop, benchmark/viewer loop, or `scripts/run_eval.py` was run. No file was written by the skill-creator consultation itself; both `SKILL.md` files were authored directly in this packet, respecting the allowed write surface in `P2A/authorization.md`.

## Required outputs (this packet)

1. `framework/capabilities/work-packet-design/agent/work-packet-designer/SKILL.md`;
2. `framework/capabilities/work-packet-design/agent/work-packet-reviewer/SKILL.md`;
3. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P2A/authorization.md`;
4. This work package;
5. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P2A/result.md`.

## Declared result

Terminal status for this packet: `PACKAGING_CANDIDATE_PASS_PENDING_FRESH_SESSION_EMPIRICAL_VALIDATION`.

Primary disposition: `WPDC_AGENT_SKILL_PACKAGING_CANDIDATE`.

Next gate: `GG_WPDC_AGENT_SKILL_001_P3_FRESH_SESSION_EMPIRICAL_SKILL_VALIDATION`.

## Required validation

Before this packet is treated as complete:

1. `skill-creator:skill-creator` was explicitly invoked — verified above.
2. Both packages conform to the creator's current structural conventions (frontmatter present, concise body, progressive-disclosure references to canonical material) — self-checked against the extracted checklist.
3. Exact skill names are correct (`work-packet-designer`, `work-packet-reviewer`, matching their directories) — verified.
4. Descriptions distinguish Designer from Reviewer and from generic planning/review — self-checked (see `result.md` for the exact frontmatter text).
5. No normative WPDC fork was introduced — self-checked: neither `SKILL.md` restates the invariant enumeration, the resolution enum, or the disposition precedence rule; each cites `role.md`/`contract.md` by path and section for authoritative content.
6. No provider/adopter-specific semantics were introduced — self-checked: no Claude-, Codex-, Cursor-, or SVP-specific tool-call syntax or path appears in either file beyond the Agent Skill frontmatter format itself.
7. No `.claude/skills` or `.agents/skills` projection was created — verified by directory search.
8. Exact authorized-path diff — verified by `git diff --stat`/`--name-only` against the predecessor commit.
9. `git diff --check` reports no whitespace/conflict-marker errors — verified.
10. The existing WPDC deterministic regression suite was run before and after packaging, to confirm packaging did not alter existing behavior — verified (see `result.md`); the known pre-existing release-digest mismatch is expected and was not repaired.

## Validation results

Executed inside the isolated worktree (`../general-governance-wt-wpdc-agent-skill-001-packaging`, branch `method/wpdc-agent-skill-001-packaging`, predecessor `9744449c9144d99f0d0372bbdd4514662dd23e0e`):

- `git status --porcelain` — showed exactly two untracked files before staging, both under the allowed `SKILL.md` paths.
- `git diff --cached --stat 9744449c9144d99f0d0372bbdd4514662dd23e0e` (after staging) — reported exactly:
  - `framework/capabilities/work-packet-design/agent/work-packet-designer/SKILL.md` (new, 35 lines);
  - `framework/capabilities/work-packet-design/agent/work-packet-reviewer/SKILL.md` (new, 35 lines).
- `git diff --cached --name-only 9744449c9144d99f0d0372bbdd4514662dd23e0e -- <contract.md and both role.md paths>` — empty output, confirming those three files are byte-identical to the predecessor.
- `git diff --check --cached` — reported no output (pass).
- Directory search for `.claude/skills` or `.agents/skills` anywhere under the worktree — no matches.
- No SVP repository, path, or artifact was created, read for mutation purposes, or modified.

## Out of scope

- redesigning or restating WPDC semantics, the Designer/Reviewer role content, or the agent contract;
- modifying `framework/capabilities/work-packet-design/agent/contract.md` or either existing `role.md`;
- any WPDC fixture, normative/adoption contract, machine schema, or `tools/validate_work_packet.py` change;
- any `.claude/skills/**` or `.agents/skills/**` provider projection;
- skill-creator's description-optimization loop, benchmark/viewer loop, or `scripts/run_eval.py`;
- any empirical/fresh-session activation or discovery test of either packaged skill (reserved for P3);
- any change to `release-manifest.json`, `RELEASE_VERSION`, CI workflows, or `L0` semantics;
- any SVP repository, path, packet, or artifact;
- pull request creation, merge, tag, release, deployment, or publication of this candidate commit.
