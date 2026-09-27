# Experiment 05: Asynchronous Replication Lag and Read-Your-Own-Writes

## 1. Chaos Experiment Thesis
> Simulate a read replica with 300ms replication delay and test how session-based Read-Your-Own-Writes routing prevents user-visible stale data anomalies.

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: Read-After-Write Inconsistency: User updates profile/creates an order, is redirected to the view page, reads from a lagging replica, and sees stale pre-update state.
- **Verification Metric**: Stale read rate: Random replica routing yields 100% stale reads during lag window; sticky session / LSN token routing yields 0% stale reads.

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
