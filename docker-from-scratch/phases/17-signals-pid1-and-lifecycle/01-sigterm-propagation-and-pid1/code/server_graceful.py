#!/usr/bin/env python3
"""
server_graceful.py
Registers a SIGTERM signal handler to demonstrate graceful container shutdown.
"""

import signal
import sys
import time

def handle_sigterm(signum, frame):
    sys.stdout.write(f"\n[server_graceful PID {sys.argv[0]}] Caught SIGTERM! Draining connections...\n")
    sys.stdout.flush()
    time.sleep(0.5)
    sys.stdout.write("[server_graceful] Graceful drain complete. Exiting cleanly with code 0.\n")
    sys.stdout.flush()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

if __name__ == "__main__":
    print(f"[server_graceful] Application started. Listening for signals...")
    sys.stdout.flush()
    while True:
        time.sleep(1)
