#!/usr/bin/env python3
def explain_broker_addition():
    print("=== Broker Expansion vs Data Movement ===\n")
    print("1. Broker 4 registers with KRaft quorum: OK (Takes ~2 seconds)")
    print("2. Topic 'orders' partitions: [P0 on Broker 1, P1 on Broker 2, P2 on Broker 3]")
    print("3. Does Broker 4 host any partitions? NO. (0 partitions assigned)")
    print("4. Conclusion: Kafka does NOT automatically re-shuffle existing data!")
    print("5. Required Action: Run 'kafka-reassign-partitions.sh' to rebalance workload.\n")

if __name__ == "__main__":
    explain_broker_addition()
