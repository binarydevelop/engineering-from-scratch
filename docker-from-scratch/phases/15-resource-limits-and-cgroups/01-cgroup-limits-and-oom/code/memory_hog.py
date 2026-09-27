#!/usr/bin/env python3
"""
memory_hog.py
Intentionally allocates heap memory until restricted by cgroup limits.
Demonstrates the Linux Out-Of-Memory (OOM) Killer.
"""

import sys
import time

def allocate_memory():
    print("=== Memory Hog Process Starting ===")
    print("Allocating memory in chunks of 10 MB...\n")
    chunks = []
    total_mb = 0
    try:
        while True:
            # Allocate 10 MB chunk of bytes
            chunk = b"X" * (10 * 1024 * 1024)
            chunks.append(chunk)
            total_mb += 10
            print(f"Allocated: {total_mb} MB in RAM")
            sys.stdout.flush()
            time.sleep(0.2)
    except MemoryError:
        print("Python caught MemoryError!")

if __name__ == "__main__":
    allocate_memory()
