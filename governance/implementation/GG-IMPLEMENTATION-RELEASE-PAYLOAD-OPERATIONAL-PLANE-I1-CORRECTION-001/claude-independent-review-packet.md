---
review_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-CORRECTION-001-IR-001
correction_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-CORRECTION-001
reviewer: CLAUDE
mode: INDEPENDENT_READ_ONLY_SEMANTIC_SECURITY_REVIEW
candidate: 2567fbd67e7fff50383d347913cf6442fbdebc61
predecessor_candidate: b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea
historical_baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
status: PREPARED_FOR_EXTERNAL_INDEPENDENT_REVIEW
---

# Claude independent review — I1 FIND-001 successor correction

## Independence and authority boundary

Run in a fresh Claude/Claude Code session that did not implement this correction. Review is read-only. You may execute non-mutating commands and use temporary fixtures outside the repository, but MUST NOT modify tracked files, commit, push, open/modify a PR, merge, tag, release, deploy, publish, or repair findings.

The exact functional candidate to review is:

`2567fbd67e7fff50383d347913cf6442fbdebc61`

Do not review later governance-only custody commits as implementation content.

The predecessor that received Claude `CHANGES_REQUIRED` is:

`b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea`

Historical rc.7 baseline:

`22a1d5e2f759fda53574884e1056a3a56baa211a`

Previous blocking finding:

`FIND-001_TRACKED_SYMLINK_CONTENT_SMUGGLING_DEFEATS_GATE_B`

Previous material finding `FIND-002` documented that Gate A and legacy checkout regressions are expected to remain non-green until separately authorized P1 successor manifest/version packaging. Do not reinterpret that bootstrap state as a new correction defect unless the corrected candidate introduces a different failure.

## What changed in the correction

The correction is bounded to exactly:

- `tools/release_payload.py`
- `tests/test_release_payload_identity.py`
- `tests/test_release_payload_projection.py`

The intended semantics are:

1. Git index mode is inspected for tracked entries.
2. Release-included paths and `release-manifest.json` accept only regular Git modes `100644` and `100755`.
3. Included `120000` symlinks, `160000` gitlinks, and unsupported modes fail closed before digest/projection.
4. Every component of an included repository-relative filesystem path is checked for symlink traversal, so a regular index entry cannot be redirected using an ancestor symlink such as `tools -> governance`.
5. Projection verification likewise rejects direct or ancestor symlink substitution.
6. A symlink wholly inside an operationally excluded path such as `governance/**` remains outside scoped payload identity and must not re-couple the operational plane to release identity.
7. Historical rc.7 reproduction and exact-commit binding must remain intact.

An intermediate correction SHA `96512f33ee4af4e189a7648d48772ea38c45d8b9` is explicitly NOT the candidate. Self-adversarial review rejected it after discovering that an ancestor-directory symlink could bypass final-component-only checks. Review only `2567fbd...` as the proposed corrected state, but verify that the ancestor attack is truly closed.

## Required inspection

At minimum inspect:

- full functional diff `22a1d5e2f759fda53574884e1056a3a56baa211a..2567fbd67e7fff50383d347913cf6442fbdebc61`;
- correction diff `b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea..2567fbd67e7fff50383d347913cf6442fbdebc61`;
- `tools/release_payload.py`;
- `tests/test_release_payload_identity.py`;
- `tests/test_release_payload_projection.py`;
- unchanged `tools/validate_consumer.py`;
- unchanged `tools/validate_work_packet.py`;
- `contracts/release-manifest.schema.json`;
- `contracts/consumer-lock.schema.json`;
- `.github/workflows/conformance-ci.yml`;
- historical rc.7 `release-manifest.json` and `RELEASE_VERSION`.

## Mandatory adversarial questions

