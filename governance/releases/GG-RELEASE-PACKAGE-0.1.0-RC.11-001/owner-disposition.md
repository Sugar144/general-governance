---
disposition_id: GG-RC11-OWNER-DISPOSITION-001
record_type: PROJECT_OWNER_DISPOSITION
status: ACCEPTED
disposition_date: 2026-09-22
owner_authorization_prompt_id: GG-MP-0011
owner_authorization_source: governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.11-001/material-prompt.md
target_release: 0.1.0-rc.11
candidate_commit_sha: e64324e3b0104ec98594d85505a4a9804a212ca2
integrated_main_commit_sha: 4eb2e8295ac99a8cfb26fb9976a779fa70bd540d
release_content_sha256: 70bf517f755557772c85c62ff1999b7df45dd093f0ee57be610cc2e96740a5ad
release_manifest_git_blob_sha: 62cccd9c9253f04b2be9b0d4de3987f5354a3062
---

# General Governance rc.11 — Project Owner disposition

The Project Owner accepts the exact General Governance `0.1.0-rc.11` successor candidate identified above. This successor exists solely because the qualified Factory runner migration changes `.github/workflows/conformance-ci.yml`, an explicitly protected `SCOPED_TRACKED_FILES_V1` release surface, and therefore cannot reuse the immutable rc.10 content identity.

The exact Owner instruction authorizing rc.11 packaging and integration is preserved under prompt identity `GG-MP-0011` at the repository-custodied source identified in the front matter.

The technical candidate `e64324e3b0104ec98594d85505a4a9804a212ca2` qualified with both `Factory Runner Conformance` and the protected `consumer-contract` workflow passing. Gate B isolated payload self-sufficiency and Gate A exact checkout release identity both passed against release-content SHA-256 `70bf517f755557772c85c62ff1999b7df45dd093f0ee57be610cc2e96740a5ad`. The candidate was then integrated through PR #40 as main commit `4eb2e8295ac99a8cfb26fb9976a779fa70bd540d` without bypassing branch protection.

This disposition closes the Owner-decision boundary for the exact rc.11 candidate identity. It does not rewrite `release-manifest.json`; the manifest's `IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION` value remains historical candidate-state truth, consistent with prior release practice. This operational disposition lives under the reserved `governance/` prefix and therefore remains outside the scoped rc.11 release-content identity.

## Accepted change

The Owner accepts the provider-free Factory runner conformance migration for General Governance:

- canonical `factory-ci` self-hosted execution;
- preprovisioned Python 3.12 verification instead of runtime baseline installation;
- isolated job dependencies;
- preserved consumer-contract semantics and release-payload gates;
- repository-local Factory Runner Conformance enforcement.

No reusable framework capability semantics beyond this execution/integration surface are accepted or changed by rc.11.

## Authority granted

This disposition authorizes treating the exact rc.11 identity above as the Owner-accepted General Governance successor candidate and authorizes ASF to re-anchor General Governance portfolio qualification from the temporary candidate ref to `main`.

## Authority not granted

This disposition does not authorize:

- a Git tag or GitHub Release;
- release publication, deployment, or production-readiness claims;
- provider/model execution;
- downstream adopter rebinding except the bounded ASF portfolio-ref reconciliation;
- bypass of adopter-owned validation, review, currentness, compatibility, or merge gates.
