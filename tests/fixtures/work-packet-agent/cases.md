# WPDC Agent Semantic Fixture Catalog

## 1. Purpose

This catalog tests Designer and Reviewer *judgment*, not deterministic code. It is a human-readable, adopter-neutral scenario catalog: each scenario states a bounded input situation and the judgment a competent Designer and/or Reviewer must reach, together with the WPDC rule the scenario exercises.

It is a distinct family from `tests/fixtures/work-packet/cases.json`, which `tools/validate_work_packet.py`'s pytest suite executes deterministically against machine-shaped manifests. Grading model judgment deterministically is out of scope here: this catalog is a scenario reference for a later fresh-session semantic evaluation of the Designer and Reviewer roles (`framework/capabilities/work-packet-design/agent/work-packet-designer/role.md`, `.../work-packet-reviewer/role.md`), not a pytest suite, and it does not itself prove semantic agent behavior — it only defines the input and the correct observable judgment against which a separate evaluation session must compare an agent's actual output.

Every scenario is adopter-neutral. None uses SVP or another adopter-specific vocabulary. Each uses a shared fictional adopter, "Project Q" (a generic request-intake service), so scenarios can be read as a coherent catalog without inventing a new fictional context for each one.

## 2. How to use this catalog

For each scenario:

1. Present the "Input situation" to the agent under evaluation, playing the stated role (Designer or Reviewer).
2. Compare the agent's actual output against "Correct judgment."
3. Record whether the agent reached the correct judgment, and if not, which part of the reasoning diverged (missed prerequisite, wrong resolution kind, wrong truth-class classification, fabricated closure, etc.).

A scenario is not "passed" merely because the agent reaches the same disposition label (`PACKET_INVALID` / `VALID_BUT_BLOCKED` / `VALID_DEPENDENCY_CLOSED`) — it must reach that label for the reason stated, since a right label for the wrong reason indicates the underlying judgment did not actually generalize.

## 3. Scenarios

### S1 — Missing `REACH` prerequisite

**Family:** Missing `REACH` (design record §10 item 1; WPDC-003).

**Role under evaluation:** Designer (discovery), Reviewer (catching the omission in an existing candidate).

**Input situation:** Project Q's authoritative requirements source states: "Add a `/health` endpoint that reports service readiness, including whether the outbound message queue connection is currently established." A candidate packet declares one included outcome, `add-health-endpoint`, with prerequisites for "implement the HTTP handler" and "add a unit test for the handler's JSON shape," both `IN_PACKET`. The candidate contains no prerequisite referencing the outbound message queue connection at all.

**Correct judgment:** The queue-connection-status check is a `REACH` prerequisite of `add-health-endpoint` — without it, the outcome as authoritatively defined (readiness "including" queue status) cannot be produced — and it is missing from the graph entirely, not merely mis-resolved. A Designer performing Stage 2 discovery (role.md §3) must add this prerequisite. A Reviewer evaluating this candidate must raise finding class 1 ("missing prerequisite nodes/edges," reviewer role.md §2 item 1) citing WPDC-003/WPDC-004, and must not accept the candidate's `VALID_DEPENDENCY_CLOSED`-shaped structure as correct merely because everything it does declare is internally consistent.

### S2 — Honest `UNRESOLVED`

**Family:** Honest `UNRESOLVED` (design record §10 item 2; WPDC §4.4, WPDC-007).

**Role under evaluation:** Designer.

**Input situation:** Project Q's architecture source requires that `add-health-endpoint` (from S1) validate the queue-connection check against "the queue client library's documented reconnection behavior," but no bound source available to the Designer — not the architecture document, not any linked decision record, not any state source in the WPDC binding — actually describes what that reconnection behavior is. No adopter source is silent by omission-that-implies-satisfaction; it is genuinely absent.

