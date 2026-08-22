# Release Payload Identity and Operational Evidence Plane

Status: prospective implementation for the first successor release after
`0.1.0-rc.7`.

This document describes the machine interpretation implemented by
`tools/release_payload.py`. It does not create release, merge, publication, or
adopter authority.

## 1. Two identities, one repository

General Governance keeps one Git repository but distinguishes two content
planes:

1. **Framework Release Payload** — bytes that can affect reusable framework
   semantics, contracts, validators, compatibility, conformance, reusable
   tooling, or release interpretation.
2. **GG Operational / Evolution Plane** — repository-local governance and
   evidence used to operate and evolve General Governance itself.

The exact Git commit always binds the complete repository revision. The release
manifest hash binds the exact release declaration. For a scoped release,
`content_sha256` binds only the classified Framework Release Payload.

This is not a weaker repository identity. It is a separation between whole-tree
identity and consumer-visible release-payload identity.

## 2. Historical dispatch

Manifest schema `1.3.0` retains the historical method used by rc.7:
`LEGACY_COMPLETE_TRACKED_FILES_V1`.

For that method, the digest input is every Git-tracked path except
`release-manifest.json`, using the existing record encoding:

`<path>\0<SHA-256(exact file bytes)>\n`

Records are sorted lexicographically and the concatenated UTF-8 byte stream is
SHA-256 hashed.

Historical rc.7 is never rewritten or reinterpreted under the scoped method.

## 3. Scoped method

Manifest schema `1.4.0` may declare `SCOPED_TRACKED_FILES_V1` with default
classification `RELEASE_INCLUDED`, manifest self-exclusion, reserved operational
prefix `governance/`, and bounded exact-path operational exclusions.

The release manifest is excluded only from `content_sha256` to avoid
self-reference. It remains independently bound by `release_manifest_sha256`
and is never operational evidence.

### 3.1 Fail-closed default

Any tracked path that is not explicitly operational is `RELEASE_INCLUDED`. A
new unknown path therefore changes the release-payload digest by default.

### 3.2 Protected release surfaces

Method v1 treats these as release payload and refuses policy attempts to exclude
them: `framework/**`, `contracts/**`, `tools/**`, `tests/**`, `docs/**`,
`provenance/**`, `RELEASE_VERSION`, `README.md`, and
`.github/workflows/conformance-ci.yml`.

### 3.3 Reserved operational namespace

`governance/**` is reserved for General Governance project-operational custody.
Reusable consumer-visible framework behavior must not be implemented there.

### 3.4 Exact-path operational exceptions

Method v1 allows only the accepted exact-path allow-list: `.gitignore`,
`AGENTS.md`, `PROJECT_STATE.yaml`, `ROADMAP.md`,
`project-state-integrity.json`, `scripts/project_state_integrity.py`,
`.github/pull_request_template.md`, and
`.github/workflows/project-state-integrity.yml`.

Omission is fail-closed: an omitted path becomes `RELEASE_INCLUDED`. Arbitrary
globs, regex, negation, last-rule-wins semantics, and user-defined prefixes are
unsupported.

## 4. Scoped digest algorithm

Historical `LEGACY_COMPLETE_TRACKED_FILES_V1` keeps its existing record encoding
unchanged:

`<path>\0<file-sha256>\n`

For `SCOPED_TRACKED_FILES_V1`, validate the manifest, enumerate tracked entries,
classify every path, omit only the manifest and operational exclusions, and
authenticate each included path, its supported tracked Git mode, and the
SHA-256 of its exact file bytes. The sorted scoped record encoding is:

`<path>\0<git-mode>\0<file-sha256>\n`

Supported regular-file modes are `100644` and `100755`; unsupported tracked
modes fail closed. The SHA-256 of the concatenated scoped record stream must
equal manifest `content_sha256`. A chmod-only change of an included file
therefore changes the scoped payload identity even when its bytes are unchanged.

## 5. Isolated payload projection

A scoped digest alone does not prove that excluded files are non-functional.
`build_projection` constructs a fresh directory containing every
`RELEASE_INCLUDED` path, `release-manifest.json`, and a temporary
`projection-index.json`. It excludes `.git`, all operational paths, and any
undeclared extras.

`verify_projection` fails on missing/changed included files, injected excluded
files, undeclared extras, manifest mismatch, or digest mismatch.

The projection API is separate from production consumer validation. There is no
`skip_git_check`, `ignore_commit`, or equivalent bypass.

## 6. Gate A — full checkout identity

Gate A runs on the real candidate checkout and validates exact release identity,
historical rc.7 reproduction, compatibility and existing consumer/WPDC
regressions. A release-included implementation branch with an unchanged legacy
rc.7 manifest is expected to fail Gate A and is not a release candidate.

## 7. Gate B — isolated payload self-sufficiency

Gate B applies to scoped candidates and later operational-only changes retaining
the scoped identity. It runs projection-safe schema, compile/import, provenance,
and projection tests with operational files and `.git` physically absent. If
included code requires excluded operational bytes, Gate B fails. Gate B never
replaces Gate A.

## 8. Consumer lock

The consumer lock remains `(repository, version, commit_sha,
release_manifest_sha256)` for schema `2.0.0`. The manifest hash binds the policy;
the exact commit binds the whole repository. Any future need for a new adopter
field requires compatibility review.

## 9. Payload-equivalent repository revisions

After a scoped release exists, operational-only commits may share framework
version, manifest, and payload digest while remaining distinct exact Git
revisions. They do not become publication anchors implicitly. Changing any
`RELEASE_INCLUDED` byte requires coherent successor release packaging.

## 10. Bootstrap from rc.7

The implementation introducing this mechanism cannot be merged as rc.7 because
release-included changes correctly break rc.7's legacy digest. The transition is
therefore two-effect: I1 implementation remains
`NON_INTEGRABLE_PENDING_SUCCESSOR_RELEASE_PACKAGING`; later P1, under separate
authority, selects the successor version, updates version/manifest, computes the
scoped digest, and runs Gate A + Gate B before a merge-eligible candidate exists.

## 11. Operational evidence references

An adopter may reference a GG operational artifact by exact commit/path/blob
independently from its framework lock. That reference is evidence only: it does
not upgrade the framework lock or transfer authority.
