# Configuring Your Project to Use the Dev Environment

This guide walks you through integrating your project with the shared development infrastructure (Ollama, SonarQube, documentation indexing, etc.).

## Quick Start

### 1. Verify Dev Server is Running

From the dev environment directory:

```bash
cd <path-to-dev_tools>
docker compose ps
```

<details>
<summary>PowerShell equivalent</summary>

```powershell
cd <path-to-dev_tools>
docker compose ps
```

</details>

All services should show `healthy` or `running` status.

### 2. Access the Homepage

Open [http://localhost](http://localhost) in your browser to see all available services.

---

## Creating a New Project with Copier

See **[Copier Template Guide](../template/README.md)** for complete instructions.

Set this once for shell examples that reference the dev tools repo:

```bash
export DEV_TOOLS_ROOT=/absolute/path/to/dev_tools
```

<details>
<summary>PowerShell equivalent</summary>

```powershell
$env:DEV_TOOLS_ROOT = "<absolute-path-to-dev_tools>"
```

</details>

### New project (single command)

```bash
# From this repo root:
copier copy ./template my_project --trust

# Or from any location:
export DEV_TOOLS_ROOT=/absolute/path/to/dev_tools
copier copy "$DEV_TOOLS_ROOT/template" my_project --trust
```

### Apply to existing project

```bash
cd MyExistingProject
copier copy "$DEV_TOOLS_ROOT/template" . --trust
```

### Update an existing Copier-managed project

```bash
copier update --trust
```

`--trust` is required because this template runs Copier tasks to preserve merge behavior (`.vscode` merge, copy-if-missing for instructions/agents).

Execution mode guidance:

- `container`: best when most tooling should run in a reproducible dev container.
- `host`: best when your core workflow depends on host-native SDKs/editors.
- `hybrid`: best when editor/runtime stays on host, but lint/test/docs tooling should stay containerized.

---

## VSCode Integration

### Copy Example Configuration

```bash
# From your project root
mkdir -p .vscode
cp "$DEV_TOOLS_ROOT/example-vscode/mcp.json" .vscode/mcp.json
```

<details>
<summary>PowerShell equivalent</summary>

```powershell
# From your project root
New-Item -ItemType Directory -Path .vscode -Force | Out-Null
Copy-Item "$env:DEV_TOOLS_ROOT\example-vscode\mcp.json" ".vscode\mcp.json"
```

</details>

### Configure SonarQube Token

1. Get your SonarQube token:
   - Open [http://sonarqube.localhost](http://sonarqube.localhost)
   - Login (default: `admin` / `admin`)
   - Menu: User > My Account > Security
   - Click "Generate Token"
   - Copy the token

2. Set the environment variable in your project:

   **PowerShell:**

   ```powershell
   $env:SONARQUBE_TOKEN = "sqp_your_token_here"
   ```

   **Bash/WSL:**

   ```bash
   export SONARQUBE_TOKEN="sqp_your_token_here"
   ```

   **Persistent (add to `.env.local`):**

   ```env
   SONARQUBE_TOKEN=sqp_your_token_here
   ```

3. Add to `.gitignore`:

   ```gitignore
   .env.local
   .vscode/mcp.json
   ```

4. Restart VS Code to activate MCP servers

### Available MCP Servers

Once configured, you'll have access to:

| Server        | Purpose                                            | Status           |
| ------------- | -------------------------------------------------- | ---------------- |
| **docs-mcp**  | Search documentation and code using AI embeddings  | Always available |
| **sonarqube** | Code quality, vulnerability, and security analysis | Requires token   |

---

## Docker Compose Integration

If your project also runs Docker containers and needs to access shared services:

### Add Dev Network to Your `docker-compose.yml`

```yaml
version: "3.8"

services:
  myapp:
    build: .
    environment:
      # Access internal services via container network
      OLLAMA_API_URL: http://ollama:11434
      SONARQUBE_URL: http://sonarqube:9000
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
    networks:
      - default

networks:
  default:
    external: true
    name: <your-compose-project-name>_dev-network
```

Find the actual network name on your machine:

```bash
docker network ls | grep dev-network
```

<details>
<summary>PowerShell equivalent</summary>

```powershell
docker network ls | Select-String dev-network
```

</details>

### Service Endpoints (from containers)

When your container is on the dev tools `dev-network`, use these internal addresses:

| Service   | Internal URL            | Port  |
| --------- | ----------------------- | ----- |
| Ollama    | `http://ollama:11434`   | 11434 |
| SonarQube | `http://sonarqube:9000` | 9000  |
| Postgres  | `postgres:5432`         | 5432  |
| docs-mcp  | `http://docs-mcp:6280`  | 6280  |
| Traefik   | `http://traefik:80`     | 80    |

---

## Using SonarQube for Code Analysis

### Analyze Your Code

```bash
# Install scanner (one-time)
npm install -g sonarqube-scanner

# Run analysis from your project root
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://sonarqube.localhost \
  -Dsonar.login=$SONARQUBE_TOKEN
```

<details>
<summary>PowerShell equivalent</summary>

```powershell
sonar-scanner `
  -Dsonar.projectKey=my-project `
  -Dsonar.sources=. `
  -Dsonar.host.url=http://sonarqube.localhost `
  -Dsonar.login=$env:SONARQUBE_TOKEN
```

</details>

### View Results

1. Open [http://sonarqube.localhost](http://sonarqube.localhost)
2. Navigate to your project
3. Review issues, vulnerabilities, and metrics

---

## Optional VS Code Security & Quality Tasks

If you used the Copier template, your project includes optional security scanning tasks:

### `sonar-scan` Task

Runs SonarQube analysis directly from VS Code.

**Prerequisites:**

- Install `sonar-scanner` CLI: `npm install -g sonarqube-scanner`
- Set `SONARQUBE_TOKEN` environment variable (see above)

**Behavior:**

- **Host/hybrid mode**: Connects to `http://sonarqube.localhost`
- **Container mode**: Connects to `http://sonarqube:9000`
- **Non-blocking**: Skips gracefully if token not set

**Run via:**

- VS Code Command Palette: `Tasks: Run Task` → `sonar-scan`
- Terminal: `sonar-scanner -Dsonar.host.url=http://sonarqube.localhost -Dsonar.token="$SONARQUBE_TOKEN"`

### `trivy-scan` Task

Scans your project for vulnerabilities and misconfigurations using Trivy.

**Prerequisites:**

- Install Trivy CLI: See [Trivy installation docs](https://aquasecurity.github.io/trivy/)
- Dev tools server must be running (provides Trivy server)

**Behavior:**

- **Host/hybrid mode**: Connects to Trivy server at `http://localhost:8080`
- **Container mode**: Connects to `http://trivy-server:8080`
- **Non-blocking**: Reports findings but doesn't fail the workflow
- Scans filesystem for: vulnerabilities, misconfigurations

**Run via:**

- VS Code Command Palette: `Tasks: Run Task` → `trivy-scan`
- Terminal (host): `trivy fs --server http://localhost:8080 --scanners vuln,misconfig .`
- Terminal (container): `trivy fs --server http://trivy-server:8080 --scanners vuln,misconfig .`

**Note:** Both tasks are optional and designed to be non-blocking. They gracefully skip if dependencies or credentials are unavailable.

---

## Using Ollama for Local LLMs

### Available Models

By default, the `nomic-embed-text` embedding model is available. Additional models can be pulled:

```bash
# Add the model to your compose file volumes
docker exec ollama-server ollama pull llama2
```

### From Your Application

```python
import requests
import json

# Connect to Ollama from your app
response = requests.post(
    'http://ollama.localhost:11434/api/generate',
    json={
        'model': 'llama2',
        'prompt': 'Hello!',
        'stream': False
    }
)
print(response.json()['response'])
```

### From Your Container

```python
# Use internal network address
response = requests.post(
    'http://ollama:11434/api/generate',
    json={'model': 'llama2', 'prompt': 'Hello!', 'stream': False}
)
```

---

## Exposing Your Project's Services

If you want to expose your dev server on Traefik (e.g., `http://my-project.localhost`):

1. Edit `<path-to-dev_tools>/traefik/dynamic/dev-projects.yml`:

```yaml
http:
  routers:
    my-project:
      entryPoints:
        - web
      rule: Host(`my-project.localhost`)
      service: my-project-service

  services:
    my-project-service:
      loadBalancer:
        servers:
          - url: http://host.docker.internal:3000 # Your app's port on host
```

Linux note: add `extra_hosts: ["host.docker.internal:host-gateway"]` to the container that needs host access.

2. Reload Traefik:

```bash
cd <path-to-dev_tools>
docker compose restart traefik
```

3. Access your app at [http://my-project.localhost](http://my-project.localhost)

---

## Troubleshooting

### Services Not Reachable from `localhost`

**Issue:** `http://sonarqube.localhost` returns "Cannot GET"

**Solution:**

1. Verify Traefik is running: `docker compose ps traefik`
2. Check Traefik logs: `docker compose logs traefik`
3. Verify route config: `traefik/dynamic/dev-projects.yml`
4. Restart Traefik: `docker compose restart traefik`

### MCP Servers Not Connecting in VS Code

**Issue:** "Unable to connect to sonarqube" or "docs-mcp not responding"

**Solution:**

1. Verify dev server is running: `docker compose ps`
2. Check container logs: `docker compose logs sonarqube` or `docker compose logs docs-mcp`
3. Verify SONARQUBE_TOKEN is set: Check your environment variable
4. Reload VS Code window from the command palette (`Developer: Reload Window`)

### Ollama Model Not Available

**Issue:** "Model not found" errors when querying Ollama

**Solution:**

```bash
# List available models
docker exec ollama-server ollama list

# Pull a new model
docker exec ollama-server ollama pull mistral
```

### Docker Container Can't Reach Dev Services

**Issue:** `Connection refused` when container tries `http://ollama:11434`

**Solution:**

1. Verify container is on correct network: `docker network inspect <your-compose-project-name>_dev-network`
2. Update `docker-compose.yml` to use external network (see Docker Compose Integration section)
3. Restart your containers after network changes

---

## Security Considerations

- **Never commit tokens to git**: Use `.env.local` or environment variables
- **Keep credentials secret**: Don't share your SonarQube token
- **Rotate tokens periodically**: Generate new tokens for long-running services
- **Review shared access**: If team members share this dev server, document who has access
- **Isolate sensitive code**: Don't analyze proprietary/confidential code in shared analysis tools

---

## Next Steps

1. **Set up VSCode integration** (follow VSCode Integration section above)
2. **Generate SonarQube token** and configure it
3. **Run your first analysis**: Use sonarqube-mcp or sonar-scanner
4. **Explore documentation search**: Try docs-mcp in Copilot
5. **Add Traefik route** if you want to expose your app
