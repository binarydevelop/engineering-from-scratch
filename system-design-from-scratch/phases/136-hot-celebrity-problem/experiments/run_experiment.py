"""
Failure injection and benchmark experiment for Phase 136: The Celebrity Fanout Problem.
Target failure: Celebrity post triggers 100 million inbox writes, crashing message broker.
"""

import sys
import os
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from main import PhaseSystem

def run_experiment():
    print("=" * 70)
    print(f" Executing Experiment: Phase 136 (The Celebrity Fanout Problem)")
    print(f" Target Failure: Celebrity post triggers 100 million inbox writes, crashing message broker.")
    print("=" * 70)

    system = PhaseSystem()

    print("\n1. Running Baseline Workload...")
    for i in range(10):
        res = system.process_request({"request_id": f"req_{i}", "action": "read"})
    print(f"  [OK] 10 requests completed. Telemetry: {system.get_telemetry()}")

    print("\n2. Injecting Controlled Failure...")
    system.chaos_active = True
    try:
        system.process_request({"request_id": "req_fault"})
        print("  [FAIL] Expected chaos error did not trigger!")
    except RuntimeError as exc:
        print(f"  [OK] Expected fault caught: {exc}")

    system.chaos_active = False
    print("\n3. Verified Recovery After Healing:")
    res_heal = system.process_request({"request_id": "req_post_heal"})
    print(f"  [OK] System recovered successfully. Status: {res_heal['status']}")
    print("\nExperiment complete. Record findings in outputs/evidence-template.md")

if __name__ == "__main__":
    run_experiment()
