# Lesson 24: KRaft and Cluster Metadata

## Motto
"Kafka now uses Kafka to manage Kafka."

## Problem
In early Kafka architectures (v0.8 to v2.8), Kafka relied on an external Apache ZooKeeper cluster to store topic metadata, partition leadership, and broker registrations.
This caused major architectural headaches:
1. **Dual System Overhead:** Operating two distinct distributed systems (ZooKeeper + Kafka) with separate configurations, security, and failure modes.
2. **Metadata Desync:** Controllers had to synchronize state from ZooKeeper into broker memory, creating multi-minute recovery delays during restarts.
3. **Partition Scalability Limits:** ZooKeeper struggled past 200,000 partitions.
How does modern Kafka manage its own cluster metadata natively?

## Prediction
Where is cluster metadata stored in a modern KRaft (Kafka Raft) cluster?

## Why this matters
KRaft (KIP-500) is the modern foundation of Apache Kafka. ZooKeeper is deprecated and removed. Understanding KRaft controllers and the `@metadata` partition is essential for modern cluster operations.

## First principles
* **KRaft Quorum:** Selected brokers act as KRaft Controllers. They run an event-driven Raft consensus algorithm.
* **The Metadata Log (`@metadata-0`):** All cluster metadata changes (topic creation, partition reassignment, broker registration) are appended as records to an internal Raft log.
* **Instantaneous Failover:** Because controllers replicate the metadata log continuously, when the active controller leader dies, a standby controller takes over in milliseconds.

## Mental model
```text
Legacy Architecture (ZooKeeper - DEPRECATED)
[ ZooKeeper Ensemble ] ◄── Watchers ──► [ Kafka Controller ] ──RPC──► [ Brokers ]
(Dual clusters, slow state loading, double operational complexity)

Modern Architecture: KRaft Mode (Apache Kafka 3.8.0)
┌────────────────────────────────────────────────────────┐
│ KRaft Controller Quorum (Raft Consensus)               │
│ Controller 1 (Leader) ◄── Raft ──► Controller 2 / 3    │
│   └── Replicates internal log: @metadata-0             │
└────────────────────────────────────────────────────────┘
                           │
       Direct Metadata Push (Sub-second convergence)
                           ▼
┌────────────────────────────────────────────────────────┐
│ Broker Data Plane (Partitions & Storage)               │
│ Broker 1               Broker 2               Broker 3 │
└────────────────────────────────────────────────────────┘
```

## Build it
See [kraft_metadata_explorer.py](../code/kraft_metadata_explorer.py).
We inspect the KRaft metadata state and controller identity.

## Use Kafka
Run the official KRaft metadata shell tool to inspect the cluster metadata hierarchy:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092
```

## Inspect it
Observe the metadata directory on disk: `/tmp/kraft-combined-logs/__cluster_metadata-0`.

## Measure it
Compare controller failover time in KRaft (< 100ms) vs legacy ZooKeeper (30+ seconds).

## Break it
Check how controllers handle quorum loss (e.g. killing 2 out of 3 controllers in a quorum).

## Recover it
Restore quorum nodes and observe leadership re-election.

## Modify it
Inspect the `meta.properties` file in Kafka's log directory and find the `cluster.id`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is KRaft described as "Kafka using Kafka to manage Kafka"?
2. What happens to Kafka cluster operations if the KRaft controller quorum loses majority?

## Guarantees
* All committed cluster metadata changes are strictly ordered and replicated via Raft.

## Non-guarantees
* KRaft does not replicate data plane topic messages; it replicates only control plane metadata.

## When to use this
* In all modern Kafka deployments (Kafka 3.0+).

## When not to use this
* ZooKeeper is legacy and should never be chosen for new architectures.

## What comes next
In Phase 25, we dig beneath the network protocol into Kafka's physical on-disk storage format: Segments and Indexes.
