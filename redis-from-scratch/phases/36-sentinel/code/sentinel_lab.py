#!/usr/bin/env python3
def explain_sentinel_topology():
    print("Redis Sentinel High Availability Architecture:")
    print("""
             [ Sentinel 1 ] ─── [ Sentinel 2 ] ─── [ Sentinel 3 ]
                   │                  │                  │
                   └──────────┬───────┴──────────┬───────┘
                              ▼                  ▼
                       [ Primary (6379) ]    [ Replica (6380) ]
    """)
    print("Failover Sequence:")
    print("  1. Primary stops responding to PING for 'down-after-milliseconds' (e.g. 5000ms).")
    print("  2. Sentinel detects SDOWN (Subjectively Down).")
    print("  3. Sentinel queries peers: if >= QUORUM agree, state transitions to ODOWN.")
    print("  4. Sentinels elect an Epoch Leader to conduct failover.")
    print("  5. Leader promotes best Replica to Primary via 'REPLICAOF NO ONE'.")
    print("  6. Remaining replicas are reconfigured to follow the new primary.")
    print("  7. Clients connecting via Sentinel driver are automatically redirected!")

if __name__ == "__main__":
    explain_sentinel_topology()
