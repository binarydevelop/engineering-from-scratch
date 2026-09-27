# Part X — Retrieval Systems (RAG) (Phases 134 – 144)

> **Motto:** Grounding beats guessing. Retrieve precise external evidence before asking a probabilistic model to synthesize facts.

---

## Phases 134 – 139: Indexing, Embeddings & Chunking
- **Phase 134 — Why Retrieval?:** Private data, freshness, and reducing hallucination without retraining.
- **Phase 135 — Lexical / Keyword Search:** Inverted index and BM25 scoring from first principles.
- **Phase 136 — Vector Embeddings:** Mapping text into high-dimensional latent space; embedding geometry and cosine distance.
- **Phase 137 — Vector Similarity Search:** Exact brute-force kNN vs approximate nearest neighbor (HNSW intuition).
- **Phase 138 — Chunking Strategies:** Fixed character chunks vs sliding windows vs sentence/semantic chunk boundaries.
- **Phase 139 — Metadata Filtering:** Pre-filtering by tenant ID, date range, and document classification before search.

---

## Phases 140 – 144: Hybrid Search, Reranking & Provenance
- **Phase 140 — Hybrid Search:** Reciprocal Rank Fusion (RRF) combining dense vector similarity with sparse BM25.
- **Phase 141 — Reranking:** Cross-encoder rerankers scoring candidate passages; measuring latency vs NDCG gains.
- **Phase 142 — RAG Pipeline:** Complete pipeline: ingestion $\to$ chunking $\to$ indexing $\to$ retrieval $\to$ synthesis (`projects/p10_production_rag_system.py`).
- **Phase 143 — Retrieval Failure Decomposition:** Isolating failure: Did retrieval miss? Was noise returned? Did model ignore?
- **Phase 144 — Citations & Provenance:** Grounding responses in retrieved chunks; detecting fabricated citations.
