# WhatsApp Analytics Launcher for Windows (PowerShell)
# Starts Chrome with extension loaded via Puppeteer

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Starting WhatsApp Analytics..." -ForegroundColor Green
node launch.js $args
