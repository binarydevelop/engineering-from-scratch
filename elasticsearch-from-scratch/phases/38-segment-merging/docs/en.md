# Lesson 38.1: Segment Merging

## Motto
"Many small immutable segments exhaust file descriptors and slow down queries; tiered merging consolidates them into fewer, larger segments."

## Problem
Every refresh generates a new immutable segment. After 10,000 writes and refreshes, a shard could have 10,000 individual segment files! Searching 10,000 files in parallel would exhaust file descriptors, saturate operating system threads, and ruin query performance.

## Prediction
What happens to documents marked as deleted in `.del` bitsets during a segment merge?

## Why this matters
Segment merging is Lucene's automatic garbage collection mechanism. It merges smaller segments of similar size into larger segments and physically purges deleted documents from disk.

## First principles
* **Tiered Merge Policy:** Segments of comparable sizes are grouped and merged in the background.
* Merging reads multiple segments, writes a single consolidated new segment, atomically swaps the segment pointer, and deletes the old segments.
* **Deleted Documents Purged:** Only during a merge are documents marked in `.del` files physically erased from disk!

## Mental model
```text
Before Merge:
  Segment _0 (100 docs, 20 deleted)
  Segment _1 (120 docs, 10 deleted)
  Segment _2 (90 docs,  30 deleted)
               │
      [ Background Merge ]
               ▼
After Merge:
  Segment _3 (250 docs, 0 deleted!)
  (Old segments _0, _1, _2 deleted from disk; disk space reclaimed!)
```

## Build it
See `code/merge_policy_sim.py` implementing tiered merging and deletion purging in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/38-segment-merging/experiments/run_experiment.sh
```

## Inspect it
Create multiple tiny segments by indexing documents with `?refresh=true`:
```bash
curl -s "http://localhost:9200/_cat/segments/merge_demo?v"
# Trigger forced merge down to 1 segment:
curl -X POST "http://localhost:9200/merge_demo/_forcemerge?max_num_segments=1"
curl -s "http://localhost:9200/_cat/segments/merge_demo?v"
```

## Measure it
Observe segment count drop to 1 and deleted document count drop to 0!

## Break it
Run `_forcemerge` on a heavily writing, active production index and observe massive disk I/O saturation.

## Recover it
Only run `_forcemerge` on static, read-only, or time-series indices that will never receive further writes.

## Modify it
Inspect merge throttling settings: `index.merge.scheduler.max_thread_count`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does deleting a document in Elasticsearch initially INCREASE disk usage?
2. Why should `_forcemerge` never be run on an index that is actively being written to?

## Guarantees
* Segment merging physically purges deleted documents and optimizes search index structures.

## Non-guarantees
* `_forcemerge` does not run instantly; it is an I/O-intensive rewrite of the entire index.

## When to use this
* Background merge runs automatically.
* Use `_forcemerge` explicitly on cold/frozen historical indices.

## When not to use this
* Never force-merge active hot write-heavy indices.

## What comes next
In Phase 39, we study how immutable segments handle Updates and Deletes.
