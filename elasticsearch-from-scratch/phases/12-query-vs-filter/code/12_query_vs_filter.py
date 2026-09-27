#!/usr/bin/env python3
import time
import math

def simulate_query_context(docs, term):
    # Computes scoring cost
    hits = []
    for doc_id, text in docs.items():
        count = text.lower().count(term)
        if count > 0:
            score = count * math.log(100.0)
            hits.append((doc_id, score))
    return hits

def simulate_filter_context(docs, target_category):
    # Binary bitset check
    bitset = []
    for doc_id, cat in docs.items():
        bitset.append((doc_id, 1 if cat == target_category else 0))
    return [doc_id for doc_id, matched in bitset if matched == 1]

if __name__ == "__main__":
    docs = {i: "ergonomic wireless keyboard mechanical switch" for i in range(10000)}
    categories = {i: "electronics" if i % 2 == 0 else "furniture" for i in range(10000)}

    t0 = time.perf_counter()
    for _ in range(50):
        _ = simulate_query_context(docs, "wireless")
    query_time = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    for _ in range(50):
        _ = simulate_filter_context(categories, "electronics")
    filter_time = (time.perf_counter() - t0) * 1000

    print(f"50x Query Context (Scoring): {query_time:.2f} ms")
    print(f"50x Filter Context (Bitset):  {filter_time:.2f} ms")
