---
name: systematic-debugging
description: Diagnose failures using evidence, hypotheses, and minimal reproducible checks.
---

# Systematic Debugging

Use this for failing tests, builds, or runtime defects.

## Procedure

1. Capture the exact failure and environment details.
2. Form a short list of hypotheses.
3. Test hypotheses with the smallest possible experiment.
4. Apply the fix and verify with the failing reproduction plus regression checks.

## Rules

- Base each debugging step on observed evidence and explicitly tested hypotheses.
- Keep a trace of what was tried and what was disproven.
