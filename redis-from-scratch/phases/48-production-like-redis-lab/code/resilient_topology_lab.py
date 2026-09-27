#!/usr/bin/env python3
def explain_capstone_topology():
    print("==================================================")
    print("  CAPSTONE 2: RESILIENT PRODUCTION TOPOLOGY LAB   ")
    print("==================================================")
    print("""
    [ Fast API / Client Application ]
                 │
                 ├── Writes ──► [ Primary Redis (6379) ] ── (Async Stream) ──► [ Replica (6380) ]
                 │                     ▲                                              ▲
                 │                     └──────────┬───────────────────────────────────┘
                 ▼                                │ (Health Monitoring & Failover)
          [ Sentinel Quorum ] ────────────────────┘
    """)
    print("Verification Scenarios:")
    print("  1. Standard Baseline: Read from cache, fallback to PostgreSQL.")
    print("  2. Primary Crash: Kill redis-primary container.")
    print("  3. Sentinel Failover: Observe Sentinel promoting replica to primary.")
    print("  4. Client Reconnect: Application automatically redirects writes to new primary.")

if __name__ == "__main__":
    explain_capstone_topology()
