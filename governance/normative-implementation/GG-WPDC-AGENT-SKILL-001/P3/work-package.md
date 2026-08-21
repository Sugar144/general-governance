---
work_package_id: GG-WPDC-AGENT-SKILL-001-P3
block_id: GG-WPDC-AGENT-SKILL-001
authorization_record: governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P3/authorization.md
status: EMPIRICAL_VALIDATION_COMPLETE
general_governance_baseline: 09d678374c310d67a7ce56ef536dce6d94caef01
predecessor_commit: e313d6ea3f0a6f7f8cc237741393f88925bd3543
branch: method/wpdc-agent-skill-001-validation
---

# Work Package and Output Contract — WPDC Agent Skill Fresh-Session Empirical Validation (P3)

## Objective

Empirically validate the packaged `work-packet-designer` and `work-packet-reviewer` Agent Skills from fresh Claude Code sessions, against the exact P2A candidate commit `e313d6ea3f0a6f7f8cc237741393f88925bd3543`, without modifying the skills, roles, contract, or fixture catalog under test.

## Preflight performed

1. Resolved the required P2A candidate prefix `e313d6ea` via `git rev-parse --disambiguate=e313d6ea`: exactly one match, `e313d6ea3f0a6f7f8cc237741393f88925bd3543` — unambiguous.
2. Confirmed this commit is the tip of `method/wpdc-agent-skill-001-packaging`, carries commit message "governance(wpdc-agent-skill-001): P2A packaging authority, work package, and result evidence", and contains exactly the six required grounding paths (`agent/contract.md`, both `SKILL.md`, both `role.md`, `tests/fixtures/work-packet-agent/cases.md`).
3. Created an isolated, detached-HEAD `git worktree` at `/tmp/gg-wpdc-agent-skill-p3/candidate-worktree`, pinned exactly to `e313d6ea3f0a6f7f8cc237741393f88925bd3543`.
4. Created this governance-evidence worktree, `/home/sugar/Proyectos/general-governance-wt-wpdc-agent-skill-001-validation`, on new branch `method/wpdc-agent-skill-001-validation`, branched directly from `e313d6ea3f0a6f7f8cc237741393f88925bd3543` — the exact required P2A candidate — mirroring the P1→P2→P2A predecessor-verification precedent.

## Grounding read

- `framework/capabilities/work-packet-design/agent/contract.md` (agent-layer boundary contract `1.0.0`), in full;
- `framework/capabilities/work-packet-design/agent/work-packet-designer/SKILL.md` and `.../role.md`, in full;
- `framework/capabilities/work-packet-design/agent/work-packet-reviewer/SKILL.md` and `.../role.md`, in full;
- `tests/fixtures/work-packet-agent/cases.md` (S1–S8 scenario catalog), in full.

## Evaluation method

