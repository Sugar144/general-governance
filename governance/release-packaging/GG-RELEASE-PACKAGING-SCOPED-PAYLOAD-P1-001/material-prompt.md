# Material Prompt — GG-MP-0011

Prepare the first coherent successor General Governance release package from exact source candidate `201a4566bfff7c35c56ad112f203c46f19d70385`.

Execution is blocked until the Project Owner explicitly selects and authorizes one exact successor framework version.

Once authorized, modify only:

- `RELEASE_VERSION`
- `release-manifest.json`

Required packaging semantics:

- `RELEASE_VERSION` and `release-manifest.json::framework_version` must equal the exact Owner-authorized successor version.
- `release-manifest.json::manifest_schema_version` must be `1.4.0`.
- replace legacy `content_identity_method` with `content_identity` using `SCOPED_TRACKED_FILES_V1`.
- default classification must be `RELEASE_INCLUDED`.
- `release-manifest.json` is self-excluded from `content_sha256` only.
- reserved operational prefix must be exactly `governance/`.
- operational exact-path exclusions must remain within the fixed allowlist already encoded by I1.
- compatibility declarations remain unchanged unless deterministic evidence forces STOP.
- `content_sha256` must be recomputed from the exact scoped Framework Release Payload after the version/manifest packaging mutation.

Validation must establish full Gate A and Gate B, targeted and full-suite regressions, exact historical rc.7 reproduction, WPDC unchanged compatibility, consumer-lock `2.0.0` sufficiency, symlink/gitlink/executable-mode hardening preservation, and a fresh independent semantic/security review.

Any need to mutate another non-custody path is a terminal STOP requiring new Owner disposition.

This prompt grants no PR, merge, tag, release, deployment, publication, adopter mutation, frozen PR #15/#16 mutation, learning-pilot successor, PSI successor, or SVP mutation authority.
