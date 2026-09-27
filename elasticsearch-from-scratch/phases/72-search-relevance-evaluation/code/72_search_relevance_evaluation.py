#!/usr/bin/env python3

def precision_at_k(retrieved_ids, relevant_ids, k=5):
    top_k = retrieved_ids[:k]
    matches = [d for d in top_k if d in relevant_ids]
    return len(matches) / float(k)

def reciprocal_rank(retrieved_ids, relevant_ids):
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

if __name__ == "__main__":
    golden_relevant = {101, 102}
    algo_a_results = [101, 500, 102, 600, 700]
    algo_b_results = [800, 900, 101, 102, 950]

    print("Algorithm A Results:", algo_a_results)
    print(f"  Precision@5: {precision_at_k(algo_a_results, golden_relevant, 5):.2f}")
    print(f"  MRR:         {reciprocal_rank(algo_a_results, golden_relevant):.2f}")

    print("\nAlgorithm B Results:", algo_b_results)
    print(f"  Precision@5: {precision_at_k(algo_b_results, golden_relevant, 5):.2f}")
    print(f"  MRR:         {reciprocal_rank(algo_b_results, golden_relevant):.2f}")
    print("\nAlgorithm A achieved superior MRR because the first relevant item appeared at rank 1!")
