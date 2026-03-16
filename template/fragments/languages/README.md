# Language-Specific Fragments

This directory contains language-specific VS Code configuration fragments that are merged into generated projects.

## Extension Recommendations

### Testing Extension Strategy

Testing extensions were added selectively based on ecosystem maturity and integration quality:

**Extensions Added:**

- **Python** (`python-extensions.json`): `ryanluker.vscode-coverage-gutters` - Universal coverage visualization for pytest-cov, coverage.py (3.8M+ downloads)
- **Node.js** (`nodejs-extensions.json`): `orta.vscode-jest` - Official Jest test runner with inline results and debugging (9M+ downloads)
- **C++** (`cpp-extensions.json`): `matepek.vscode-catch2-test-adapter` - Test adapter for Catch2, Google Test, doctest (440K+ downloads)

**Extensions Intentionally Not Added:**

- **Rust** (`rust-extensions.json`): `rust-analyzer` already provides excellent built-in test support with inline test running and debugging
- **Godot** (`godot-extensions.json`): Limited VS Code testing ecosystem; GUT (Godot Unit Test) integration is project-specific and not universally applicable
- Godot defaults intentionally stay minimal: `godot-tools` plus task-level guidance for official CLI checks and optional GUT setup
- **Unreal** (`unreal-extensions.json`): Testing via built-in Automation Framework accessed through Unreal Editor; minimal VS Code integration available

## File Types

- `*-extensions.json`: Recommended VS Code extensions
- `*-settings.json`: Language-specific VS Code settings
- `*-keybindings.json`: Language-specific keyboard shortcuts (rare; currently only Unreal)
- `godot-mcp.json`: Godot-only MCP overlay merged into `.vscode/mcp.json`

## Merge Behavior

These fragments are merged via `tasks/merge_and_setup.py`:

- **Extensions**: Union + deduplicate by extension ID
- **Settings**: Deep object merge with project values winning on conflicts
- **Keybindings**: Union + deduplicate by command; project bindings win
