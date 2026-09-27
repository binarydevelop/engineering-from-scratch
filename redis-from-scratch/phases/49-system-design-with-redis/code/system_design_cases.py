#!/usr/bin/env python3
def print_system_design_scenarios():
    print("12 PRODUCTION SYSTEM DESIGN SCENARIOS WITH REDIS:")
    scenarios = [
        "1. Distributed Session Store (String with TTL / volatile-lru)",
        "2. API Rate Limiting Gateway (Token Bucket via Lua Script)",
        "3. Real-Time Gaming Leaderboard (Sorted Set with ZREVRANGE)",
        "4. Live Chat User Presence System (Bitmap / Set with Heartbeat TTL)",
        "5. Distributed Mutex Lock (Single Instance SET NX PX with UUID token)",
        "6. E-Commerce Flash Sale Inventory (Lua Atomic Decrement)",
        "7. Asynchronous Task Queue (Redis Streams with Consumer Groups)",
        "8. Web Page Cache-Aside Layer (Strings with Jittered TTL + Single-Flight)",
        "9. Top-K Trending Hashtags (Count-Min Sketch + Sorted Set)",
        "10. Idempotency Key Validator (SET NX EX for Payment APIs)",
        "11. Delayed Job Scheduler (Sorted Set with Execution Timestamp Score)",
        "12. Real-Time Analytics Counter Aggregator (HyperLogLog & Hashes)"
    ]
    for s in scenarios:
        print(f"  • {s}")

if __name__ == "__main__":
    print_system_design_scenarios()
