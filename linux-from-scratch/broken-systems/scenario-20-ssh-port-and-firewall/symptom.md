# SSH Connection Refused After Port Change

**Category**: Networking / SSH  
**Severity**: Critical

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
An administrator edited `/etc/ssh/sshd_config` to change the port to `2222` and restarted `ssh`. Connecting via `ssh user@host` hangs and times out.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
