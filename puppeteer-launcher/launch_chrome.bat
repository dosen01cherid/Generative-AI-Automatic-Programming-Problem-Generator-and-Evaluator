@echo off
REM Simple Chrome Launcher with WhatsApp Analytics Extension
REM No dependencies needed - just launches Chrome directly

cd /d "%~dp0"

REM Default paths
set CHROME_PATH=chrome-win\chrome.exe
set EXTENSION_PATH=..\whatsapp-analytics-extension
set ANALYTICS_PATH=..\analytics_for_problem.html
set PROFILE_DIR=chrome-profile

REM Check if CHROMIUM_PATH environment variable is set
if defined CHROMIUM_PATH (
    set CHROME_PATH=%CHROMIUM_PATH%
)

REM Check if Chrome exists
if not exist "%CHROME_PATH%" (
    echo ERROR: Chrome not found at: %CHROME_PATH%
    echo.
    echo Please either:
    echo 1. Download portable Chrome and extract to: chrome-win\
    echo    Download from: https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html
    echo 2. Set CHROMIUM_PATH environment variable
    echo    Example: set CHROMIUM_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
    echo.
    pause
    exit /b 1
)

REM Check if extension exists
if not exist "%EXTENSION_PATH%" (
    echo ERROR: Extension not found at: %EXTENSION_PATH%
    echo Make sure the whatsapp-analytics-extension folder exists
    echo.
    pause
    exit /b 1
)

REM Create profile directory if needed
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

echo Starting Chrome with WhatsApp Analytics extension...
echo.
echo Chrome: %CHROME_PATH%
echo Extension: %EXTENSION_PATH%
echo Profile: %PROFILE_DIR%
echo.

REM Parse arguments
set WHATSAPP_URL=https://web.whatsapp.com
set ANALYTICS_URL=file:///%CD:\=/%/%ANALYTICS_PATH:\=/%

set OPEN_WHATSAPP=1
set OPEN_ANALYTICS=1

:parse_args
if "%~1"=="--whatsapp-only" (
    set OPEN_ANALYTICS=0
    shift
    goto parse_args
)
if "%~1"=="--analytics-only" (
    set OPEN_WHATSAPP=0
    shift
    goto parse_args
)
if not "%~1"=="" (
    shift
    goto parse_args
)

REM Build Chrome command
set CHROME_CMD="%CHROME_PATH%" --load-extension="%EXTENSION_PATH%" --user-data-dir="%PROFILE_DIR%" --no-first-run --no-default-browser-check --start-maximized --allow-file-access-from-files --allow-file-access

REM Add URLs
if %OPEN_WHATSAPP%==1 set CHROME_CMD=%CHROME_CMD% "%WHATSAPP_URL%"
if %OPEN_ANALYTICS%==1 set CHROME_CMD=%CHROME_CMD% "%ANALYTICS_URL%"

echo ========================================
echo Chrome will open with:
if %OPEN_WHATSAPP%==1 echo   - WhatsApp Web
if %OPEN_ANALYTICS%==1 echo   - Analytics Dashboard
echo   - Extension loaded and active
echo ========================================
echo.
echo How to use:
echo 1. WhatsApp: Messages with progress reports will be captured
echo 2. Click the extension icon to see captured reports
echo 3. Click "Auto-Inject to Analytics" to send data
echo.
echo Launching Chrome...
echo.

REM Launch Chrome
start "" %CHROME_CMD%

echo Chrome launched successfully!
echo You can close this window - Chrome will keep running.
echo.
pause
