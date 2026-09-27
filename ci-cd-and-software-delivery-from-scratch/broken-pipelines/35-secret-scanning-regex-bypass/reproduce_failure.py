#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 35: 35-secret-scanning-regex-bypass
Demonstrates: Secret Scanner Bypassed by Base64 Encoded Token
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 35-secret-scanning-regex-bypass")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A committed secret is ignored by regex scanner because the token was base64 encoded.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
