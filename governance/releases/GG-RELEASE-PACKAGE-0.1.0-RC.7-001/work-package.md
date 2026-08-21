---
package_id: GG-RELEASE-PACKAGE-0.1.0-RC.7-001
block_id: GG-WPDC-AGENT-SKILL-001-P5
status: AUTHORIZED_IN_PROGRESS
target_release: 0.1.0-rc.7
base_main: 09d678374c310d67a7ce56ef536dce6d94caef01
integration_branch: release/0.1.0-rc.7
accepted_candidate: 1d67a70ae64b9b46227f9d56b1a3c40aba40373c
---

# Work Package — WPDC Agent Layer rc.7 Release Integration

## Objective

Produce and publish the exact General Governance `0.1.0-rc.7` release candidate containing the reviewed WPDC agent layer, with a reproducible release-content identity and one pull request to `main`.

## Authorized tracked write surface

Existing files:

- `RELEASE_VERSION`;
- `release-manifest.json` as the final tracked mutation.

New release-package custody is limited to:

- `governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.7-001/**`.

`README.md`, `docs/consumer-contract.md`, and `.github/workflows/conformance-ci.yml` may change only if direct inspection establishes a mechanical release-consistency requirement. No such requirement is presumed. No reviewed agent implementation, fixture, P1/P2/P2A/P3 evidence, WPDC contract, schema, or validator may change.

## Required release properties

- framework contract remains `2.0.0`;
- consumer lock schema remains `2.0.0`;
- consumer configuration schema remains `1.0.0`;
- capability composition remains optional at contract/schema `1.0.0`;
- WPDC remains optional with contract, adoption contract, binding schema, and manifest schema `1.0.0`;
- the five canonical agent surfaces are required framework surfaces; provider projections and fixture files are not;
- `PF-1` remains `NON_BLOCKING_ACCEPTED_LIMITATION` and is not corrected here;
- rc.6's content identity is neither preserved nor rewritten.

## Integration gates

Before publication, confirm the required `origin/main` and accepted-candidate ancestry, run the existing conformance/release gates using the CI-supported Python version, reproduce the final content digest, and verify that `release-manifest.json` is the final tracked mutation.

The release branch may be pushed and one PR to `main` opened only after local gates pass. Required CI must be observed. This package does not authorize tag creation, GitHub Release creation, deployment, SVP action, or merge.

## Exact next gate

When required CI is green: `INDEPENDENT_EXACT_CANDIDATE_RECHECK_OF_GG_0.1.0_RC.7`.
