# Rust Conventions

- Keep `cargo fmt` and `clippy` clean.
- Prefer explicit error types and `Result` returns.
- Separate binary crate wiring from library logic.
- Keep unsafe blocks small and documented.

## Verification Commands

- **Test**: `cargo test`
- **Lint**: `cargo clippy`
- **Build**: `cargo build` or `cargo build --release`
- **Format check**: `cargo fmt --check`
