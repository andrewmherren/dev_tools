$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Path $PSScriptRoot -Parent
Push-Location $repoRoot

try {
    git config core.hooksPath .githooks
    Write-Host "Configured git hooks path: .githooks"
    Write-Host "Pre-commit hook will keep homepage/docs markdown in sync (cross-platform runtime detection)."
} finally {
    Pop-Location
}
