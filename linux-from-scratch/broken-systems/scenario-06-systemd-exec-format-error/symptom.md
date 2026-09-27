# Service Fails Instantly with Exit Code 203/EXEC

**Category**: Services / systemd  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
A newly deployed service `lfs-worker.service` fails to start. `systemctl status` reports: `Active: failed (Result: exit-code)` with `Process: 1421 ExecStart=/opt/worker.sh (code=exited, status=203/EXEC)`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
