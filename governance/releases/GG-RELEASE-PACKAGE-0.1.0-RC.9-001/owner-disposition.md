---
disposition_id: GG-RC9-OWNER-DISPOSITION-001
record_type: PROJECT_OWNER_DISPOSITION
status: ACCEPTED
disposition_date: 2026-08-30
owner_authorization_prompt_id: GG-MP-0009
owner_authorization_source: governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.9-001/material-prompt.md
target_release: 0.1.0-rc.9
candidate_commit_sha: d74b5d25258ed3679ed8135061ca540ba6f83b61
release_content_sha256: 8ee5329e806de07d7db0d9cf642a2a52496de6dc9f4ce3e567e9ac92c4849c86
release_manifest_git_blob_sha: a86bab92395f70ed56596f41cca940f72cbe432f
---

# General Governance rc.9 — Project Owner disposition

The Project Owner accepts the exact General Governance `0.1.0-rc.9` immutable candidate identified above after the WPDC Designer dependency-discovery hardening integrated through PR #33.

The exact Owner instruction authorizing this disposition is preserved under prompt identity `GG-MP-0009` at the repository-custodied source identified in the front matter.

This disposition closes the Owner-decision boundary for the exact rc.9 candidate identity. It does not rewrite `release-manifest.json`: the manifest remains part of the immutable release payload and its `IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION` text is historical candidate-state truth. This operational disposition lives under the reserved `governance/` prefix and therefore remains outside the scoped rc.9 release-content identity.

## Accepted capability change

The Owner accepts the rc.9 WPDC Designer hardening that requires:

- local/external seam separation when bound sources require packet-local consumption work;
- surface-to-node closure;
- integration-edge closure;
- validation-reachability closure;
- Stage 8 no-findings output to remain bounded self-challenge evidence rather than a semantic-completeness warrant;
- regression qualification of those controls in the release payload.

WPDC capability/adoption/binding/manifest contract versions remain `1.0.0`; no schema, resolution enum, deterministic-validator semantic, or execution-authority expansion is accepted by this disposition.

## Authority granted

This disposition authorizes treating the exact rc.9 identity above as an Owner-accepted General Governance candidate for future explicitly bounded adopter evaluation/rebinding work, subject to each adopter's own authority, currentness, compatibility, conformance, review, and merge gates.

It also authorizes repository-local governance records to cite this disposition as the Owner acceptance evidence for rc.9.

## Authority not granted

This disposition does not authorize:

- a General Governance Git tag or GitHub Release;
- deployment, publication, or production-readiness claims;
- mutation of the immutable rc.9 release-content bytes;
- automatic rebinding or mutation of Dopis or any other adopter;
- Dopis P6, AEA D1/D2, product implementation, pilot, deployment, or public launch;
- bypass of adopter-owned validation, review, currentness, or merge gates.

Any Dopis rebind from rc.8 to rc.9 remains a separate downstream block with its own repository evidence and merge gate.
