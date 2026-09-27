# Process Cannot be Killed Even with kill -9

**Category**: Kernel / Process States  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
An operator attempts `kill -9 4812`, but the process continues to appear in `ps aux`. State code is `D`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
