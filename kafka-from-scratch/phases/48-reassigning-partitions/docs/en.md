# Lesson 48: Reassigning Partitions

## Motto
"Data does not move on its own; rebalancing a cluster requires deliberate, throttled partition migration."

## Problem
Your 3-broker cluster has been running for 6 months.
Brokers 1 and 2 are running at 85% disk capacity, while Broker 3 was recently added and sits at 10% disk capacity.
How do you safely move partition replicas from overloaded brokers to underutilized brokers without causing downtime or saturating the network?

## Prediction
What tool in Apache Kafka 3.8.0 coordinates moving partition replicas between brokers?

## Why this matters
Partition reassignment is the core mechanism for cluster rebalancing, expanding cluster capacity, and decommissioning failing hardware.

## First principles
* **`kafka-reassign-partitions.sh`:** The administrative utility that generates, executes, and verifies partition movement plans.
* **Movement Mechanics:**
  1. The new broker joins the partition replica set as a follower and begins fetching historical log segments.
  2. Once the new replica catches up and enters the ISR, leadership can transfer safely.
  3. The old broker drops the replica and deletes its local files.
* **Replication Throttling:** Moving gigabytes of data can saturate broker network cards. Kafka allows setting replication throttles (`--throttle`) to limit inter-broker bandwidth.

## Mental model
```text
Step 1: Partition 0 Replicas currently on [Broker 1, Broker 2]
Step 2: Add Broker 3 to replica set -> [Broker 1, Broker 2, Broker 3]
Step 3: Broker 3 fetches historical segments over network (Throttled at 50 MB/s)
Step 4: Broker 3 catches up and joins ISR!
Step 5: Drop Broker 1 from replica set -> [Broker 2, Broker 3]
Result: Partition successfully migrated with ZERO downtime!
```

## Build it
See [reassign_partitions_demo.py](../code/reassign_partitions_demo.py).
We generate a reassignment plan JSON and execute partition migration.

## Use Kafka
Execute partition reassignment using official CLI tooling.

## Inspect it
Monitor migration progress using `--verify`:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-reassign-partitions.sh   --bootstrap-server localhost:9092   --reassignment-json-file /tmp/reassign.json   --verify
```

## Measure it
Measure network replication throughput during migration.

## Break it
Execute reassignment without a network throttle during peak business traffic; observe producer latency spikes due to network congestion.

## Recover it
Apply dynamic bandwidth throttling (`--throttle 50000000` = 50 MB/s).

## Modify it
Generate reassignment plans using the `--generate` flag.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is applying a bandwidth throttle critical when executing partition reassignments in production?
2. What happens to client writes while a partition reassignment is actively copying historical segments?

## Guarantees
* Zero-downtime online migration; partition remains fully available for reads and writes throughout.

## Non-guarantees
* Reassignment does not complete instantly; multi-terabyte partitions require hours to replicate.

## When to use this
* Adding new brokers to an existing cluster, decommissioning hardware, resolving broker disk skew.

## When not to use this
* Avoid moving massive partitions during peak traffic windows if network bandwidth is limited.

## What comes next
In Phase 49, we explore Adding a Broker and debunk the myth that Kafka automatically rebalances data on its own.
