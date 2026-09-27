# Lesson 63: When Kafka Is the Wrong Tool

## Motto
"The senior engineer's superpower is knowing when NOT to use Kafka."

## Problem
Kafka has immense momentum in the industry.
Engineers frequently propose Kafka for:
* Sending simple background email tasks
* Serving user profile lookups by ID
* Handling synchronous HTTP requests between two microservices
* Small systems with 50 messages/minute
This introduces massive operational overhead: KRaft clusters, disk storage, partition rebalance debugging, and schema governance for zero architectural benefit.
When is Kafka the wrong tool?

## Prediction
What simpler technology should you pick if you just need to pop background tasks across 20 workers without ordering constraints?

## Why this matters
**System design is the science of trade-offs.** Recommending Kafka everywhere is the hallmark of inexperienced architecture.

## First principles
| Requirement | Why Kafka is the WRONG Tool | Better Alternative |
| :--- | :--- | :--- |
| **Simple Task Queue** | Kafka partitions limit concurrency; no per-message ack or priority | **RabbitMQ, AWS SQS, Celery, Redis Lists** |
| **Random Key-Value Lookup** | Kafka is an append-only log; random seeks by key require scanning segments | **PostgreSQL, DynamoDB, Redis, Cassandra** |
| **Synchronous RPC** | Request-reply over Kafka introduces high latency and correlation complexity | **gRPC, REST HTTP/2** |
| **Tiny Volume (<10 msgs/s)** | Operational overhead of Kafka cluster dwarfs utility | **Postgres table or Redis Streams** |
| **Complex Graph / Ad-Hoc SQL** | Kafka is not a relational query engine | **PostgreSQL, Snowflake, ClickHouse** |
| **Multi-Megabyte Video Files** | Evicts page cache, saturates network buffers | **S3 / Object Storage + Claim-Check** |

## Mental model
```text
The Architecture Decision Filter:
Do you need:
1. High-throughput (>10,000 msgs/sec)?
2. Multiple independent consumer groups reading the same stream?
3. Historical event replay from days ago?
4. Strict per-entity ordered partitioning?

If YES to 2 or more ──► KAFKA IS A GREAT FIT!
If NO to all 4       ──► KAFKA IS PROBABLY OVERKILL! Use SQS, Postgres, or Redis!
```

## Build it
See [evaluate_kafka_fit.py](../code/evaluate_kafka_fit.py).
An interactive technical evaluation matrix.

## Use Kafka
Run the decision advisor against 5 classic architectural scenarios.

## Inspect it
Observe why a synchronous REST call or simple SQS queue is vastly simpler for specific requirements.

## Measure it
Compare operational complexity: lines of configuration for SQS vs 3-node KRaft cluster.

## Break it
Attempt to use Kafka as a database by issuing random key queries; observe performance degradation.

## Recover it
Pair Kafka with a proper read database (CQRS pattern).

## Modify it
Add your company's current workload into the evaluation framework.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is RabbitMQ superior to Kafka for complex routing keys and per-message task timeouts?
2. When does adopting Kafka become a net negative for an engineering team?

## Guarantees
* Honest evaluation framework preventing costly architectural blunders.

## Non-guarantees
* No technology choice is permanently static; requirements evolve as scale grows.

## When to use this
* Architecture reviews, tech stack selection, RFC evaluations.

## When not to use this
* Post-facto rationalization of bad technical decisions.

## What comes next
In Phase 64, we document 14 Catastrophic Kafka Anti-Patterns.
