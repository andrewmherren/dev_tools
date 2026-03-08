# Git Safety and Secrets Hygiene

## Core Rules

- Never commit real credentials or tokens.
- Store secrets in `.env` or `.env.local` only.
- Keep `.vscode/mcp.json` secret-free and use environment variable references.
- Run the pre-commit hook (`.githooks/pre-commit`) to catch accidental secrets before commit.

## Required Setup

1. Copy `.env.example` to `.env`.
2. Fill in token placeholders locally.
3. Set git hooks path once per clone:

```bash
git config core.hooksPath .githooks
```

## Recommended `.gitignore` Entries

```gitignore
.env
.env.local
.env.*.local
```
