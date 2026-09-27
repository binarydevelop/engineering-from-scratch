# Experiment 06: Multi-Tenant Noisy Neighbor Starvation and Fair Quotas

## 1. Chaos Experiment Thesis
> Simulate a multi-tenant service where an abusive tenant floods the queue, comparing unmetered shared queues against Per-Tenant Token Bucket rate limiting.

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: Noisy Neighbor Starvation: A single rogue or high-volume tenant consumes 100% of shared worker threads, denying service to well-behaved tenants.
- **Verification Metric**: Well-behaved tenant success rate: 12% under shared unmetered queue vs 100% under isolated per-tenant token bucket rate limiting.

## 3. Experiment Procedure
1. **Normal Baseline**: System operates under steady-state load with expected latency and 0% errors.
2. **Failure Injection**: Inject the targeted fault (network partition, cache expiration, downstream latency, or noisy neighbor flood).
3. **Observation**: Measure system degradation (error rate, queue depth, database query spike).
4. **Defense Activation**: Enable the resilience pattern (singleflight, majority quorum, circuit breaker, deadline cancellation, sticky routing, or token bucket).
5. **Recovery Verification**: Measure metrics to verify stability has been restored.

## 4. Running the Experiment

Run directly:
```bash
python experiment.py
```

Run test suite:
```bash
pytest tests/
```
