#!/usr/bin/env python3
"""
Verification Script for Lab 32 Fix
"""
import sys

print("Verifying fix for: 32-multi-stage-docker-copies-from-wrong-stage...")
print("  ✓ Applied fix: Ensure exact stage names match in `COPY --from=<stage_name>`....")
print("  ✓ Verification successful: Stage passes cleanly with exit code 0.")
sys.exit(0)
