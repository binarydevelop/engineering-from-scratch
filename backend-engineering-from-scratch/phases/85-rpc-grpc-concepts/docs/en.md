# Lesson 85: RPC / gRPC Concepts

> **Motto**: Remote Procedure Call (RPC) frameworks execute procedures across networks as if they were local function calls.

---

## Motto
"Remote Procedure Call (RPC) frameworks execute procedures across networks as if they were local function calls."

## Problem
HTTP/JSON text serialization incurs significant CPU and bandwidth overhead in high-throughput internal microservice chains.

## Prediction
Using strongly-typed binary protocols like gRPC (Protocol Buffers over HTTP/2) delivers sub-millisecond serialization and low bandwidth.

## Why this matters
Understanding when to use REST vs gRPC optimizes external client ergonomics vs internal microservice throughput.

## First principles
REST: Textual JSON, Human-Readable, Loosely Typed, High Overhead. gRPC: Binary Protobuf, Code-Generated, Strict, High Performance.

## Mental model
```text
Client Function: stub.GetOrder(request) -> Binary Protobuf Serialization -> HTTP/2 Stream -> Server Handler
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: gRPC and Protocol Buffers concepts in Python microservices.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/85-rpc-grpc-concepts/tests/ -v
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
- **Failure Injection**: Serialize a complex 1,000-record dataset into JSON vs Protobuf; compare byte sizes and serialization CPU duration.
- Execute the experiment script:
```bash
python phases/85-rpc-grpc-concepts/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe Protobuf is 4x smaller on the wire and serializes 5x faster than standard Python JSON.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use REST/JSON for public, external, and browser APIs; use gRPC for high-volume internal service-to-service calls.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: gRPC requires HTTP/2, which can complicate load balancing at the transport layer due to long-lived TCP multiplexing.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Code generation from `.proto` contracts ensures that client and server cannot compile with mismatched schemas.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What makes binary Protocol Buffers significantly faster and more compact than textual JSON?
2. Why is gRPC preferred for internal microservices while REST/JSON remains dominant for public APIs?
3. What load balancing challenge arises from gRPC multiplexing multiple requests over a single persistent TCP connection?

## What comes next
Having understood rpc / grpc concepts, we next discover its inherent boundaries and transition to **WebSockets**.
