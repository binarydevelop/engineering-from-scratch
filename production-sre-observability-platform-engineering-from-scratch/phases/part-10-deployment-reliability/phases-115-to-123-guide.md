# Phases 115 – 123: Deployment Reliability & Change Safety

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phases 115 – 119: Change Risk, Probes & Graceful Shutdown

### Health Checks Matrix (Phase 116)
```text
┌─────────────────┬──────────────────────────────────────────┬───────────────────────────────────────┐
│ Probe Type      │ When it Runs                             │ Failure Action                        │
├─────────────────┼──────────────────────────────────────────┼───────────────────────────────────────┤
│ **startup**     │ On container boot until first success    │ Kills container if timeout exceeded   │
│ **readiness**   │ Continuous (every 5-10s)                 │ Removes pod from Load Balancer pool   │
│ **liveness**    │ Continuous (only after startup passes)   │ Sends SIGKILL and restarts container  │
└─────────────────┴──────────────────────────────────────────┴───────────────────────────────────────┘
```

### Graceful Draining on SIGTERM (Phase 117)
```python
import signal, time, sys

def sigterm_handler(signum, frame):
    print("SIGTERM received. Stopping listener socket...")
    server.stop_accepting() # Remove from LB
    time.sleep(5)           # Allow in-flight requests to complete
    db_pool.close_all()     # Cleanly close DB sockets
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)
```

---

## Phases 120 – 123: Canaries, Blue/Green & Schema Evolution

### Canary Progressive Analysis (Phase 120)
1. Route 5% of production traffic to Canary pods (Image v1.4.2).
2. Measure Canary error rate vs Baseline error rate for 10 minutes.
3. If Canary error rate > Baseline error rate by $> 0.2\%$, trigger automatic rollback immediately.

### Zero-Downtime Database Schema Migration (Phase 123)
The **Expand and Contract Sequence**:
```text
Step 1: Add column 'email_normalized' (Nullable). Both old and new app versions work.
Step 2: Deploy code writing to BOTH 'email' and 'email_normalized'.
Step 3: Run background backfill script to populate existing rows.
Step 4: Deploy code reading exclusively from 'email_normalized'.
Step 5: Drop old column 'email'.
```
Never execute `ALTER TABLE ALTER COLUMN` with locks during peak business hours!
