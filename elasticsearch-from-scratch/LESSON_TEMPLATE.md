# Lesson <Phase>.<Sublesson>: <Lesson Title>

## Motto
"<A concise, unforgettable engineering maxim highlighting the underlying physical or mathematical reality.>"

## Problem
<Describe the concrete systems engineering or data access problem in production. Why does standard naive approach fail? What is the operational pain point?>

## Prediction
<A concrete, quantitative, or behavioral question. Before running any code or commands, write down what you expect to observe.>

## Why this matters
<Connect this concept to latency, storage, memory, query accuracy, cluster health, or distributed failure modes.>

## First principles
<Explain the mathematical, physical, or algorithmic mechanism underpinning this feature (e.g. hash partitioning, inverted index postings, term saturation, columnar doc values, segment immutability).>

## Mental model
```text
<ASCII or Mermaid architectural diagram contrasting the naive approach vs the engine's internal mechanism>
```

## Build it
<Build the simplified concept from scratch in pure Python without external dependencies. Demonstrate the core algorithm before touching Elasticsearch.>
* See `code/<script_name>.py`

## Use Elasticsearch
<Execute the canonical Elasticsearch REST command or script exercising the feature.>
```bash
# Example curl or script invocation
./phases/<phase_dir>/experiments/run_experiment.sh
```

## Inspect it
<Commands to inspect internal state, segment metadata, mappings, cluster routing, or explain plans.>
```bash
curl -s http://localhost:9200/_cat/indices?v
curl -s http://localhost:9200/<index>/_explain/<id> -d '...'
```

## Measure it
<Quantify the behavior: latency (p50, p95, p99), index byte size, heap allocation, segment counts, or QPS.>

## Break it
<Intentionally misconfigure, overload, corrupt, or simulate a failure condition to observe the exact failure mode.>

## Recover it
<Step-by-step diagnostic and remediation process to restore the system to green/healthy state.>

## Modify it
<Variations, parameter experiments (e.g. changing refresh_interval, k1/b BM25 params, routing keys, heap limits) and observed impacts.>

## Evidence
Record your experimental observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. <Deep reasoning question probing trade-offs and edge cases.>
2. <Operational question testing diagnostic intuition.>

## Guarantees
* <What the system provably guarantees when this feature is used correctly.>

## Non-guarantees
* <What the system does NOT guarantee, and common false assumptions.>

## When to use this
* <Clear, production-validated use cases.>

## When not to use this
* <Scenarios where this feature introduces unnecessary complexity, latency, or fragility.>

## What comes next
<Connection to the subsequent lesson in the dependency chain.>
