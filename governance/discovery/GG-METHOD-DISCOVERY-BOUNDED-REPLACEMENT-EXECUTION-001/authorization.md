---
record_id: GG-METHOD-DISCOVERY-BOUNDED-REPLACEMENT-EXECUTION-001-AUTH-001
record_type: PROJECT_OWNER_FORMAL_EXECUTION_AUTHORIZATION
status: ACTIVE_PROSPECTIVE
execution_id: GG-METHOD-DISCOVERY-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
work_identity: GG-METHOD-DISCOVERY-BOUNDED-REPLACEMENT-EXECUTION-001
role: METHOD_DISCOVERY_ANALYST
mode: READ_ONLY_SYNTHESIS
protocol: GG-METHOD-DISCOVERY-PROTOCOL-001
formal_input_package_sha256: 88033d59120ab2a3e9e226fd5f4985d7952a5dc7ecda8601b14c89da8dd7cbe8
permitted_execution_count: 1
general_governance_baseline: 91fa0727abf730e142a4c43f2da68b1281be1121
branch: method/discovery-bounded-replacement-execution-001
owner_issue: 5
owner_authorization_comment_id: 5335539678
---

# Formal Discovery Execution Authorization

## Owner authority

The Project Owner's current instruction was `adelante`. It was resolved prospectively and durably in General Governance Issue #5 comment `5335539678` as:

`AUTHORIZE_GG_METHOD_DISCOVERY_BOUNDED_REPLACEMENT_EXECUTION_001`

That record authorizes exactly one formal discovery execution for the execution identity above.

## Authorized effects

This authorization permits, only for this work identity:

1. creation/use of the dedicated discovery branch from the exact General Governance baseline;
2. repository custody of this authorization, the bound input package, work package/output contract, material prompt, preflight, run record, validation record, and declared discovery result;
3. one read-only methodology analysis over the bound evidence;
4. materialization and deterministic validation of the declared result under the discovery directory;
5. durable issue bookkeeping needed to point reviewers to the exact result.

The analysis may recommend a later normative clarification. Recommendation is not adoption authority.

## Allowed write surface

Only:

`governance/discovery/GG-METHOD-DISCOVERY-BOUNDED-REPLACEMENT-EXECUTION-001/**`

No pre-existing file may be modified by this execution.

## Forbidden actions

The execution MUST NOT:

- modify `framework/core/project-operating-contract.md`;
- modify any file under `framework/**`, `contracts/**`, `tools/**`, `tests/**`, `provenance/**`, `.github/**`, or `docs/**`;
- modify `README.md`, `RELEASE_VERSION`, or `release-manifest.json`;
- rewrite any SVP historical evidence;
- merge;
- tag;
- release;
- deploy;
- claim Project Owner acceptance;
- claim normative adoption;
- create or infer a second, replacement, retry, or recovery execution.

A failure does not create additional execution authority.

## Fail-closed conditions

The run MUST NOT begin, or MUST stop immediately, if:

- General Governance `main` is not exactly `91fa0727abf730e142a4c43f2da68b1281be1121`;
- the dedicated branch was not derived from that exact baseline;
- the formal input package digest differs from `88033d59120ab2a3e9e226fd5f4985d7952a5dc7ecda8601b14c89da8dd7cbe8`;
- any bound immutable source identity differs;
- any required preparation artifact is missing;
- the planned write surface expands beyond the discovery directory;
- a failed or indeterminate preparation gate occurs;
- the analysis requires a new material authority, scope, architecture, security/privacy, release, or adoption decision.

## Authority boundary

This record is execution authority, not methodology acceptance. The terminal discovery result remains `PENDING_PROJECT_OWNER_REVIEW` until the Owner separately accepts, rejects, or refines it.
