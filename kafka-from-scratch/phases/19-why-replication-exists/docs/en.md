# Lesson 19: Why Replication Exists

## Motto
"Hardware dies, cables get cut, and kernels panic; replication turns hardware mortality into system availability."

## Problem
In Phases 00 through 18, we operated a single Kafka broker.
What happens if the host machine's power supply explodes or the kernel panics?
* All topics hosted on that broker become immediately unreachable (total downtime).
* If the hard drive suffers a mechanical head crash, all data is permanently destroyed.
How do distributed systems survive physical machine destruction without data loss?

## Prediction
If you write a record to Machine A, how can Machine B serve read requests for that record if Machine A ceases to exist?

## Why this matters
Replication is the core difference between a single-machine database and a fault-tolerant distributed system.
Kafka organizes replication at the **partition** level.

## Mental model
```text
Single Broker (No Replication):
Broker 1 (DEAD) ──► Data Unavailable! Total Outage!

Replicated Cluster (Replication Factor = 3):
Broker 1 (LEADER - Writes & Reads)
  ├── Replicates over TCP ──► Broker 2 (FOLLOWER - Hot Standby)
  └── Replicates over TCP ──► Broker 3 (FOLLOWER - Hot Standby)

If Broker 1 dies, Broker 2 takes over in milliseconds! Zero data loss!
```

## Build it
See [replication_sim.py](../code/replication_sim.py).
We build a 3-node in-memory replication simulator where a Leader node pushes appends to 2 Follower nodes and elects a new leader upon crash.

## Use Kafka
Launch our 3-broker KRaft cluster:
```bash
make up-cluster
```

## Inspect it
Check running containers: `kafka-node-1`, `kafka-node-2`, `kafka-node-3`.

## Measure it
Measure time required to replicate an append across simulated nodes.

## Break it
Kill the simulated Leader node.

## Recover it
Promote Follower 1 to become the new Leader and continue serving appends.

## Modify it
Simulate network latency on Follower 2 and observe how replication lag accumulates.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka replicate partitions rather than entire brokers?
2. What is the storage cost of setting `replication.factor=3`?

## Guarantees
* With replication factor $N$, the cluster can survive $N-1$ broker failures without data loss (when properly configured).

## Non-guarantees
* Replication does not protect against bugs that write bad application data to all replicas simultaneously.

## When to use this
* Every production Kafka deployment must use `replication.factor >= 3`.

## When not to use this
* Ephemeral testing environments where data loss is inconsequential and resource consumption must be minimized.

## What comes next
In Phase 20, we explore Partition Leaders, Followers, and the In-Sync Replica (ISR) set in our 3-broker Kafka cluster.
