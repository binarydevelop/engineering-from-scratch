# All HTTPS Connections Fail with SSL Certificate Errors

**Category**: Time / TLS  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
`curl https://github.com` fails with: `SSL certificate problem: certificate has expired or is not yet valid`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
