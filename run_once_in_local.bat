@echo off
REM Run the SIMPLE Tor Browser automation (PyAutoGUI - No Selenium)
REM This works with Tor Browser without compatibility issues!

echo ============================================================
echo TOR BROWSER SIMPLE AUTOMATION (PyAutoGUI)
echo ============================================================
echo.
echo This script uses PyAutoGUI to automate Tor Browser.
echo It does NOT have the Selenium compatibility issues!
echo.
echo IMPORTANT: Do NOT move your mouse during automation!
echo Move mouse to top-left corner to abort (FAILSAFE).
echo.
timeout /t 5

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
echo Running SIMPLE automation...
uv run tor-automate

echo.
echo ============================================================
echo Script completed!
echo ============================================================
