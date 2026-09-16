# AKC Repository Retrieval Adoption

This is a non-normative operational scaffold for projects that choose to consume the AI Knowledge Compiler repository-retrieval capability.

Authority boundaries:

- AKC owns the runtime retrieval contract and implementation.
- The adopter owns its repository scope, exact source revision, budgets, smoke/qualification fixtures, and qualification disposition.
- General Governance provides the reusable adoption shape only; it does not duplicate the AKC runtime schema and does not grant retrieval/model/provider/product authority.
- Indexes are rebuildable discovery state and must not be treated as canonical source authority.

## Adoption states

`ADOPTION_DECLARED` means the project has created an adopter manifest and pinned both an exact AKC provider revision and an exact adopter source revision, but the capability has not yet been proven usable against that exact pair. This is the template's initial state.

`CAPABILITY_AVAILABLE` requires provider-free doctor evidence bound to the exact pinned AKC revision, exact pinned adopter source revision, adopter `source_id`, and deterministic fingerprint of the complete adoption/retrieval identity. The manifest also pins the exact doctor artifact bytes through `qualification.evidence_sha256`. It proves the consumer can execute its configured smoke checks; it does **not** mean retrieval quality is qualified for ordinary project work.

`PROJECT_QUALIFIED` retains the same doctor proof and additionally requires separate adopter-specific retrieval-quality evidence bound to that same complete adoption identity. The project-quality artifact is independently pinned through `qualification.project_evidence_sha256` and must itself bind both the doctor path and doctor SHA-256. A project must not promote itself merely because another repository, revision, source identity, retrieval policy, or replacement evidence file qualified the same AKC runtime.

The manifest distinguishes the two evidence layers explicitly:

- `qualification.evidence` + `qualification.evidence_sha256`: committed doctor-v1 `PASS` artifact and immutable content identity required for every post-declaration state;
- `qualification.project_evidence` + `qualification.project_evidence_sha256`: additional committed project-quality `PASS` artifact and immutable content identity required only for `PROJECT_QUALIFIED`.

The v1 runtime does not trust these fields merely because they are non-empty. Before a query it resolves evidence inside the adopter repository, requires repository-relative tracked clean files with **no symbolic-link component anywhere in the evidence path**, verifies their declared SHA-256 digests, validates the expected evidence schema and `PASS` result, and checks exact capability/provider/source/mode bindings plus `source_id` and a deterministic adoption fingerprint covering schema/capability/provider/source/retrieval policy, including budgets and smoke queries. Project-quality evidence must bind the same fingerprint and the exact capability-evidence path and SHA-256.

State transitions are explicit; a successful command does not mutate the adopter manifest automatically. Advancing the adopter repository does not move the qualified source revision automatically either: change `source.revision`, re-run the applicable evidence, and promote explicitly. Changing `source_id`, retrieval budgets, smoke queries, another fingerprinted adoption-policy field, or either evidence artifact's bytes likewise invalidates prior qualification until the corresponding pins/evidence are renewed.

## Minimum adopter surface

Recommended path:

```text
.governance/capabilities/akc-retrieval.json
```

The manifest must pin two independent Git identities:

- `provider.revision`: the exact AKC commit that owns and executes the runtime contract;
- `source.revision`: the exact adopter commit whose canonical bytes may be discovered and materialized.

The reusable template uses forty zeroes only as an obvious placeholder. Replace both placeholder revisions with real 40-hex Git commit SHAs before running `doctor`; a template placeholder is never qualification evidence.

The source binding uses:

```json
{
  "revision": "<exact-adopter-commit>",
  "revision_policy": "PINNED_EXACT_REVISION"
}
```

The runtime schema is owned by the pinned AKC revision:

```text
contracts/repository-retrieval-adoption-v1.json
```

The v1 runtime is expected to execute from the exact Git-backed AKC checkout declared by `provider.revision`; it verifies provider repository identity, provider HEAD, and a completely clean provider checkout before retrieval. It separately verifies the adopter repository identity and that `source.revision` exists. Retrieval then builds and re-materializes evidence from that pinned source commit, not from whichever commit happens to be checked out later.

