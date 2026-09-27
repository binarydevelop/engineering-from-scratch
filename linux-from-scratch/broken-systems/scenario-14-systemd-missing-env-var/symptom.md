# Service Works Manually But Fails Under Systemd

**Category**: Services / Environment  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Running `/usr/local/bin/api_server` directly from the bash terminal succeeds. Starting it via `systemctl start api_server` fails immediately with `KeyError: 'DATABASE_URL'`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
