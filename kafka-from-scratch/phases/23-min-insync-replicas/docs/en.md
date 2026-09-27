# Lesson 23: min.insync.replicas

## Motto
"acks=all without min.insync.replicas is an illusion of safety."

## Problem
You configure your producer with `acks=all`, believing your writes are replicated across multiple machines.
However, unknown to you, Broker 2 and Broker 3 died earlier today.
The topic's ISR shrank to just `[Broker 1]`.
When your producer sends with `acks=all`, the leader (Broker 1) checks the current ISR, sees that 100% of the ISR (which is just itself!) has written the record, and returns **SUCCESS**!
One minute later, Broker 1 crashes.
**All those records are permanently lost!**
How do we stop Kafka from accepting writes when the cluster has degraded below safe replication limits?

## Prediction
If a topic has `replication.factor=3` and `min.insync.replicas=2`, what happens to writes sent with `acks=all` if two brokers die?

## Why this matters
**The combination of `acks=all` AND `min.insync.replicas=2` is the industry gold standard for zero data loss.**
It instructs Kafka: "If at least 2 replicas cannot acknowledge this write, REFUSE IT rather than risking data loss."

## First principles
* **`min.insync.replicas`:** The minimum number of replicas in the ISR that must acknowledge a produce request when `acks=all`.
* If $\text{Current ISR Size} < \text{min.insync.replicas}$, the leader immediately rejects the write with:
  `NotEnoughReplicasException` or `NotEnoughReplicasAfterAppendException`.

## Mental model
```text
Configuration: replication.factor = 3, min.insync.replicas = 2, acks = all

Scenario 1: 3 Brokers Online (ISR = [1, 2, 3])
Writes succeed! (3 >= 2)

Scenario 2: Broker 3 Dies (ISR = [1, 2])
Writes succeed! (2 >= 2) - Cluster is degraded but safe!

Scenario 3: Broker 2 Also Dies (ISR = [1])
Writes REJECTED with NotEnoughReplicasException! (1 < 2)
Kafka chooses AVAILABILITY DOWNTIME over PERMANENT DATA LOSS!
```

## Build it
See [min_isr_lab.py](../code/min_isr_lab.py).
We test produce behavior when ISR size drops below `min.insync.replicas`.

## Use Kafka
Set `min.insync.replicas=2` on a topic:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-configs.sh   --bootstrap-server localhost:9092   --alter --entity-type topics --entity-name durable-topic   --add-config min.insync.replicas=2
```

## Inspect it
Check topic configuration using `kafka-configs.sh --describe`.

## Measure it
Observe producer exception metrics when replicas are killed.

## Break it
Stop 2 brokers in the cluster and send a write with `acks=all`. Observe the `NotEnoughReplicasException`.

## Recover it
Restart one broker; as soon as it rejoins the ISR, writes succeed again!

## Modify it
Test sending with `acks=1` while ISR size is below `min.insync.replicas` and observe that `acks=1` dangerously ignores `min.insync.replicas`!

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `acks=1` bypass `min.insync.replicas` enforcement?
2. In a 3-broker cluster, why should `min.insync.replicas` be set to 2 rather than 3? (Hint: what happens if 1 broker goes down for maintenance?).

## Guarantees
* When `acks=all`, Kafka guarantees records are acknowledged by at least `min.insync.replicas` before returning success.

## Non-guarantees
* `min.insync.replicas` provides zero protection if producers send with `acks=1` or `acks=0`.

## When to use this
* In all mission-critical, zero-data-loss topics.

## When not to use this
* Never set `min.insync.replicas = replication.factor` in production, because losing even a single node for rolling updates halts all cluster writes.

## What comes next
In Phase 24, we explore KRaft architecture and understand how Kafka coordinates cluster metadata without ZooKeeper.
