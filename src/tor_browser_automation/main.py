"""
Simple Tor Browser Automation Script using PyAutoGUI
This version uses keyboard/mouse automation instead of Selenium.
Works perfectly with Tor Browser - no compatibility issues!
Configured via .env file.
"""

import subprocess
import time
import os
import psutil
from dotenv import load_dotenv
import pyautogui

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
TOR_BROWSER_PATH = os.getenv("TOR_BROWSER_PATH")

def close_existing_instances(process_name="firefox.exe"):
    """Find and close any existing instances of Tor Browser."""
    print(f"Checking for existing instances of {process_name}...")
    found = False
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # Tor Browser runs as firefox.exe but its path usually contains 'Tor Browser'
            if proc.info['name'].lower() == process_name.lower():
                exe_path = proc.info['exe']
                if exe_path and 'Tor Browser' in exe_path:
                    print(f"Terminating existing Tor Browser process (PID: {proc.info['pid']})...")
                    proc.terminate()
                    proc.wait(timeout=5)
                    found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue
    
    if found:
        print("✓ Existing instances closed.")
        time.sleep(2)  # Wait for cleanup
    else:
        print("No existing Tor Browser instances found.")

# Parse multiple URLs from comma-separated string
TARGET_URLS_STRING = os.getenv("TARGET_URLS", "")
TARGET_URLS = [url.strip() for url in TARGET_URLS_STRING.split(",") if url.strip()]

INITIAL_WAIT_TIME = int(os.getenv("INITIAL_WAIT_TIME", "10"))
PAGE_LOAD_WAIT = int(os.getenv("PAGE_LOAD_WAIT", "8"))
DOWNLOAD_WAIT = int(os.getenv("DOWNLOAD_WAIT", "3"))
URL_SWITCH_WAIT = int(os.getenv("URL_SWITCH_WAIT", "2"))

# PyAutoGUI safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.5  # Pause between actions


def open_tor_browser():
    """Launch Tor Browser and wait for it to be ready. Closes existing instances first."""
    close_existing_instances()
    
    print(f"Launching Tor Browser from: {TOR_BROWSER_PATH}")
    
    if not os.path.exists(TOR_BROWSER_PATH):
        raise FileNotFoundError(f"Tor Browser not found at: {TOR_BROWSER_PATH}")
    
    subprocess.Popen([TOR_BROWSER_PATH])
    print(f"Waiting {INITIAL_WAIT_TIME}s for Tor Browser to start...")
    time.sleep(INITIAL_WAIT_TIME)
    print("✓ Tor Browser should be ready")


def navigate_to_url(url, new_tab=False):
    """Navigate to a URL using keyboard shortcuts. Optionally opens a new tab first."""
    print(f"Navigating to: {url} {'(New Tab)' if new_tab else ''}")
    
    if new_tab:
        # Open new tab (Ctrl+T)
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
    
    # Focus address bar (Ctrl+L)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    
    # Type URL slowly to ensure accuracy
    pyautogui.typewrite(url, interval=0.02)
    time.sleep(0.5)
    
    # Press Enter to navigate
    pyautogui.press('enter')
    print(f"Waiting {PAGE_LOAD_WAIT}s for page to load...")
    time.sleep(PAGE_LOAD_WAIT)


def click_buttons_on_page():
    """Click Preview and Download buttons using keyboard searching."""
    print("Preparing page (scrolling)...")
    
    # 0. Scroll to bottom slowly
    print("Scrolling to bottom...")
    for i in range(8):
        pyautogui.press('pagedown')
        time.sleep(0.3)
    
    # Go back to top
    print("Returning to top...")
    pyautogui.press('home')
    time.sleep(1)

    print("Looking for buttons on the page...")
    
    # 1. Search and Click "Preview"
    print("Searching for 'Preview' button...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.typewrite('Preview', interval=0.05)
    time.sleep(1) # Wait for highlight
    pyautogui.press('esc') # Close find - focus stays on first match
    time.sleep(0.5)
    
    print("✓ Triggering Preview (Enter)...")
    pyautogui.press('enter')
    time.sleep(2) # Wait for preview to open/expand
    
    # 2. Search and Click "Download"
    print("Searching for 'Download' button...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.typewrite('Download', interval=0.05)
    time.sleep(1) # Wait for highlight (don't press Enter here, it skips the first match)
    pyautogui.press('esc') # Close find - focus stays on first match
    time.sleep(0.5)
    
    print("✓ Triggering Download (Enter)...")
    pyautogui.press('enter')
    time.sleep(DOWNLOAD_WAIT)


def process_url(url, index, total, is_first=False):
    """Process a single URL."""
    print(f"\n{'='*60}")
    print(f"Processing URL {index}/{total}")
    print(f"{'='*60}")
    
    try:
        # Open in new tab if not the first URL
        navigate_to_url(url, new_tab=not is_first)
        click_buttons_on_page()
        print(f"✓ Completed URL {index}/{total}")
        return True
    except Exception as e:
        print(f"✗ Error processing URL {index}/{total}: {e}")
        return False


def main():
    """Main automation function."""
    print("="*60)
    print("TOR BROWSER SIMPLE AUTOMATION")
    print("Multi-URL Support | PyAutoGUI Method")
    print("="*60)
    print()
    
    # Validate configuration
    if not TARGET_URLS:
        print("ERROR: No URLs configured!")
        print("Please add TARGET_URLS to your .env file")
        return
    
    print(f"Found {len(TARGET_URLS)} URL(s) to process")
    print()
    print("⚠ IMPORTANT: Do NOT move your mouse during automation!")
    print("⚠ Move mouse to top-left corner to abort (FAILSAFE)")
    print()
    
    try:
        # Launch Tor Browser
        open_tor_browser()
        
        # Process each URL
        successful = 0
        failed = 0
        
        for i, url in enumerate(TARGET_URLS, 1):
            if process_url(url, i, len(TARGET_URLS), is_first=(i == 1)):
                successful += 1
            else:
                failed += 1
            
            # Wait between URLs
            if i < len(TARGET_URLS):
                print(f"\nWaiting {URL_SWITCH_WAIT}s before next URL...")
                time.sleep(URL_SWITCH_WAIT)
        
        # Summary
        print(f"\n{'='*60}")
        print("AUTOMATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total URLs: {len(TARGET_URLS)}")
        print(f"✓ Successful: {successful}")
        print(f"✗ Failed: {failed}")
        print()
        print("Files should be in your download folder")
        print("You can close Tor Browser manually when ready")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
