#!/usr/bin/env python3
def explain_slot_migration():
    print("Redis Cluster Online Resharding Protocol:")
    print("""
    [ Client ] ──────── 1. GET key ────────► [ Source Node (Slot 500) ]
                                                    │
                                                    │ Key already migrated?
                                                    ▼
    [ Client ] ◄─── 2. -ASK 500 10.0.0.2 ───────────┘
        │
        ├────── 3. ASKING ────────────────► [ Target Node (Slot 500) ]
        └────── 4. GET key ───────────────► Returns value!
    """)
    print("Properties:")
    print("  • -ASK redirect is temporary (only for that one query).")
    print("  • Client does NOT update its permanent slot cache until slot migration finishes")
    print("    and node broadcasts permanent -MOVED redirect.")

if __name__ == "__main__":
    explain_slot_migration()
