#!/usr/bin/env python3
"""
logger_app.py
Emits structured output to stdout and diagnostic warnings to stderr.
"""

import sys
import time

def main():
    for i in range(1, 4):
        sys.stdout.write(f"[INFO stdout] Processing batch job #{i} at {time.time()}\n")
        sys.stdout.flush()
        
        sys.stderr.write(f"[WARN stderr] High latency warning on worker thread #{i}\n")
        sys.stderr.flush()
        time.sleep(0.2)

if __name__ == "__main__":
    main()
