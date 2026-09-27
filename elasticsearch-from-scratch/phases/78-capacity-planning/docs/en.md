# Lesson 78.1: Capacity Planning

## Motto
"Capacity planning is applied math: calculate storage, shards, JVM heap, CPU cores, and network bandwidth."

## Problem
A company estimates hardware requirements by guessing: "Let's buy 3 huge servers". After launch, they run out of disk space in 3 weeks and spend weeks panicking during emergency data migrations.

## Prediction
Given 100 GB of raw JSON per day with 30-day retention and 1 replica, how many terabytes of physical storage and how many primary shards do you actually need?

## Why this matters
Search engine storage expands due to inverted index structures, doc values, and replicas. Calculating requirements in advance prevents costly under-provisioning or wasteful over-provisioning.

## First principles
The Sizing Formulas:
1. **Daily Raw Data:** $D_{	ext{raw}}$
2. **Index Overhead Factor:** Indexing adds inverted indexes, doc values, and BKD trees (typically $1.1	imes$ to $1.3	imes$ raw size).
3. **Total Disk Required:**
   $$	ext{Storage} = D_{	ext{raw}} 	imes 	ext{Overhead} 	imes (1 + 	ext{Replicas}) 	imes 	ext{Retention Days} 	imes 1.3 	ext{ (Watermark Buffer)}$$
4. **Target Shard Size:** 30 GB to 50 GB per shard.
   $$	ext{Primary Shards/Day} = rac{D_{	ext{raw}} 	imes 	ext{Overhead}}{	ext{Target Shard Size (e.g. 40 GB)}}$$

## Mental model
```text
Daily Raw Data: 100 GB
  ├── With Index Overhead (1.2x): 120 GB/day
  ├── With 1 Replica (2x): 240 GB/day
  ├── 30-day Retention: 7,200 GB (7.2 TB)
  └── With 30% Headroom Buffer (Watermarks): ~9.5 TB Physical Disk!
Shard Strategy: 120 GB / 40 GB = Exactly 3 Primary Shards per day!
```

## Build it
See `code/capacity_planner.py` calculating hardware, shard, and RAM budgets in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/78-capacity-planning/experiments/run_experiment.sh
```

## Inspect it
Calculate capacity for your organization's specific data profile.

## Measure it
Compare calculated theoretical storage against actual disk consumed by test indices via `_cat/indices?v&h=index,pri.store.size,store.size`.

## Break it
Under-estimate index expansion overhead ($0.5	imes$ instead of $1.2	imes$) and watch disk hit high watermark days ahead of schedule.

## Recover it
Incorporate safety headroom buffers ($1.3	imes$ margin for watermarks and segment merge spikes).

## Modify it
Calculate sizing for cold frozen storage using searchable snapshots.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an index on disk typically occupy more bytes than the original raw JSON payload?
2. Why must total disk capacity include a 30% buffer above calculated storage? (To prevent crossing disk watermarks and allow background segment merges).

## Guarantees
* Mathematical capacity models provide reliable upper bounds for hardware budgeting.

## Non-guarantees
* Estimates must be validated with representative real-world data and query loads.

## When to use this
* Architecture reviews, annual budget planning, and cloud deployment sizing.

## When not to use this
* Guessing without measuring.

## What comes next
In Phase 79, we systematically execute 7 Controlled Failure Scenarios.
