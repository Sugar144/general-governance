---
proposal_id: GG-IMPLEMENTATION-PROPOSAL-RELEASE-PAYLOAD-OPERATIONAL-PLANE-001
run_id: GG-IMPLEMENTATION-PROPOSAL-RELEASE-PAYLOAD-OPERATIONAL-PLANE-001-RUN-001
status: EXECUTED_PENDING_VALIDATION
disposition: IMPLEMENTATION_PACKAGE_READY_FOR_OWNER_AUTHORIZATION
baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
input_sha256: 0f3ff2a6f6e29f4006d6efe4f3a9adf512d7b3aca904b988162d75c0a9d3e74e
---

# Scoped release payload identity — implementation proposal

## Current state and currentness

The exact implementation-proposal baseline is General Governance `main` at `22a1d5e2f759fda53574884e1056a3a56baa211a`, framework `0.1.0-rc.7`. `release-manifest.json` is schema `1.3.0`, blob `2f400cb80a10bea2c5c69bc37017f393e72c7555`, and declares the legacy all-tracked-files content digest `14fceee7fb261fee6c2b515cbd81e39c91daaaaa3aa8dc431d3c1beac754d15e`.

The accepted architecture is bound by validated HEAD `b6db69bd23b0a8c085c23dd4a6eef38fd205ac54`, design blob `e82dca5ccf3d907b41105b13ec59565fb4f24aee`, validation blob `7fdfb9dbf68e272a0f6bbec9926e3cd29b8d6cd0`, and Owner acceptance comment `5381200259`.

No implementation byte may be represented as rc.7. Any branch containing release-included implementation changes is necessarily non-integrable until separately authorized successor release packaging supplies a coherent new manifest/version identity.

## Exact implementation write surface

The smallest coherent **implementation-stage** write surface is exactly:

1. **ADD** `tools/release_payload.py`
   - canonical identity-method dispatch;
   - fail-closed path classification;
   - scoped/legacy digest calculation;
   - isolated projection construction and verification;
   - no authority semantics.
2. **ADD** `contracts/release-manifest.schema.json`
   - machine contract for recognized legacy `1.3.0` and prospective scoped `1.4.0` manifest shapes;
   - scoped `content_identity` structure constrained fail-closed.
3. **MODIFY** `tools/validate_consumer.py`
   - import/use canonical release-payload implementation;
   - retain `release_content_digest(framework)` as a compatibility wrapper so existing internal callers do not need an API change;
   - retain production exact Git HEAD and exact manifest-hash gates.
4. **MODIFY** `.github/workflows/conformance-ci.yml`
   - add release-payload unit checks;
   - add explicit Gate A full-checkout identity checks;
   - add Gate B isolated-payload self-sufficiency checks;
   - fetch sufficient Git history for the exact rc.7 historical regression fixture.
5. **ADD** `tests/test_release_payload_identity.py`
   - classification, policy, digest, historical dispatch, exact-lock and WPDC-consumer integration regressions.
6. **ADD** `tests/test_release_payload_projection.py`
   - deterministic projection integrity and self-sufficiency regressions with operational files and `.git` physically absent.
7. **MODIFY** `docs/consumer-contract.md`
   - distinguish exact repository revision identity from scoped framework payload identity;
   - document historical method dispatch and non-floating `main` semantics.
8. **ADD** `docs/architecture/release-payload-identity.md`
   - normative-interpretation documentation for the two-plane release identity mechanism, classification algorithm, Gate A/Gate B, and release-anchor lifecycle.

The implementation stage must **not** modify:

- `release-manifest.json` or `RELEASE_VERSION` — these belong to the separately authorized successor release-packaging effect;
- `tools/validate_work_packet.py` — its current import of `release_content_digest` can remain valid if the compatibility wrapper is preserved;
- `tests/test_work_packet_contract.py` — new integration coverage belongs in `tests/test_release_payload_identity.py` unless implementation proves an existing WPDC fixture itself must change;
- consumer-lock/configuration schemas — no adopter-owned field is currently required;
- `framework/core/project-operating-contract.md` — no semantic contradiction has been demonstrated;
- `provenance/evolution-manifest.json` — current `verify_evolution.py` covers extracted framework surfaces only, and none of the eight implementation-stage paths are extraction-manifest destinations.

Any need to widen this exact implementation surface is a STOP and requires explicit Owner disposition before the extra mutation.

## Shared release identity API and ownership

`tools/release_payload.py` becomes the single implementation owner for release-content identity. Proposed public/internal API:

