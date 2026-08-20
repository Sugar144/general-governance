---
package_id: GG-RELEASE-PACKAGE-0.1.0-RC.5-001
execution_id: GG-RELEASE-PACKAGE-0.1.0-RC.5-001-RUN-001
role: RELEASE_PACKAGE_IMPLEMENTER
mode: BOUNDED_RELEASE_PACKAGING
protocol: GG-RELEASE-PACKAGE-PROTOCOL-001
formal_input_package_sha256: 652e11827aabc0f3538bb7fbeda634d4af0ef73cd19c3a350286b73cefb9c54c
permitted_execution_count: 1
status: PREPARED
---

# General Governance 0.1.0-rc.5 — Release Work Package

## Objective

Materialize one release-conformant `0.1.0-rc.5` candidate on top of the exact accepted readiness lineage without modifying the accepted Project Operating Contract.

## Required tracked mutations before manifest finalization

- `RELEASE_VERSION`: `0.1.0-rc.4` -> `0.1.0-rc.5`.
- `README.md`: describe rc.5 and bounded replacement-execution semantics while preserving prior compatibility history.
- `docs/consumer-contract.md`: document rc.5 compatibility and rc.4 -> rc.5 immutable-lock transition with no configuration migration.
- `provenance/evolution-manifest.json`: bind accepted POC SHA-256 `5a54eb128b36cffbf12fdaf3070a88cc7c84d9f696333e01c679d31fa5de723b` and extend the L0 reason only.
- create all package custody/evidence intended to ship.

## Final tracked mutation

Update `release-manifest.json` last:
- `framework_version = 0.1.0-rc.5`;
- preserve compatibility and capability declarations;
- bind the content digest of the complete tracked tree excluding the manifest itself.

## Validation contract

Before finalization:
1. `main` currentness exact.
2. branch descends from accepted readiness HEAD.
3. accepted POC Git blob and SHA-256 exact.
4. only authorized surfaces differ.
5. release version and docs state rc.5.
6. compatibility declarations unchanged.
7. evolution provenance binds exact POC.
8. existing deterministic evolution/schema/syntax checks can proceed.
9. all tracked package evidence is complete.

After manifest finalization, read-only:
1. no tracked mutation after manifest commit;
2. release digest reproduces manifest `content_sha256`;
3. `verify_evolution` semantics hold;
4. consumer conformance and repository CI are checked on the exact final commit when observable;
5. final compare proves no unauthorized change.

## Stop conditions

Stop on any identity/currentness drift, unapproved write surface, POC change, compatibility change, failed/indeterminate gate, digest mismatch, or need for a post-manifest tracked mutation.
