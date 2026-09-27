#!/usr/bin/env python3
import mmh3 # MurmurHash3 or built-in hash
import zlib
from collections import defaultdict

def kafka_default_partitioner(key_bytes: bytes, num_partitions: int) -> int:
    """
    Kafka's DefaultPartitioner uses Murmur2 (or positive hash % num_partitions).
    Here we simulate using standard 32-bit hash % num_partitions.
    """
    # Use CRC32 / positive int representation
    hash_val = zlib.crc32(key_bytes) & 0x7fffffff
    return hash_val % num_partitions

if __name__ == "__main__":
    num_partitions = 3
    print(f"Topic has {num_partitions} partitions.\n")

    # 1. Same key repeatedly
    key_a = b"user-42"
    print(f"--- 1. Producing 5 events with SAME key: {key_a.decode()} ---")
    for i in range(5):
        part = kafka_default_partitioner(key_a, num_partitions)
        print(f" Event {i} (Key: {key_a.decode()}) -> Partition: {part}")

    # 2. Different keys
    print("\n--- 2. Producing events with DIFFERENT keys ---")
    keys = [b"user-1", b"user-2", b"user-3", b"user-4", b"user-5", b"user-6"]
    dist = defaultdict(list)
    for k in keys:
        part = kafka_default_partitioner(k, num_partitions)
        dist[part].append(k.decode())
        print(f" Key: {k.decode()} -> Partition: {part}")

    print("\nSummary Partition Allocation:")
    for p in range(num_partitions):
        print(f"  Partition {p}: {dist[p]}")
