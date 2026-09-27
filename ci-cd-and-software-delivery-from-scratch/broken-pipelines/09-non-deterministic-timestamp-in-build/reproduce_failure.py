#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 09: 09-non-deterministic-timestamp-in-build
Demonstrates: Embedded Wall-Clock Timestamp Prevents Build Reproducibility
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 09-non-deterministic-timestamp-in-build")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Rebuilding the exact same commit SHA produces a different SHA-256 binary hash, breaking artifact verification and caching.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
