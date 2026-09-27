#!/usr/bin/env python3
import time
from collections import defaultdict

class MiniInvertedIndex:
    def __init__(self):
        # term -> sorted list of doc_ids
        self.index = defaultdict(list)
        self.documents = {}

    def add_document(self, doc_id, text):
        self.documents[doc_id] = text
        # Simple whitespace splitting for now
        tokens = text.lower().split()
        seen = set()
        for token in tokens:
            if token not in seen:
                self.index[token].append(doc_id)
                seen.add(token)

    def search(self, term):
        term = term.lower()
        return self.index.get(term, [])

if __name__ == "__main__":
    engine = MiniInvertedIndex()
    docs = [
        "Distributed search with Elasticsearch",
        "Apache Kafka event streaming architecture",
        "Redis in-memory caching and search",
        "Distributed database replication and sharding"
    ]
    for idx, doc in enumerate(docs):
        engine.add_document(idx, doc)

    query = "distributed"
    start = time.perf_counter()
    results = engine.search(query)
    elapsed = (time.perf_counter() - start) * 1000

    print(f"Query: '{query}' -> Matching Doc IDs: {results}")
    print(f"Matching Documents:")
    for doc_id in results:
        print(f"  - [{doc_id}]: {engine.documents[doc_id]}")
    print(f"Lookup Latency: {elapsed:.4f} ms")
