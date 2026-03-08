# C++ Conventions

- Keep headers minimal and include what you use.
- Prefer RAII and smart pointers over manual ownership.
- Keep compiler warnings enabled and treated seriously.
- Use `tasks.json` build tasks as the canonical local workflow.

## Verification Commands

- **Test**: Project-specific (e.g., `ctest`, `./build/tests`)
- **Build**: Use VS Code build task or `cmake --build build`
- **Lint**: `clang-tidy` or project-configured linter
- Note: Verification commands vary by build system; check tasks.json.
