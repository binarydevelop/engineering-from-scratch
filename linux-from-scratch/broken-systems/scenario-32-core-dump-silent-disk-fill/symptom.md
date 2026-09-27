# Silent Disk Saturation in /var/lib/systemd/coredump

**Category**: Storage / Systemd  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Disk space is dwindling by 2GB every hour. No large log files are visible in `/var/log`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
