# Lesson 19: Database Connections

> **Motto**: Opening a database connection requires a TCP 3-way handshake, TLS negotiation, authentication, and backend process spawning.

---

## Motto
"Opening a database connection requires a TCP 3-way handshake, TLS negotiation, authentication, and backend process spawning."

## Problem
Opening and closing a new database connection for every single incoming HTTP request destroys throughput.

## Prediction
Measuring the latency of connection establishment demonstrates why connections are expensive operating system resources.

## Why this matters
High connection churn causes PostgreSQL process exhaustion and ephemeral port exhaustion on application hosts.

## First principles
Creating a connection costs 10-50ms of network roundtrips and operating system fork overhead on PostgreSQL.

## Mental model
```text
Client -> TCP Handshake (1 RTT) -> TLS Handshake (1-2 RTT) -> Auth Exchange (1 RTT) -> Backend Process Initialized
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Connection lifecycle manager maintaining persistent connections.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/19-database-connections/tests/ -v
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
- **Failure Injection**: Open 1,000 raw connections rapidly in a tight loop.
- Execute the experiment script:
```bash
python phases/19-database-connections/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe database error: 'FATAL: sorry, too many clients already' and OS socket exhaustion.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Establish persistent connections and transition immediately to connection pooling.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Database connection strings contain credentials and must be protected in environment variables.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: PostgreSQL forks a dedicated backend process per connection; 1,000 connections can overwhelm host RAM.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does opening a PostgreSQL connection take significantly longer than opening a persistent SQLite connection?
2. What operating system resources are allocated when a database connection is created?
3. How does connection churn trigger ephemeral port exhaustion?

## What comes next
Having understood database connections, we next discover its inherent boundaries and transition to **Connection Pooling**.
