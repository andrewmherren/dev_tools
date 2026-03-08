#!/usr/bin/env sh
set -e

if command -v python3 >/dev/null 2>&1; then
  python3 scripts/sync-homepage-docs.py "$@"
elif command -v python >/dev/null 2>&1; then
  python scripts/sync-homepage-docs.py "$@"
else
  echo "sync-homepage-docs.sh requires python3 or python" >&2
  exit 1
fi
