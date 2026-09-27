# Server Reaches Local Subnet but Cannot Reach Internet

**Category**: Networking / Routing  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
The server can ping other hosts on the `192.168.1.0/24` subnet, but pinging `8.8.8.8` returns `connect: Network is unreachable`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
