---
record_id: GG-METHOD-NORMATIVE-CLARIFICATION-BOUNDED-REPLACEMENT-EXECUTION-001-PROPOSAL-001
execution_id: GG-METHOD-NORMATIVE-CLARIFICATION-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
status: VALIDATED_PENDING_PROJECT_OWNER_REVIEW
disposition: NORMATIVE_WORDING_CANDIDATE
general_governance_baseline: 91fa0727abf730e142a4c43f2da68b1281be1121
accepted_discovery_head: 9be04b980cdaffa0bf61a41687e39700554fecbf
formal_input_package_sha256: a3e1b427579579432dff3556f06afdc746c0e0fd67c2ab5a72b423f88c936825
---

# Bounded Replacement Execution — Normative Clarification Proposal

## 1. Executive proposal

**Primary disposition: `NORMATIVE_WORDING_CANDIDATE`.**

The accepted discovery can be closed with one narrow Project Operating Contract addition. No new authority subsystem, schema, L6 lifecycle helper, or provider-specific retry rule is needed.

The proposal adds a new subsection, **Bounded replacement execution**, immediately after `## Formal execution, orchestration, and output contract` and before `## Versioned formal-run correction identity`. This location makes replacement execution a peer lifecycle concept to formal execution and correction without changing bounded operational delegation.

## 2. Bound evidence

This proposal is bound to:

- General Governance baseline `91fa0727abf730e142a4c43f2da68b1281be1121`;
- `framework/core/project-operating-contract.md` blob `d9ca298b973d9cf91792f77dfd7fd4ff274d0a78`, version `0.4.0`;
- accepted discovery HEAD `9be04b980cdaffa0bf61a41687e39700554fecbf`;
- accepted discovery result blob `633fe688ecdb354a139c2b41b635936ecaf0c92b`;
- accepted discovery validation blob `8dca0042ef4e0e7f8446606e309b111feba76759`;
- Project Owner acceptance in Issue #5 comment `5343199362`;
- formal drafting authorization in Issue #6 comment `5360001203`.

SVP Packet 03 remains evidence only. HTTP 429, provider identity, zero product paths, and one-replacement policy are not promoted into General Governance core semantics.

## 3. Exact insertion point

Insert the new subsection **after** the final paragraph of `## Formal execution, orchestration, and output contract`:

> Formal architecture and implementation reports used as durable design, review, validation, or implementation evidence must be imported into repository custody before the associated change is committed.

and **before**:

`## Versioned formal-run correction identity`

No existing rc.4 paragraph needs deletion or semantic weakening.

## 4. Proposed normative wording

```markdown
## Bounded replacement execution

A terminal failure never creates execution authority. A replacement execution is a distinct formal execution identity causally linked to a prior execution that crossed its authoritative execution boundary and reached a terminal failed state. It does not resume, unconsume, reopen, overwrite, or correct the failed execution; the failed execution and its evidence remain immutable.

A replacement may execute only under explicit finite authority that admits replacement semantics, either through a separately granted post-failure authorization or through a prospective conditional replacement policy bound before execution. A bare `permitted_execution_count > 1` is only a quantity bound and does not by itself classify, permit, or imply causal replacement execution. Prospective conditional replacement authority must define eligible failure classes, maximum replacement allowance, lineage requirements, effect-state safety gates, allowance-consumption boundary, currentness requirements, and stop conditions.

Before replacement execution, the governing gate must establish: the prior execution is terminal and consumed; preserved evidence supports the admitted failure classification; material non-idempotent effects are absent or reconciled to an exact bound state; the bounded work intent and material input scope remain unchanged; currentness gates still pass; and the applicable replacement policy or authorization admits the observed failure class. Provider, transport, HTTP status, model, executor, or harness facts may support that evidence but are not universal replacement criteria unless the applicable protocol explicitly makes them so.

The replacement record or run set must bind the replacement identity, `replacement_of` failed execution identity, replacement authority, failure-evidence reference or digest, bounded work/input lineage, bound role/mode/protocol, and finite replacement allowance or ordinal. Crossing the replacement's authoritative execution boundary consumes its admitted allowance. Failure of a replacement creates zero new authority edges: a later replacement may execute only if an already-bound prospective policy still has unused explicitly admitted allowance or a new competent authorization is granted.

Resume remains continuation of the same execution identity only while the governing protocol treats that execution as resumable; a terminal consumed failure is not reopened by calling it a resume. `R<N>` remains the correction identity for an immutable completed formal-run result and is not replacement execution.

A continuation that changes an authority-bound role, mode, protocol, material input scope, safety or validation control, execution-environment assumption, effect model, or mutation surface requires new execution-strategy authority and must not be relabeled as replacement under prior authority. Selection among prospectively declared interchangeable providers or executors does not by itself require new strategy authority when the bound mode, protocol, controls, scope, and effect model remain unchanged.
```

## 5. Clause-by-clause rationale

1. **“Terminal failure never creates execution authority”** makes the anti-recursion rule explicit at the lifecycle boundary.
2. **Distinct identity + immutable failed run** separates replacement from retry-as-rewrite and preserves existing historical immutability.
3. **Two valid authority forms** preserves rc.4 prospective bounded authority while allowing the post-failure pattern demonstrated by SVP.
4. **Execution count is quantity only** closes the demonstrated ambiguity around `permitted_execution_count`.
5. **Eligibility gate** prevents blind replay when failure classification or material effect state is ambiguous.
6. **Provider-neutral evidence** allows adopter protocols to use HTTP/provider facts without hard-coding them into core methodology.
7. **Explicit lineage and finite allowance** makes causal replacement reviewable and prevents recursive manufacturing of retries.
8. **Resume / `R<N>` distinctions** preserve existing same-identity interruption semantics and formal-run correction semantics.
9. **Execution-strategy boundary** captures the accepted `RECOVERY-001` lesson without treating every provider/executor substitution as a strategy change.

