#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 27: 27-canary-promoted-despite-elevated-5xx-errors
Demonstrates: Canary Rollout Metric Threshold Too Lenient, Promoting Buggy Code
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 27-canary-promoted-despite-elevated-5xx-errors")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A new release with a 5% error rate is promoted to 100% traffic because the canary check only monitored HTTP 200 count.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
