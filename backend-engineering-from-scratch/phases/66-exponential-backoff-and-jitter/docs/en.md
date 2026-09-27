# Lesson 66: Exponential Backoff and Jitter

> **Motto**: Exponential backoff spreads retry attempts over increasing intervals, while randomized jitter prevents the thundering herd.

---

## Motto
"Exponential backoff spreads retry attempts over increasing intervals, while randomized jitter prevents the thundering herd."

## Problem
When a service experiences an outage and recovers, 1,000 clients retrying at the exact same fixed interval immediately crash it again.

## Prediction
Multiplying delay by $2^n$ and adding randomized jitter decorrelates retry traffic, allowing services to recover safely.

## Why this matters
Backoff with jitter is the universal gold standard for resilient network communication.

## First principles
Delay = $\min(MaxDelay, BaseDelay \times 2^{attempt}) \times \text{random}(0.5, 1.5)$.

## Mental model
```text
Attempt 1: ~1s -> Attempt 2: ~2s -> Attempt 3: ~4s -> Attempt 4: ~8s (Jitter decorrelates traffic spike)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Tenacity retry configurations with `wait_random_exponential`.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/66-exponential-backoff-and-jitter/tests/ -v
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
- **Failure Injection**: Simulate 100 concurrent clients retrying simultaneously without jitter vs with jitter.
- Execute the experiment script:
```bash
python phases/66-exponential-backoff-and-jitter/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Without jitter: 100 requests hit simultaneously in spikes. With jitter: traffic is smoothly distributed across the timeline.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Full Jitter: $Sleep = \text{random}(0, \min(MaxDelay, Base \times 2^n))$. Proved by AWS to be optimal.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Retry storms can overwhelm network infrastructure and firewalls; jitter prevents packet synchronization.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Include `Retry-After` header values from upstream 429/503 responses into backoff calculations.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is a 'thundering herd' retry storm in distributed systems?
2. Why is exponential backoff alone insufficient without randomized jitter?
3. How does Full Jitter decorrelate synchronized client retries mathematically?

## What comes next
Having understood exponential backoff and jitter, we next discover its inherent boundaries and transition to **Circuit Breaker**.
