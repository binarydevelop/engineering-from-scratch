#!/usr/bin/env python3
"""
test_cow_isolation.py
Proves Copy-on-Write (CoW) filesystem isolation between two containers
started from the exact same base image, and demonstrates the ephemeral lifecycle
of the container's writable layer.
"""

import subprocess
import sys
import time

def run_cmd(cmd: list) -> str:
    return subprocess.check_output(cmd).decode().strip()

def main():
    print("=== Copy-on-Write (CoW) Filesystem Isolation Test ===\n")
    
    # 1. Clean prior test containers if any
    for name in ["dfs-cow-1", "dfs-cow-2", "dfs-cow-3"]:
        subprocess.run(["docker", "rm", "-f", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Start container 1 and create a unique file
    print("1. Launching container dfs-cow-1 and writing /tmp/unique_to_c1.txt")
    run_cmd(["docker", "run", "-d", "--name", "dfs-cow-1", "alpine:latest", "sleep", "60"])
    run_cmd(["docker", "exec", "dfs-cow-1", "sh", "-c", "echo 'Hello from Container 1' > /tmp/unique_to_c1.txt"])
    
    # 3. Start container 2 from the SAME image and check if it sees c1's file
    print("2. Launching container dfs-cow-2 from the same image")
    run_cmd(["docker", "run", "-d", "--name", "dfs-cow-2", "alpine:latest", "sleep", "60"])
    
    print("\n3. Testing file visibility in container dfs-cow-2:")
    check_c2 = subprocess.run(
        ["docker", "exec", "dfs-cow-2", "cat", "/tmp/unique_to_c1.txt"],
        capture_output=True, text=True
    )
    if check_c2.returncode != 0:
        print(" [ISOLATION VERIFIED] Container 2 CANNOT see /tmp/unique_to_c1.txt!")
        print(f"   Stderr: {check_c2.stderr.strip()}")
    else:
        print(" [FAILURE] Isolation broken! Container 2 saw Container 1's file.")
        sys.exit(1)

    # 4. Inspect changes to the writable layer using docker diff
    print("\n4. Inspecting filesystem mutations (docker diff):")
    diff_c1 = run_cmd(["docker", "diff", "dfs-cow-1"])
    print(f"--- docker diff dfs-cow-1 ---")
    print(diff_c1)
    
    diff_c2 = run_cmd(["docker", "diff", "dfs-cow-2"])
    print(f"--- docker diff dfs-cow-2 ---")
    print(diff_c2 if diff_c2 else "(No changes to writable layer)")

    # 5. Delete container 1, launch container 3, verify data is permanently gone
    print("\n5. Removing dfs-cow-1 and launching fresh dfs-cow-3:")
    run_cmd(["docker", "rm", "-f", "dfs-cow-1"])
    run_cmd(["docker", "run", "-d", "--name", "dfs-cow-3", "alpine:latest", "sleep", "60"])
    check_c3 = subprocess.run(
        ["docker", "exec", "dfs-cow-3", "cat", "/tmp/unique_to_c1.txt"],
        capture_output=True, text=True
    )
    if check_c3.returncode != 0:
        print(" [EPHEMERALITY VERIFIED] dfs-cow-3 has no trace of dfs-cow-1's file.")
        print("   The writable layer was erased when dfs-cow-1 was removed.")

    # Cleanup
    for name in ["dfs-cow-2", "dfs-cow-3"]:
        subprocess.run(["docker", "rm", "-f", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\nTest completed successfully.")

if __name__ == "__main__":
    main()
