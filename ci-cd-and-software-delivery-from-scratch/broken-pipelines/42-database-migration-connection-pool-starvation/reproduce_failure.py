#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 42: 42-database-migration-connection-pool-starvation
Demonstrates: Long-Running Migration Locks Table, Exhausting Connection Pool
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 42-database-migration-connection-pool-starvation")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Running an unindexed table scan update causes incoming HTTP requests to queue, crashing the application with pool timeouts.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
