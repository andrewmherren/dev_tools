<!--
Generated file. Source: README.md
Update source docs, then run: python scripts/sync-homepage-docs.py
-->
# Dev Environment Infrastructure

A Docker-based shared infrastructure server providing AI-driven development tools, code quality analysis, CI/CD, and security scanning for local development projects.

## Quick Start

```bash
# Clone or navigate to the repository root
git clone https://github.com/andrewmherren/dev_tools
cd dev_tools

# Copy environment configuration
cp .env.example .env

# Edit .env with your storage paths and settings
# Example:
#   OLLAMA_STORAGE_PATH=/absolute/path/to/dev_tools/.server_data/.ollama
#   SONARQUBE_STORAGE_PATH=/absolute/path/to/dev_tools/.server_data/.sonarqube

# Start all services
docker compose up -d

# Access the homepage
# Open http://localhost in your browser
```

<details>
<summary>PowerShell equivalents</summary>

```powershell
git clone https://github.com/andrewmherren/dev_tools
cd dev_tools
Copy-Item .env.example .env
docker compose up -d
```

</details>

## Services Included

- **Ollama** — GPU-accelerated local LLM inference
- **SonarQube** — Code quality and security analysis
- **docs-mcp** — AI-powered documentation indexing
- **Traefik** — Reverse proxy and load balancer
- **Drone CI** — Container-native CI/CD pipelines
- **Trivy** — Vulnerability scanner
- **Postgres** — Database backend with pgvector

## Project Scaffolding

Start new projects using the unified Copier template. See **[Copier Template Guide](guides/copier-guide.md)** for quick start, language/mode options, merge behavior, and update workflow (`copier update`). For convenience, see **[Command Shortcuts](guides/copier-guide.md#command-shortcuts)** to create shell aliases like `devtools-new my_project`.

## Documentation

- **[Server Day-to-Day Guide](README.md)** — Start, verify, inspect, and maintain the dev tools server
- **[Copier Project Day-to-Day Guide](guides/copier-guide.md)** — Create and update projects with the unified template
- **[Project Integration Guide](guides/project-integration.md)** — Connect downstream projects to shared services
- **[Safe Integration Patterns](guides/git-safety.md)** — Credential and local-only safety practices
- **[MCP Servers & Policy](guides/mcp-policy.md)** — MCP endpoints, auth, and usage policy

### Homepage-Served Docs

The homepage container can only serve files under `homepage/`. To keep homepage links in sync with canonical docs in the repo root and `template/`, we publish selected docs into `homepage/guides/`.

Refresh published docs:

```bash
python scripts/sync-homepage-docs.py
```

Optional: enable repository git hooks so docs are synced automatically before commits:

```bash
sh scripts/install-git-hooks.sh
```

If your checkout does not preserve executable bits on Unix-like systems, run:

```bash
chmod +x .githooks/pre-commit scripts/install-git-hooks.sh scripts/sync-homepage-docs.sh scripts/sync-homepage-docs.py
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/install-git-hooks.ps1
```

Convenience wrappers are also available:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync-homepage-docs.ps1
```

```bash
sh scripts/sync-homepage-docs.sh
```

## License

Provided as-is for local development use.
