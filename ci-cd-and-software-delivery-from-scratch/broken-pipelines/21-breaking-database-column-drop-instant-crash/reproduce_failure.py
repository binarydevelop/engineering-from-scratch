#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 21: 21-breaking-database-column-drop-instant-crash
Demonstrates: Instant Column Drop Crashes Running Application Replicas
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 21-breaking-database-column-drop-instant-crash")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Database migration drops `legacy_user_id`; running v1 pods instantly fail on all user queries with `no such column`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
