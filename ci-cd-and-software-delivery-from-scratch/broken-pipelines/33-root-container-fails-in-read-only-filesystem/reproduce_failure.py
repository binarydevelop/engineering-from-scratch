#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 33: 33-root-container-fails-in-read-only-filesystem
Demonstrates: Container Assumes Root Access and Writable Root Filesystem
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 33-root-container-fails-in-read-only-filesystem")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Container runs fine locally, but crashes on Kubernetes with `Permission denied: cannot write to /app`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
