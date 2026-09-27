# Single Log File Saturates 100GB Root Partition

**Category**: Logging / Storage  
**Severity**: Critical

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
The root partition reached 100% capacity. `du -ahx /var/log | sort -rh | head -5` reveals `/var/log/app/trace.log` is 92 Gigabytes!
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
