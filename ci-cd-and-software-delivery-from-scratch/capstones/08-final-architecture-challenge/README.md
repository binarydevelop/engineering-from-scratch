# Capstone 8: Final Enterprise CI/CD Architecture Challenge

## 1. Challenge Prompt
> "Design the end-to-end software delivery platform for an enterprise with 300 engineers, 100 microservices, Kubernetes clusters, multiple environments, strict compliance mandates, and a requirement to deploy safely dozens of times per day."

---

## 2. Architectural Requirements & Invariants
- [ ] Source event & webhook ingestion architecture
- [ ] Ephemeral runner fleet sizing & caching strategy
- [ ] Testing portfolio (unit, integration, contract, smoke) with SLA limits
- [ ] Build Once, Promote Many artifact lifecycle with SLSA Level 3 provenance
- [ ] OIDC short-lived credential federation with AWS/GCP (Zero static keys)
- [ ] Expand / Migrate / Contract zero-downtime database evolution
- [ ] Pull-based GitOps deployment with Argo CD and multi-environment separation
- [ ] Progressive canary traffic shifting with automated abort triggers
- [ ] DORA delivery metrics observability and pipeline SLOs

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/08-final-architecture-challenge/verify.py
```
