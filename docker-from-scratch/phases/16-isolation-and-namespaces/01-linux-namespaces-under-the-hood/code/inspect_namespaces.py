#!/usr/bin/env python3
"""
inspect_namespaces.py
Inspects namespace dual-identity: compares the PID of a process
inside its container namespace with its real PID on the host/VM.
"""

import subprocess
import sys

def main(container_name: str):
    print(f"=== Process Dual Identity in Linux Namespaces: {container_name} ===")
    
    # Inside the container PID namespace:
    try:
        container_ps = subprocess.check_output(
            ["docker", "exec", container_name, "ps", "-o", "pid,comm"]
        ).decode().strip()
        print("\n1. Inside Container PID Namespace (What the container sees):")
        print(container_ps)
    except Exception as e:
        print(f"Error checking container ps: {e}")

    # On the Host / VM engine side:
    try:
        docker_top = subprocess.check_output(
            ["docker", "top", container_name, "-o", "pid,ppid,comm"]
        ).decode().strip()
        print("\n2. Engine / Host Process Table (docker top - What the kernel sees):")
        print(docker_top)
    except Exception as e:
        print(f"Error checking docker top: {e}")

if __name__ == "__main__":
    c_name = sys.argv[1] if len(sys.argv) > 1 else "dfs-ns-demo"
    main(c_name)
