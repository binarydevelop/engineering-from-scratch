# Capstone 6: Internal Developer Platform & Golden Pipeline

## 1. Challenge Prompt
> "Act as a Platform Delivery Engineer. Create a repository template and Golden Pipeline that allows internal developers to spin up a new microservice with automated lint, test, build, scan, artifact, and deployment in under 5 minutes."

---

## 2. Architectural Requirements & Invariants
- [ ] Zero copy-pasted 500-line YAML workflows in application repos
- [ ] Centrally versioned reusable workflow (`reusable-build.yml@v1`)
- [ ] Minimal configuration surface: developer provides only service path and test command
- [ ] Organizational policy enforcement (tests mandatory, image must be signed)
- [ ] Self-service onboarding documentation

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/06-platform-engineering/verify.py
```
