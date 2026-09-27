# Filesystem Suddenly Re-mounted as Read-Only

**Category**: Storage / Recovery  
**Severity**: Critical

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
All disk write operations fail across `/var`: `Read-only file system`. `dmesg` shows I/O barrier errors.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
