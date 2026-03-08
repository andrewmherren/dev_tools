param(
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Path $PSScriptRoot -Parent
$pythonScriptPath = Join-Path $repoRoot "scripts/sync-homepage-docs.py"

if (-not (Test-Path $pythonScriptPath)) {
    throw "Sync script not found: $pythonScriptPath"
}

$pythonCommand = ""
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCommand = "py -3"
} else {
    throw "Python is required. Install python3 and retry."
}

$quietArg = ""
if ($Quiet) {
    $quietArg = "--quiet"
}

Push-Location $repoRoot
try {
    Invoke-Expression "$pythonCommand scripts/sync-homepage-docs.py $quietArg"
} finally {
    Pop-Location
}
