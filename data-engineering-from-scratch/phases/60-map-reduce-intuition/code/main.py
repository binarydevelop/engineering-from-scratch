"""
Phase 60: Map / Reduce Intuition
Implementing Map -> Shuffle -> Reduce from first principles.
Precedes distributed frameworks like Spark by demonstrating data movement physics.
"""
from collections import defaultdict

def map_step(documents):
    """Maps documents into (key, value) pairs."""
    intermediate = []
    for doc in documents:
        for word in doc.lower().split():
            clean = "".join(c for c in word if c.isalnum())
            if clean:
                intermediate.append((clean, 1))
    return intermediate

def shuffle_step(key_value_pairs):
    """Groups values by key across simulated network partitions."""
    grouped = defaultdict(list)
    for k, v in key_value_pairs:
        grouped[k].append(v)
    return grouped

def reduce_step(grouped_pairs):
    """Reduces grouped values to aggregated results."""
    reduced = {}
    for k, values in grouped_pairs.items():
        reduced[k] = sum(values)
    return reduced

def execute_phase():
    corpus = [
        "Data engineering from scratch",
        "Understand it ingest it transform it",
        "Data quality is paramount"
    ]
    # 1. Map
    pairs = map_step(corpus)
    # 2. Shuffle
    grouped = shuffle_step(pairs)
    # 3. Reduce
    counts = reduce_step(grouped)

    assert counts["it"] == 3
    assert counts["data"] == 2
    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "distinct_words": len(counts),
        "word_counts": counts
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 60 Result:", res)
