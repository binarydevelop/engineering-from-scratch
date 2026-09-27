# Lesson 22: Leader Failure

## Motto
"A leader will die; a resilient system mourns for 50 milliseconds and continues."

## Problem
In Phase 20, we saw that all client writes flow to the partition Leader.
What happens when the machine hosting that leader suffers a catastrophic power outage?
* What happens to ongoing produce requests in-flight?
* Who elects the new leader?
* How long does failover take?
* Do producers and consumers crash, or do they recover transparently?

## Prediction
If a producer is sending continuous records and the partition leader broker is killed via `SIGKILL`, will the producer crash with an unhandled exception or retry automatically?

## Why this matters
Understanding leader failover mechanics demystifies client retry settings, metadata refresh intervals, and cluster availability SLAs.

## First principles
* **Leader Liveness:** KRaft controllers monitor broker heartbeats. If a leader broker disconnects, the KRaft active controller triggers partition leader election.
* **Election Candidates:** The controller selects a replacement leader exclusively from the partition's current **ISR**.
* **Leader Epoch:** The new leader increments the leader epoch integer, invalidating any lingering stale leader writes (fencing).
* **Client Metadata Refresh:** Clients receive `NOT_LEADER_OR_FOLLOWER` error, refresh cluster metadata, and redirect traffic to the new leader.

## Mental model
```text
T0: Broker 1 (Leader P0) ──► Producer writes normally
T1: kill -9 Broker 1      (Broker dies!)
T2: KRaft Controller detects Broker 1 offline
T3: Controller elects Broker 2 (from ISR) as NEW LEADER (Epoch = 2)
T4: Producer receives NOT_LEADER_OR_FOLLOWER, fetches fresh metadata
T5: Producer resumes sending to Broker 2 seamlessly!
```

## Build it
See [leader_failover_lab.py](../code/leader_failover_lab.py).
We run a continuous producer loop while killing the active leader container.

## Use Kafka
Execute leader failover against the 3-broker KRaft cluster.

## Inspect it
Observe consumer and producer recovery in console output.

## Measure it
Measure total downtime window (in milliseconds) from leader kill to successful write on the new leader.

## Break it
Kill the leader broker container using `docker stop kafka-node-1`.

## Recover it
Observe the client retry and reconnect to `kafka-node-2` without dropping records.

## Modify it
Restart the old leader container (`docker start kafka-node-1`) and observe it rejoin as a Follower.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What prevents a split-brain scenario where two brokers both believe they are the leader for Partition 0?
2. What role does `leader.epoch` play in log reconciliation?

## Guarantees
* Failover elects a replica that is guaranteed to have all committed records up to the High Watermark.

## Non-guarantees
* In-flight requests during the exact moment of leader death may fail if client retries are disabled (`retries=0`).

## When to use this
* Disaster recovery planning and high availability verification.

## When not to use this
* Avoid manual broker restarts during peak production traffic without graceful shutdown (`SIGTERM` allows clean leadership transfer).

## What comes next
In Phase 23, we explore `min.insync.replicas` and examine how it prevents data loss during cascading broker failures.
