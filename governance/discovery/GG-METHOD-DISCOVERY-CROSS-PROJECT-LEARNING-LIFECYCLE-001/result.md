---
work_package_id: GG-METHOD-DISCOVERY-CROSS-PROJECT-LEARNING-LIFECYCLE-001
execution_id: GG-METHOD-DISCOVERY-CROSS-PROJECT-LEARNING-LIFECYCLE-001-RUN-001
status: VALIDATED_PENDING_PROJECT_OWNER_REVIEW
primary_disposition: SPLIT_FRAMEWORK_ADOPTER_CONTRACT_CANDIDATE
general_governance_baseline: 640fb33bc96bff75d757b8325ae6290c1a4e0f2f
formal_input_package_sha256: a57300daf086814204f41bfc1c649525728309b1bd9b30842a606fe32165c71e
---

# Cross-Project Learning Evidence Lifecycle Discovery

## 1. Executive disposition

**Primary disposition: `SPLIT_FRAMEWORK_ADOPTER_CONTRACT_CANDIDATE`.**

The bound evidence demonstrates a real gap between General Governance rc.5's learning intent and the operational lifecycle needed to guarantee that empirical delivery work produces reusable evidence without relying on the Project Owner remembering to request it.

The gap is not that rc.5 lacks learning semantics. The Project Operating Contract already requires material failures, near misses, ambiguities, Owner corrections, defects, tooling gaps and material cost waste to be triaged, and it requires methodology proposals discovered during orchestration to enter durable custody. The demonstrated gap is that rc.5 does not define when the learning obligation must be discharged in the execution lifecycle, and the consumer validator does not prove that the configured learning surface even exists.

The smallest candidate is split across layers:

1. reusable GG semantics define three lifecycle invariants: **capture material learning at event time, declare a learning disposition before packet/work-package terminal closure, and perform one bounded vertical/slice learning closeout**;
2. adopter-owned contracts define their concrete storage/report/packet representations;
3. deterministic checks verify existence, declared dispositions and reference integrity, while causal analysis/generalizability remain judgment.

A direct rc.6 amendment is **not** recommended yet. First pilot this split contract prospectively in SVP Guided Answering and in Dopis, then use the resulting evidence to decide normative adoption.

## 2. Bound evidence and evidence limits

### General Governance

Baseline: `640fb33bc96bff75d757b8325ae6290c1a4e0f2f`.

- `framework/core/project-operating-contract.md` blob `9abe903e6c045fd67c1a061e8dff79fbb076fdd3`, version `0.5.0`.
- `tools/validate_consumer.py` blob `816a94685726bd6aa1d265da18bf7b26cf24754c`.
- Issue #11 and authorization comment `5361498381`.

### Stakeholder Validation Portal

Baseline: `39302e21e4aac26da387d5d3dcd9c00be71c8f1d`.

- `docs/governance/configuration.yaml` blob `985f17b131d90b1290ee06a3a0d5c4fdbf5c7974` declares `docs/governance/learning/README.md`.
- That declared learning README is absent at the bound baseline.
- `AGENTS.md` blob `a2c5b25b765ab38ad6db8774943cc02f464f1a78` requires every modifying work package to preserve one durable report containing attempts, failures, corrections, validation and next gate.
- Packet 03's lease prospectively included its lessons-learned artifact.
- Packet 03 produced both local lessons and a later cross-project learning harvest that successfully routed one GG gap into the bounded replacement-execution discovery that became rc.5.

### Dopis

Baseline: `d8e18eec269924ff89162e6bfcc5b6849cf8e292`.

- `docs/governance/configuration.yaml` blob `3ce402649655c63ea2002dce92d869e40bf0380e` declares the learning README.
- `docs/governance/learning/README.md` blob `35deb69efefd8d72004fc2b5dada5908a3375972` exists.
- Dedicated learning records exist, including `DOPIS-LEARNING-009` blob `1b54ae5a620f6030e2e30a8e47490c7d9a5cec04` and `DOPIS-LEARNING-010` blob `6cd6893d9a688e6bae8b03729b344b40e2fced6c`.
- These records already use a useful causal pattern: observation, impact, cause, containment, correction, prevention, evidence limits and validation plan.

### Evidence limits

This discovery has two adopter patterns, but not enough evidence to define universal risk tiers, numeric review-depth thresholds, token budgets, mandatory telemetry fields or a single repository layout. SVP and Dopis must not be forced into one file structure merely because both need the same lifecycle semantics.

## 3. Current rc.5 coverage

