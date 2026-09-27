# Lesson 32: Backpressure

## Motto
"Kafka buffers work, but buffering is an emergency brake, not an infinite engine."

## Problem
In a push-based message broker, if workers cannot keep up, the broker pushes messages anyway, crashing the workers with out-of-memory errors.
In Kafka:
* Consumers **pull** data at their own pace via `poll()`.
* Therefore, consumers naturally control their own backpressure.
However, if $\text{Producer Rate} > \text{Consumer Rate}$ for hours or days:
* The buffer on disk grows without bound.
* When retention expires, data is lost.
How do we reason about buffer saturation and system capacity?

## Prediction
If incoming traffic is 10,000 msgs/s and consumer capacity is 8,000 msgs/s, how long until a 100GB disk partition fills up if each record is 1 KB?

## Why this matters
Backpressure reasoning connects software architecture to physics and queueing theory (**Little's Law**: $L = \lambda W$).

## First principles
* **Pull-Based Flow Control:** Because Kafka never pushes records, consumers cannot be overwhelmed by network bursts.
* **Storage as Buffer:** Unprocessed messages accumulate on disk.
* **Catch-up Math:** If a backlog of $B$ records builds up, and consumers process at rate $C$ while producers send at rate $P$:
  $$\text{Catch-up Time} = \frac{B}{C - P} \quad (\text{Requires } C > P)$$

## Mental model
```text
Producer Rate: 10,000/s ──► [ Kafka Disk Buffer ] ──► Consumer Rate: 2,000/s (Slow!)
                                  │
                                  ▼
                         Backlog Growing at +8,000 msgs/sec!
                         Disk consumption: +8 MB/sec
                         In 24 hours: 691 GB accumulated!
```

## Build it
See [backpressure_sim.py](../code/backpressure_sim.py).
We model queue accumulation and calculate exact catch-up times under different consumer scaling scenarios.

## Use Kafka
Run a high-speed producer against a rate-limited consumer and observe lag growth.

## Inspect it
Observe disk space consumption and consumer lag trajectory.

## Measure it
Measure time taken to drain the backlog once additional consumer instances join.

## Break it
Simulate $C < P$ indefinitely until topic retention is breached.

## Recover it
Scale consumer parallelism or optimize per-record database batching.

## Modify it
Calculate capacity requirements for an e-commerce flash sale event.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a pull model protect consumers from crashing due to memory exhaustion?
2. If your consumers are processing at maximum CPU capacity and lag is growing, what are your two architectural options?

## Guarantees
* Consumers only receive records when they explicitly request them via `poll()`.

## Non-guarantees
* Kafka's disk buffer does not protect you from business failure if catch-up rate never exceeds production rate.

## When to use this
* Capacity planning, peak load sizing, and autoscaling design.

## When not to use this
* Assuming that because Kafka buffers data, downstream capacity can be ignored.

## What comes next
In Phase 33, we study Producer Retries and observe how network timeouts create duplicate records.
