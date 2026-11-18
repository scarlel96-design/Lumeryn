# Lumeryn WO preflight for Windows PowerShell (no installation or login).
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^(WO-[A-Z0-9-]+|FT-[0-9]{2}|REL-[0-9]{2})$')]
    [string]$WorkOrder
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $python = Get-Command py -ErrorAction SilentlyContinue
    if ($null -ne $python) {
        & py -3.12 scripts/verify_project.py read --wo $WorkOrder
    }
    else {
        & python scripts/verify_project.py read --wo $WorkOrder
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'Project document preflight failed. Do not start implementation.'
    }
    Write-Output 'Complete: required documents printed. The agent must read them and write a start report.'
}
finally {
    Pop-Location
}
