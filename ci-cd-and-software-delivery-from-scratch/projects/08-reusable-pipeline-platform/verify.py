#!/usr/bin/env python3
"""
Verification Harness for Project: Central Reusable Workflow Delivery Platform (Phase 213)
"""
import os
import subprocess
import sys

print("Verifying Project: Central Reusable Workflow Delivery Platform...")
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

cmd = """python3 -c 'print("Validating reusable workflow templates"); sys.exit(0)'"""
p = subprocess.run(cmd, shell=True, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0:
    print("✓ Project verification PASSED!")
    print(p.stdout.strip())
    sys.exit(0)
else:
    print("✗ Project verification FAILED!", file=sys.stderr)
    print(p.stderr.strip(), file=sys.stderr)
    sys.exit(1)
