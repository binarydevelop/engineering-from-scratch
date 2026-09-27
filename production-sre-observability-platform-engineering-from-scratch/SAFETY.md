# Production & Chaos Safety Guide

> **Motto**: Never experiment without an abort condition; never break systems without a blast radius; never simulate failure without a recovery guarantee.

---

## 1. The Cardinal Rule of Production & Chaos Engineering

Chaos engineering is NOT random sabotage or cowboy testing. It is the disciplined empirical validation of system resilience hypotheses under strictly bounded failure domains.

Every experiment, load test, failure injection, and incident simulation in this repository MUST comply with the **Five Safety Invariants**:

```text
1. Predefined Hypothesis: Know exactly what state transition is expected before breaking anything.
2. Bounded Blast Radius: The experiment must run only in isolated lab containers or ephemeral environments.
3. Automated Abort Condition: Immediate programmatic termination if safety thresholds are breached.
4. Guaranteed Recovery Path: A verifiable mechanism to restore normal operation in seconds.
5. Evidence Collection: Every run must produce timestamped metrics, logs, traces, and state diffs.
```

---

## 2. Blast Radius Containment

All exercises in this repository are designed for **Tier 1 (Local Docker Compose)** and **Tier 2 (Local Disposable Kubernetes)**:

* **Docker Network Isolation**: Labs communicate over isolated user-defined Docker bridges (`sre-lab-net`). They do NOT bind to public host interfaces or bridge to corporate intranets.
* **Process Confinement**: CPU and memory pressure scripts execute inside containers with enforced cgroup constraints (`cpus: "1.0"`, `mem_limit: 512m`) or through disposable local processes with OS resource rlimits (`RLIMIT_AS`, `RLIMIT_CPU`).
* **Filesystem Safety**: Disk pressure tests allocate sparse files or write exclusively to ephemeral scratch volumes (`/tmp/lab-scratch`), never the host root partition.

---

## 3. The Chaos Experiment Safety Contract

Before running any script in `chaos/` or simulating any scenario in `incidents/`:

```bash
# 1. Verify baseline health
make health-check

# 2. Confirm your abort trigger
# E.g., if checkout error rate > 50% for 30s, automatically abort:
./chaos/latency_injector.py --service payment-service --abort-error-threshold 0.50

# 3. Emergency stop (always available)
make emergency-stop
# Or:
./scripts/reset-lab.sh
```

---

## 4. Cloud Safety Invariants (Tier 3 Optional)

If deploying optional cloud scenarios (AWS / GCP / Azure):
1. **Cost Caps**: Never run without budget alerts enabled.
2. **Ephemeral Tags**: Tag every cloud resource with `Lab=ProductionSRE` and `Expires=<Timestamp>`.
3. **Automated Destruction**: Always run the cleanup script and execute verification:
   ```bash
   make cloud-verify-clean
   ```

---

## 5. Security & Secret Hygiene

* **No Hardcoded Secrets**: Default development credentials (`sre_admin`, `reliable_production_secret_2026`) are provided strictly for local offline container demonstration. Never reuse them in any remote environment.
* **Telemetry Redaction**: Trace attributes and structured logs must NEVER record:
  - Credit card numbers / CVV
  - Bearer tokens or API keys
  - Plaintext passwords
  - Unsanitized raw SQL queries containing user payload data