rc.5 already establishes four important foundations:

1. material learning must be preserved instead of silently repaired;
2. completed evidence is immutable and methodology changes prospectively;
3. methodology proposals discovered during orchestration must enter durable custody;
4. `configuration.paths.learning_readme` is an adopter-owned configuration value.

These semantics are necessary and should be preserved.

The consumer validator, however, only requires the configured learning path value to be a non-empty string. It does not establish path existence, discoverability, event capture, packet disposition, vertical closeout, cross-project routing or terminal-learning completeness.

Therefore this discovery does **not** reopen the existing causal-learning record model. It identifies a lifecycle/operationalization gap around it.

## 4. Demonstrated operational gap

The gap is demonstrated by the contrast between the two adopters.

Dopis materializes the configured learning surface and has accumulated dedicated learning records. SVP declares the same configured learning surface but does not materialize it; nevertheless, SVP captured rich learning through packet-specific reports and artifacts, and only Packet 03 later received an explicit cross-project harvest.

This proves two things simultaneously:

- a mandatory single file layout would be wrong, because SVP's report/packet model and Dopis's dedicated-record model both preserve useful evidence;
- a purely declarative `learning_readme` value is insufficient, because an adopter can satisfy the configuration shape without having a complete operational learning lifecycle.

The missing generic lifecycle is:

```text
material event
  -> durable local capture

packet/work-package terminal close
  -> explicit learning disposition

vertical/slice learning closeout
  -> no-cross-project-signal declaration OR one cross-project harvest

cross-project signal
  -> candidate target intake under separate authority
```

## 5. Event-time capture contract

### Trigger

A material learning event requires durable local capture when it is one or more of:

- a failed or indeterminate required gate with reusable causal value;
- an independent-review finding requiring material correction;
- an Owner correction that reveals a method/specification/authority weakness;
- a material near miss;
- a validator/harness false positive or false negative;
- tooling/orchestration failure that distorts execution truth, scope, evidence or authority;
- an authority, scope, currentness or ambiguous-effect stop with reusable implications;
- replacement, recovery or execution-strategy change evidence;
- material context/token/cost waste attributable to the method or tooling;
- a material control that prevented an unsafe or unauthorized effect and therefore supplies confirmatory evidence.

### Non-trigger

Ordinary expected red/green development, a trivial typo, a mechanically corrected formatting error, a harmless warning, or a low-value one-off test failure does not automatically require a durable learning record.

### Minimum semantic record

The adopter must preserve, directly or by durable reference:

- stable local learning identity;
- observation;
- impact;
- causal classification or `UNKNOWN`;
- containment/correction when applicable;
- prevention or follow-up hypothesis;
- evidence references and evidence limits;
- local disposition;
- whether a cross-project signal is claimed and, if so, candidate target(s).

A dedicated file is optional. A qualifying immutable section inside a packet/work-package report may satisfy the same semantic record.

## 6. Packet/work-package closeout disposition

Every governed packet/work package that can produce material execution learning must declare exactly one terminal learning disposition before **governance terminal closure**:

- `NO_MATERIAL_LEARNING`
- `LOCAL_LEARNING_RECORDED`
- `CROSS_PROJECT_SIGNAL_RECORDED`

Rules:

1. `NO_MATERIAL_LEARNING` is an explicit assertion, not absence of a field.
2. `LOCAL_LEARNING_RECORDED` must reference at least one durable local record and asserts that no cross-project candidate is currently claimed.
3. `CROSS_PROJECT_SIGNAL_RECORDED` must reference at least one durable local record carrying one or more candidate target classifications.
4. Material observed events cannot be silently discarded to obtain `NO_MATERIAL_LEARNING`.
5. Product acceptance, merge or deployment are not retroactively invalidated merely because learning closeout is pending; instead the work package remains **governance-not-terminal** until the learning disposition is complete.
6. Learning capture itself does not grant authority to fix the target project.

This gate removes the need for the Project Owner to remember to ask, while keeping the cost of a no-learning packet to one explicit disposition.

## 7. Vertical/slice cross-project harvest

A vertical/slice receives a separate **learning closeout** after its constituent packet/work-package evidence is stable.

Exactly one terminal vertical learning disposition is required:

- `NO_CROSS_PROJECT_SIGNALS`
- `HARVEST_RECORDED`

`NO_CROSS_PROJECT_SIGNALS` is valid only if no constituent packet closed with `CROSS_PROJECT_SIGNAL_RECORDED`.

