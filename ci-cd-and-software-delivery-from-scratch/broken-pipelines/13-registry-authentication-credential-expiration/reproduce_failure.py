#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 13: 13-registry-authentication-credential-expiration
Demonstrates: Docker Push Fails at End of 45-Minute Build Job
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 13-registry-authentication-credential-expiration")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Build job compiles and runs tests for 45 minutes, then fails at final step with `unauthorized: authentication required`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
