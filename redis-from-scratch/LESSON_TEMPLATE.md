# Lesson [Phase Number].[Lesson Number]: [Title]

## Motto
"[A one-sentence mechanical insight or warning about this mechanism]"

## Problem
[Describe the engineering challenge, architectural bottleneck, or failure mode that necessitates this mechanism. Why can we not simply use a basic in-memory variable or SQL database here?]

## Prediction
Before executing any code or commands, answer these questions:
1. [What do you expect the return value or behavior to be when X happens?]
2. [What failure or latency impact will occur if we stress Y?]

## Why this matters
[Connect this lesson directly to real-world production systems and system design trade-offs (e.g. latency, memory footprint, cache stampedes, data loss, split-brain).]

## First principles
[Explain the underlying physical and architectural mechanics: CPU cache lines, DRAM access times, OS network buffers, TCP packet framing, hash table bucket arrays, or disk write barriers.]

## Mental model
```text
[ASCII diagram representing the exact data structures, network packets, or memory layout involved in this lesson]
```

## Build it
[Write or explain a minimal, zero-magic Python implementation from scratch before touching real Redis.]

* See [implementation.py](../code/implementation.py)

```python
# Code snippet highlighting the core first-principles algorithm
```

## Use Redis
[Execute the official Redis commands or run the Python client script that uses the pinned Redis engine.]

```bash
# Example shell commands
redis-cli [COMMAND]
```

## Inspect it
[Use diagnostic commands to look underneath the abstraction: OBJECT ENCODING, MEMORY USAGE, DEBUG, SLOWLOG, INFO, or MONITOR.]

```bash
redis-cli OBJECT ENCODING [key]
redis-cli MEMORY USAGE [key]
```

## Measure it
[Collect quantitative metrics: latency percentiles (p50, p95, p99), throughput (ops/sec), memory bytes allocated, or cache hit/miss ratio.]

| Scenario | Operations/sec | Mean Latency (ms) | p99 Latency (ms) | Memory Used |
| :--- | :--- | :--- | :--- | :--- |
| Baseline | ... | ... | ... | ... |
| Optimized | ... | ... | ... | ... |

## Break it
[Intentionally trigger a catastrophic failure: cut the network connection, expire a key under load, corrupt an AOF byte, exceed maxmemory, or introduce a race condition.]

```bash
# Step to inject failure
```

## Debug it
[Diagnose the failure using evidence from logs, SLOWLOG, error replies, or network packet captures. Show how to restore normal operation.]

## Modify it
[Provide a concrete exercise where the learner changes an algorithm parameter, eviction policy, buffer size, or threshold to observe the behavioral shift.]

1. Change `X` to `Y` in the script.
2. Re-run and observe how metric `Z` responds.

## Evidence
Record your results in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. [Conceptual system design question testing deep understanding rather than memorization]
2. [Failure analysis scenario question]
3. [Algorithmic complexity question]

## When to use this
* [Concrete production scenario 1]
* [Concrete production scenario 2]

## When not to use this
* [Counter-indication scenario 1]
* [Counter-indication scenario 2]

## What comes next
[A transition sentence leading into the next phase and the next mechanical problem to be solved.]
