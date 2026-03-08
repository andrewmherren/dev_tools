# MCP Usage Policy

## Available Defaults

- `docs-mcp` via SSE (`http://docs.localhost/sse`, fallback `http://localhost/docs/sse`)
- `filesystem` via local stdio server
- `sonarqube` disabled by default, enabled after token setup

## Optional Verification Tools

- SonarQube: Requires `SONARQUBE_TOKEN` environment variable (see git-safety.md)
- Trivy: Available when dev_tools server running; non-blocking if unavailable
- See agent-verification.md for fallback behavior when tools are not configured

## Security

- Never hardcode tokens in `.vscode/mcp.json`.
- Use `${SONARQUBE_TOKEN}` and similar environment references only.
- Prefer project-local scopes when connecting filesystem MCP tools.
