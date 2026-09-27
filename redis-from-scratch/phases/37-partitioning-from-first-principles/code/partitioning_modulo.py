#!/usr/bin/env python3
import hashlib

def hash_key(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

def test_modulo_reshuffle(num_keys=10000):
    keys = [f"user_{i}" for i in range(num_keys)]
    
    # 4 Nodes
    assignments_4 = {k: hash_key(k) % 4 for k in keys}
    # Add Node 5
    assignments_5 = {k: hash_key(k) % 5 for k in keys}
    
    moved = sum(1 for k in keys if assignments_4[k] != assignments_5[k])
    pct = (moved / num_keys) * 100
    print(f"Naive Modulo Partitioning (Adding 1 node to a 4-node cluster):")
    print(f"  • Total keys: {num_keys:,}")
    print(f"  • Dislocated keys: {moved:,} ({pct:.1f}% of entire database had to move!)")
    print("Takeaway: This is why Redis Cluster uses 16,384 fixed Hash Slots rather than naive modulo.")

if __name__ == "__main__":
    test_modulo_reshuffle()
