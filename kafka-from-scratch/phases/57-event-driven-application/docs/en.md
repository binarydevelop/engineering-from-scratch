# Lesson 57: Capstone 2 — Event-Driven Application

## Motto
"True resilience means one service can be on fire while the rest of the company processes transactions as normal."

## Problem
Build a realistic multi-service event-driven e-commerce architecture:
1. **Order API:** Publishes `OrderPlaced` events to Kafka `orders` topic.
2. **Payment Worker:** Dedicated consumer group. Idempotent charging. Routes failures to Retry Topic.
3. **Email Worker:** Dedicated consumer group. Sends customer receipts.
4. **Analytics Worker:** Dedicated consumer group. Aggregates revenue.
5. **Lag Monitor:** Background thread calculating consumer lag in real time.
6. **Failure Injection:** Kill the Payment service and prove the Order API continues accepting orders and Email/Analytics continue processing uninterrupted!

## Prediction
What happens to Order API response time when the downstream Email service is down?

## Why this matters
This capstone integrates every operational, architectural, and resilience concept taught in the first 55 phases into a cohesive system.

## Mental model
```text
Order API ──(Publish)──► [ Topic: orders ]
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   Payment Worker        Email Worker      Analytics Worker
   (Group: payments)     (Group: emails)   (Group: analytics)
   ├── Idempotent DB     └── Sends email   └── Computes revenue
   └── On Error:
       Retry Topic ──► Dead-Letter Topic
```

## Build it
See [event_driven_app.py](../code/event_driven_app.py).

## Use Kafka
Run the multi-threaded application against our Kafka broker.

## Inspect it
Observe independent consumer group offsets and lag metrics.

## Measure it
Measure system throughput and latency under 100 concurrent orders.

## Break it
Simulate payment gateway failure and observe events routing to the retry topic and DLT.

## Recover it
Demonstrate how the payment worker catches up after recovering from an outage.

## Modify it
Add a new `fraud-detection` worker without modifying a single line of the Order API code!

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does the event-driven architecture prevent payment gateway outages from impacting checkout availability?
2. What role does the idempotency key play when replaying orders from the Dead-Letter Queue?

## Guarantees
* Complete decoupling of business services across failure domains.

## Non-guarantees
* Eventual consistency: email receipts may arrive a few seconds after order completion.

## When to use this
* In all modern decoupled microservice systems.

## When not to use this
* Simple monoliths with low complexity.

## What comes next
In Phase 58, we explore Event Sourcing and reconstruct state through log replay.
