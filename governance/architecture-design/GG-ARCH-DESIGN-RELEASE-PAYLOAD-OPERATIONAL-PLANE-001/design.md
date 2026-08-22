---
design_id: GG-ARCH-DESIGN-RELEASE-PAYLOAD-OPERATIONAL-PLANE-001
run_id: GG-ARCH-DESIGN-RELEASE-PAYLOAD-OPERATIONAL-PLANE-001-RUN-001
status: EXECUTED_PENDING_VALIDATION
disposition: ARCHITECTURE_READY_FOR_IMPLEMENTATION_PROPOSAL
baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
input_sha256: 4d847d44e76ab73ec853b76466e59625d991a0303c82e80d3c95f7a7315e55f2
---

# Scoped release payload and GG operational plane — architecture design

## Design decision

Adopt prospectively a **single-repository, two-content-plane architecture**.

General Governance keeps one Git repository and one exact Git commit identity per selected revision, while distinguishing:

1. the **Framework Release Payload**, whose bytes are distributed/validated as reusable General Governance behavior; and
2. the **GG Operational / Evolution Plane**, whose bytes govern and evidence the General Governance project itself but must not influence consumer-visible framework behavior.

The exact Git `commit_sha` continues to bind the complete tree. The exact `release_manifest_sha256` continues to bind the release declaration. Prospectively, `content_sha256` identifies only the Framework Release Payload under an explicit fail-closed classification declared by the release manifest.

The new identity method is prospective only. rc.7 remains permanently interpreted under its historical complete-tracked-content method.

This design does not make `main` a consumer reference. Consumers still bind an exact immutable commit SHA and exact manifest hash.

## Content-plane taxonomy and ownership

### RELEASE_INCLUDED

A tracked path is `RELEASE_INCLUDED` when its bytes can alter consumer-visible semantics, machine contracts, reusable execution behavior, compatibility, adopter conformance, optional capability behavior, release verification semantics, or documentation/provenance required to interpret the release.

For the first scoped-payload release, these classes are protected and cannot be excluded by policy:

- `RELEASE_VERSION`;
- `release-manifest.json` as the independently hash-bound release declaration, although it remains outside `content_sha256` to avoid self-reference;
- `framework/**`;
- `contracts/**`;
- `tools/**`;
- `tests/**`;
- `docs/**`;
- `provenance/**`;
- `.github/workflows/conformance-ci.yml`;
- `README.md`.

A future design may narrow additional release-only paths, but not through an operational commit. Changing protected classes or exclusion semantics is itself release-payload architecture change and requires a new release identity.

### OPERATIONAL_EXCLUDED

A tracked path may be `OPERATIONAL_EXCLUDED` only when it is repository-local governance/evidence and release behavior remains valid with that path physically absent.

The initial candidate exclusion policy is intentionally narrow:

- reserved prefix `governance/**` — formal runs, decisions, discovery, design, implementation/process evidence, release-process evidence, pilots and learning custody;
- exact path `.gitignore`;
- exact path `AGENTS.md`;
- exact path `PROJECT_STATE.yaml`;
- exact path `ROADMAP.md`;
- exact path `project-state-integrity.json`;
- exact path `scripts/project_state_integrity.py`;
- exact path `.github/pull_request_template.md`;
- exact path `.github/workflows/project-state-integrity.yml`.

`governance/**` becomes a reserved GG-project namespace: consumer-visible reusable behavior must not be implemented there. If reusable behavior is needed, it must live in a release-included surface such as `framework/**`, `contracts/**`, `tools/**`, `docs/**`, or another release-included path.

The root and `.github` exact exclusions above are repository controls whose locations are constrained by GitHub/agent/project-state integration. They are exceptions, not precedent for broad root exclusions.

### UNKNOWN

There is no persistent `UNKNOWN` class. Any tracked path not matched by an accepted operational exclusion is classified `RELEASE_INCLUDED`.

This is the central fail-closed rule:

`unknown tracked path -> RELEASE_INCLUDED`

## Fail-closed classification algorithm

For a prospective scoped-payload manifest:

