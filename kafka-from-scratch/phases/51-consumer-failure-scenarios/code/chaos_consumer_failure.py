#!/usr/bin/env python3
import time

def simulate_consumer_failure_modes():
    print("=== Consumer Failure Scenario Matrix ===\n")
    print("Scenario A: Worker killed by SIGKILL (Crash before commit)")
    print(" -> Consequence: Assigned partitions reassigned to peer; uncommitted batch reprocessed (DUPLICATE RISK)\n")

    print("Scenario B: Worker hangs on external API call > max.poll.interval.ms")
    print(" -> Consequence: Coordinator evicts worker! Triggers group REBALANCE!\n")

    print("Scenario C: Poison pill deserialization error")
    print(" -> Consequence: Crash loop forever without DLT quarantine!\n")

if __name__ == "__main__":
    simulate_consumer_failure_modes()
