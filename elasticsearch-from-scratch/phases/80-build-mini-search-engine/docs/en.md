# Lesson 80.1: Build Mini Search Engine (Capstone 3)

## Motto
"Capstone 3: Construct a complete standalone search engine in pure Python: document store, tokenizer, inverted index, BM25 ranking, and boolean filters."

## Problem
True systems understanding is demonstrated by synthesis. If you truly understand Elasticsearch, you should be able to build a miniature, fully working search engine in pure Python without importing Lucene or external search libraries.

## Prediction
Can you build an end-to-end search engine in 250 lines of Python that indexes documents, builds inverted indexes, computes BM25 relevance, and executes boolean filters?

## Why this matters
This is the ultimate capstone of the single-node information retrieval curriculum.

## First principles
Mini Search Engine Components:
1. **Document Store:** Holds original raw documents (`_source`).
2. **Analysis Pipeline:** Lowercases, tokenizes on word boundaries, and discards stop words.
3. **Inverted Index:** Sorted postings lists with term frequencies and positions.
4. **Columnar Doc Values:** Fast column lookup for filtering and sorting.
5. **BM25 Scorer:** Implements $k_1$ saturation and $b$ length normalization.
6. **Query Engine:** Parses and executes `must`, `filter`, and `should` queries.

## Mental model
```text
┌─────────────────────────────────────────────────────────────┐
│                 MINI SEARCH ENGINE IN PYTHON                │
├─────────────────────────────────────────────────────────────┤
│  Document Store  │ Inverted Index │ Doc Values │ BM25 Scorer│
└─────────────────────────────────────────────────────────────┘
                               │
               API: engine.index(id, doc)
               API: engine.search(query_dsl)
                               │
                               ▼
           Top-K Scored & Filtered Search Results!
```

## Build it
See `projects/mini_search_engine/` and `code/mini_search_engine.py` for the complete implementation.

## Use Elasticsearch
Run the experiment:
```bash
./phases/80-build-mini-search-engine/experiments/run_experiment.sh
```

## Inspect it
Index a corpus of 100 documents and execute multi-clause boolean queries.

## Measure it
Benchmark query latency on our Python mini engine vs Elasticsearch.

## Break it
Feed edge-case inputs: empty strings, unknown terms, all-stop-word queries.

## Recover it
Implement graceful empty-result handling.

## Modify it
Add phrase matching using the stored token positions.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does your Python inverted index mirror Lucene's internal data structures?
2. What trade-offs did you make between memory usage and query speed in your implementation?

## Guarantees
* A self-contained, dependency-free reference implementation of core search engine principles.

## Non-guarantees
* Not intended for multi-terabyte production data (pure in-memory Python).

## When to use this
* Deep conceptual mastery and interview demonstration of search internals.

## When not to use this
* Large-scale production storage.

## What comes next
In Phase 81, we simulate distributed cluster coordination across multiple shards and nodes.
