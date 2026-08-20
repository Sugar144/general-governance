---
record_id: GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001-RESULT-001
execution_id: GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
status: VALIDATED_PENDING_PROJECT_OWNER_REVIEW
disposition: COMBINED_RELEASE_READY_INTEGRATION_REQUIRED
general_governance_main_baseline: 91fa0727abf730e142a4c43f2da68b1281be1121
accepted_implementation_head: 95e7dafac6afee54ca1ff6112dcd0cded74d08e8
formal_input_package_sha256: b9dde57a0d25e8ec21808581595fcbaa6ed7a17d802bca6d6c19ed3fef333d26
---

# Bounded Replacement Execution — Integration Readiness Result

## 1. Executive disposition

**Primary disposition: `COMBINED_RELEASE_READY_INTEGRATION_REQUIRED`.**

The accepted normative implementation must **not** be merged into `main` by itself. The safe path is to prepare `0.1.0-rc.5` release packaging on top of the exact accepted implementation lineage, validate the complete release-ready tree, and only then expose that complete tree to PR/merge.

This is not because the accepted Project Operating Contract change is defective. It is because General Governance release identity is content-bound: `release-manifest.json.content_sha256` covers every tracked file except the manifest itself, and `tools/verify_evolution.py` also binds the evolved Project Operating Contract bytes. Merging the POC alone would knowingly create a release-incoherent `main`.

## 2. Bound identities

This readiness decision is bound to:

- `main`: `91fa0727abf730e142a4c43f2da68b1281be1121`;
- accepted normative implementation HEAD: `95e7dafac6afee54ca1ff6112dcd0cded74d08e8`;
- accepted normative candidate commit: `ef10fb6baca3844d156abd9f5c79517b404889f2`;
- accepted POC blob: `9abe903e6c045fd67c1a061e8dff79fbb076fdd3`;
- implementation validation blob: `9aa898fc4df8e09e083b8c7d7f1e365f20f16949`;
- rc.4 `RELEASE_VERSION` blob: `9ad3f36aa010e24aa5c6abfb54a3ccc221617fdf`;
- rc.4 release-manifest blob: `048a6148e6192cccf6e33916606f2699635620c1`;
- rc.4 evolution-manifest blob: `2b76a961545c87dbedae5b503ea7756faacfbc46`;
- rc.4 consumer-contract blob: `ccaafcd63b5f874efb6bad25ecb9d21e243dc8c2`;
- historical rc.4 materialization commit: `e84e733730ce14f128653b4f9060c283ba6060bf`.

The accepted POC bytes are immutable input to future release packaging. rc.5 packaging may describe and identify them, but must not refine them.

## 3. Release-conformance dependency

Two existing deterministic mechanisms make release packaging mandatory before merge.

First, `tools/validate_consumer.py` recomputes a release content digest over **all tracked files except `release-manifest.json`** and requires it to equal `release-manifest.json.content_sha256`.

Second, `tools/verify_evolution.py` requires each evolved extracted surface to match the `candidate_sha256` declared in `provenance/evolution-manifest.json`. The current evolution manifest still identifies the prior POC candidate bytes.

Therefore the accepted POC candidate is a valid pre-release normative candidate but is not independently merge-ready. `main` must not advance to it while retaining rc.4 release identity.

## 4. Minimum rc.5 packaging surface

The smallest justified **existing-file** release-packaging surface on top of the accepted implementation is exactly five files:

1. `RELEASE_VERSION`
   - change `0.1.0-rc.4` -> `0.1.0-rc.5`.

2. `README.md`
   - identify rc.5 as the current prospective correction candidate;
   - preserve rc.2 configuration contracts, rc.3 capability composition and rc.4 bounded operational delegation;
   - summarize the new bounded replacement-execution lifecycle clarification.

