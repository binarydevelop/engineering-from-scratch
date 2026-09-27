#!/usr/bin/env python3
import subprocess
import sys

def inspect_segments():
    print("Inspecting Kafka partition directories inside container...")
    cmd = ["docker", "exec", "kafka-lab-single", "ls", "-la", "/tmp/kraft-combined-logs/"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(res.stdout)
    else:
        print(f"Error inspecting container: {res.stderr}")

if __name__ == "__main__":
    inspect_segments()
