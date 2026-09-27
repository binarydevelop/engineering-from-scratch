# Solution: Broken Pipeline Lab 19 — Readiness Probe Timeout Causes Rolling Deployment Deadlock

## 1. Root Cause Analysis
Readiness probe endpoint `/health/readiness` had a 1-second timeout, but application startup required 2.5 seconds to establish DB connection pool.

---

## 2. Step-by-Step Fix
Configure `initialDelaySeconds: 5` and increase probe timeout to accommodate realistic cold startup.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/19-failing-readiness-probe-causes-deploy-loop/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Benchmark application cold-start latency under realistic CPU constraints.
