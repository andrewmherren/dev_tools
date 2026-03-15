---
name: test-driven-development
description: Apply a red-green-refactor cycle to implement behavior changes safely.
---

# Test-Driven Development

Use when changing behavior or adding new logic.

## Cycle

1. Red: add or update a test that fails for the intended reason.
2. Green: implement the minimal code to make the test pass.
3. Refactor: improve design while keeping tests green.
4. Re-run affected verification commands.

## Rules

- Start each behavior change by creating a failing test before writing the main implementation.
- Keep each cycle focused on one behavior change.
