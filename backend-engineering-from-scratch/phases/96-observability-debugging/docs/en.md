# Lesson 96: Observability Debugging

> **Motto**: Triangulating metrics, logs, and traces isolates the root cause of production anomalies without guessing.

---

## Motto
"Triangulating metrics, logs, and traces isolates the root cause of production anomalies without guessing."

## Problem
When an incident strikes, developers guess blindly, adding print statements and restarting servers at random.

## Prediction
Following a disciplined diagnosis funnel from high-level RED metrics to correlated trace spans isolates bottlenecks in minutes.

## Why this matters
Observability transforms chaotic outages into calm, evidence-based engineering investigations.

## First principles
Symptom (Metrics spike) -> Breadth (Which routes/tenants?) -> Depth (Trace span) -> Ground Truth (Log traceback).

## Mental model
```text
Dashboard Alert: p99 Latency > 2s -> Scrape RED Metrics -> Pinpoint Route -> Open Distributed Trace -> Find Slow Span
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: OpenTelemetry and Prometheus debugging workflows.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/96-observability-debugging/tests/ -v
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
- **Failure Injection**: Trigger an incident where p99 latency doubles while CPU remains idle; execute diagnostic triage.
- Execute the experiment script:
```bash
python phases/96-observability-debugging/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Follow the diagnosis funnel: confirm traffic is normal, isolate slow endpoint, trace span to lock wait, and identify root cause.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never restart services without capturing active diagnostic state (goroutines/threads, open connections, lock queries).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Correlate client-reported incident timestamps with server error spikes to narrow the investigation window.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Document post-mortem incident reviews with timeline evidence and preventative architectural fixes.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does restarting a service during an active investigation destroy crucial debugging evidence?
2. How do distributed trace spans pinpoint whether a delay originated in application CPU, database lock, or external API?
3. What steps constitute the systematic backend debugging funnel?

## What comes next
Having understood observability debugging, we next discover its inherent boundaries and transition to **Testing Pyramid / Strategy**.
