# Lesson 66.1: Index Lifecycle Concepts

## Motto
"Data ages: Hot nodes write, Warm nodes query, Cold nodes freeze, and Delete purges."

## Problem
In a logging cluster generating 500GB/day, storing 1 year of logs on ultra-fast NVMe SSDs would cost tens of thousands of dollars per month. Yet 95% of all searches only target the last 7 days!

## Prediction
Can you automatically move older indices from expensive fast SSD nodes to cheaper dense storage nodes as they age?

## Why this matters
**Index Lifecycle Management (ILM)** automates data tiering, rollover, shrinking, force-merging, and deletion based on index age and size.

## First principles
The Four Data Tiers:
1. **Hot Tier:** Active ingestion. High write speed, NVMe SSDs, fast CPUs.
2. **Warm Tier:** Read-only queries. Lower ingestion, force-merged segments to 1 segment, cheaper SSDs.
3. **Cold Tier:** Infrequent queries. Fully frozen segments, low-cost HDDs or object store.
4. **Delete Phase:** Automatically drops indices after retention period expires (e.g. 90 days).

## Mental model
```text
Day 1 (Hot Tier): Active writes, 1s refresh, fast SSDs
       │ Rollover after 50 GB or 1 day
       ▼
Day 7 (Warm Tier): Read-only, force-merged to 1 segment, replicas=1
       │ Migrate after 30 days
       ▼
Day 30 (Cold Tier): Frozen segments, zero write buffers, dense storage
       │ Purge after 90 days
       ▼
Day 90 (Delete Phase): Index deleted. Storage reclaimed.
```

## Build it
See `code/ilm_state_machine.py` simulating lifecycle phase transitions in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/66-index-lifecycle-concepts/experiments/run_experiment.sh
```

## Inspect it
Create an ILM policy:
```bash
curl -X PUT http://localhost:9200/_ilm/policy/logs_policy -H "Content-Type: application/json" -d '{
  "policy": {
    "phases": {
      "hot": { "actions": { "rollover": { "max_primary_shard_size": "50gb", "max_age": "7d" } } },
      "delete": { "min_age": "30d", "actions": { "delete": {} } }
    }
  }
}'
```

## Measure it
Inspect policy status: `curl -s http://localhost:9200/_ilm/policy/logs_policy?pretty`.

## Break it
Configure rollover with an alias that does not have a write index designated (`is_write_index: true`).

## Recover it
Mark the active index in the alias: `{"actions": [{"add": {"index": "logs-000001", "alias": "logs", "is_write_index": true}}]}`.

## Modify it
Add a warm phase action that force-merges to 1 segment: `{"actions": {"forcemerge": {"max_num_segments": 1}}}`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does force-merging an index to 1 segment in the Warm phase reduce memory and search cost?
2. What is the role of an Index Alias in automated Rollover?

## Guarantees
* ILM enforces storage retention policies automatically in the background.

## Non-guarantees
* ILM will not delete data if the policy is misconfigured or cluster disk is full.

## When to use this
* Time-series indices, application logs, metrics, audit records, and security events.

## When not to use this
* Static entity catalogs (e.g. product catalog updated by daily batch).

## What comes next
In Phase 67, we build a complete Time-Series / Logging Workload.
