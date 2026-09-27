# Capstone 2: Continuous Delivery & Environment Promotion

## 1. Challenge Prompt
> "Implement a full Continuous Delivery pipeline where the same immutable artifact is promoted from CI -> Registry -> Staging -> Smoke Tests -> Production Approval -> Production, recording a complete auditable release ledger."

---

## 2. Architectural Requirements & Invariants
- [ ] Build Once principle strictly enforced across dev, staging, and production
- [ ] Staging environment deployed automatically on merge to main
- [ ] Automated smoke tests probe liveness, readiness, and contract schema
- [ ] Production gate requires explicit authorized approval
- [ ] Complete release manifest records Git SHA, artifact digest, SBOM, and provenance

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/02-continuous-delivery/verify.py
```
