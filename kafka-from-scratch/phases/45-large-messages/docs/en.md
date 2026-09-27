# Lesson 45: Large Messages

## Motto
"Kafka is built for streaming event streams, not moving gigabyte video files."

## Problem
A machine learning team wants to pass 50 MB trained model weights or 25 MB high-resolution medical images between services.
They attempt to produce them directly to Kafka.
Immediately:
* Producer throws `RecordTooLargeException`.
* If you tune Kafka's `max.message.bytes` to 50 MB, broker memory buffers balloon, page cache gets thrash-evicted, and network saturation causes broker heartbeats to drop, triggering cluster-wide rebalances!
How should large binary payloads be handled in event-driven systems?

## Prediction
What happens to broker OS page cache performance when 50 MB payloads are passed through Kafka?

## Why this matters
Kafka is optimized for small to medium streaming records (1 KB to 100 KB). Forcing large binary blobs through Kafka violates mechanical sympathy. The solution is the **Claim-Check Pattern**.

## First principles
* **Default Limits:** `max.message.bytes=1048576` (1 MB).
* **The Claim-Check Pattern:**
  1. Producer uploads the heavy binary blob (video, PDF, ML weights) directly to Object Storage (Amazon S3, Google Cloud Storage, MinIO).
  2. Producer gets back an immutable URI: `s3://bucket/models/v1.bin`.
  3. Producer sends a lean event (1 KB) to Kafka containing the URI and metadata.
  4. Consumer receives the lean event from Kafka and downloads the payload directly from Object Storage.

## Mental model
```text
Bad Design (Forcing 50MB into Kafka):
Producer ──(50 MB Record)──► [ Kafka Broker ] ──(Memory Balloon! Heartbeat Timeout!)

The Claim-Check Pattern (Clean & Fast):
Producer ──(50 MB Blob)──► [ Object Storage: S3 / MinIO ]
   │                                  ▲
   ├──(1 KB Event with URI)──► [ Kafka ]
                                  │
                                  ▼
Consumer ◄────────────────(1 KB Event)
Consumer ──(Fetches 50MB directly)──► [ Object Storage ]
```

## Build it
See [claim_check_pattern.py](../code/claim_check_pattern.py).
We implement the Claim-Check pattern using local file storage to simulate object storage.

## Use Kafka
Observe that Kafka only transports the lightweight metadata event.

## Inspect it
Check the record size inside Kafka: < 500 bytes.

## Measure it
Compare broker throughput and memory footprint transporting 1 KB claim checks vs 10 MB raw payloads.

## Break it
Attempt to send a 2 MB record when `max.request.size=1048576` and observe `RecordTooLargeException`.

## Recover it
Implement claim-check routing for any payload exceeding 256 KB.

## Modify it
Add payload SHA-256 checksums to the Kafka event to guarantee data integrity between object storage and consumer.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does passing multi-megabyte payloads through Kafka evict valuable small events from the OS page cache?
2. How does the Claim-Check pattern solve payload retention independent of Kafka retention?

## Guarantees
* Keeps Kafka throughput and page cache utilization optimal.

## Non-guarantees
* Consumers must handle separate failure modes if Object Storage is temporarily unreachable.

## When to use this
* Whenever payload sizes regularly exceed 500 KB (images, PDFs, audio, machine learning models).

## When not to use this
* Standard domain events under 100 KB.

## What comes next
In Phase 46, we learn how to calculate Broker Disk and Capacity sizing before deploying to production.
