# Secrets Management

## Mandatory Practices

- Keep all secrets in local environment files (`.env`, `.env.local`) and never commit them.
- Do not store secrets in source files, README examples, or VS Code settings.
- `.vscode/mcp.json` must only reference environment variables (for example `${SONARQUBE_TOKEN}`).

## SonarQube Example

1. Copy `.env.example` to `.env`.
2. Set `SONARQUBE_TOKEN=your_sonarqube_token_here`.
3. Restart VS Code so MCP processes read updated environment values.

## Rotation and Revocation

- Rotate leaked tokens immediately.
- Invalidate old tokens in provider dashboards.
- Update `.env` and retry local workflows.
