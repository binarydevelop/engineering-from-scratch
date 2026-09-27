# Lesson 86.1: System Design With Elasticsearch

## Motto
"Architecting for scale: answer the 20 fundamental design questions across 8 real-world enterprise architectures."

## Problem
In a distributed systems design interview or production RFC, stating *"we will put it in Elasticsearch"* is unacceptable. You must justify every architectural parameter: shard count, replicas, mapping types, routing strategy, refresh interval, and disaster recovery.

## Prediction
Can you answer all 20 architectural questions for an E-Commerce Search, Log Analytics, or Autocomplete system?

## Why this matters
System design is the ultimate test of engineering maturity. This phase provides the comprehensive blueprint.

## First principles
The 20 Architectural Questions for Every Search System:
1. **Why Elasticsearch?** (What specific IR or analytical need justifies it?)
2. **What is the Source of Truth?** (Where is raw data permanently stored?)
3. **What is the synchronization mechanism?** (CDC, Kafka, Batch ETL?)
4. **What documents are indexed?** (Entity granularity?)
5. **What is the mapping schema?**
6. **Which fields are `text`?** (Tokenized for search?)
7. **Which fields are `keyword`?** (Exact filtering, sorting, aggregations?)
8. **What custom analyzers are needed?** (Stemming, stop words, shingles?)
9. **What is the query pattern?** (`bool` with `must` + `filter`?)
10. **What aggregations are computed?** (Terms, ranges, histograms?)
11. **What is the expected read QPS?**
12. **What is the peak indexing rate?** (Docs/sec?)
13. **What is the total data volume?** (GB/TB per day/year?)
14. **What is the retention period?**
15. **What is the sharding strategy?** (How many primary shards and why?)
16. **What is the replica strategy?** (High availability and read scaling?)
17. **What is the freshness requirement?** (`refresh_interval`: 1s vs 30s?)
18. **Is custom routing (`_routing`) appropriate?**
19. **What is the reindex / migration strategy?** (Aliases and versioned indices?)
20. **What failure modes exist and how does the system recover?**

## Mental model
```text
┌─────────────────────────────────────────────────────────────┐
│                 SYSTEM DESIGN SCENARIOS                     │
├─────────────────────────────────────────────────────────────┤
│ 1. E-Commerce Product Catalog Search                        │
│ 2. Centralized Microservice Log Analytics (APM)             │
│ 3. Multi-Tenant SaaS Knowledge Base                         │
│ 4. Sub-10ms Global Autocomplete Search Bar                  │
│ 5. Security Information & Event Management (SIEM)           │
│ 6. Real-Time Geospatial Store & Ride Finder                 │
│ 7. Job Portal & Resume Candidate Matching                   │
│ 8. Audit Event Trail with Cold Tiering                      │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/system_design_evaluator.py` validating architecture specifications against the 20 criteria in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/86-system-design-with-elasticsearch/experiments/run_experiment.sh
```

## Inspect it
Review the architectural blueprints for all 8 enterprise scenarios.

## Measure it
Evaluate sizing calculations for a 10,000 QPS e-commerce platform.

## Break it
Challenge the architecture: what happens when daily indexing volume triples?

## Recover it
Scale horizontally by adding data nodes and increasing primary shards via rollover.

## Modify it
Adapt the architecture for multi-region active-passive disaster recovery.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How do you defend your choice of shard count in a system design interview?
2. Why is decoupling the search view from the relational source of truth essential?

## Guarantees
* Rigorous answers to all 20 questions guarantee an operationally sound production search architecture.

## Non-guarantees
* Real production workloads require continuous monitoring and benchmark validation.

## When to use this
* Architecture proposals, tech design documents, and technical interviews.

## When not to use this
* Trivial prototype projects.

## What comes next
In Phase 87, we synthesize the Final Complete Mental Model: tracing an index write and search query end-to-end.
