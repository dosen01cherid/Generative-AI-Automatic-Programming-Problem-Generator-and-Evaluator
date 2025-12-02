@echo off
REM WhatsApp Analytics Launcher for Windows
REM Starts Chrome with extension loaded via Puppeteer

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

echo Starting WhatsApp Analytics...
node launch.js %*
