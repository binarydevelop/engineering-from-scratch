import os
import signal
import sys
import time
import subprocess

def handle_sigterm(signum, frame):
    print("[*] Caught SIGTERM in Python worker! Exiting cleanly immediately...", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

print(f"[*] Worker started with PID {os.getpid()}, PPID {os.getppid()}", flush=True)

# Spawn a child process that exits immediately and is orphaned
for i in range(3):
    pid = os.fork()
    if pid == 0:
        # Child process exits immediately
        sys.exit(0)
    # Parent does NOT waitpid(), leaving child as zombie until reaped by PID 1

print("[*] Spawned 3 zombie child processes. Running worker loop...", flush=True)

while True:
    time.sleep(1)
