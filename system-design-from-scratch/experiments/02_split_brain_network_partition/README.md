# Experiment 02: Network Partition and Split-Brain Prevention via Quorum

## 1. Chaos Experiment Thesis
> Inject a network partition into a 5-node distributed cluster, isolating 3 nodes from 2 nodes, and verify that split-brain is prevented through majority quorum.

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: Split-Brain: Two disconnected partitions both believe they are the authoritative cluster leader, accepting conflicting writes that permanently corrupt data.
- **Verification Metric**: Majority partition (3 nodes) accepts writes; minority partition (2 nodes) fences itself and rejects writes.

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
