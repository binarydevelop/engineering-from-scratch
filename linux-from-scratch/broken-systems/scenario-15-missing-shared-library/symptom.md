# Binary Fails with 'error while loading shared libraries'

**Category**: Packages / Libraries  
**Severity**: Medium

---

## Incident Symptom & Ticket
```text
INCIDENT ALERT:
Running a custom compiled binary `/opt/bin/fastcalc` returns: `error while loading shared libraries: libmkl.so: cannot open shared object file: No such file or directory`.
```

---

## Triage Instructions
1. Reproduce the failure state by running `./setup.sh`.
2. Do **NOT** reboot the host.
3. Do **NOT** blindly run commands with `sudo` or execute `chmod 777`.
4. Inspect the underlying Linux state to find definitive proof.
5. Formulate a hypothesis, apply the fix, and run `./verify.sh`.
