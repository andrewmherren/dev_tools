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

## Command Shortcuts

To avoid typing the full `copier copy "$DEV_TOOLS_ROOT/template" <destination> --trust` command repeatedly, you can create shell shortcuts. These examples use `devtools-new`, `devtools-apply`, and `devtools-update` as command names, but you can customize them to your preference (e.g., `new_project`, `dt-new`, etc.).

### Prerequisites

Set `DEV_TOOLS_ROOT` as a persistent environment variable pointing to the dev_tools repository root:

<details>
<summary>Bash/Zsh (Linux/macOS/WSL)</summary>

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
export DEV_TOOLS_ROOT="/absolute/path/to/dev_tools"
```

Reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

</details>

<details>
<summary>PowerShell (Windows)</summary>

Add to your PowerShell profile. First, find your profile location:

```powershell
$PROFILE
```

Open/create the profile file:

```powershell
notepad $PROFILE
```

Add this line:

```powershell
$env:DEV_TOOLS_ROOT = "D:\path\to\dev_tools"
```

Reload your profile:

```powershell
. $PROFILE
```

</details>

### Bash/Zsh Functions

Add these functions to `~/.bashrc` or `~/.zshrc`:

```bash
# Create a new project from template
devtools-new() {
  if [ -z "$1" ]; then
    echo "Usage: devtools-new <project_name> [additional-copier-args]"
    return 1
  fi
  copier copy "$DEV_TOOLS_ROOT/template" "$1" --trust "${@:2}"
}

# Apply template to existing project (current directory)
devtools-apply() {
  copier copy "$DEV_TOOLS_ROOT/template" . --trust "$@"
}

# Update current project from template
devtools-update() {
  copier update --trust "$@"
}
```

Reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

**Usage examples:**

```bash
devtools-new my_python_app
devtools-new my_nodejs_app --answers-file my-answers.yml

cd MyExistingProject
devtools-apply

cd MyManagedProject
devtools-update
```

### PowerShell Functions

Add these functions to your PowerShell profile (`$PROFILE`):

```powershell
function devtools-new {
    param(
        [Parameter(Mandatory=$true, Position=0)]
        [string]$ProjectName,
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$AdditionalArgs
    )

    if (-not $env:DEV_TOOLS_ROOT) {
        Write-Error "DEV_TOOLS_ROOT environment variable not set"
        return
    }

    $templatePath = Join-Path $env:DEV_TOOLS_ROOT "template"
    copier copy $templatePath $ProjectName --trust @AdditionalArgs
}

function devtools-apply {
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$AdditionalArgs
    )

    if (-not $env:DEV_TOOLS_ROOT) {
        Write-Error "DEV_TOOLS_ROOT environment variable not set"
        return
    }

    $templatePath = Join-Path $env:DEV_TOOLS_ROOT "template"
    copier copy $templatePath . --trust @AdditionalArgs
}

function devtools-update {
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$AdditionalArgs
    )

    copier update --trust @AdditionalArgs
}
```

Reload your profile:

```powershell
. $PROFILE
```

**Usage examples:**

```powershell
devtools-new my_python_app
devtools-new my_nodejs_app --answers-file my-answers.yml

cd MyExistingProject
devtools-apply

cd MyManagedProject
devtools-update
```

### Verification

Test that your shortcuts work:

```bash
# Should show usage/error message
devtools-new

