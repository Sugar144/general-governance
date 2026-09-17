# General Governance — Capabilities

This document explains, in plain language, what the General Governance framework provides and what problem each reusable capability solves.

General Governance is not a product application. It is a reusable set of governance contracts, schemas, validators and optional capabilities that other repositories can adopt without copying their own incompatible governance rules.

## How to read this document

Each capability explains **what it does**, **the problem it solves**, **an example**, **its limits**, and the **technical references** for deeper inspection.

## Capability: Shared project-governance vocabulary and core semantics

**What it does.** General Governance defines common concepts for project identity, authority, evidence, state, decisions and controlled transitions so different repositories can use the same basic governance language.

**Problem it solves.** If every project invents its own meaning for words such as "authorized", "accepted", "current", "evidence" or "closed", cross-project coordination becomes ambiguous and agents can easily treat one project's status as equivalent to another's when it is not.

**Example.** Two repositories can both adopt the same framework semantics for distinguishing implementation authority from merge or acceptance authority, while still keeping their own project-specific decisions and state.

**Limits.** The framework does not decide a project's business requirements or grant project-specific authority. Adopters still own their concrete values, decisions, evidence and state.

**Technical references.** `framework/core/`, framework release documentation, `docs/consumer-contract.md`.

## Capability: Versioned consumer adoption and immutable pinning

**What it does.** A consuming repository can pin an exact General Governance release and upgrade intentionally rather than silently following whatever happens to be newest.

**Problem it solves.** Governance rules are part of a project's operating contract. If they change automatically underneath a project, the meaning of its existing evidence and workflows can change without an explicit decision.

**Example.** Dopis can lock one exact GOV-GEN revision and validate against it. A later framework release may exist, but Dopis does not adopt it until its own upgrade process says so.

**Limits.** Publishing a framework release does not activate it in every consumer. Adoption is always an adopter-owned action.

**Technical references.** `docs/consumer-contract.md`, release/version surfaces and adopter binding contracts.

## Capability: Compose optional governance capabilities

**What it does.** The framework supports optional capability modules that can be added to a consumer only when needed, instead of forcing every project to adopt every governance mechanism.

**Problem it solves.** A small project and a multi-agent programme do not need identical process complexity. A monolithic governance framework would either be too weak for complex projects or too heavy for simple ones.

**Example.** A consumer can adopt Work Packet Design without necessarily enabling the Hierarchical Work Graph capability, or can later add HWG through its explicit configuration binding.

**Limits.** Presence of a capability in a General Governance release does not mean a consumer has adopted it. Each optional capability has its own adoption contract.

**Technical references.** `framework/capabilities/`, capability adoption contracts, consumer configuration schema.

## Capability: Work Packet Design & Dependency Closure (WPDC)

**What it does.** WPDC provides a reusable way to turn a meaningful unit of work into a bounded packet with explicit objective, inputs, dependencies, authority, write/effect surface, validation, stop conditions and evidence expectations.

**Problem it solves.** AI-assisted work often fails because tasks are either too vague ("implement the feature") or overloaded with unrelated responsibilities. A bounded work packet makes it possible for a fresh execution session to understand exactly what result it is responsible for and what it must not do.

**Example.** A feature can be represented as several packets where one packet produces a schema, another depends on that schema to implement runtime code and a later packet performs independent validation.

**Limits.** A well-formed packet does not itself grant authority or prove that its proposed design is correct. Adopter-specific approval and execution remain separate.

**Technical references.** `framework/capabilities/work-packet-design/contract.md`, `framework/capabilities/work-packet-design/adoption-contract.md`, `docs/architecture/work-packet-design-dependency-closure.md`.

## Capability: Work-packet designer and reviewer agent guidance

**What it does.** The framework includes reusable agent-facing guidance for designing a packet from accepted inputs and independently reviewing an existing packet for gaps or unsafe assumptions.

**Problem it solves.** Even with a packet schema, an AI agent can create a structurally valid but semantically poor packet—for example, missing a dependency or combining unrelated authority boundaries. Dedicated roles make the design/review responsibilities explicit.

**Example.** A designer can produce a packet candidate from a project's accepted source material, while a separate reviewer checks that candidate without redesigning the whole project from scratch.

**Limits.** These skills assist bounded reasoning; they do not replace Owner decisions, project-specific architecture or deterministic validation.

**Technical references.** `framework/capabilities/work-packet-design/agent/`, designer/reviewer `SKILL.md` files and agent contract.

## Capability: Hierarchical Work Graph (HWG)

**What it does.** HWG represents work at several levels—such as an overall product outcome, the work packets that contribute to it and the smaller execution units inside those packets—while preserving exact parent/child and dependency relationships.

**Problem it solves.** Large plans become difficult to manage when everything is flattened into one huge list. At the same time, generating every tiny task upfront creates stale planning and large context payloads. HWG lets work be expanded progressively as its parent context becomes stable.

**Example.** A product outcome can contain several work packets; one packet can later be expanded into execution units only when that packet is ready, instead of defining the entire project down to the smallest task on day one.

**Limits.** The graph says how work is structured and related. It does not make the work safe to execute concurrently, and graph validity is not authority.

**Technical references.** `framework/capabilities/hierarchical-work-graph/contract.md`, `framework/capabilities/hierarchical-work-graph/adoption-contract.md`, `docs/architecture/hierarchical-work-graph.md`.

## Capability: Exact lineage between plans, graph nodes and source material

**What it does.** HWG and related contracts preserve explicit identity and lineage so a generated unit can be traced back to the graph node, parent work and source material it came from.

**Problem it solves.** When work is decomposed repeatedly by agents, it can become impossible to answer why a small task exists or which accepted requirement it implements. Lost lineage makes review and later correction expensive.

**Example.** An execution unit can retain a stable identity and parent relation back to its work packet, allowing a reviewer to verify that the leaf still belongs to the accepted outcome.

**Limits.** Lineage proves derivation/relationship, not correctness or acceptance.

**Technical references.** HWG schemas/contracts and graph validation tooling.

## Capability: Fail-closed structural validation

**What it does.** The framework provides schemas and deterministic validators that reject malformed or internally inconsistent governance artifacts instead of allowing agents to continue with ambiguous structure.

**Problem it solves.** A missing dependency, duplicate identity or invalid graph shape can cause later execution to operate on a false plan. Catching those errors mechanically is cheaper and more reliable than hoping an AI model notices them later.

**Example.** A work graph with an invalid parent reference or an unsupported field can fail validation before it reaches an execution system.

**Limits.** Deterministic validation checks what can be encoded as rules. It cannot prove that a requirement is sensible, that a design is good or that a human decision has been made correctly.

**Technical references.** `contracts/`, `tools/validate_*`, capability-specific schemas and tests.

## Where exact current status lives

The root `README.md`, release/version files, capability contracts and consumer/adoption documentation define the exact currently released framework surface. This guide explains the purpose of those capabilities; it does not activate them for a consumer or create new normative semantics.
