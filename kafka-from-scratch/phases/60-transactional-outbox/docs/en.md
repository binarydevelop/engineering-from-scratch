# Lesson 60: Transactional Outbox

## Motto
"Never write to the database and Kafka in the same function without an Outbox."

## Problem
In a microservice, an order is placed:
```python
def checkout(order):
    db.insert_order(order)       # Step 1: Database write
    kafka.publish_event(order)   # Step 2: Kafka write
```
This is the notorious **Dual-Write Problem**:
* If Step 1 succeeds and Step 2 fails (network glitch, Kafka timeout) $\implies$ The database has the order, but Kafka never gets the event! Downstream fulfillment never runs!
* If Step 2 succeeds and Step 1 fails $\implies$ Kafka has an event for an order that does not exist in the database!
How can you write to a database and Kafka with atomic consistency without distributed two-phase commit transactions?

## Prediction
Can a database transaction span across a SQL database and an external Kafka cluster?

## Why this matters
**The Transactional Outbox Pattern is the most important reliability pattern in microservice architecture.**
It guarantees that an event is *always* published to Kafka if and only if the database transaction commits.

## First principles
* **Atomic Outbox Table:** Inside the *exact same* ACID database transaction as the business table, insert the event into an `outbox` table.
* **Transaction Invariant:** Either *both* the business row and the outbox row commit together, or *both* rollback.
* **Asynchronous Relay:** A separate background process (or CDC connector) reads the outbox table and publishes events to Kafka.
* **At-Least-Once Delivery:** The relay marks events as published after Kafka acks. Downstream consumers remain idempotent.

## Mental model
```text
Application (Checkout Service)
   │
   ▼ (BEGIN TRANSACTION)
┌────────────────────────────────────────────────────────┐
│ PostgreSQL Database                                    │
│   ├── INSERT INTO orders VALUES (...)                  │
│   └── INSERT INTO outbox_events VALUES (...)           │
└────────────────────────────────────────────────────────┘
   │
   ▼ (COMMIT TRANSACTION - 100% ATOMIC!)
   
Background Relay Poller (or Debezium CDC)
   │
   ▼ Reads unpublished rows from outbox_events
[ Publishes to Kafka Topic: orders ] ──► Kafka Ack!
   │
   ▼ Marks outbox row as published=TRUE
```

## Build it
See [transactional_outbox_lab.py](../code/transactional_outbox_lab.py).
We demonstrate dual-write failure followed by the Transactional Outbox solution.

## Use Kafka
Execute the outbox pattern against SQLite and Kafka.

## Inspect it
Query database tables to verify exact consistency between orders and outbox events.

## Measure it
Measure latency overhead of writing to the outbox table within the business transaction.

## Break it
Simulate Kafka broker downtime during checkout; observe that checkout completes successfully and the outbox buffers events safely until Kafka recovers!

## Recover it
Restore Kafka; watch the relay drain the outbox table to Kafka with zero data loss.

## Modify it
Add payload deduplication keys to the outbox event payload.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does writing to the `outbox` table within the business SQL transaction eliminate the dual-write risk?
2. Why does the Transactional Outbox guarantee At-Least-Once delivery to Kafka rather than Exactly-Once?

## Guarantees
* Guarantees zero data loss between database state and Kafka event publication.

## Non-guarantees
* The relay may republish an event if it crashes before marking it published; downstream consumers must be idempotent.

## When to use this
* Whenever a service must update its primary database AND emit an event to Kafka.

## When not to use this
* Pure streaming services that have no relational database.

## What comes next
In Phase 61, we explore Kafka Streams Concepts and stream processing topologies.
