#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 06: 06-poisoned-dependency-cache
Demonstrates: Poisoned Dependency Cache Restoring Corrupted Binaries
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 06-poisoned-dependency-cache")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Build fails with `corrupt zipfile` or `ModuleNotFoundError` across all branches until cache is manually purged.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
