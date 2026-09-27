# Project: Central Reusable Workflow Delivery Platform (Phase 213)

## 1. Project Goal
Centralize delivery logic across 30 microservices using versioned GitHub Actions reusable workflows and golden templates.

---

## 2. Core Architectural Deliverables
- [ ] Versioned reusable workflow (`reusable-build.yml`) with strict inputs/outputs
- [ ] Golden Pipeline template (`golden-pipeline.yml`) providing standard delivery
- [ ] Deprecation and version pinning strategy preventing cascading breaks
- [ ] Local test harness proving reusable workflow invocation

---

## 3. Verification Command
To verify your project implementation, execute:
```bash
python3 projects/08-reusable-pipeline-platform/verify.py
```
