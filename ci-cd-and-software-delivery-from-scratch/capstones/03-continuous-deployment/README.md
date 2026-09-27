# Capstone 3: Continuous Deployment with Automated Safety Guardrails

## 1. Challenge Prompt
> "Remove the manual human approval gate. Configure an automated Continuous Deployment pipeline that automatically deploys every verified commit to production while enforcing strict health probes and SLO guardrails."

---

## 2. Architectural Requirements & Invariants
- [ ] Zero human clicks required from Git push to production
- [ ] Pre-flight database migration compatibility check
- [ ] Automated post-deployment verification against live traffic endpoints
- [ ] Instant automated rollback triggered if error budget is exceeded
- [ ] Delivery telemetry recorded in deployment ledger

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/03-continuous-deployment/verify.py
```
