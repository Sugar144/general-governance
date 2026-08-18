---
record_id: GG-METHOD-DISCOVERY-BOUNDED-REPLACEMENT-EXECUTION-001-RESULT-001
execution_id: GG-METHOD-DISCOVERY-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
status: VALIDATED_PENDING_PROJECT_OWNER_REVIEW
disposition: NORMATIVE_CLARIFICATION_CANDIDATE
general_governance_baseline: 91fa0727abf730e142a4c43f2da68b1281be1121
formal_input_package_sha256: 88033d59120ab2a3e9e226fd5f4985d7952a5dc7ecda8601b14c89da8dd7cbe8
---

# Bounded Replacement-Execution Semantics — Method Discovery Result

## 1. Executive disposition

**Primary disposition: `NORMATIVE_CLARIFICATION_CANDIDATE`.**

The SVP Packet 03 evidence demonstrates a real provider-neutral lifecycle gap in General Governance rc.4, but the gap is narrower than a new authority subsystem.

rc.4 already supplies the necessary primitives for safe behavior: prospective exact authority, finite execution counts, fail-closed delegation, immutable historical runs, interruption/resumption, `R<N>` correction identity, currentness fences, and explicit separation of execution from acceptance. What rc.4 does **not** define is the semantic relationship between a consumed terminally failed execution and a separately authorized new execution whose purpose is to re-attempt the same bounded work without rewriting the failed execution.

That missing relationship matters because a bare execution count does not answer whether a later invocation is an ordinary execution, resume, correction, replacement, or strategy recovery; nor does it define eligibility, lineage, allowance consumption, or anti-recursion.

The smallest justified next step is therefore a prospective clarification in the Project Operating Contract. No schema, tooling, release, or implementation change is justified by this discovery alone.

## 2. Bound evidence and evidence limits

General Governance evidence:

- baseline commit: `Sugar144/general-governance@91fa0727abf730e142a4c43f2da68b1281be1121`;
- operating contract: `framework/core/project-operating-contract.md`, blob `d9ca298b973d9cf91792f77dfd7fd4ff274d0a78`, version `0.4.0`;
- L6 bounded authority helper inspected at the same baseline: `framework/core/l6/authority.py`, blob `094ac7aa5fc4bbfefe78c6ada79eb8c0b494a963`;
- intake disposition: Issue #4, comment `5335497863`;
- formal discovery authorization: Issue #5, comment `5335539678`.

SVP evidence:

- harvest-containing commit: `Sugar144/stakeholder-validation-portal@b82925b5b756f7bde4bc153acf46abb97928c682`;
- evidence baseline declared inside the harvest: `62af73a5c2006e618cff0be03c33dbb35b2cac91`;
- cross-project harvest blob: `6c1824c9d222530a716c0829a1161470273db397`;
- Packet 03 lessons blob: `0fbe8ba61c65da3ab233def580b3d7e8ac4f6f31`;
- Amendment 002 blob: `d37d00fe8777a8762772888a23ab740c52bf0d03`;
- Amendment 003 blob: `62e2e2e605eea112ef1c9e5346759730e922070a`.

Observed Packet 03 facts are evidence, not universal policy. In particular, this discovery does **not** infer that HTTP 429 is intrinsically replacement-eligible, that zero product paths is always required, or that provider identity itself belongs in General Governance core semantics.

## 3. Existing rc.4 coverage

rc.4 already covers most safety properties that Packet 03 exercised:

1. formal execution requires exact prospective Owner authority binding run, role, mode, protocol, input-package hash, execution count, and forbidden actions;
2. bounded operational delegation is finite, prospective, identity/currentness-fenced, and fail-closed;
3. failed or indeterminate gates stop delegated execution;
4. interruption recovery uses the repository-custodied prompt and durable evidence and must not silently substitute a revised prompt;
5. completed runs and their evidence remain immutable;
6. `R<N>` is explicitly a correction of an immutable completed formal run and does not overwrite the base run;
7. anti-recursion requires stopping when the next step needs new authority, evidence, or contract correction.

The L6 `authority.py` helper reinforces the same direction at the action/path layer: denied or indeterminate requests return `retry_with_new_authority=true`; the helper contains no rule by which failure generates authority. It also contains no run-lineage or replacement-attempt model.

Therefore the missing concept is not “how to authorize something.” It is “how to classify and constrain a new execution that causally replaces a consumed failed execution.”

## 4. Lifecycle taxonomy

The following taxonomy is provider-neutral and non-overlapping enough for General Governance.

### Ordinary execution

A prospectively authorized formal execution with its own exact identity and execution contract. Crossing its protocol-defined execution boundary consumes the execution allowance according to that protocol.

### Consumed failed execution

