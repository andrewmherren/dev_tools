# Dev Tools - AI Agent Instructions

This is a Docker-based development tools server providing shared infrastructure (AI/LLM inference, code quality analysis, CI/CD, documentation indexing) for local development projects.

## Architecture & Service Stack

### Two-Network Design

- **internal-network**: Isolated network with no external internet access for core services (Ollama, Postgres, SonarQube, docs-mcp)
- **dev-network**: Bridge network for services needing host/project communication (Trivy, Traefik)
- **Traefik** routes `*.localhost` subdomains and acts as gateway between networks

### Core Services (docker-compose.yml)

- **Ollama** (ollama-server): GPU-accelerated LLM inference with NVIDIA Docker runtime; auto-downloads `nomic-embed-text` on first start
- **docs-mcp** (docs-mcp-server): Documentation indexing MCP server with SSE endpoint; uses Ollama for embeddings
- **SonarQube** (sonarqube-server): Code quality analysis with Postgres+pgvector backend; exposed via `sonarqube-mcp` to AI agents
- **Traefik** (ai-dev-traefik): Reverse proxy serving homepage at `http://localhost` and routing all `*.localhost` domains
- **Trivy** (trivy-server): Vulnerability scanner for containers/IaC; server mode on port 8080
- **Drone CI** (drone-server/drone-agent): Commented out by default; requires Git provider configuration

All services use security hardening: `no-new-privileges`, `cap_drop: ALL`, memory limits, and minimal capabilities.

### Storage Paths (Environment Variables)

Configure in `.env` (copy from `.env.example`):

- `OLLAMA_STORAGE_PATH`: Models storage (~several GB per model)
- `SONARQUBE_STORAGE_PATH`: Analysis cache and database
- `DOCS_MCP_STORAGE_PATH`: Documentation index
- `DRONE_RPC_SECRET`: Shared secret for Drone server-agent communication (if enabled)

## Copier Template System

### Single-Template Scaffolding Pattern

A single unified template at `template/` handles all language + execution-mode combinations.

- **Single command (from repo root):** `copier copy ./template <destination>`
- **Single command (from any location):** `copier copy "$DEV_TOOLS_ROOT/template" <destination>`
- **Language choices:** python, nodejs, rust, godot, unreal, cpp
- **Execution modes:** container, host, hybrid

### Template Directory Structure

```
template/
├── copier.yaml                   # Questions, validation, tasks, exclusions
├── tasks/
│   ├── merge_and_setup.py        # Host-side merge/copy logic
│   ├── container_setup.jinja     # Container workflow notes
│   └── host_setup.jinja          # Host workflow notes
├── fragments/
│   ├── shared/                   # Base VS Code + MCP fragments
│   ├── execution/                # Mode-specific fragments
│   └── languages/                # Language-specific fragments
├── instructions/
│   ├── common/                   # Shared instruction docs
│   ├── languages/                # Per-language conventions
│   └── agents/                   # Optional AI agent guidance
└── *.jinja                       # Rendered project files
```

### Critical Merging Behavior (template/tasks/merge_and_setup.py)

1. **Settings merge**: Deep object merge where **project values always win** on conflicts
2. **Extensions merge**: Union + deduplicate by extension ID
3. **Keybindings merge**: Union + deduplicate by command; project bindings win
4. **Instructions/agents**: Copy to `.github/instructions/` and `.github/agents/` only if destination file is missing

### Template Commands

Set `DEV_TOOLS_ROOT` once if you run commands outside this repository root.

```powershell
# Create a new project
copier copy .\template my_python_app --trust

# Apply to an existing project directory
cd MyExistingProject
copier copy "$env:DEV_TOOLS_ROOT\template" . --trust

# Update from newer template version
copier update --trust
```

`--trust` is required because the template uses Copier tasks for merge/copy-if-missing behavior.

### Idempotency Tracking

Copier stores answers in `.copier-answers.yml` and uses them during `copier update`.

## Developer Workflows

### Starting the Dev Environment

```bash
cd <path-to-dev_tools>
docker compose up -d          # Start all services
docker compose ps            # Verify status
```

