# Lesson 20: Connection Pooling

> **Motto**: A connection pool amortizes handshake costs by maintaining a bounded set of pre-established, reusable connections.

---

## Motto
"A connection pool amortizes handshake costs by maintaining a bounded set of pre-established, reusable connections."

## Problem
Under traffic spikes, an unpooled backend spawns thousands of connections, crashing the database cluster.

## Prediction
A bounded pool queues or rejects excess requests when all connections are checked out, protecting database health.

## Why this matters
Connection pooling is the essential barrier preventing traffic surges from taking down relational databases.

## First principles
A pool is a thread-safe blocking queue of initialized database connection objects.

## Mental model
```text
Request -> Pool.acquire() -> [Available Connection] -> Execute Query -> Pool.release() -> Next Request in Queue
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: SQLAlchemy QueuePool and asyncpg connection pool implementations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/20-connection-pooling/tests/ -v
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
- **Failure Injection**: Set pool size to 2 and bombard with 10 concurrent requests; measure queueing delay and timeout failures.
- Execute the experiment script:
```bash
python phases/20-connection-pooling/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect pool stats; observe waiting requests queue up and exceed pool_timeout.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Tune pool sizing according to Little's Law: $PoolSize = RPS 	imes QueryDuration$.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Connection leak: forgetting to release a connection back to the pool freezes all subsequent requests.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: In multi-replica Kubernetes deployments, total database connections = Replicas x Pool Size.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What happens to an HTTP request when all connections in a pool are busy and pool timeout is exceeded?
2. Why is a connection pool of 20 often faster than a connection pool of 500 under heavy load?
3. How does a connection leak bring down an entire backend service?

## What comes next
Having understood connection pooling, we next discover its inherent boundaries and transition to **Repository Boundary**.
