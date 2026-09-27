#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 03: 03-missing-lockfile-drift
Demonstrates: Developer Machine Uses Different Transitive Dependency than CI
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 03-missing-lockfile-drift")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Code passes locally on developer laptop but crashes in CI runner due to subtle behavior difference in transitive helper library.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
