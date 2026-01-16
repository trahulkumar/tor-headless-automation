"""
Linux/Docker version of the Tor Browser Automation Script.
Adapted for running inside Xvfb virtual desktop.
"""

import subprocess
import time
import os
import psutil
from dotenv import load_dotenv
import pyautogui

# Load environment variables
load_dotenv()

# In Docker, we use the pre-installed Tor Browser path
TOR_BROWSER_PATH = os.getenv("TOR_BROWSER_DOCKER_PATH", "/app/tor-browser/Browser/start-tor-browser")

def close_existing_instances():
    """Find and close any existing instances of Tor Browser on Linux."""
    print("Checking for existing Tor Browser instances...")
    # Linux Tor Browser usually has processes named 'firefox' or 'firefox.real'
    target_names = ["firefox", "firefox.real"]
    found = False
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in target_names:
                print(f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})...")
                proc.terminate()
                proc.wait(timeout=5)
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue
    
    if found:
        print("✓ Existing instances closed.")
        time.sleep(2)
    else:
        print("No existing instances found.")

# Configuration
TARGET_URLS_STRING = os.getenv("TARGET_URLS", "")
TARGET_URLS = [url.strip() for url in TARGET_URLS_STRING.split(",") if url.strip()]

INITIAL_WAIT_TIME = int(os.getenv("INITIAL_WAIT_TIME", "20")) # Longer for Docker
PAGE_LOAD_WAIT = int(os.getenv("PAGE_LOAD_WAIT", "15")) # Longer for Docker
DOWNLOAD_WAIT = int(os.getenv("DOWNLOAD_WAIT", "5"))
URL_SWITCH_WAIT = int(os.getenv("URL_SWITCH_WAIT", "5"))

# PyAutoGUI settings for Linux
pyautogui.FAILSAFE = False # No mouse corner in headless
pyautogui.PAUSE = 1.0     # More relaxed for virtual desktop

def open_tor_browser():
    """Launch Tor Browser inside the container."""
    close_existing_instances()
    
    print(f"Launching Tor Browser (Linux) from: {TOR_BROWSER_PATH}")
    
    # In Linux TB bundle, we run the start script
    subprocess.Popen([TOR_BROWSER_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Waiting {INITIAL_WAIT_TIME}s for Tor Browser initialization...")
    
    # Wait half the time, then try to connect, then wait the rest
    time.sleep(10)
    
    print("Attempting to force connection (clicking 'Connect')...")
    # Sometimes Tor Browser needs a nudge to connect even if configured to auto-connect
    # We try to click a generic 'Connect' button location or search for it
    
    # Strategy 1: Search for "Connect" text and press Enter
    try:
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.typewrite('Connect', interval=0.1)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('esc')
        time.sleep(1)
        pyautogui.press('enter') # Click it if found
        print("✓ Sent 'Connect' command.")
    except Exception as e:
        print(f"Warning: Could not force connect: {e}")

    # Wait the remaining time
    remaining_wait = max(0, INITIAL_WAIT_TIME - 15)
    print(f"Waiting {remaining_wait}s for network connection...")
    time.sleep(remaining_wait)
    
    print("✓ Tor Browser started.")

def navigate_to_url(url, new_tab=False):
    """Navigate to a URL using keyboard shortcuts."""
    print(f"Navigating to: {url} {'(New Tab)' if new_tab else ''}")
    
    if new_tab:
        pyautogui.hotkey('ctrl', 't')
        time.sleep(2)
    
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    
    pyautogui.typewrite(url + '\n', interval=0.05)
    print(f"Waiting {PAGE_LOAD_WAIT}s for page load...")
    time.sleep(PAGE_LOAD_WAIT)

def click_buttons_on_page():
    """Click Preview and Download buttons using keyboard searching."""
    print("Preparing page (scrolling inside Docker)...")
    
    # 0. Scroll to bottom slowly
    print("Scrolling to bottom...")
    for i in range(10):
        pyautogui.press('pagedown')
        time.sleep(0.5)
    
    # Go back to top
    print("Returning to top...")
    pyautogui.press('home')
    time.sleep(1.5)

    print("Looking for buttons on the page...")
    
    # 1. Search and Click "Preview"
    print("Searching for 'Preview' on page...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.typewrite('Preview', interval=0.1)
    time.sleep(1.5)
    pyautogui.press('esc')
    time.sleep(1)
    
    print("✓ Triggering Preview (Enter)...")
    pyautogui.press('enter')
    time.sleep(3) # Wait for preview to open/expand
    
    # 2. Search and Click "Download"
    print("Searching for 'Download' on page...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.typewrite('Download', interval=0.1)
    time.sleep(1.5)
    pyautogui.press('esc')
    time.sleep(1)
    
    print("✓ Triggering Download (Enter)...")
    pyautogui.press('enter')
    time.sleep(DOWNLOAD_WAIT)

def main():
    print("="*60)
    print("TOR DOCKER AUTOMATION (Headless Mode)")
    print("="*60)
    
    if not TARGET_URLS:
        print("ERROR: No TARGET_URLS found in .env")
        return

    try:
        open_tor_browser()
        
        for i, url in enumerate(TARGET_URLS, 1):
            print(f"\n[{i}/{len(TARGET_URLS)}] Processing...")
            navigate_to_url(url, new_tab=(i > 1))
            click_buttons_on_page()
            
            if i < len(TARGET_URLS):
                time.sleep(URL_SWITCH_WAIT)
                
        print("\n✓ All URLs processed successfully!")
        print("Note: In Docker, files are saved to the mapped 'downloads' folder.")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
