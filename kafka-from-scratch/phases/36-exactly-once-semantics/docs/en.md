# Lesson 36: Exactly-Once Semantics

## Motto
"Exactly-once processing in Kafka does not mean magic exactly-once effects across the universe."

## Problem
Marketing materials often claim: *"Kafka provides Exactly-Once Semantics (EOS)!"*
Software engineers then build pipelines that read from Kafka and call an external payment gateway or insert into MySQL, and are shocked when duplicate payments still occur.
What does Kafka's "Exactly-Once" guarantee actually mean, and where does that guarantee stop?

## Prediction
Can Kafka transactions guarantee that a third-party non-transactional REST API will be called exactly once?

## Why this matters
Clarifying the precise technical boundary of EOS separates senior distributed systems architects from engineers who believe in magic.

## First principles
**The Reality of Kafka Exactly-Once Processing:**
* **Within Kafka Boundary:** Reading from Kafka, transforming in memory, and writing back to Kafka CAN be strictly exactly-once.
* **Outside Kafka Boundary:** Once an external system is touched (HTTP requests, external SQL databases, email gateways, file systems), Kafka's transactional coordinator has no jurisdiction!
* Achieving true end-to-end exactly-once with external systems requires **Idempotency** or the **Transactional Outbox Pattern** (Phase 60).

## Mental model
```text
The Kafka EOS Boundary:
┌────────────────────────────────────────────────────────┐
│ Kafka Input ──► Kafka Stream ──► Kafka Output Topic    │
│ [ EXACTLY-ONCE SEMANTICS GUARANTEED BY 2PC & KIP-98 ]  │
└────────────────────────────────────────────────────────┘
                           │
                           ▼ Outside the Boundary!
┌────────────────────────────────────────────────────────┐
│ External REST API / Stripe / SendGrid / Postgres       │
│ [ AT-LEAST-ONCE ONLY! Requires Idempotency Keys! ]     │
└────────────────────────────────────────────────────────┘
```

## Build it
See [eos_boundaries_lab.py](../code/eos_boundaries_lab.py).
We demonstrate the boundary where Kafka EOS ends and external side-effects require application-level idempotency.

## Use Kafka
Evaluate `read_committed` consumers reading transactional topics.

## Inspect it
Observe how committed and aborted transaction records are handled.

## Measure it
Measure throughput delta between EOS transactions and standard idempotent producer writes.

## Break it
Simulate an external API call inside a Kafka transaction; crash after the API call succeeds but before Kafka commit; observe the duplicate API call!

## Recover it
Add idempotency keys (`Idempotency-Key` HTTP header) to the external API call.

## Modify it
Document the failure matrix for hybrid Kafka + Database pipelines.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is the phrase "Exactly-Once Delivery" technically impossible over an unreliable network, while "Exactly-Once Processing" is achievable?
2. If your consumer writes to an external non-transactional database, how do you achieve effective exactly-once results?

## Guarantees
* Exactly-once state updates for Kafka-in to Kafka-out streaming topologies.

## Non-guarantees
* Does not guarantee exactly-once side effects on external services or databases.

## When to use this
* Pure Kafka streaming transformations (aggregations, joins, filtering).

## When not to use this
* Believing it eliminates the need for database idempotency.

## What comes next
In Phase 37, we explore Schema Evolution and see how event schemas evolve without breaking consumers.
