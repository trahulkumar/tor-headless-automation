# 🧅 Tor Browser Automation Suite

A robust, privacy-focused automation tool for managing Tor Browser workflows. This suite supports both **local Windows execution** and **headless Docker execution**, allowing you to automate repetitive tasks (like downloading files) while maintaining the security of the Tor network.

---

## 🏗️ Architecture

### 1. Local Mode (Windows)
*   **Engine**: `src/tor_browser_automation/main.py`
*   **Mechanism**: Uses `pyautogui` to simulated keyboard/mouse input directly on your Windows desktop.
*   **Pros**: Easiest to debug, visible execution.
*   **Cons**: Occupies your mouse/keyboard; cannot use computer while running.

### 2. Docker Mode (Headless)
*   **Engine**: `src/tor_browser_automation/docker_main.py`
*   **Environment**: Runs inside a Linux container (Debian-based Python slim image).
*   **Mechanism**:
    *   **Xvfb**: Creates a virtual framebuffer (fake monitor) inside the container.
    *   **Fluxbox**: Lightweight window manager to handle application windows.
    *   **VNC (x11vnc)**: Exposes the virtual desktop so you can watch it.
    *   **noVNC**: Web-based viewer to see the desktop in your browser.
*   **Pros**: Runs in background; does NOT interfere with your mouse; totally isolated.
*   **Cons**: Requires Docker Desktop.

### 3. The Repeater Logic
*   **Engine**: `src/tor_browser_automation/repeater.py`
*   **Function**: Wrapper script that runs the main automation in a loop.
*   **Intelligence**: Automatically detects if it is running in Docker or Local and selects the correct automation engine.
*   **Configuration**: Interval and Cycle count are configurable via `.env`.

---

## 🚀 Getting Started

### 1. Prerequisites
*   **Docker Desktop**: Must be installed and running.
*   **Python (uv)**: We use `uv` for fast dependency management.
    ```powershell
    irm https://astral.sh/uv/install.ps1 | iex
    ```

### 2. Configuration (`.env`)
Create a `.env` file in the root directory. Key settings:

```ini
# --- Target URLs ---
TARGET_URLS=https://example.com/file1, https://example.com/file2

# --- Timing (Seconds) ---
INITIAL_WAIT_TIME=45   # Time for Tor to connect (longer for Docker)
PAGE_LOAD_WAIT=15      # Time for page render
REPEATER_WAIT_TIME=120 # Wait time between cycles (2 minutes)
REPEATER_CYCLES=30     # Number of loops to run (30 * 2m = 60m total)
```

---

## 🛠️ Docker Workflow (Recommended)

Follow this 2-step process for a perfect setup.

### Step 1: Manual Configuration (One-Time Setup)
Because Tor Browser requires a specialized setup (bridges, security levels), we use a dedicated "Setup Mode" to save your profile permanently.

1.  Run the setup script:
    ```powershell
    .\docker\run_docker_setup.bat
    ```
2.  Wait for the **SUCCESS** message.
3.  Open your browser to: [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html)
4.  Click **Connect**. You will see a virtual desktop.
5.  Open the Terminal inside VNC (Right Click -> Applications -> Shell -> bash) or use the shortcut.
6.  Run the browser:
    ```bash
    /app/tor-browser-bundle/Browser/start-tor-browser
    ```
7.  **Configure**: Set your Security Level, Bridges, and check "Always Connect".
8.  **Close Tor Browser** inside the VNC window.
9.  Return to your Windows Terminal and **press any key** to clean up and save changes.

> **Note**: Your settings are saved to `d:\AI\Git\agents\web_landing\tor_profile` on your host machine.

### Step 2: Run Automation
Once configured, run the repeater. It will spin up a fresh container using your saved profile.

```powershell
.\auto_repeat_in_docker.bat
```

*   **View Progress**: [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html)
*   **Stop**: Press `Ctrl+C` in the terminal. The script will automatically stop and remove the container.
*   **Downloads**: Files appear in `d:\AI\Git\agents\web_landing\downloads_docker`.

---

## 💻 Local Workflow (Alternative)

If you prefer running it directly on your desktop:

1.  Edit `.env` to point `TOR_BROWSER_PATH` to your Windows installation.
2.  Run the automation:
    ```powershell
    .\auto_repeat_in_local.bat
    ```
    *(Remember: Do not touch your mouse while this is running!)*

---

## 🔧 Troubleshooting

### "Invalid file request tor_profile/lock"
*   **Cause**: Docker tried to build the image while a `lock` file existed in your profile folder.
*   **Fix**: We added `.dockerignore` to exclude `tor_profile` from the build. Ensure `.dockerignore` exists.

### "Run as root" Error
*   **Fix**: Already patched in `Dockerfile`. We modify the Tor Browser script during the build to allow root execution:
    `sed -i 's/id -u" -eq 0/id -u" -eq 1/g' ...`

### Settings Not Saving
*   **Fix**: Ensure your `docker-compose.yml` mounts the PARENT directory:
    `- ../tor_profile:/app/tor-browser-bundle/Browser/TorBrowser/Data/Browser`
    If it mounts just `profile.default`, `profiles.ini` is lost, and Tor Browser creates a new profile on every restart.

### VNC Screen is Blank
*   **Fix**: The `entrypoint.sh` starts Fluxbox and VNC automatically. Give it 10-15 seconds. If it stays blank, check logs:
    `docker logs tor_bg_automation`

---

## 📁 Directory Structure

```text
web_landing/
├── src/
│   └── tor_browser_automation/
│       ├── main.py          # Local Automation Engine
│       ├── docker_main.py   # Docker Automation Engine
│       └── repeater.py      # Universal Loop Coordinator
├── docker/
│   ├── Dockerfile           # Image definition (Python + Xvfb + Tor)
│   ├── docker-compose.yml   # Volume & Port mapping
│   └── run_docker_setup.bat # Setup Script
├── tor_profile/             # SAVED USER DATA (Synced with Docker)
├── downloads_docker/        # DOWNLOADED FILES (Synced with Docker)
├── auto_repeat_in_docker.bat # MAIN ENTRY POINT
└── .env                     # Configuration
```
