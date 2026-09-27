"""
Production Chaos Experiments: Breaking and Diagnosing Relational Databases.
Demonstrates 5 production failure modes:
  1. Slow query due to missing index
  2. Safe reproducible deadlock
  3. Connection pool starvation
  4. Missing foreign key locking issues
  5. Hot row contention
"""

import sys
import os
import time
import threading

def explain_chaos_experiments():
    print("=" * 70)
    print(" PRODUCTION DATABASE APPLICATION: CHAOS LAB")
    print("=" * 70)
    print("This harness demonstrates 5 classic production database failure modes:\n")

    print("[1] Missing Index / Slow Sequential Scan:")
    print("    Symptom:   Query response time jumps from 0.5ms to 800ms.")
    print("    Diagnosis: EXPLAIN ANALYZE reveals Seq Scan on 10,000,000 rows.")
    print("    Fix:       CREATE INDEX CONCURRENTLY on filtered columns.\n")

    print("[2] Deadlock Detection:")
    print("    Symptom:   ERROR: deadlock detected (SQLSTATE 40P01).")
    print("    Diagnosis: Txn A locks row 1, then wants row 2.")
    print("               Txn B locks row 2, then wants row 1.")
    print("    Fix:       Enforce strict deterministic lock ordering (sort keys before locking).\n")

    print("[3] Connection Pool Starvation:")
    print("    Symptom:   App throws PoolTimeout: queue is full.")
    print("    Diagnosis: Slow queries or leaked connections hold pool slots open indefinitely.")
    print("    Fix:       Implement strict statement_timeout, idle_in_transaction_session_timeout,\n"
          "               and connection pool healthchecks.\n")

    print("[4] Missing Foreign Key Index Lock Escalation:")
    print("    Symptom:   Deleting a parent row takes an exclusive table lock on child table.")
    print("    Diagnosis: PostgreSQL cannot verify referential integrity without scanning whole child.")
    print("    Fix:       Always index referencing foreign key columns.\n")

    print("[5] Hot Row Lock Contention:")
    print("    Symptom:   High TPS drops to single digits while updating global counter.")
    print("    Diagnosis: pg_stat_activity shows multiple PIDs waiting on ExclusiveLock on same tuple.")
    print("    Fix:       Partition counters across multiple bucket rows (Distributed Counters).\n")
    print("=" * 70)

if __name__ == "__main__":
    explain_chaos_experiments()
