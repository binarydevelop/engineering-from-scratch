#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 17: 17-unpinned-third-party-action-supply-chain-tamper
Demonstrates: Third-Party Action Tag Hijacked by Malicious Release
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 17-unpinned-third-party-action-supply-chain-tamper")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Workflow using `uses: third-party/action@v1` executes malicious code after upstream repository account was compromised.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
