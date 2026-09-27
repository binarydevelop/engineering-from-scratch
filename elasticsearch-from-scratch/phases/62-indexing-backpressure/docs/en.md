# Lesson 62.1: Indexing Backpressure

## Motto
"Search clusters have finite write capacity: when bulk queues fill, client requests must back off."

## Problem
During peak traffic, ingestion workers submit bulk batches at 100,000 docs/sec, but disk write speed on data nodes caps out at 30,000 docs/sec. The cluster thread pool write queue fills up, and Elasticsearch begins returning HTTP 429 Too Many Requests (`EsRejectedExecutionException`).

## Prediction
What happens if clients ignore HTTP 429 errors and immediately retry at full speed?

## Why this matters
Elasticsearch is not an unbounded message broker like Kafka. It uses fixed-capacity thread pool queues. Responding to backpressure with exponential backoff prevents cluster crashes.

## First principles
* **Write Thread Pool:** Fixed number of worker threads (typically equal to CPU cores).
* **Write Queue:** Fixed-size queue (default **10,000** tasks).
* When queue is full, new requests are rejected with **HTTP 429** (`EsRejectedExecutionException`).
* Clients must implement **Exponential Backoff with Jitter**.

## Mental model
```text
Client Workers ──► Submitting 100k docs/sec
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
Write Threads (8 cores)           Write Queue (Capacity: 10,000)
(Pinned at 100% CPU)              (Full! 10,000 tasks waiting!)
                                          │
                                          ▼
                               HTTP 429 Too Many Requests!
                               (Client MUST back off!)
```

## Build it
See `code/backoff_simulator.py` demonstrating exponential backoff with jitter in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/62-indexing-backpressure/experiments/run_experiment.sh
```

## Inspect it
Monitor write queue depth and rejections:
```bash
curl -s "http://localhost:9200/_cat/thread_pool/write?v&h=node_name,name,active,queue,rejected,completed"
```

## Measure it
Measure retry latency and success rate during induced queue saturation.

## Break it
Launch 50 parallel Python processes submitting massive bulk payloads to induce HTTP 429 rejections.

## Recover it
Implement client retry logic:
$$	ext{sleep} = \min(	ext{max\_sleep}, 	ext{base} 	imes 2^{	ext{attempt}}) \pm 	ext{jitter}$$

## Modify it
Inspect ingest node backpressure metrics: `node_stats.indexing.throttle_time_in_millis`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch reject writes with HTTP 429 instead of expanding its queue infinitely in memory?
2. What is "jitter" and why is it critical when retrying after backpressure?

## Guarantees
* Fixed write queues protect the JVM from running out of heap memory under write floods.

## Non-guarantees
* Elasticsearch does not buffer rejected writes for you; the client is responsible for retrying.

## When to use this
* Every production ingestion pipeline, Kafka consumer, and log shipper.

## When not to use this
* Low-volume systems where write queue saturation is physically impossible.

## What comes next
In Phase 63, we analyze JVM Heap and Operating System Memory.
