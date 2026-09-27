# Application Fails to Write Database Files

**Category**: Permissions / Ownership  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Database engine runs as dedicated user `postgres`. On startup, it reports: `FATAL: could not create lock file 'postmaster.pid': Permission denied`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
