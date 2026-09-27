# Project: Declarative GitOps Delivery with Argo CD Reconciler (Phase 215)

## 1. Project Goal
Implement pull-based GitOps software delivery where cluster state continuously reconciles toward version-controlled desired state.

---

## 2. Core Architectural Deliverables
- [ ] Separate Application and Configuration repository structure
- [ ] Local GitOps reconciler engine detecting drift between Git and live cluster
- [ ] Automated sync and out-of-band drift correction
- [ ] Safeguards against hazardous force-replace sync options

---

## 3. Verification Command
To verify your project implementation, execute:
```bash
python3 projects/10-gitops-delivery/verify.py
```
