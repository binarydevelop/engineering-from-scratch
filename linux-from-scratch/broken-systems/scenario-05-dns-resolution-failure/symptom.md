# Host Cannot Reach External APIs via Hostname

**Category**: Networking / DNS  
**Severity**: High

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Curl command `curl https://api.stripe.com` fails immediately with `curl: (6) Could not resolve host: api.stripe.com`. However, `ping 8.8.8.8` works flawlessly!
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
