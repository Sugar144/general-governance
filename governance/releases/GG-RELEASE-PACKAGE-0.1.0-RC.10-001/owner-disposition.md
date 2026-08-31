---
disposition_id: GG-RC10-OWNER-DISPOSITION-001
record_type: PROJECT_OWNER_DISPOSITION
status: ACCEPTED
disposition_date: 2026-08-31
owner_authorization_prompt_id: GG-MP-0010
owner_authorization_source: governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.10-001/material-prompt.md
target_release: 0.1.0-rc.10
candidate_commit_sha: 976ddd086e72cfa3cfc31073b9013e17e97cb41b
release_content_sha256: 6d9c44c437fb8c34782d7935e1fd6e25310cb5c896df5296a01a6e63441b9733
release_manifest_git_blob_sha: 9f32618b82623591679918dd37b9adbd10a4e7ae
---

# General Governance rc.10 — Project Owner disposition

The Project Owner accepts the exact General Governance `0.1.0-rc.10` immutable candidate identified above after the Hierarchical Work Graph capability integrated through PR #35 and the exact implementation head `94ed6d116a55261f19ce138a6fcb34a0941c93ce` received an independent Codex `PASS` with no actionable findings.

The exact Owner instruction authorizing this disposition is preserved under prompt identity `GG-MP-0010` at the repository-custodied source identified in the front matter.

This disposition closes the Owner-decision boundary for the exact rc.10 candidate identity. It does not rewrite `release-manifest.json`: the manifest remains part of the immutable release payload and its `IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION` text is historical candidate-state truth. This operational disposition lives under the reserved `governance/` prefix and therefore remains outside the scoped rc.10 release-content identity.

## Accepted capability change

The Owner accepts HWG `1.0.0` as an optional reusable General Governance L2 capability with:

- project-type-neutral ordered hierarchy profiles;
- sibling-only DAG dependencies;
- exact reciprocal parent/child graph expansion;
- progressive/JIT materialization;
- exact graph-file and represented source lineage;
- no forced one-parent/one-child decomposition;
- completion eligibility explicitly separate from acceptance;
- graph validity explicitly separate from implementation authority;
- absence of dependency explicitly insufficient to prove concurrent safety;
- optional adopter activation through `configuration.capabilities.hierarchical_work_graph.bundle_path`.

The Owner also accepts the review hardening incorporated before merge: graph SHA-256 and parse operate on the same single-read byte buffer, and dependency/hierarchy traversal no longer depends on Python recursion depth.

## Authority granted

This disposition authorizes treating the exact rc.10 identity above as an Owner-accepted General Governance candidate for future explicitly bounded adopter evaluation/rebinding work, subject to each adopter's own authority, currentness, compatibility, conformance, review, and merge gates.

It also authorizes repository-local governance records to cite this disposition as the Owner acceptance evidence for rc.10.

## Authority not granted

This disposition does not authorize:

- a General Governance Git tag or GitHub Release;
- release publication, deployment, or production-readiness claims;
- mutation of the immutable rc.10 release-content bytes;
- AEA D1/D2 rerun or any provider execution;
- Dopis product implementation execution;
- scheduler/CWG runtime activation;
- pilot, deployment, or public launch;
- bypass of adopter-owned validation, review, currentness, or merge gates.

A Dopis rebind from rc.9 to rc.10 remains a separate downstream repository block even though the Owner has already authorized that bounded rebind work.
