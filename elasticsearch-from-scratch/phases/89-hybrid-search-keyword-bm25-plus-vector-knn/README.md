# Phase 89: Hybrid Search: Combining BM25 Keyword Relevance with Dense Vector kNN

## 1. Why This Matters for MAANG & Senior/Staff Roles
Traditional keyword search (BM25) fails on semantic meaning, synonyms, and conversational queries ('laptop that runs fast and does not heat up'). Pure vector search (dense embeddings via kNN) struggles with exact product SKUs, model numbers ('iPhone 15 Pro Max 256GB'), and rare keywords. Modern production search and RAG platforms combine BM25 and Vector Search into a unified Hybrid Search pipeline.

---

## 2. Core Concepts & Architecture Deep-Dive
### Architecture of Hybrid Search
1. **Dual Indexing**:
   - Field `content`: Analyzed text indexed into standard Lucene Inverted Index (BM25 term frequency / inverse document frequency).
   - Field `embedding`: Dense float vector (e.g., 768 or 1536 dimensions) indexed into HNSW (Hierarchical Navigable Small World) graph.
2. **Query Execution**:
   - Query executes BM25 search -> returns top-K ranked documents by keyword match score.
   - Query embedding executes kNN vector search -> returns top-K ranked documents by cosine similarity.
3. **Score Normalization & Fusion**:
   BM25 scores (unbounded: 0 to infinity) cannot be added directly to cosine similarity scores (0 to 1). We apply **Reciprocal Rank Fusion (RRF)**:
   `RRF_Score(doc) = Sum( 1 / (k + rank_i(doc)) )`
   where `k` is a smoothing constant (typically 60). Documents appearing near the top of both keyword and vector result lists receive the highest composite rank.

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Optimization Strategies
- **"Why is exact kNN impossible at scale and how do you mitigate it?"**:
  Exact kNN computes distance against every document in the index (O(N) brute force), which is unusable on 100 million documents. Production systems use Approximate Nearest Neighbor (ANN) algorithms (HNSW graph or Inverted File Index - IVF) trading 1-2% recall for sub-10ms response times.
- **"How does Vector Quantization (SQ / PQ) reduce memory costs?"**:
  Storing millions of 1536-dimensional float32 vectors in RAM consumes hundreds of gigabytes. Scalar Quantization (SQ) compresses 32-bit floats to 8-bit integers (`int8`), reducing RAM by 75% with negligible recall degradation.

---

## 4. Hands-On Practice & Implementation Drills
### Elasticsearch Hybrid Search Query DSL
```json
{
  "query": {
    "match": {
      "title": "lightweight developer laptop"
    }
  },
  "knn": {
    "field": "title_embedding",
    "query_vector": [0.021, -0.043, 0.129, 0.088],
    "k": 50,
    "num_candidates": 100
  },
  "rank": {
    "rrf": {
      "window_size": 50,
      "rank_constant": 60
    }
  }
}
```

---

## 5. Key Takeaways & Cheat Sheet
- BM25 handles exact keyword and SKU matching; Vector kNN handles semantic intent.
- Hybrid Search combines both paths using Reciprocal Rank Fusion (RRF).
- Use HNSW for Approximate Nearest Neighbor (ANN) search to ensure low latency.
- Crucial for modern search engines, e-commerce discovery, and enterprise RAG systems.
