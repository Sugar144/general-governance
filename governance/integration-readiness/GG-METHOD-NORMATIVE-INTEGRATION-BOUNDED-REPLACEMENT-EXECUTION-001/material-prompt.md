---
prompt_id: GG-MP-0004
version: 1.0.0
category: FORMAL_INTEGRATION_READINESS
custody_status: APPROVED_NOT_EXECUTED
execution_id: GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001-RUN-001
formal_input_package_sha256: b9dde57a0d25e8ec21808581595fcbaa6ed7a17d802bca6d6c19ed3fef333d26
authority_record: GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001-AUTH-001
output_path: governance/integration-readiness/GG-METHOD-NORMATIVE-INTEGRATION-BOUNDED-REPLACEMENT-EXECUTION-001/result.md
---

# Material Prompt Snapshot

Execute exactly one read-only integration-readiness analysis over the accepted normative implementation HEAD `95e7dafac6afee54ca1ff6112dcd0cded74d08e8`.

Determine the smallest rc.5 packaging surface and the sequencing required so `main` is never advanced to a state where tracked framework content differs from the release identity carried by `release-manifest.json`.

Use the current validators and rc.4 materialization history as evidence. Preserve the accepted POC bytes exactly. Pay special attention to the release-content digest covering all tracked files except `release-manifest.json`, including governance evidence files.

Do not modify release-facing files, create a PR, merge, tag, release, publish, or infer authority from readiness. Materialize and validate only the declared readiness result. No second run is authorized.
