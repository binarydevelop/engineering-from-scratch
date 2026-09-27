#!/usr/bin/env python3
"""
Verification Harness for Project: Progressive Canary Deployment with Automated Abort (Phase 216)
"""
import os
import subprocess
import sys

print("Verifying Project: Progressive Canary Deployment with Automated Abort...")
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

cmd = """python3 deployment-labs/deploy_simulator.py --strategy canary --steps 1,10,50,100"""
p = subprocess.run(cmd, shell=True, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0:
    print("✓ Project verification PASSED!")
    print(p.stdout.strip())
    sys.exit(0)
else:
    print("✗ Project verification FAILED!", file=sys.stderr)
    print(p.stderr.strip(), file=sys.stderr)
    sys.exit(1)
