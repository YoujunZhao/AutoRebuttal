param(
    [string]$Destination = (Join-Path $HOME ".claude/skills/super-rebuttal")
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path (Join-Path $root "skill") "super-rebuttal"
$installer = Join-Path (Join-Path $source "scripts") "install_skill.py"

if (-not (Test-Path -LiteralPath $installer)) {
    throw "Missing install helper: $installer"
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $installer --source $source --destination $Destination
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $installer --source $source --destination $Destination
} else {
    throw "Python 3 is required to install SuperRebuttal."
}

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Installed SuperRebuttal to $Destination"
