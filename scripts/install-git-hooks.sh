#!/usr/bin/env sh
set -e

git config core.hooksPath .githooks
printf '%s\n' "Configured git hooks path: .githooks"
printf '%s\n' "Pre-commit hook will keep homepage/docs markdown in sync."