- `load_release_manifest(root: Path) -> dict`
- `validate_release_manifest(manifest: dict) -> None`
- `identity_method(manifest: dict) -> str`
- `tracked_paths(root: Path) -> tuple[str, ...]`
- `classify_path(path: str, manifest: dict) -> str`
- `classify_tracked_paths(paths, manifest) -> Classification`
- `content_digest(root: Path, manifest: dict) -> str`
- `release_content_digest(root: Path) -> str`
- `build_projection(source: Path, destination: Path) -> ProjectionIndex`
- `verify_projection(projection: Path, index: ProjectionIndex) -> None`

The classifier hard-codes method-v1 protected release surfaces and rejects unsupported exclusion semantics. `validate_consumer.py` re-exports or wraps `release_content_digest` under its current name. This preserves `tools/validate_work_packet.py::verify_locked_framework_identity` without changing WPDC code.

The helper may expose a small CLI (`digest`, `project`, `verify-projection`) for CI. The CLI is deterministic tooling only and must not infer authority or release status.

## Manifest and schema migration

Implementation prepares support for two explicit manifest families:

- legacy `1.3.0`: current rc.7 shape and `LEGACY_COMPLETE_TRACKED_FILES_V1` behavior;
- scoped `1.4.0`: structured `content_identity` with method `SCOPED_TRACKED_FILES_V1`.

The new schema should use strict `oneOf` branches or equivalent closed shapes. For scoped `1.4.0`, require:

- `content_identity.method = SCOPED_TRACKED_FILES_V1`;
- `default_classification = RELEASE_INCLUDED`;
- `manifest_self_excluded = true`;
- `reserved_operational_prefixes = ["governance/"]` exactly for method v1;
- `operational_exact_paths` restricted to the accepted exact operational-path allow-list;
- unique, normalized repository-relative paths;
- no arbitrary glob, regex, negation, last-rule-wins, or additional exclusion language.

Protected release classes remain code invariants and cannot be weakened by manifest data.

The implementation stage adds parser/schema support but does not change the live rc.7 manifest. Successor packaging later writes the first actual `1.4.0` manifest.

## Historical rc.7 dispatch

`release_content_digest(root)` dispatches from the exact manifest:

- `1.3.0` / legacy shape -> hash every tracked path except `release-manifest.json`, exactly reproducing rc.7 semantics;
- `1.4.0` + `SCOPED_TRACKED_FILES_V1` -> classify tracked paths and hash only `RELEASE_INCLUDED` paths;
- any unknown/malformed method/schema combination -> fail closed.

The regression suite must obtain the exact rc.7 commit `22a1d5e2f759fda53574884e1056a3a56baa211a` from Git history or a cryptographically bound fixture and prove both its manifest hash and legacy content digest remain exact. CI should use `actions/checkout` with enough history (`fetch-depth: 0` is the simplest bounded choice) so the regression cannot silently validate the implementation branch as though it were rc.7.

No historical manifest, tag, lock, or digest is rewritten.

## Isolated release-payload projection

`build_projection` operates only after manifest-policy validation. It:

1. enumerates source tracked paths;
2. classifies every path;
3. creates a fresh empty destination;
4. copies exact bytes for every `RELEASE_INCLUDED` path plus `release-manifest.json`;
5. does not copy `.git` or any `OPERATIONAL_EXCLUDED` path;
6. emits a temporary `projection-index.json` containing source commit (when available), manifest SHA-256, included path/hash records, and excluded path list;
7. verifies the projection contains every included path, no excluded path, and no undeclared extra path other than the temporary index;
8. recomputes the scoped digest from projection bytes without requiring Git.

The projection API must not contain a production `skip_git_check`, `ignore_commit`, or equivalent switch. Production consumer validation remains exact-checkout-bound. Projection validation is a separate API with a different contract rather than a bypass flag.

## Gate A and Gate B CI changes

**Gate A — full checkout identity** runs on the exact candidate checkout and must:

- validate all JSON schemas, including `release-manifest.schema.json`;
- compile/import release-facing Python tooling;
- run evolution verification;
- validate exact manifest/current content identity;
- run existing consumer, WPDC and capability regressions;
- run `tests/test_release_payload_identity.py`;
- reproduce the exact historical rc.7 identity from the bound historical commit/fixture;
- fail if a release-included byte changes without coherent successor packaging.

**Gate B — isolated payload self-sufficiency** must first build a fresh projection, then run only projection-safe release-facing checks from that directory, including:

