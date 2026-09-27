# Lesson 65: Capstone 3 — Production-Like Kafka Lab

## Motto
"Theory ends here; run the full cluster, inject chaos, and observe graceful recovery."

## Problem
In this capstone, you will operate a full **3-broker KRaft cluster** hosting multiple partitioned, replicated topics:
* Topics: `orders` (3 partitions, RF=3), `payments` (3 partitions, RF=3), `notifications` (3 partitions, RF=3).
* High durability: `acks=all`, `min.insync.replicas=2`, `enable.idempotence=true`.
* Continuous producer pushing realistic e-commerce traffic.
* Multiple consumer groups actively processing records.
* Injected chaos:
  1. Kill a follower broker -> Verify writes continue without error.
  2. Kill the leader broker -> Verify leader election from ISR in <100ms and zero lost writes.
  3. Inject poison pill -> Verify quarantine to DLT.
  4. Measure end-to-end throughput, latency, and lag throughout the storm!

## Prediction
Will the continuous producer experience an unhandled crash when the leader broker is killed with `SIGKILL`?

## Why this matters
Proving that your system survives simultaneous broker failure, consumer death, and poisoned payloads validates complete mastery of Apache Kafka.

## Mental model
```text
3-Broker KRaft Cluster Lab
Broker 1 (9092) ◄──► Broker 2 (9094) ◄──► Broker 3 (9096)
       │                    │                    │
[ P0 Leader ]        [ P1 Leader ]        [ P2 Leader ]
       │                    │                    │
Producer (acks=all) ──► Replicated across all 3 nodes!
       │
CHAOS INJECTION:
docker stop kafka-node-1 (LEADER DIES!)
       │
KRaft Controller elects Broker 2 as NEW LEADER in 50ms!
Producer retries transparently -> ZERO DATA LOSS!
```

## Build it
See [production_lab_runner.py](../code/production_lab_runner.py).
We execute the multi-broker chaos verification pipeline.

## Use Kafka
Launch the 3-broker cluster:
```bash
make up-cluster
```

## Inspect it
Observe topic metadata across all 3 nodes:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --describe --topic replicated-orders
```

## Measure it
Capture throughput, p99 latency, and failover interruption time.

## Break it
Run the automated chaos suite: kill leader, kill follower, inject lag.

## Recover it
Restart stopped containers; watch ISR recover to `[1, 2, 3]`.

## Modify it
Add bandwidth throttles to observe degraded follower synchronization.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why did the producer survive the leader crash with zero exceptions thrown to the application?
2. What would have happened if `min.insync.replicas` had been set to 3 instead of 2 when Broker 1 died?

## Guarantees
* Complete, verified high-availability and fault tolerance under multi-node failure.

## Non-guarantees
* Does not survive simultaneous destruction of all 3 brokers.

## When to use this
* As the final practical operational benchmark of this course.

## When not to use this
* Never skip chaos validation before taking a streaming system to production.

## What comes next
In Phase 66, we transition to System Design: interrogating real-world architectures with the 20-Question Kafka Framework.
