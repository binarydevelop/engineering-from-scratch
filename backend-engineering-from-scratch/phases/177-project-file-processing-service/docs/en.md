# Lesson 177: Project: File Processing Service

> **Motto**: Build an asynchronous file processing pipeline handling multipart uploads, object storage, background workers, and thumbnailing.

---

## Motto
"Build an asynchronous file processing pipeline handling multipart uploads, object storage, background workers, and thumbnailing."

## Problem
Processing large files synchronously inside web handlers causes memory exhaustion, slow responses, and HTTP gateway timeouts.

## Prediction
Uploading directly to storage, queuing processing tasks, and having workers transform assets keeps web servers fast and responsive.

## Why this matters
File processing pipelines are essential for modern media platforms, document management, and data import tools.

## First principles
Client Uploads -> Stream to Storage -> Enqueue Task -> Worker downloads, resizes/converts, uploads result, updates status.

## Mental model
```text
Client ──[Upload Image]──> Web API (Streams to S3) ──[Enqueues Task]──> Worker (Generates Thumbnails) ──> S3
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Asynchronous media and document processing pipeline.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/177-project-file-processing-service/tests/ -v
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
- **Failure Injection**: Upload a 50MB file; verify API responds in < 20ms with job ID; worker generates 3 thumbnail sizes and marks job ready.
- Execute the experiment script:
```bash
python phases/177-project-file-processing-service/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Query job status endpoint; observe status transition from 'processing' to 'completed' with download URLs.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never read entire large files into memory: stream uploads in 64KB chunks to maintain flat process memory footprints.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Clean up temporary working directories in worker processes using context managers to prevent filling worker disks.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Validate file MIME types by inspecting magic header bytes to block malicious executable uploads.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must file uploads be streamed in chunks rather than read entirely into process memory?
2. How does passing object storage keys in worker queue messages prevent memory bloat across the messaging cluster?
3. How do magic byte checks protect file processing pipelines from malicious executable uploads?

## What comes next
Having understood project: file processing service, we next discover its inherent boundaries and transition to **Project: Analytics Event API**.
