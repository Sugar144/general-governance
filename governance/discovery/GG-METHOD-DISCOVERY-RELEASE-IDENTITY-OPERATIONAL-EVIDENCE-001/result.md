---
discovery_id: GG-METHOD-DISCOVERY-RELEASE-IDENTITY-OPERATIONAL-EVIDENCE-001
run_id: GG-METHOD-DISCOVERY-RELEASE-IDENTITY-OPERATIONAL-EVIDENCE-001-RUN-001
status: EXECUTED_PENDING_VALIDATION
disposition: RELEASE_IDENTITY_ARCHITECTURE_CHANGE_CANDIDATE
baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
input_sha256: 2457e3f0e1b12af74e91697bedd91550d59c7c16828006ac203e10bdc27ecc41
---

# Release identity vs repository operational evidence — discovery result

## Evidence and facts

1. General Governance rc.7 is represented on `main` by exact commit `22a1d5e2f759fda53574884e1056a3a56baa211a`. Its `release-manifest.json` declares framework version `0.1.0-rc.7` and `content_sha256 = 14fceee7fb261fee6c2b515cbd81e39c91daaaaa3aa8dc431d3c1beac754d15e`.
2. `docs/consumer-contract.md` defines an immutable consumer identity tuple containing repository, version, exact `commit_sha`, and exact `release_manifest_sha256`. It additionally states that the release manifest hashes the complete release content set excluding the manifest itself.
3. `tools/validate_consumer.py::release_content_digest` implements that statement by hashing every Git-tracked path except `release-manifest.json`.
4. `tools/validate_consumer.py` separately requires the running framework checkout HEAD to equal the exact commit selected by the consumer lock, requires the release-manifest bytes to reproduce the lock's manifest digest, and requires the release content digest to reproduce the manifest.
5. `tools/validate_work_packet.py::verify_locked_framework_identity` imports the same `release_content_digest` and applies the same exact checkout/manifest/content-identity gates before WPDC adopter validation.
6. The Project Operating Contract simultaneously requires repository custody for material prompts/formal-run evidence and requires material learning/methodology evidence to become durable rather than remain only in chat. General Governance therefore has legitimate tracked repository state that serves project/evolution governance rather than consumer framework behavior.
7. PR #15, Project State Integrity adoption, adds repository-control/state surfaces. Its dedicated Project State Integrity workflow passed, while `conformance-ci` failed in WPDC regressions because the checkout content digest became `d0fda78cc3f459e6b33340c5e1e373035fc1d03d257b5410b79ad5685a3a108e`, which no longer matched the immutable rc.7 manifest.
8. PR #16, the validated cross-project learning pilot package, independently produced the same failure class. Its package-local validation was `17/17 PASS`, while `conformance-ci` run `32580573924` failed because the checkout content digest became `07bf76879f79b0071398f903404ed7bb626fd7fac6c1ebd700f70473014f7ab3`.
9. PR #15 and PR #16 have different purposes and different changed files. Their common failure is therefore structural rather than specific to either feature.
10. No evidence supports weakening immutable consumer commit binding, changing rc.7 retrospectively, or treating the failures as flaky CI.

## Identity invariant analysis

The three current identity elements serve different purposes and should remain distinct:

- `commit_sha` binds the complete immutable Git repository revision and therefore protects all tracked bytes, including operational/evolution evidence, in that selected revision.
- `release_manifest_sha256` binds the exact release declaration: version, compatibility, capability advertisement, content-identity method and release metadata.
- `content_sha256` provides a deterministic content identity independent of Git object/history encoding. Its semantic purpose should be to identify the **framework release payload**, not necessarily every byte used to operate the General Governance repository as a project.

The current architecture makes `content_sha256` coextensive with the complete tracked tree. That is stronger than necessary for consumer payload integrity because the exact Git commit is already independently bound. It also couples two lifecycle domains:

1. **framework release evolution** — normative contracts, schemas, consumer-facing tools, reusable implementation, release documentation and other bytes whose change can alter what a consumer receives or how it is validated; and
2. **repository operational/evolution custody** — Project Owner decisions, project state/roadmap, repository-agent instructions, discovery/pilot evidence, work-package evidence and repository-only controls.

The coupling is operationally unsustainable under the current POC: routine evidence custody can require a new framework release even when no framework payload byte or consumer-facing semantic changed.

The safe correction is not to stop binding operational bytes. Git `commit_sha` continues to bind them. The correction is to stop claiming that every tracked byte is part of the framework **release payload identity**.

A path excluded from release-payload hashing must never be allowed to become an undeclared dependency of consumer-visible release behavior. Therefore any scoped content model requires a deterministic independence gate, not just an exclusion list.

rc.7 itself must remain interpreted exactly under its existing complete-tracked-content method. The new model can only be prospective.

## Alternatives and trade-offs

### A — Preserve all-tracked-files release identity

**Advantages**

- simplest rule;
- maximal single-digest coverage of the repository tree;
- no new classification mechanism.

**Costs / failure mode**