An execution that crossed its authoritative execution boundary and then reached a terminal failed state. Its identity, evidence, and consumed status remain immutable. Terminal failure does not by itself determine whether later work is a correction, replacement, recovery, or new work.

### Interruption / resume

Continuation of the **same execution identity** from repository-custodied prompt and durable state after an interruption, when the governing protocol still treats the execution as resumable rather than terminally consumed. Preparation failure before the execution boundary also remains within the same unexecuted identity.

Resume is not a mechanism for reopening a terminal consumed failure.

### `R<N>` correction

A versioned correction of an immutable completed formal run whose produced output requires bounded correction. The correction binds the base input/output and correction findings, preserves unaffected meaning, creates a new output contract, and receives independent evaluation.

`R<N>` addresses a defective or incomplete **result artifact**. It is not the natural identity for a re-execution caused by a terminal external execution failure before the contracted result was successfully produced.

### Replacement execution

A **distinct formal execution identity** causally linked to a prior consumed terminally failed execution, created to re-attempt the same bounded work under materially unchanged work scope and execution class.

A replacement:

- never unconsumes or rewrites the failed execution;
- never derives authority from the failure itself;
- requires authority that is either already prospectively explicit or separately granted after the failure;
- consumes its own finite allowance when it crosses its own authoritative execution boundary;
- carries explicit lineage to the failed execution and replacement authority.

### Execution-strategy recovery

A distinct execution performed after the prior execution path is exhausted or unsuitable **and** the new execution changes a bound execution property such as mode, protocol, control surface, or other authority-relevant mechanism.

A strategy recovery is not merely a renamed replacement. Packet 03 `RECOVERY-001`, which changed from the empirical SDK channel to host-assisted non-empirical recovery, is a clear example because the execution mode/protocol changed and therefore needed separate authority.

## 5. Replacement eligibility

Failure must never create replacement authority. It may only make a failed execution **eligible for consideration** under authority that already exists or is newly granted.

A provider-neutral minimum eligibility gate should require all of the following:

1. **Consumed terminal execution** — the prior execution demonstrably crossed its authoritative boundary and is terminally failed.
2. **Preserved causal evidence** — immutable or digest-bound evidence supports the failure classification strongly enough for the governing protocol to distinguish it from an ordinary product/result defect.
3. **Effect-state safety** — there is no unresolved ambiguity about material non-idempotent effects. Either no material effects occurred, or the exact resulting state/checkpoint has been reconciled and is bound as the replacement starting state.
4. **Unchanged bounded work intent** — the accepted work scope and intended result remain materially unchanged. A new requirement or new material scope is new work, not a replacement.
5. **Currentness** — inputs, candidate/base state, and authority-relevant identities still satisfy their currentness gates.
6. **Policy match** — the observed failure class is explicitly admitted by the applicable replacement policy/authority.

Provider HTTP status, transport details, model/provider identifiers, or “useful candidate” judgments may be evidence used by an adopter protocol, but they should not be hard-coded as General Governance eligibility semantics.

## 6. Authority model

Replacement authority can be valid in two forms.

### A. Separately granted post-failure authority

After a consumed failure, the Owner may authorize a replacement that binds at minimum:

- failed execution identity;
- replacement execution identity or deterministic derivation;
- failure-evidence reference/digest;
- unchanged bounded work scope;
- mode/protocol;
- maximum replacement allowance;
- safety/currentness gates;
- forbidden recursive or out-of-scope continuation.

Packet 03 Amendment 002 is evidence for this form.

### B. Prospectively granted conditional replacement authority

General Governance rc.4 already supports finite prospective authority. Therefore a future execution contract may prospectively authorize a bounded replacement policy **if and only if the policy itself is explicit before execution**.

It must define the eligible failure classes, finite maximum replacement count, lineage rule, effect-state safety gate, allowance-consumption boundary, and stop conditions.

A bare `permitted_execution_count > 1` is **not sufficient by itself** to infer replacement semantics. Quantity alone does not define causal relation, eligibility, identity, or anti-recursion. The protocol/authorization must state that some of the finite count is conditional replacement allowance and how that allowance is admitted.

This preserves rc.4 bounded delegation while preventing “the counter says 3, therefore retry” reasoning.

## 7. Lineage and anti-recursion

A reusable replacement relation should minimally carry these conceptual bindings:

- `execution_id` — the replacement's distinct identity;
- `replacement_of` — the consumed failed execution being replaced;
- `replacement_authority_id` — the authority under which the replacement exists;
- `failure_evidence_ref` or digest — immutable evidence supporting eligibility;
- `replacement_ordinal` and/or finite allowance identity;
- bound work scope/input lineage;
- bound mode/protocol.

Historical state is append-only: the original remains `FAILED / CONSUMED`; the replacement never rewrites it.

The anti-recursion invariant is:

**failure produces zero authority edges.**

