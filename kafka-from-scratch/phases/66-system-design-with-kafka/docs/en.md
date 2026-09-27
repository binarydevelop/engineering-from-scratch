# Lesson 66: System Design With Kafka

## Motto
"Architecture is not drawing boxes on a whiteboard; architecture is answering the 20 questions."

## Problem
In system design interviews or enterprise design reviews, engineers often draw a box labeled *"Kafka"* in the middle of a diagram and assume their job is done.
A senior architect interrogates that box with **20 precise mechanical questions**:
1. Why Kafka? Why not direct API calls or Redis Streams?
2. What is the topic design (broad vs fine-grained)?
3. What is the partition key?
4. What ordering guarantees are required?
5. Expected peak throughput (records/sec and MB/sec)?
6. Average and maximum record size?
7. Time-based retention or size-based retention?
8. Is log compaction required?
9. Replication factor (typically 3)?
10. `min.insync.replicas` setting (typically 2)?
11. Producer acknowledgment strategy (`acks=all` vs `1`)?
12. Consumer group architecture and member scaling limits?
13. Retry pattern (in-process vs retry topics)?
14. Consumer idempotency strategy (deduplication key)?
15. Tolerable consumer lag SLA?
16. Failure behavior (what happens when a broker or consumer dies)?
17. Historical replay requirements?
18. Schema evolution strategy (Avro/Protobuf/JSON Schema)?
19. Security protocol (SASL_SSL + ACLs)?
20. What alternative technology could have solved this simpler?

## Prediction
Can you answer all 20 questions for an Uber ride-tracking telemetry pipeline?

## Why this matters
Mastering these 20 questions elevates you from a developer who uses Kafka CLI commands to a principal systems architect who designs durable distributed platforms.

## Build it
See [system_design_evaluator.py](../code/system_design_evaluator.py).
We apply the 20-Question framework to 10 real-world systems:
* Ride-sharing GPS telemetry
* Real-time payment processing
* Ad-tech clickstream analytics
* Healthcare patient vitals monitoring
* IoT smart meter ingestion
* Database CDC search indexing
* E-commerce order fulfillment
* Security SIEM audit logging
* Centralized distributed logging
* Video streaming view metrics

## Use Kafka
Evaluate architectural trade-offs across each system.

## Inspect it
Observe how different domain requirements lead to radically different partition keys and retention settings.

## Measure it
Calculate hardware and partition counts for high-volume scenarios.

## Break it
Propose an architecture that uses an unkeyed topic for payment balance updates and diagnose the resulting failure.

## Recover it
Apply entity keying to guarantee partition order.

## Modify it
Pick a system from your own job and document its 20-question specification.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does partition key selection directly determine both ordering safety and workload balance?
2. In what scenario would you configure `cleanup.policy=compact` instead of time retention?

## Guarantees
* Complete, rigorous architectural specification for any event streaming system.

## Non-guarantees
* No design is immune to changing business requirements; re-evaluate questions periodically.

## When to use this
* System design interviews, architecture design documents (ADD), technical RFCs.

## When not to use this
* Trivial internal scripts.

## What comes next
In Phase 67, we synthesize the Final Mental Model and trace a single record from socket to disk to consumer commit.
