#!/usr/bin/env python3
def assign_partitions_range(partitions: list[int], consumers: list[str]) -> dict[str, list[int]]:
    """Simulates Kafka's RangeAssignor algorithm."""
    if not consumers: return {}
    num_parts = len(partitions)
    num_cons = len(consumers)
    parts_per_cons = num_parts // num_cons
    extra = num_parts % num_cons

    assignment = {}
    idx = 0
    for i, cons in enumerate(consumers):
        take = parts_per_cons + (1 if i < extra else 0)
        assignment[cons] = partitions[idx : idx + take]
        idx += take
    return assignment

if __name__ == "__main__":
    partitions = [0, 1, 2, 3] # 4 Partitions
    print(f"Topic Partitions: {partitions}\n")

    print("--- Scenario A: 1 Consumer in Group ---")
    print(assign_partitions_range(partitions, ["Consumer-A"]))

    print("\n--- Scenario B: 2 Consumers in Group ---")
    print(assign_partitions_range(partitions, ["Consumer-A", "Consumer-B"]))

    print("\n--- Scenario C: 4 Consumers in Group ---")
    print(assign_partitions_range(partitions, ["Consumer-A", "Consumer-B", "Consumer-C", "Consumer-D"]))
