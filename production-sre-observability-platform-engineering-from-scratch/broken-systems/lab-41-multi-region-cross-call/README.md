# Lab 41: lab-41-multi-region-cross-call

## Domain: Networking
## Symptom: Service in us-west synchronously calls database in eu-central

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Service in us-west synchronously calls database in eu-central**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
