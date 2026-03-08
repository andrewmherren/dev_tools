# Agent Verification Contract

## Core Principle

After making code edits, agents MUST attempt verification and report results transparently.

## Verification Workflow

1. **Execute verification**: Run `test` or `verify` task (via VS Code tasks or equivalent command).
2. **Report exact commands**: State the actual command executed (e.g., `pytest tests/`, `npm test`).
3. **Report pass/fail status**: Clearly indicate success, failure, or partial completion.
4. **Identify uncovered risks**: Explicitly note what was NOT verified (e.g., "integration tests skipped", "linting not run", "type checking unavailable").

## Fallback Behavior

### When tasks are unavailable

- Check for canonical test commands in language conventions (e.g., `pytest`, `npm test`, `cargo test`).
- If no test framework detected, state: "No test framework found; verification skipped."
- Suggest setup steps if user requests verification.

### When tools fail

- Report exact error message and exit code.
- Do NOT claim success if verification failed or was skipped.
- Suggest diagnostic steps (e.g., "Install dependencies first: `pip install -e .[dev]`").

### When credentials/secrets missing

- Honor security policy: Never propose hardcoding secrets.
- State: "Verification requires environment setup (see git-safety.md)."
- If verification can proceed with reduced scope, clearly indicate limitations.

## Example Reports

### Success

```
Verification: PASS
Command: pytest tests/ -v
Exit code: 0
Coverage: 87% (not enforced)
Risks: Integration tests require live database (skipped).
```

### Failure

```
Verification: FAIL
Command: npm test
Exit code: 1
Error: 3 test cases failed in auth.test.ts
Risks: Type checking not run; build task not verified.
```

### Unavailable

```
Verification: SKIPPED
Reason: No test task configured and no test files detected.
Suggestion: Add test framework and configure .vscode/tasks.json test task.
```

## Compatibility Notes

- Verification MUST NOT require committing secrets (see git-safety.md).
- Use environment variables for tokens/credentials (see mcp-policy.md).
- If verification depends on external services (Sonar, Trivy), clearly mark as optional.