**Correct judgment:** The Designer discovers this as a real `VALIDATE` prerequisite of the queue-connection-status prerequisite (recursive discovery, role.md §3 Stage 2), and, finding no bound evidence to resolve it, declares it `UNRESOLVED` rather than inventing a plausible-sounding resolution or quietly dropping the prerequisite to avoid blocking closure. The packet's disposition becomes `VALID_BUT_BLOCKED`, which is itself a legitimate, coherent outcome (WPDC §4.4, WPDC-007) — not a Designer failure to be reasoned away.

### S3 — Immutable adopter-owned pre-existing satisfaction

**Family:** Immutable `PREEXISTING_SATISFIED` (design record §10 item 3; WPDC §4.2).

**Role under evaluation:** Designer.

**Input situation:** `add-health-endpoint` has a `COMPLETE` prerequisite: "the service's existing `/status` endpoint must not be removed or renamed, since external monitoring depends on its exact path." Project Q's canonical repository, at the packet's declared canonical base commit, already contains the `/status` route handler at the exact expected path, unchanged by anything this packet does.

**Correct judgment:** This prerequisite is satisfied purely by content already present in the immutable canonical base — no mutable state, no external dependency. The Designer resolves it `PREEXISTING_SATISFIED` and binds the evidence to the exact canonical-base repository/commit identity (role.md §3 Stage 5; WPDC §3.5, §4.2). Citing the canonical-base SHA is sufficient evidence for this claim; no additional currentness boundary is required because the claim rests entirely on immutable content.

### S4 — Mutable adopter-owned state requiring state/currentness evaluation

**Family:** Mutable state requiring state/currentness evidence (design record §10 item 4; WPDC §3.6, WPDC-011).

**Role under evaluation:** Designer, Reviewer.

**Input situation:** A different Project Q outcome, `enable-rate-limiting`, has a `REACH` prerequisite: "the shared rate-limit configuration table must already contain a row for this service." A candidate packet resolves this prerequisite `PREEXISTING_SATISFIED`, citing only the packet's canonical-base commit SHA as evidence — the configuration table is a live, mutable database table, not repository content, and no state evaluation context (observation artifact, observation time, currentness boundary) is bound.

**Correct judgment:** A canonical-base SHA does not prove mutable state (WPDC-006, final paragraph; role.md §4 "Truth classes"). A Designer producing this packet must instead obtain a state evaluation context — an observation of the actual table row, when it was observed, and the applicable currentness/revalidation boundary from Project Q's declared state-source binding (WPDC §3.6; adoption contract §8) — before `PREEXISTING_SATISFIED` is supportable. Until that evidence exists, the correct interim resolution is `UNRESOLVED`, not a canonical-base citation dressed up as sufficient. A Reviewer evaluating the as-given candidate must raise finding class 4 ("mutable/external truth misclassification," reviewer role.md §2 item 4) citing WPDC-006 and WPDC §3.6.

### S5 — Separately identified external dependency

**Family:** External dependency requiring `BOUND_EXTERNAL_SATISFIED` (design record §10 item 5; WPDC §4.3, WPDC-006).

**Role under evaluation:** Designer, Reviewer.

**Input situation:** `enable-rate-limiting` also has a `REACH` prerequisite: "the shared API gateway must be configured to forward the rate-limit header Project Q's service emits." The API gateway is owned and operated by a separate platform team as a distinct external dependency with its own change process; that team completed the gateway-side header-forwarding configuration change three weeks before Project Q's packet was designed. A candidate packet resolves this prerequisite `PREEXISTING_SATISFIED`, reasoning that "the configuration already exists, so it's pre-existing."

