# Godot Conventions

- Keep scene and script naming consistent.
- Favor small reusable scenes over large monolith scenes.
- Store project settings in text mode for reviewability.
- Keep assets and scripts in predictable folders.
- Prefer typed GDScript (`: Type` and `-> ReturnType`) in gameplay-critical scripts.
- Prefer connecting signals in code for reproducible reviews when using external editors.

## Verification Commands

- **Parse check (official CLI)**: `godot --headless --path . --script res://<script>.gd --check-only`
- **Import check (official CLI)**: `godot --headless --path . --import`
- **Export check (official CLI)**: `godot --headless --path . --export-debug "<Preset Name>" build/<artifact>`
- **Test**: GDScript unit testing with GUT or project-specific framework
- **Lint**: No first-party GDScript linter in Godot CLI; use typed GDScript + editor warnings and optional third-party tools
- **Editor validation (required)**: Open project in Godot editor and validate scene load, node wiring, animation state, physics behavior, and import warnings

## Agent Workflow Notes

- Agents can safely automate code changes, docs lookup, and CLI checks.
- Agents cannot directly manipulate the Godot GUI editor; keep manual validation checkpoints in every plan.
- When reporting verification, separate CLI checks from editor-only checks.