1. enumerate tracked paths from the exact checkout with `git ls-files -z`;
2. normalize each path as repository-relative POSIX text;
3. reject duplicate, absolute, traversal, empty, or non-normalized policy entries;
4. validate the manifest exclusion policy before classifying files;
5. classify `release-manifest.json` as `MANIFEST_SELF_EXCLUDED` only for `content_sha256`; it is never operational;
6. reject any operational rule that matches a protected release path/class;
7. for each remaining tracked path:
   - if it matches an accepted exact operational exclusion, classify `OPERATIONAL_EXCLUDED`;
   - else if it is below the reserved `governance/` prefix, classify `OPERATIONAL_EXCLUDED`;
   - otherwise classify `RELEASE_INCLUDED`;
8. unknown/new paths therefore enter the release payload automatically;
9. no glob, regular-expression, negation, last-rule-wins, or user-defined arbitrary prefix semantics are allowed in v1;
10. an exclusion-policy change changes the manifest bytes and therefore the immutable release identity; it cannot be introduced as an operational-only commit.

The implementation must hard-code the protected release classes for method v1 in the release-identity validator as well as validate the manifest declaration. A malicious or mistaken manifest cannot exclude `framework/**`, `contracts/**`, `tools/**`, `tests/**`, `docs/**`, `provenance/**`, `RELEASE_VERSION`, `README.md`, or the release conformance workflow under method v1.

## Manifest and policy representation

The first scoped-payload release should bump the release manifest schema prospectively from `1.3.0` to `1.4.0` and add one explicit object. Proposed shape:

```json
{
  "manifest_schema_version": "1.4.0",
  "repository": "Sugar144/general-governance",
  "framework_version": "<NEXT_RELEASE_VERSION>",
  "release_status": "IMMUTABLE_RELEASE_CANDIDATE_PENDING_OWNER_DISPOSITION",
  "content_sha256": "<64 hex>",
  "content_identity": {
    "method": "SCOPED_TRACKED_FILES_V1",
    "default_classification": "RELEASE_INCLUDED",
    "manifest_self_excluded": true,
    "reserved_operational_prefixes": [
      "governance/"
    ],
    "operational_exact_paths": [
      ".gitignore",
      "AGENTS.md",
      "PROJECT_STATE.yaml",
      "ROADMAP.md",
      "project-state-integrity.json",
      "scripts/project_state_integrity.py",
      ".github/pull_request_template.md",
      ".github/workflows/project-state-integrity.yml"
    ]
  }
}
```

The actual manifest retains its existing compatibility/capability/provenance fields; the snippet shows only the identity addition.

A prospective `contracts/release-manifest.schema.json` SHOULD be introduced so schema `1.4.0` is machine-validated. The schema must require the exact method token, `RELEASE_INCLUDED` default, `manifest_self_excluded=true`, unique normalized exclusion entries, and no unsupported keys.

The v1 protected release paths/classes are validator invariants, not mutable manifest data. This avoids allowing a manifest author to weaken the protected set merely by editing the manifest.

No separate policy file is required in v1. Embedding the small policy in `release-manifest.json` is safer and simpler because the consumer lock already binds the exact manifest SHA-256. Any policy change therefore creates a different immutable release declaration.

## Release-payload digest algorithm

For `SCOPED_TRACKED_FILES_V1`:

1. resolve tracked files from the exact Git checkout;
2. validate manifest/schema and content-plane policy;
3. classify every tracked path using the algorithm above;
4. omit only:
   - `release-manifest.json` from the content digest to avoid self-reference;
   - paths classified `OPERATIONAL_EXCLUDED`;
5. for every `RELEASE_INCLUDED` path calculate SHA-256 of exact file bytes;
6. create lexicographically ordered records exactly as today:

   `<path>\0<SHA-256(file bytes)>\n`

7. SHA-256 the concatenated UTF-8 record stream;
8. compare the result to manifest `content_sha256`.

Keeping the existing record encoding minimizes change and keeps the architectural correction limited to path selection.

File-mode/symlink identity remains protected by the exact Git commit. Changing digest record encoding or adding Git mode identity is outside this correction unless implementation evidence proves it necessary.

## Isolated projection and validation contract

