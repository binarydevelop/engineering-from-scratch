# Lesson 39.1: Updates and Deletes

## Motto
"In an immutable segment architecture, there is no in-place update: an update is a delete plus an insert."

## Problem
In a relational database, `UPDATE users SET status = 'active' WHERE id = 1` overwrites bytes inside a disk page in-place. Because Lucene segments are strictly immutable, how can Elasticsearch update a document?

## Prediction
If you issue 100 consecutive updates to the same document ID, how many total Lucene documents and deleted markers will exist before a merge occurs?

## Why this matters
Understanding that an update is a **Delete + Insert** explains why update-heavy workloads generate high write amplification and accumulate deleted document markers.

## First principles
When an update request arrives:
1. Lucene looks up the existing document via its `_id`.
2. Marks the existing document ID as deleted in the `.del` bitset of its segment.
3. Indexes the new updated document version as a brand-new document into the in-memory indexing buffer.
4. Increments the `_version` counter in metadata.

## Mental model
```text
Document ID: 42 (Version 1 in Segment _0)
                  │
   [ Update arrives: price = 99.99 ]
                  │
   ├── Mark Version 1 in Segment _0 as DELETED in _0.del
   └── Index Version 2 as a new doc in Segment _1!
```

## Build it
See `code/update_delete_sim.py` demonstrating versioning and soft-deletes in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/39-updates-and-deletes/experiments/run_experiment.sh
```

## Inspect it
Update a document multiple times and inspect `_cat/indices` and `_cat/segments`:
```bash
curl -X PUT http://localhost:9200/update_demo/_doc/1 -H "Content-Type: application/json" -d '{"v": 1}'
curl -X POST http://localhost:9200/update_demo/_update/1 -H "Content-Type: application/json" -d '{"doc": {"v": 2}}'
curl -X POST http://localhost:9200/update_demo/_update/1 -H "Content-Type: application/json" -d '{"doc": {"v": 3}}'
curl -s "http://localhost:9200/_cat/indices/update_demo?v&h=docs.count,docs.deleted"
```
Notice: `docs.count: 1`, `docs.deleted: 2`!

## Measure it
Compare write throughput of pure inserts vs repeated updates on the same document IDs.

## Break it
Execute 50,000 updates on a single document in a tight loop and observe deleted doc count and disk bloat.

## Recover it
Trigger `_forcemerge` or wait for background merge policy to purge stale versions.

## Modify it
Use optimistic concurrency control: pass `if_seq_no` and `if_primary_term` to prevent lost update race conditions.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an update in Elasticsearch require both a read and a write operation?
2. How does optimistic concurrency control (`if_seq_no`) protect against concurrent update overwrites?

## Guarantees
* Elasticsearch guarantees that only the newest version of a document is returned by search.

## Non-guarantees
* Updates do NOT modify disk blocks in-place.

## When to use this
* Standard entity updates and document modifications.

## When not to use this
* High-frequency counters incremented 10,000 times a second (use Redis for atomic in-memory counters).

## What comes next
In Phase 40, we contrast 1 doc/request indexing with the Bulk API.
