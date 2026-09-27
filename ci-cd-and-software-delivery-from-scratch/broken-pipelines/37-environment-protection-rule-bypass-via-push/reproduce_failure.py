#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 37: 37-environment-protection-rule-bypass-via-push
Demonstrates: Direct Branch Push Bypasses Required Review and Staging Gate
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 37-environment-protection-rule-bypass-via-push")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: An unverified commit is pushed directly to main and immediately deployed to production without review.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