A scoped digest is insufficient on its own. Every candidate using `SCOPED_TRACKED_FILES_V1` must prove that operationally excluded files are not hidden dependencies of the release payload.

### Projection construction

A deterministic helper should:

1. receive the exact source checkout and validated release manifest;
2. obtain the complete tracked path set;
3. classify all paths;
4. create a fresh temporary directory;
5. copy only:
   - every `RELEASE_INCLUDED` path;
   - `release-manifest.json`;
6. preserve exact file bytes and relative paths;
7. create a temporary, non-release `projection-index.json` containing source commit, manifest SHA-256, included path list/hashes and excluded path list solely for CI verification;
8. verify no excluded path exists in the projection;
9. never copy `.git` or operational evidence into the projection.

### Two required validation gates

**Gate A — Full checkout identity**

Runs against the exact Git checkout and proves:

- exact HEAD equals the selected consumer/release commit where applicable;
- exact release manifest hash;
- historical/scoped content digest reproduction;
- compatibility/capability declarations;
- content-plane policy validity.

**Gate B — Isolated payload self-sufficiency**

Runs with the projection as working root and operational files physically absent. It must execute all release-facing checks that do not logically require Git-history identity, including at minimum:

- release-manifest schema validation;
- all contract schema validation;
- Python syntax/import checks for release tools and reusable L6 code;
- evolution/provenance verification that is declared part of the payload;
- WPDC deterministic regression suite;
- consumer-conformance regression suite in a projection-safe harness;
- capability-composition regression suite;
- release-payload digest/projection-index verification.

The implementation may refactor shared release-identity functions so projection tests can run without a Git repository, but the production consumer validator must retain the exact Git-head gate when validating a real locked checkout. A test-only or hidden bypass of exact commit checking is forbidden.

If an included tool imports, opens, shells to, or otherwise requires an excluded operational file during isolated validation, Gate B fails closed. The correct response is either to remove that dependency or reclassify the required file as release included through a new release identity.

CI must run Gate B unconditionally for scoped-payload release candidates and for subsequent operational-only PRs. Operational-only classification must never be used to skip release conformance.

## Historical rc.7 compatibility

Historical manifests remain interpreted by their historical method.

Validator dispatch must be explicit:

- manifest schema/method through rc.7 (`1.3.0`, complete tracked content): reproduce the existing algorithm exactly — every tracked path except `release-manifest.json` contributes to `content_sha256`;
- schema `1.4.0` with `SCOPED_TRACKED_FILES_V1`: use the new classification and scoped digest.

No rc.7 bytes, manifest fields, digest, tag/ref or consumer lock may be rewritten.

Regression fixtures must preserve the exact rc.7 manifest SHA/content digest and prove that future tooling still validates an exact historical rc.7 checkout under the legacy method.

## Consumer-lock compatibility decision

**Decision: keep consumer-lock schema `2.0.0` and its identity tuple unchanged.**

The tuple remains:

`(repository, version, commit_sha, release_manifest_sha256)`

The lock does not need to duplicate the content-plane policy. The exact manifest hash already binds the policy and identity method; the exact commit still binds every repository byte.

The existing compatibility tuple may remain at framework contract `2.0.0`, consumer-lock schema `2.0.0`, and consumer-configuration schema `1.0.0` if implementation confirms no adopter-owned field or semantic obligation changes. The new release identity method is a framework validation implementation detail carried by the exact release manifest and validator.

If implementation discovers an adopter-visible obligation that cannot be represented by the existing lock/configuration contracts, it must STOP and reopen this compatibility decision rather than silently bump compatibility.

## Main and release-anchor lifecycle

`main` is a moving project branch and is never a valid floating consumer selector.

A release candidate or published release is anchored by an exact commit plus its exact manifest. After the first scoped-payload release identity exists, later commits may change only `OPERATIONAL_EXCLUDED` bytes while retaining the same framework version, manifest and `content_sha256`.

Such commits are **payload-equivalent repository revisions**, not new framework releases. They remain distinguishable because their exact Git commit SHAs differ.

A consumer may only use a specific exact SHA that reproduces the exact manifest/payload identity selected in its lock. A branch name such as `main`, `latest`, or `current` remains invalid.

