# AKC Repository Retrieval Adoption

This is a non-normative operational scaffold for projects that choose to consume the AI Knowledge Compiler repository-retrieval capability.

Authority boundaries:

- AKC owns the runtime retrieval contract and implementation.
- The adopter owns its repository scope, budgets, smoke/qualification fixtures, and qualification disposition.
- General Governance provides the reusable adoption shape only; it does not duplicate the AKC runtime schema and does not grant retrieval/model/provider/product authority.
- Indexes are rebuildable discovery state and must not be treated as canonical source authority.

## Adoption states

`CAPABILITY_AVAILABLE` means the adopter can invoke the pinned AKC capability and the provider-free doctor passes. It does **not** mean retrieval quality is qualified for that project.

`PROJECT_QUALIFIED` requires adopter-specific qualification evidence. A project must not promote itself to this state merely because another repository qualified the same AKC revision.

## Minimum adopter surface

Recommended path:

```text
.governance/capabilities/akc-retrieval.json
```

The manifest should pin an exact AKC Git revision and use the runtime schema owned by that revision:

```text
contracts/repository-retrieval-adoption-v1.json
```

## Context policy

Consumers should use the following order:

1. exact deterministic lookup when an ID/path is already known;
2. AKC bounded retrieval when relevant evidence must be discovered in a large repository corpus;
3. full-file or full-corpus inspection only when the task explicitly requires completeness.

Do not preload large canonical documents merely because they are authoritative. Retrieval must return bounded evidence and canonical bytes must be re-materialized from the exact Git revision before admission.

## Provider-free baseline

The v1 baseline is `lexical_v1`, using AKC BM25/FTS discovery plus exact Git re-materialization. `hybrid_v1` is a separately qualified capability because embedding/model identity and project-specific retrieval quality must be explicit.

Recommended conformance command from an AKC checkout pinned to the manifest revision:

```bash
python -m akc.repository_consumer doctor \
  --repo /path/to/adopter \
  --adoption /path/to/adopter/.governance/capabilities/akc-retrieval.json \
  --workspace "$XDG_CACHE_HOME/akc/<project>/doctor"
```

A green doctor establishes capability availability only. Project qualification requires a separate retrieval-quality fixture and evidence record.

## Index custody

Do not commit generated SQLite indexes, vectors, embeddings, or corpus chunk packages into adopter repositories. Keep them in rebuildable cache/workspace storage keyed by exact source revision and AKC transform identity.

## Reference adopter

Dopis is the intended first v1 adopter because AKC already has historical empirical retrieval qualification evidence over a Dopis holdout. That historical evidence does not automatically qualify a new Dopis revision; the adopter must bind and validate its own current revision.
