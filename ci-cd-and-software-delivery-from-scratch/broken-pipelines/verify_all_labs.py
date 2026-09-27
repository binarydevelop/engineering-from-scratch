#!/usr/bin/env python3
"""
Automated Verifier for All 42 Broken CI/CD Labs
Ensures:
1. Every broken lab properly reproduces the failure (exit code != 0)
2. Every solution properly verifies the resolution (exit code == 0)
3. Documentation and structure conform to curriculum standards
"""

import os
import subprocess
import sys


def verify_all_labs():
    base_dir = os.path.dirname(__file__)
    labs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d[0].isdigit()])

    print("========================================================================")
    print(f" VERIFYING ALL {len(labs)} BROKEN CI/CD LABS")
    print("========================================================================")

    passed_count = 0
    failed_count = 0

    for lab in labs:
        lab_dir = os.path.join(base_dir, lab)
        repro_script = os.path.join(lab_dir, "reproduce_failure.py")
        solution_script = os.path.join(lab_dir, "solution", "verify_fix.py")
        readme = os.path.join(lab_dir, "README.md")
        sol_md = os.path.join(lab_dir, "solution", "SOLUTION.md")

        # Check documentation presence
        if not os.path.exists(readme) or not os.path.exists(sol_md):
            print(f"✗ [FAIL] {lab}: Missing documentation files!", file=sys.stderr)
            failed_count += 1
            continue

        # 1. Test failure reproduction (must exit non-zero)
        p_repro = subprocess.run([sys.executable, repro_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p_repro.returncode == 0:
            print(f"✗ [FAIL] {lab}: reproduce_failure.py did NOT fail (exit 0)!", file=sys.stderr)
            failed_count += 1
            continue

        # 2. Test fix verification (must exit zero)
        p_sol = subprocess.run([sys.executable, solution_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p_sol.returncode != 0:
            print(f"✗ [FAIL] {lab}: verify_fix.py failed with exit code {p_sol.returncode}!", file=sys.stderr)
            failed_count += 1
            continue

        passed_count += 1
        print(f"  ✓ [{lab}] Repro fails (exit {p_repro.returncode}) & Fix passes (exit 0)")

    print("========================================================================")
    print(f"RESULTS: {passed_count}/{len(labs)} labs verified successfully. ({failed_count} failures)")
    print("========================================================================")

    return failed_count == 0


if __name__ == "__main__":
    success = verify_all_labs()
    sys.exit(0 if success else 1)
