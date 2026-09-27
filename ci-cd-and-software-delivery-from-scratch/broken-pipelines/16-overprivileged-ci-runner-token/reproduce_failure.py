#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 16: 16-overprivileged-ci-runner-token
Demonstrates: CI Token Holds Full Cloud Administrator Privileges
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 16-overprivileged-ci-runner-token")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A compromised npm dependency in CI attempts to provision cloud resources or delete S3 buckets.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
