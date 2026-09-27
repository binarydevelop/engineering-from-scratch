# Lesson 83.1: Elasticsearch vs Vector Search

## Motto
"Lexical search matches exact terms; vector search matches conceptual embeddings. Hybrid search unites both."

## Problem
A user searches for: *"something comfortable to sleep on during a hiking trip"*.
A traditional lexical BM25 query looks for documents containing the words `"comfortable"`, `"sleep"`, and `"hiking"`. If an item is titled *"Ultralight Inflatable Camp Mattress"*, BM25 returns 0 hits because the words do not overlap lexically!

## Prediction
Can dense vector embeddings match semantically related items that share zero common words with the query?

## Why this matters
Modern search combines **Lexical BM25 Search** (for exact keywords, part numbers, SKUs, and names) with **Dense Vector Search** (for conceptual semantic intent) using **Reciprocal Rank Fusion (RRF)**.

## First principles
* **Lexical Search (BM25):** Operates on discrete tokens in an inverted index. Fast, precise, but suffers from vocabulary mismatch.
* **Vector Search ($k$-NN / HNSW):** Encodes text into a continuous high-dimensional vector space ($\mathbb{R}^{768}$ or $\mathbb{R}^{1536}$). Finds nearest neighbors using cosine similarity.
* **Hybrid Search (Elasticsearch 8.x):** Executes both lexical BM25 and dense vector search in parallel, merging candidate lists with Reciprocal Rank Fusion (RRF).

## Mental model
```text
Query: "portable sleeping mat"
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
1. LEXICAL BM25             2. DENSE VECTOR (HNSW)
(Exact term matches)        (Embedding distance in 768 dims)
"portable", "sleeping"      Matches "Ultralight Inflatable Pad"
       │                           │
       └─────────────┬─────────────┘
                     ▼
        RECIPROCAL RANK FUSION (RRF)
     ──► Perfectly Balanced Hybrid Hits!
```

## Build it
See `code/vector_vs_lexical_sim.py` demonstrating cosine vector similarity vs BM25 in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/83-elasticsearch-vs-vector-search/experiments/run_experiment.sh
```

## Inspect it
Create an index with `dense_vector` mapping:
```bash
curl -X PUT http://localhost:9200/vector_demo -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "embedding": {
        "type": "dense_vector",
        "dims": 3,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}'
```

## Measure it
Compare query latency: BM25 inverted index lookup (< 2ms) vs HNSW graph traversal (~10ms).

## Break it
Search for an exact part number (`"X49-B091-REV3"`) using pure vector search: vector embeddings struggle with exact alphanumeric codes!

## Recover it
Use **Hybrid Search**: BM25 catches exact codes, vector search catches conceptual meaning.

## Modify it
Execute an Elasticsearch $k$-NN query:
```json
{
  "knn": {
    "field": "embedding",
    "query_vector": [0.1, 0.8, -0.4],
    "k": 5,
    "num_candidates": 50
  }
}
```

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does pure vector search often fail on exact model numbers and serial numbers?
2. What is Reciprocal Rank Fusion (RRF) and why is it preferred over raw score addition?

## Guarantees
* Dense vector search matches semantic concepts without requiring shared vocabulary.

## Non-guarantees
* Vector search is computationally more expensive and consumes significantly more RAM than inverted indexes.

## When to use this
* Natural language questions, semantic discovery, and AI-assisted search.

## When not to use this
* Exact SKU lookup, structured log filtering, or numeric range filtering.

## What comes next
In Phase 84, we catalogue the 15 Fatal Elasticsearch Anti-Patterns.
