# Lesson 59: Change Data Capture (CDC)

## Motto
"The database transaction log was the original event stream; CDC unlocks it."

## Problem
A legacy monolithic database holds user and order records.
Your team wants to build a real-time Elasticsearch search index, a Redis cache, and a fraud detection pipeline.
If you use **periodic polling** (`SELECT * FROM orders WHERE updated_at > ?`):
* Frequent queries place massive read load on the production database.
* Hard deletes (`DELETE FROM orders`) are completely invisible to polling!
* Sub-second latency is impossible without saturating database CPU.
How do you capture database changes with zero polling overhead?

## Prediction
Where does a relational database (Postgres, MySQL) record row changes before committing them to data tables?

## Why this matters
**Change Data Capture (CDC)** turns relational databases into real-time Kafka event streams by reading the database's internal write-ahead log (Postgres WAL / MySQL binlog).

## First principles
* **Write-Ahead Log (WAL):** Every SQL `INSERT`, `UPDATE`, and `DELETE` is written sequentially to the database WAL for crash recovery.
* **CDC Engine (e.g. Debezium):** Connects as a replication client, parses WAL binary bytes, and streams change events directly to Kafka.
* **Zero Database Query Overhead:** Reads WAL files directly; does not execute SQL queries against tables.
* **Captures All Changes:** Captures deletes, old row state, new row state, and transaction commit timestamps.

## Mental model
```text
Application ──(SQL INSERT/UPDATE/DELETE)──► PostgreSQL
                                                 │
                                                 ▼ (Appends to WAL)
                                            Postgres WAL
                                                 │
                                                 ▼ (Streams binary changes)
                                         Debezium CDC Connector
                                                 │
                                                 ▼ (Produces events)
Kafka Topic: "postgres.public.orders" ◄──────────┘
      ├──► Real-Time Elasticsearch Indexer
      ├──► Redis Cache Invalidator
      └──► Fraud Scoring Service
```

## Build it
See [cdc_simulation.py](../code/cdc_simulation.py).
We simulate parsing database transaction log records into structured Kafka change events.

## Use Kafka
Observe the standard Debezium CDC event envelope (`before`, `after`, `op`, `ts_ms`).

## Inspect it
Compare CDC event structures for INSERT (`op="c"`), UPDATE (`op="u"`), and DELETE (`op="d"`).

## Measure it
Compare database CPU impact: periodic polling vs streaming CDC.

## Break it
Execute a hard SQL `DELETE` and observe how CDC captures the delete with a tombstone record.

## Recover it
Downstream consumers delete cached entries in response to delete events.

## Modify it
Map a PostgreSQL schema change to a Kafka topic event.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does CDC capture hard deletes that polling queries miss?
2. What is the danger of downstream consumers receiving CDC events out of order?

## Guarantees
* Every committed database mutation is captured in exact commit order.

## Non-guarantees
* Uncommitted (rolled back) SQL transactions are never published to Kafka.

## When to use this
* Database cache invalidation, search indexing, microservice data synchronization.

## When not to use this
* When business logic demands high-level semantic domain events (e.g. `OrderShipped`) rather than low-level row mutations (`status='shipped'`).

## What comes next
In Phase 60, we solve the classic dual-write problem using the Transactional Outbox Pattern.
