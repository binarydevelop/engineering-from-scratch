# Lesson 01: Why Kafka Exists

## Motto
"Synchronous point-to-point connections turn downstream latency spikes into upstream system outages."

## Problem
In early web architectures, Service A (e.g. Checkout Service) synchronously called Service B (Inventory), Service C (Payment), Service D (Analytics), and Service E (Email Notifications).
As systems scale, this direct architecture collapses under:
1. **Tight Coupling:** Adding a new downstream consumer requires modifying and redeploying upstream producers.
2. **Cascading Failures:** If Service E stalls or crashes, Service A's HTTP worker threads block waiting for timeouts, exhausting thread pools and causing checkout outages.
3. **Inability to Replay:** If Analytics has a bug and needs last week's data recalculated, Service A cannot re-send millions of historical requests.

## Prediction
What happens to checkout response time when one of four downstream services encounters a 500ms database lock?

## Why this matters
Decoupling producers from consumers via an immutable log changes distributed system architecture from fragile request-reply webs into resilient, asynchronous event streams.

## Mental model
```text
The Fragile Web (Synchronous Direct Calls)
Checkout API ──(HTTP)──► Inventory (15ms)
             ├──(HTTP)──► Payment (50ms)
             ├──(HTTP)──► Analytics (400ms - SLOW!)  <-- Blocks Checkout!
             └──(HTTP)──► Email (Down! Timeout 3s)    <-- Fails Checkout!

The Decoupled Log (Kafka Architecture)
Checkout API ──(Append)──► [ Durable Log: orders ]
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
    Inventory Worker     Payment Worker        Analytics Worker
    (Reads at 15ms)      (Reads at 50ms)       (Reads at its own pace)
```

## Build it
See [direct_coupled_services.py](../code/direct_coupled_services.py) which simulates a synchronous checkout pipeline and measures total latency when downstream services degrade.

## Use Kafka
In Kafka, the producer performs a single fast append to the `orders` topic. Downstream workers independently pull events without impacting checkout latency.

## Inspect it
Observe how total latency in direct coupling equals the sum of all downstream latencies plus any timeouts.

## Measure it
Compare total transaction latency of synchronous calls vs. appending to an asynchronous event buffer.

## Break it
Inject a 3-second sleep into the Email notification service and watch the entire checkout process freeze.

## Recover it
Decouple the notification service using an intermediate queue or log.

## Modify it
Add a 5th downstream service (Fraud Scoring) to the synchronous pipeline and observe code changes required in the checkout service.

## Evidence
Record results in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does temporal decoupling allow services to undergo maintenance without dropping events?
2. Why is an append-only log superior to a simple in-memory queue for analytics fan-out?

## Guarantees
* Asynchronous log ingestion isolates producer latency from consumer processing time.

## Non-guarantees
* Asynchronous decoupling does not guarantee immediate consistency; downstream consumers will have eventual consistency.

## When to use this
* High-throughput event ingestion, multi-team decoupled microservices, audit logging, analytics fan-out.

## When not to use this
* Strict synchronous request-response workflows where the caller immediately requires an interactive query result (e.g. user authentication).

## What comes next
In Phase 02, we discard all third-party software and build an append-only log from scratch in pure Python.
