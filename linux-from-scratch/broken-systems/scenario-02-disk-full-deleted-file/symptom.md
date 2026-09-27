# Disk 100% Full But du Shows Empty Space

**Category**: Storage / VFS  
**Severity**: Critical

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Alert fires: `/tmp/lfs-lab/mnt` is 100% full (`df -h`). However, running `du -sh /tmp/lfs-lab/mnt` reports only 12KB of files! New file creation fails with `No space left on device`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