- every material prompt, discovery record, project-state update, pilot record or repository-control change forces release-manifest/version packaging;
- makes Project Operating Contract evidence custody fight the release lifecycle;
- encourages moving governance evidence outside repository custody merely to avoid release churn;
- empirically blocked both PR #15 and PR #16 despite their local controls passing.

**Disposition:** reject as the long-term operating model.

### B — Scoped framework release payload

Define `content_sha256` over an explicitly classified release payload while exact Git commit binding continues to protect the complete repository revision.

**Advantages**

- directly solves the observed coupling;
- preserves exact immutable Git identity;
- allows repository-operation evidence to evolve without pretending the framework payload changed;
- can default unknown paths to release-included, keeping the model fail-closed.

**Risks**

- unsafe if exclusions are broad or implicit;
- unsafe if consumer-visible code reads/imports excluded files;
- requires new manifest/content-identity semantics and tests.

**Disposition:** necessary component, but insufficient without release/development lifecycle clarification and an independence gate.

### C — Immutable release refs separate from moving repository `main`

Treat an accepted/candidate exact commit/ref as the immutable release identity while allowing `main` to advance for repository-operation/evolution changes that do not alter the declared release payload.

**Advantages**

- stops equating `main` with a release artifact;
- preserves historical release commit immutably;
- fits ordinary repository evolution.

**Risks**

- alone does not solve current CI because the complete-tree content digest still changes;
- needs clear rules preventing a payload-changing `main` commit from masquerading as the previous release.

**Disposition:** necessary lifecycle complement to B, not a standalone solution.

### D — Separate custody repository/plane

Move discovery, pilots and operational evidence into a different repository.

**Advantages**

- release repository could remain release-only.

**Costs / failure mode**

- root `AGENTS.md`, project state, roadmap, PR templates and repository CI govern this repository and cannot be cleanly externalized;
- splits authority/currentness/custody across repositories;
- increases cross-repository failure modes merely to preserve an over-broad content digest.

**Disposition:** reject as primary architecture. External evidence repositories may remain useful for particular data classes but do not solve the root problem.

### E — Recommended hybrid: scoped payload + operational plane + immutable release anchor

Combine B and the bounded part of C:

- one Git repository;
- two explicitly governed content planes;
- exact Git commits continue to bind the whole tree;
- release manifests identify only release-payload bytes;
- immutable release/candidate commits remain historical anchors;
- `main` may advance through operational-only changes while the last release payload version/digest remains unchanged;
- any release-payload change requires a new release package/identity before it can be represented as a valid release.

**Disposition:** recommended.

## Recommended ownership and content-plane model

### Plane 1 — Framework Release Payload

This plane contains every byte whose change can alter consumer-visible semantics, machine contracts, reusable execution behavior, consumer conformance, capability behavior, compatibility or required release documentation/provenance.

Candidate classes include, subject to design confirmation:

- `RELEASE_VERSION`;
- `framework/**`;
- `contracts/**`;
- consumer-facing `tools/**`;
- release/consumer/architecture/upgrade documentation required by the manifest;
- release provenance needed to interpret or verify those surfaces;
- any test fixture or artifact explicitly declared part of the distributable/verifiable release payload.

Unknown tracked paths MUST default to release-payload inclusion unless an accepted content-plane policy explicitly classifies them otherwise.

### Plane 2 — GG Repository Operational / Evolution Plane

This plane contains project-local governance that operates the General Governance repository but is not itself framework payload semantics.

Candidate classes demonstrated by current evidence include:

- `governance/discovery/**`;
- `governance/pilots/**`;
- project-state / roadmap projections;
- root repository-agent instructions such as `AGENTS.md`;
- Project State Integrity configuration/checker/workflow/PR-template surfaces;
- other repository-only decision, learning, execution and coordination evidence that is not consumed as framework semantics.

The exact path policy must be designed deliberately. This discovery does **not** normatively declare that every future file under a broad prefix is safe to exclude.

### Deterministic safety model

The prospective content policy should use **default include / explicit exclusion**, not default exclusion.

A release build/check must construct an isolated temporary **release-payload projection** containing only release-included files and run consumer-facing conformance/WPDC/release checks against that projection. This provides a deterministic proof that operationally excluded files are not required to execute or validate the release payload.

Required properties:

1. unknown path -> release included by default;
2. excluded operational path -> still immutable under Git commit identity;
3. changing an included file -> changes payload digest and requires release packaging;
4. changing only an accepted excluded file -> leaves payload digest stable;
5. release-payload validation must succeed with excluded files physically absent from the projection;
6. a release payload reference/import/runtime dependency on an excluded file -> fail closed;
7. content-plane policy itself is release content and changing it requires a new release identity.

A PR-level deterministic `Release-Payload-Impact` projection may later classify whether a change touches the release plane, but semantic authority must not be inferred from that classification.

## Consumer and adopter compatibility impact

rc.7 consumers remain unchanged. Their existing locks continue to bind exact rc.7 commit/manifests under the old complete-tracked-content semantics.

The architecture change should be introduced only in a future release identity. A likely implementation requires a new release-manifest schema/content-identity method, but does **not necessarily require changing the consumer-lock tuple**: repository/version/commit/manifest digest can remain intact.

