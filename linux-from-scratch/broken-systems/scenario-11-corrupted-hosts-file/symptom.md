# Internal Microservice Connecting to Wrong Host

**Category**: Networking / Name Resolution  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
The billing backend cannot connect to `db.internal`. `ping db.internal` attempts to reach `10.99.99.99` instead of the actual database IP `10.0.1.50`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
