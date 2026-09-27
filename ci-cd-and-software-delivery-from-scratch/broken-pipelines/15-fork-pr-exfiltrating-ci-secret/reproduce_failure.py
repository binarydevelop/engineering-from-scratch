#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 15: 15-fork-pr-exfiltrating-ci-secret
Demonstrates: Malicious Fork PR Leverages pull_request_target to Read Secrets
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 15-fork-pr-exfiltrating-ci-secret")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: External contributor submits PR modifying test code to send `env` output to webhook; secrets compromised.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
