# Lesson 52: Producer Failure Scenarios

## Motto
"A producer's configuration is not a preference; it is a mathematical guarantee."

## Problem
What can go wrong when a producer calls `send()`?
* Broker is unreachable (`NetworkException`).
* Topic does not exist and auto-creation is disabled (`UnknownTopicOrPartitionException`).
* Record exceeds 1 MB (`RecordTooLargeException`).
* Topic ISR is below minimum (`NotEnoughReplicasException`).
* Producer memory buffer is full (`BufferExhaustedException`).
Which errors are transient and retriable? Which errors are fatal?

## Prediction
Will the Kafka client automatically retry a `RecordTooLargeException`?

## Why this matters
Distinguishing **Retriable Errors** from **Fatal Errors** determines whether your application can self-heal or must alert immediately.

## First principles
* **Retriable Errors:** Caused by transient conditions (leader election, temporary network loss). The client library automatically retries if `retries > 0`.
  * Examples: `NotLeaderOrFollowerException`, `NetworkException`, `LeaderNotAvailableException`.
* **Fatal Non-Retriable Errors:** Fundamental structural flaws. Retrying will never succeed and will waste CPU.
  * Examples: `RecordTooLargeException`, `SerializationException`, `TopicAuthorizationException`.

## Mental model
```text
producer.send(record)
        │
        ▼ (Error received from broker)
Is error Retriable?
   ├── YES ──► Sleep retry_backoff_ms ──► RETRY (Up to retries limit)
   └── NO  ──► FATAL! Raise exception to application immediately!
```

## Build it
See [chaos_producer_failure.py](../code/chaos_producer_failure.py).
We categorize Kafka exceptions and test application handling.

## Use Kafka
Trigger producer errors intentionally and observe client logging.

## Inspect it
Observe producer callback futures under error conditions.

## Measure it
Measure time taken for a producer to exhaust retries during extended broker outages.

## Break it
Send a record to a non-existent topic with auto-create disabled.

## Recover it
Create the topic or handle the exception cleanly.

## Modify it
Set `max.block.ms=2000` to prevent producer threads from hanging forever when broker buffers are full.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must `max.block.ms` be configured on producers in high-throughput web APIs?
2. What happens if a producer's buffer memory fills up?

## Guarantees
* Retriable errors are retried automatically by the client library up to configured limits.

## Non-guarantees
* The producer cannot automatically recover from fatal schema or authorization failures.

## When to use this
* In all producer error handling and alerting architecture.

## When not to use this
* Swallowing producer exceptions silently with empty `except:` blocks.

## What comes next
In Phase 53, we cover Kafka Security Basics: TLS, SASL, and ACLs.
