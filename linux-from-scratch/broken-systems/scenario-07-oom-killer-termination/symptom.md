# Database Process Mysteriously Disappears without Trace

**Category**: Performance / Memory  
**Severity**: Critical

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
A Redis or PostgreSQL server process unexpectedly vanished. No crash dump was generated, and no log was written to the application log. The service simply stopped.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
