#!/usr/bin/env python3
"""
mini_controller.py - The Conceptual Seed of Kubernetes

A pure Python reconciliation loop demonstrating declarative desired state vs.
observed actual state.

The system does NOT issue imperative commands like "start 3 processes".
Instead, it declares:
    DESIRED: 3 running worker processes

The controller continuously loops:
    1. OBSERVE: Count currently alive worker processes
    2. COMPARE: delta = desired - actual
    3. ACT: Start replacements or terminate excess
    4. REPEAT: Sleep briefly and repeat indefinitely
"""

import sys
import os
import time
import signal
import subprocess
from typing import List, Dict

class MiniReconciler:
    def __init__(self, desired_replicas: int = 3):
        self.desired_replicas = desired_replicas
        self.workers: Dict[int, subprocess.Popen] = {}
        self.iteration = 0

    def observe(self) -> List[int]:
        """Inspects all tracked worker processes to verify who is actually alive."""
        alive_pids = []
        for pid, proc in list(self.workers.items()):
            poll_result = proc.poll()
            if poll_result is None:
                # Process is still executing in the OS
                alive_pids.append(pid)
            else:
                # Process exited or was killed
                print(f"  [OBSERVE] Worker PID {pid} has died (exit code {poll_result}).")
                del self.workers[pid]
        return alive_pids

    def act(self, alive_pids: List[int]):
        """Reconciles the difference between desired and observed state."""
        actual_count = len(alive_pids)
        delta = self.desired_replicas - actual_count

        if delta > 0:
            print(f"  [RECONCILE] Deficit detected! Desired: {self.desired_replicas}, Actual: {actual_count}. Spawning {delta} worker(s)...")
            for _ in range(delta):
                # Spawn a simple dummy worker that sleeps
                proc = subprocess.Popen(
                    [sys.executable, "-c", "import time, os; print(f'Worker {os.getpid()} started'); time.sleep(300)"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.workers[proc.pid] = proc
                print(f"  [ACTION] Started replacement process PID {proc.pid}.")
        elif delta < 0:
            excess = abs(delta)
            print(f"  [RECONCILE] Excess detected! Desired: {self.desired_replicas}, Actual: {actual_count}. Terminating {excess} worker(s)...")
            pids_to_kill = list(self.workers.keys())[:excess]
            for pid in pids_to_kill:
                proc = self.workers[pid]
                proc.terminate()
                proc.wait()
                del self.workers[pid]
                print(f"  [ACTION] Terminated excess process PID {pid}.")
        else:
            print(f"  [STEADY] Desired ({self.desired_replicas}) == Actual ({actual_count}). Zero delta. No action needed.")

    def reconcile_once(self):
        self.iteration += 1
        print(f"\n--- [Iteration {self.iteration}] ---")
        alive = self.observe()
        self.act(alive)

    def cleanup(self):
        print("\n[CLEANUP] Shutting down all worker processes...")
        for pid, proc in list(self.workers.items()):
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except Exception:
                proc.kill()
        print("[CLEANUP] All workers stopped cleanly.")

def run_test():
    """Headless automated test validating the reconciliation cycle."""
    print("Running MiniReconciler automated test...")
    reconciler = MiniReconciler(desired_replicas=3)
    try:
        # Step 1: Initial state (0 workers) -> Should create 3
        reconciler.reconcile_once()
        assert len(reconciler.workers) == 3, f"Expected 3 workers, got {len(reconciler.workers)}"

        # Step 2: Steady state -> Should do nothing
        reconciler.reconcile_once()
        assert len(reconciler.workers) == 3

        # Step 3: Fault Injection -> Intentionally kill 1 process
        killed_pid = list(reconciler.workers.keys())[0]
        print(f"\n[FAULT INJECTION] Intentionally killing worker PID {killed_pid} with SIGKILL...")
        os.kill(killed_pid, signal.SIGKILL)
        time.sleep(0.5)

        # Step 4: Next reconciliation iteration -> Controller must notice and replace
        reconciler.reconcile_once()
        assert len(reconciler.workers) == 3, f"Expected 3 workers after replacement, got {len(reconciler.workers)}"
        assert killed_pid not in reconciler.workers, "Killed PID should no longer be tracked"
        print("\n[SUCCESS] Controller detected the killed worker and automatically reconciled state to 3 replicas!")
    finally:
        reconciler.cleanup()

def main():
    if "--test" in sys.argv:
        run_test()
        sys.exit(0)

    reconciler = MiniReconciler(desired_replicas=3)
    print("==========================================================")
    print("  mini_controller.py: Declarative Desired State Engine    ")
    print("  Desired Replicas: 3                                    ")
    print("  Press Ctrl+C to stop. Try killing a worker PID!         ")
    print("==========================================================")

    try:
        while True:
            reconciler.reconcile_once()
            time.sleep(2)
    except KeyboardInterrupt:
        reconciler.cleanup()

if __name__ == "__main__":
    main()
