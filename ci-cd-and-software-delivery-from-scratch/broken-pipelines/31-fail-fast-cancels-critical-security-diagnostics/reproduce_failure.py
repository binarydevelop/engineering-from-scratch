#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 31: 31-fail-fast-cancels-critical-security-diagnostics
Demonstrates: Fail-Fast Option Suppresses Security and Coverage Reports
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 31-fail-fast-cancels-critical-security-diagnostics")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Linting fails, causing CI to instantly abort test and security jobs, leaving developers blind to test results.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
