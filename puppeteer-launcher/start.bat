@echo off
REM WhatsApp Analytics Launcher - Windows Batch Script
REM Installs dependencies and launches Chrome with extension

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    echo Please install pip or reinstall Python with pip included
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import pyppeteer" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Launch the browser
echo.
python launch.py %*

pause
