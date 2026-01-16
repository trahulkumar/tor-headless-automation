# ✅ WORKING SOLUTION: Simple Automation for Tor Browser

## Why This Works

**Problem:** Selenium + Tor Browser = Incompatible ❌  
**Solution:** PyAutoGUI + Tor Browser = Works Perfect! ✅

The simple script uses **keyboard automation** (Ctrl+L, type URL, Enter, etc.) instead of Selenium, so it has **zero compatibility issues** with Tor Browser!

---

## 🚀 Quick Start

### Run the Simple Automation

```bash
run_simple_automation.bat
```

**OR manually:**
```bash
uv run tor-automate
```

---

## ⚠️ Important Rules

1. **Don't move your mouse** during automation
2. **Don't click anything** while it's running  
3. Move mouse to **top-left corner to abort** (FAILSAFE)
4. Tor Browser window must be **visible** (not minimized)

---

## How It Works

1. **Self-Cleanup**: Finds and closes any existing Tor Browser (`firefox.exe`) windows.
2. **Browser Launch**: Launches a fresh Tor Browser instance.
3. **Multi-Tab Execution**:
   - For each URL in `.env`:
     - Opens a new tab (`Ctrl+T`) if needed.
     - Presses `Ctrl+L` (focus address bar).
     - Types the URL and presses `Enter`.
     - Waits for page load.
     - Uses `Ctrl+F` to find "Download" and clicks it.
4. **Summary**: Shows success/failure count at the end.

---

## Comparison

| Feature | Selenium Version | Simple Version (PyAutoGUI) |
|---------|-----------------|----------------------------|
| **Works with Tor Browser** | ❌ No | ✅ Yes |
| **Requires GeckoDriver** | ✅ Yes | ❌ No |
| **Multi-URL Support** | ✅ Yes | ✅ Yes |
| **Requires mouse control** | ❌ No | ✅ Yes |
| **Reliability** | Complex | Simple |

---

## Files

- **Source Code:** `src/tor_browser_automation/main.py`
- **Runner:** `run_simple_automation.bat`
- **Config:** `.env` (same configuration file)
