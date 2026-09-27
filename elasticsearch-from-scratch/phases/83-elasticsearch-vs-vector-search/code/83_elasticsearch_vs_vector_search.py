#!/usr/bin/env python3
import math

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    return dot / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0.0

if __name__ == "__main__":
    # Simulated 3D semantic embeddings
    query_vec = [0.8, 0.6, 0.0] # "camping sleeping gear"
    doc_a_vec = [0.78, 0.62, 0.05] # "ultralight mattress pad" (No common words, but high semantic similarity!)
    doc_b_vec = [0.1, 0.05, 0.99] # "gardening lawn mower"

    sim_a = cosine_similarity(query_vec, doc_a_vec)
    sim_b = cosine_similarity(query_vec, doc_b_vec)

    print("Vector Search Semantic Matching:")
    print(f"  Similarity to 'ultralight mattress pad': {sim_a:.4f} (High match!)")
    print(f"  Similarity to 'gardening lawn mower':   {sim_b:.4f} (Low match)")
