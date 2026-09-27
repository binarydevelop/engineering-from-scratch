# Lesson 79: Object Storage

> **Motto**: Relational databases store structured metadata; unstructured binary blobs belong in scalable object stores.

---

## Motto
"Relational databases store structured metadata; unstructured binary blobs belong in scalable object stores."

## Problem
Storing large PDFs, images, and videos as BYTEA/BLOB columns in PostgreSQL bloats databases, degrades backups, and exhausts RAM.

## Prediction
Storing metadata (filename, size, S3 URL) in SQL and binary data in S3-compatible storage optimizes cost and performance.

## Why this matters
Object storage provides near-infinite scale, multi-region durability, and direct-to-client presigned downloads.

## First principles
Relational DB: `id, filename, s3_key, size, uploaded_at` <───> S3 Bucket: `s3_key -> [Binary Blob Bytes]`.

## Mental model
```text
API -> Save File to Object Storage -> Get Object Key -> Insert Record in PostgreSQL (Metadata Only)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: MinIO / AWS S3 client integration in Python backends.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/79-object-storage/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Benchmark query latency and database file size when storing 100 images in SQL BLOBs vs SQL metadata + Object Store.
- Execute the experiment script:
```bash
python phases/79-object-storage/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Database with BLOBs explodes in size and query latency degrades; metadata-only database remains tiny and sub-millisecond.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Generate presigned upload and download URLs so clients transfer files directly to S3 without traversing API servers.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never make object storage buckets publicly writable; restrict access to presigned URLs with short expiration windows.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Object storage is optimized for throughput, not low-latency random seeks; design access patterns accordingly.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should large binary files never be stored directly in relational database tables?
2. What is a presigned S3 URL and how does it reduce bandwidth and load on application API servers?
3. How do you ensure consistency between a metadata record in SQL and an object in S3?

## What comes next
Having understood object storage, we next discover its inherent boundaries and transition to **Download Streaming**.
