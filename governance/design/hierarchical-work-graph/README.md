# HWG candidate workspace

This directory is General Governance design-process custody for the non-normative `GG-HWG-ARCH-001` candidate.

It is intentionally outside the current General Governance release payload.

## Surfaces

- `GG_HWG_ARCHITECTURE_CANDIDATE_001.md` — architecture and candidate invariants;
- `contracts/hwg-bundle.schema.json` — bundle/profile/graph-file reference schema;
- `contracts/work-graph.schema.json` — WorkGraph/WorkNode schema;
- `validate_hwg_candidate.py` — deterministic structural validator;
- `tests/test_validate_hwg_candidate.py` — synthetic positive/negative tests.

## Candidate self-test

From the General Governance repository root:

```text
python -m unittest -v governance/design/hierarchical-work-graph/tests/test_validate_hwg_candidate.py
```

Requires `jsonschema`, already used by the current General Governance validation toolchain.

These candidate tests are deliberately not wired into the current release conformance workflow because `governance/**` is design/evolution custody and HWG has not been promoted into the current reusable release payload.

## Validate an adopter bundle

```text
python governance/design/hierarchical-work-graph/validate_hwg_candidate.py \
  /path/to/hwg/bundle.json \
  --source-root /path/to/adopter/repository
```

`--source-root` is optional. When supplied, `SHA256` and `GIT_BLOB_SHA1` source references are checked against the current adopter bytes. `OPAQUE_EXACT` references remain structural exact labels and are not externally resolved by this candidate.

A `VALID` structural result proves neither authority nor concurrent safety.
