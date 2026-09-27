# Lesson 78: Uploads

> **Motto**: File uploads must be streamed directly to temporary storage or object stores without buffering entire gigabytes into RAM.

---

## Motto
"File uploads must be streamed directly to temporary storage or object stores without buffering entire gigabytes into RAM."

## Problem
Reading `await file.read()` on a 2GB video upload loads 2GB of raw bytes into Python process memory, triggering OOM kills.

## Prediction
Streaming file chunks (e.g. 64KB buffers) keeps memory usage flat regardless of whether the file is 1MB or 50GB.

## Why this matters
Handling file uploads correctly allows servers to accept large assets with minimal memory footprints.

## First principles
Client Stream -> 64KB Chunk Buffer -> Write to Disk / S3 -> Next Chunk -> Memory usage strictly capped at 64KB.

## Mental model
```text
Upload Stream ──[Chunk 1: 64KB]──> Temp File on Disk ──[Chunk 2: 64KB]──> Temp File on Disk (Flat RAM)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI `UploadFile` (spooled temporary file) vs `bytes` parameter.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/78-uploads/tests/ -v
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
- **Failure Injection**: Upload a 500MB synthetic file using `bytes` parameter vs `UploadFile` streaming; measure process memory RSS.
- Execute the experiment script:
```bash
python phases/78-uploads/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Bytes parameter: Memory spikes by 500MB. UploadFile streaming: Memory remains flat with < 2MB change.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce strict maximum file size limits (`Content-Length` header check and streaming byte counter) to prevent disk filling.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Validate file MIME types by inspecting magic header bytes, never by trusting client-supplied file extensions.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Store uploaded files outside the web root and serve them through presigned URLs or object stores.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does reading an uploaded file with `await file.read()` risk an Out-Of-Memory crash?
2. How does chunked stream processing keep upload memory usage flat regardless of file size?
3. Why must file MIME types be verified using magic bytes rather than the file extension?

## What comes next
Having understood uploads, we next discover its inherent boundaries and transition to **Object Storage**.
