# Project: OIDC Short-Lived Workload Identity Federation (Phase 211)

## 1. Project Goal
Eliminate static long-lived cloud credentials from CI repository secrets by implementing OpenID Connect (OIDC) token exchange.

---

## 2. Core Architectural Deliverables
- [ ] OIDC token request and claim verification engine
- [ ] Cloud Security Token Service (STS) trust policy matching repository and branch
- [ ] Short-lived session token issuance (15-minute TTL)
- [ ] Rejection tests for untrusted fork pull requests

---

## 3. Verification Command
To verify your project implementation, execute:
```bash
python3 projects/06-oidc-deployment/verify.py
```
