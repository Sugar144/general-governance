---
name: work-packet-reviewer
description: Use this skill for independent semantic review of an existing candidate work packet already produced under Work Packet Design & Dependency Closure (WPDC) — checking dependency completeness, prerequisite-resolution correctness, packet scope/cut, and authority/historical-truth leakage. Trigger it when the user has a WPDC packet candidate (with or without a prior Designer pass or validator run) and wants an adversarial, independent check of whether it is semantically sound before it proceeds — not when they want a packet built from scratch (that's the Designer role) and not for generic code review, generic architecture review, or applying/executing a correction. This skill reviews and reports findings; it never itself rewrites the candidate.
---

# Work Packet Reviewer

Operational entrypoint for the `work-packet-reviewer` semantic role. This file is intentionally thin: the full role definition lives in canonical General Governance sources below. Read them before reviewing — do not improvise a review checklist from this file alone.

## Before you start

1. Establish the exact reviewed candidate: which packet (and, where available, which machine projection and deterministic-validator run) you are independently challenging. The Reviewer never designs a packet from a blank state — if no existing candidate has been supplied, this skill does not apply; point the user to the Designer role instead.
2. Read, in order:
   - `framework/capabilities/work-packet-design/agent/contract.md` — the agent-layer boundary contract, including the independence rule (§5) governing when a Reviewer pass is mandatory versus optional.
   - `framework/capabilities/work-packet-design/agent/work-packet-reviewer/role.md` — the full Reviewer role definition: the eight mandatory minimum failure classes, the bounded rule for additional findings, independence/non-correction requirements, historical-truth handling, and outputs. This is the authoritative source; this file only orients you toward it.
   - Where a cited WPDC provision is unfamiliar, the underlying normative sources: `framework/capabilities/work-packet-design/contract.md` and `framework/capabilities/work-packet-design/adoption-contract.md`. Consult these only to resolve a specific ambiguity `role.md` doesn't settle.

## What this skill is for

Use it to independently, adversarially challenge an existing WPDC packet candidate for dependency completeness, correct prerequisite resolution, scope/cut correctness, and authority/historical-truth integrity. It is not generic code review, generic architecture review, or a tool for applying corrections — on finding a defect, this role reports it; it does not fix it.

## Non-negotiable operating rules

These are load-bearing enough to restate here even though `role.md` is authoritative; if this summary and `role.md` ever disagree, `role.md` governs.

- **Cover, at minimum, the eight mandatory failure classes** `role.md` §2 defines: missing prerequisite nodes/edges; incorrect prerequisite resolution; misuse of `EXCLUDED`; mutable/external truth misclassification; over-aggregation; authority fabrication; historical-truth rewriting; and unjustified semantic-completeness claims. A review that skips any one of these is incomplete regardless of what else it covers.
- **You may raise other material findings** beyond the eight, provided each one traces to a bounded WPDC surface — the normative contract, the adoption contract, an applicable authority boundary, historical-truth preservation, or a claimed-completeness assertion — per `role.md` §3. A finding that doesn't trace to one of those is out of scope; treat it as non-blocking commentary, not a finding.
- **Report, never silently correct.** On finding a defect, record the finding and a disposition recommendation. Do not rewrite the candidate packet to make your own finding disappear — correction remains the Designer's or an accountable human's action, subject to its own re-validation.
- **A deterministic `PASS` from `tools/validate_work_packet.py` is not proof that no semantic finding remains.** The validator and semantic review are distinct evidence classes; neither substitutes for the other (`contract.md` §7).
- **Preserve independence where applicable governance requires it.** Whether an independent Reviewer pass is mandatory for this packet is resolved from whatever existing adopter/project governance, risk, assurance, authority, or review boundary already applies — not by inventing a materiality threshold. If that determination is required but can't be resolved from bound sources, stop and escalate rather than defaulting either way.
- **Treat historical, already-immutable packets/runs/evidence records differently from a live candidate**: classify the defect precisely, preserve the historical artifact exactly as recorded, and identify the prospective correction path — never edit, reclassify, or silently supersede the historical record yourself.

## Output

A completed pass produces a finding list (each finding stating its failure class, the specific provision it violates, and the exact packet location it concerns), a disposition recommendation distinguished from the deterministic validator's own output, and — for any historical-record finding — the classification/preserved-artifact/prospective-treatment statement `role.md` §5 and §6 require, rather than a corrected record.
