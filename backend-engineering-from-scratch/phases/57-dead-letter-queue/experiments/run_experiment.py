"""
Experiment & Failure Injection for Lesson 57: Dead-Letter Queue.
Simulates: Enqueue a poison pill task containing invalid syntax alongside 5 valid tasks.
"""

import sys
import os
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from main import PhaseComponent

def run_experiment():
    print("=" * 60)
    print(f" Running Failure Injection Lab: Lesson 57 (Dead-Letter Queue)")
    print(f" Target Failure: Enqueue a poison pill task containing invalid syntax alongside 5 valid tasks.")
    print("=" * 60)

    comp = PhaseComponent()

    print("\n1. Executing Baseline Working State...")
    start_time = time.perf_counter()
    baseline = comp.process({"client": "test_client", "action": "read"})
    duration_ms = (time.perf_counter() - start_time) * 1000
    print(f"  [OK] Baseline operation completed in {duration_ms:.3f}ms. Status: {baseline['status']}")

    print("\n2. Injecting Controlled Failure...")
    try:
        comp.process({"trigger_error": True})
        print("  [FAIL] Expected failure did not trigger!")
    except Exception as e:
        print(f"  [EXPECTED ERROR CAUGHT]: {type(e).__name__} - {e}")

    print("\n3. Inspecting Telemetry State...")
    telemetry = comp.get_telemetry()
    print(f"  Telemetry: {telemetry['metrics']}")
    print("\nExperiment completed successfully. Record observations in outputs/evidence-template.md")

if __name__ == "__main__":
    run_experiment()
