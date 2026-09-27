# Experiment 04: Deadline Propagation and Resource Exhaustion in Call Chains

## 1. Chaos Experiment Thesis
> Simulate a 3-tier microservice call chain where client timeouts occur, comparing systems without deadline propagation (wasted work) against deadline-aware cancellation.

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: Wasted Work Cascades: Upstream clients time out and cancel HTTP requests, but downstream servers continue executing long-running database queries and RPCs.
- **Verification Metric**: Downstream execution time: Non-deadline-aware executes 500ms wasted work; deadline-aware aborts immediately when remaining budget <= 0.

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
