---
prompt_id: GG-MP-0003
version: 1.0.0
execution_id: GG-RELEASE-PACKAGE-0.1.0-RC.5-001-RUN-001
formal_input_package_sha256: 652e11827aabc0f3538bb7fbeda634d4af0ef73cd19c3a350286b73cefb9c54c
status: APPROVED_NOT_EXECUTED
---

# Material Prompt — rc.5 Release Packaging

Prepare and execute exactly one bounded General Governance `0.1.0-rc.5` release package on top of accepted readiness HEAD `5ef26e8adbc167a88bfa6ef64bfeac5a75369b43`.

Preserve `framework/core/project-operating-contract.md` exactly at blob `9abe903e6c045fd67c1a061e8dff79fbb076fdd3`.

Modify only `RELEASE_VERSION`, `README.md`, `docs/consumer-contract.md`, `provenance/evolution-manifest.json`, and finally `release-manifest.json`, plus new tracked custody/evidence under `governance/releases/GG-RELEASE-PACKAGE-0.1.0-RC.5-001/**`.

Finalize all tracked files before calculating the release content digest. Make `release-manifest.json` the final tracked mutation. After that boundary, perform only read-only validation and external Issue bookkeeping.

Do not create a PR, merge, tag, release, deploy, publish, alter compatibility contracts, or infer any second execution.
