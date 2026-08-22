# Material prompt — scoped Git-mode identity correction

Identity: `GG-MP-0012/1.0.0`

Implement exactly one bounded correction for `P1-FIND-EXECUTABLE-MODE-NOT-AUTHENTICATED-001` from predecessor PR head `c787971f33c78d1d5b8cf57bdf1dc983acd22e53`.

Goal: make `SCOPED_TRACKED_FILES_V1` authenticate included tracked Git mode (`100644` or `100755`) together with normalized path and exact file-byte SHA-256, while preserving the historical legacy `1.3.0` / rc.7 record encoding exactly.

Required scoped record encoding:

`<path>\0<git-mode>\0<SHA-256(file bytes)>\n`

Required legacy encoding remains:

`<path>\0<SHA-256(file bytes)>\n`

Add deterministic regressions proving:

1. same path + same bytes + `100644 -> 100755` changes scoped `content_sha256`;
2. changing a projected file mode and its projection-index mode field together cannot preserve/reproduce the manifest scoped digest;
3. rc.7 historical reproduction remains exact.

Update `docs/architecture/release-payload-identity.md` to describe the corrected prospective scoped algorithm while leaving historical governance design evidence untouched.

Rebind `release-manifest.json.content_sha256` only after exact local computation from the completed authorized release-included changes.

Do not change version, schema token, scoped method token, compatibility tuple, policy exclusions, consumer locks, validators outside `tools/release_payload.py`, CI, framework/provenance, or adopter surfaces.

Any need for a sixth functional path is a terminal STOP requiring new Owner disposition.