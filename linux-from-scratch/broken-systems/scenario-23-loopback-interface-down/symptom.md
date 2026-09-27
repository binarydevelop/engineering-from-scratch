# Local Sockets Fail with 'Network is unreachable'

**Category**: Networking / Interfaces  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Connecting to `localhost` or `127.0.0.1` fails instantly: `connect: Network is unreachable`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
