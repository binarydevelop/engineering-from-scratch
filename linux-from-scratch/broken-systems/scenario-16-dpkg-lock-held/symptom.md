# Package Manager Blocked by Stale Lock File

**Category**: Package Management  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Running `apt-get install htop` fails with: `E: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 3241 (unattended-upgr)`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
