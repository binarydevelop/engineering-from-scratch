#!/usr/bin/env python3
"""
Verification Harness for Project: Protected Production Delivery with Approvals & Rollback (Phase 210)
"""
import os
import subprocess
import sys

print("Verifying Project: Protected Production Delivery with Approvals & Rollback...")
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

cmd = """bash scripts/rollback.sh staging prev-known-good"""
p = subprocess.run(cmd, shell=True, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0:
    print("✓ Project verification PASSED!")
    print(p.stdout.strip())
    sys.exit(0)
else:
    print("✗ Project verification FAILED!", file=sys.stderr)
    print(p.stderr.strip(), file=sys.stderr)
    sys.exit(1)