Canonical release publication may continue to point to a chosen exact release anchor commit. Later payload-equivalent operational commits do not retroactively become the published release anchor merely because they contain the same payload.

Any change to a `RELEASE_INCLUDED` byte causes the scoped digest to differ from the current manifest and must fail conformance until a separately governed successor release package updates version/manifest/content identity. No operational commit may regenerate the manifest merely to absorb release-payload drift.

## Prospective implementation write surface

A future implementation proposal should be bounded initially to the minimum coherent release-identity change set:

- `release-manifest.json` — prospective schema/method/policy for the successor release candidate;
- `RELEASE_VERSION` — only as part of separately authorized successor release packaging;
- `contracts/release-manifest.schema.json` — new manifest schema validation;
- `tools/validate_consumer.py` — historical/scoped identity dispatch using one canonical payload classifier/digest implementation;
- `tools/validate_work_packet.py` — preserve exact lock boundary while consuming the shared identity implementation;
- `tools/release_payload.py` — candidate shared deterministic classifier/digest/projection helper;
- `.github/workflows/conformance-ci.yml` — add full-checkout and isolated-payload gates;
- release/consumer/WPDC/capability regression tests under `tests/**`;
- `docs/consumer-contract.md` — explain repository revision vs release payload identity and moving `main`;
- release/architecture documentation required to make the new identity method interpretable;
- `provenance/evolution-manifest.json` or other existing release provenance only if the accepted implementation changes a surface whose provenance contract requires it;
- operational custody under `governance/**` for the accepted design/implementation/package evidence.

The future implementation package must derive its exact write set after inspecting current main and provenance requirements. This list is an architectural maximum candidate set, not mutation authority.

The Project Operating Contract is not a required semantic change for this architecture. Its evidence-custody obligations support the separation. A narrow wording correction may be proposed only if implementation finds an actual contradiction.

## Regression matrix and counterexamples

A successor implementation is not ready unless it demonstrates at least these cases:

| Case | Expected result |
| --- | --- |
| Exact historical rc.7 checkout + rc.7 lock | PASS using legacy all-tracked method |
| rc.7 checkout plus one extra tracked file | FAIL under legacy method |
| Scoped release with unchanged payload + new `governance/discovery/**` record | scoped payload digest unchanged; full Git SHA changes; PASS |
| Scoped release with changed `framework/**` byte | payload digest changes; old manifest FAIL |
| Scoped release with changed `tools/**` byte | payload digest changes; old manifest FAIL |
| New unknown root file | included by default; old manifest FAIL |
| Manifest tries to exclude `framework/**` | FAIL policy validation |
| Manifest tries to exclude `tools/**` | FAIL policy validation |
| New file under reserved `governance/**` | operationally excluded; isolated gate still required |
| Excluded file imported/read by included validator | isolated payload gate FAIL |
| Change only `PROJECT_STATE.yaml` | payload digest unchanged; repository state CI runs; release conformance still runs |
| Change `.github/workflows/conformance-ci.yml` | release payload changes; successor release required |
| Change `.github/workflows/project-state-integrity.yml` only | payload digest unchanged under explicit exact exclusion |
| Consumer lock uses `main`/floating ref | invalid; exact SHA still required |
| Exact commit differs but payload/manifest are identical | valid only when lock names that exact commit; semantically payload-equivalent, not canonical publication anchor |
| Policy exclusion list changes | manifest hash changes; not operational-only |
| Projection contains an excluded path | FAIL projection integrity |
| Projection omits an included path | FAIL projection-index/content verification |

## Migration and release packaging strategy

1. Keep rc.7 and all current blocked branches immutable.
2. Accept/reject this design under a separate Owner gate.
3. If accepted, open a separately authorized implementation proposal; do not merge this design branch into rc.7 because rc.7 correctly rejects added tracked content.
4. Build the implementation from exact then-current `main`, consuming this validated design by exact commit/blob as evidence.
5. Implement historical method dispatch, scoped classification, manifest/schema support, projection tooling, tests and CI.
6. Validate the implementation with synthetic operational-only and release-payload-changing fixtures before packaging.
7. Package the first successor framework release identity under separate release authority. The release version is intentionally not selected by this design; `0.1.0-rc.8` is a possible future Owner choice, not an authorization or fact.
8. The successor release manifest is the first manifest allowed to declare `SCOPED_TRACKED_FILES_V1`.
9. Existing adopters remain on their exact historical locks until separately upgraded. No automatic upgrade occurs.
10. After the new identity architecture is integrated and its release gate is resolved, create successor candidates for Project State Integrity and the learning pilot from the new baseline.

