@echo off
echo Starting Problem Creator (Offline Version)...
echo.
echo Opening browser in 2 seconds...
timeout /t 2 /nobreak > nul
start http://localhost:8000/create_problem_offline_embedded.html
cd /d "%~dp0"
python -m http.server 8000
