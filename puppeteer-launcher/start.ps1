#!/usr/bin/env pwsh
# WhatsApp Analytics Launcher - PowerShell Script
# Installs dependencies and launches Chrome with extension

$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion"
} catch {
    Write-Error "ERROR: Python is not installed or not in PATH"
    Write-Host "Please install Python 3.7+ from https://www.python.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is installed
try {
    pip --version | Out-Null
} catch {
    Write-Error "ERROR: pip is not installed"
    Write-Host "Please install pip or reinstall Python with pip included"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
try {
    python -c "import pyppeteer" 2>&1 | Out-Null
} catch {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "ERROR: Failed to install dependencies"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Launch the browser
Write-Host ""
python launch.py $args

if ($LASTEXITCODE -ne 0) {
    Read-Host "Press Enter to exit"
}
