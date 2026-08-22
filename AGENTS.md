# General Governance — Repository Execution Contract

This file defines provider-neutral execution behavior for work in this repository. Repository state and accepted canonical artifacts are durable truth; conversation, summaries, and model memory are working context only.

General Governance is a reusable framework repository. Framework-owned normative surfaces, immutable release evidence, Project Owner decisions, and adopter-owned state remain distinct. Repository access or framework availability does not grant adopter mutation, release, publication, deployment, or acceptance authority.

Before material work, resolve the exact repository/ref, applicable accepted authority, current project state, controlling framework/release artifacts, permitted write/effect surface, validation, publication boundary, and mandatory stop.

## Project state integrity

This repository adopts the project-local state/roadmap integrity contract declared in `project-state-integrity.json`.

- Before material work, read `project-state-integrity.json`, `PROJECT_STATE.yaml`, and `ROADMAP.md`.
- Every pull request must contain exactly one `Project-State-Impact: none|state|roadmap|both` declaration.
- If merging the change would materially change accepted/canonical project truth — including phase, milestone, status, active or next gate, integrated work, material blocker, release-candidate disposition, or tracked authority state — the same pull request must update `PROJECT_STATE.yaml` and declare `state` or `both`.
- If the project plan itself changes materially — including phase structure, sequencing, dependencies, deferral, cancellation, or newly defined future work — the same pull request must update `ROADMAP.md` and declare `roadmap` or `both`.
- `none` is valid only when neither canonical project truth nor roadmap structure changes; it must never be used to avoid required state bookkeeping.
- `PROJECT_STATE.yaml` is the compact current-state projection for portfolio consumption. It does not replace immutable release manifests, framework contracts, provenance, historical evidence, or Owner decisions.
- State/roadmap bookkeeping records an already-authorized or accepted result. It does not grant merge, Owner acceptance, release/tag/publication, deployment, adopter mutation, risk acceptance, or constitutional authority.
- Run the Project State Integrity checker/workflow before completion. The checker validates declared/file consistency only; the implementer and reviewer remain responsible for the semantic impact classification.

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
