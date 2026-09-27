# Lesson 17: Compression

## Motto
"Compressing individual messages compresses noise; compressing batches compresses structure."

## Problem
JSON and XML events are verbose and repetitive. Field names like `timestamp`, `customer_id`, and `transaction_type` repeat on every event.
If you send uncompressed events, network bandwidth and broker disk storage fill up rapidly.
If you compress single messages independently, compression dictionaries have almost nothing to work with.
How does Kafka achieve 5x to 10x compression ratios?

## Prediction
Why does Kafka compress an entire `RecordBatch` rather than individual records?

## Why this matters
Kafka's compression happens **at the batch level**. Because a batch contains hundreds of structurally identical records, compression algorithms achieve staggering efficiency. Furthermore, Kafka brokers store the compressed batch directly to disk without decompressing it, preserving CPU!

## First principles
* **End-to-End Compression:** The producer compresses the batch. The broker validates headers and writes the compressed bytes directly to disk. The consumer decompresses the batch. Broker CPU overhead is minimal!
* **Supported Codecs:** `gzip` (highest ratio, higher CPU), `snappy` (balanced, low CPU), `lz4` (fastest, high throughput), `zstd` (modern, high ratio + fast decompression).

## Mental model
```text
Producer (Compresses Batch)
[ Rec 1, Rec 2, ... Rec 100 ] ──(LZ4)──► [ 1 Compressed RecordBatch ]
                                                │
Kafka Broker (Zero-Decompression Storage)        ▼ (Wire Transfer: 85% smaller)
Disk Log File: [ 1 Compressed RecordBatch ] ◄──┘ (Written directly to disk!)
                                                │
Consumer (Decompresses Batch)                    ▼ (Wire Fetch)
[ Rec 1, Rec 2, ... Rec 100 ] ◄──(LZ4 Decompress)
```

## Build it
See [compression_benchmark.py](../code/compression_benchmark.py).
We compare wire byte size and compression ratios across `none`, `gzip`, and `lz4`.

## Use Kafka
Set `compression_type='lz4'` in `KafkaProducer`.

## Inspect it
Use `kafka-dump-log.sh` to observe the `compresscodec` field in on-disk record batch headers.

## Measure it
Measure total payload bytes sent and CPU duration across codecs.

## Break it
Send pre-compressed binary data (e.g. encrypted JPEG images) with `gzip` enabled; observe that payload size actually *increases* due to compression overhead.

## Recover it
Disable compression for already compressed or encrypted binary payloads.

## Modify it
Test `snappy` vs `gzip` on repetitive JSON structures and document trade-offs.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does end-to-end compression keep Kafka broker CPU utilization low?
2. Under what workload would compression decrease overall system throughput?

## Guarantees
* Decompressed records on the consumer are bit-for-bit identical to producer input.

## Non-guarantees
* Compression does not reduce size for random binary or pre-compressed payloads.

## When to use this
* Standard JSON, Avro, Protobuf, or text payloads in production pipelines.

## When not to use this
* Streaming video, compressed JPEGs, or pre-encrypted binary streams.

## What comes next
In Phase 18, we investigate Producer Acknowledgments (`acks=0`, `acks=1`, `acks=all`).
