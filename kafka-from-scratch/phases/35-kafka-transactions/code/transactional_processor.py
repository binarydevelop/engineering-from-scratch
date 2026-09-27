#!/usr/bin/env python3
import time

def simulate_transactional_flow():
    print("--- Simulating Kafka Two-Phase Transactional Commit ---")
    print("1. Producer registers transactional.id='order-processor-txn-1'")
    print("2. Coordinator assigns Producer ID (PID: 2005, Epoch: 1)")
    print("3. beginTransaction()")
    print("4. Appending transformed output record to 'orders-processed'...")
    print("5. Committing input offset 42 via sendOffsetsToTransaction()...")
    print("6. commitTransaction(): Coordinator appends COMMIT markers to logs.")
    print("7. Downstream read_committed consumer sees record! SUCCESS!\n")

    print("--- Simulating Aborted Transaction (Rollback) ---")
    print("1. beginTransaction()")
    print("2. Appending tentative record to 'orders-processed'...")
    print("3. CRASH / ERROR DETECTED! Calling abortTransaction()...")
    print("4. Coordinator appends ABORT marker.")
    print("5. Downstream read_committed consumer SKIPS tentative record! ZERO LEAKAGE!")

if __name__ == "__main__":
    simulate_transactional_flow()
