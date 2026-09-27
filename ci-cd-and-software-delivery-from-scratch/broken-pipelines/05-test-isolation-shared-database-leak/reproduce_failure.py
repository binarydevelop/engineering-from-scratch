#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 05: 05-test-isolation-shared-database-leak
Demonstrates: Parallel Test Shards Bleeding State into Shared Database
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 05-test-isolation-shared-database-leak")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Tests pass when run individually (`test_user_signup`), but fail when run in parallel with `DuplicateKeyError: user 'test@example.com' already exists`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