`HARVEST_RECORDED` must reference exactly one bounded harvest artifact for that vertical/slice. The harvest may aggregate/deduplicate multiple packet records and must not rewrite them.

The harvest is therefore conditional: **every vertical has learning closeout, but only a vertical with cross-project signals pays the cost of a full harvest.**

This is the correct point to generalize because the vertical provides enough context to distinguish repeated/systemic behavior from packet-local accidents while avoiding retrospective reconstruction from chat.

## 8. Classification and target routing

The Packet 03 taxonomy is useful but needs one additional terminal category. Recommended harvest classifications are:

- `CONFIRMATORY_EVIDENCE`
- `ADOPTER_INPUT`
- `GAP_CANDIDATE`
- `LOCAL_PROMOTION`
- `DEPENDENT_FUTURE_INPUT`
- `NOT_GENERALIZABLE`

A harvested item may name more than one candidate target.

Target routing must bind a stable target identity (preferably repository/project identity) and the evidence refs supporting the classification. Routing is **advisory evidence only**. It must not automatically create a target work package, implementation authority, risk acceptance or normative change.

The target project must independently perform intake against its current canonical baseline.

## 9. Deterministic versus judgment boundary

### Deterministic

A repository-controlled checker can establish:

- configured learning discovery surface exists;
- packet/work-package terminal disposition is one allowed enum;
- required referenced local learning identities resolve;
- a `CROSS_PROJECT_SIGNAL_RECORDED` disposition has at least one target-bearing learning ref;
- vertical closeout has one allowed enum;
- `NO_CROSS_PROJECT_SIGNALS` is inconsistent with any constituent cross-project signal;
- `HARVEST_RECORDED` references exactly one existing bounded harvest;
- referenced packet/vertical identities are known;
- historical completed records are not silently replaced in-place.

### Judgment

Human/model judgment remains required for:

- whether an event is materially reusable;
- causal analysis;
- whether several events share one cause;
- whether an observation is local or generalizable;
- classification among confirmatory/adopter/gap/dependent outcomes;
- target-project selection;
- whether evidence is sufficient to propose a normative change.

A deterministic checker must never infer `GAP_CANDIDATE` merely because a test failed.

## 10. Proportionality and anti-bureaucracy controls

1. **Capture early, generalize late.** Preserve causal facts at event time; do not cross-project synthesize every event immediately.
2. **One cause may aggregate many symptoms.** Repeated failures with one demonstrated cause can share one learning record.
3. **Existing durable reports may satisfy the record contract.** Do not force a new file when the adopter already has an appropriate immutable report.
4. **No-learning is cheap.** A packet with no material learning needs only `NO_MATERIAL_LEARNING`.
5. **No-signal vertical is cheap.** It needs only `NO_CROSS_PROJECT_SIGNALS`, not an empty harvest report.
6. **Owner attention is not the capture mechanism.** Routine capture/disposition is operational bookkeeping inside already authorized work; Owner attention is reserved for target intake, methodology changes, risk or other reserved decisions.
7. **Independent review is not required merely because a learning record exists.** Review belongs to the material result/risk or to a later target-project proposal.
8. **Do not duplicate raw evidence.** Records should reference canonical logs, reports, commits and telemetry rather than copy them.

## 11. Framework/adopter layer placement

The evidence supports a split placement.

### Reusable General Governance semantics candidate

L0 should eventually define only:

- the three lifecycle moments: event capture, work-package learning disposition, vertical/slice learning closeout;
- preservation/immutability and no-authority-transfer rules;
- the distinction between local record and cross-project harvest;
- proportionality.

### Adopter-owned contract

Each adopter owns:

- what constitutes its packet/work-package and vertical/slice identities;
- where local learning records live;
- whether a local record is a dedicated file or embedded section;
- how terminal dispositions are represented;
- how its validator discovers constituent packets;
- which candidate target identifiers it permits.

### Configuration/L6 candidate

The existing `configuration.paths.learning_readme` should at minimum resolve to an existing discoverable surface before conformance can claim the learning path is usable.

Future L6 support may validate terminal disposition/reference integrity, but the pilot should first determine whether this belongs in GG generic helpers or adopter-local validators.

### Issue #11 question answers