3. `docs/consumer-contract.md`
   - identify compatibility as `0.1.0-rc.5`;
   - state that framework contract `2.0.0`, consumer-lock schema `2.0.0`, consumer-configuration schema `1.0.0`, and capability-composition contract/schema `1.0.0` remain unchanged;
   - describe bounded replacement execution as an L0 clarification;
   - state that rc.4 -> rc.5 requires a new immutable lock identity but no configuration migration.

4. `provenance/evolution-manifest.json`
   - preserve the original extraction baseline;
   - update the POC evolved-surface `candidate_sha256` to the SHA-256 of the exact accepted POC bytes;
   - extend the reason to cover bounded replacement-execution semantics;
   - leave the unchanged configuration-schema evolved surface unchanged.

5. `release-manifest.json`
   - change `framework_version` to `0.1.0-rc.5`;
   - preserve compatibility declarations and required-framework surfaces;
   - set `content_sha256` to the digest of the **final** tracked release tree, excluding `release-manifest.json` itself.

No new schema, tool, test, L6, configuration, extraction-manifest, capability-composition, or migration document change is justified.

The accepted `framework/core/project-operating-contract.md` is already part of the release-ready lineage and must remain byte-identical to blob `9abe903e6c045fd67c1a061e8dff79fbb076fdd3`.

Historical rc.4 materialization provides direct precedent for this surface: rc.4 updated README, RELEASE_VERSION, consumer contract, POC evolution provenance and release manifest alongside the L0 change.

## 5. Safe branch and commit sequencing

The release-ready branch should descend from the **validated and accepted readiness lineage**, which itself descends from accepted implementation HEAD `95e7dafa...`. This preserves the accepted normative implementation as an immutable ancestor rather than recreating or cherry-picking its meaning.

Recommended sequence for the future rc.5 package:

1. bind exact `main`, accepted implementation, accepted readiness result, and the five rc.4 release-facing blobs;
2. create one release-packaging branch from the accepted readiness HEAD;
3. add repository-custodied release-package authority, input package, prompt, work package and preflight;
4. modify `RELEASE_VERSION`, `README.md`, `docs/consumer-contract.md`, and `provenance/evolution-manifest.json`;
5. prepare all tracked release-package evidence that is intended to remain in the final release tree, including a pre-manifest validation record;
6. verify the POC blob remains exactly `9abe903e...` and all non-release surfaces remain fenced;
7. compute `release_content_digest` over that complete tracked tree;
8. update `release-manifest.json` **as the final tracked content mutation**;
9. perform post-manifest validation read-only;
10. after step 8, do not add or modify any tracked file on the release candidate.

The final post-manifest terminal record should therefore live outside the tracked release tree, e.g. as durable Issue/PR evidence, because adding a repository file after finalizing the manifest would change the content digest it is supposed to identify.

## 6. PR and merge topology

Use **one release-ready PR**, not a normative-only PR followed by a release-fix PR.

That PR should carry one coherent descendant history containing:

- the already accepted normative implementation;
- accepted readiness custody/evidence;
- the separately authorized rc.5 packaging;
- the finalized rc.5 release manifest.

Separate commits are desirable for reviewability, but they must be in one branch/PR whose **final tree is release-conformant before merge**.

A normative-only PR is rejected because merging it first would knowingly place `main` in a state whose tracked content does not match the rc.4 release manifest.

PR creation itself remains a separate effect and should happen only after the release-ready candidate is deterministically validated and reviewed under its own authority.

## 7. Content-digest finalization rule

The decisive invariant is:

**`release-manifest.json` must be the last tracked-file mutation in the final release-ready candidate.**

Reason: `release_content_digest()` hashes every tracked path other than `release-manifest.json`. This includes governance custody, work-package, validation, and other evidence files if they are tracked.

Consequences:

- all tracked rc.5 package evidence that will ship must exist before the digest is computed;
- no tracked validation record may be appended after manifest finalization;
- no Owner-acceptance repository file may be added to that exact candidate after manifest finalization;
- issue comments, PR reviews/checks, and merge metadata may record post-finalization decisions because they do not change the Git tree;
- if any tracked file changes after manifest finalization, the candidate is invalidated and the manifest must be recomputed under valid authority.

