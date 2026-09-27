# Lesson [Phase Number]: [Title]

## Motto
"[A one-sentence mechanical insight or warning about this mechanism]"

## Problem
[Describe the engineering bottleneck, distributed systems failure mode, or architectural challenge that necessitates this mechanism. Why can we not simply use a traditional database, an in-memory queue, or basic RPC here?]

## Prediction
Before executing any code or commands, answer these questions:
1. [What do you predict will happen when X occurs?]
2. [What failure, latency spike, or data anomaly will occur if we stress or disconnect Y?]

## Why this matters
[Connect this lesson directly to real-world production systems and system design trade-offs: latency vs. throughput, availability vs. consistency, duplicate processing, partition skew, network partition behavior.]

## First principles
[Explain the physical and architectural mechanics: OS page cache, sequential disk heads/NAND pages, TCP socket buffers, monotonic 64-bit sequence numbers, Raft consensus logs, or network packet framing.]

## Mental model
```text
[ASCII diagram representing the exact data structures, partition layouts, or network interactions involved in this lesson]
```

## Build it
[Write or explain a minimal, zero-magic Python implementation from scratch before touching real Kafka.]

* See [implementation.py](../code/implementation.py)

```python
# Code snippet demonstrating the core mechanism in pure Python
```

## Use Kafka
[Execute the official Kafka commands or run the Python client script using the pinned Kafka 3.8.0 engine.]

```bash
# Example shell commands
docker exec -it kafka-lab-single /opt/kafka/bin/...
```

## Inspect it
[Use diagnostic CLI tools or Python APIs to look underneath the abstraction: topic metadata, partition log dumps, consumer group offsets, or KRaft metadata trees.]

```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-dump-log.sh ...
```

## Measure it
[Collect quantitative metrics: records/sec, MB/sec, producer latency percentiles (p50, p95, p99), consumer lag, or batch size efficiency.]

| Scenario | Records/sec | Throughput (MB/s) | p50 Latency (ms) | p99 Latency (ms) | Consumer Lag |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Baseline | ... | ... | ... | ... | ... |
| Stressed | ... | ... | ... | ... | ... |

## Break it
[Intentionally trigger a catastrophic failure: kill the partition leader broker, simulate a slow consumer, inject poison pill records, cause key skew, or cut network reachability.]

```bash
# Command to inject failure
```

## Recover it
[Diagnose the failure using evidence from logs, consumer group describe outputs, or broker metrics. Show the exact mechanical steps to restore normal operation.]

## Modify it
[Provide a concrete exercise where the learner changes a parameter: linger.ms, batch.size, acks, min.insync.replicas, or partition keys to observe the behavioral shift.]

1. Change `X` to `Y` in the configuration/code.
2. Re-run the experiment and observe how metric `Z` responds.

## Evidence
Record your results in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. [Deep reasoning question testing architectural understanding rather than CLI memorization]
2. [Failure analysis scenario question]
3. [Trade-off evaluation question]

## Guarantees
* [Explicit guarantee 1 provided by this mechanism]
* [Explicit guarantee 2]

## Non-guarantees
* [Crucial misconception / what this mechanism does NOT guarantee]
* [Boundary of safety]

## When to use this
* [Concrete production scenario 1]
* [Concrete production scenario 2]

## When not to use this
* [Counter-indication scenario 1]
* [Counter-indication scenario 2]

## What comes next
[A transition sentence leading into the next phase and the next mechanical problem to be solved.]
