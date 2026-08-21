---
authorization_id: AUTHORIZE_GG_RELEASE_PACKAGE_0.1.0_RC.7_001
package_id: GG-RELEASE-PACKAGE-0.1.0-RC.7-001
block_id: GG-WPDC-AGENT-SKILL-001-P5
owner_authorization_source: project conversation
authorized_at_branch_head: 1d67a70ae64b9b46227f9d56b1a3c40aba40373c
main_baseline: 09d678374c310d67a7ce56ef536dce6d94caef01
target_release: 0.1.0-rc.7
---

# rc.7 Release Integration Authorization

The Project Owner authorized this bounded release integration to produce and publish exactly one rc.7 release-candidate pull request from the accepted Block 4 candidate, subject to all repository gates, currentness checks, and review findings passing.

The authorization covers release-package custody, the rc.7 version and release manifest, deterministic release-content identity finalization, branch publication, one pull request to `main`, and correction only of release-integration defects within this write surface.

It does not authorize modification of the reviewed agent implementation, fixtures, P1/P2/P2A/P3 evidence, WPDC contracts, schemas, validators, tags, GitHub Releases, deployments, SVP, or merge.

## Bound inputs

- accepted Block 4 candidate: `1d67a70ae64b9b46227f9d56b1a3c40aba40373c`;
- required `origin/main`: `09d678374c310d67a7ce56ef536dce6d94caef01`;
- target release: `0.1.0-rc.7`;
- release-package precedent: `governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.6-001/`.

## Release sequencing invariant

Every tracked rc.7 mutation other than `release-manifest.json` MUST be complete before calculating the release content digest. `release-manifest.json` MUST be the final tracked-file mutation; no tracked file may change after it is finalized.

PF-1 remains `NON_BLOCKING_ACCEPTED_LIMITATION` and is not a correction target in this release integration.
