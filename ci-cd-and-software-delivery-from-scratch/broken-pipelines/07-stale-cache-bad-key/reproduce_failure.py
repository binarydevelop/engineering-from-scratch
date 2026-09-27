#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 07: 07-stale-cache-bad-key
Demonstrates: Cache Key Ignores Lockfile Hash, Serving Stale Packages
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 07-stale-cache-bad-key")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Dependency version bumped in lockfile, but CI runner continues executing with old library version, ignoring the update.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
