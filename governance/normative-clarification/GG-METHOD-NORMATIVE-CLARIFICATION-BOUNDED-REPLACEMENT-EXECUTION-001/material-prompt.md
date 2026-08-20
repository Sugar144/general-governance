---
prompt_id: GG-MP-0002
version: 1.0.0
category: FORMAL_NORMATIVE_CLARIFICATION_DRAFTING
custody_status: APPROVED_NOT_EXECUTED
execution_id: GG-METHOD-NORMATIVE-CLARIFICATION-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
formal_input_package_sha256: a3e1b427579579432dff3556f06afdc746c0e0fd67c2ab5a72b423f88c936825
authority_record: GG-METHOD-NORMATIVE-CLARIFICATION-BOUNDED-REPLACEMENT-EXECUTION-001-AUTH-001
output_path: governance/normative-clarification/GG-METHOD-NORMATIVE-CLARIFICATION-BOUNDED-REPLACEMENT-EXECUTION-001/proposal.md
---

# Material Prompt Snapshot

Execute exactly one proposal-only formal normative-clarification drafting analysis for
`GG-METHOD-NORMATIVE-CLARIFICATION-BOUNDED-REPLACEMENT-EXECUTION-001`.

Use only the evidence bound by input package SHA-256
`a3e1b427579579432dff3556f06afdc746c0e0fd67c2ab5a72b423f88c936825`, the exact General Governance baseline
`91fa0727abf730e142a4c43f2da68b1281be1121`, and the accepted discovery at
`9be04b980cdaffa0bf61a41687e39700554fecbf`.

Draft the minimum exact provider-neutral wording needed in the Project Operating Contract to define bounded replacement execution after a consumed terminal failure. Specify the exact insertion point, show compatibility with rc.4, prove that delegated authority is not enlarged, and test the wording against the accepted counterexamples.

The wording must preserve that failure creates zero authority, replacement is a distinct identity, bare `permitted_execution_count > 1` is not replacement authority, same-identity resume and `R<N>` correction remain distinct, replacement allowance is finite and explicit, and authority-bound execution-strategy changes require new authority.

Do not edit the Project Operating Contract or any existing file. Do not create schemas/tooling, PRs, merges, releases, tags, deployments, or a second run.

Materialize the proposal exactly at the declared output path with one permitted proposal disposition and status `VALIDATED_PENDING_PROJECT_OWNER_REVIEW`. A validated wording proposal is not normative adoption or implementation authority.
