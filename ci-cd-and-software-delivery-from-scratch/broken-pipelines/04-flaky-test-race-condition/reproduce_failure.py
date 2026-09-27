#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 04: 04-flaky-test-race-condition
Demonstrates: Flaky Asynchronous Race Condition in Integration Suite
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 04-flaky-test-race-condition")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Test passes 4 out of 5 runs, but intermittently fails with `AssertionError: Expected status 'completed', got 'processing'`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
