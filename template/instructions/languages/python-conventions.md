# Python Conventions

- Format with Black.
- Keep imports sorted and grouped.
- Favor explicit typing on public interfaces.
- Use pytest for tests and keep tests deterministic.

## Verification Commands

- **Test**: `pytest` or `pytest tests/` (see agent-verification.md)
- **Lint**: `ruff check .` or `flake8 .`
- **Type check**: `mypy .` or `pyright`