1. Does the exact original exploit `tools/evil.py -> ../governance/secret.txt` now fail before excluded bytes can enter digest or projection?
2. Does a broken included symlink fail from Git entry semantics rather than target existence?
3. Does an included gitlink/submodule mode `160000` fail closed?
4. Can a regular `100644`/`100755` tracked file still be redirected through a symlinked parent directory (`tools -> governance`, nested ancestor variants, absolute/relative targets)?
5. Can `build_projection()` copy bytes through any direct or ancestor symlink that classification did not intend?
6. Can `verify_projection()` be fooled after build by replacing an included file or any parent directory with a symlink, including a target containing byte-identical content?
7. Can an excluded operational path or parent symlink be injected into the isolated projection without detection?
8. Does allowing a tracked symlink wholly under `governance/**` correctly preserve two-plane decoupling, or does it create a different hidden dependency/bypass?
9. Are Git-mode checks applied to exactly the right set: release-included paths plus manifest, without unnecessarily making excluded operational entries part of payload identity?
10. Are path normalization, duplicate entries, non-zero index stages, malformed `git ls-files -s -z` metadata, encoding failures, missing files and unsupported modes deterministic and fail closed?
11. Does the new path-component check have a static or TOCTOU/race weakness material under the intended validation threat model? If so, demonstrate or classify it rather than assuming safety.
12. Is `100755` support semantically safe given that content identity hashes bytes and projection creation may normalize filesystem permissions? Determine whether exact Git commit binding is sufficient or whether Gate B must preserve/verify executable mode.
13. Is historical rc.7 exact content identity still reproduced with the current helper?
14. Does consumer-lock schema `2.0.0` remain sufficient?
15. Does WPDC remain source-unchanged and behaviorally compatible?
16. Do the new tests actually falsify the old vulnerable behavior and pass only for the corrected behavior, or are any assertions weak/tautological?
17. Did correction stay inside the three authorized functional paths?
18. Does the branch remain deliberately non-integrable until P1? Gate A/bootstrap failures must be disclosed as expected, not counted as green.

## Required execution evidence

Run at minimum, read-only:

```text
git rev-parse HEAD
git diff --stat b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea..2567fbd67e7fff50383d347913cf6442fbdebc61
git diff --stat 22a1d5e2f759fda53574884e1056a3a56baa211a..2567fbd67e7fff50383d347913cf6442fbdebc61
python3 -m py_compile tools/release_payload.py tests/test_release_payload_identity.py tests/test_release_payload_projection.py
python3 -m unittest -v tests/test_release_payload_identity.py tests/test_release_payload_projection.py
```

Also run the full suite or the relevant pre-existing WPDC/consumer suites. If failures are solely the already-documented legacy Gate A bootstrap mismatch, state them explicitly as `EXPECTED_BOOTSTRAP_FAIL_PENDING_P1`; any additional failure is a finding.

Construct independent temporary fixtures for direct symlink, broken symlink, ancestor-directory symlink, gitlink, operational-only symlink, direct projection symlink tamper, ancestor projection symlink tamper, and 100755 behavior. Do not rely only on the added tests.

## Required verdict

Begin with exactly one:

- `PASS`
- `CHANGES_REQUIRED`
- `INDETERMINATE`

Then provide:

### Candidate reviewed
Exact SHA.

### Findings
Stable ID, severity (`BLOCKING`, `MATERIAL`, `MINOR`), exact surface/reproduction, violated requirement, bounded recommendation. Do not repair.

### Validation evidence
Exact commands/fixtures actually executed and results. Distinguish observation from reasoning.

### FIND-001 closure assessment
Explicitly state whether the original direct-symlink exploit and the discovered ancestor-directory variant are both closed.

### Required invariants assessment
PASS/FAIL/INDETERMINATE for:

- included tracked symlink fail-closed;
- included gitlink/unsupported-mode fail-closed;
- ancestor-directory symlink fail-closed;
- projection direct-symlink tamper detection;
- projection ancestor-symlink tamper detection;
- operational-plane decoupling;
- scoped manifest/schema enforcement;
- exact-commit preservation;
- legacy rc.7 reproduction;
- consumer-lock 2.0.0 sufficiency;
- WPDC source-unchanged compatibility;
- I1 correction write-surface compliance;
- bootstrap non-integrability disclosure.

### Authority statement
State that review grants no correction, retry, P1 packaging, PR, merge, release, publication or adopter authority.

A `PASS` is valid only if no BLOCKING/MATERIAL finding remains and FIND-001 is independently demonstrated closed. If evidence is insufficient, return `INDETERMINATE`.
