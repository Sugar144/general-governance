---
disposition_id: GG-RC8-DOPIS-ADOPTION-DISPOSITION-001
record_type: PROJECT_OWNER_DISPOSITION
status: ACCEPTED
disposition_date: 2026-08-28
owner_authorization_source: project_conversation
target_release: 0.1.0-rc.8
candidate_commit_sha: 486a6826685635eff0b4098fd33c4dfd826fb7ed
release_content_sha256: 1ab4589a24a9e8a8bd8dce96931d4d7e2468a5644fad853bcdab411808b0cecf
release_manifest_sha256: ee9fb895c98f6c18b04b1896d579c42e4cb7e333286103de11898bfd0d972c66
adopter: Sugar144/dopis
adopter_plan: DOPIS-PLAN-005
---

# General Governance rc.8 — bounded Dopis adoption disposition

The Project Owner accepts the exact General Governance `0.1.0-rc.8` immutable candidate identified above for bounded external-consumer adoption by `Sugar144/dopis` under `DOPIS-PLAN-005`.

This disposition closes the Owner-decision boundary for Dopis to pin that exact immutable framework identity and explicitly activate the optional Work Packet Design & Dependency Closure capability, subject to Dopis-owned consumer conformance, capability binding, capability-stack compatibility evidence, and its own authority model.

The disposition does not rewrite `release-manifest.json` or the rc.8 release-content identity. The record lives under the reserved operational `governance/` prefix and therefore remains outside the scoped rc.8 release-content identity.

## Authority granted

For Dopis only, this disposition authorizes the bounded adopter-side work needed to:

- replace the current Dopis General Governance lock with the exact rc.8 identity above;
- create and select an adopter-owned WPDC binding compliant with WPDC adoption contract `1.0.0`;
- update Dopis capability-composition evidence for the new exact General Governance identity;
- run deterministic General Governance consumer, capability-stack, and WPDC validation;
- use the resulting valid WPDC adoption for the technical-planning scope already authorized by `DOPIS-PLAN-005`.

## Authority not granted

This disposition does not authorize:

- a General Governance tag or GitHub Release;
- deployment or publication beyond the exact bounded adopter use above;
- mutation of any other adopter;
- Dopis product implementation, merge of product code, pilot, deployment, or public launch;
- modification of WPDC normative semantics, schemas, validators, or accepted rc.8 release content;
- acceptance of an invalid or non-conforming Dopis binding;
- general-platform or production-readiness claims for General Governance.

Dopis product implementation remains a later, separate Owner decision bound to the validated implementation scope produced by `DOPIS-PLAN-005`.
