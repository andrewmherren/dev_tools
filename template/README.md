# Copier Template Guide

This directory contains the unified single-command Copier flow.

## Quick Start

```bash
# Option A (from this repository root):
copier copy ./template my_project --trust

# Option B (from any location):
export DEV_TOOLS_ROOT=/absolute/path/to/dev_tools
copier copy "$DEV_TOOLS_ROOT/template" my_project --trust

# Apply to an existing project directory
cd my_existing_project
copier copy "$DEV_TOOLS_ROOT/template" . --trust
```

<details>
<summary>PowerShell equivalents</summary>

```powershell
# Option A (from this repository root):
copier copy .\template my_project --trust

# Option B (from any location):
$env:DEV_TOOLS_ROOT = "<absolute-path-to-dev_tools>"
copier copy "$env:DEV_TOOLS_ROOT\template" my_project --trust

# Apply to an existing project directory
cd my_existing_project
copier copy "$env:DEV_TOOLS_ROOT\template" . --trust
```

</details>

Copier records answers in `.copier-answers.yml`, enabling future upgrades with:

```powershell
copier update --trust
```

### Why `--trust` is required

This template uses Copier `tasks` (`tasks/merge_and_setup.py`) to preserve non-destructive merge behavior.
Copier treats tasks as an unsafe feature unless `--trust` is provided.

If you run without trust, the only fallback is to skip tasks:

```bash
# From this repo root:
copier copy ./template my_project --skip-tasks

# Or from any location:
copier copy "$DEV_TOOLS_ROOT/template" my_project --skip-tasks
```

`--skip-tasks` will generate files, but it will **not** run merge/copy-if-missing logic, so behavior differs from the supported workflow.

## Prompt Model

Template prompts include:

- `project_name`
- `project_slug`
- `description`
- `language` (`python`, `nodejs`, `rust`, `godot`, `unreal`, `cpp`)
- `execution_mode` (`container`, `host`, `hybrid`)
- language-specific conditional prompts (`python_package_manager`, `node_package_manager`, `cpp_build_system`)

### Execution mode quick guide

- `container`: Use when most development tooling should be reproducible in a dev container (typical for Python/Node/Rust).
- `host`: Use when primary SDK/editor workflows are host-native (typical for Unreal, some C++/Godot setups).
- `hybrid`: Use when runtime/editor is best on host, but you still want containerized tooling for consistency (for example, host Unreal/Godot editor + container lint/test/docs tooling).

## Merge Behavior (Preserved)

The Copier task `tasks/merge_and_setup.py` runs on host and preserves prior behavior:

- `.vscode/settings.json`: deep object merge with project values winning
- `.vscode/extensions.json`: union + deduplicate by extension ID
- `.vscode/keybindings.json`: union + deduplicate by command, project values winning
- `.github/instructions/*`: copied only when destination file is missing
- `.github/agents/*`: copied only when destination file is missing

## Container vs Host

- Container/hybrid modes generate `.devcontainer/devcontainer.json` with language-appropriate base image and in-container `postCreateCommand` installs.
- Host mode removes `.devcontainer/` in the post-copy task and relies on host tasks in `.vscode/tasks.json`.

## VS Code Tasks

Generated projects include standard tasks in `.vscode/tasks.json`:

- **test**: Language-specific test runner (marked as default test task)
- **lint**: Code linting with safe placeholders for configuration
- **typecheck**: Type checking (Python/Node/Rust only)
- **verify**: Compound task running test + lint + typecheck in parallel
- **format**: Code formatting placeholder
- **build**: Conditional on language/execution mode (C++/Unreal/Godot)

Tasks use safe echo placeholders before tooling is configured to avoid failing prescriptively. Concrete commands are provided where universally safe (e.g., `cargo test`, `npm test`).

## Security Defaults

Generated projects include:

- `.env.example` placeholders (no real secrets)
- `.gitignore` entries for `.env` and `.env.local`
- secret-free `.vscode/mcp.json` (environment variable references only)
- `.githooks/pre-commit` secret scan hook
- `.github/instructions/secrets-management.md`

## Adding a New Language

1. Add `fragments/languages/<lang>-settings.json`.
2. Add `fragments/languages/<lang>-extensions.json`.
3. Optionally add `fragments/languages/<lang>-keybindings.json`.
4. Add `instructions/languages/<lang>-conventions.md`.
5. Add `<lang>` to `language` choices and validator logic in `copier.yml`.
6. Update `.devcontainer/devcontainer.json.jinja` and `.vscode/tasks.json.jinja` if language needs special workflows.
