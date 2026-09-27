"""
projects/distributed_simulator/cluster_simulator.py - Phase 81 Distributed Search Simulator.
Simulates a distributed cluster:
- 1 Coordinator Node (scatter-gather, query reduction, timeouts)
- 3 Shard Worker instances (independent data partitions)
- Primary shard hash routing
- Tail latency injection and partial hit tolerance
"""

import hashlib
import heapq
import time

class ShardNode:
    def __init__(self, node_id, lag_ms=0.0):
        self.node_id = node_id
        self.lag_ms = lag_ms
        self.is_alive = True
        self.documents = {}

    def index(self, doc_id, doc):
        if not self.is_alive:
            raise RuntimeError(f"Node {self.node_id} is down!")
        self.documents[doc_id] = doc

    def search_local(self, query_term, top_k=5):
        if not self.is_alive:
            raise RuntimeError(f"Node {self.node_id} connection refused!")
        if self.lag_ms > 0:
            time.sleep(self.lag_ms / 1000.0)

        candidates = []
        for doc_id, doc in self.documents.items():
            text = doc.get("text", "").lower()
            if query_term in text:
                # Local BM25 score simulation
                score = round(1.0 + len(text) * 0.05 + (doc_id % 5) * 0.2, 3)
                candidates.append((score, doc_id, self.node_id, doc))

        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[:top_k]

class CoordinatingNode:
    def __init__(self, shard_nodes):
        self.shards = {n.node_id: n for n in shard_nodes}

    def route_doc(self, doc_id):
        # hash(id) % num_shards
        h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
        return h % len(self.shards)

    def index(self, doc_id, doc):
        target = self.route_doc(doc_id)
        self.shards[target].index(doc_id, doc)
        return target

    def search(self, query_term, top_k=5, timeout_ms=100.0):
        t0 = time.perf_counter()
        gathered = []
        shards_successful = 0
        shards_failed = 0

        # Phase 1: Scatter to all shards
        for shard_id, node in self.shards.items():
            try:
                # Query shard
                shard_hits = node.search_local(query_term, top_k=top_k)
                gathered.extend(shard_hits)
                shards_successful += 1
            except Exception as e:
                shards_failed += 1

        # Phase 2: Priority Queue Merge (Top-K Reduction)
        winning_candidates = heapq.nlargest(top_k, gathered, key=lambda x: x[0])
        elapsed = (time.perf_counter() - t0) * 1000.0

        return {
            "took_ms": round(elapsed, 2),
            "timed_out": elapsed > timeout_ms,
            "_shards": {
                "total": len(self.shards),
                "successful": shards_successful,
                "failed": shards_failed
            },
            "hits": [
                {"_id": c[1], "_shard": c[2], "_score": c[0], "_source": c[3]}
                for c in winning_candidates
            ]
        }
