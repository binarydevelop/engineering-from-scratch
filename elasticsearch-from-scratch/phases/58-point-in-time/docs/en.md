# Lesson 58.1: Point in Time (PIT)

## Motto
"Point-in-Time freezes a lightweight search view of segments, preventing documents from shifting or disappearing during pagination."

## Problem
You are paginating through 50,000 results using `search_after`. While the user is browsing page 3, background updates and deletions insert new items and delete old ones. The document IDs shift, causing duplicate hits on page 4 or missed records entirely!

## Prediction
Can you freeze a consistent snapshot view of an index for search queries without copying the underlying data?

## Why this matters
The **Point in Time (PIT)** API (Elasticsearch 8.x) locks the set of Lucene segments participating in search. It guarantees consistent pagination even while the index is actively being modified.

## First principles
* **Lightweight Snapshot:** A PIT does not duplicate data; it simply retains open file handles to existing immutable segments, preventing the merge policy from deleting them until the PIT expires.
* Combines with `search_after` for consistent, reliable pagination.
* Must be closed explicitly (`DELETE /_pit`) when finished to release disk space.

## Mental model
```text
Live Index:
  Segments constantly refreshing, updating, and merging.

Point-in-Time (PIT Token):
  Retains references to [Segment _0, Segment _1] as they existed at Time T0.
  Subsequent updates do not alter this PIT search view!
```

## Build it
See `code/pit_simulation.py` simulating consistent read snapshots in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/58-point-in-time/experiments/run_experiment.sh
```

## Inspect it
Open a Point in Time:
```bash
PIT_ID=$(curl -s -X POST "http://localhost:9200/products_phase06/_pit?keep_alive=1m" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Opened PIT ID: $PIT_ID"
```
Query using the PIT:
```bash
curl -X POST http://localhost:9200/_search -H "Content-Type: application/json" -d "{
  "size": 5,
  "pit": { "id": "$PIT_ID", "keep_alive": "1m" }
}"
```
Close the PIT:
```bash
curl -X DELETE http://localhost:9200/_pit -H "Content-Type: application/json" -d "{"id": "$PIT_ID"}"
```

## Measure it
Verify query consistency: index new documents while paginating with PIT and confirm they do NOT appear in the PIT view.

## Break it
Open 1,000 PITs with `keep_alive: 24h` and never close them. Segment merging cannot reclaim deleted documents, causing disk usage to swell!

## Recover it
Delete lingering PITs via `DELETE /_pit` with `{"id": "_all"}`.

## Modify it
Combine PIT with `search_after` for zero-drift infinite scrolling.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does keeping a PIT open prevent disk space from being reclaimed after segment merges?
2. What is the difference between a Point-in-Time view and a database transaction?

## Guarantees
* A PIT view is completely frozen and consistent across multiple sequential search requests.

## Non-guarantees
* A PIT is not an ACID transaction (it is read-only).

## When to use this
* Large-scale data exports, audit pagination, and reliable cursor browsing.

## When not to use this
* Quick single-page queries.

## What comes next
In Phase 59, we compare Relevance Sorting with Field Sorting on Doc Values.
