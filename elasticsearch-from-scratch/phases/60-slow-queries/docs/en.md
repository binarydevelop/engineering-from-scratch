# Lesson 60.1: Slow Queries

## Motto
"Slow queries are caused by predictable anti-patterns: leading wildcards, script scoring, deep paging, and giant aggs."

## Problem
A search endpoint intermittently spikes from 10ms to 8,000ms, causing cascading timeouts in upstream microservices. How do you identify which specific queries are responsible?

## Prediction
Can you configure Elasticsearch to automatically log any query that takes longer than 200ms to a dedicated slow-log file?

## Why this matters
Slow queries block search thread pool queues. Finding and optimizing slow queries is the core operational duty of search engineering.

## First principles
The Four Horsemen of Slow Queries:
1. **Leading Wildcards / Unanchored Regex:** `*search*` scans the entire term dictionary.
2. **Deep Pagination:** `from: 50000` forces massive coordinator sorting.
3. **High-Cardinality Deep Aggregations:** Combinatorial explosion of bucket allocations.
4. **Painless Script Filters:** Running runtime scripts on every document bypasses Lucene indexes.
* **Search Slow Log:** Automatically records slow queries exceeding configurable latency thresholds (`warn`, `info`, `debug`, `trace`).

## Mental model
```text
Client Query ──► Executes on Shard
                        │
                [ Query took 450ms ]
                        │
              Is 450ms > threshold (200ms)?
                        │
                        ▼ YES
            Append full query JSON & shard details
            to 'elasticsearch_index_search_slowlog.log'!
```

## Build it
See `code/slow_query_detector.py` analyzing query complexity patterns in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/60-slow-queries/experiments/run_experiment.sh
```

## Inspect it
Configure dynamic slow log thresholds on an index:
```bash
curl -X PUT http://localhost:9200/products_phase06/_settings -H "Content-Type: application/json" -d '{
  "index.search.slowlog.threshold.query.warn": "200ms",
  "index.search.slowlog.threshold.query.info": "50ms"
}'
```

## Measure it
Run an expensive wildcard query and inspect slow log output.

## Break it
Execute a regex query with multiple wildcards across millions of documents to trigger slow logs.

## Recover it
Replace slow wildcards with `wildcard` field types or edge n-grams.

## Modify it
Set `index.indexing.slowlog.threshold.index.warn` to audit slow write operations.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a Painless script filter execute slower than an equivalent Lucene boolean query?
2. What information does the Elasticsearch search slow log capture?

## Guarantees
* Slow logs provide an exact audit trail of offending queries and their execution times.

## Non-guarantees
* Slow logs record slow queries after they complete; they do not automatically cancel them.

## When to use this
* Production query auditing and latency SLA enforcement.

## When not to use this
* Setting slowlog thresholds to `0ms` in high-QPS production (will flood disk with logging I/O).

## What comes next
In Phase 61, we profile queries using the Search Profiling API.
