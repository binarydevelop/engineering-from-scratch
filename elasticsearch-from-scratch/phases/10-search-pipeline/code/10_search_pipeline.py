#!/usr/bin/env python3

def simulate_query_phase(shards_data, query_term, top_k=2):
    # Phase 1: Query Phase (returns only doc_id and score)
    shard_results = {}
    for shard_id, docs in shards_data.items():
        candidates = []
        for doc_id, text in docs.items():
            if query_term in text.lower():
                score = round(1.0 + (len(text) % 3) * 0.5, 2)
                candidates.append((doc_id, score))
        candidates.sort(key=lambda x: x[1], reverse=True)
        shard_results[shard_id] = candidates[:top_k]
    return shard_results

def simulate_fetch_phase(shards_data, winning_ids):
    # Phase 2: Fetch Phase (retrieves full body only for winning IDs)
    docs = {}
    for shard_id, shard_docs in shards_data.items():
        for doc_id in winning_ids:
            if doc_id in shard_docs:
                docs[doc_id] = shard_docs[doc_id]
    return docs

if __name__ == "__main__":
    cluster_shards = {
        "shard_0": {101: "Elasticsearch distributed cluster", 102: "Kafka streaming log"},
        "shard_1": {201: "Elasticsearch fast inverted index", 202: "Redis in-memory store"}
    }
    print("--- Phase 1: Query Phase ---")
    shard_candidates = simulate_query_phase(cluster_shards, "elasticsearch", top_k=2)
    print("Shard candidate scores:", shard_candidates)

    all_candidates = []
    for s_hits in shard_candidates.values():
        all_candidates.extend(s_hits)
    all_candidates.sort(key=lambda x: x[1], reverse=True)
    top_winners = [doc_id for doc_id, score in all_candidates[:2]]
    print("Top global winners:", top_winners)

    print("\n--- Phase 2: Fetch Phase ---")
    fetched = simulate_fetch_phase(cluster_shards, top_winners)
    print("Fetched documents:", fetched)
