#!/usr/bin/env python3
import heapq

def simulate_shard_search(shard_id, docs, query, top_k=5):
    # Local shard search
    candidates = []
    for doc_id, text in docs.items():
        if query in text:
            # Score simulation
            score = round(len(text) * 0.1 + (doc_id % 7) * 0.5, 2)
            candidates.append((score, doc_id, shard_id))
    candidates.sort(reverse=True)
    return candidates[:top_k]

def coordinate_scatter_gather(shards_data, query, top_k=5):
    # 1. Scatter to all shards
    gathered_candidates = []
    for s_id, docs in shards_data.items():
        shard_top = simulate_shard_search(s_id, docs, query, top_k)
        gathered_candidates.extend(shard_top)

    # 2. Global priority queue merge
    global_top = heapq.nlargest(top_k, gathered_candidates, key=lambda x: x[0])
    return global_top

if __name__ == "__main__":
    shards = {
        0: {1: "distributed search engine", 2: "kafka log engine"},
        1: {3: "search engine indexing", 4: "redis memory cache"},
        2: {5: "search relevance engine", 6: "postgres sql database"}
    }
    top_results = coordinate_scatter_gather(shards, "engine", top_k=3)
    print("Coordinating Node - Global Merged Top 3 Results:")
    for score, doc_id, shard_id in top_results:
        print(f"  Doc [{doc_id}] from Shard [{shard_id}] - Score: {score}")
