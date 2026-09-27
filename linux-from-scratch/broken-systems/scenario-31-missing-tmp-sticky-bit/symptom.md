# Users Able to Delete Other Users' Temporary Files

**Category**: Security / Permissions  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
User `alice` creates `/tmp/alice_task.pid`. User `bob` is able to run `rm /tmp/alice_task.pid` and delete it without permission errors!
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