- manifest/schema validation;
- Python compile/import checks for `tools/**` and reusable framework code;
- `verify_evolution.py`;
- `tests/test_release_payload_projection.py`;
- WPDC/capability deterministic tests that are demonstrably projection-safe;
- payload/index integrity verification.

Existing tests that logically require a Git repository remain Gate A tests; they must not be made to pass Gate B by weakening production exact-commit validation. If a release-facing module cannot even import or execute its non-Git logic without an excluded operational file, Gate B fails.

Gate B runs unconditionally for scoped-payload candidates and later operational-only PRs. An operational-only diff classification never skips release conformance.

## Regression and counterexample matrix

Implementation authorization must require, at minimum:

- exact rc.7 checkout -> legacy digest PASS;
- rc.7 plus tracked extra file -> legacy digest mismatch;
- scoped manifest + new `governance/discovery/**` file -> payload digest unchanged;
- scoped manifest + changed `framework/**` or `tools/**` -> old payload digest fails;
- new unknown root path -> `RELEASE_INCLUDED` and old payload digest fails;
- policy tries to exclude protected release path -> policy validation fails;
- arbitrary glob/regex/prefix exclusion -> schema/policy validation fails;
- excluded file required by included code/test -> Gate B fails;
- projection contains excluded file -> fails;
- projection omits included file -> fails;
- policy bytes change -> manifest hash changes;
- exact commit differs while payload/manifest match -> only the commit explicitly named by a consumer lock is accepted;
- floating `main`/branch identity -> rejected;
- current consumer-lock schema `2.0.0` remains accepted for the successor when compatibility declaration remains unchanged;
- `tools/validate_work_packet.py` succeeds against a correctly bound scoped release without source modification;
- malformed/unknown content-identity method -> fail closed.

## Consumer-lock compatibility decision

Proposal disposition: **consumer-lock schema `2.0.0` remains sufficient and should not change in the implementation package.**

Reason: the adopter still selects exactly `(repository, version, commit_sha, release_manifest_sha256)`. The exact manifest hash now binds the content-identity method and exclusion policy; the exact commit still binds every repository byte. No new adopter-owned value or authority obligation is introduced.

This remains an empirical gate. If implementation can only make the scoped method work by adding a consumer-owned lock/configuration field or weakening the exact-commit check, STOP with `COMPATIBILITY_REVIEW_REQUIRED`; do not silently change schemas or compatibility declarations.

## Documentation and provenance effects

Required implementation documentation is limited to `docs/consumer-contract.md` plus new `docs/architecture/release-payload-identity.md`.

No POC correction is required by the current design: POC repository custody is an input justification for the operational plane, not a contradiction.

No implementation-stage change to `provenance/evolution-manifest.json` is required under the current verifier because its entries are limited to extraction-manifest destination paths, while this proposal modifies no extracted framework surface. If implementation discovers a provenance contract not represented by current `verify_evolution.py` that requires a provenance mutation, STOP and request write-surface expansion rather than mutating it implicitly.

Successor packaging must update `release-manifest.json.required_framework_surfaces` to include the new release-manifest schema, release-payload helper, and required architecture documentation as appropriate.

## Implementation sequencing and bootstrap

The safe sequence is deliberately two-effect:

### I1 — implementation candidate, non-integrable

Under separate implementation authority, branch from the then-current exact `main` and apply only the eight implementation-stage paths above. Run unit/static/fixture validations that do not claim the branch is a valid rc.7 release.

Terminal state must be `IMPLEMENTED_PENDING_SUCCESSOR_RELEASE_PACKAGING`, not merge-ready. No PR to `main` is required before packaging; if a PR is opened for review it must be draft and explicitly non-mergeable because the current rc.7 manifest cannot reproduce release-included changes.

### P1 — successor release packaging, separately authorized

Only after I1 is validated and independently reviewed does the Owner authorize successor release packaging. P1 resolves the successor version, updates `RELEASE_VERSION` and `release-manifest.json` to schema `1.4.0` / `SCOPED_TRACKED_FILES_V1`, recalculates the new payload digest, adds the version-specific upgrade/release documentation required by the packaging process, and runs full Gate A + Gate B.

The first candidate eligible for a normal integration PR is the **packaged successor candidate**, never the un-packaged implementation branch.

This sequence preserves effect separation without pretending intermediate release-included bytes are rc.7.

## Successor release packaging boundary

