@echo off
SETLOCAL EnableDelayedExpansion

REM ============================================================
REM Tor Browser Docker SETUP Mode
REM ============================================================

echo ============================================================
echo TOR BROWSER DOCKER SETUP MODE
echo ============================================================
echo This script starts the Docker environment but NOT the automation.
echo Use this to manually configure bridges, security, etc.
echo.
echo 1. Wait for SUCCESS message.
echo 2. Connect via VNC to localhost:5900
echo 3. Open terminal in VNC and run: ./tor-browser-bundle/Browser/start-tor-browser
echo 4. Close the VNC window when done.
echo.

REM Check if Docker is installed
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not installed!
    timeout /t 5
    exit /b 1
)

echo Starting Docker in SETUP mode (no automation)...
REM Override the entrypoint to just keep the container alive with VNC
docker-compose -f docker/docker-compose.yml run -d --name tor_setup --service-ports tor-automation tail -f /dev/null

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start setup container.
    timeout /t 5
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS: Setup container is running!
echo ============================================================
echo Connect via Web Browser: http://localhost:6080/vnc.html
echo Connect via VNC Viewer: localhost:5900
echo.
echo Inside the VNC terminal, type:
echo /app/tor-browser-bundle/Browser/start-tor-browser
echo.
echo After you finish your settings and close the browser,
echo PRESS ANY KEY to stop and clean up the setup container.
echo.
pause
echo Stopping and removing setup container...
docker stop tor_setup
docker rm tor_setup
echo Done.
