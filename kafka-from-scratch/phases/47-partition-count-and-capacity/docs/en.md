# Lesson 47: Partition Count and Capacity

## Motto
"More partitions mean more parallelism; too many partitions mean delayed failover and operating system exhaustion."

## Problem
An engineer reasons:
*"If partitions give us throughput, why not create 1,000 partitions for every topic?"*
They deploy 50 topics with 1,000 partitions each on a 3-broker cluster (50,000 total partitions).
Suddenly:
* Broker startup time jumps to 15 minutes.
* Broker memory spikes due to open file handles and indexes.
* When a broker restarts, controller leader election experiences latency spikes.
How do you determine the *optimal* number of partitions?

## Prediction
What are the hidden operational costs of having tens of thousands of idle partitions on a Kafka cluster?

## Why this matters
Sizing partition count is a balancing act between **required consumer throughput** and **broker operational overhead**.

## First principles
**The Partition Sizing Rule of Thumb:**
$$\text{Partitions} = \max\left( \frac{\text{Target Producer Throughput}}{P_p}, \frac{\text{Target Consumer Throughput}}{C_p} \right)$$
* Where $P_p$ is single-partition producer throughput (~10-20 MB/s).
* Where $C_p$ is single-partition consumer throughput (~2-5 MB/s, often bottlenecked by DB writes).
* **The Costs of Excessive Partitions:**
  1. Open file descriptors (each partition segment requires 2-3 open files).
  2. Memory buffers allocated per partition in client producers (`batch.size` $\times$ partitions).
  3. Increased leader election and metadata sync duration during broker failovers.

## Mental model
```text
Under-Partitioned (1 Partition):
- Max throughput = 2,000 msgs/s
- Bottleneck! Cannot scale consumer workers!

Optimal (6 to 12 Partitions):
- Matches consumer concurrency needs
- Low metadata overhead, fast failover (<100ms)

Over-Partitioned (1,000 Partitions for low traffic):
- Thousands of tiny files on disk
- Producer client memory waste
- Slower cluster recovery
```

## Build it
See [partition_sizing_tool.py](../code/partition_sizing_tool.py).
We calculate partition recommendations based on producer and consumer benchmarks.

## Use Kafka
Inspect current cluster partition count and partition-to-broker ratios.

## Inspect it
Check open file descriptors used by the Kafka broker process using `lsof`.

## Measure it
Compare client producer memory footprint with 3 partitions vs 100 partitions.

## Break it
Create 1,000 partitions on a tiny single-broker lab container and observe memory and file handle growth.

## Recover it
Plan topics with conservative partition counts (e.g. 6, 12, or 24); scale up only when measured throughput demands it.

## Modify it
Test altering partition count dynamically on an active topic.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can topic partition count be increased with `kafka-topics.sh --alter`, but NEVER decreased?
2. How does the number of partitions impact client-side producer memory allocation?

## Guarantees
* Higher partition count enables higher active consumer group parallelism.

## Non-guarantees
* Adding partitions does not improve throughput if producer keys are severely skewed.

## When to use this
* In all topic creation and architecture design decisions.

## When not to use this
* Creating hundreds of partitions "just in case" without throughput data.

## What comes next
In Phase 48, we learn how to balance clusters by Reassigning Partitions across brokers.
