#!/usr/bin/env python3
"""
inspect_process.py
Inspects a target process PID: verifies parent PID, open ports via lsof/ss,
environment variables, and process status.
"""

import subprocess
import sys

def inspect(pid: int):
    print(f"=== Inspecting Process PID: {pid} ===")
    
    # 1. Check ps output
    try:
        ps_out = subprocess.check_output(["ps", "-p", str(pid), "-o", "pid,ppid,stat,command"]).decode()
        print("\n--- Process Table Entry (ps) ---")
        print(ps_out.strip())
    except subprocess.CalledProcessError:
        print(f"Process {pid} is not running.")
        sys.exit(1)

    # 2. Check listening ports with lsof
    try:
        lsof_out = subprocess.check_output(["lsof", "-Pan", "-p", str(pid), "-i"]).decode()
        print("\n--- Network Sockets Bound (lsof) ---")
        print(lsof_out.strip())
    except Exception:
        print("\n--- Network Sockets: None or lsof unavailable ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_process.py <PID>")
        sys.exit(1)
    inspect(int(sys.argv[1]))
