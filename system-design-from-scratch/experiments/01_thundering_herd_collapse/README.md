# Experiment 01: Thundering Herd Cache Stampede and Coalescing Defense

## 1. Chaos Experiment Thesis
> Simulate what happens when a hot cache key expires under 1,000 concurrent requests, comparing unprotected cache-aside against Singleflight mutex coalescing.

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: Cache Stampede: Simultaneous cache misses by hundreds of concurrent threads flood the underlying database, causing thread exhaustion, high latency, and cascading failure.
- **Verification Metric**: Number of database queries executed for 500 concurrent requests on an expired key (500 without singleflight vs 1 with singleflight).

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
