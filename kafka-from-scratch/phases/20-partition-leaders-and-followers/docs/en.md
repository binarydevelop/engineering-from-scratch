# Lesson 20: Partition Leaders and Followers

## Motto
"All writes go to the Leader; Followers are active copiers waiting to step up."

## Problem
In a multi-broker cluster, a topic has 3 partitions and a replication factor of 3.
That means there are $3 \times 3 = 9$ physical partition replicas spread across the brokers.
For any specific partition (say, Partition 0):
* Which broker accepts writes from producers?
* Which broker serves reads to consumers?
* What do the other brokers do with their copies?

## Prediction
If Broker 1 is the leader for Partition 0, what does Broker 2 do when a producer sends a record to Partition 0?

## Why this matters
Kafka uses a **single-leader replication model**. By default, all client writes and reads are handled exclusively by the designated partition leader. Followers run continuous background fetch loops to replicate data from the leader.

## First principles
* **Leader:** Handles client produce requests, assigns sequential offsets, and appends to disk.
* **Follower:** Acts like a specialized consumer; issues `FetchRequest` calls to the leader and writes fetched batches to its local disk.
* **Metadata Quorum:** KRaft controllers decide which broker is leader for each partition and distribute this routing table to all clients.

## Mental model
```text
Topic: "orders", Partition 0 (Replication Factor: 3)
┌────────────────────────────────────────────────────────┐
│ Broker 1: LEADER                                       │
│   ├── Receives Producer writes                         │
│   ├── Serves Consumer reads                            │
│   └── Exposes fetch interface to followers             │
└────────────────────────────────────────────────────────┘
          │                                  │
          ▼ (TCP Fetch Requests)             ▼ (TCP Fetch Requests)
┌───────────────────────┐          ┌───────────────────────┐
│ Broker 2: FOLLOWER    │          │ Broker 3: FOLLOWER    │
│ (Replicates silently) │          │ (Replicates silently) │
└───────────────────────┘          └───────────────────────┘
```

## Build it
See [cluster_metadata_inspector.py](../code/cluster_metadata_inspector.py).
We query the 3-broker cluster to map topic partitions to their respective leaders and replica sets.

## Use Kafka
Create a topic with replication factor 3 and inspect it:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --topic replicated-orders --partitions 3 --replication-factor 3
```

## Inspect it
Run `kafka-topics.sh --describe --topic replicated-orders`:
Observe fields: `Leader`, `Replicas`, `Isr`.

## Measure it
Inspect network I/O on follower brokers during heavy producer writes.

## Break it
Notice what happens if you attempt to create a topic with `--replication-factor 4` on a 3-broker cluster (`InvalidReplicationFactorException`).

## Recover it
Ensure replication factor never exceeds the count of active brokers.

## Modify it
Inspect leader distribution across brokers to verify even cluster balance.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka default to having consumers read from the Leader rather than Followers?
2. What feature in modern Kafka allows consumers to read from the closest replica (Fetch from Follower / KIP-392)?

## Guarantees
* Only the active partition leader accepts produce requests.

## Non-guarantees
* Having 3 replicas does not mean all 3 are synchronized at every microsecond.

## When to use this
* Standard topology for all production Kafka topics.

## When not to use this
* Replication factor 1 should only be used in temporary scratch/local testing.

## What comes next
In Phase 21, we examine the In-Sync Replicas (ISR) set and explore what happens when a replica lags behind.
