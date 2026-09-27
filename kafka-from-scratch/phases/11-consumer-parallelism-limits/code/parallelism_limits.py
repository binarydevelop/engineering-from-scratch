#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../10-consumer-groups-from-first-principles/code")))
from consumer_group_sim import assign_partitions_range

def test_limits():
    partitions = [0, 1, 2] # 3 Partitions
    consumers = [f"Worker-{i}" for i in range(1, 6)] # 5 Consumers

    assignment = assign_partitions_range(partitions, consumers)
    print(f"Topic Partitions: {len(partitions)}")
    print(f"Active Consumers in Group: {len(consumers)}\n")

    for cons, parts in assignment.items():
        status = f"ACTIVE (Partitions: {parts})" if parts else "IDLE (Hot-standby)"
        print(f"  {cons}: {status}")

if __name__ == "__main__":
    test_limits()
