# General Governance Roadmap

This is the compact planning surface used by Project State Integrity and portfolio aggregation. It does not replace immutable release manifests, framework contracts, provenance, historical evidence, or Project Owner decisions.

## Current stage — rc.8 operationalization

General Governance `0.1.0-rc.8` is integrated on `main` with manifest schema `1.4.0` and `SCOPED_TRACKED_FILES_V1`.

Completed in this stage:

- separate Framework Release Payload from the GG Operational / Evolution Plane;
- preserve historical rc.7 identity semantics unchanged;
- validate scoped payload identity with full-checkout Gate A and isolated-payload Gate B;
- harden scoped identity against unsupported Git entry types and executable-mode drift;
- integrate the rc.8 successor release candidate;
- prove operational-plane evolution by integrating the non-normative SVP Guided Answering learning-lifecycle PRE-RUN-002 without changing the rc.8 framework payload digest;
- adopt Project State Integrity on the rc.8 operational plane.

## Active release gate

The rc.8 manifest remains `IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION`.

Completion condition for this gate:

- the Project Owner records an explicit disposition of the exact rc.8 release candidate under the applicable release authority.

Merge of operational-plane work does not imply release acceptance. Tagging, GitHub Release creation, deployment/publication, consumer/adopter upgrade, and adopter mutation remain separately governed effects.

## Operational / evolution work

Repository-operational evidence, project state, roadmap, instructions, and bounded pilots may evolve without creating a new framework release identity only when `release-manifest.json` explicitly classifies those paths as operational and all applicable governance/currentness/CI gates remain satisfied.

The cross-project learning lifecycle pilot remains non-normative. Any further pilot execution, target-project mutation, normative promotion, or framework change requires its own accepted authority and evidence.

## Historical preservation

PR #15 (Project State Integrity on rc.7) and PR #16 (learning PRE-RUN-001 on rc.7) remain frozen empirical evidence of the legacy all-tracked-files release-identity limitation. They are not successors to current operational work and must not be rebased, repaired in place, or merged.

## Planning rule

Material changes to phase structure, sequencing, dependencies, deferral, cancellation, or newly defined future work must update this roadmap in the same pull request and declare `Project-State-Impact: roadmap` or `both`.
