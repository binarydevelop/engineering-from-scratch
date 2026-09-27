#!/usr/bin/env python3

class BitsetCacheSim:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def query_filter(self, segment_id, filter_term, doc_stream):
        key = (segment_id, filter_term)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        # Build bitset
        bitset = [1 if d.get("category") == filter_term else 0 for d in doc_stream]
        self.cache[key] = bitset
        return bitset

if __name__ == "__main__":
    docs = [{"id": i, "category": "tech" if i % 2 == 0 else "home"} for i in range(100)]
    c = BitsetCacheSim()
    print("Executing query 10 times for category='tech':")
    for _ in range(10):
        _ = c.query_filter("seg_0", "tech", docs)
    print(f"Results: Hits={c.hits}, Misses={c.misses} (First query built bitset, next 9 were instant cache hits!)")
