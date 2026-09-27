#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 28: 28-feature-flag-deadlock-stale-flag-debt
Demonstrates: Stale Feature Flag Code Path Causes Production Deadlock
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 28-feature-flag-deadlock-stale-flag-debt")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A feature flag toggle deployed 8 months ago is toggled off by an operator, exposing an unmaintained bitrotted code path.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
