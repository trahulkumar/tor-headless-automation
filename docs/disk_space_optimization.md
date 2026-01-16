# Disk Space Optimization Guide (Moving to D:)

> [!WARNING]
> **DO NOT move the entire `C:\Users\{User}\AppData\Local` folder.**
> This folder contains system-critical configurations for Windows and nearly every installed application. Moving it will break your OS, Start Menu, and permissions.

Instead, use the targeted strategies below to move the "Big Three" space hogs: **Docker**, **UV/Pip**, and **AI Models (HuggingFace)**.

---

## 1. Moving Docker Storage (The Largest Consumer)
Docker on Windows uses a WSL 2 virtual hard disk file that grows indefinitely. You can verify its size at:
`%LOCALAPPDATA%\Docker\wsl\data\ext4.vhdx`

**Strategy**: Move the entire WSL distribution to the D: drive.

### Steps (Run in PowerShell as Administrator)

1.  **Prepare the destination**:
    ```powershell
    mkdir "D:\AppData\DockerData"
    ```
2.  **Stop Docker Desktop** completely (Right-click icon in tray > Quit Docker Desktop).
3.  **Shut down WSL**:
    ```powershell
    wsl --shutdown
    ```
4.  **Export current data** (This may take a while if large):
    ```powershell
    wsl --export docker-desktop-data "D:\AppData\DockerData\docker-data.tar"
    ```
5.  **Unregister the old distribution** (This deletes it from C:):
    ```powershell
    wsl --unregister docker-desktop-data
    ```
6.  **Import to new location**:
    ```powershell
    wsl --import docker-desktop-data "D:\AppData\DockerData" "D:\AppData\DockerData\docker-data.tar" --version 2
    ```
7.  **Clean up**:
    ```powershell
    del "D:\AppData\DockerData\docker-data.tar"
    ```
8.  **Restart Docker Desktop**. It will now use the D: drive.

---

## 2. Moving Cache Folders (uv, pip, HuggingFace)
Tools like `uv`, `pip`, and AI libraries store gigabytes of cached whls and models.
**Strategy**: Use **Directory Junctions**. This essentially creates a "wormhole" so the software *thinks* it's writing to C:, but the files actually land on D:.

### Steps (Run in PowerShell as Administrator)

**1. Create Destination Folder**
```powershell
mkdir "D:\AppData\AI_Cache"
```

**2. Example: Moving `uv` Cache**
*   **Source**: `C:\Users\trahu\AppData\Local\uv`
*   **Destination**: `D:\AppData\AI_Cache\uv`

```powershell
# 1. Close any running python/uv processes

# 2. Move existing data to D:
# (Note: Use Robocopy for safe move, or just Cut/Paste in Explorer)
robocopy "C:\Users\trahu\AppData\Local\uv" "D:\AppData\AI_Cache\uv" /E /MOVE /XJ

# 3. Create the Junction (The Magic Link)
mklink /J "C:\Users\trahu\AppData\Local\uv" "D:\AppData\AI_Cache\uv"
```
*Result: `uv` still looks at C:, but uses disk space on D:.*

---

## 3. Moving AI Models (HuggingFace)
If you use `transformers` or `diffusers`, this is usually huge.
*   **Source**: `C:\Users\trahu\.cache\huggingface`
*   **Destination**: `D:\AppData\AI_Cache\huggingface`

```powershell
# 1. Move data
robocopy "C:\Users\trahu\.cache\huggingface" "D:\AppData\AI_Cache\huggingface" /E /MOVE /XJ

# 2. Create Junction
mklink /J "C:\Users\trahu\.cache\huggingface" "D:\AppData\AI_Cache\huggingface"
```

---

## Summary Checklist
- [ ] **Docker**: Moved to `D:\AppData\DockerData`
- [ ] **uv**: Linked to `D:\AppData\AI_Cache\uv`
- [ ] **HuggingFace**: Linked to `D:\AppData\AI_Cache\huggingface`
