# Read-only Windows environment inventory for WO-AGENT-00 / WO-01.
# Does not print tokens, credential files, environment variables or user directories.
$ErrorActionPreference = 'Continue'
Write-Output '== OS =='
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber
Write-Output '== Hardware =='
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Write-Output '== NVIDIA GPU (if available) =='
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
}
else {
    Write-Output 'nvidia-smi: NOT_INSTALLED_OR_UNAVAILABLE'
}
Write-Output '== Tool availability (no login performed) =='
foreach ($name in @('git', 'python', 'py', 'codex', 'grok', 'agy', 'wsl', 'docker', 'ollama')) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        Write-Output "$name : NOT_FOUND"
    }
    else {
        Write-Output "$name : FOUND"
    }
}
Write-Output '== WSL status (if available) =='
if (Get-Command wsl -ErrorAction SilentlyContinue) {
    & wsl --status
}
Write-Output 'Inventory only: no authentication, installation or runtime tests were performed.'
