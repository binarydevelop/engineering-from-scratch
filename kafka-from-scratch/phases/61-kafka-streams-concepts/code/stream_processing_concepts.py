#!/usr/bin/env python3
def explain_stream_concepts():
    print("=== Core Stream Processing Concepts (Kafka Streams / Flink) ===\n")
    print("1. Stateless vs Stateful Operations:")
    print("   - Stateless: filter(), mapValues() -> 0 memory overhead.")
    print("   - Stateful:  count(), aggregate(), join() -> Requires persistent State Store (RocksDB).\n")

    print("2. The Stream-Table Duality (KStream vs KTable):")
    print("   - KStream: Every record is an INSERT. (e.g. clickstream, sensor reads)")
    print("   - KTable:  Every record is an UPSERT on key. (e.g. user profiles, account balances)\n")

    print("3. Co-Partitioning Invariant:")
    print("   - Joining Topic A and Topic B requires BOTH topics to have identical partition counts")
    print("     and identical key partitioners! Otherwise, matching keys land on different nodes!\n")

if __name__ == "__main__":
    explain_stream_concepts()
