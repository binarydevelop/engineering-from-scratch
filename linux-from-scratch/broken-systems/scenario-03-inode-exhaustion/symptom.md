# No Space Left on Device Despite 50GB Free Space

**Category**: Storage / Inodes  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Application crashes with `IOError: [Errno 28] No space left on device`. Running `df -h` shows 52GB of free disk space. Why is file creation failing?
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