This distinction is deliberate. If an adopter is qualified at source commit A and its working checkout advances to B, evidence remains bound to A until governance explicitly repins to B and produces the required evidence for B.

## Context policy

Consumers should use the following order:

1. exact deterministic lookup when an ID/path is already known;
2. AKC bounded retrieval when relevant evidence must be discovered in a large repository corpus and the adopter has the required qualification for that use;
3. full-file or full-corpus inspection only when the task explicitly requires completeness.

Do not preload large canonical documents merely because they are authoritative. Retrieval must return bounded evidence and canonical bytes must be re-materialized from the exact pinned `source.revision` before admission. An `ADOPTION_DECLARED` adopter may run `doctor`, but the v1 query interface remains fail-closed until the adopter has reached a post-declaration state with verified doctor evidence. A `CAPABILITY_AVAILABLE` adopter may use the bounded capability only within the scope permitted by its local policy; ordinary governed work must not make AKC retrieval mandatory until the adopter reaches the qualification state required by that policy.

## Query-result provenance

The CLI `query` command emits `akc-repository-retrieval-query-result/1.0.0`, not a bare `EvidenceSet`. The result envelope preserves alongside the bounded evidence:

- provider repository and exact provider revision;
- adopter `source_id`, repository and exact source revision;
- retrieval mode and deterministic adoption fingerprint;
- lifecycle qualification status;
- capability-evidence path and SHA-256;
- project-evidence path and SHA-256 when project-qualified;
- the exact executed `ContextQuery`, including intent, exact terms, path/authority filters, requested evidence classes, source identity/revision and budget;
- `query_fingerprint`, a deterministic SHA-256 over every serialized `ContextQuery` field.

The runtime builds this provenance from the same `ContextQuery` object passed into lexical discovery and evidence admission, rather than reconstructing query metadata afterwards. Reusing a `query_id` with different intent, exact terms, path filters, authority filters, source fields or budget therefore produces distinguishable query provenance.

This makes an archived or handed-off retrieval result attributable to the exact transformation, query and evidence that authorized it. Consumers must not strip that provenance when persisting or passing query output across agents.

## Provider-free baseline

The v1 baseline is `lexical_v1`, using AKC BM25/FTS discovery plus exact Git re-materialization. `hybrid_v1` is a separately qualified capability because embedding/model identity and project-specific retrieval quality must be explicit.

Recommended conformance command from a clean AKC checkout pinned to `provider.revision`:

```bash
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}"
python -m akc.repository_consumer doctor \
  --repo /path/to/adopter \
  --adoption /path/to/adopter/.governance/capabilities/akc-retrieval.json \
  --workspace "$CACHE_ROOT/akc/<project>/doctor"
```

The adopter checkout does not have to be detached at `source.revision`; the runtime uses the manifest's exact source commit. The commit must exist in that repository checkout/object database and must belong to the declared repository identity.

A green doctor is evidence that may support an explicit promotion from `ADOPTION_DECLARED` to `CAPABILITY_AVAILABLE`; it does not perform that promotion itself. Commit the doctor JSON inside the adopter repository, compute its SHA-256, and reference both through `qualification.evidence` and `qualification.evidence_sha256` before promotion. Project qualification requires a separate committed retrieval-quality evidence record referenced by path and SHA-256 through `qualification.project_evidence` and `qualification.project_evidence_sha256`; that record must also bind the same exact provider/source identity, `source_id`, deterministic adoption fingerprint, and doctor path/hash.

## Index custody

Do not commit generated SQLite indexes, vectors, embeddings, or corpus chunk packages into adopter repositories. Keep them in rebuildable cache/workspace storage keyed by exact source revision and AKC transform identity.

## Reference adopter

Dopis is the intended first v1 adopter because AKC already has historical empirical retrieval qualification evidence over a Dopis holdout. That historical evidence does not automatically qualify a new Dopis revision. The adopter must bind an explicit `source.revision`, validate that exact commit, and repeat the required evidence whenever it chooses to repin or otherwise changes the fingerprinted adoption identity or evidence bytes.