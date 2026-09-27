# Capstone 7: Delivery Failure Day (Chaos Simulation)

## 1. Challenge Prompt
> "Execute a full-scale delivery failure drill. Deliberately break 10 critical systems across the delivery lifecycle: Git provider outage, runner saturation, dependency registry 429, test flakiness, corrupted artifact, OIDC expiration, Kubernetes probe timeout, broken DB migration, GitOps drift war, and canary regression."

---

## 2. Architectural Requirements & Invariants
- [ ] Simulate each of the 10 real-world failure scenarios
- [ ] Collect diagnostic evidence from logs and exit codes before attempting fixes
- [ ] Execute documented recovery runbooks
- [ ] Calculate Mean Time to Recovery (MTTR) for each incident
- [ ] Produce an incident post-mortem with preventive guardrails

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/07-delivery-failure-day/verify.py
```
