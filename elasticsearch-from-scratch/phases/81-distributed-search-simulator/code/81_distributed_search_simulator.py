#!/usr/bin/env python3
import time
import hashlib
import random

class ShardWorker:
    def __init__(self, shard_id, lag_ms=0):
        self.shard_id = shard_id
        self.lag_ms = lag_ms
        self.data = {}

    def index(self, doc_id, text):
        self.data[doc_id] = text

    def query(self, term):
        if self.lag_ms > 0:
            time.sleep(self.lag_ms / 1000.0)
        hits = [(doc_id, text) for doc_id, text in self.data.items() if term in text.lower()]
        return {"shard": self.shard_id, "hits": hits}

class Coordinator:
    def __init__(self, shards):
        self.shards = shards

    def index(self, doc_id, text):
        h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
        target = h % len(self.shards)
        self.shards[target].index(doc_id, text)

    def search(self, term):
        t0 = time.perf_counter()
        results = []
        for s in self.shards:
            res = s.query(term)
            results.extend(res["hits"])
        elapsed = (time.perf_counter() - t0) * 1000
        return results, elapsed

if __name__ == "__main__":
    # Shard 0 & 1 are fast; Shard 2 has 80ms network lag!
    workers = [ShardWorker(0, lag_ms=2), ShardWorker(1, lag_ms=3), ShardWorker(2, lag_ms=80)]
    coord = Coordinator(workers)

    coord.index(1, "distributed systems design")
    coord.index(2, "distributed database replication")
    coord.index(3, "distributed search algorithms")

    hits, duration = coord.search("distributed")
    print(f"Distributed Search completed across 3 Shards:")
    print(f"  Total Hits: {len(hits)}")
    print(f"  Total Duration: {duration:.2f} ms (Bounded by Shard 2's 80ms lag!)")
