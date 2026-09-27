# Cron Job Fails Silently Due to Minimal PATH

**Category**: Automation / Cron  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
A maintenance script runs perfectly when executed in bash, but fails every midnight under cron with `command not found: aws`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
