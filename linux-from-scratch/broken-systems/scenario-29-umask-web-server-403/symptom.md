# Uploaded Files Result in HTTP 403 Forbidden

**Category**: Permissions / Web Server  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Users upload images to `/var/www/uploads`. Nginx returns `403 Forbidden` when serving them. The directory permissions are `0755`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