Bootstrap rule: the accepted architecture/design evidence may remain on its exact design branch until the successor implementation/package can include the `governance/**` custody records under the new scoped method. This is not evidence loss: the design commit/blob is immutable and referenceable. It avoids corrupting rc.7 merely to merge process evidence.

## Frozen PR #15 and PR #16 successor strategy

### PR #15 — Project State Integrity

Keep `b5ea02b74a04457ddffbe03caa81818903484a83` frozen as evidence. Do not rebase or mutate it.

After the scoped-payload architecture is integrated, create a fresh successor from current main. Re-evaluate its seven-file design and independently address the existing review finding about merge-base computation. The successor may reuse semantic design evidence, not old merge authority.

Project State files and repository-only PSI controls should then fall under the explicit operational exclusions defined above, while `.github/workflows/conformance-ci.yml` remains release included.

### PR #16 — learning lifecycle pilot

Keep `d3e1f0d96e23698e740511e7cd8d21d542e17741` frozen as `VALIDATED_BUT_INTEGRATION_BLOCKED` evidence. Do not rerun its failed CI as a transient failure and do not mutate it.

After the new identity architecture is current, create a fresh pilot successor from current main. Its `governance/pilots/**` custody is operationally excluded under the reserved `governance/**` namespace, so adding the pilot evidence does not change framework payload identity. Fresh currentness and package validation remain mandatory.

## SVP learning-pilot impact

The architecture deliberately separates two identities:

- SVP's General Governance **framework lock** selects an exact released GG payload/revision;
- a non-normative **pilot evidence reference** may separately bind an exact GG operational artifact commit/blob.

Therefore the resumed SVP learning pilot need not force an SVP framework upgrade merely because GG records pilot evidence. The exact cross-project package must still specify its own authority/currentness and the GG operational reference by immutable commit/blob.

No pilot evidence transfers framework, execution or adopter authority. The future Claude Agent SDK C2 RUN-001 remains separately governed by the pre-run component-set and Owner-authority gates already established outside this architecture design.

## Non-goals and stop conditions

This design does not:

- alter or reinterpret rc.7;
- authorize implementation or a successor release;
- authorize a version string such as rc.8;
- authorize merge of this design branch;
- weaken exact Git commit or manifest binding;
- permit arbitrary glob/regex exclusions;
- permit operational exclusions under protected release roots;
- permit consumer-visible code to depend on excluded paths;
- make `main` a floating consumer selector;
- change consumer-lock schema by default;
- merge Project State Integrity or the learning pilot;
- repair/retry/rebase PR #15 or PR #16;
- change SVP/Dopis/adopter state.

STOP and return to architecture review if implementation evidence shows any of the following:

- exact lock tuple cannot safely remain unchanged;
- excluded operational bytes are required by consumer-visible validation/runtime;
- historical rc.7 cannot be reproduced exactly;
- default include cannot be enforced deterministically;
- protected release roots need to become excludable;
- isolated projection cannot execute required release-facing tests without a bypass that weakens production identity checks;
- a release-payload change can reach protected `main` while the old manifest still passes;
- resolving the architecture requires rewriting historical release evidence.

## Final disposition

`ARCHITECTURE_READY_FOR_IMPLEMENTATION_PROPOSAL`

The design resolves the accepted discovery without weakening immutable consumer locks: one Git commit continues to identify the complete repository revision; the manifest independently identifies the release declaration; and the prospective payload digest covers a fail-closed, explicitly classified release payload. `governance/**` becomes the reserved operational/evolution custody namespace, root repository-control exceptions are explicit, protected release roots cannot be excluded, and isolated-payload validation proves excluded bytes are not hidden dependencies.
