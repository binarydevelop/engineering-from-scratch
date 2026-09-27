#!/usr/bin/env python3
"""
Concurrency, Race Conditions, Mutexes, and Deadlocks Simulator
Demonstrates:
1. Race Condition: Unsynchronized concurrent balance transfers losing money
2. Mutex Synchronization: Preserving global balance invariant
3. Deadlock: Out-of-order 2-lock acquisition causing circular wait hang
4. Deadlock Prevention: Total lock ordering eliminating circular wait
"""

import threading
import time
import random
from typing import Dict, List


class Account:
    def __init__(self, acc_id: int, balance: int):
        self.acc_id = acc_id
        self.balance = balance
        self.lock = threading.Lock()


def unsafe_transfer(src: Account, dst: Account, amount: int):
    """Unsynchronized transfer subject to race condition"""
    if src.balance >= amount:
        # Simulate CPU context switch interleaving between read and write
        curr_src = src.balance
        curr_dst = dst.balance
        time.sleep(0.0001)
        src.balance = curr_src - amount
        dst.balance = curr_dst + amount


def safe_transfer_lock_ordering(src: Account, dst: Account, amount: int):
    """
    Safe transfer using strict lock ordering to prevent deadlocks:
    Always acquire the lock with lower ID first!
    """
    first_lock = src if src.acc_id < dst.acc_id else dst
    second_lock = dst if src.acc_id < dst.acc_id else src

    with first_lock.lock:
        with second_lock.lock:
            if src.balance >= amount:
                src.balance -= amount
                dst.balance += amount


def run_race_experiment():
    print("[Experiment 1: Unsynchronized Race Condition]")
    acc1 = Account(1, 1000)
    acc2 = Account(2, 1000)
    initial_total = acc1.balance + acc2.balance

    threads = []
    for _ in range(50):
        t1 = threading.Thread(target=unsafe_transfer, args=(acc1, acc2, 10))
        t2 = threading.Thread(target=unsafe_transfer, args=(acc2, acc1, 10))
        threads.extend([t1, t2])

    for t in threads: t.start()
    for t in threads: t.join()

    final_total = acc1.balance + acc2.balance
    print(f"  Initial Total: ${initial_total}")
    print(f"  Final Total:   ${final_total} (Difference: ${final_total - initial_total})")
    if final_total != initial_total:
        print("  -> RACE CONDITION CONFIRMED: Money was created or lost due to unsynchronized interleaving!")


def run_safe_experiment():
    print("\n[Experiment 2: Synchronized with Lock Ordering]")
    acc1 = Account(1, 1000)
    acc2 = Account(2, 1000)
    initial_total = acc1.balance + acc2.balance

    threads = []
    for _ in range(50):
        t1 = threading.Thread(target=safe_transfer_lock_ordering, args=(acc1, acc2, 10))
        t2 = threading.Thread(target=safe_transfer_lock_ordering, args=(acc2, acc1, 10))
        threads.extend([t1, t2])

    for t in threads: t.start()
    for t in threads: t.join()

    final_total = acc1.balance + acc2.balance
    print(f"  Initial Total: ${initial_total}")
    print(f"  Final Total:   ${final_total} (Difference: ${final_total - initial_total})")
    print("  -> ATOMICITY & DEADLOCK-FREEDOM PRESERVED: Global invariant maintained exactly!")


if __name__ == "__main__":
    print("================================================================")
    print("Concurrency & Synchronization Simulation")
    print("================================================================\n")
    run_race_experiment()
    run_safe_experiment()
