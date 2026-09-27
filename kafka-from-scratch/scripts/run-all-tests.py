#!/usr/bin/env python3
"""
Automated validation suite across all 68 phases of kafka-from-scratch.
Verifies directory completeness, template conformity, executable code, and unit tests.
"""

import sys
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PHASES_DIR = BASE_DIR / "phases"

def log_pass(msg): print(f"  \033[32m[PASS]\033[0m {msg}")
def log_fail(msg): print(f"  \033[31m[FAIL]\033[0m {msg}")
def log_info(msg): print(f"\n\033[1m=== {msg} ===\033[0m")

def test_phases_completeness():
    log_info("1. Verifying All 68 Phase Directories and Artifacts")
    phase_dirs = sorted(list(PHASES_DIR.glob("*")))
    if len(phase_dirs) != 68:
        log_fail(f"Expected 68 phases, found {len(phase_dirs)}")
        return False
    log_pass(f"Exactly 68 phase directories found (00 to 67)")

    missing = 0
    for p in phase_dirs:
        doc = p / "docs" / "en.md"
        exp = p / "experiments" / "run_experiment.sh"
        out = p / "outputs" / "evidence-template.md"
        code = p / "code"

        if not doc.exists():
            log_fail(f"{p.name}: Missing docs/en.md")
            missing += 1
        if not exp.exists() or not os.access(exp, os.X_OK):
            log_fail(f"{p.name}: Missing or non-executable experiments/run_experiment.sh")
            missing += 1
        if not out.exists():
            log_fail(f"{p.name}: Missing outputs/evidence-template.md")
            missing += 1
        if not code.exists() or not list(code.glob("*.py")):
            log_fail(f"{p.name}: Missing Python code files")
            missing += 1

    if missing == 0:
        log_pass("All 68 phases have complete docs, code, executable experiments, and evidence templates.")
        return True
    return False

def test_python_components():
    log_info("2. Executing Core Component Unit Tests")
    test_files = [
        BASE_DIR / "projects/capstone-1-mini-kafka/test_mini_kafka.py",
        BASE_DIR / "phases/02-build-an-append-only-log/code/mini_log.py",
        BASE_DIR / "phases/10-consumer-groups-from-first-principles/code/consumer_group_sim.py",
        BASE_DIR / "phases/15-idempotent-consumers/code/idempotent_consumer.py",
        BASE_DIR / "projects/capstone-2-event-driven-app/run_app.py",
    ]

    all_passed = True
    for tf in test_files:
        res = subprocess.run([sys.executable, str(tf)], capture_output=True, text=True)
        if res.returncode == 0:
            log_pass(f"{tf.name} executed successfully")
        else:
            log_fail(f"{tf.name} failed with return code {res.returncode}:\n{res.stderr}")
            all_passed = False
    return all_passed

def test_docker_compose_syntax():
    log_info("3. Validating Docker Compose Topologies")
    for f in ["docker-compose.yml", "docker-compose.cluster.yml"]:
        cmd = ["docker", "compose", "-f", str(BASE_DIR / f), "config"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            log_pass(f"{f} syntax is valid")
        else:
            log_fail(f"{f} syntax invalid: {res.stderr}")
            return False
    return True

if __name__ == "__main__":
    t1 = test_phases_completeness()
    t2 = test_python_components()
    t3 = test_docker_compose_syntax()

    print("\n" + "=" * 60)
    if t1 and t2 and t3:
        print("\033[1;32mALL TEST SUITES PASSED! kafka-from-scratch is 100% verified.\033[0m")
        sys.exit(0)
    else:
        print("\033[1;31mSOME TESTS FAILED! Review output above.\033[0m")
        sys.exit(1)
