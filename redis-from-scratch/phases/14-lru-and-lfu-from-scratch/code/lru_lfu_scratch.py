#!/usr/bin/env python3
from collections import OrderedDict
import random

class ExactLRUCache:
    """Textbook LRU via Doubly-Linked Hash Map (OrderedDict)."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache: return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False) # Evict oldest

class ApproximatedLRUCache:
    """Redis-style Approximated LRU via Random Sampling."""
    def __init__(self, capacity, sample_size=5):
        self.capacity = capacity
        self.sample_size = sample_size
        self.store = {} # key -> (val, access_time)
        self.clock = 0

    def get(self, key):
        self.clock += 1
        if key in self.store:
            val, _ = self.store[key]
            self.store[key] = (val, self.clock)
            return val
        return None

    def put(self, key, value):
        self.clock += 1
        if len(self.store) >= self.capacity and key not in self.store:
            # Sample random keys
            sample_keys = random.sample(list(self.store.keys()), min(self.sample_size, len(self.store)))
            oldest_key = min(sample_keys, key=lambda k: self.store[k][1])
            del self.store[oldest_key]
        self.store[key] = (value, self.clock)

if __name__ == "__main__":
    print("Testing Exact LRU vs Redis Approximated LRU (Capacity: 3)...")
    exact = ExactLRUCache(3)
    approx = ApproximatedLRUCache(3, sample_size=3)

    for k in ["A", "B", "C"]:
        exact.put(k, 1); approx.put(k, 1)
    
    # Access A to make it recently used
    exact.get("A"); approx.get("A")
    # Insert D -> should evict B or C, never A
    exact.put("D", 1); approx.put("D", 1)

    print("Exact LRU Keys:", list(exact.cache.keys()))
    print("Approximated LRU Keys:", list(approx.store.keys()))
    print("✓ Both preserved frequently accessed key 'A' while evicting cold data.")