If a replacement fails, a later execution is allowed only when:

1. an already-existing prospective finite policy still contains unused explicitly admitted replacement allowance; or
2. a new competent authority object is granted.

There is no implicit `replacement -> replacement -> replacement` recursion. Once allowance is exhausted, execution stops.

This invariant is stronger and more general than “allow exactly one replacement.” Packet 03 used one replacement, but General Governance should standardize finite explicit authority, not one provider-specific count.

## 8. Execution-strategy boundary

Changing provider, executor, host, harness, or transport is **not automatically** a new strategy authority in every system. The decisive boundary is whether the change violates or changes an authority-bound execution property.

A new authority object is required when the continuation changes any bound or materially controlling property, including:

- `mode`;
- `protocol`;
- role;
- material input package/scope;
- safety or validation controls;
- authority-relevant execution environment assumption;
- effect model or mutation surface.

If the governing protocol prospectively declares multiple interchangeable providers/executors within one unchanged mode and control contract, selecting among them need not create a new strategy authority.

Packet 03 `RECOVERY-001` required separate authority because the execution mechanism moved from empirical provider execution to host-assisted non-empirical implementation recovery. That changed the execution class, not merely a provider endpoint.

## 9. Representation decision

The smallest justified General Governance change is a **normative clarification candidate in the Project Operating Contract**, adjacent to formal execution / correction semantics.

The clarification should define only:

1. consumed failure does not create authority;
2. replacement is a distinct execution identity linked to a consumed failed execution;
3. replacement may be post-failure authorized or prospectively conditionally authorized;
4. bare execution count is not enough to infer replacement semantics;
5. replacement eligibility requires evidence, effect-state safety, unchanged bounded scope, currentness, and policy match;
6. finite allowance is consumed at the replacement execution boundary;
7. replacement failure cannot recursively manufacture authority;
8. a material change to a bound mode/protocol/control mechanism requires new execution-strategy authority;
9. replacement is distinct from same-identity resume and `R<N>` correction.

**No machine-checkable schema change is recommended at this stage.**

Reason: General Governance currently has no formal-run lineage schema to extend. `framework/core/l6/authority.py` is an action/path authorization guard, not a formal-run lifecycle state machine. Adding replacement lineage there now would conflate layers and exceed the demonstrated need.

If a future formal-run record/controller schema is introduced, the lineage and allowance fields above should then become machine-checkable.

## 10. Counterexample tests

| Case | Correct classification / result |
|---|---|
| Preparation fails before execution boundary | repair same unexecuted identity; not replacement |
| Execution is interrupted but protocol says resumable and exact prompt/checkpoint exists | resume same identity |
| Completed run produces an artifact later found defective by independent review | `R<N>` correction |
| Consumed run terminally fails with strong admitted external-failure evidence, effect state reconciled, one explicit replacement allowance exists | distinct replacement may execute |
| Consumed run fails but observer state leaves a non-idempotent effect ambiguous | replacement blocked until state is reconciled; no blind replay |
| Replacement fails and finite allowance is exhausted | STOP; no implicit next execution |
| Original authority says `permitted_execution_count: 3` but defines no replacement policy | count alone does not classify or authorize causal replacement behavior |
| Replacement would require changed requirements or material scope | new work / new authority, not replacement |
| Provider/executor changes but remains within a prospectively declared interchangeable set and unchanged mode/protocol | may remain within same replacement authority |
| Execution changes from empirical provider run to host-assisted non-empirical recovery | new execution-strategy authority required |

These counterexamples distinguish the semantic class without embedding HTTP 429, Claude, browser, shell, or SVP-specific behavior in General Governance.

## 11. What is explicitly not being changed

This discovery does not reopen or challenge:

- bounded operational delegation;
- currentness/scope-drift stop rules;
- failed/indeterminate gate behavior;
- separation of modification, commit, push, PR, merge, release, deployment, and acceptance;
- merge-not-equal-acceptance;
- minimal durable bookkeeping after Owner decisions;
- historical immutability;
- `R<N>` correction identity;
- Packet 03 RUN-003, RUN-004, or RECOVERY-001 historical classification.

It also creates no schema, tool, release, publication, merge, deployment, or normative-amendment authority.

## 12. Recommended next decision

The Project Owner should decide whether to accept this discovery disposition:

`NORMATIVE_CLARIFICATION_CANDIDATE`

If accepted, the next separately authorized work should be a **small normative drafting package**, not a broad rc.4 redesign.

That package should be constrained to proposing the minimum Project Operating Contract clarification described in section 9, plus focused consistency tests/document checks. It should not introduce a run schema or modify L6 tooling unless the drafting/review process demonstrates a concrete machine-checkability requirement.

Until such a package is separately authorized and accepted, General Governance rc.4 remains unchanged.
