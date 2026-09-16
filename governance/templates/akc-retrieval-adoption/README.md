# AKC Repository Retrieval Adoption

This is a non-normative operational scaffold for projects that choose to consume the AI Knowledge Compiler repository-retrieval capability.

Authority boundaries:

- AKC owns the runtime retrieval contract and implementation.
- The adopter owns its repository scope, budgets, smoke/qualification fixtures, and qualification disposition.
- General Governance provides the reusable adoption shape only; it does not duplicate the AKC runtime schema and does not grant retrieval/model/provider/product authority.
- Indexes are rebuildable discovery state and must not be treated as canonical source authority.

## Adoption states

`ADOPTION_DECLARED` means the project has created an adopter manifest and pinned an exact AKC revision, but the capability has not yet been proven usable against that exact project revision. This is the template's initial state.

`CAPABILITY_AVAILABLE` requires provider-free doctor evidence bound to the exact pinned AKC revision and adopter revision. It proves the consumer can execute its configured smoke checks; it does **not** mean retrieval quality is qualified for ordinary project work.

`PROJECT_QUALIFIED` requires separate adopter-specific retrieval-quality evidence. A project must not promote itself to this state merely because another repository qualified the same AKC revision.

Both `CAPABILITY_AVAILABLE` and `PROJECT_QUALIFIED` must reference non-empty evidence in the adopter manifest. State transitions are explicit; a successful command does not mutate the adopter manifest automatically.

## Minimum adopter surface

Recommended path:

```text
.governance/capabilities/akc-retrieval.json
```

The manifest should pin an exact AKC Git revision and use the runtime schema owned by that revision:

```text
contracts/repository-retrieval-adoption-v1.json
```

The v1 runtime is expected to execute from that exact Git-backed AKC checkout; it verifies both provider repository identity and provider HEAD before retrieval.

## Context policy

Consumers should use the following order:

1. exact deterministic lookup when an ID/path is already known;
2. AKC bounded retrieval when relevant evidence must be discovered in a large repository corpus and the adopter has the required qualification for that use;
3. full-file or full-corpus inspection only when the task explicitly requires completeness.

Do not preload large canonical documents merely because they are authoritative. Retrieval must return bounded evidence and canonical bytes must be re-materialized from the exact Git revision before admission. An `ADOPTION_DECLARED` or `CAPABILITY_AVAILABLE` adopter may run bounded doctor/qualification work, but ordinary governed work must not make AKC retrieval mandatory until the adopter reaches the qualification state required by its local policy.

## Provider-free baseline

The v1 baseline is `lexical_v1`, using AKC BM25/FTS discovery plus exact Git re-materialization. `hybrid_v1` is a separately qualified capability because embedding/model identity and project-specific retrieval quality must be explicit.

Recommended conformance command from an AKC checkout pinned to the manifest revision:

```bash
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}"
python -m akc.repository_consumer doctor \
  --repo /path/to/adopter \
  --adoption /path/to/adopter/.governance/capabilities/akc-retrieval.json \
  --workspace "$CACHE_ROOT/akc/<project>/doctor"
```

A green doctor is evidence that may support an explicit promotion from `ADOPTION_DECLARED` to `CAPABILITY_AVAILABLE`; it does not perform that promotion itself. Project qualification requires a separate retrieval-quality fixture and evidence record.

## Index custody

Do not commit generated SQLite indexes, vectors, embeddings, or corpus chunk packages into adopter repositories. Keep them in rebuildable cache/workspace storage keyed by exact source revision and AKC transform identity.

## Reference adopter

Dopis is the intended first v1 adopter because AKC already has historical empirical retrieval qualification evidence over a Dopis holdout. That historical evidence does not automatically qualify a new Dopis revision; the adopter must bind and validate its own current revision.