## 6. Compatibility with rc.4

The wording is additive and consistent with every relevant rc.4 rule:

- bounded operational delegation remains prospective, finite, fail-closed, identity/currentness-fenced, and scope-bounded;
- failed or indeterminate gates still stop delegated execution;
- formal execution still requires an exact Owner authorization binding run, role, mode, protocol, input-package hash, permitted execution count, and forbidden actions;
- prompt-custody interruption recovery still resumes only from exact preserved state;
- completed/consumed run evidence remains immutable;
- `R<N>` correction identity remains unchanged;
- anti-recursion still stops when new authority or evidence is needed;
- Owner acceptance remains distinct from execution, validation, merge, release, or deployment.

The new subsection specializes lifecycle classification; it does not grant an additional operational effect or relax any existing authority gate.

## 7. Authority non-expansion proof

The candidate cannot widen authority for four reasons.

First, it states that failure creates **zero** authority. Second, it treats `permitted_execution_count` as insufficient without an explicit replacement policy. Third, every replacement must pass a new eligibility/currentness/effect-state gate under already-existing or newly granted competent authority. Fourth, any authority-bound strategy change forces new authority.

Therefore the candidate is strictly no-more-permissive than rc.4's existing bounded-delegation model. It adds constraints and classification; it does not introduce a new source of authority.

## 8. Counterexample tests

| Case | Required result under proposed wording |
|---|---|
| Preparation fails before execution boundary | Same unexecuted identity may be repaired; not replacement. |
| Execution is interrupted and protocol still marks it resumable with exact custody | Resume same identity. |
| Completed run output is later found defective | Use `R<N>` correction, not replacement. |
| Consumed terminal failure; explicit admitted replacement policy; effect state reconciled | Distinct replacement may execute within remaining finite allowance. |
| Prior authority has `permitted_execution_count: 3` but no replacement policy | No replacement semantics may be inferred from the count. |
| Consumed failure leaves a non-idempotent side effect ambiguous | Replacement is blocked until state is reconciled and bound. |
| Replacement fails and explicit finite replacement allowance is exhausted | STOP; failure creates no successor authority. |
| A second replacement is already prospectively admitted and unused | It may execute only after its gates pass; it is not created by the prior failure. |
| Work requirements or material input scope change | New work/new authority, not replacement. |
| Provider changes inside an explicitly interchangeable set while mode/protocol/controls remain bound and unchanged | No strategy-authority change solely because of provider selection. |
| Execution changes from empirical provider mode to host-assisted non-empirical recovery | New execution-strategy authority required. |

## 9. Deterministic validation plan

A future implementation package should validate the exact candidate with deterministic checks where possible:

1. baseline blob/currentness fence for `project-operating-contract.md`;
2. exact single insertion point between formal execution and `R<N>` correction sections;
3. document frontmatter version change only as separately authorized;
4. presence of the invariants `failure creates zero authority`, distinct replacement identity, bare count insufficiency, finite allowance, lineage, effect-state safety, resume distinction, correction distinction, and strategy-authority boundary;
5. absence of provider-specific universal eligibility terms such as a hard-coded HTTP status;
6. no deletion or weakening of existing bounded operational delegation, Owner acceptance, correction, immutability, or anti-recursion text;
7. documentation/conformance tests continue to pass;
8. diff fence limited to the separately authorized implementation surface.

No new machine-checkable formal-run schema is justified by this wording candidate.

## 10. Exact future write surface

For the **normative implementation candidate itself**, the smallest justified write surface is:

- `framework/core/project-operating-contract.md`

No schema, `framework/core/l6/**`, tool, or test implementation is required by the accepted discovery.

Release/publication bookkeeping is a separate effect and should not be silently bundled into the normative edit. If the accepted wording is later packaged as the next General Governance release candidate, release-facing surfaces may need a separately authorized update after the normative candidate is accepted.

## 11. Release/version implications

Because the wording adds a new provider-neutral lifecycle class and normative constraints, it is more than an editorial patch.

Recommended document-version implication if implemented:

- `GOV-METHOD-OPERATING-CONTRACT-001`: `0.4.0` -> `0.5.0`.

Recommended framework release implication **only if separately accepted and packaged for release**:

- `General Governance 0.1.0-rc.4` -> prospective `0.1.0-rc.5`.

A future rc.5 release package would need to determine and authorize the exact consistency/bookkeeping surfaces such as `RELEASE_VERSION`, release manifest, README/consumer-facing compatibility text, and evolution provenance. This drafting run neither changes nor authorizes those surfaces.

No consumer configuration or schema migration is indicated by the accepted evidence because the proposal changes lifecycle semantics, not configuration/schema contracts.

## 12. Explicit exclusions

This proposal does not:

- edit or supersede rc.4;
- create implementation authority;
- create PR/merge/release/deployment authority;
- add a formal-run schema or lifecycle state machine;
- modify L6 authority helpers;
- establish HTTP 429 or any provider-specific condition as universal replacement eligibility;
- guarantee every external failure is replacement-eligible;
- authorize recursive replacement;
- rewrite SVP RUN-003, RUN-004, or RECOVERY-001 history;
- reopen bounded operational delegation semantics already accepted in rc.4.

## 13. Recommended next decision

The Project Owner should review and either accept, reject, or request refinement of:

`NORMATIVE_WORDING_CANDIDATE`

If accepted, the next separately authorized package should implement **only** the exact accepted wording in `framework/core/project-operating-contract.md`, including the accepted document-version change, validate the resulting candidate, and stop for Owner review before any release/version-publication package is undertaken.
