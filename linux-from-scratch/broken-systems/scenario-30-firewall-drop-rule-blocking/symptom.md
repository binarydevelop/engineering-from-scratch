# Web Server Running and Listening But Inaccessible

**Category**: Networking / Firewall  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
`systemctl status nginx` is active. `ss -lntp` shows port 80 and 443 listening on `0.0.0.0`. Yet clients cannot connect.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
