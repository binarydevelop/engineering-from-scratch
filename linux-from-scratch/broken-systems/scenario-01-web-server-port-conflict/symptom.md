# Web Server Fails to Bind: Address Already in Use

**Category**: Networking / Sockets  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
The production API server fails to start with error: `[Errno 98] Address already in use: 0.0.0.0:8080`. No web server process appears in `ps aux | grep nginx`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
