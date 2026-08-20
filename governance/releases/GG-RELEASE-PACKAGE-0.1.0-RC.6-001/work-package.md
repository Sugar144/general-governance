---
package_id: GG-RELEASE-PACKAGE-0.1.0-RC.6-001
block_id: GG-WPDC-FRAMEWORK-RELEASE-INTEGRATION-001
status: AUTHORIZED_IN_PROGRESS
target_release: 0.1.0-rc.6
base_main: 640fb33bc96bff75d757b8325ae6290c1a4e0f2f
integration_branch: method/wpdc-normative-capability-adoption-001
pull_request: 13
---

# Work Package — WPDC Framework Release Integration

## Objective

Integrate the accepted WPDC architecture, normative/adoption contracts, machine schemas, dedicated validator, and generic regressions into one coherent General Governance release candidate `0.1.0-rc.6`, preserving optional adoption and all existing rc.5 compatibility contracts.

## Authorized tracked write surface

Existing files:

- `RELEASE_VERSION`;
- `README.md`;
- `docs/consumer-contract.md`;
- `.github/workflows/conformance-ci.yml`;
- `release-manifest.json` as the final tracked mutation.

New release-package custody is limited to:

- `governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.6-001/**`.

No other existing framework/schema/validator/test semantics may change inside this block unless a final gate reveals an implementation defect strictly within the already accepted WPDC contract.

## Required release properties

- framework contract remains `2.0.0`;
- consumer lock schema remains `2.0.0`;
- consumer configuration schema remains `1.0.0`;
- capability composition remains optional contract/schema `1.0.0`;
- WPDC is advertised as optional L2 contract/adoption/machine contract version `1.0.0`;
- absence of WPDC adoption causes no consumer configuration migration;
- `VALID_DEPENDENCY_CLOSED` never creates execution authority;
- rc.5 identity is never rewritten.

## CI gates

Under GitHub Actions CPython 3.12:

1. validate all JSON schemas;
2. compile capability-stack and WPDC validators;
3. run prospective extraction-evolution verification;
4. compute exact release content digest;
5. run existing consumer conformance tests;
6. run WPDC machine-contract and control-declaration regressions.

## Integration gates

PR #13 may leave draft only when:

- `release-manifest.json` reproduces the exact tracked-content digest;
- required `consumer-contract` is green on the exact candidate;
- WPDC tests are green under CI Python 3.12;
- referenced architecture/normative/machine provenance remains reachable;
- PR is mergeable against unchanged/current `main`;
- no unresolved material review thread remains.

If all gates pass, the block authorization permits exact-head merge. It does not authorize tag, GitHub Release, deployment, SVP adoption, or skill implementation.
