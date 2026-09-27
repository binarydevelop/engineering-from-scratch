#!/usr/bin/env python3
import sys

def simulate_fielddata_build(postings):
    # Un-invert postings list into doc_id -> list of terms in RAM
    fielddata_heap = {}
    for term, doc_ids in postings.items():
        for d in doc_ids:
            fielddata_heap.setdefault(d, []).append(term)
    return fielddata_heap

if __name__ == "__main__":
    postings = {
        f"term_{i}": list(range(i % 100, 1000, 50)) for i in range(5000)
    }
    print(f"Inverted Index Postings Count: {len(postings)} terms")
    fielddata = simulate_fielddata_build(postings)
    print(f"Un-inverted Fielddata Map Size in RAM: {len(fielddata)} docs")
    print(f"Estimated memory overhead of heap mapping: {sys.getsizeof(fielddata)} bytes")