# Should create a test project (you can delete it after)
devtools-new test_project
```

### Customizing Command Names

You can use any command names you prefer. Simply rename the functions:

- `new_project` instead of `devtools-new`
- `dt-new` for brevity
- `copier-dev new` if you prefer subcommand-style

Just ensure the function names don't conflict with existing commands on your system.

## Prompt Model

Template prompts include:

- `project_name`
- `project_slug`
- `description`
- `language` (`python`, `nodejs`, `rust`, `godot`, `unreal`, `cpp`)
- `execution_mode` (`container`, `host`, `hybrid`)
- language-specific conditional prompts (`python_package_manager`, `node_package_manager`, `cpp_build_system`)
- Godot-only prompts (`godot_version`, `godot_test_framework`)

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
- `.github/skills/**`: copied only when destination files are missing
- `.github/prompts/*`: copied only when destination file is missing
- `.github/hooks/**`: copied only when destination files are missing
- `.vscode/mcp.json`: merged from shared + language overlay (project values win)
- Godot MCP scaffolds (`.vscode/mcp.godot.json`, `docker-compose.godot-mcp.yml`) copied when `language=godot`

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

For Godot projects, generated tasks also include host/hybrid workflow helpers:

- `run-godot`
- `godot-import`
- `godot-parse-check`
- `godot-export-debug`

## Security Defaults

Generated projects include:

- `.env.example` placeholders (no real secrets)
- `.gitignore` entries for `.env` and `.env.local`
- secret-free `.vscode/mcp.json` (environment variable references only)
- `.githooks/pre-commit` secret scan hook
- `.github/instructions/secrets-management.md`

## Available Agents

Generated projects include specialized AI agents in `.github/agents/` that can be invoked directly in VS Code Copilot. These agents are designed for specific workflows and include tool restrictions to ensure safe, focused operation.

### teacher

**Purpose**: Interactive step-by-step learning and tutorial workflows

**Invocation**: `@teacher walk me through implementing [feature]`

**Key Features**:

- Guides users through learning tasks one step at a time
- Defaults to pseudocode/high-level patterns to encourage learning-by-doing
- Provides production-ready code snippets when explicitly requested
- Includes verification instructions for each step (following agent verification contract)
- Can index new documentation sources when teaching topics without current docs
- Never executes changes directly; guides user through implementation

**Tools**: Read-only exploration (`read`, `search`, `glob`, `webSearch`) + docs-mcp operations (`search_docs`, `scrape_docs`, `refresh_version`)

**Use Cases**:

- Learning new language features or frameworks
- Understanding project architecture
- Implementing complex features step-by-step
- Debugging with guided problem-solving
- Establishing best practices through practice

### research-agent

**Purpose**: Evidence-based research using indexed documentation and web search

**Invocation**: `@research-agent compare [technology A] and [technology B]`

**Key Features**:

- Performs concise, source-backed comparisons and recommendations
- Prefers official documentation first
- Separates verified facts from opinions
- Cites sources and calls out trade-offs

**Tools**: Read-only exploration + docs-mcp search operations

**Use Cases**:

- Technology evaluation and comparison
- Finding best practices from official docs
- Understanding API capabilities and limitations
- Research without modifying code

### documentation-indexer

**Purpose**: Discovers and indexes official documentation into docs-mcp

**Invocation**: `@documentation-indexer index documentation for [library/framework]`

**Key Features**:

- Finds official documentation URLs
- Indexes documentation into local docs-mcp server
- Refreshes existing indexed versions
- Reports job status and completion

**Tools**: Web search + docs-mcp management operations (`scrape_docs`, `refresh_version`, `list_jobs`)

**Use Cases**:

- Adding documentation for new dependencies
- Keeping indexed docs current
- Preparing documentation before research or learning sessions

### Agent Customization

Agents are copied only when destination files are missing (see [Merge Behavior](#merge-behavior-preserved)), so projects can customize agents in `.github/agents/` without interference from template updates. To add custom agents, create new `.agent.md` files following the YAML frontmatter pattern (see existing agents for examples).

## Copilot Workflow Pack

Generated projects now include a Copilot-native workflow pack that recreates the main Superpowers-style development stages using standard VS Code customization primitives.

### Included custom agents

- `planner`: Design and task planning before implementation.
- `implementation`: Execute approved tasks with explicit verification.
- `reviewer`: Severity-first review focused on defects and regressions.

These are in addition to `teacher`, `research-agent`, and `documentation-indexer`.

For non-trivial work, these agents are intended to hand off through persisted docs as well as chat context:

- `docs/design/<feature>.md` for approved design decisions.
- `docs/plans/<feature>-plan.md` for executable task plans and verification steps.

### Included skills

Skills are copied to `.github/skills/` and can be invoked as slash commands or loaded automatically when relevant.

- `brainstorming`: Purpose: clarify requirements, alternatives, constraints, and success criteria before coding. Usage: run when a request is still high-level or ambiguous.
- `writing-plans`: Purpose: convert an approved design into small, verifiable implementation tasks. Usage: run after design approval and before coding starts.
- `test-driven-development`: Purpose: enforce red-green-refactor for behavior changes. Usage: run while implementing new or changed logic.
- `systematic-debugging`: Purpose: debug from evidence and hypotheses instead of guesswork. Usage: run when tests/build/runtime fail.
- `verification-before-completion`: Purpose: require explicit verification evidence before marking work done. Usage: run at the end of each meaningful task.
- `requesting-code-review`: Purpose: prepare a change for reviewer consumption with risk and verification context. Usage: run before requesting review.
- `using-git-worktrees`: Purpose: isolate parallel or risky work in dedicated worktrees/branches. Usage: run before starting multi-track work.
- `finishing-development-branch`: Purpose: close out a branch with final verification and cleanup. Usage: run when implementation and feedback are complete.

### Included prompt files

Prompt files are copied to `.github/prompts/` and provide quick entry points for common workflows.

- `/start-feature-design`: Purpose: kick off design and planning for a feature. Usage: first step for new feature work.
- `/implement-approved-plan`: Purpose: execute the approved plan in small verified steps. Usage: after plan approval.
- `/run-tdd-cycle`: Purpose: run one focused red-green-refactor cycle. Usage: during implementation of a specific behavior.
- `/review-implementation`: Purpose: run severity-first review against plan and risk areas. Usage: after implementation and before merge.
- `/index-documentation`: Purpose: discover and index official docs into docs-mcp. Usage: when docs are missing/outdated for current work.

### Included hook

A session-start hook is copied to `.github/hooks/workflow-session-start.json`.

Purpose: give the agent a brief reminder at the beginning of a chat session that the workflow pack exists and that durable handoff docs should live in `docs/design/` and `docs/plans/`.

What it does: it injects a short startup context message into the session. It does not edit files, run tests, or force the workflow by itself.

### How Stage Handoff Works

By default, handoff can use chat context, but this workflow pack now prefers durable file-based handoff for non-trivial work.

1. Stage 1 (`planner` or `/start-feature-design`) produces a design summary + task plan in chat.
2. Stage 1 should also persist the approved design to `docs/design/<feature>.md` and the task plan to `docs/plans/<feature>-plan.md`.
3. Stage 2 (`implementation` or `/implement-approved-plan`) uses those docs as the durable handoff source, plus current code and verification output.
4. Stage 3 (`reviewer` or `/review-implementation`) reviews implementation against the same saved design/plan docs and verification evidence.

Generated projects include starter folders for these artifacts:

- `docs/design/`
- `docs/plans/`

Optional PR/checklist notes can still be used for review criteria, but the design and plan docs should be the main handoff artifacts.

### Suggested flow

1. Run `/start-feature-design` or use `@planner`.
2. Save or update `docs/design/<feature>.md` and `docs/plans/<feature>-plan.md`.
3. Run `/implement-approved-plan` or use `@implementation`.
4. Run `/review-implementation` or use `@reviewer`.

## Adding a New Language

1. Add `fragments/languages/<lang>-settings.json`.
2. Add `fragments/languages/<lang>-extensions.json`.
3. Optionally add `fragments/languages/<lang>-keybindings.json`.
4. Add `instructions/languages/<lang>-conventions.md`.
5. Add `<lang>` to `language` choices and validator logic in `copier.yml`.
6. Update `.devcontainer/devcontainer.json.jinja` and `.vscode/tasks.json.jinja` if language needs special workflows.
