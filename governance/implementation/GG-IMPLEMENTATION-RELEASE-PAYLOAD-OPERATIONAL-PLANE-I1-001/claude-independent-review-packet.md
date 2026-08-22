---
review_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-001-IR-001
implementation_id: GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-001
reviewer: CLAUDE
review_mode: INDEPENDENT_READ_ONLY_SEMANTIC_SECURITY_REVIEW
candidate: b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea
baseline: 22a1d5e2f759fda53574884e1056a3a56baa211a
status: PREPARED_FOR_EXTERNAL_INDEPENDENT_REVIEW
---

# Claude independent review packet — I1 scoped release payload identity

## Independence requirement

Run this review in a fresh Claude/Claude Code session that did not implement I1 and is not given the implementation agent's hidden reasoning. The reviewer is read-only: it may inspect repository history, candidate content, tests, architecture/proposal records, and execute non-mutating validation commands, but it MUST NOT modify files, commit, push, open/merge a PR, or repair findings.

The review target is the exact functional candidate:

`b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea`

The historical baseline is:

`22a1d5e2f759fda53574884e1056a3a56baa211a`

Do not review the later governance-only closure commits as implementation content. They may be consulted only as claimed evidence, never as a substitute for inspecting the exact candidate.

## Required sources

At minimum inspect:

- the exact diff `22a1d5e2f759fda53574884e1056a3a56baa211a..b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea`;
- `tools/release_payload.py`;
- `contracts/release-manifest.schema.json`;
- `tools/validate_consumer.py`;
- `.github/workflows/conformance-ci.yml`;
- `tests/test_release_payload_identity.py`;
- `tests/test_release_payload_projection.py`;
- `docs/consumer-contract.md`;
- `docs/architecture/release-payload-identity.md`;
- historical `release-manifest.json` and `RELEASE_VERSION` at baseline and candidate;
- `tools/validate_work_packet.py` to verify source-compatibility without modification;
- `contracts/consumer-lock.schema.json` to assess whether schema `2.0.0` remains sufficient;
- Issue #20 requirements and terminal evidence if useful.

## Mandatory review questions

1. Does classification fail closed? Any unknown/unmatched tracked path MUST become `RELEASE_INCLUDED`.
2. Can a malicious, ambiguous, overlapping, normalized, traversal-like, symlink-like, case/encoding-sensitive, or otherwise adversarial path bypass protected release classes or become operationally excluded incorrectly?
3. Are operational exclusions bounded exactly to the accepted method-v1 policy, with protected release surfaces non-excludable?
4. Is the scoped manifest validated both semantically and against its machine schema, with unsupported/extra structure rejected?
5. Is historical rc.7 behavior preserved exactly for the legacy manifest method, including content identity semantics?
6. Does production consumer validation preserve exact Git commit binding, with no `skip_git_check`, `ignore_commit`, projection shortcut, or equivalent bypass?
7. Is consumer-lock schema `2.0.0` genuinely sufficient for the new release identity model, or does the adopter need a new obligation/field?
8. Does `tools/validate_work_packet.py` remain behaviorally compatible without source modification, including error classification/exception behavior and digest calls?
9. Does Gate B actually prove isolated release-payload self-sufficiency with operational evidence and `.git` physically absent, rather than merely testing imports or a weaker proxy?
10. Can a hidden dependency on `governance/**` or other excluded operational content survive Gate B?
11. Can projection creation or verification omit, add, mutate, misclassify, or fail to bind release-included files without detection?
12. Are digest calculation, path ordering, path normalization, file-mode/symlink handling, missing-file handling, Git command failures, and schema failures deterministic and fail closed?
13. Is the CI ordering safe: do identity/schema/projection failures occur before any result could be interpreted as release-ready?
14. Is any current test coupled to rc.7 in a way that would falsely block the first legitimate scoped successor release?
15. Is any current test too weak and capable of passing while the intended security/property invariant is false?
16. Did I1 stay inside its authorized eight-path functional write surface and leave `release-manifest.json`, `RELEASE_VERSION`, WPDC source, consumer-lock/config schemas, POC, and provenance unchanged?
17. Is the candidate correctly classified as non-integrable until separately authorized successor packaging supplies a coherent version/manifest/digest and reruns full gates?

## Required adversarial validation

The reviewer should execute read-only tests or construct temporary fixtures outside the repository when useful. At minimum challenge:

- unknown paths;
- attempts to exclude protected paths;
- malformed/extra manifest fields;
- overlapping exclusion rules;
- hidden operational dependencies;
- missing manifest/schema files;
- Git/I/O/subprocess failures;
- projection tampering;
- exact-commit mismatch;
- legacy rc.7 reproduction;
- WPDC compatibility;
- consumer-lock sufficiency.

Do not accept implementation-agent claims without independently checking them.

## Required output

Return exactly one top-level verdict:

- `PASS`
- `CHANGES_REQUIRED`
- `INDETERMINATE`

Then provide:

### Candidate reviewed
Exact SHA.

### Findings
For every finding: stable ID, severity (`BLOCKING`, `MATERIAL`, `MINOR`), exact file/line or reproducible surface, why it violates the accepted architecture/proposal/Issue #20 requirement, and a bounded correction recommendation. Do not implement the correction.

### Validation evidence
Commands/tests/fixtures actually executed and observed result. Distinguish observed evidence from reasoning.

### Required invariants assessment
Explicit PASS/FAIL/INDETERMINATE for: fail-closed classification; protected exclusion boundaries; scoped manifest/schema enforcement; exact-commit preservation; legacy rc.7 reproduction; consumer-lock 2.0.0 sufficiency; WPDC source-unchanged compatibility; isolated payload Gate B; hidden-dependency detection; I1 write-surface compliance; non-integrable bootstrap state.

### Authority statement
State explicitly that the review grants no correction, retry, packaging, PR, merge, release, publication, or adopter authority.

A `PASS` is valid only if no blocking/material finding remains and all mandatory invariants are established from independent evidence. If repository access or evidence is insufficient, return `INDETERMINATE`, never infer PASS.
