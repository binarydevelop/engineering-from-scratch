#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 10: 10-mutable-latest-image-tag-overwrite
Demonstrates: Production Pulls Unexpected Code Due to Overwritten 'latest' Tag
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 10-mutable-latest-image-tag-overwrite")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Staging was tested on version 1.2.0, but when production pods restarted, they pulled newly pushed version 1.3.0 because both were tagged `:latest`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
