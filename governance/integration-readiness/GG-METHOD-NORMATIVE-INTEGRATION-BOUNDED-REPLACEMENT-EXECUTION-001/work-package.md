---
work_package_id: GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001
protocol_id: GG-METHOD-INTEGRATION-READINESS-PROTOCOL-001
protocol_version: 1.0.0
execution_id: GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
status: PREPARED
formal_input_package_sha256: b9dde57a0d25e8ec21808581595fcbaa6ed7a17d802bca6d6c19ed3fef333d26
accepted_implementation_head: 95e7dafac6afee54ca1ff6112dcd0cded74d08e8
---

# Work Package and Output Contract

## Objective

Determine the smallest release-packaging surface and safe sequencing needed to integrate the accepted bounded-replacement normative candidate without ever advancing `main` to a release-incoherent state.

## Required questions

1. Must rc.5 packaging be prepared on top of the accepted implementation before any PR/merge?
2. Which exact release-facing files must change and why?
3. Should normative implementation and rc.5 packaging be one release-ready PR or separate PRs?
4. What currentness and candidate-identity fences are required?
5. Which deterministic/CI checks must pass before merge?
6. How must PR, merge, tag, release, publication, and Owner acceptance remain separated?
7. How must the release content digest be sequenced relative to tracked validation/custody artifacts?

## Protocol

1. verify exact identities and preflight;
2. inspect only bound immutable evidence and current accepted branch state;
3. derive the minimum release surface from current validators plus prior rc.4 materialization evidence;
4. reject any plan that permits an incoherent intermediate `main`;
5. account for the fact that `release-manifest.json.content_sha256` covers every tracked file except the manifest itself;
6. produce one provider-neutral readiness result;
7. stop after validation; do not perform release packaging or publication.

## Declared output

`governance/integration-readiness/GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001/result.md`

Status: `VALIDATED_PENDING_PROJECT_OWNER_REVIEW`

Primary disposition must be exactly one of:

- `COMBINED_RELEASE_READY_INTEGRATION_REQUIRED`
- `SEPARATE_NORMATIVE_MERGE_SAFE`
- `NEEDS_REFINEMENT`
- `BLOCKED`

## Required result sections

1. Executive disposition
2. Bound identities
3. Release-conformance dependency
4. Minimum rc.5 packaging surface
5. Safe branch and commit sequencing
6. PR and merge topology
7. Content-digest finalization rule
8. CI and deterministic gates
9. Authority boundaries
10. Currentness and anti-drift fences
11. Explicit exclusions
12. Recommended next package

## Validation contract

Validate exact input digest, accepted implementation identity, all required sections, one disposition, release-surface rationale, safe no-intermediate-main proof, digest sequencing, CI gates, authority separation, and write-surface confinement.
