# Lesson 156: Capacity Estimation

> **Motto**: Capacity estimation calculates required CPU, memory, database QPS, network bandwidth, and storage from business requirements.

---

## Motto
"Capacity estimation calculates required CPU, memory, database QPS, network bandwidth, and storage from business requirements."

## Problem
Guessing server sizes leads to massive over-provisioning cloud costs or catastrophic traffic saturation crashes.

## Prediction
Calculating throughput, database queries per second, and network egress from first principles sizes infrastructure accurately.

## Why this matters
Capacity estimation allows engineers to design systems that handle peak traffic within budget before writing code.

## First principles
RPS = DAU x Actions / Seconds. QPS = RPS x Queries/Req. Bandwidth = RPS x Payload Size. Storage = RPS x Size x Days.

## Mental model
```text
1,000 RPS -> 5 DB Queries/Req = 5,000 QPS -> 10KB Payload = 10MB/sec Bandwidth -> Sizing infrastructure accurately!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: System design capacity estimation modeling.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/156-capacity-estimation/tests/ -v
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
- **Failure Injection**: Given 10 million Daily Active Users (DAU), calculate average RPS, peak RPS (2x), database QPS, and annual storage needs.
- Execute the experiment script:
```bash
python phases/156-capacity-estimation/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert calculations match expected architectural limits; verify database pool sizing satisfies peak concurrent connections.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always design for PEAK traffic, not average traffic: peak load is typically 2x to 5x higher than daily average load.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Calculate database storage growth over 3 years: include index overhead (typically +50% of raw table data).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Include network egress bandwidth costs in capacity models; cloud bandwidth pricing can exceed server compute costs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How do you estimate peak Requests Per Second (RPS) from Daily Active User (DAU) figures?
2. Why must database IOPS and connection pool sizing be calculated using peak traffic rather than average traffic?
3. What hidden storage overheads (indexes, logs, backups) must be accounted for beyond raw table row data?

## What comes next
Having understood capacity estimation, we next discover its inherent boundaries and transition to **Little's Law Intuition**.
