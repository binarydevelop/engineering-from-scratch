# Single CPU Core Pinned at 100% Load

**Category**: Performance / CPU  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
System load average spikes to 1.00 on a single-core VM. Top shows process `worker.py` consuming 99.8% CPU in user mode (`us`).
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
