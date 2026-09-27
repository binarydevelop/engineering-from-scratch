#!/usr/bin/env python3
import time

def generate_docs(count):
    terms = ["wireless", "mechanical", "ergonomic", "bluetooth", "gaming", "portable", "battery", "fast", "quiet"]
    docs = []
    for i in range(count):
        desc = f"Product {i} has high quality features: {terms[i % len(terms)]} design with durable components."
        docs.append({"id": i, "description": desc})
    return docs

def linear_search(docs, term):
    hits = []
    for doc in docs:
        if term in doc["description"]:
            hits.append(doc["id"])
    return hits

if __name__ == "__main__":
    for size in [1000, 10000, 50000]:
        corpus = generate_docs(size)
        start = time.perf_counter()
        hits = linear_search(corpus, "wireless")
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Corpus size: {size:6d} docs | Hits: {len(hits):5d} | Latency: {elapsed:.3f} ms")
