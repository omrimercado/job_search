@echo off
chcp 65001 >nul
echo ========================================
echo   Job Search Automation - Quick Start
echo ========================================
echo.
echo Choose an option:
echo [1] Run once (fetch jobs now)
echo [2] Run on schedule (every 24 hours)
echo [3] Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Running job search...
    python main.py --once
    echo.
    echo Done! Check jobs_output.html in your browser.
    pause
)

if "%choice%"=="2" (
    echo.
    echo Starting scheduled job search (every 24 hours)...
    echo Press Ctrl+C to stop
    python main.py --schedule
)

if "%choice%"=="3" (
    exit
)
