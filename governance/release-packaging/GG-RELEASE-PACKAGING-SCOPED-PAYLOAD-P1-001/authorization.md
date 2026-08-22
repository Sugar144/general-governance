---
record_id: GG-RELEASE-PACKAGING-SCOPED-PAYLOAD-P1-001-AUTH-001
record_type: PROJECT_OWNER_EXECUTION_AUTHORITY
status: ACTIVE_FOR_ONE_BOUNDED_P1_EXECUTION
issue: 24
authorized_version: 0.1.0-rc.8
source_i1_candidate: 201a4566bfff7c35c56ad112f203c46f19d70385
prepared_branch_head_before_authority: 676977a76db152cabd757f3d5fb0e5513f8a30a6
---

# P1 execution authority

The Project Owner explicitly authorized the immediately preceding P1 version gate by replying `autorizo`. The bound version is `0.1.0-rc.8`, which was the exact version proposal presented at that gate.

## Authorized non-custody write surface

Exactly:

- `RELEASE_VERSION`
- `release-manifest.json`

Custody writes are limited to:

`governance/release-packaging/GG-RELEASE-PACKAGING-SCOPED-PAYLOAD-P1-001/**`

## Authorized packaging semantics

- `RELEASE_VERSION = 0.1.0-rc.8`
- `manifest_schema_version = 1.4.0`
- `content_identity.method = SCOPED_TRACKED_FILES_V1`
- default classification `RELEASE_INCLUDED`
- manifest self-excluded from `content_sha256`
- reserved operational prefix exactly `governance/`
- operational exact-path exclusions only from the accepted fixed allowlist
- compatibility tuple remains framework contract `2.0.0`, consumer-lock schema `2.0.0`, consumer-configuration schema `1.0.0`

## Required gates

The resulting exact candidate must pass Gate A, Gate B, targeted release-payload regressions, the full test suite with the P1 bootstrap failures eliminated, rc.7 historical reproduction, WPDC compatibility, consumer-lock sufficiency, and fresh independent semantic/security review.

## Stop conditions

STOP on any need to modify a third non-custody path, compatibility drift, failed or indeterminate required gate, candidate/currentness drift, or any requirement for PR/merge/tag/release/publication/adopter mutation.

## Authority exclusions

This authority grants no PR, merge, tag, GitHub Release, deployment/publication, adopter mutation, frozen PR #15/#16 mutation, learning-pilot successor execution, PSI successor execution, or SVP mutation authority.
