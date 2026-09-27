#!/usr/bin/env python3
"""
worker.py - Background Task Consumer

A resilient background worker that:
1. Connects to the task queue service
2. Dequeues and processes tasks
3. Responds cleanly to SIGTERM signals for graceful termination
"""

import os
import sys
import time
import signal

keep_running = True

def handle_sigterm(signum, frame):
    global keep_running
    print(f"\n[WORKER {os.getpid()}] Caught SIGTERM! Finishing current task before exiting...")
    keep_running = False

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

def main():
    worker_id = os.environ.get("HOSTNAME", f"local-{os.getpid()}")
    queue_host = os.environ.get("QUEUE_HOST", "queue-svc")
    print(f"==========================================================")
    print(f"  Worker {worker_id} starting up...                     ")
    print(f"  Connecting to queue at {queue_host}...                ")
    print(f"==========================================================")

    task_count = 0
    while keep_running:
        task_count += 1
        print(f"[WORKER {worker_id}] Dequeued task #{task_count}. Processing...")
        # Simulate processing work
        time.sleep(2)
        print(f"[WORKER {worker_id}] Task #{task_count} completed successfully.")

    print(f"[WORKER {worker_id}] Graceful shutdown finished. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
