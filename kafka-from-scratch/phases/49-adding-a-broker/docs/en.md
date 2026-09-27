# Lesson 49: Adding a Broker

## Motto
"A new broker joins the cluster in seconds; data moves only when you tell it to."

## Problem
Your cluster is running low on capacity.
You boot up Broker 4 and register it with the KRaft quorum.
`kafka-cluster.sh` happily reports 4 active brokers!
The operations team celebrates, assuming the load has been redistributed.
One week later, Broker 1 runs out of disk and crashes.
Why did the new broker not absorb any existing data?

## Prediction
Does Apache Kafka automatically redistribute existing topic partitions to a newly joined broker?

## Why this matters
**Kafka does NOT automatically rebalance existing partitions when a new broker appears.**
New topics will place partitions on the new broker, but historical partitions stay exactly where they were until you explicitly trigger a partition reassignment (Phase 48).

## First principles
* **Broker Registration:** In KRaft, a new broker joins by connecting to the controller quorum and registering its `node.id`.
* **Static Partition Placement:** Partitions remain on their assigned replica brokers unless explicitly moved.
* **Rebalance Discipline:** After adding brokers, an engineer must run `kafka-reassign-partitions.sh` (or an automation tool like Cruise Control) to move partitions onto the new machine.

## Mental model
```text
Existing 3-Broker Cluster:
Broker 1: [ P0, P1, P2 ] (Disk 80%)
Broker 2: [ P0, P1, P2 ] (Disk 80%)
Broker 3: [ P0, P1, P2 ] (Disk 80%)

Add Broker 4:
Broker 4 joins cluster!
State:
Broker 1: [ P0, P1, P2 ] (Disk 80%)
Broker 2: [ P0, P1, P2 ] (Disk 80%)
Broker 3: [ P0, P1, P2 ] (Disk 80%)
Broker 4: [ EMPTY! 0 Partitions! 0 Disk Used! ] <--- DOES NOT AUTO-BALANCE!
```

## Build it
See [add_broker_simulation.py](../code/add_broker_simulation.py).
We inspect partition placement before and after a new broker is registered.

## Use Kafka
Observe cluster metadata after adding a node.

## Inspect it
List topic partitions and verify zero partitions have migrated automatically.

## Measure it
Measure disk usage across brokers to prove skew.

## Break it
Assume auto-rebalance happens; watch existing brokers continue to run out of disk while the new node sits completely idle.

## Recover it
Execute a partition reassignment to migrate a share of partitions to the new broker.

## Modify it
Create a *new* topic and verify that Kafka's default placement assignor does place new partitions on the new broker.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka avoid automatically shifting partitions when a new broker starts up? (Hint: what if a crashed broker is just rebooting?).
2. How does LinkedIn's Cruise Control project automate partition rebalancing in large fleets?

## Guarantees
* A newly registered broker is immediately available for new topic creation and metadata quorum.

## Non-guarantees
* Existing data will never move to the new broker automatically.

## When to use this
* Scaling cluster storage and compute horizontally.

## When not to use this
* Never consider a broker addition complete until existing partitions have been redistributed.

## What comes next
In Phase 50, we enter Module 10 and systematically execute controlled Broker Failure Scenarios.