Packaging is not authorized by this proposal. Its future minimum effects are expected to include:

- resolve the exact successor framework version under Owner authority;
- modify `RELEASE_VERSION`;
- replace `release-manifest.json` with a coherent schema-1.4.0 scoped manifest and new payload digest;
- update `required_framework_surfaces` for new release assets;
- add/update version-specific upgrade/release documentation required by existing packaging conventions;
- run complete release packaging, exact digest reproduction, Gate A, Gate B, independent review and currentness fences;
- only then request PR/merge authority.

No proposal statement authorizes the name `rc.8`; the successor version is a later explicit packaging decision.

## Frozen PR #15 and PR #16 successor strategy

PR #15 (`b5ea02b74a04457ddffbe03caa81818903484a83`) and PR #16 (`d3e1f0d96e23698e740511e7cd8d21d542e17741`) remain frozen empirical evidence. Do not rebase, retry, amend, or merge them in place.

After the scoped release identity is integrated:

- prepare a fresh Project State Integrity successor candidate from then-current `main`, incorporating the independent review finding already associated with PR #15;
- prepare a fresh learning-pilot successor candidate from then-current `main`, using PR #16's five-file package only as bounded input evidence and re-running currentness/validation;
- close/supersede the old PRs only under their appropriate bookkeeping authority after successor identities exist.

## SVP learning pilot resume path

The fastest safe resume path after the scoped identity release is integrated is:

1. create a fresh GG operational learning-pilot successor on current `main`;
2. materialize only `governance/**` pilot evidence/binding under the accepted scoped operational policy;
3. run Gate A and Gate B even though the diff is operational-only;
4. integrate that exact operational candidate under separate authority;
5. let SVP reference the exact GG operational artifact commit separately from its framework lock;
6. materialize the already-designed SVP adopter projection under its own SVP authority;
7. verify/rebind the exact local C2 baseline and all other independent pre-run dependencies;
8. only then seek separate prospective authority for the future empirical C2 RUN-001.

The operational evidence reference does not upgrade SVP's framework lock and transfers no authority.

## Validation and review plan

Future implementation I1 requires:

- exact baseline/currentness preflight;
- deterministic unit/static validation of all new identity/policy/projection behavior;
- regression coverage for every counterexample above;
- evidence that `validate_work_packet.py` remains source-unchanged and compatible;
- explicit consumer-lock `2.0.0` compatibility result;
- explicit provenance sufficiency result;
- independent semantic/security review focused on fail-closed classification and exact-commit preservation;
- terminal Owner review before packaging authority.

Future packaging P1 additionally requires:

- exact implementation-candidate binding;
- successor version/manifest/content digest reproduction;
- full Gate A and Gate B green;
- branch protection required check green;
- exact-candidate review with no unresolved material thread;
- separate PR/merge/release/publication authority as applicable.

## Rollback and stop conditions

STOP rather than widening or weakening if:

- `main` drifts before a future authority is bound;
- implementation requires editing a path outside the eight-file implementation surface;
- `validate_work_packet.py` must change despite compatibility-wrapper design;
- consumer-lock/configuration schema must change;
- exact Git commit enforcement must be bypassed for projection tests;
- unknown paths can become excluded by default;
- manifest data can exclude a protected release class;
- Gate B reveals a hidden dependency on operational files;
- legacy rc.7 exact digest cannot be reproduced;
- implementation needs to rewrite historical rc.7 bytes or semantics;
- provenance requirements demand an unapproved mutation;
- a partial implementation is proposed for merge before coherent successor packaging;
- PR #15/#16 mutation is proposed as a shortcut;
- SVP or another adopter is mutated from GG implementation authority.

Rollback for I1 is abandonment of the isolated branch; no `main` state is changed. Packaging failure leaves I1 non-integrated and creates no merge/retry/release authority.

## Final disposition

`IMPLEMENTATION_PACKAGE_READY_FOR_OWNER_AUTHORIZATION`

The accepted architecture can be implemented with an eight-path implementation-stage surface while leaving WPDC source, consumer-lock schemas, POC and provenance unchanged. The implementation must remain non-integrable until a separately authorized successor release package supplies the first schema-1.4.0 `SCOPED_TRACKED_FILES_V1` manifest and coherent version/content identity. This separation is the minimum approach that preserves rc.7 immutably, maintains exact consumer commit binding, proves operational exclusions through isolated validation, and unblocks later operational evidence such as Project State Integrity and the SVP learning lifecycle without forcing a new framework release for each such record.
