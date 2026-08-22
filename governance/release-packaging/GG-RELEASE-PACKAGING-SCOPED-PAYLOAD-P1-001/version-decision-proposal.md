# Successor Version Decision Proposal

Status: `PROPOSED_NOT_AUTHORIZED`

Recommended successor version:

`0.1.0-rc.8`

Rationale:

- protected `main` currently publishes the `0.1.0-rc.7` release-candidate line;
- P1 packages a prospective mechanism already independently validated in I1 rather than declaring General Governance `0.1.0` final;
- incrementing the prerelease ordinal preserves the existing release-candidate sequence without reinterpreting rc.7;
- no compatibility declaration is changed by this recommendation.

This proposal does not select the version and grants no mutation authority. The Project Owner must explicitly authorize the exact version before P1 execution may modify `RELEASE_VERSION` or `release-manifest.json`.
