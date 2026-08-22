# Claude review execution instructions

Use a fresh Claude Code session that did not implement I1.

Review target: `b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea`

Historical baseline: `22a1d5e2f759fda53574884e1056a3a56baa211a`

Recommended isolation:

```bash
git fetch origin
git worktree add ../gg-i1-independent-review b8766d5f316b1a4c05f1bbeebd5ef148bf45e7ea
cd ../gg-i1-independent-review
```

Then open a **new** Claude Code session from that detached worktree. Give Claude the contents of:

`governance/implementation/GG-IMPLEMENTATION-RELEASE-PAYLOAD-OPERATIONAL-PLANE-I1-001/claude-independent-review-packet.md`

Because that review packet was added after the functional candidate, it is not present inside the detached candidate worktree. Read/copy it from the I1 coordination branch or from GitHub, but do not switch the review worktree away from the exact candidate.

Claude must remain read-only. It may run tests and create temporary fixtures outside the repository, but it must not edit repository files, commit, push, open/merge PRs, or apply fixes.

Return the complete reviewer output verbatim so it can be bound to `IR-001` and evaluated against the exact candidate. A valid top-level verdict is only `PASS`, `CHANGES_REQUIRED`, or `INDETERMINATE`.
