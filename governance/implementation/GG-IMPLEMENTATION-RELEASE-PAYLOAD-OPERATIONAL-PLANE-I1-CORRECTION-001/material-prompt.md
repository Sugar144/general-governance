---
prompt_id: GG-MP-0011
version: 1.0.0
mode: BOUNDED_FINDING_CORRECTION
status: APPROVED_FOR_SINGLE_EXECUTION
---

# Material prompt — I1 correction successor

Correct only `FIND-001_TRACKED_SYMLINK_CONTENT_SMUGGLING_DEFEATS_GATE_B` from Claude IR-001.

Use Git index entry mode as the authoritative tracked-entry type. Fail closed unless a tracked entry is a regular file with mode `100644` or `100755`. In particular, reject mode `120000` symlinks before any filesystem dereference, hashing, projection, or manifest handling; reject gitlinks/submodules (`160000`) and unknown modes likewise.

Preserve the predecessor candidate's accepted semantics, historical rc.7 digest reproduction, exact-commit validation, consumer-lock 2.0.0 compatibility, WPDC source compatibility, and non-integrable bootstrap state.

Add adversarial regressions proving an included symlink pointing into `governance/**` cannot smuggle operational bytes, a broken symlink fails because of Git mode, unsupported modes fail closed, and ordinary regular/executable files remain supported.

Do not modify any non-custody path beyond:

- `tools/release_payload.py`
- `tests/test_release_payload_identity.py`
- `tests/test_release_payload_projection.py`

Stop after producing and validating an exact corrected candidate. Do not package P1, open a PR, merge, release, or mutate adopters. A fresh Claude Independent Reviewer must review the corrected exact SHA.