1. Built a sanitized template (`/tmp/gg-wpdc-agent-skill-p3/base`) from the pinned candidate worktree: full repository content minus `.git/`, minus `tests/fixtures/work-packet-agent/` (fixture answers), minus `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/` (this block's own design/evidence history, to prevent an evaluated session from recognizing it is the subject of a validation exercise).
2. From that template, built fourteen isolated per-case project directories under `/tmp/gg-wpdc-agent-skill-p3/eval-projects/**`, each with the exact candidate `work-packet-designer/SKILL.md` and `work-packet-reviewer/SKILL.md` copied byte-identically into `.claude/skills/work-packet-designer/SKILL.md` and `.claude/skills/work-packet-reviewer/SKILL.md` (verified via `diff` against the candidate worktree — identical).
3. Each case was run as one genuinely fresh, isolated `claude -p` session (`--no-session-persistence`, no prior conversation, own cwd, own `.claude/skills/**`), with `--output-format stream-json --verbose` to capture the full raw transcript (tool calls and text), stored under each case's own directory in `/tmp` and never committed.
4. Case prompts never named the scenario id (`S1`…`S8`), the WPDC invariant identifiers, or any "Correct judgment" text from `cases.md`; each supplied only the "Input situation" content (paraphrased/adapted) plus an explicit in-prompt statement standing in for a WPDC adoption binding — a pilot run against the raw `cases.md` framing showed a correctly-behaving Designer stops at Stage 0 for lack of a bound adoption artifact for the fictional "Project Q" adopter, since no such binding exists anywhere in this repository; each prompt therefore explicitly supplies itself as the "exact bounded reference standing in for one" that `role.md` §0/§2 allows, so Stage 0 can resolve without fabrication and later-stage judgment (Stages 2–8) is what is actually exercised.

## Case set (14 fresh sessions)

- `explicit-designer`, `explicit-reviewer` — dedicated explicit-invocation checks, each naming the skill directly and requiring the transcript to show the skill/role/contract documents actually being read.
- `s1`…`s8` — the eight fixture scenarios from `tests/fixtures/work-packet-agent/cases.md`, each run under the role(s) `cases.md` names: `s2`, `s3` as Designer; `s1`, `s4`, `s5`, `s6`, `s7`, `s8` as Reviewer (each of these presents an already-drafted candidate, which is the natural Reviewer posture `cases.md` describes for that scenario).
- `auto-pos-designer`, `auto-pos-reviewer`, `auto-neg-trivial`, `auto-generic-product` — the observational automatic-discovery set: a WPDC-context Designer-shaped task and a WPDC-context Reviewer-shaped task, neither naming a skill; a trivial off-topic question; and a generic product/architecture question, to observe both true-positive discovery and false-positive boundary-holding without naming either skill.

## Required outputs (this packet)

1. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P3/authorization.md`;
2. This work package;
3. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P3/scenario-results.json`;
4. `governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/P3/result.md`.

## Declared result

See `result.md` for the full verdict, per-case results, and material findings. Terminal status for this packet: `EMPIRICAL_VALIDATION_COMPLETE`.

## Required validation

Before this packet is treated as complete:

1. Tested skill/role/contract files remain byte-identical to the P2A candidate — verified by `diff` of each `.claude/skills/**` projection against the candidate worktree, and by the fact that no operation in this packet ever wrote to the candidate worktree or to `framework/capabilities/work-packet-design/agent/**` in any tracked repository.
2. S1–S8 all pass (right disposition/finding for the stated reason, not merely a matching label) — see `scenario-results.json` and `result.md`.
3. Explicit Designer and Reviewer checks pass (skill actually consulted and applied, not merely named) — see `scenario-results.json`.
4. Role separation holds (Designer sessions constructed rather than adversarially reviewed; Reviewer sessions reported findings and a disposition recommendation without rewriting the candidate) — see `result.md`.
5. Only the four authorized P3 evidence paths changed in this repository — verified by `git status --porcelain` / `git diff --stat` against `e313d6ea3f0a6f7f8cc237741393f88925bd3543` before commit.
6. No `.claude/skills/**` path is tracked in this repository — verified by `git status --porcelain` (all `.claude/skills/**` content exists only under `/tmp`, outside any git-tracked worktree of this repository).
7. `git diff --check` passes — verified before commit.

## Out of scope

- redesigning or restating WPDC semantics, the Designer/Reviewer role content, or the agent contract;
- modifying `framework/capabilities/work-packet-design/agent/**` or `tests/fixtures/work-packet-agent/cases.md`;
- any WPDC normative/adoption contract, machine schema, or `tools/validate_work_packet.py` change;
- `skill-creator`'s evaluation loop or `scripts/run_eval.py`;
- committing raw transcripts or eval-project copies (`/tmp` artifacts are preserved only in `/tmp`, per this packet's instructions);
- independent final review of this validation packet itself (reserved for the next gate);
- any SVP repository, path, packet, or artifact;
- pull request creation, merge, tag, release, deployment, or publication of this candidate commit.
