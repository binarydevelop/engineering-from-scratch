# Lesson 38: Event Design

## Motto
"An event should tell a complete story, not send consumers on a database scavenger hunt."

## Problem
What should the payload of an event actually look like?
Consider two extremes:
* **Bad Minimal Event (Event Notification):** `{"event": "ORDER_UPDATED", "order_id": 501}`
  * Every consumer must immediately make an HTTP call back to Order Service to ask *"What changed?"*, destroying decoupling and causing a thundering herd.
* **Bad Bloated Event:** A 15 MB payload containing entire historical customer records, tax forms, and attachments.
How do we balance self-contained richness with lean payload size?

## Prediction
What is the difference between Event Notification and Event-Carried State Transfer?

## Why this matters
Event schema design dictates how tightly coupled downstream systems remain to the original producing service.

## First principles
* **Event Notification:** Signals only that something happened (`order_id: 101`). Downstream services query upstream API for details. Low payload, high RPC coupling.
* **Event-Carried State Transfer (ECST):** Carries all relevant state attributes needed by downstream consumers (`order_id`, `items`, `total`, `tax`, `customer_address`). Eliminates RPC queries, achieves true temporal decoupling.
* **Essential Event Metadata:** Every event should contain:
  1. `event_id`: Unique UUID for idempotency.
  2. `event_type`: Domain action in past tense (`OrderCreated`, `PaymentCompleted`).
  3. `timestamp`: Event creation time (epoch ms).
  4. `entity_id`: Domain entity key.
  5. `schema_version`: For evolution.

## Mental model
```text
Event Notification (Causes Scavenger Hunt):
Producer ──► [ OrderUpdated(id=101) ] ──► Consumer ──(HTTP GET /orders/101)──► Producer DB!

Event-Carried State Transfer (Decoupled & Self-Contained):
Producer ──► [ OrderCreated { id: 101, items: [...], total: 99.50, addr: "..." } ]
                   │
                   ▼
             Consumer processes event directly without touching any other service!
```

## Build it
See [event_design_patterns.py](../code/event_design_patterns.py).
We contrast lean vs well-structured domain events.

## Use Kafka
Produce structured domain events with metadata envelopes.

## Inspect it
Observe how standard metadata envelopes make generic logging, routing, and tracing trivial.

## Measure it
Compare downstream query load under Event Notification vs Event-Carried State Transfer.

## Break it
Send an event with vague semantics (`{"action": "modify"}`) and observe how multiple consumers misinterpret it.

## Recover it
Use explicit past-tense domain events (`OrderAddressChanged`, `OrderItemAdded`).

## Modify it
Add correlation IDs (`trace_id`, `span_id`) to enable OpenTelemetry distributed tracing across Kafka.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why should event types always be named in the past tense (e.g. `OrderPlaced` rather than `PlaceOrder`)?
2. What are the trade-offs of Event-Carried State Transfer regarding data privacy and GDPR?

## Guarantees
* Rich events provide full temporal decoupling.

## Non-guarantees
* Event-Carried State Transfer does not reflect subsequent modifications unless new events are emitted.

## When to use this
* In all enterprise event-driven architectures.

## When not to use this
* Highly sensitive PII that cannot be persisted in unencrypted distributed logs.

## What comes next
In Phase 39, we examine Ordering Guarantees and learn where Kafka preserves order and where it does not.
