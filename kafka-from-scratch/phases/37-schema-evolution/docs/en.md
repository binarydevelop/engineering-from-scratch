# Lesson 37: Schema Evolution

## Motto
"An event format without a schema contract is a ticking production landmine."

## Problem
In early development, teams publish arbitrary JSON payloads:
`{"user_id": 42, "name": "Alice"}`
Six months later, the producer team renames `user_id` to `customer_uuid`:
`{"customer_uuid": "c-99", "name": "Alice"}`
The instant this event is published, 4 downstream consumer services crash with `KeyError: 'user_id'`.
How do producers and consumers evolve independently without coordinated deployment locks?

## Prediction
What is the difference between Backward Compatibility and Forward Compatibility in event schemas?

## Why this matters
In event-driven systems, producers and consumers are deployed independently by different teams. **Schema Evolution** is the discipline that ensures events remain readable across system versions.

## First principles
* **Backward Compatibility:** A new consumer (v2) can read data produced by an old producer (v1). (e.g. adding an optional field with a default value).
* **Forward Compatibility:** An old consumer (v1) can read data produced by a new producer (v2). (e.g. consumer ignores unknown new fields).
* **Full Compatibility:** Both backward and forward compatible.
* **Breaking Changes:** Renaming fields, changing data types (integer to string), deleting required fields.

## Mental model
```text
Producer v2 (Adds optional 'loyalty_tier')
   │
   ▼
Event: {"user_id": 42, "name": "Alice", "loyalty_tier": "GOLD"}
   ├──► Consumer v1 (Reads 'user_id' & 'name', safely IGNORES 'loyalty_tier') -> OK!
   └──► Consumer v2 (Reads all fields including 'loyalty_tier')               -> OK!
Result: Zero downtime deployment!
```

## Build it
See [schema_evolution_lab.py](../code/schema_evolution_lab.py).
We test schema evolution and observe consumer compatibility breaks.

## Use Kafka
Produce evolving JSON payloads with schema version headers.

## Inspect it
Observe how resilient consumers gracefully fallback when optional fields are missing.

## Measure it
Benchmark parsing overhead of schema validation.

## Break it
Simulate a producer renaming a required field without a migration window; watch legacy consumers crash.

## Recover it
Maintain deprecated fields alongside new fields during a transition period.

## Modify it
Implement schema evolution using Avro or Protobuf specifications.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is renaming a field always a breaking change in JSON and Protobuf?
2. Why must newly added fields always specify a default value to maintain backward compatibility?

## Guarantees
* Compatible schemas allow consumers and producers to be deployed in any arbitrary order.

## Non-guarantees
* Raw JSON without validation does not enforce schema constraints at compile time.

## When to use this
* In all cross-team production event streams.

## When not to use this
* Throwaway internal prototypes where all code is in a single repository.

## What comes next
In Phase 38, we examine Event Design: Event Notification vs. Event-Carried State Transfer.
