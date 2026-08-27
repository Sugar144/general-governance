---
prompt_id: GG-MP-0014
version: 1.0.0
mode: BOUNDED_ARCHITECTURE_CANDIDATE_CORRECTION
status: APPROVED_FOR_SINGLE_EXECUTION
---

# Material prompt — cross-project execution identity candidate correction

## Exact Project Owner instruction

`adelante te autorizo`

## Resolved authorization context

The instruction authorizes exactly the correction action proposed immediately before it: produce one corrected architecture candidate on branch `architecture/cross-project-execution-identity`, preserving predecessor candidate commit `e3d198fe6857babad573e3a0a2c610124d3dc6cf` as historical evidence after review verdict `CHANGES_REQUIRED`.

The correction is limited to resolving the six identified review findings:

1. `EXEC` must not require every execution to belong to an Implementation Packet; packet binding is optional generically and mandatory only for implementation-packet executions.
2. Replace the new generic `Semantic Outcome` term with `Semantic Intent` so it does not collide with WPDC's existing normative `declared outcome`; use `intent_refs` for upstream semantic intent references.
3. Permit `PKT -> 0..N EXEC` so a packet can exist before any executable specification is created.
4. Define Attempt identity at invocation/admission lifecycle entry rather than only after execution/provider boundary crossing; boundary crossing becomes evidence/state of an Attempt.
5. Preserve existing GG formal-run correction identity `<BASE_RUN_ID>-R<N>` and state explicitly that correction, recovery, replacement, and retry are distinct semantics.
6. Rename `Execution Scope` to `Identity Scope` and state explicitly that scope membership grants no execution authority.

Also make explicit that `REV != RUN`; a formal review may be produced by a RUN through an explicit typed relation.

## Authorized write surface

Exactly:

- `docs/architecture/cross-project-execution-identity.md`
- this material-prompt custody record

## Required preservation

- Preserve artifact identity `GG-STANDARD-CROSS-PROJECT-EXECUTION-IDENTITY-001`.
- Preserve identity schema family `gg.execution-identity/v1` as a proposed semantic schema name; no machine schema is authorized.
- Preserve historical accepted identities without retroactive renaming or reinterpretation.
- Preserve WPDC `work packet` and `declared outcome` semantics; this correction must not modify WPDC artifacts.
- Preserve the existing Project Operating Contract correction identity `<BASE_RUN_ID>-R<N>`; this correction must not modify L0.
- Preserve predecessor candidate commit `e3d198fe6857babad573e3a0a2c610124d3dc6cf` as the immutable reviewed predecessor.

## Forbidden actions

Do not modify AEC, SVP, Dopis, OPD, WPDC, the GG learning lifecycle, schemas, validators, runtime code, or release surfaces.

Do not create a pull request, merge, release, tag, publish, deploy, or claim Owner acceptance.

Stop after producing an exact corrected candidate ready for a fresh review.
