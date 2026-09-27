# Lesson 58: Event Sourcing Experiment

## Motto
"State is a snapshot of time; events are the fundamental truth."

## Problem
In standard CRUD architectures, databases overwrite state:
`UPDATE accounts SET balance = 50 WHERE id = 1;`
When an auditor asks: *"How did the balance reach $50? Who authorized it? What was the balance at 2:15 PM last Thursday?"*
The CRUD database cannot answer; historical state was destructively overwritten.
How does **Event Sourcing** solve this?

## Prediction
If you delete your application's current database state, can you recreate it with 100% fidelity by replaying the event log?

## Why this matters
In Event Sourcing, the append-only log of events is the **source of truth**. Current state is merely a derived projection (cache).

## First principles
* **Event Ledger:** Every state change is stored as an immutable domain event (`AccountOpened`, `MoneyDeposited`, `MoneyWithdrawn`).
* **State Reconstruction:** Current state is computed by folding (reducing) events from offset 0:
  $$\text{State}_T = \sum_{t=0}^T \text{Event}_t$$
* **Replay Resilience:** If the database becomes corrupted or a new read model is needed, delete the database and replay the log!

## Mental model
```text
Event Stream (Source of Truth):
[ AccountOpened($0) ──► Deposited($100) ──► Withdrawn($40) ──► Deposited($20) ]
                                 │
                                 ▼ (Projection Engine)
                       Current State: $80.00
                       (Delete state? Replay log to rebuild $80.00!)
```

## Build it
See [event_sourcing_lab.py](../code/event_sourcing_lab.py).
We build an event-sourced bank ledger, wipe the projection database, and rebuild state from the log.

## Use Kafka
Store domain events in an infinite-retention Kafka topic.

## Inspect it
Observe state evolution as each event is applied sequentially.

## Measure it
Measure replay speed across 10,000 historical events.

## Break it
Inject an invalid event into the stream (e.g. overdraft) and observe domain model rejection.

## Recover it
Implement snapshotting to avoid replaying millions of events from year 2020.

## Modify it
Add a new projection (e.g. `TotalDepositVolumeProjection`) and build it from the historical log.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Event Sourcing provide a tamper-evident financial audit trail?
2. What is the role of Snapshots in event-sourced architectures?

## Guarantees
* 100% deterministic state reconstruction from the event log.

## Non-guarantees
* Event sourcing does not make schema migrations trivial; old event schemas must be handled forever.

## When to use this
* Financial systems, medical records, supply chain tracking, git-like versioning.

## When not to use this
* Simple CRUD applications with high update rates and zero audit requirements.

## What comes next
In Phase 59, we study Change Data Capture (CDC) and see how database transactions become Kafka streams.
