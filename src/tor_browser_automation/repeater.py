"""
Repeater script for Tor Browser Automation.
Runs the automation logic every 5 minutes for 1 hour.
"""

import time
import sys
import os

# Check if we are running in Docker
IS_DOCKER = os.path.exists('/.dockerenv')

if IS_DOCKER:
    from tor_browser_automation.docker_main import main as run_automation
else:
    from tor_browser_automation.main import main as run_automation

def run_repeater():
    # Load configuration from environment
    total_cycles = int(os.getenv("REPEATER_CYCLES", "20"))
    wait_seconds = int(os.getenv("REPEATER_WAIT_TIME", "120"))

    print("="*60)
    print("TOR BROWSER AUTOMATION REPEATER (Python Version)")
    print("="*60)
    print(f"Scheduled: {total_cycles} cycles, every {wait_seconds/60:.1f} minutes.")
    print("Starting automatically in 5 seconds...")
    print("="*60)
    
    # Initial 5 second wait as requested
    time.sleep(5)

    for i in range(1, total_cycles + 1):
        timestamp = time.strftime("%H:%M:%S")
        print(f"\n[{timestamp}] Starting Cycle {i} of {total_cycles}...")
        print("-" * 60)
        
        try:
            # Execute the main automation logic
            run_automation()
        except KeyboardInterrupt:
            print("\n\n!! Repeater stopped by user (Ctrl+C) !!")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Error in Cycle {i}: {e}")
            print("The repeater will try to continue with the next cycle.")

        if i < total_cycles:
            next_run = time.strftime("%H:%M:%S", time.localtime(time.time() + wait_seconds))
            print(f"\n[{time.strftime('%H:%M:%S')}] Cycle {i} complete.")
            print(f"Waiting 5 minutes for next run...")
            print(f"Next run scheduled for approximately: {next_run}")
            
            try:
                # Wait for 5 minutes
                time.sleep(wait_seconds)
            except KeyboardInterrupt:
                print("\n\n!! Repeater stopped by user (Ctrl+C) !!")
                sys.exit(0)

    print("\n" + "="*60)
    print("REPEATER TASK FINISHED")
    print("="*60)

if __name__ == "__main__":
    run_repeater()
