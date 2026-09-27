# Lesson 84.1: Elasticsearch Anti-Patterns

## Motto
"Learn from the graveyard of search outages: 15 fatal architectural blunders and their concrete mitigations."

## Problem
Most Elasticsearch outages are self-inflicted by well-intentioned engineers applying patterns from relational databases or message queues to a search engine.

## Prediction
Can you identify at least 5 common configuration or architectural mistakes that bring down production search clusters?

## Why this matters
Mastery is not just knowing how to build; it is knowing what NEVER to build.

## First principles
The 15 Fatal Search Anti-Patterns:
1. **Primary OLTP Source of Truth:** Using ES as the sole transactional database without ACID backups.
2. **Oversharding:** 5,000 tiny 50MB shards exhausting JVM heap metadata.
3. **Uncontrolled Dynamic Mappings:** Dynamic user keys triggering mapping explosions.
4. **Leading Wildcard Queries:** `*search*` forcing full dictionary scans.
5. **Deep Pagination with `from + size`:** Requesting page 5,000 and crashing coordinator memory.
6. **Massive Documents:** Indexing 50MB PDF blobs into JSON `_source`.
7. **Mapping Analyzed Text as IDs:** Querying tokenized UUIDs with `match` instead of exact `keyword`.
8. **High-Cardinality Deep Aggregations:** Terms aggregations on millions of unique values.
9. **Replicas Treated as Backups:** Zero snapshots taken because "we have replicas".
10. **Giant Single Bulk Requests:** Sending 1GB bulk payloads tripping circuit breakers.
11. **One Hot Shard:** Skewed custom routing pinning 1 node at 100% CPU.
12. **Excessive Refresh Frequency:** Calling `?refresh=true` on every write in a tight loop.
13. **Monolithic Multi-Year Log Index:** 20TB in a single index instead of daily rolling indices.
14. **Allocating 100% RAM to JVM Heap:** Depriving the OS page cache of memory for Lucene segments.
15. **Public Cluster Exposure:** Running port 9200 without authentication on the public internet.

## Mental model
```text
           THE RESILIENT SEARCH ARCHITECTURE
┌─────────────────────────────────────────────────────────────┐
│ 1. Dedicated Master Nodes (split-brain immune)              │
│ 2. Shards sized 20GB - 50GB (No oversharding)               │
│ 3. Explicit Mappings with .keyword multi-fields             │
│ 4. Search API Gateway with query validation                 │
│ 5. Daily Snapshots to S3/GCS                                │
│ 6. Memory: 50% JVM Heap (max 31GB), 50% OS Page Cache       │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/antipattern_auditor.py` auditing cluster configurations against the 15 anti-patterns in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/84-elasticsearch-anti-patterns/experiments/run_experiment.sh
```

## Inspect it
Review the audit checklist against your lab cluster.

## Measure it
Assess risk levels across indexing and search configurations.

## Break it
Pick any anti-pattern from the list and test its failure mode in our test environment.

## Recover it
Apply the corresponding documented remediation.

## Modify it
Add custom organizational linting rules to the auditor script.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is treating replica shards as backups a fatal assumption?
2. Why is mapping an order UUID as `text` dangerous?

## Guarantees
* Eliminating these 15 anti-patterns guarantees rock-solid cluster stability.

## Non-guarantees
* Hardware failures (disk corruption, power outages) still require automated failover and snapshot restores.

## When to use this
* Architecture reviews, incident post-mortems, and pre-production go-live checklists.

## When not to use this
* Ignoring operational warnings.

## What comes next
In Phase 85, we establish clear boundaries: When Elasticsearch Is the WRONG Tool.
