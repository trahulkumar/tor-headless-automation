@echo off
SETLOCAL EnableDelayedExpansion

REM ============================================================
REM Tor Browser Automation Repeater
REM Mode: Every 2 minutes
REM ============================================================

echo ============================================================
echo TOR BROWSER AUTOMATION REPEATER
echo ============================================================
echo This script will run the automation every 2 minutes.
echo Using Python-based repeater for maximum reliability.
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: uv is not installed!
    timeout /t 5
    exit /b 1
)

echo Installing/syncing dependencies...
uv sync

echo.
echo Running REPEATER automation...
uv run tor-repeat


echo.
echo Cleaning up leftover processes...
taskkill /IM "tor.exe" /F >nul 2>&1
echo Cleanup complete.

echo.
echo ============================================================
echo Script completed!
echo ============================================================
