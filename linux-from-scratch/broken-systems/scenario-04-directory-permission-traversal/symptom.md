# Permission Denied Reading Existing File Owned by User

**Category**: Permissions / DAC  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
User `deploy` tries to read `/data/apps/prod/settings.env`. The file permissions are `-rw-r--r-- deploy deploy`. Yet running `cat /data/apps/prod/settings.env` produces `cat: Permission denied`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
