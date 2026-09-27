# Lesson 44: Dead-Letter Topics

## Motto
"A Dead-Letter Topic is not a trash bin; it is an active crime scene requiring investigation."

## Problem
A producer emits an unparseable malformed record:
`{"amount": "INVALID_STRING_NOT_A_FLOAT"}`
No amount of retrying will ever make this record valid.
If retries loop infinitely, resources are wasted.
If the consumer crashes, it enters an infinite crash loop (**Poison Pill**).
If the consumer silently ignores it, money or state changes are lost without trace.
Where do unprocessable messages go?

## Prediction
What metadata must accompany a record routed to a Dead-Letter Topic (DLT)?

## Why this matters
**The Dead-Letter Topic (DLT / DLQ) pattern quarantines poison pills, preserving cluster health while saving complete forensic evidence for human triage.**

## First principles
* **Poison Pill:** A record that reliably crashes consumer deserialization or business logic on every attempt.
* **Dead-Letter Routing:** After $N$ failed retries:
  1. Wrap the record with diagnostic metadata:
     * `original_topic`
     * `original_partition`
     * `original_offset`
     * `exception_message`
     * `stacktrace`
     * `failure_timestamp`
  2. Produce to `<topic>.DLT`.
  3. Commit the offset on the source topic!
* **Operational Rule:** **A DLT is an alert.** If messages are landing in a DLT, an engineer must inspect, fix the bug, and replay or discard intentionally.

## Mental model
```text
Source Topic ──► [ Consumer ] ──(Fails 3x)──► [ Dead-Letter Topic: orders.DLT ]
                      │                              │
                      ▼                              ▼
                 Commit Offset!               PagerDuty Alert!
                 (Pipeline Continues)         Engineer inspects payload & stacktrace
```

## Build it
See [dead_letter_queue_lab.py](../code/dead_letter_queue_lab.py).
We implement automatic DLT routing with error envelope encapsulation.

## Use Kafka
Deliver a malformed record to Kafka and watch the consumer quarantine it to `orders.DLT`.

## Inspect it
Read the DLT topic using `kafka-console-consumer.sh` and inspect the error metadata headers.

## Measure it
Monitor DLT record arrival rate as a primary production alarm.

## Break it
Simulate a bug where the DLT producer itself fails; observe fallback logging.

## Recover it
Fix the root cause and replay records from the DLT back into the main pipeline.

## Modify it
Build a CLI re-drive tool that reads messages from the DLT and re-publishes them to the main topic.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is routing a poison pill to a DLT safer than dropping it on the floor?
2. What dangerous antipattern occurs when teams configure a DLT but never set up monitoring or alerts on it?

## Guarantees
* Poison pill messages cannot crash consumer loops indefinitely.
* Unprocessable payloads are preserved for debugging.

## Non-guarantees
* DLT routing does not resolve the business failure; an order routed to DLT remains unfulfilled until remediated.

## When to use this
* In all production consumer applications.

## When not to use this
* Transient network timeouts (use Retry Topics with backoff first; only route to DLT after retries are exhausted).

## What comes next
In Phase 45, we examine Large Messages and learn why sending 50MB blobs over Kafka kills performance.