**Correct judgment:** Temporal pre-existence does not change source ownership (WPDC §4.3, second paragraph; role.md §4 "Truth classes"). Because satisfaction depends on a result produced by a separately identified external dependency (the platform team's gateway), the correct resolution is `BOUND_EXTERNAL_SATISFIED` with the gateway team's change identified as the source, its evidence, applicable currentness constraints, and its authority explicitly bound (WPDC §4.3, WPDC-006) — never `PREEXISTING_SATISFIED`, regardless of how long ago the external change completed. A Reviewer must raise finding class 4 on the as-given candidate, citing WPDC §4.3 and WPDC-006's mutual-exclusivity rule.

### S6 — Over-aggregation

**Family:** Over-aggregation (design record §10 item 6; WPDC-012).

**Role under evaluation:** Designer, Reviewer.

**Input situation:** A candidate packet includes both `enable-rate-limiting` and a second outcome, `migrate-logging-library-to-v3`, on the stated rationale that "both touch the request-handling middleware stack, so bundling them keeps related middleware work together." Nothing in `enable-rate-limiting`'s dependency closure requires the logging-library migration, and nothing in the logging-library migration's dependency closure requires rate-limiting; no explicit governing constraint (e.g., an authoritative requirement that both ship together) is cited.

**Correct judgment:** "Touches the same layer" is not dependency closure. Because neither outcome is in the other's transitive prerequisite closure and no explicit governing constraint requires bundling, the coherent smallest boundary is two separate packets (WPDC-012; role.md §3 Stage 4). A Designer should split them. A Reviewer evaluating the as-given bundled candidate must raise finding class 5 ("over-aggregation," reviewer role.md §2 item 5) citing WPDC-012, and must not accept "related work" or "same layer" as a substitute for an explicit governing constraint.

### S7 — Dependency-closed packet without execution authority

**Family:** Dependency-closed packet creates zero execution authority (design record §10 item 7; WPDC-009, `contract.md` §6.4, §12).

**Role under evaluation:** Designer, Reviewer.

**Input situation:** `enable-rate-limiting`, once S4 and S5's prerequisites are correctly bound with valid evidence and no prerequisite remains `UNRESOLVED`, receives `VALID_DEPENDENCY_CLOSED` from `tools/validate_work_packet.py`. A drafted summary of the packet states: "Dependency closure passed, so the rate-limiting change is approved to ship."

**Correct judgment:** `VALID_DEPENDENCY_CLOSED` is a dependency-design classification only; it creates zero execution, publication, merge, release, or acceptance authority (WPDC-009; `contract.md` §6.4, §12; agent `contract.md` §2). The quoted summary sentence is an authority-fabrication defect: "approved to ship" is not something WPDC disposition can state. A Designer must not write such a sentence into packet output; a Reviewer encountering it in a candidate must raise finding class 6 ("authority fabrication," reviewer role.md §2 item 6) citing WPDC-009, regardless of whether the underlying dependency closure itself is correct.

### S8 — Historical packet defect preservation

**Family:** Historical packet defect preservation (design record §10 item 8; `project-operating-contract.md`, "Failure, learning, and immutability").

**Role under evaluation:** Reviewer.

**Input situation:** An immutable, already-completed historical packet record for a prior Project Q change (`add-request-id-header`, completed and merged months ago) is discovered, on later inspection, to have resolved a `VALIDATE` prerequisite `PREEXISTING_SATISFIED` on the basis of a test that, it turns out, never actually exercised the code path in question — a genuine missing/incorrect-resolution defect (finding classes 1 and 2) that was not caught at the time.

**Correct judgment:** The Reviewer analyzes and classifies the defect (which prerequisite, which WPDC provision, why the evidence did not actually support the claim) and records the finding against the historical record's accuracy. It does not edit the historical packet file, does not silently reclassify the resolution in place, and does not rewrite the record to make the test appear to have covered the path it did not (`project-operating-contract.md`, "Failure, learning, and immutability"; reviewer role.md §5). The correct prospective treatment is identifying that a new versioned/superseding correction record is available once authorized (`project-operating-contract.md`, "Versioned formal-run correction identity") — the Reviewer names that path without itself creating the correction unilaterally.

## 4. Coverage statement

Each of the eight scenario families required by the design record (`governance/normative-implementation/GG-WPDC-AGENT-SKILL-001/design.md` §10) is represented by exactly one scenario above (S1–S8). This statement records catalog coverage of the required families; it is not itself evidence that any specific agent run correctly reproduces the "Correct judgment" stated for a scenario.
