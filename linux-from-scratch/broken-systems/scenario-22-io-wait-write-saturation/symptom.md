# System Sluggish with High %wa in Top

**Category**: Performance / I/O  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
The terminal feels unresponsive. Running `top` reveals CPU utilization is mostly `0.5% us, 1.2% sy, 89.4% wa`. Load average is climbing rapidly.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
