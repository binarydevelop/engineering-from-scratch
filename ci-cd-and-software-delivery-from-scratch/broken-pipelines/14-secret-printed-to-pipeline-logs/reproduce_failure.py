#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 14: 14-secret-printed-to-pipeline-logs
Demonstrates: Verbose Bash Debugging Prints Cloud Token to Public Log
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 14-secret-printed-to-pipeline-logs")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A `set -x` in build script prints full AWS access token or database password to standard error in CI logs.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
