# Load Testing Suite

High-throughput, asynchronous load generation harness for backend services.

---

## 1. Principles of Load Testing
- **Concurrency vs Throughput**: Concurrency measures active in-flight requests; throughput (RPS) measures completed requests per unit of time.
- **Latency Percentiles (p50, p95, p99)**: Never rely on averages. In backends with multi-step fan-out, p99 dictates user experience.
- **Coordinated Omission**: Avoiding client-side backpressure that masks server degradation during saturation.

---

## 2. Directory Structure
- `load_test_runner.py`: Async load generator engine calculating throughput, error rates, and p50/p95/p99 percentiles.
- `scenarios/orders_spike.py`: High-concurrency flash-sale spike testing inventory race conditions and transactional consistency.
- `scenarios/read_heavy_traffic.py`: High-volume read-heavy traffic distribution (90% reads, 10% writes) testing cache hit performance.

---

## 3. Running Scenarios
```bash
python load-tests/scenarios/orders_spike.py
python load-tests/scenarios/read_heavy_traffic.py
```
