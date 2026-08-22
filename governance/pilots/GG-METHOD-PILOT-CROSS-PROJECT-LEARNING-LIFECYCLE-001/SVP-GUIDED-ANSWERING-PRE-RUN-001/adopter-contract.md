---
package_id: GG-METHOD-PILOT-CROSS-PROJECT-LEARNING-LIFECYCLE-001-SVP-GA-PRE-RUN-001
pilot_id: GG-METHOD-PILOT-CROSS-PROJECT-LEARNING-LIFECYCLE-001
status: NON_NORMATIVE_PILOT_CANDIDATE
adopter: Sugar144/stakeholder-validation-portal
vertical: SVP-STAGE2A-GUIDED-ANSWERING-001
packet: SVP-STAGE2A-GUIDED-ANSWERING-PACKET-01-C2
---

# SVP adopter contract — cross-project learning lifecycle pilot

## 1. Ownership boundary

General Governance owns only the pilot semantics in this package. SVP owns the adopter projection and all empirical evidence it produces.

This contract is a non-normative pilot. It does not amend General Governance rc.7 and does not change Guided Answering requirements, architecture, or ST-01 product scope.

No cross-project learning signal transfers execution, implementation, acceptance, publication, merge, release, deployment, risk, retry, replacement, or normative authority to any target project.

## 2. Exact adopter identity

The prospective adopter packet is:

- repository: `Sugar144/stakeholder-validation-portal`;
- vertical: `SVP-STAGE2A-GUIDED-ANSWERING-001`;
- packet: `SVP-STAGE2A-GUIDED-ANSWERING-PACKET-01-C2`;
- branch: `implementation/stage2a-guided-answering-st01-c2`;
- reported preparation HEAD: `280aab9c202394cca4107c3ac3df0885be6a9164`;
- evidence class for that HEAD: `OWNER_REPORTED_LOCAL_UNPUBLISHED`;
- C2 WPDC: `VALID_DEPENDENCY_CLOSED`;
- independent Reviewer: `PASS`;
- local coordination start gate: `CLEAR`;
- functional ST-01 implementation: `NOT_STARTED`.

The C2 SHA is not remotely resolvable from the GitHub surface available to this GG package. SVP must verify it locally before use. Any different HEAD requires explicit rebinding or a fresh adopter-package currentness disposition; it must not be silently substituted.

Abandoned C1 product implementation is not a product implementation source for C2. Historical C1 evidence remains historical evidence only.

## 3. Material event-time capture

Capture a learning event when the event has reusable causal value, including material required-gate failure/indeterminacy, material independent-review finding, Owner correction revealing a method or authority weakness, near miss, validator/harness false positive or negative, tooling/orchestration failure affecting execution truth, scope/currentness/ambiguous-effect stop, replacement/recovery/strategy-change evidence, material method/tooling cost waste, or a material control that prevented an unsafe or unauthorized effect.

Do not create a durable learning event merely for ordinary expected TDD red/green cycles, trivial typos, harmless warnings, mechanical formatting corrections, or one-off low-value failures.

Existing truthful packet/work-package reporting may satisfy event-time capture. A dedicated per-event file is not required.

## 4. Packet terminal disposition

Before governance-terminal closure of C2, the packet report must declare exactly one:

- `NO_MATERIAL_LEARNING`;
- `LOCAL_LEARNING_RECORDED`;
- `CROSS_PROJECT_SIGNAL_RECORDED`.

`LOCAL_LEARNING_RECORDED` and `CROSS_PROJECT_SIGNAL_RECORDED` must reference durable evidence. `CROSS_PROJECT_SIGNAL_RECORDED` must name candidate target project(s) but creates no authority there.

The same semantic rule is intended for later Guided Answering packets, but each later packet must enter the pilot through its own current bounded adopter identity/write surface rather than inheriting C2 execution authority.

## 5. Vertical learning closeout

At learning closeout of `SVP-STAGE2A-GUIDED-ANSWERING-001`, record exactly one:

- `NO_CROSS_PROJECT_SIGNALS`; or
- `HARVEST_RECORDED`.

A full cross-project harvest is required if and only if one or more constituent governed packets recorded `CROSS_PROJECT_SIGNAL_RECORDED`. The harvest aggregates and classifies existing evidence; it must not rewrite packet evidence or reconstruct missing history as if it were contemporaneous.

## 6. Authorized SVP pilot write surface

This GG package defines the maximum candidate SVP pilot surface. It does not itself perform or authorize the mutation; the separately authorized SVP adopter package must bind and apply it prospectively.

1. `docs/governance/learning/README.md` — create if absent; discoverable learning surface/index only.
2. `docs/governance/learning/GG-METHOD-PILOT-CROSS-PROJECT-LEARNING-LIFECYCLE-001.yaml` — adopter-owned prospective pilot binding.
3. `reports/work-packages/SVP-STAGE2A-GUIDED-ANSWERING-PACKET-01-C2.md` — C2 event-learning references, pilot measurements, and terminal learning disposition only.
4. `reports/work-packages/SVP-STAGE2A-GUIDED-ANSWERING-LEARNING-CLOSEOUT-001.md` — exactly one vertical learning closeout, created only at vertical closeout.
5. `reports/work-packages/SVP-STAGE2A-GUIDED-ANSWERING-CROSS-PROJECT-LEARNING-HARVEST-001.md` — conditional; create only when at least one packet recorded a cross-project signal.

The SVP adopter package may narrow this surface. Widening it requires new authority.

## 7. Measurements

Preserve only actual observations. Do not invent unavailable counts, time, token, or cost data.

Measure:

- packet learning disposition;
- number/type of material learning records;
- cross-project signals and candidate targets;
- material learning discovered only retrospectively;
- whether Owner prompting/reminding was needed to trigger capture or harvest;
- noise/duplicates avoided when observable;
- lifecycle/reporting friction;
- ambiguity over materiality;
- deterministic checks found useful or overly rigid.

## 8. Pre-run validation and stop conditions

Before any future C2 empirical/implementation execution crosses its separately authorized boundary, SVP must establish:

- local HEAD equals `280aab9c202394cca4107c3ac3df0885be6a9164`, or an explicit rebinding has been accepted before use;
- current branch identity is `implementation/stage2a-guided-answering-st01-c2`;
- C2 remains `VALID_DEPENDENCY_CLOSED`;
- independent Reviewer remains `PASS`, or a material packet change has been re-reviewed under applicable governance;
- coordination start gate remains `CLEAR`;
- the adopter pilot projection is already materialized prospectively;
- the separately governed AET-P4 and P5B pre-run dependencies are integrated;
- future Claude Agent SDK RUN-001 has an exact component set and separate prospective Owner authorization.

STOP on any baseline/currentness drift, WPDC/review/coordination regression, product/architecture/write-surface drift, attempt to combine the AET-P4 or P5B authorities into this package, attempt to infer RUN-001 authority, or need to fabricate/reconstruct learning evidence.

## 9. Integration boundary

This GG-side candidate requires separate publication/integration authority before it can become an accepted `main`-reachable GG pilot reference for SVP.

No SVP mutation and no C2 RUN-001 is authorized by this artifact.
