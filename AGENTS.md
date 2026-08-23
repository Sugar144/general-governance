# General Governance — Repository Execution Contract

This file defines provider-neutral execution behavior for material work in this repository. Repository state, accepted canonical artifacts, exact Git identities, and durable Owner decisions are truth; conversation, summaries, and model memory are working context only.

General Governance is both a reusable framework repository and a governed project. Its Framework Release Payload and its GG Operational / Evolution Plane are distinct. `release-manifest.json` controls that classification; repository access or framework availability never grants adopter mutation, release, publication, deployment, or acceptance authority.

Before material work, resolve the exact repository/ref, applicable accepted authority, `PROJECT_STATE.yaml`, `ROADMAP.md`, controlling release/framework artifacts, permitted write/effect surface, validation requirements, publication boundary, and mandatory stop.

## Project State Integrity

This repository adopts the project-local state/roadmap integrity contract declared in `project-state-integrity.json`.

- Before material work, read `project-state-integrity.json`, `PROJECT_STATE.yaml`, and `ROADMAP.md`.
- Every pull request must contain exactly one `Project-State-Impact: none|state|roadmap|both` declaration.
- If merging a change would materially change accepted/canonical project truth — including phase, milestone, status, active or next gate, accepted/integrated work that changes project position, material blocker, release-candidate disposition, or tracked authority state — the same pull request must update a configured state path and declare `state` or `both`.
- If the project plan changes materially — including phase structure, sequencing, dependencies, deferral, cancellation, or newly defined future work — the same pull request must update a configured roadmap path and declare `roadmap` or `both`.
- `none` is valid only when neither semantic condition applies. It must never be used to avoid required bookkeeping.
- `PROJECT_STATE.yaml` is the compact current-state projection for portfolio consumption. It does not replace immutable release manifests, framework contracts, provenance, historical execution/review evidence, or Owner decisions.
- A richer canonical ledger may coexist with this projection. Preserve its authority and keep the compact projection synchronized; do not create competing truths.
- State/roadmap bookkeeping records already-authorized or accepted truth. It does not grant merge, Owner acceptance, tag/release/publication, deployment, adopter mutation, risk acceptance, or constitutional authority.
- Run the Project State Integrity checker/workflow before completion. The checker validates deterministic declaration/file consistency only; implementer and reviewer remain responsible for semantic impact classification.

## Release and operational-plane boundary

For `0.1.0-rc.8` and later scoped identities, `SCOPED_TRACKED_FILES_V1` is fail-closed: unknown tracked paths are release-included unless the manifest explicitly classifies them as operational. The root PSI surfaces are operational exact-path exclusions already declared by the rc.8 manifest. Changes under those excluded surfaces must still preserve exact repository identity, governance authority, and all applicable CI; operational exclusion is not a bypass.

Historical rc.7 evidence retains its legacy all-tracked-files identity and must never be reinterpreted through rc.8 semantics.

## Authority boundary

Preserve these distinctions:

```text
design != modify
modify != commit/push
commit/push != PR
PR/review != merge/release/publication/acceptance
```

Optional framework capabilities are absent unless explicitly adopted by a consumer. General Governance authority does not extend into adopter repositories without an exact accepted cross-repository task.

Stop at the next genuine material authority boundary.