This sequencing avoids a self-invalidating release candidate and avoids any need for a self-referential validation record.

## 8. CI and deterministic gates

Before any merge authority is exercised, the exact final release-ready candidate must pass at minimum:

1. `main` currentness fence against the authorized baseline;
2. accepted implementation ancestor/head and POC-blob fence;
3. exact five-file rc.5 packaging surface plus authorized new custody/evidence only;
4. `RELEASE_VERSION == 0.1.0-rc.5`;
5. `release-manifest.json.framework_version == 0.1.0-rc.5`;
6. unchanged compatibility declarations;
7. `provenance/evolution-manifest.json` candidate SHA-256 reproduces the accepted POC bytes;
8. `python3 tools/verify_evolution.py` PASS;
9. release content digest reproduces `release-manifest.json.content_sha256`;
10. all contract schemas remain valid;
11. `python3 -m py_compile tools/validate_capability_stack.py` PASS;
12. `python3 -m unittest -v tests/test_consumer_contract.py` PASS;
13. the repository `conformance-ci` workflow is green on the exact release-ready commit;
14. final compare proves no accepted POC wording refinement and no unapproved schema/tool/test/L6/configuration change.

A PR-triggered CI run may repeat these checks, but it does not replace the exact-candidate identity/currentness fence required before merge.

## 9. Authority boundaries

Future effects remain distinct:

- **rc.5 packaging mutation**: requires separate prospective authority over the five release-facing files plus its custody/evidence directory;
- **branch commits/pushes**: must be explicitly included in that package authority if performed;
- **PR creation**: separate publication effect unless explicitly prospectively included in a later bounded grant;
- **review**: evaluates the exact release-ready candidate but does not accept it;
- **Project Owner acceptance**: remains reserved and must bind the exact release-ready candidate;
- **merge**: requires its own authority or an explicit prospective bounded integration grant and must recheck exact currentness/candidate identity;
- **tag/release/publication**: remain separate effects after integration;
- merge, green CI, tag, or release never substitute for Owner acceptance.

This readiness result creates none of those authorities.

## 10. Currentness and anti-drift fences

At future rc.5 packaging admission, require:

- `main == 91fa0727abf730e142a4c43f2da68b1281be1121`, unless a new Owner-authorized re-evaluation binds a later baseline;
- accepted implementation remains ancestor-identical at `95e7dafa...`;
- POC blob remains `9abe903e...`;
- accepted readiness result identity is exact;
- all five release-facing source blobs remain the bound rc.4 blobs before mutation.

Before PR creation and again before merge:

- final release-ready branch HEAD must equal the reviewed candidate;
- `main` must still satisfy its currentness fence;
- the candidate tree must still contain exact accepted POC bytes;
- CI must correspond to the exact candidate;
- no tracked post-manifest mutation may exist.

Any drift stops integration. Do not silently rebase, regenerate wording, or recompute a new release candidate under stale authority.

## 11. Explicit exclusions

This readiness run does not:

- modify any release-facing file;
- create rc.5;
- alter the accepted POC;
- modify schemas, tooling, tests, L6, configuration, or capability composition;
- create a PR;
- merge to `main`;
- tag or release;
- publish or deploy;
- accept a future release-ready candidate;
- authorize a second readiness execution.

## 12. Recommended next package

If the Project Owner accepts this readiness result, open a separately identified:

`GG-RELEASE-PACKAGE-0.1.0-RC.5-001`

The package should be authorized to prepare and validate the five-file rc.5 release surface **on top of this accepted lineage**, preserve POC blob `9abe903e...`, finalize `release-manifest.json` last, and stop with a fully conformance-green release-ready candidate for Owner review.

PR creation, merge, tag, release, and publication should remain outside that package unless the Owner explicitly grants those effects prospectively and the final candidate/currentness gates are defined.
