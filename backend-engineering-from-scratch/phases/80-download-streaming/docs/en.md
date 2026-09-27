# Lesson 80: Download Streaming

> **Motto**: Streaming responses deliver large files or datasets in incremental chunks, avoiding buffering large payloads into memory.

---

## Motto
"Streaming responses deliver large files or datasets in incremental chunks, avoiding buffering large payloads into memory."

## Problem
Loading an entire 1GB export file into a Python variable before returning causes massive memory spikes and delays time-to-first-byte.

## Prediction
Yielding data chunk-by-chunk using chunked transfer encoding starts client downloads instantly and uses fixed memory.

## Why this matters
Streaming responses enable fast exports, real-time audio/video delivery, and memory-safe CSV generation.

## First principles
Chunked Transfer Encoding: Transfer-Encoding: chunked. Server sends hex chunk length followed by chunk bytes.

## Mental model
```text
Generator function: yield chunk_1 -> Socket write -> yield chunk_2 -> Socket write -> yield b'' (Done)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI `StreamingResponse` with generator iterators.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/80-download-streaming/tests/ -v
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
- **Failure Injection**: Download a 100MB synthetic dataset; measure server memory and time-to-first-byte (TTFB) with vs without streaming.
- Execute the experiment script:
```bash
python phases/80-download-streaming/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Without streaming: TTFB = 1.2s, RAM = +100MB. With streaming: TTFB = 4ms, RAM = flat (< 1MB).
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Handle client disconnects gracefully: detect when a client terminates the connection early and abort generator execution.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Streaming responses bypass downstream middleware that attempts to inspect the entire response body in memory.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Always set `Content-Disposition: attachment; filename=...` headers to prompt browser download dialogs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is Chunked Transfer Encoding in HTTP/1.1?
2. How does streaming a download response improve Time-To-First-Byte (TTFB)?
3. What happens to an active generator if the downloading client closes the browser tab midway?

## What comes next
Having understood download streaming, we next discover its inherent boundaries and transition to **API Versioning**.
