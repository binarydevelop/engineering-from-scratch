# Phases 148 – 157: Chaos & Failure Engineering

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 148: Why Inject Failures?

### Motto
"If you do not test your failure recovery paths, production will test them for you when you are asleep."

### The Chaos Invariant
Systems are non-linear complex networks. You cannot predict how connection pools, circuit breakers, and timeouts interact under stress through mental reasoning alone. You must execute controlled, empirical failure experiments.

---

## Phases 149 – 156: The Concrete Failure Experiments

### 1. Process Kill Failover (`SIGKILL`) (Phase 149)
```bash
docker compose kill payment-service
```
Observe how the API Gateway handles the sudden connection drop: Does it retry? Does it fail fast with HTTP 503, or does it hang for 30 seconds?

### 2. Dependency Latency Injection (Phase 150)
```bash
./scripts/inject-failure.sh payment-latency 1500
```
Observe:
* `checkout-service` p99 latency climbs to 1,500ms.
* Active requests gauge climbs from 5 to 45.
* If circuit breakers are configured, the breaker trips open after 5 requests, dropping p99 back down to 5ms with fast-failing HTTP 503!

### 3. CPU Saturation Stress (Phase 155)
```bash
./scripts/inject-failure.sh cpu-burn 30
```
Observe the correlation between host CPU utilization and histogram tail latency buckets in Prometheus.

---

## Phase 157: Formal Chaos Experiment Design

### The Chaos Contract
Every chaos experiment MUST define:
```text
1. HYPOTHESIS: "If payment-service latency increases to 1.5s, the checkout circuit breaker will trip within 10s, preventing gateway connection pool exhaustion."
2. BLAST RADIUS: Isolated to 'payment-service' container in local Tier 1 network.
3. ABORT CONDITION: If gateway error rate > 30% for > 20s, automatically abort fault.
4. EXPECTED BEHAVIOR: Error rate rises briefly, breaker trips, p99 drops, user cart is preserved.
5. CLEANUP: Clear latency injection and verify baseline health returns.
```
