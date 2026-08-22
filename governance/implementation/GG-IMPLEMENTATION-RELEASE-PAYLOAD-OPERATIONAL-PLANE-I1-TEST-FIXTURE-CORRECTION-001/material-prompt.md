---
prompt_id: GG-MP-0013
version: 1.0.0
mode: BOUNDED_FINDING_CORRECTION
status: APPROVED_FOR_SINGLE_EXECUTION
---

# Material prompt — executable-mode test fixture correction

Correct only `FIND-EXEC-MODE-TEST-001` from Claude Independent Review `GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-EXEC-MODE-CORRECTION-001-IR-001`.

The production executable-mode implementation is already independently demonstrated correct. Do not modify production code.

Repair the two tests that add `tools/run.sh` after `ProjectionRepo.__init__` has already bound `release-manifest.json::content_sha256`. After mutating the tracked RELEASE_INCLUDED file set, deterministically recompute the fixture manifest content digest, rewrite/stage/commit the fixture manifest, and only then call `build_projection()`.

Keep the stale-manifest fail-closed behavior intact. The tests must reach and exercise their executable-mode assertions rather than bypassing identity validation.

Authorized non-custody write surface is exactly:

- `tests/test_release_payload_projection.py`

Do not address `FIND-MANIFEST-MODE-001` or `FIND-TOCTOU-001`. Do not package P1, modify the real release manifest/version, change WPDC/consumer-lock, open a PR, merge, release, publish, deploy, or mutate adopters.

Stop after producing an exact corrected candidate and preparing it for a fresh Claude Independent Reviewer.