A future validator can derive the payload scope from the exact locked release manifest and reproduce the corresponding payload digest. `tools/validate_work_packet.py` may continue to delegate payload reproduction to `tools/validate_consumer.py`, preserving one identity implementation.

Adopters should not be forced to upgrade merely because General Governance records new project-operational evidence on `main`. They upgrade only when they intentionally adopt a new framework release identity.

Specifically, the SVP learning pilot can ultimately reference an exact GG operational artifact/commit as separately governed non-normative pilot evidence while SVP remains locked to its independently selected framework release, if the accepted cross-project package so defines. That reference does not itself upgrade the GG framework lock or transfer authority.

## Migration strategy

1. Preserve rc.7 and both blocked PRs unchanged as evidence.
2. Project Owner reviews this discovery. Acceptance creates only a design/implementation candidate, not rc.8 authority.
3. Under separate authority, design the exact release-payload policy, manifest version/method, isolated-payload validation and repository lifecycle wording.
4. Resolve the independent rc.7 Owner-disposition gate before any release packaging that claims a successor identity.
5. Implement the architecture prospectively in a new framework release candidate; do not rewrite rc.7's digest semantics.
6. Required regression suite must prove at least:
   - exact rc.7 remains valid under its historical method;
   - an operational-only fixture leaves the new payload digest unchanged;
   - a release-payload byte change changes the digest;
   - an unknown new path is included/fails closed by default;
   - an excluded file required by consumer-visible validation causes isolated-payload conformance failure;
   - exact commit and manifest locking remain enforced;
   - WPDC adopter validation retains its fail-closed identity boundary.
7. Only after the new architecture is integrated may successor candidates for Project State Integrity and the learning pilot be prepared from the new current baseline.
8. Existing adopters remain on their exact historical GG locks until separately upgraded.

## Disposition of PR #15 and PR #16

### PR #15

Keep the existing head `b5ea02b74a04457ddffbe03caa81818903484a83` frozen as empirical evidence. Do not merge it by weakening rc.7 checks and do not mutate it into the release-identity correction.

It also contains an independent review finding concerning PR merge-base calculation, so any later Project State Integrity adoption should be a successor candidate from the then-current baseline and must incorporate/review that finding separately.

### PR #16

Keep exact head `d3e1f0d96e23698e740511e7cd8d21d542e17741` frozen as the validated-but-integration-blocked pilot candidate. Do not rerun the failed CI as if it were transient and do not regenerate rc.7's manifest around the five pilot files.

After an accepted release-identity solution exists, create a successor adopter-pilot integration candidate from the new baseline. The five-file package may be used as bounded design/input evidence, but its new candidate must receive fresh currentness and validation; the old head does not acquire merge authority retroactively.

## Required prospective normative and tooling surfaces

If this discovery is accepted, a separately authorized design/implementation phase should evaluate the minimum coherent change set including:

- `docs/consumer-contract.md` — redefine complete repository content vs framework release payload identity and clarify `main` vs immutable release anchors;
- `release-manifest.json` contract/schema/version — declare the content-identity method/policy prospectively;
- `tools/validate_consumer.py` — reproduce the declared scoped payload identity fail-closed;
- `tools/validate_work_packet.py` — continue exact lock/manifest/payload enforcement under the new method;
- release/consumer/WPDC regression tests;
- `.github/workflows/conformance-ci.yml` — validate an isolated release-payload projection and repository operational controls separately;
- release packaging/provenance surfaces needed for the next release identity.

The Project Operating Contract does not obviously require semantic weakening. Its repository-custody requirements are evidence supporting this separation. A future design may add a narrow clarification identifying release payload vs repository operational custody, but should not relax prompt/run/learning immutability or authority boundaries.

## Non-goals and stop conditions

This discovery does not:

- reinterpret or modify rc.7;
- authorize rc.8;
- authorize changes to release-manifest, validators, schemas or POC;
- authorize merging/correcting/retrying PR #15 or PR #16;
- authorize moving evidence out of repository custody;
- classify every `governance/**`, `.github/**`, `scripts/**` or root file as operational by default;
- allow excluded operational files to influence release payload behavior silently;
- remove exact Git commit binding from consumer locks;
- change any adopter lock or mutate SVP/Dopis;
- make `main` a floating consumer identity.

STOP if a future design requires weakening exact commit locking, silently changing historical rc.7 semantics, default-excluding unknown files, or allowing release behavior to depend on bytes outside the declared payload projection.

## Final disposition

`RELEASE_IDENTITY_ARCHITECTURE_CHANGE_CANDIDATE`

The evidence is sufficient to reject the current all-tracked-files digest as the sustainable repository operating model. The recommended direction is a prospective two-plane architecture in the same repository: exact Git commit identity continues to protect the full repository revision, while the release manifest hashes an explicitly governed, fail-closed framework release payload. Immutable release/candidate commits remain historical anchors; operational-only `main` evolution may occur without a framework payload/version change once the new architecture is separately designed, implemented, validated, accepted and released.
