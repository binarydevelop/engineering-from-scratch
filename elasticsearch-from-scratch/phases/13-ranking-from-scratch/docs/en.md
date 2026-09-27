# Lesson 13.1: Ranking From Scratch

## Motto
"Searching without ranking is finding needles in haystacks without knowing which needle is sharpest."

## Problem
A search for `"database"` matches 10,000 documents. If all matching documents are returned in arbitrary insertion order, the user must browse hundreds of pages to find the most relevant document.

## Prediction
If Document A mentions `"database"` once in a 1,000-word essay, and Document B mentions `"database"` five times in a 20-word summary, which document should rank first?

## Why this matters
Search quality is defined by ranking accuracy. A search engine that returns the right document at rank 50 is functionally equivalent to broken search.

## First principles
Ranking primitives:
1. **Term Frequency (TF):** How often does the term appear in this document? (More is generally better).
2. **Document Length:** How long is the document? (A match in a short title is more specific than in an encyclopedia).
3. **Document Frequency (DF):** How common is the word across all documents?

## Mental model
```text
Doc 1: "Database internals and database architecture." (Len: 5 words, TF: 2) ──► High Density!
Doc 2: "A very long history of computing mentioning a database once..." (Len: 50 words, TF: 1) ──► Low Density
```

## Build it
See `code/naive_ranking.py` implementing match-count vs density ranking in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/13-ranking-from-scratch/experiments/run_experiment.sh
```

## Inspect it
Observe ordering differences between raw occurrence count and density-normalized scores.

## Measure it
Compare top-3 ranks under naive count vs length-normalized ranking.

## Break it
Notice keyword stuffing: an author repeats `"database database database database"` 50 times to game naive frequency ranking.

## Recover it
Apply Term Frequency Saturation (introduced in Phase 15 with BM25).

## Modify it
Add title field weighting (boost factor $2	imes$) to simulate multi-field ranking.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does raw term count fail to rank documents accurately?
2. What is keyword stuffing and how does information retrieval defend against it?

## Guarantees
* Density ranking penalizes excessively verbose documents.

## Non-guarantees
* Simple density does not account for the global rarity of words.

## When to use this
* As the conceptual bridge from boolean matching to probabilistic ranking.

## When not to use this
* Production search (use modern BM25 instead).

## What comes next
In Phase 14, we introduce Inverse Document Frequency (TF-IDF intuition).