1. **Event trigger:** material causal/authority/evidence/tooling/near-miss/cost/control events; not ordinary noise.
2. **Packet closeout:** yes, require one explicit terminal learning disposition.
3. **Vertical closeout:** yes, require one learning closeout; full harvest only when cross-project signals exist.
4. **Taxonomy:** six harvest classifications listed in §8.
5. **Target routing:** candidate identity + evidence only; no authority transfer.
6. **Storage:** semantic surfaces are required, exact file layout is adopter-owned.
7. **Machine enforcement:** existence/enums/reference consistency deterministic; causal/generalization classification judgment.
8. **Cost:** material-only triggers, deduplication, reuse existing reports, conditional harvest.
9. **Adopter compatibility:** contract semantics fit both SVP packet reports and Dopis dedicated records without structural convergence.
10. **Framework placement:** split L0 invariants + adopter representation + possible L6 deterministic helper.

## 12. Counterexample tests

| Case | Expected outcome |
|---|---|
| A unit test fails once during normal TDD and is immediately corrected with no reusable cause | No durable learning record required. |
| Independent review finds a validator accepts a vocabulary forbidden by its contract | Material local learning record required; possible cross-project signal only after causal assessment. |
| Five failures are all caused by one stale fixture | One aggregated learning record with five evidence refs is sufficient. |
| Packet finishes cleanly with no material learning | `NO_MATERIAL_LEARNING`; no learning file required. |
| Packet records a product-local defect with no plausible reusable target | `LOCAL_LEARNING_RECORDED`, later harvest not required for that item. |
| Packet records a governance lifecycle ambiguity also relevant to GG | `CROSS_PROJECT_SIGNAL_RECORDED` with GG as candidate target; no GG authority created. |
| Vertical has three packets and none signals cross-project learning | `NO_CROSS_PROJECT_SIGNALS`; no empty harvest report. |
| Vertical has one or more cross-project signals | Exactly one harvest before vertical learning closeout. |
| Product is already accepted but learning disposition was omitted | Accepted product remains accepted; governance terminal closure remains incomplete until disposition is recorded. |
| Harvest classifies a GG gap | Separate GG intake/discovery authority is still required before any GG change. |

All cases preserve the distinction between evidence capture and authority.

## 13. Minimal pilot for SVP and Dopis

A prospective pilot should run **before** changing rc.5.

### SVP Guided Answering

Use `SVP-STAGE2A-GUIDED-ANSWERING-001` ST-01/ST-02/ST-03 as one pilot vertical:

- materialize a discoverable SVP learning surface;
- add one terminal learning disposition to each implementation packet/work package;
- allow packet reports or dedicated learning records to satisfy local capture;
- require one vertical learning closeout after ST-01/ST-03 evidence is stable;
- create a full harvest only if at least one packet records a cross-project signal.

### Dopis

Use the next bounded implementation vertical(s):

- preserve the existing `DOPIS-LEARNING-*` model;
- add the same semantic packet/work-package disposition without changing the dedicated-record format;
- perform one vertical learning closeout with the same conditional-harvest rule.

### Pilot measurements

Preserve only actual observed values:

- number of material events;
- number of learning records;
- number of grouped/deduplicated events;
- packet terminal dispositions;
- cross-project signals and target candidates;
- full harvest count;
- false-trigger/noise cases;
- Owner reminders/interventions required solely to obtain learning;
- evidence lost or reconstructed retrospectively;
- material governance effort attributable to the lifecycle.

The pilot succeeds if neither adopter depends on the Owner remembering to request learning capture/harvest, while record volume remains proportional.

## 14. What is explicitly not being changed

This discovery does not:

- modify rc.5 or any normative file;
- modify the consumer schema or validator;
- change SVP or Dopis;
- require every failure to become a durable record;
- impose one shared repository layout;
- create risk tiers or review-depth tiers;
- make AET mandatory for learning capture;
- automatically create target-project issues/work packages;
- grant target-project implementation authority;
- open a PR, merge, release, tag or rc.6 package.

## 15. Recommended next decision

Authorize a **prospective cross-adopter pilot contract**, not a normative rc.6 amendment.

Suggested next work identity:

`GG-METHOD-PILOT-CROSS-PROJECT-LEARNING-LIFECYCLE-001`

The pilot should define the minimum semantic contract above and then create separately bounded adopter implementation work in SVP and Dopis. It should preserve rc.5 unchanged.

After the SVP Guided Answering vertical and at least one Dopis vertical have exercised the pilot, perform one bounded pilot evaluation. Only then decide among:

- promote the lifecycle into a normative GG clarification / successor release;
- keep only selected deterministic adopter tooling;
- revise the contract and collect more evidence;
- reject the reusable lifecycle.

This sequence directly addresses the demonstrated problem—Owner-memory dependence—without prematurely hardening the current hypothesis into General Governance.
