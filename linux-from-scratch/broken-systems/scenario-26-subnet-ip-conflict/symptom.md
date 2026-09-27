# Intermittent Packet Loss and Flapping SSH Connections

**Category**: Networking / ARP  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
SSH connection disconnects every 30 seconds. Ping packet loss is ~50%. Running `arping` shows conflicting responses.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
