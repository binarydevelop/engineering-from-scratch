# Capstone 5: Enterprise GitOps Platform with Argo CD

## 1. Challenge Prompt
> "Construct a multi-service declarative GitOps platform separating application source repositories from deployment configuration repositories, featuring automated sync, out-of-band drift detection, and safe sync policies."

---

## 2. Architectural Requirements & Invariants
- [ ] Application repo pushes images to OCI registry and updates Config repo via PR
- [ ] In-cluster reconciler synchronizes live Kubernetes cluster state
- [ ] Drift detector catches manual 'kubectl' edits and alerts or restores Git state
- [ ] Hazardous flags (`--replace`, `--force`) strictly forbidden by policy
- [ ] GitOps rollback executed via Git revert commit

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/05-gitops-platform/verify.py
```
