# Lesson 18: Producer Acknowledgments

## Motto
"acks=all is not a magic shield; it is only as strong as your replica count and min.insync.replicas."

## Problem
When a producer writes data to Kafka, when should the broker reply that the write succeeded?
* If the broker replies immediately before touching disk, writes are blazing fast, but data vanishes if the broker power fails.
* If the broker waits for disk sync and full cluster quorum replication, data is bulletproof, but latency increases.
How do we control this safety vs speed knob?

## Prediction
What happens to producer latency and data loss risk when switching from `acks=0` to `acks=all`?

## Why this matters
Producer acknowledgments (`acks`) define the durability contract. Misunderstanding `acks` leads either to silent data loss during failovers or unneeded latency bottlenecks.

## First principles
* **`acks=0` (Fire-and-Forget):** Producer considers write complete the instant bytes hit the local OS network socket. Zero broker confirmation.
* **`acks=1` (Leader Local):** Leader writes to its local log/page cache and immediately acknowledges. If leader crashes before replicas fetch, records are lost.
* **`acks=-1` / `acks=all` (Quorum):** Leader waits until all current In-Sync Replicas (ISR) have appended the batch to their logs before replying.

## Mental model
```text
acks=0:   Producer ──► [Socket] ──► (Assumes success immediately! No Ack!)
acks=1:   Producer ──► Leader Log Appended ──► Ack! (Followers haven't replicated yet!)
acks=all: Producer ──► Leader Log ──► Follower 1 ──► Follower 2 ──► Ack! (Quorum Replicated!)
```

## Build it
See [acks_durability_lab.py](../code/acks_durability_lab.py).
We test produce latency across `acks=0`, `acks=1`, and `acks=all`.

## Use Kafka
Execute producer scripts specifying different acknowledgment levels.

## Inspect it
Observe round-trip produce latency metrics.

## Measure it
Compare write latency across all 3 levels.

## Break it
Under `acks=1`, produce records and kill the single broker container; verify un-replicated records are at risk.

## Recover it
Configure `acks=all` combined with a multi-broker cluster (Phase 20).

## Modify it
Change producer timeout (`request.timeout.ms`) to observe client retry behavior when acknowledgments stall.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `acks=all` on a topic with `replication.factor=1` provide NO additional durability over `acks=1`?
2. If `acks=all` is configured, what happens if network latency between leader and follower spikes?

## Guarantees
* `acks=all` guarantees that all currently active In-Sync Replicas hold the record before acknowledgment.

## Non-guarantees
* `acks=all` does NOT guarantee zero data loss if `min.insync.replicas=1` and all replicas die.

## When to use this
* `acks=all`: Financial ledgers, orders, user credentials, audits.
* `acks=1`: General telemetry, user activity feeds.
* `acks=0`: Loss-tolerant metrics where throughput trumps everything.

## What comes next
In Phase 19, we explore why replication exists and how multi-broker clusters survive physical hardware failure.
