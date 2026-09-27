# Lesson 64: Kafka Anti-Patterns

## Motto
"Experience is what you get right after you needed it; study anti-patterns to avoid paying the price."

## Problem
Distributed systems fail in predictable, recurring patterns.
Over a decade of Kafka adoption in production, teams keep making the same 14 catastrophic mistakes:
1. One partition for 100,000 msgs/sec requirement.
2. Random unkeyed records when per-entity order is mandatory.
3. Committing offsets before business processing (data loss).
4. Committing after every single record (throughput destroyed).
5. Ignoring Consumer Lag until disk fills.
6. Assuming `acks=all` means magic zero loss without setting `min.insync.replicas=2`.
7. Passing 20 MB binary payloads through Kafka brokers.
8. Unmonitored Dead-Letter Topics (silent graveyard).
9. Synchronous request-reply over Kafka without justification.
10. Creating 5,000 micro-topics on a 3-broker cluster.
11. Non-idempotent consumers under At-Least-Once delivery.
12. Relying on auto-topic creation in production.
13. In-process retry loops that stall partition consumption.
14. Believing Kafka transactions magically protect external databases.

## Prediction
Which of these 14 anti-patterns causes immediate permanent data loss?

## Why this matters
Knowing how systems break before they go into production saves careers and prevents catastrophic outages.

## First principles
Each anti-pattern violates a specific first principle: mechanical sympathy, network invariants, or consumer group contracts.

## Mental model
```text
The Hall of Anti-Patterns:
1. Auto-Topic Creation Enabled ──► Typo in topic name ("ordrs") creates phantom empty topic!
2. acks=all + min_isr=1        ──► 2 brokers die, leader accepts write, leader dies -> DATA LOST!
3. Commit Before Work          ──► Process crashes -> RECORD PERMANENTLY SKIPPED!
4. Unkeyed Banking Events      ──► Withdrawal processed before deposit -> FALSE OVERDRAFT!
```

## Build it
See [anti_patterns_analyzer.py](../code/anti_patterns_analyzer.py).
We catalog the anti-patterns and their structural remediations.

## Use Kafka
Audit your cluster configuration against the anti-pattern checklist.

## Inspect it
Check broker configs: verify `auto.create.topics.enable=false`.

## Measure it
Quantify the blast radius of each failure mode.

## Break it
Simulate an unkeyed financial stream and observe out-of-order interleaving.

## Recover it
Apply explicit keying and verify strict ordering restoration.

## Modify it
Create a production readiness pre-launch checklist based on these 14 rules.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is `auto.create.topics.enable=true` considered a major operational hazard in production?
2. Why is a Dead-Letter Topic that nobody monitors worse than letting the consumer crash loudly?

## Guarantees
* Eliminating these 14 anti-patterns prevents 95% of common Kafka production outages.

## Non-guarantees
* Operational diligence must be maintained continuously as new engineers join the team.

## When to use this
* Production readiness reviews (PRR), architectural audits, code reviews.

## When not to use this
* Ignoring anti-patterns because "our system is small right now".

## What comes next
In Phase 65, we build Capstone 3: A Production-Like Resilient Kafka Laboratory!
