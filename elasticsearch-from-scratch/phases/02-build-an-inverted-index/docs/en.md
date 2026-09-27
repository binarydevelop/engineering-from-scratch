# Lesson 02.1: Build an Inverted Index

## Motto
"The inverted index is the atom of search: map terms to sorted document IDs, and search becomes set intersection."

## Problem
In Phase 01, linear scan required checking every document. We need an indexing data structure where looking up any word immediately gives us the exact list of matching documents in $O(1)$ time.

## Prediction
Will building an in-memory inverted index permit query execution in under 0.05 milliseconds regardless of corpus size?

## Why this matters
Every modern search engine (Elasticsearch, Lucene, Solr, Tantivy) is fundamentally an inverted index manager. Mastering this structure removes all mysticism from full-text search.

## First principles
A forward index maps:
`Document ID -> [List of Words]`
An **inverted index** inverts this relationship:
`Word (Term) -> [Sorted List of Document IDs]` (called the Postings List).

## Mental model
```text
Documents:
  Doc 1: "redis cache"
  Doc 2: "kafka log stream"
  Doc 3: "redis stream"

Inverted Index:
  cache  ──► [1]
  kafka  ──► [2]
  log    ──► [2]
  redis  ──► [1, 3]
  stream ──► [2, 3]
```

## Build it
See `code/mini_search.py` which builds a dictionary-based inverted index supporting `index()` and `search()`.

## Use Elasticsearch
Run the experiment:
```bash
./phases/02-build-an-inverted-index/experiments/run_experiment.sh
```

## Inspect it
Inspect the postings list generated for common terms in `code/mini_search.py`.

## Measure it
Compare query latency: linear scan ($O(N)$) vs inverted index ($O(1)$ dictionary lookup).

## Break it
Search for uppercase `"Redis"` in our naive inverted index without normalization. Observe that it fails to match `"redis"`.

## Recover it
This limitation motivates Phase 03 (Tokenization) and Phase 04 (Normalization).

## Modify it
Extend `mini_search.py` to index 20,000 documents and measure index construction time vs query time.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must the postings list be stored in sorted order by Document ID?
2. What is the space-time trade-off of maintaining an inverted index?

## Guarantees
* Query time is independent of non-matching document volume.

## Non-guarantees
* An inverted index does not preserve document sentence structure or formatting.

## When to use this
* As the foundational data structure for any full-text or tokenized attribute search.

## When not to use this
* When data changes every millisecond and write throughput cannot tolerate index updates.

## What comes next
In Phase 03, we explore tokenization: converting arbitrary strings into discrete index terms.