Access homepage: `http://localhost` (lists all services with links)

### Adding Language Support

1. Add `fragments/languages/{lang}-settings.json`.
2. Add `fragments/languages/{lang}-extensions.json`.
3. Optionally add `fragments/languages/{lang}-keybindings.json`.
4. Add `instructions/languages/{lang}-conventions.md`.
5. Add `{lang}` to `copier.yaml` language choices and validator rules.
6. Update `.devcontainer/devcontainer.json.jinja` and `.vscode/tasks.json.jinja` if needed.
7. Verify with `copier copy` and `copier update`.

### MCP Server Configuration (example-vscode/mcp.json)

Projects use MCP servers for AI-assisted development:

- **docs-mcp**: SSE endpoint at `http://docs.localhost/sse` (fallback: `http://localhost/docs/sse` if `.localhost` DNS routing is unavailable on your machine)
- **sonarqube**: Requires token from `http://sonarqube.localhost` → User > My Account > Security > Generate Token

Store token in environment variable: `SONARQUBE_TOKEN=sqp_xxxxx`

### Service Access Patterns

- From **host**: Use `http://{service}.localhost` (Traefik routing)
- From **containers**: Use `http://{service-name}:{port}` (e.g., `http://ollama:11434`, `http://sonarqube:9000`)
- **Fallback (any OS)**: If `.localhost` doesn't resolve, use `http://localhost/{service}/`

## Project-Specific Conventions

### VS Code Settings Merge Strategy

When modifying template fragments, remember:

- **Project values always win** on conflicts (merge.py:deep_merge)
- New keys from template are added
- Nested objects are recursively merged
- Arrays are NOT automatically merged in deep_merge (handle separately with merge_extensions)

### Security Patterns

- Store tokens/secrets in `.env` or `.env.local` (**never commit**)
- Keep `.vscode/mcp.json` committed but secret-free using environment variable references only
- All Docker services run with `security_opt: no-new-privileges:true` and `cap_drop: ALL`
- Only add back specific capabilities needed (e.g., `NET_BIND_SERVICE` for Traefik)

### Documentation Conventions (docs/)

- `git-safety.md`: Credential management patterns and local-only MCP guidelines
- `mcp-policy.md`: Available MCP servers, endpoints, authentication, and compatibility notes

### Resource Limits Pattern

Every service in `docker-compose.yml` has explicit memory limits under `deploy.resources.limits.memory`. Example:

```yaml
deploy:
  resources:
    limits:
      memory: 2g
```

## Key Files Reference

- **docker-compose.yml**: Service definitions, networks, volumes, security policies
- **template/README.md**: Copier workflow guide, merge behavior, and maintainer instructions
- **template/copier.yaml**: Prompt schema, validation rules, task wiring, and exclusions
- **template/tasks/merge_and_setup.py**: Core merge utilities and copy-if-missing behavior
- **homepage/README.md**: Full infrastructure guide with service details, setup, and troubleshooting
- **homepage/PROJECT_SETUP.md**: How downstream projects integrate with this dev environment
- **docs/mcp-policy.md**: MCP server endpoints and configuration examples
- **example-vscode/mcp.json**: Sample MCP configuration for projects

## Common Tasks

### Adding a New Service to docker-compose.yml

1. Choose appropriate network(s): `internal-network` (isolated) or `dev-network` (host access)
2. Add security hardening: `security_opt`, `cap_drop: ALL`, minimal `cap_add`
3. Set memory limit under `deploy.resources.limits.memory`
4. Use environment variables from `.env` for storage paths
5. Add volume mounts for persistent data
6. Configure Traefik labels if web UI needed (see existing services for pattern)

### Modifying Template Merge Logic

Edit `template/tasks/merge_and_setup.py` for merge behavior and copy-if-missing logic. Keep project-wins semantics unchanged for settings/keybindings and union-dedupe behavior for extensions.

### Debugging Service Issues

```powershell
docker compose logs {service-name}    # View logs
docker compose ps                     # Check status
docker exec -it {container-name} sh   # Shell into container
```

For Ollama model issues: `docker logs ollama-server` to check download progress.
