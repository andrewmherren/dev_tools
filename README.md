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

Start new projects using the unified Copier template. See **[Copier Template Guide](template/README.md)** for quick start, language/mode options, merge behavior, and update workflow (`copier update`).

## Documentation

- **[Full Infrastructure Guide](homepage/README.md)** — Complete architecture, setup, and service details
- **[Project Integration Guide](homepage/PROJECT_SETUP.md)** — How to configure your projects to use this dev environment
- **[Safe Integration Patterns](docs/git-safety.md)** — Best practices for consuming shared services
- **[MCP Servers & Policy](docs/mcp-policy.md)** — Available servers and access control

See [Full Guide](homepage/README.md) for detailed resource breakdown.

## License

Provided as-is for local development use.
