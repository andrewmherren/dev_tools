---
name: verification-before-completion
description: Require explicit verification evidence before declaring a task complete.
---

# Verification Before Completion

Use this at the end of each meaningful change.

## Checklist

1. Run the relevant test/lint/typecheck/build commands.
2. Report pass/fail results and command coverage.
3. Explicitly state what was not verified.
4. If verification fails, return to debugging instead of marking done.

## Reference

Follow `.github/instructions/agent-verification.md` for expected reporting format.
