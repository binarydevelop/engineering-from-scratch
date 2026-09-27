# Experiment 03: Downstream Degradation, Retry Storms, and Circuit Breaker Defense

## 1. Chaos Experiment Thesis
> Induce latency in a downstream service and demonstrate how unjittered immediate retries cause exponential traffic multiplication vs Circuit Breaker containment.

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: Retry Storm: Failing or slow services receive amplified request volume from naive retry loops, converting a mild transient slowdown into total systemic collapse.
- **Verification Metric**: Total requests fired: Naive retry generates 4x load; Circuit Breaker trips to OPEN after threshold failures and drops downstream traffic to 0.

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
