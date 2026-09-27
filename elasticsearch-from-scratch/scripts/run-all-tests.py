#!/usr/bin/env python3
"""
scripts/run-all-tests.py - Comprehensive test runner across all phases and capstones.
"""

import glob
import os
import subprocess
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_command(cmd, cwd=BASE_DIR):
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        elapsed = (time.perf_counter() - t0) * 1000
        return proc.returncode == 0, elapsed, proc.stdout, proc.stderr
    except Exception as e:
        elapsed = (time.perf_counter() - t0) * 1000
        return False, elapsed, "", str(e)

def main():
    print("=" * 80)
    print("  elasticsearch-from-scratch Automated Test Suite")
    print("=" * 80)

    test_targets = [
        ("Capstone 3: Mini Search Engine Unit Tests", "python3 projects/mini_search_engine/test_engine.py"),
        ("Phase 81: Distributed Cluster Simulator Unit Tests", "python3 projects/distributed_simulator/test_cluster.py")
    ]

    # Automatically discover all phase python scripts
    phase_dirs = sorted([d for d in os.listdir(os.path.join(BASE_DIR, "phases")) if os.path.isdir(os.path.join(BASE_DIR, "phases", d))])
    for pd in phase_dirs:
        code_dir = os.path.join(BASE_DIR, "phases", pd, "code")
        if os.path.isdir(code_dir):
            py_files = [f for f in os.listdir(code_dir) if f.endswith(".py")]
            for pf in py_files:
                rel_path = os.path.relpath(os.path.join(code_dir, pf), BASE_DIR)
                label = f"Phase {pd[:2]}: {pf}"
                test_targets.append((label, f"python3 {rel_path}"))

    passed = 0
    failed = 0

    print(f"\n{'Test Case / Module':58s} | {'Status':8s} | {'Time':8s}")
    print("-" * 80)

    for desc, cmd in test_targets:
        success, elapsed, out, err = run_command(cmd)
        if success:
            passed += 1
            print(f"{desc:58s} | \033[0;32mPASSED\033[0m   | {elapsed:6.1f} ms")
        else:
            failed += 1
            print(f"{desc:58s} | \033[0;31mFAILED\033[0m   | {elapsed:6.1f} ms")
            if err:
                print(f"   Error: {err.strip()[:100]}")

    print("-" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_targets)} total test cases.")
    print("=" * 80)

    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
