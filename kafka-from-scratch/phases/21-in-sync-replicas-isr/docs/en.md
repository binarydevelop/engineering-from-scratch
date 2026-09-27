# Lesson 21: In-Sync Replicas (ISR)

## Motto
"A replica that exists on disk is not the same as a replica that is caught up."

## Problem
A topic has replication factor 3 on Brokers 1, 2, and 3.
Broker 3 experiences a 30-second garbage collection pause or network packet loss.
While Broker 3 is frozen, the leader (Broker 1) appends 50,000 new records.
Can Broker 3 still be trusted to participate in quorum acks (`acks=all`)?
If Broker 1 crashes, should Broker 3 be allowed to become the new leader?
How does Kafka determine which replicas are healthy enough to be considered **In-Sync**?

## Prediction
If a follower fails to fetch records for longer than `replica.lag.time.max.ms`, what happens to the topic's ISR list?

## Why this matters
**The ISR is the foundation of Kafka's durability and leader election guarantees.**
Only replicas inside the ISR are eligible to be elected leader during standard failovers.

## First principles
* **In-Sync Replicas (ISR):** The subset of replicas actively keeping up with the partition leader.
* **`replica.lag.time.max.ms` (default: 30,000ms):** If a follower does not send a fetch request within this window, the leader removes it from the ISR.
* **High Watermark (HW):** The highest offset replicated to ALL current ISR members. Consumers can only read up to the High Watermark!

## Mental model
```text
Leader Log:      [ 0 | 1 | 2 | 3 | 4 | 5 ]  (LEO = 6)
Follower 2 Log:  [ 0 | 1 | 2 | 3 | 4 | 5 ]  (In-Sync! Lag = 0)
Follower 3 Log:  [ 0 | 1 | 2 ]              (Lagging behind! Stalled!)

ISR: [ Broker 1, Broker 2 ]  <-- Broker 3 DROPPED from ISR!
High Watermark = 5           <-- Replicated to all members of current ISR
```

## Build it
See [isr_monitor.py](../code/isr_monitor.py).
We monitor ISR changes dynamically.

## Use Kafka
Inspect the ISR list:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --describe --topic replicated-orders
```

## Inspect it
Observe the `Isr: 1,2,3` field in output.

## Measure it
Measure how quickly a stopped follower is dropped from the ISR.

## Break it
Pause or stop `kafka-node-3`:
```bash
docker stop kafka-node-3
```
Watch the ISR shrink from `[1, 2, 3]` to `[1, 2]`.

## Recover it
Restart `kafka-node-3`:
```bash
docker start kafka-node-3
```
Observe the follower fetch missed records, catch up, and rejoin the ISR (`[1, 2, 3]`).

## Modify it
Lower `replica.lag.time.max.ms` to 5000ms and observe faster shrink detection.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are consumers prohibited from reading beyond the High Watermark?
2. What would happen if a replica outside the ISR was elected leader (unclean leader election)?

## Guarantees
* Any member of the ISR holds all committed messages up to the High Watermark.

## Non-guarantees
* Replicas are not guaranteed to be in the ISR if network connectivity or GC pauses exceed timeout thresholds.

## When to use this
* In all durability reasoning and under-replicated partition monitoring.

## When not to use this
* Do not set `replica.lag.time.max.ms` too aggressively low, or minor GC pauses will trigger constant ISR flapping.

## What comes next
In Phase 22, we kill the partition leader broker and observe Leader Failure and Failover in action.
