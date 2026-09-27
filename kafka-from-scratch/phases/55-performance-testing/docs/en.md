# Lesson 55: Performance Testing

## Motto
"Never quote a benchmark without quoting the payload size, the acks setting, and the hardware."

## Problem
Engineers frequently read blog posts claiming *"Kafka handles 2 million messages/sec!"*
They run it on their laptop or cloud VM and get 15,000 msgs/sec, wondering what broke.
A benchmark without documented conditions is meaningless marketing.
How do you conduct rigorous, scientific performance testing on Apache Kafka?

## Prediction
What has a bigger impact on producer throughput: changing `acks` from `1` to `all`, or changing batch size from 1 KB to 32 KB?

## Why this matters
**Benchmark literacy** empowers you to evaluate performance claims, size clusters accurately, and verify SLA commitments under realistic workload conditions.

## First principles
**The 6 Mandatory Benchmark Conditions:**
1. **Payload Size:** 100 bytes vs 10 KB fundamentally alters throughput (records/sec vs MB/sec).
2. **Acknowledgment Setting:** `acks=0` vs `acks=1` vs `acks=all`.
3. **Batching Knobs:** `batch.size` and `linger.ms`.
4. **Compression Codec:** `none`, `snappy`, `lz4`, `zstd`.
5. **Partition Count & Broker Count:** Hardware concurrency layout.
6. **Network & Disk Hardware:** Local NVMe SSD vs cloud networked EBS.

## Mental model
```text
Benchmark Execution Matrix:
Run 1: Baseline (Uncompressed, acks=1, batch=16K)  ──► 35,000 rec/s | 3.5 MB/s
Run 2: Tuned Batching (batch=64K, linger=15ms)      ──► 95,000 rec/s | 9.5 MB/s
Run 3: Full Durability (acks=all, min_isr=2)       ──► 70,000 rec/s | 7.0 MB/s
```

## Build it
See [benchmark_runner.py](../code/benchmark_runner.py).
We execute a standardized benchmark capturing records/sec, MB/sec, and latency percentiles.

## Use Kafka
Run the benchmark suite against your local Kafka broker.

## Inspect it
Inspect the resulting performance metrics table.

## Measure it
Capture p50, p95, and p99 latency percentiles alongside throughput.

## Break it
Saturate producer concurrency until consumer lag explodes and latency percentiles spike.

## Recover it
Identify the bottleneck (CPU, disk I/O, network) and apply appropriate batching or partition tuning.

## Modify it
Test different payload sizes (128 bytes vs 1024 bytes) and plot the results.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does high throughput (MB/sec) often correlate with higher individual message latency (due to batching delay)?
2. Why is measuring p99 latency far more important for user-facing systems than measuring average latency?

## Guarantees
* Benchmarks provide reproducible measurements under strictly defined test parameters.

## Non-guarantees
* Laptop benchmark results cannot be extrapolated directly to distributed multi-node cloud clusters.

## When to use this
* Pre-production validation, capacity planning, configuration tuning.

## When not to use this
* Quoting generic numbers in architectural discussions without defining test parameters.

## What comes next
In Phase 56, we embark on Capstone 1: Building a Mini-Kafka from scratch in pure Python!
