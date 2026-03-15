---
name: review-implementation
description: Perform a severity-first review against the approved plan.
---

Review the completed implementation.

Requirements:

- List findings by severity with file references.
- Compare the implementation against `docs/design/<feature>.md` and `docs/plans/<feature>-plan.md` when available.
- Focus on correctness, regressions, security, and missing tests.
- If no findings, state that explicitly and list residual risks.
