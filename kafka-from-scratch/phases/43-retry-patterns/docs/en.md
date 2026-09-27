# Lesson 43: Retry Patterns

## Motto
"Retrying in a tight in-process loop stalls the entire partition; retry topics preserve pipeline flow."

## Problem
A consumer fetches an order event and calls the inventory API.
The inventory API returns `503 Service Unavailable` due to a transient blip.
If the consumer:
* **Retries in-process in a tight loop:** It blocks the poll loop. If it takes longer than `max.poll.interval.ms`, the consumer is kicked out of the group (rebalance storm!). Meanwhile, thousands of healthy orders behind it are blocked.
* **Drops the message:** Data loss!
How do you implement delayed retries with exponential backoff without stalling the main partition?

## Prediction
What happens if you route failed events to a dedicated `orders-retry-1` topic instead of sleeping in the main consumer thread?

## Why this matters
**Non-blocking retry architectures are mandatory for high-throughput consumers.**
They allow healthy events to flow uninterrupted while failing events receive controlled, delayed retries.

## First principles
* **In-Process Retry:** Fine for quick retries (e.g. 2 attempts with 50ms backoff).
* **Retry Topic Pattern:** If in-process retries fail:
  1. Produce failed record to `topic.RETRY-1` with error headers and retry count.
  2. Commit offset on main topic! (Main pipeline continues at full speed!)
  3. A dedicated retry worker consumes from `topic.RETRY-1` with backoff delay.
  4. If it fails again $\implies$ Route to `topic.RETRY-2` or `topic.DLT` (Phase 44).

## Mental model
```text
Main Consumer Loop (NEVER BLOCKS!)
[ Ord 1 (OK) | Ord 2 (Fails!) | Ord 3 (OK) | Ord 4 (OK) ]
      │             │               │            │
      ▼             ▼               ▼            ▼
   Processed   Publish to        Processed   Processed
               orders.RETRY-1
               & Commit Offset!
                    │
                    ▼
Dedicated Retry Consumer (Processes with 10s delay, doesn't block main queue!)
```

## Build it
See [retry_topic_pattern.py](../code/retry_topic_pattern.py).
We implement the non-blocking retry topic pattern with exponential delay.

## Use Kafka
Execute the retry workflow and observe message progression across topics.

## Inspect it
Observe headers attached to retried records: `retry_count`, `original_topic`, `error_reason`.

## Measure it
Measure main partition throughput with and without retry topic offloading under 10% failure rates.

## Break it
Create an infinite retry loop without backoff limits; watch retry topics explode.

## Recover it
Enforce a strict maximum retry count (e.g. 3 attempts) before routing to a Dead-Letter Topic.

## Modify it
Implement exponential backoff calculation: $\text{delay} = \text{base} \times 2^{\text{retry\_count}}$.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an in-process `time.sleep(30)` inside a Kafka consumer poll loop trigger a group rebalance?
2. What happens to strict entity ordering when a failed record is moved to a retry topic?

## Guarantees
* Main consumer partition continues processing healthy events without being blocked by isolated failures.

## Non-guarantees
* Routing failed records to retry topics breaks strict FIFO ordering relative to newer records for that entity.

## When to use this
* In all high-throughput services with transient downstream dependencies (APIs, third-party services).

## When not to use this
* Workloads where strict per-entity FIFO order cannot be compromised under any circumstances.

## What comes next
In Phase 44, we study Dead-Letter Topics (DLT) for unrecoverable messages.
