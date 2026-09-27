#!/usr/bin/env python3
def explain_anti_patterns():
    print("==================================================")
    print("      THE TEN CATASTROPHIC REDIS ANTI-PATTERNS    ")
    print("==================================================")
    patterns = [
        ("1. Running KEYS *", "O(N) full keyspace scan blocks the single-threaded event loop for seconds/minutes. Fix: Use SCAN."),
        ("2. Giant Values (>1MB)", "Saturates network buffers and causes allocation stalls. Fix: Chunk or store in S3."),
        ("3. Unbounded Keyspace", "Writing keys with no TTL or eviction policy guarantees OOM crash. Fix: Set maxmemory + TTL."),
        ("4. Synchronized TTL", "Setting 10,000 keys with identical 300s TTL causes simultaneous stampede. Fix: Add TTL jitter."),
        ("5. Unsafe Lock Release", "Releasing lock without verifying ownership token deletes another worker's lock."),
        ("6. Pub/Sub for Tasks", "Pub/Sub is ephemeral; offline workers lose messages permanently. Fix: Use Streams."),
        ("7. Deserialization Churn", "Storing domain objects as JSON blobs requires full serialization for 1 field. Fix: Hashes."),
        ("8. Monolithic Hash/Set", "Putting 1,000,000 items in one key destroys clustering and listpack benefits. Fix: Shard keys."),
        ("9. Assuming Sync Replicas", "Replication is async; reading immediately from replica returns stale data. Fix: Read primary or WAIT."),
        ("10. Cross-Slot Transactions", "MULTI/EXEC across different cluster slots fails without hash tags {...}.")
    ]
    for name, desc in patterns:
        print(f"\n• {name}\n  {desc}")

if __name__ == "__main__":
    explain_anti_patterns()
