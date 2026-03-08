#!/usr/bin/env sh
set -eu

if ! command -v git >/dev/null 2>&1; then
  exit 0
fi

staged_files="$(git diff --cached --name-only --diff-filter=ACM)"
if [ -z "$staged_files" ]; then
  exit 0
fi

pattern='(SONARQUBE_TOKEN\s*=\s*[^$]|GITHUB_TOKEN\s*=\s*[^$]|API[_-]?KEY\s*=\s*[^$]|SECRET\s*=\s*[^$]|PASSWORD\s*=\s*[^$]|sqp_[A-Za-z0-9]+)'

if git diff --cached | grep -E -i "$pattern" >/dev/null 2>&1; then
  echo "❌ Potential secret detected in staged changes."
  echo "   Move secrets to .env/.env.local and reference via environment variables."
  exit 1
fi

exit 0
