# HWG design provenance

This directory preserves the General Governance design-process custody that produced `GG-HWG-ARCH-001`.

The empirical candidate has now been promoted on this branch into the prospective reusable `0.1.0-rc.10` release. The duplicate candidate schemas, validator and tests were removed after promotion so there is only one live machine contract.

## Preserved design artifact

- `GG_HWG_ARCHITECTURE_CANDIDATE_001.md` — design rationale, candidate invariants, empirical adoption reasoning and scope boundaries that preceded normative promotion.

## Normative rc.10 surfaces

The current reusable implementation is owned exclusively by release-included paths:

- `framework/capabilities/hierarchical-work-graph/contract.md`;
- `framework/capabilities/hierarchical-work-graph/adoption-contract.md`;
- `contracts/hierarchical-work-graph-bundle.schema.json`;
- `contracts/work-graph.schema.json`;
- `tools/validate_hierarchical_work_graph.py`;
- `tests/test_hierarchical_work_graph.py`;
- `docs/architecture/hierarchical-work-graph.md`.

The design provenance under `governance/**` remains outside the reusable release payload and is not an alternative contract.

## Empirical basis

The pre-promotion generic candidate passed eight positive/negative structural tests, including the three-level hierarchy case, cycle rejection, cross-graph dependency rejection, reciprocal parent binding, adjacent-level expansion, single-parent enforcement, orphan rejection and graph-digest rejection.

Dopis supplied the first adopter evidence by deterministically projecting its accepted vertical-slice topology and the already-established Ordering work-packet expansion without duplicating product truth.

Normative rc.10 conformance subsequently exercises the promoted schemas/validator under both the full-checkout and isolated release-payload gates.
