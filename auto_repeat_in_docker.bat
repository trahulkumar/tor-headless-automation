@echo off
SETLOCAL EnableDelayedExpansion

REM ============================================================
REM Tor Browser Docker Automation Runner
REM ============================================================

echo ============================================================
echo TOR BROWSER DOCKER AUTOMATION
echo ============================================================
echo This script will launch the automation in a background 
echo Docker container with its own virtual desktop.
echo.

REM Check if Docker is installed
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not installed or not in PATH!
    timeout /t 5
    exit /b 1
)

echo Starting Docker container...
docker-compose -f docker/docker-compose.yml up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start Docker container.
    echo Make sure Docker Desktop is RUNNING and green.
    timeout /t 5
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS: Automation is now running!
echo ============================================================
echo.
echo View live progress (Browser): http://localhost:6080/vnc.html
echo View live progress (VNC Client): localhost:5900
echo.
echo [To STOP the automation and clean up Docker, press Ctrl+C]
echo.

REM Wait for the container to finish or user to interrupt
docker logs -f tor_bg_automation

echo.

echo Stopping automation and cleaning up...
docker-compose -f docker/docker-compose.yml down

echo.
echo Shutting down Docker Desktop to save resources...
taskkill /IM "Docker Desktop.exe" /F >nul 2>&1
taskkill /IM "com.docker.backend.exe" /F >nul 2>&1
taskkill /IM "dockerd.exe" /F >nul 2>&1
echo Docker Desktop has been shut down.
echo Done.
