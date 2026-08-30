# GG-WPDC-DESIGNER-HARDENING-001

Date: 2026-08-30
Status: ACTIVE_CANDIDATE_HARDENING
Source adopter: `Sugar144/dopis`
Source packet lineage: `DOPIS-WP-VS-ORDERING-001-001` → `DOPIS-WP-VS-ORDERING-001-002`

## Incident

A real bounded Dopis WPDC adoption exposed a repeatable weakness in the canonical Work Packet Designer procedure. The initial Designer candidate passed deterministic Stage 7 and its own Stage 8 self-challenge, but the independently bound Reviewer later found material omissions in prerequisite discovery and graph representation.

The material classes were:

1. local prerequisite work required to consume owner/external seams was collapsed into unresolved owner-state prerequisites instead of being represented separately as `IN_PACKET` adapters, ledgers, records, and schema invariants;
2. a known frontend-to-runtime reachability edge was omitted;
3. the validation environment did not declare reachability to every runtime/frontend/persistence surface required by the bound acceptance sources;
4. the Stage 8 no-finding wording was too easy to read as a completeness warrant even though WPDC-003 forbids such a claim.

The corrected successor represented those obligations explicitly and passed a fresh deterministic validation, bounded Stage 8 self-challenge, and independent Reviewer pass.

## Cause

The existing Designer role correctly required recursive `REACH`/`VALIDATE`/`COMPLETE` discovery, but did not force four concrete cross-checks that make common omissions visible before machine projection:

- separate local seam-consumption work from external/owner authoritative state;
- trace every declared execution/effect/persistence surface to a producing prerequisite node;
- verify integration edges between declared client/frontend and runtime/API surfaces;
- prove that each validation surface can reach every runtime/frontend/persistence prerequisite needed to execute the validation method.

Stage 8 also required a missing-dependency challenge but did not constrain the no-finding wording strongly enough to prevent a result label that could be mistaken for semantic completeness evidence.

## Prevention

The rc.9 candidate hardens the canonical Designer role and skill with mandatory cross-checks for those four patterns and adds a release-included regression qualification. The qualification must fail if those controls disappear or if Stage 8 regresses to completeness-warrant wording.

This hardening does not change WPDC resolution enums, manifest schema, deterministic validator semantics, execution authority, or the normative WPDC contract version. It is a compatible strengthening of the semantic-role procedure.

## Historical truth

The accepted `0.1.0-rc.8` release identity remains immutable and is not amended. This hardening is prospective and must be carried by a new release-content identity (`0.1.0-rc.9` candidate) before any adopter can bind to it.
